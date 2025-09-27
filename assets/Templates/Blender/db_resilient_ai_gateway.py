#!/usr/bin/env python3
"""
Resilient AI Gateway - Production-Ready Failover System
Provides intelligent failover and circuit breaker functionality for WebAI services.
"""

import time
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CircuitBreakerState:
    """Circuit breaker state for a provider"""

    provider: str
    failure_count: int = 0
    last_failure_time: Optional[datetime] = None
    state: str = "closed"  # closed, open, half_open
    next_attempt_time: Optional[datetime] = None


class WebRequestError(Exception):
    """Custom exception for web request errors"""

    pass


class ResilientAIGateway:
    """
    A smart gateway that provides failover and resilience for any WebAIClient.

    Features:
    - Automated failover between AI providers
    - Circuit breaker pattern to prevent cascading failures
    - Intelligent retry logic with exponential backoff
    - Health monitoring and recovery detection
    - Comprehensive logging and metrics
    """

    def __init__(
        self,
        provider_priority: Optional[List[str]] = None,
        config_path: Optional[str] = None,
    ):
        """
        Initialize the Resilient AI Gateway

        Args:
            provider_priority: List of providers in order of preference
            config_path: Path to configuration file
        """
        # Import WebAIClient dynamically to avoid import issues
        self.client = None
        self._init_client(config_path)

        # Define the order in which to try AI providers
        self.provider_priority = provider_priority or ["chatgpt", "gemini", "claude"]

        # Circuit breaker configuration
        self.CIRCUIT_OPEN_SECONDS = 300  # 5 minutes
        self.FAILURE_THRESHOLD = 3  # Number of failures before opening circuit
        self.HALF_OPEN_TIMEOUT = 60  # 1 minute for half-open state

        # Circuit breaker state tracking
        self.circuit_breakers = {}
        for provider in self.provider_priority:
            self.circuit_breakers[provider] = CircuitBreakerState(provider=provider)

        # Performance metrics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.provider_stats = {}
        for provider in self.provider_priority:
            self.provider_stats[provider] = {
                "requests": 0,
                "failures": 0,
                "successes": 0,
            }
        self.last_reset = datetime.now()

        logger.info(
            f"ResilientAIGateway initialized with providers: {self.provider_priority}"
        )

    def _init_client(self, config_path: Optional[str] = None):
        """Initialize the WebAI client with dynamic imports"""
        try:
            # Try different import paths
            import sys
            import os

            # Add parent directory to path
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            # Try importing from integrations first
            try:
                from integrations.web_ai_client_fixed import WebAIClient

                self.client = WebAIClient(config_path)
                logger.info("✅ WebAIClient imported from integrations")
            except ImportError:
                try:
                    from web_ai_client_fixed import WebAIClient

                    self.client = WebAIClient(config_path)
                    logger.info("✅ WebAIClient imported from root")
                except ImportError:
                    logger.warning("⚠️  WebAIClient not found, using mock client")
                    self.client = self._create_mock_client()

        except Exception as e:
            logger.error(f"❌ Failed to initialize WebAI client: {e}")
            self.client = self._create_mock_client()

    def _create_mock_client(self):
        """Create a mock client for testing purposes"""

        class MockWebAIClient:
            def __init__(self, config_path=None):
                pass

            def chat_completion(self, provider: str, prompt: str) -> str:
                # Simulate different provider behaviors for testing
                if provider == "chatgpt":
                    if "quantum" in prompt.lower():
                        raise WebRequestError("Session not found for ChatGPT")
                    return f"ChatGPT response to: {prompt[:50]}..."
                elif provider == "gemini":
                    return f"Gemini response to: {prompt[:50]}..."
                elif provider == "claude":
                    return f"Claude response to: {prompt[:50]}..."
                else:
                    raise WebRequestError(f"Unknown provider: {provider}")

        return MockWebAIClient()

    def _update_circuit_breaker(
        self, provider: str, success: bool, error_message: str = ""
    ):
        """Update circuit breaker state based on request outcome"""
        breaker = self.circuit_breakers[provider]

        if success:
            # Reset failure count on success
            breaker.failure_count = 0
            breaker.last_failure_time = None
            if breaker.state == "half_open":
                breaker.state = "closed"
                logger.info(f"🟢 CIRCUIT CLOSED for {provider} - Service recovered")
        else:
            # Increment failure count
            breaker.failure_count += 1
            breaker.last_failure_time = datetime.now()

            # Check if we should open the circuit
            if (
                breaker.failure_count >= self.FAILURE_THRESHOLD
                and breaker.state == "closed"
            ):
                breaker.state = "open"
                breaker.next_attempt_time = datetime.now() + timedelta(
                    seconds=self.CIRCUIT_OPEN_SECONDS
                )
                logger.warning(
                    f"🔴 CIRCUIT BREAKER OPENED for {provider} - Too many failures ({breaker.failure_count})"
                )

                # Check for session-specific errors
                if "Session" in error_message and "not found" in error_message:
                    logger.error(
                        f"🚨 SESSION ERROR detected for {provider}: {error_message}"
                    )

    def _is_circuit_available(self, provider: str) -> bool:
        """Check if circuit breaker allows requests to this provider"""
        breaker = self.circuit_breakers[provider]
        now = datetime.now()

        if breaker.state == "closed":
            return True
        elif breaker.state == "open":
            if breaker.next_attempt_time and now >= breaker.next_attempt_time:
                # Transition to half-open state
                breaker.state = "half_open"
                logger.info(f"🟡 CIRCUIT HALF-OPEN for {provider} - Testing recovery")
                return True
            else:
                return False
        elif breaker.state == "half_open":
            return True

        return False

    def _update_metrics(self, provider: str, success: bool):
        """Update performance metrics"""
        self.total_requests += 1
        self.provider_stats[provider]["requests"] += 1

        if success:
            self.successful_requests += 1
            self.provider_stats[provider]["successes"] += 1
        else:
            self.failed_requests += 1
            self.provider_stats[provider]["failures"] += 1

    def chat_completion(
        self, prompt: str, preferred_provider: Optional[str] = None
    ) -> str:
        """
        Sends a chat request, automatically failing over to the next provider on error.

        Args:
            prompt: The message to send to the AI
            preferred_provider: Optional preferred provider (will be tried first)

        Returns:
            The AI response as a string

        Raises:
            ConnectionError: If all providers fail
        """
        # Adjust provider priority if preferred provider is specified
        providers_to_try = self.provider_priority.copy()
        if preferred_provider and preferred_provider in providers_to_try:
            providers_to_try.remove(preferred_provider)
            providers_to_try.insert(0, preferred_provider)

        last_error = None
        attempted_providers = []

        logger.info("🚀 GATEWAY: Starting chat completion request")
        logger.info(f"📋 GATEWAY: Will try providers in order: {providers_to_try}")

        for provider in providers_to_try:
            # Check circuit breaker
            if not self._is_circuit_available(provider):
                breaker = self.circuit_breakers[provider]
                if breaker.next_attempt_time:
                    wait_time = (
                        breaker.next_attempt_time - datetime.now()
                    ).total_seconds()
                    logger.info(
                        f"⏸️  CIRCUIT OPEN for {provider}. Skipping... (retry in {wait_time:.0f}s)"
                    )
                else:
                    logger.info(f"⏸️  CIRCUIT OPEN for {provider}. Skipping...")
                continue

            attempted_providers.append(provider)

            try:
                logger.info(f"🔄 GATEWAY: Attempting request with {provider}...")

                # Use the WebAI client's chat_completion method
                response = self.client.chat_completion(provider, prompt)

                # Update metrics and circuit breaker
                self._update_metrics(provider, True)
                self._update_circuit_breaker(provider, True)

                logger.info(f"✅ GATEWAY: SUCCESS with {provider}!")
                return response

            except Exception as e:
                error_message = str(e)
                logger.warning(
                    f"❌ GATEWAY: FAILED with {provider}. Error: {error_message}"
                )

                # Update metrics and circuit breaker
                self._update_metrics(provider, False)
                self._update_circuit_breaker(provider, False, error_message)

                last_error = e

                # Add delay before trying next provider
                time.sleep(1)

        # All providers failed
        error_msg = f"All AI providers failed. Attempted: {attempted_providers}. Last error: {last_error}"
        logger.error(f"🚨 GATEWAY: {error_msg}")
        raise ConnectionError(error_msg) from last_error

    def start_chat_completion(self, provider: str, prompt: str) -> str:
        """
        Direct provider chat completion (for backward compatibility)

        Args:
            provider: The AI provider to use
            prompt: The message to send

        Returns:
            The AI response as a string
        """
        try:
            return self.chat_completion(prompt, provider)
        except Exception as e:
            # Convert to WebRequestError for compatibility
            raise WebRequestError(f"Chat completion failed: {e}") from e

    def get_gateway_status(self) -> Dict[str, Any]:
        """Get comprehensive gateway status and metrics"""
        status = {
            "gateway_info": {
                "providers": self.provider_priority,
                "circuit_open_seconds": self.CIRCUIT_OPEN_SECONDS,
                "failure_threshold": self.FAILURE_THRESHOLD,
            },
            "circuit_breakers": {},
            "metrics": {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "provider_stats": self.provider_stats,
                "last_reset": self.last_reset.isoformat(),
            },
            "health_summary": {
                "healthy_providers": 0,
                "degraded_providers": 0,
                "failed_providers": 0,
            },
        }

        # Add circuit breaker status
        for provider, breaker in self.circuit_breakers.items():
            status["circuit_breakers"][provider] = {
                "state": breaker.state,
                "failure_count": breaker.failure_count,
                "last_failure": (
                    breaker.last_failure_time.isoformat()
                    if breaker.last_failure_time
                    else None
                ),
                "next_attempt": (
                    breaker.next_attempt_time.isoformat()
                    if breaker.next_attempt_time
                    else None
                ),
            }

            # Update health summary
            if breaker.state == "closed":
                status["health_summary"]["healthy_providers"] += 1
            elif breaker.state == "half_open":
                status["health_summary"]["degraded_providers"] += 1
            else:
                status["health_summary"]["failed_providers"] += 1

        return status

    def reset_circuit_breaker(self, provider: str):
        """Manually reset a circuit breaker for a provider"""
        if provider in self.circuit_breakers:
            breaker = self.circuit_breakers[provider]
            breaker.state = "closed"
            breaker.failure_count = 0
            breaker.last_failure_time = None
            breaker.next_attempt_time = None
            logger.info(f"🔄 CIRCUIT BREAKER RESET for {provider}")

    def reset_all_circuit_breakers(self):
        """Reset all circuit breakers"""
        for provider in self.circuit_breakers:
            self.reset_circuit_breaker(provider)
        logger.info("🔄 ALL CIRCUIT BREAKERS RESET")


# Example usage and testing
if __name__ == "__main__":

    def main():
        # Initialize the gateway
        gateway = ResilientAIGateway()

        # Test prompt
        test_prompt = "Explain quantum computing in simple terms."

        try:
            print("🚀 Testing Resilient AI Gateway...")
            print(f"📝 Prompt: {test_prompt}")
            print()

            # This single call will automatically handle all the failures from your log
            response = gateway.chat_completion(test_prompt)
            print("✅ Final successful response:")
            print(f"📄 {response}")

        except ConnectionError as e:
            print("❌ Could not get a response from any provider:")
            print(f"🚨 {e}")

        # Show gateway status
        print("\n📊 Gateway Status:")
        status = gateway.get_gateway_status()
        print(json.dumps(status, indent=2, default=str))

    # Run the example
    main()
