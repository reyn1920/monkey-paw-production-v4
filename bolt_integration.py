#!/usr/bin/env python3
"""
Bolt.diy Integration for Monkey Paw AI CEO
Handles rapid prototyping and deployment pipeline
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path


class BoltDIYIntegration:
    """Integration with Bolt.diy for rapid prototyping and deployment"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def connect(self) -> dict:
        """Connect to Bolt.diy platform"""
        try:
            # Check if bolt CLI is available
            result = subprocess.run(
                ['which', 'bolt'], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                return {
                    'status': 'error',
                    'message': 'Bolt CLI not found. Please install bolt-cli',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Test connection
            result = subprocess.run(
                ['bolt', 'status'], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Connected to Bolt.diy successfully")
                return {
                    'status': 'connected',
                    'message': 'Bolt.diy connection established',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to Bolt.diy',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def sync_project(self, project_path: str) -> dict:
        """Sync project with Bolt.diy"""
        try:
            # Initialize bolt project if not exists
            bolt_config = Path(project_path) / 'bolt.config.js'
            if not bolt_config.exists():
                self._initialize_bolt_project(project_path)
            
            # Sync files
            result = subprocess.run(
                ['bolt', 'sync'], 
                cwd=project_path,
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f"Project synced: {project_path}")
                return {
                    'status': 'success',
                    'message': 'Project synchronized with Bolt.diy',
                    'timestamp': datetime.now().isoformat(),
                    'project_path': project_path
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Sync failed: {result.stderr}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def create_rapid_prototype(self, template_type: str,
                               project_name: str) -> dict:
        """Create rapid prototype from template"""
        try:
            templates = {
                'react': self._create_react_template,
                'vue': self._create_vue_template,
                'html': self._create_html_template
            }
            
            if template_type not in templates:
                raise ValueError(f"Unknown template: {template_type}")
            
            # Create project directory
            project_path = Path(self.workspace_path) / project_name
            project_path.mkdir(exist_ok=True)
            
            # Generate template
            template_func = templates[template_type]
            template_func(project_path)
            
            self.logger.info(
                f"Created {template_type} prototype: {project_name}"
            )
            
            return {
                'status': 'success',
                'project_path': str(project_path),
                'template_type': template_type,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Prototype creation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def deploy_to_production(self, project_path: str) -> dict:
        """Deploy project to production using GitHub Actions"""
        try:
            # Create GitHub Actions workflow
            workflow_content = self._create_github_workflow()
            
            workflow_dir = Path(project_path) / '.github' / 'workflows'
            workflow_dir.mkdir(parents=True, exist_ok=True)
            
            workflow_file = workflow_dir / 'deploy.yml'
            with open(workflow_file, 'w') as f:
                f.write(workflow_content)
            
            # Commit and push to trigger deployment
            commands = [
                'git add .',
                'git commit -m "Add deployment workflow"',
                'git push origin main'
            ]
            
            for cmd in commands:
                result = subprocess.run(
                    cmd.split(), 
                    cwd=project_path, 
                    capture_output=True, 
                    text=True
                )
                if result.returncode != 0:
                    raise Exception(f"Command failed: {cmd}")
            
            return {
                'status': 'success',
                'message': 'Deployment workflow created and triggered',
                'timestamp': datetime.now().isoformat(),
                'workflow_file': str(workflow_file)
            }
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_deployment_status(self) -> dict:
        """Get current deployment status"""
        try:
            # Check GitHub Actions status
            result = subprocess.run(
                ['gh', 'run', 'list', '--limit', '1', '--json', 'status'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                runs = json.loads(result.stdout)
                if runs:
                    status = runs[0]['status']
                    return {
                        'status': 'success',
                        'deployment_status': status,
                        'timestamp': datetime.now().isoformat()
                    }
            
            return {
                'status': 'success',
                'deployment_status': 'unknown',
                'message': 'No recent deployments found',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Status check failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _initialize_bolt_project(self, project_path: str):
        """Initialize Bolt.diy project configuration"""
        config_content = """
module.exports = {
  framework: 'react',
  buildCommand: 'npm run build',
  outputDirectory: 'dist',
  installCommand: 'npm install',
  devCommand: 'npm run dev'
};
"""
        config_file = Path(project_path) / 'bolt.config.js'
        with open(config_file, 'w') as f:
            f.write(config_content)
    
    def _create_react_template(self, project_path: Path):
        """Create React template"""
        # Package.json
        package_json = {
            "name": project_path.name,
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^4.0.0",
                "vite": "^4.4.0"
            }
        }
        
        with open(project_path / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # Create basic React app structure
        src_dir = project_path / 'src'
        src_dir.mkdir(exist_ok=True)
        
        # App.jsx
        app_content = """
import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Bolt.diy React App</h1>
        <p>Created with Monkey Paw AI CEO</p>
      </header>
    </div>
  );
}

export default App;
"""
        with open(src_dir / 'App.jsx', 'w') as f:
            f.write(app_content)
        
        # main.jsx
        main_content = """
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
        with open(src_dir / 'main.jsx', 'w') as f:
            f.write(main_content)
        
        # index.html
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Bolt.diy React App</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>
"""
        with open(project_path / 'index.html', 'w') as f:
            f.write(html_content)
    
    def _create_vue_template(self, project_path: Path):
        """Create Vue template"""
        # Basic Vue setup
        package_json = {
            "name": project_path.name,
            "version": "1.0.0",
            "scripts": {
                "dev": "vite",
                "build": "vite build"
            },
            "dependencies": {
                "vue": "^3.3.0"
            },
            "devDependencies": {
                "@vitejs/plugin-vue": "^4.0.0",
                "vite": "^4.4.0"
            }
        }
        
        with open(project_path / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
    
    def _create_html_template(self, project_path: Path):
        """Create HTML template"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bolt.diy HTML App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bolt.diy HTML App</h1>
        <p>Created with Monkey Paw AI CEO</p>
    </div>
</body>
</html>
"""
        with open(project_path / 'index.html', 'w') as f:
            f.write(html_content)
    
    def _create_github_workflow(self) -> str:
        """Create GitHub Actions workflow for deployment"""
        return """name: Deploy to Production

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build project
      run: npm run build
    
    - name: Deploy to Netlify
      uses: nwtgck/actions-netlify@v2.0
      with:
        publish-dir: './dist'
        production-branch: main
        github-token: ${{ secrets.GITHUB_TOKEN }}
        deploy-message: "Deploy from GitHub Actions"
      env:
        NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
        NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
"""


def main():
    """Main function for testing"""
    integration = BoltDIYIntegration()
    
    # Test connection
    result = integration.connect()
    print(f"Connection result: {result}")
    
    # Test prototype creation
    result = integration.create_rapid_prototype('react', 'test-app')
    print(f"Prototype result: {result}")


if __name__ == "__main__":
    main()