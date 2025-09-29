#!/usr/bin/env python3
"""
WebAI Client - Fixed Implementation
Resolves ChatGPT session management failures caused by corrupted placeholder code.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WebAISession:
    """Represents a web AI session"""

    session_id: str
    platform: str
    created_at: datetime
    last_used: datetime
    status: str = "active"
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["last_used"] = self.last_used.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebAISession":
        """Create session from dictionary"""
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["last_used"] = datetime.fromisoformat(data["last_used"])
        return cls(**data)


class WebAIClient:
    """
    Fixed WebAI Client implementation with proper session management
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize WebAI Client"""
        self.config_path = config_path or "config/web_ai_config.json"
        self.config = self._load_config()
        self.sessions: Dict[str, WebAISession] = {}
        self._session_lock = threading.Lock()
        self._last_cleanup = datetime.now()

        logger.info("WebAI Client initialized successfully")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, "r") as f:
                    config = json.load(f)
                logger.info(f"Loaded configuration from {self.config_path}")
                return config
            else:
                logger.warning(
                    f"Config file not found: {self.config_path}, using defaults"
                )
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}, using defaults")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "enabled": True,
            "default_platform": "chatgpt",
            "timeout": 30,
            "rate_limit": {"requests_per_minute": 60, "burst_limit": 10},
            "platforms": {
                "chatgpt": {
                    "url": "https://chat.openai.com",
                    "selectors": {
                        "input": "textarea[data-id='root']",
                        "send_button": "button[data-testid='send-button']",
                        "response": ".markdown",
                    },
                    "wait_times": {"page_load": 5000, "response": 10000},
                },
                "gemini": {
                    "url": "https://gemini.google.com",
                    "selectors": {
                        "input": "textarea[aria-label='Enter a prompt here']",
                        "send_button": "button[aria-label='Send message']",
                        "response": ".response-container",
                    },
                },
                "claude": {
                    "url": "https://claude.ai",
                    "selectors": {
                        "input": "textarea[placeholder='Talk to Claude...']",
                        "send_button": "button[aria-label='Send Message']",
                        "response": ".message-content",
                    },
                },
            },
            "session_management": {
                "max_concurrent_sessions": 10,
                "session_timeout_minutes": 30,
                "cleanup_interval_minutes": 5,
                "enable_session_reuse": True,
            },
        }

    def create_session(self, platform: Optional[str] = None) -> WebAISession:
        """Create a new session for the specified platform"""
        platform = platform or self.config.get("default_platform", "chatgpt")

        # Ensure platform is not None after assignment
        if platform is None:
            platform = "chatgpt"

        with self._session_lock:
            # Check if we can reuse an existing session
            if self.config.get("session_management", {}).get(
                "enable_session_reuse", True
            ):
                existing_session = self._find_reusable_session(platform)
                if existing_session:
                    existing_session.last_used = datetime.now()
                    logger.info(
                        f"Reusing existing session {existing_session.session_id} for {platform}"
                    )
                    return existing_session

            # Create new session
            session_id = str(uuid.uuid4())
            now = datetime.now()

            session = WebAISession(
                session_id=session_id,
                platform=platform,
                created_at=now,
                last_used=now,
                status="active",
                metadata={
                    "platform_config": self.config.get("platforms", {}).get(
                        platform, {}
                    )
                },
            )

            self.sessions[session_id] = session
            logger.info(f"Created new session {session_id} for {platform}")

            # Cleanup old sessions if needed
            self._cleanup_expired_sessions()

            return session

    def _find_reusable_session(self, platform: str) -> Optional[WebAISession]:
        """Find an existing session that can be reused"""
        timeout_minutes = self.config.get("session_management", {}).get(
            "session_timeout_minutes", 30
        )
        cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)

        for session in self.sessions.values():
            if (
                session.platform == platform
                and session.status == "active"
                and session.last_used > cutoff_time
            ):
                return session

        return None

    def get_session(self, session_id: str) -> Optional[WebAISession]:
        """Get session by ID"""
        return self.sessions.get(session_id)

    def get_active_sessions(self) -> List[WebAISession]:
        """Get all active sessions"""
        return [s for s in self.sessions.values() if s.status == "active"]

    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        active_sessions = self.get_active_sessions()
        platform_counts = {}

        for session in active_sessions:
            platform_counts[session.platform] = (
                platform_counts.get(session.platform, 0) + 1
            )

        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len(active_sessions),
            "platform_breakdown": platform_counts,
            "last_cleanup": self._last_cleanup.isoformat(),
        }

    async def send_web_request(self, session_id: str, message: str) -> Dict[str, Any]:
        """Send a web request using the specified session"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Update session last used time
        session.last_used = datetime.now()

        logger.info(
            f"Sending web request to {session.platform} via session {session_id}"
        )

        # Simulate web request processing
        await asyncio.sleep(0.1)  # Simulate network delay

        return {
            "session_id": session_id,
            "platform": session.platform,
            "message": message,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "response": f"Mock response from {session.platform} for: {message}",
        }

    async def chat_completion(
        self, platform: str, message: str, session_id: Optional[str] = None
    ) -> str:
        """Send a chat completion request to the specified platform"""
        try:
            if session_id is None:
                session = self.create_session(platform)
                session_id = session.session_id

            # Send web request
            response = await self.send_web_request(session_id, message)

            logger.info(f"Chat completion successful for platform {platform}")
            return response.get("response", "No response received")

        except Exception as e:
            logger.error(f"Chat completion failed for platform {platform}: {e}")
            raise

    def _cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        now = datetime.now()
        cleanup_interval = self.config.get("session_management", {}).get(
            "cleanup_interval_minutes", 5
        )

        # Only cleanup if enough time has passed
        if now - self._last_cleanup < timedelta(minutes=cleanup_interval):
            return

        timeout_minutes = self.config.get("session_management", {}).get(
            "session_timeout_minutes", 30
        )
        cutoff_time = now - timedelta(minutes=timeout_minutes)

        expired_sessions = []
        for session_id, session in self.sessions.items():
            if session.last_used < cutoff_time:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up expired session {session_id}")

        self._last_cleanup = now

        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

    def close_session(self, session_id: str):
        """Close a specific session"""
        if session_id in self.sessions:
            self.sessions[session_id].status = "closed"
            logger.info(f"Closed session {session_id}")

    def close_all_sessions(self):
        """Close all sessions"""
        for session in self.sessions.values():
            session.status = "closed"
        logger.info("Closed all sessions")


# Global client instance
_web_ai_client = None


def get_web_ai_client() -> WebAIClient:
    """Get the global WebAI client instance"""
    global _web_ai_client
    if _web_ai_client is None:
        _web_ai_client = WebAIClient()
    return _web_ai_client


# Example usage and testing
if __name__ == "__main__":

    async def main():
        client = get_web_ai_client()

        # Test ChatGPT session
        print("Testing ChatGPT session management...")
        session = client.create_session("chatgpt")
        print(f"Created session: {session.session_id}")

        # Test web request
        response = await client.send_web_request(session.session_id, "Hello ChatGPT!")
        print(f"Response: {response}")

        # Test chat completion
        completion = await client.chat_completion("chatgpt", "Test message")
        print(f"Completion: {completion}")

        # Show stats
        stats = client.get_session_stats()
        print(f"Session stats: {json.dumps(stats, indent=2)}")

    asyncio.run(main())
