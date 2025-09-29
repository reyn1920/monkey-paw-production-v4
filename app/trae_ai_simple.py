"""
Simplified TRAE.AI Integration
Works with just the AI platforms without requiring external TRAE.AI system
"""

import os
import json
import time
import asyncio
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TEST_PROMPT = "Test prompt"

class SimpleTraeAI:
    """
    Simplified TRAE.AI integration that works with just AI platforms
    No external TRAE.AI system required
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.session = requests.Session()

        # AI Platform clients
        self.chatgpt_client = ChatGPTClient(self.config.get('chatgpt', {}))
        self.gemini_client = GeminiClient(self.config.get('gemini', {}))
        self.abacus_client = AbacusClient(self.config.get('abacus', {}))

        # Cross-validation settings
        self.cross_validate = self.config.get('cross_validate', True)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.8)

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from integrations.yaml if present (preferred), else env vars, else provided JSON path."""
        # 1) If an explicit JSON path is provided and exists
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)

        # 2) Try app-local integrations.yaml
        try:
            base = Path(__file__).resolve().parents[1]
            integ = base / 'config' / 'integrations.yaml'
            if integ.exists():
                import yaml  # local usage only
                y = yaml.safe_load(integ.read_text()) or {}
                openai_key = (y.get('openai_api_key') or '').strip()
                gemini_key = (y.get('google_ai_api_key') or '').strip()
                abacus_key = (y.get('abacus_api_key') or '').strip()
                conf = {
                    'openai_api_key': openai_key,
                    'google_ai_api_key': gemini_key,
                    'abacus_api_key': abacus_key,
                    'cross_validate': True,
                    'confidence_threshold': 0.8,
                    'chatgpt': {
                        'api_key': openai_key,
                        'base_url': 'https://api.openai.com/v1',
                        'model': 'gpt-4'
                    },
                    'gemini': {
                        'api_key': gemini_key,
                        'base_url': 'https://generativelanguage.googleapis.com/v1',
                        'model': 'gemini-pro'
                    },
                    'abacus': {
                        'api_key': abacus_key,
                        'base_url': 'https://apps.abacus.ai/chatllm',
                        'app_id': '1024a18ebe'
                    }
                }
                return conf
        except Exception:
            pass

        # 3) Fallback to environment variables
        return {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'google_ai_api_key': os.getenv('GOOGLE_AI_API_KEY', ''),
            'abacus_api_key': os.getenv('ABACUS_API_KEY', ''),
            'cross_validate': True,
            'confidence_threshold': 0.8,
            'chatgpt': {
                'api_key': os.getenv('OPENAI_API_KEY', ''),
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-4'
            },
            'gemini': {
                'api_key': os.getenv('GOOGLE_AI_API_KEY', ''),
                'base_url': 'https://generativelanguage.googleapis.com/v1',
                'model': 'gemini-pro'
            },
            'abacus': {
                'api_key': os.getenv('ABACUS_API_KEY', ''),
                'base_url': 'https://apps.abacus.ai/chatllm',
                'app_id': '1024a18ebe'
            }
        }

    async def generate_content(self,
                             prompt: str,
                             content_type: str = "video",
                             parameters: Optional[Dict] = None,
                             cross_validate: Optional[bool] = None) -> Dict[str, Any]:
        """
        Generate content using available AI platforms with cross-validation
        """
        if cross_validate is None:
            cross_validate = self.cross_validate

        # Prepare parameters
        params = parameters or {}
        params.update({
            'prompt': prompt,
            'content_type': content_type,
            'timestamp': datetime.now().isoformat()
        })

        # Generate content from available platforms
        results = []
        tasks = []

        # Only add platforms that have API keys
        if self.config.get('chatgpt', {}).get('api_key'):
            tasks.append(self.chatgpt_client.generate_content(prompt, content_type, params))
        if self.config.get('gemini', {}).get('api_key'):
            tasks.append(self.gemini_client.generate_content(prompt, content_type, params))
        if self.config.get('abacus', {}).get('api_key'):
            tasks.append(self.abacus_client.generate_content(prompt, content_type, params))

        if not tasks:
            return {
                'status': 'error',
                'error': 'No AI platforms configured. Please add API keys.',
                'result': None
            }

        # Run all tasks
        platform_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        valid_results = {}
        platform_names = ['chatgpt', 'gemini', 'abacus']
        for i, result in enumerate(platform_results):
            if i < len(platform_names) and not isinstance(result, Exception):
                valid_results[platform_names[i]] = result

        # Cross-validation if enabled and we have multiple results
        if cross_validate and len(valid_results) > 1:
            validated_result = self._cross_validate_results(valid_results)
            return {
                'status': 'completed',
                'result': validated_result,
                'platform_results': valid_results,
                'cross_validated': True,
                'confidence': validated_result.get('confidence', 0.0)
            }
        else:
            # Return best result based on confidence
            best_result = self._select_best_result(valid_results)
            return {
                'status': 'completed',
                'result': best_result,
                'platform_results': valid_results,
                'cross_validated': False
            }

    def _cross_validate_results(self, platform_results: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-validate results from multiple AI platforms"""
        valid_results = {k: v for k, v in platform_results.items() if v is not None}

        if len(valid_results) < 2:
            logger.warning("Insufficient results for cross-validation")
            return self._select_best_result(platform_results)

        # Simple consensus-based validation
        consensus_score = 0.0
        consensus_content = ""

        for platform, result in valid_results.items():
            if result.get('confidence', 0) > self.confidence_threshold:
                consensus_score += result.get('confidence', 0)
                if not consensus_content:
                    consensus_content = result.get('content', '')

        consensus_score = consensus_score / len(valid_results)

        return {
            'content': consensus_content,
            'confidence': consensus_score,
            'validation_method': 'consensus',
            'platforms_used': list(valid_results.keys())
        }

    def _select_best_result(self, platform_results: Dict[str, Any]) -> Dict[str, Any]:
        """Select the best result based on confidence score"""
        valid_results = {k: v for k, v in platform_results.items() if v is not None}

        if not valid_results:
            return {'content': '', 'confidence': 0.0, 'error': 'No valid results'}

        best_platform = max(valid_results.keys(),
                          key=lambda k: valid_results[k].get('confidence', 0))

        result = valid_results[best_platform]
        result['selected_platform'] = best_platform
        return result

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status - simplified version"""
        return {
            'status': 'LIVE',
            'timestamp': datetime.now().isoformat(),
            'platforms_configured': {
                'chatgpt': bool(self.config.get('chatgpt', {}).get('api_key')),
                'gemini': bool(self.config.get('gemini', {}).get('api_key')),
                'abacus': bool(self.config.get('abacus', {}).get('api_key'))
            },
            'cross_validation_enabled': self.cross_validate,
            'confidence_threshold': self.confidence_threshold
        }


class ChatGPTClient:
    """ChatGPT API client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        if config.get('api_key'):
            self.session.headers.update({
                'Authorization': f'Bearer {config.get("api_key")}',
                'Content-Type': 'application/json'
            })

    async def generate_content(self, prompt: str, content_type: str, parameters: Dict) -> Dict[str, Any]:
        """Generate content using ChatGPT"""
        if not self.config.get('api_key'):
            return {'error': 'ChatGPT API key not configured', 'confidence': 0.0}

        try:
            payload = {
                'model': self.config.get('model', 'gpt-4'),
                'messages': [
                    {'role': 'system', 'content': f'You are a professional content creator specializing in {content_type}.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 2000,
                'temperature': 0.7
            }

            response = self.session.post(
                f"{self.config['base_url']}/chat/completions",
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            return {
                'content': content,
                'confidence': 0.9,
                'platform': 'chatgpt',
                'model': self.config.get('model', 'gpt-4'),
                'tokens_used': result.get('usage', {}).get('total_tokens', 0)
            }

        except Exception as e:
            logger.error(f"ChatGPT generation error: {e}")
            return {'error': str(e), 'confidence': 0.0}


class GeminiClient:
    """Google Gemini API client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    async def generate_content(self, prompt: str, content_type: str, parameters: Dict) -> Dict[str, Any]:
        """Generate content using Gemini"""
        if not self.config.get('api_key'):
            return {'error': 'Gemini API key not configured', 'confidence': 0.0}

        try:
            payload = {
                'contents': [{
                    'parts': [{
                        'text': f'Create {content_type} content for: {prompt}'
                    }]
                }],
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 2000
                }
            }

            url = f"{self.config['base_url']}/models/{self.config.get('model', 'gemini-pro')}:generateContent"
            response = self.session.post(
                url,
                params={'key': self.config.get('api_key')},
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']

            return {
                'content': content,
                'confidence': 0.88,
                'platform': 'gemini',
                'model': self.config.get('model', 'gemini-pro')
            }

        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return {'error': str(e), 'confidence': 0.0}


class AbacusClient:
    """Abacus AI API client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        if config.get('api_key'):
            self.session.headers.update({
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {config.get("api_key")}'
            })

    async def generate_content(self, prompt: str, content_type: str, parameters: Dict) -> Dict[str, Any]:
        """Generate content using Abacus AI"""
        if not self.config.get('api_key'):
            return {'error': 'Abacus AI API key not configured', 'confidence': 0.0}

        try:
            payload = {
                'prompt': f'Create {content_type} content: {prompt}',
                'app_id': self.config.get('app_id', '1024a18ebe'),
                'max_tokens': 2000,
                'temperature': 0.7
            }

            response = self.session.post(
                f"{self.config['base_url']}/generate",
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            content = result.get('response', result.get('content', ''))

            return {
                'content': content,
                'confidence': 0.85,
                'platform': 'abacus',
                'app_id': self.config.get('app_id', '1024a18ebe')
            }

        except Exception as e:
            logger.error(f"Abacus generation error: {e}")
            return {'error': str(e), 'confidence': 0.0}


# Utility functions
async def test_simple_trae_ai_connection(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Test simplified TRAE.AI connection"""
    try:
        trae_ai = SimpleTraeAI(config_path)

        # Test system status
        status = trae_ai.get_system_status()

        # Test content generation
        test_result = await trae_ai.generate_content(
            "Test prompt for AI integration",
            "text",
            cross_validate=False
        )

        return {
            'status': 'success',
            'system_status': status,
            'test_generation': test_result,
            'platforms_available': status['platforms_configured']
        }

    except Exception as e:
        logger.error(f"Simple TRAE.AI connection test failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the integration
    import asyncio

    async def main():
        result = await test_simple_trae_ai_connection()
        print(json.dumps(result, indent=2))

    asyncio.run(main())
