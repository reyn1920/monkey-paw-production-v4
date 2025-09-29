"""
TRAE.AI Integration Module
Comprehensive integration with ChatGPT, Gemini, and Abacus AI platforms
"""

import os
import json
import time
import asyncio
import aiohttp
import requests
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Constants
CONTENT_TYPE_JSON = "application/json"
TEST_PROMPT = "Test prompt"
KEY_POINT_KEYWORDS = ["key point", "finding", "important"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TraeAIIntegration:
    """
    Main integration class for TRAE.AI platform
    Connects to ChatGPT, Gemini, and Abacus AI with cross-validation
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self._setup_session()

        # AI Platform clients
        self.chatgpt_client = ChatGPTClient(self.config.get('chatgpt', {}))
        self.gemini_client = GeminiClient(self.config.get('gemini', {}))
        self.abacus_client = AbacusClient(self.config.get('abacus', {}))

        # Cross-validation settings
        self.cross_validate = self.config.get('cross_validate', True)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.8)

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or environment variables"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)

        # Fallback to environment variables
        return {
            'trae_master_key': os.getenv('TRAE_MASTER_KEY', ''),
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'google_ai_api_key': os.getenv('GOOGLE_AI_API_KEY', ''),
            'abacus_api_key': os.getenv('ABACUS_API_KEY', ''),
            'base_url': os.getenv('TRAE_BASE_URL', 'http://localhost:8080/api/v1'),
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

    def _setup_session(self):
        """Setup HTTP session with authentication headers"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.config.get("trae_master_key", "")}',
            'Content-Type': CONTENT_TYPE_JSON,
            'User-Agent': 'TRAE-AI-Integration/1.0',
            'X-Request-ID': f'trae_{int(time.time())}'
        })

    async def generate_content(self,
                             prompt: str,
                             content_type: str = "video",
                             parameters: Optional[Dict] = None,
                             cross_validate: Optional[bool] = None) -> Dict[str, Any]:
        """
        Generate content using all three AI platforms with cross-validation
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

        # Generate content from all platforms
        results = await asyncio.gather(
            self.chatgpt_client.generate_content(prompt, content_type, params),
            self.gemini_client.generate_content(prompt, content_type, params),
            self.abacus_client.generate_content(prompt, content_type, params),
            return_exceptions=True
        )

        # Process results
        platform_results = {
            'chatgpt': results[0] if not isinstance(results[0], Exception) else None,
            'gemini': results[1] if not isinstance(results[1], Exception) else None,
            'abacus': results[2] if not isinstance(results[2], Exception) else None
        }

        # Cross-validation if enabled
        if cross_validate:
            validated_result = self._cross_validate_results(platform_results)
            return {
                'status': 'completed',
                'result': validated_result,
                'platform_results': platform_results,
                'cross_validated': True,
                'confidence': validated_result.get('confidence', 0.0)
            }
        else:
            # Return best result based on confidence
            best_result = self._select_best_result(platform_results)
            return {
                'status': 'completed',
                'result': best_result,
                'platform_results': platform_results,
                'cross_validated': False
            }

    def _cross_validate_results(self, platform_results: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-validate results from multiple AI platforms"""
        valid_results = {k: v for k, v in platform_results.items() if v is not None}

        if len(valid_results) < 2:
            logger.warning("Insufficient results for cross-validation")
            return self._select_best_result(platform_results)

        # Simple consensus-based validation
        # In production, this would be more sophisticated
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

    def research_analyze(self,
                        query: str,
                        sources: List[str] = None,
                        depth: str = "comprehensive") -> Dict[str, Any]:
        """Perform research analysis using all AI platforms"""
        sources = sources or ["news", "academic", "social_media"]

        # Research using all platforms
        results = asyncio.run(asyncio.gather(
            self.chatgpt_client.research_analyze(query, sources, depth),
            self.gemini_client.research_analyze(query, sources, depth),
            self.abacus_client.research_analyze(query, sources, depth),
            return_exceptions=True
        ))

        # Combine and validate research results
        research_data = {
            'query': query,
            'sources': sources,
            'depth': depth,
            'platform_results': {
                'chatgpt': results[0] if not isinstance(results[0], Exception) else None,
                'gemini': results[1] if not isinstance(results[1], Exception) else None,
                'abacus': results[2] if not isinstance(results[2], Exception) else None
            },
            'timestamp': datetime.now().isoformat()
        }

        # Synthesize findings
        synthesized = self._synthesize_research(research_data)
        research_data['synthesized_findings'] = synthesized

        return research_data

    def _synthesize_research(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize research findings from multiple platforms"""
        valid_results = {k: v for k, v in research_data['platform_results'].items()
                        if v is not None}

        if not valid_results:
            return {'error': 'No valid research results'}

        # Combine key findings
        all_findings = []
        for platform, result in valid_results.items():
            findings = result.get('key_findings', [])
            for finding in findings:
                finding['source_platform'] = platform
                all_findings.append(finding)

        # Group similar findings
        grouped_findings = self._group_similar_findings(all_findings)

        return {
            'total_findings': len(all_findings),
            'unique_findings': len(grouped_findings),
            'grouped_findings': grouped_findings,
            'confidence': min(0.95, len(valid_results) * 0.3)  # Higher confidence with more sources
        }

    def _group_similar_findings(self, findings: List[Dict]) -> List[Dict]:
        """Group similar findings from different platforms"""
        # Simple grouping based on content similarity
        # In production, this would use more sophisticated NLP
        grouped = []
        used_indices = set()

        for i, finding in enumerate(findings):
            if i in used_indices:
                continue

            group = [finding]
            used_indices.add(i)

            # Find similar findings
            for j, other_finding in enumerate(findings[i+1:], i+1):
                if j in used_indices:
                    continue

                if self._findings_similar(finding, other_finding):
                    group.append(other_finding)
                    used_indices.add(j)

            grouped.append({
                'finding': group[0]['finding'],
                'confidence': max(f.get('confidence', 0) for f in group),
                'sources': [f['source_platform'] for f in group],
                'source_count': len(group)
            })

        return grouped

    def _findings_similar(self, finding1: Dict, finding2: Dict) -> bool:
        """Check if two findings are similar (simple implementation)"""
        text1 = finding1.get('finding', '').lower()
        text2 = finding2.get('finding', '').lower()

        # Simple similarity check - in production, use proper NLP
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return False

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        similarity = len(intersection) / len(union) if union else 0
        return similarity > 0.6  # 60% word overlap threshold

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status from TRAE.AI"""
        try:
            response = self.session.get(f"{self.config['base_url']}/system/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e), 'status': 'unavailable'}

    def create_video(self,
                    script: str,
                    voice_settings: Optional[Dict] = None,
                    video_settings: Optional[Dict] = None) -> Dict[str, Any]:
        """Create video using TRAE.AI video production pipeline"""
        voice_settings = voice_settings or {
            'voice_id': 'professional_male',
            'speed': 1.0,
            'pitch': 0.0,
            'volume': 0.8
        }

        video_settings = video_settings or {
            'resolution': '1920x1080',
            'fps': 30,
            'format': 'mp4',
            'quality': 'high'
        }

        payload = {
            'task_id': f'video_{int(time.time())}',
            'script': script,
            'parameters': {
                'voice_settings': voice_settings,
                'video_settings': video_settings,
                'visual_elements': {
                    'background_type': 'gradient',
                    'background_color': '#1a1a2e',
                    'text_overlays': True,
                    'transitions': 'fade'
                },
                'audio_settings': {
                    'background_music': True,
                    'music_volume': 0.3,
                    'music_genre': 'corporate',
                    'noise_reduction': True
                }
            }
        }

        try:
            response = self.session.post(
                f"{self.config['base_url']}/video/create",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return {'error': str(e), 'status': 'failed'}


class ChatGPTClient:
    """ChatGPT API client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {config.get("api_key", "")}',
            'Content-Type': CONTENT_TYPE_JSON
        })

    async def generate_content(self, prompt: str, content_type: str, parameters: Dict) -> Dict[str, Any]:
        """Generate content using ChatGPT"""
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
                'confidence': 0.9,  # ChatGPT typically high confidence
                'platform': 'chatgpt',
                'model': self.config.get('model', 'gpt-4'),
                'tokens_used': result.get('usage', {}).get('total_tokens', 0)
            }

        except Exception as e:
            logger.error(f"ChatGPT generation error: {e}")
            return {'error': str(e), 'confidence': 0.0}

    async def research_analyze(self, query: str, sources: List[str], depth: str) -> Dict[str, Any]:
        """Perform research analysis using ChatGPT"""
        try:
            system_prompt = f"""You are a research analyst. Analyze the following query using {depth} depth:
            Query: {query}
            Sources to consider: {', '.join(sources)}

            Provide key findings with confidence scores."""

            payload = {
                'model': self.config.get('model', 'gpt-4'),
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': f"Research: {query}"}
                ],
                'max_tokens': 3000,
                'temperature': 0.3
            }

            response = self.session.post(
                f"{self.config['base_url']}/chat/completions",
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse findings (simplified)
            findings = self._parse_findings(content)

            return {
                'key_findings': findings,
                'summary': content,
                'sources_analyzed': len(sources),
                'confidence': 0.85,
                'platform': 'chatgpt'
            }

        except Exception as e:
            logger.error(f"ChatGPT research error: {e}")
            return {'error': str(e), 'confidence': 0.0}

    def _parse_findings(self, content: str) -> List[Dict[str, Any]]:
        """Parse research findings from ChatGPT response"""
        # Simple parsing - in production, use more sophisticated NLP
        lines = content.split('\n')
        findings = []

        for line in lines:
            if any(keyword in line.lower() for keyword in ['finding', 'key point', 'important']):
                findings.append({
                    'finding': line.strip(),
                    'confidence': 0.8
                })

        return findings[:5]  # Limit to top 5 findings


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
                params={'key': self.config.get('api_key', '')},
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

    async def research_analyze(self, query: str, sources: List[str], depth: str) -> Dict[str, Any]:
        """Perform research analysis using Gemini"""
        try:
            prompt = f"""Research Analysis Request:
            Query: {query}
            Sources: {', '.join(sources)}
            Depth: {depth}

            Provide comprehensive analysis with key findings and confidence scores."""

            payload = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }],
                'generationConfig': {
                    'temperature': 0.3,
                    'maxOutputTokens': 3000
                }
            }

            url = f"{self.config['base_url']}/models/{self.config.get('model', 'gemini-pro')}:generateContent"
            response = self.session.post(
                url,
                params={'key': self.config.get('api_key', '')},
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']

            findings = self._parse_findings(content)

            return {
                'key_findings': findings,
                'summary': content,
                'sources_analyzed': len(sources),
                'confidence': 0.82,
                'platform': 'gemini'
            }

        except Exception as e:
            logger.error(f"Gemini research error: {e}")
            return {'error': str(e), 'confidence': 0.0}

    def _parse_findings(self, content: str) -> List[Dict[str, Any]]:
        """Parse research findings from Gemini response"""
        lines = content.split('\n')
        findings = []

        for line in lines:
            if any(keyword in line.lower() for keyword in ['finding', 'key point', 'important', 'analysis']):
                findings.append({
                    'finding': line.strip(),
                    'confidence': 0.8
                })

        return findings[:5]


class AbacusClient:
    """Abacus AI API client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.get("api_key", "")}'
        })

    async def generate_content(self, prompt: str, content_type: str, parameters: Dict) -> Dict[str, Any]:
        """Generate content using Abacus AI"""
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

    async def research_analyze(self, query: str, sources: List[str], depth: str) -> Dict[str, Any]:
        """Perform research analysis using Abacus AI"""
        try:
            prompt = f"""Research Analysis:
            Query: {query}
            Sources: {', '.join(sources)}
            Depth: {depth}

            Provide detailed analysis with key findings."""

            payload = {
                'prompt': prompt,
                'app_id': self.config.get('app_id', '1024a18ebe'),
                'max_tokens': 3000,
                'temperature': 0.3
            }

            response = self.session.post(
                f"{self.config['base_url']}/generate",
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            content = result.get('response', result.get('content', ''))

            findings = self._parse_findings(content)

            return {
                'key_findings': findings,
                'summary': content,
                'sources_analyzed': len(sources),
                'confidence': 0.80,
                'platform': 'abacus'
            }

        except Exception as e:
            logger.error(f"Abacus research error: {e}")
            return {'error': str(e), 'confidence': 0.0}

    def _parse_findings(self, content: str) -> List[Dict[str, Any]]:
        """Parse research findings from Abacus response"""
        lines = content.split('\n')
        findings = []

        for line in lines:
            if any(keyword in line.lower() for keyword in ['finding', 'key point', 'important', 'insight']):
                findings.append({
                    'finding': line.strip(),
                    'confidence': 0.8
                })

        return findings[:5]


# Utility functions for integration
async def test_trae_ai_connection(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Test TRAE.AI connection and all AI platforms"""
    try:
        trae_ai = TraeAIIntegration(config_path)

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
            'platforms_available': {
                'chatgpt': bool(trae_ai.config.get('chatgpt', {}).get('api_key')),
                'gemini': bool(trae_ai.config.get('gemini', {}).get('api_key')),
                'abacus': bool(trae_ai.config.get('abacus', {}).get('api_key'))
            }
        }

    except Exception as e:
        logger.error(f"TRAE.AI connection test failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


def create_default_config(config_path: str) -> None:
    """Create default configuration file"""
    default_config = {
        'trae_master_key': 'your_trae_master_key_here',
        'openai_api_key': 'your_openai_api_key_here',
        'google_ai_api_key': 'your_google_ai_api_key_here',
        'abacus_api_key': 'your_abacus_api_key_here',
        'base_url': 'http://localhost:8080/api/v1',
        'cross_validate': True,
        'confidence_threshold': 0.8,
        'chatgpt': {
            'api_key': 'your_openai_api_key_here',
            'base_url': 'https://api.openai.com/v1',
            'model': 'gpt-4'
        },
        'gemini': {
            'api_key': 'your_google_ai_api_key_here',
            'base_url': 'https://generativelanguage.googleapis.com/v1',
            'model': 'gemini-pro'
        },
        'abacus': {
            'api_key': 'your_abacus_api_key_here',
            'base_url': 'https://apps.abacus.ai/chatllm',
            'app_id': '1024a18ebe'
        }
    }

    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)

    logger.info(f"Default configuration created at {config_path}")


if __name__ == "__main__":
    # Test the integration
    import asyncio

    async def main():
        # Create default config if it doesn't exist
        config_path = "trae_ai_config.json"
        if not Path(config_path).exists():
            create_default_config(config_path)
            print(f"Please update {config_path} with your API keys")
            return

        # Test connection
        result = await test_trae_ai_connection(config_path)
        print(json.dumps(result, indent=2))

    asyncio.run(main())
