"""
Real-time Sync Manager
Coordinates synchronization between Cursor, Bolt.diy, Firebase, and Trae.ai
"""

import asyncio
import json
import logging
import threading
from datetime import datetime
from typing import Dict, Callable
import websockets


class SyncManager:
    """Manages real-time synchronization across all platforms"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.platforms = {}
        self.sync_queue = asyncio.Queue()
        self.subscribers = []
        self.is_running = False
        self.sync_thread = None
        self.websocket_server = None
        
    def register_platform(self, name: str, integration_instance):
        """Register a platform integration"""
        self.platforms[name] = {
            'instance': integration_instance,
            'last_sync': None,
            'status': 'registered'
        }
        self.logger.info(f"Platform registered: {name}")
    
    def subscribe(self, callback: Callable):
        """Subscribe to sync events"""
        self.subscribers.append(callback)
    
    async def start_sync_service(self):
        """Start the real-time sync service"""
        self.is_running = True
        
        # Start WebSocket server for real-time updates
        self.websocket_server = await websockets.serve(
            self.handle_websocket_connection,
            "localhost",
            8001
        )
        
        # Start sync processing loop
        asyncio.create_task(self.process_sync_queue())
        
        self.logger.info("Sync service started on ws://localhost:8001")
    
    async def handle_websocket_connection(self, websocket, path):
        """Handle WebSocket connections for real-time updates"""
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_sync_event(data)
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.logger.error(f"WebSocket error: {str(e)}")
    
    async def handle_sync_event(self, event_data: dict):
        """Handle incoming sync events"""
        try:
            event_data['timestamp'] = datetime.now().isoformat()
            await self.sync_queue.put(event_data)
            
            # Notify subscribers
            for callback in self.subscribers:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event_data)
                    else:
                        callback(event_data)
                except Exception as e:
                    self.logger.error(f"Subscriber callback error: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"Sync event handling error: {str(e)}")
    
    async def process_sync_queue(self):
        """Process sync events from the queue"""
        while self.is_running:
            try:
                # Wait for sync event
                event = await asyncio.wait_for(
                    self.sync_queue.get(), 
                    timeout=1.0
                )
                
                await self.distribute_sync_event(event)
                
            except asyncio.TimeoutError:
                # Check platform health periodically
                await self.check_platform_health()
            except Exception as e:
                self.logger.error(f"Sync processing error: {str(e)}")
    
    async def distribute_sync_event(self, event: dict):
        """Distribute sync event to relevant platforms"""
        source_platform = event.get('source_platform')
        event_type = event.get('type')
        
        for platform_name, platform_info in self.platforms.items():
            if platform_name == source_platform:
                continue  # Don't sync back to source
                
            try:
                instance = platform_info['instance']
                
                # Route event based on type
                if event_type == 'file_changed':
                    await self.sync_file_change(instance, event)
                elif event_type == 'project_updated':
                    await self.sync_project_update(instance, event)
                elif event_type == 'deployment_status':
                    await self.sync_deployment_status(instance, event)
                elif event_type == 'ai_suggestion':
                    await self.sync_ai_suggestion(instance, event)
                
                platform_info['last_sync'] = datetime.now()
                
            except Exception as e:
                self.logger.error(
                    f"Failed to sync to {platform_name}: {str(e)}"
                )
    
    async def sync_file_change(self, instance, event):
        """Sync file changes across platforms"""
        if hasattr(instance, 'handle_file_change'):
            await instance.handle_file_change(event)
    
    async def sync_project_update(self, instance, event):
        """Sync project updates across platforms"""
        if hasattr(instance, 'handle_project_update'):
            await instance.handle_project_update(event)
    
    async def sync_deployment_status(self, instance, event):
        """Sync deployment status across platforms"""
        if hasattr(instance, 'handle_deployment_status'):
            await instance.handle_deployment_status(event)
    
    async def sync_ai_suggestion(self, instance, event):
        """Sync AI suggestions across platforms"""
        if hasattr(instance, 'handle_ai_suggestion'):
            await instance.handle_ai_suggestion(event)
    
    async def check_platform_health(self):
        """Check health of all registered platforms"""
        for platform_name, platform_info in self.platforms.items():
            try:
                instance = platform_info['instance']
                
                if hasattr(instance, 'get_status'):
                    status = instance.get_status()
                    platform_info['status'] = status.get('connected', False)
                    
            except Exception as e:
                self.logger.error(
                    f"Health check failed for {platform_name}: {str(e)}"
                )
                platform_info['status'] = 'error'
    
    def trigger_sync(self, event_data: dict):
        """Trigger a sync event (thread-safe)"""
        if self.is_running:
            asyncio.run_coroutine_threadsafe(
                self.handle_sync_event(event_data),
                asyncio.get_event_loop()
            )
    
    def get_sync_status(self) -> dict:
        """Get current sync status"""
        platform_status = {}
        
        for name, info in self.platforms.items():
            platform_status[name] = {
                'status': info['status'],
                'last_sync': (
                    info['last_sync'].isoformat() 
                    if info['last_sync'] else None
                )
            }
        
        return {
            'service_running': self.is_running,
            'platforms': platform_status,
            'queue_size': (
                self.sync_queue.qsize() if self.sync_queue else 0
            ),
            'subscribers': len(self.subscribers)
        }
    
    def stop_sync_service(self):
        """Stop the sync service"""
        self.is_running = False
        
        if self.websocket_server:
            self.websocket_server.close()
        
        self.logger.info("Sync service stopped")


class PlatformSyncAdapter:
    """Base adapter for platform-specific sync handling"""
    
    def __init__(self, platform_name: str, sync_manager: SyncManager):
        self.platform_name = platform_name
        self.sync_manager = sync_manager
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")
    
    def emit_sync_event(self, event_type: str, data: dict):
        """Emit a sync event to other platforms"""
        event = {
            'source_platform': self.platform_name,
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.sync_manager.trigger_sync(event)
        self.logger.info(f"Sync event emitted: {event_type}")
    
    async def handle_file_change(self, event: dict):
        """Handle file change from another platform"""
        self.logger.info(f"File change received: {event.get('data', {})}")
    
    async def handle_project_update(self, event: dict):
        """Handle project update from another platform"""
        self.logger.info(f"Project update received: {event.get('data', {})}")
    
    async def handle_deployment_status(self, event: dict):
        """Handle deployment status from another platform"""
        self.logger.info(f"Deployment status: {event.get('data', {})}")
    
    async def handle_ai_suggestion(self, event: dict):
        """Handle AI suggestion from another platform"""
        self.logger.info(f"AI suggestion received: {event.get('data', {})}")


# Global sync manager instance
sync_manager = SyncManager()


def initialize_sync_system(platforms: Dict):
    """Initialize the sync system with platform integrations"""
    for name, instance in platforms.items():
        sync_manager.register_platform(name, instance)
    
    # Start sync service in background thread
    def run_sync_service():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(sync_manager.start_sync_service())
        loop.run_forever()
    
    sync_thread = threading.Thread(target=run_sync_service, daemon=True)
    sync_thread.start()
    
    return sync_manager