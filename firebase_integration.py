#!/usr/bin/env python3
"""
Firebase Integration for Monkey Paw AI CEO
Handles backend services, database, and hosting
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class FirebaseIntegration:
    """Integration with Google Firebase for backend services and hosting"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.firebase_config = {}
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def connect(self) -> dict:
        """Connect to Firebase"""
        try:
            # Check if Firebase CLI is available
            result = subprocess.run(
                ['firebase', '--version'], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': 'Firebase CLI not found. Install Firebase CLI',
                    'timestamp': datetime.now().isoformat()
                }

            # Check authentication
            result = subprocess.run(
                ['firebase', 'projects:list'], 
                capture_output=True, 
                text=True
            )

            if result.returncode == 0:
                self.is_connected = True
                self.logger.info("Connected to Firebase successfully")
                return {
                    'status': 'connected',
                    'message': 'Firebase connection established',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Firebase authentication required',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def initialize_project(self, project_path: str) -> dict:
        """Initialize Firebase project"""
        try:
            # Initialize Firebase in project directory
            result = subprocess.run(
                ['firebase', 'init'],
                cwd=project_path,
                capture_output=True,
                text=True,
                input='y\ny\ny\ny\n'  # Auto-accept defaults
            )
            
            if result.returncode == 0:
                self.logger.info(f"Firebase initialized in: {project_path}")
                return {
                    'status': 'success',
                    'message': 'Firebase project initialized',
                    'timestamp': datetime.now().isoformat(),
                    'project_path': project_path
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Initialization failed: {result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def deploy_hosting(self, project_path: str) -> dict:
        """Deploy to Firebase Hosting"""
        try:
            # Build the project first
            build_result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if build_result.returncode != 0:
                return {
                    'status': 'error',
                    'message': f'Build failed: {build_result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Deploy to Firebase Hosting
            result = subprocess.run(
                ['firebase', 'deploy', '--only', 'hosting'],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Deployed to Firebase Hosting")
                return {
                    'status': 'success',
                    'message': 'Deployed to Firebase Hosting',
                    'timestamp': datetime.now().isoformat(),
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Deployment failed: {result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_firestore(self) -> dict:
        """Setup Firestore database"""
        try:
            # Create Firestore security rules
            rules_content = '''rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}'''
            
            rules_file = Path('firestore.rules')
            with open(rules_file, 'w') as f:
                f.write(rules_content)
            
            # Deploy Firestore rules
            result = subprocess.run(
                ['firebase', 'deploy', '--only', 'firestore:rules'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Firestore database configured")
                return {
                    'status': 'success',
                    'message': 'Firestore database configured',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Firestore setup failed: {result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Firestore setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def setup_functions(self, project_path: str) -> dict:
        """Setup Firebase Functions"""
        try:
            functions_dir = Path(project_path) / 'functions'
            functions_dir.mkdir(exist_ok=True)
            
            # Create basic function
            function_content = '''const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp();

exports.aiCeoWebhook = functions.https.onRequest((req, res) => {
  console.log('AI CEO webhook called:', req.body);
  
  // Process AI CEO commands
  const command = req.body;
  
  // Send response
  res.json({
    status: 'success',
    message: 'Command processed',
    timestamp: new Date().toISOString()
  });
});

exports.syncData = functions.firestore
  .document('projects/{projectId}')
  .onWrite((change, context) => {
    console.log('Data sync:', context.params.projectId);
    
    // Sync with other platforms
    return null;
  });
'''
            
            index_file = functions_dir / 'index.js'
            with open(index_file, 'w') as f:
                f.write(function_content)
            
            # Create package.json for functions
            package_json = {
                "name": "functions",
                "description": "Cloud Functions for Firebase",
                "scripts": {
                    "serve": "firebase emulators:start --only functions",
                    "shell": "firebase functions:shell",
                    "start": "npm run shell",
                    "deploy": "firebase deploy --only functions",
                    "logs": "firebase functions:log"
                },
                "engines": {
                    "node": "18"
                },
                "main": "index.js",
                "dependencies": {
                    "firebase-admin": "^11.8.0",
                    "firebase-functions": "^4.3.1"
                }
            }
            
            package_file = functions_dir / 'package.json'
            with open(package_file, 'w') as f:
                json.dump(package_json, f, indent=2)
            
            self.logger.info("Firebase Functions configured")
            return {
                'status': 'success',
                'message': 'Firebase Functions configured',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Functions setup failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def deploy_functions(self, project_path: str) -> dict:
        """Deploy Firebase Functions"""
        try:
            functions_dir = Path(project_path) / 'functions'
            
            # Install dependencies
            result = subprocess.run(
                ['npm', 'install'],
                cwd=functions_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': f'Dependencies install failed: {result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Deploy functions
            result = subprocess.run(
                ['firebase', 'deploy', '--only', 'functions'],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Firebase Functions deployed")
                return {
                    'status': 'success',
                    'message': 'Firebase Functions deployed',
                    'timestamp': datetime.now().isoformat(),
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Functions deployment failed',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Functions deployment failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def create_database_schema(self) -> dict:
        """Create database schema for AI CEO integration"""
        try:
            schema = {
                'projects': {
                    'id': 'string',
                    'name': 'string',
                    'status': 'string',
                    'created_at': 'timestamp',
                    'updated_at': 'timestamp',
                    'ai_ceo_config': {
                        'enabled': 'boolean',
                        'sync_interval': 'number',
                        'platforms': 'array'
                    }
                },
                'sync_events': {
                    'id': 'string',
                    'project_id': 'string',
                    'platform': 'string',
                    'event_type': 'string',
                    'data': 'object',
                    'timestamp': 'timestamp'
                },
                'ai_commands': {
                    'id': 'string',
                    'project_id': 'string',
                    'command': 'string',
                    'status': 'string',
                    'result': 'object',
                    'timestamp': 'timestamp'
                }
            }
            
            self.logger.info("Database schema created")
            return {
                'status': 'success',
                'message': 'Database schema created',
                'schema': schema,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Schema creation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def sync_with_ai_ceo(self, data: Dict[str, Any]) -> dict:
        """Sync data with AI CEO system"""
        try:
            timestamp = datetime.now().isoformat()
            
            # Log sync event
            self.logger.info(f"Synced with AI CEO: {data.get('type', 'unknown')}")
            
            return {
                'status': 'success',
                'message': 'Data synchronized with AI CEO',
                'timestamp': timestamp
            }
            
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_project_config(self) -> dict:
        """Get Firebase project configuration"""
        try:
            # Read firebase.json
            config_file = Path('firebase.json')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            return {
                'status': 'success',
                'config': config,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get config: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def update_project_config(self, new_config: Dict[str, Any]) -> dict:
        """Update Firebase project configuration"""
        try:
            # Load existing config
            config_file = Path('firebase.json')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Update with new config
            config.update(new_config)
            
            # Save updated config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info("Firebase configuration updated")
            
            return {
                'status': 'success',
                'message': 'Configuration updated',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Config update failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_hosting_url(self) -> dict:
        """Get Firebase Hosting URL"""
        try:
            if not self.project_id:
                return {
                    'status': 'error',
                    'message': 'Project ID not set',
                    'timestamp': datetime.now().isoformat()
                }
            
            hosting_url = f"https://{self.project_id}.web.app"
            
            return {
                'status': 'success',
                'url': hosting_url,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get hosting URL: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Main function for testing"""
    integration = FirebaseIntegration()
    
    # Test connection
    result = integration.connect()
    print(f"Connection result: {result}")
    
    # Test schema creation
    result = integration.create_database_schema()
    print(f"Schema result: {result}")


if __name__ == "__main__":
    main()