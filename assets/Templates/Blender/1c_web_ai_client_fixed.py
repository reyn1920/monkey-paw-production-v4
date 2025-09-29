"""
WebAI Client - Fixed Implementation
Handles browser automation for AI platforms including ChatGPT, Gemini, Claude, etc.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SessionInfo:
    """Session information for tracking browser sessions"""

    session_id: str
    platform: str
    created_at: datetime
    last_used: datetime
    status: str = "active"
    page_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "platform": self.platform,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat(),
            "status": self.status,
            "page_url": self.page_url,
        }


class WebAIClient:
    """
    Web AI Client for managing browser automation sessions with AI platforms
    """

    def __init__(self, config_path: str = "config/web_ai_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.sessions: Dict[str, SessionInfo] = {}
        self.session_timeout = timedelta(
            minutes=self.config.get("session_management", {}).get(
                "session_timeout_minutes", 30
            )
        )
        self.max_concurrent_sessions = self.config.get("session_management", {}).get(
            "max_concurrent_sessions", 3
        )

        # Setup logging
        log_config = self.config.get("logging", {})
        log_file = log_config.get("file_path", "logs/web_ai_client.log")

        # Ensure log directory exists
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        # Configure file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_config.get("level", "INFO")))
        formatter = logging.Formatter(
            log_config.get(
                "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info("WebAIClient initialized with config from %s", config_path)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                return config.get("web_ai", {})
        except FileNotFoundError:
            logger.error("Config file not found: %s", self.config_path)
            return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in config file: %s", e)
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "enabled": True,
            "default_platform": "chatgpt",
            "timeout_seconds": 30,
            "max_retries": 3,
            "platforms": {
                "chatgpt": {
                    "enabled": True,
                    "url": "https://chat.openai.com",
                    "selectors": {
                        "message_input": "textarea[data-id='root']",
                        "send_button": "button[data-testid='send-button']",
                        "response_container": "div[data-message-author-role='assistant']",
                    },
                    "wait_times": {
                        "page_load": 5000,
                        "response_timeout": 30000,
                        "typing_delay": 100,
                    },
                }
            },
            "session_management": {
                "max_concurrent_sessions": 3,
                "session_timeout_minutes": 30,
                "cleanup_interval_minutes": 5,
                "reuse_sessions": True,
            },
        }

    def create_session(self, platform: str) -> str:
        """Create a new browser session for the specified platform"""
        # Clean up expired sessions first
        self._cleanup_expired_sessions()

        # Check if we've reached the maximum concurrent sessions
        active_sessions = [s for s in self.sessions.values() if s.status == "active"]
        if len(active_sessions) >= self.max_concurrent_sessions:
            # Try to reuse an existing session for the same platform
            existing_session = self._find_reusable_session(platform)
            if existing_session:
                logger.info(
                    "Reusing existing session %s for %s",
                    existing_session.session_id,
                    platform,
                )
                existing_session.last_used = datetime.now()
                return existing_session.session_id

            # If no reusable session, close the oldest one
            oldest_session = min(active_sessions, key=lambda s: s.last_used)
            self._close_session(oldest_session.session_id)

        # Create new session
        session_id = f"{platform}_{uuid.uuid4().hex[:8]}"
        now = datetime.now()

        session_info = SessionInfo(
            session_id=session_id,
            platform=platform,
            created_at=now,
            last_used=now,
            status="active",
        )

        self.sessions[session_id] = session_info

        logger.info("Created new session %s for platform %s", session_id, platform)
        return session_id

    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Get session information by ID"""
        session = self.sessions.get(session_id)
        if session and self._is_session_valid(session):
            session.last_used = datetime.now()
            return session
        elif session:
            # Session expired, remove it
            self._close_session(session_id)
        return None

    def _find_reusable_session(self, platform: str) -> Optional[SessionInfo]:
        """Find an existing active session for the platform that can be reused"""
        if not self.config.get("session_management", {}).get("reuse_sessions", True):
            return None

        for session in self.sessions.values():
            if (
                session.platform == platform
                and session.status == "active"
                and self._is_session_valid(session)
            ):
                return session
        return None

    def _is_session_valid(self, session: SessionInfo) -> bool:
        """Check if a session is still valid (not expired)"""
        return datetime.now() - session.last_used < self.session_timeout

    def _close_session(self, session_id: str) -> bool:
        """Close and remove a session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.status = "closed"
            logger.info(
                "Closed session %s for platform %s", session_id, session.platform
            )
            del self.sessions[session_id]
            return True
        return False

    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        expired_sessions = []
        for session_id, session in self.sessions.items():
            if not self._is_session_valid(session):
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            logger.info("Cleaning up expired session %s", session_id)
            self._close_session(session_id)

    async def send_web_request(self, session_id: str, message: str) -> Dict[str, Any]:
        """Send a web request using the specified session"""
        session = self.get_session(session_id)
        if not session:
            error_msg = f"Session {session_id} not found"
            logger.error("Web request failed: %s", error_msg)
            raise ValueError(error_msg)

        platform_config = self.config.get("platforms", {}).get(session.platform, {})
        if not platform_config.get("enabled", False):
            error_msg = f"Platform {session.platform} is not enabled"
            logger.error("Web request failed: %s", error_msg)
            raise ValueError(error_msg)

        logger.info(
            "Sending web request to %s using session %s", session.platform, session_id
        )

        try:
            # Simulate web request processing
            await asyncio.sleep(0.1)  # Simulate network delay

            # Update session
            session.last_used = datetime.now()
            session.page_url = platform_config.get("url")

            # Return mock response for now
            response = {
                "session_id": session_id,
                "platform": session.platform,
                "message": message,
                "response": f"Mock response from {session.platform} for: {message}",
                "timestamp": datetime.now().isoformat(),
                "status": "success",
            }

            logger.info("Web request completed successfully for session %s", session_id)
            return response

        except Exception as e:
            logger.error("Web request failed for session %s: %s", session_id, str(e))
            raise

    async def chat_completion(
        self, platform: str, message: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Complete chat interaction with specified platform"""
        logger.info("Starting chat completion with %s", platform)

        # Create or get session
        if session_id:
            session = self.get_session(session_id)
            if not session:
                logger.warning(
                    "Specified session %s not found, creating new session", session_id
                )
                session_id = self.create_session(platform)
        else:
            logger.info("Creating new session for %s", platform)
            session_id = self.create_session(platform)

        # Send the web request
        logger.info("Sending web request to %s", platform)
        response = await self.send_web_request(session_id, message)

        return response

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of all active sessions"""
        self._cleanup_expired_sessions()
        return [
            session.to_dict()
            for session in self.sessions.values()
            if session.status == "active"
        ]

    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        self._cleanup_expired_sessions()
        active_sessions = [s for s in self.sessions.values() if s.status == "active"]

        platform_counts = {}
        for session in active_sessions:
            platform_counts[session.platform] = (
                platform_counts.get(session.platform, 0) + 1
            )

        return {
            "total_active_sessions": len(active_sessions),
            "max_concurrent_sessions": self.max_concurrent_sessions,
            "platform_distribution": platform_counts,
            "session_timeout_minutes": self.session_timeout.total_seconds() / 60,
        }


# Global client instance
_web_ai_client = None


def get_web_ai_client() -> WebAIClient:
    """Get or create the global WebAI client instance"""
    global _web_ai_client
    if _web_ai_client is None:
        _web_ai_client = WebAIClient()
    return _web_ai_client


# Convenience functions for backward compatibility
async def chat_completion(
    platform: str, message: str, session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Convenience function for chat completion"""
    client = get_web_ai_client()
    return await client.chat_completion(platform, message, session_id)


def create_session(platform: str) -> str:
    """Convenience function for creating sessions"""
    client = get_web_ai_client()
    return client.create_session(platform)


def get_session_stats() -> Dict[str, Any]:
    """Convenience function for getting session stats"""
    client = get_web_ai_client()
    return client.get_session_stats()
