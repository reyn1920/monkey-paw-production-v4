#!/usr/bin/env python3
"""
Comprehensive Test Suite for ResilientAIGateway
Tests failover scenarios, circuit breaker functionality, and error handling.
"""

import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta

# Import the gateway
try:
    from .resilient_ai_gateway import (
        ResilientAIGateway,
        WebRequestError,
        CircuitBreakerState,
    )
except ImportError:
    from resilient_ai_gateway import (
        ResilientAIGateway,
        WebRequestError,
        CircuitBreakerState,
    )


class TestResilientAIGateway(unittest.TestCase):
    """Test suite for ResilientAIGateway"""

    def setUp(self):
        """Set up test fixtures"""
        self.gateway = ResilientAIGateway(
            provider_priority=["chatgpt", "gemini", "claude"]
        )

    def test_gateway_initialization(self):
        """Test that gateway initializes correctly"""
        self.assertEqual(
            self.gateway.provider_priority, ["chatgpt", "gemini", "claude"]
        )
        self.assertEqual(len(self.gateway.circuit_breakers), 3)
        self.assertEqual(self.gateway.total_requests, 0)
        self.assertEqual(self.gateway.successful_requests, 0)
        self.assertEqual(self.gateway.failed_requests, 0)

        # Check circuit breakers are initialized
        for provider in ["chatgpt", "gemini", "claude"]:
            self.assertIn(provider, self.gateway.circuit_breakers)
            breaker = self.gateway.circuit_breakers[provider]
            self.assertEqual(breaker.state, "closed")
            self.assertEqual(breaker.failure_count, 0)

    def test_successful_chat_completion(self):
        """Test successful chat completion with first provider"""
        # Mock the client to return a successful response
        mock_client = Mock()
        mock_client.chat_completion.return_value = "Test response from ChatGPT"
        self.gateway.client = mock_client

        response = self.gateway.chat_completion("Test prompt")

        self.assertEqual(response, "Test response from ChatGPT")
        self.assertEqual(self.gateway.total_requests, 1)
        self.assertEqual(self.gateway.successful_requests, 1)
        self.assertEqual(self.gateway.failed_requests, 0)

        # Verify client was called with correct parameters
        mock_client.chat_completion.assert_called_once_with("chatgpt", "Test prompt")

    def test_failover_to_second_provider(self):
        """Test failover when first provider fails"""
        # Mock the client to fail on first call, succeed on second
        mock_client = Mock()
        mock_client.chat_completion.side_effect = [
            WebRequestError("Session not found for ChatGPT"),
            "Test response from Gemini",
        ]
        self.gateway.client = mock_client

        response = self.gateway.chat_completion("Test prompt")

        self.assertEqual(response, "Test response from Gemini")
        self.assertEqual(self.gateway.total_requests, 2)
        self.assertEqual(self.gateway.successful_requests, 1)
        self.assertEqual(self.gateway.failed_requests, 1)

        # Verify both providers were tried
        self.assertEqual(mock_client.chat_completion.call_count, 2)

    def test_failover_to_third_provider(self):
        """Test failover when first two providers fail"""
        # Mock the client to fail on first two calls, succeed on third
        mock_client = Mock()
        mock_client.chat_completion.side_effect = [
            WebRequestError("Session not found for ChatGPT"),
            WebRequestError("Rate limit exceeded for Gemini"),
            "Test response from Claude",
        ]
        self.gateway.client = mock_client

        response = self.gateway.chat_completion("Test prompt")

        self.assertEqual(response, "Test response from Claude")
        self.assertEqual(self.gateway.total_requests, 3)
        self.assertEqual(self.gateway.successful_requests, 1)
        self.assertEqual(self.gateway.failed_requests, 2)

        # Verify all three providers were tried
        self.assertEqual(mock_client.chat_completion.call_count, 3)

    def test_all_providers_fail(self):
        """Test behavior when all providers fail"""
        # Mock the client to fail on all calls
        mock_client = Mock()
        mock_client.chat_completion.side_effect = [
            WebRequestError("Session not found for ChatGPT"),
            WebRequestError("Rate limit exceeded for Gemini"),
            WebRequestError("Service unavailable for Claude"),
        ]
        self.gateway.client = mock_client

        with self.assertRaises(ConnectionError) as context:
            self.gateway.chat_completion("Test prompt")

        self.assertIn("All AI providers failed", str(context.exception))
        self.assertEqual(self.gateway.total_requests, 3)
        self.assertEqual(self.gateway.successful_requests, 0)
        self.assertEqual(self.gateway.failed_requests, 3)

    def test_circuit_breaker_opens_after_failures(self):
        """Test that circuit breaker opens after threshold failures"""
        # Mock the client to always fail for ChatGPT
        mock_client = Mock()
        mock_client.chat_completion.side_effect = WebRequestError(
            "Session not found for ChatGPT"
        )
        self.gateway.client = mock_client

        # Make multiple requests to trigger circuit breaker
        for i in range(self.gateway.FAILURE_THRESHOLD):
            try:
                self.gateway.chat_completion("Test prompt")
            except ConnectionError:
                pass  # Expected when all providers fail

        # Check that circuit breaker is now open for ChatGPT
        chatgpt_breaker = self.gateway.circuit_breakers["chatgpt"]
        self.assertEqual(chatgpt_breaker.state, "open")
        self.assertEqual(chatgpt_breaker.failure_count, self.gateway.FAILURE_THRESHOLD)
        self.assertIsNotNone(chatgpt_breaker.next_attempt_time)

    def test_circuit_breaker_skips_open_provider(self):
        """Test that open circuit breaker skips provider"""
        # Manually open the circuit for ChatGPT
        chatgpt_breaker = self.gateway.circuit_breakers["chatgpt"]
        chatgpt_breaker.state = "open"
        chatgpt_breaker.next_attempt_time = datetime.now() + timedelta(minutes=5)

        # Mock the client to succeed with Gemini
        mock_client = Mock()
        mock_client.chat_completion.return_value = "Test response from Gemini"
        self.gateway.client = mock_client

        response = self.gateway.chat_completion("Test prompt")

        self.assertEqual(response, "Test response from Gemini")
        # Verify ChatGPT was skipped and Gemini was called directly
        mock_client.chat_completion.assert_called_once_with("gemini", "Test prompt")

    def test_circuit_breaker_half_open_recovery(self):
        """Test circuit breaker transitions to half-open and recovers"""
        # Set up an open circuit that should transition to half-open
        chatgpt_breaker = self.gateway.circuit_breakers["chatgpt"]
        chatgpt_breaker.state = "open"
        chatgpt_breaker.next_attempt_time = datetime.now() - timedelta(
            seconds=1
        )  # Past time

        # Mock successful response
        mock_client = Mock()
        mock_client.chat_completion.return_value = "Test response from ChatGPT"
        self.gateway.client = mock_client

        response = self.gateway.chat_completion("Test prompt")

        self.assertEqual(response, "Test response from ChatGPT")
        # Circuit should be closed after successful request
        self.assertEqual(chatgpt_breaker.state, "closed")
        self.assertEqual(chatgpt_breaker.failure_count, 0)

    def test_preferred_provider_priority(self):
        """Test that preferred provider is tried first"""
        # Mock the client to succeed
        mock_client = Mock()
        mock_client.chat_completion.return_value = "Test response from Claude"
        self.gateway.client = mock_client

        response = self.gateway.chat_completion(
            "Test prompt", preferred_provider="claude"
        )

        self.assertEqual(response, "Test response from Claude")
        # Verify Claude was called first (not ChatGPT)
        mock_client.chat_completion.assert_called_once_with("claude", "Test prompt")

    def test_start_chat_completion_compatibility(self):
        """Test backward compatibility method"""
        # Mock the client to succeed
        mock_client = Mock()
        mock_client.chat_completion.return_value = "Test response from Gemini"
        self.gateway.client = mock_client

        response = self.gateway.start_chat_completion("gemini", "Test prompt")

        self.assertEqual(response, "Test response from Gemini")
        # Should use the preferred provider (gemini)
        mock_client.chat_completion.assert_called_once_with("gemini", "Test prompt")

    def test_start_chat_completion_error_handling(self):
        """Test error handling in backward compatibility method"""
        # Mock the client to fail
        mock_client = Mock()
        mock_client.chat_completion.side_effect = [
            WebRequestError("Session not found"),
            WebRequestError("Rate limit exceeded"),
            WebRequestError("Service unavailable"),
        ]
        self.gateway.client = mock_client

        with self.assertRaises(WebRequestError):
            self.gateway.start_chat_completion("chatgpt", "Test prompt")

    def test_gateway_status_reporting(self):
        """Test comprehensive status reporting"""
        # Make some requests to generate metrics
        mock_client = Mock()
        mock_client.chat_completion.side_effect = [
            "Success 1",
            WebRequestError("Failure 1"),
            "Success 2",
        ]
        self.gateway.client = mock_client

        # Make requests
        self.gateway.chat_completion("Test 1")
        try:
            self.gateway.chat_completion("Test 2")
        except ConnectionError:
            pass
        self.gateway.chat_completion("Test 3")

        status = self.gateway.get_gateway_status()

        # Verify status structure
        self.assertIn("gateway_info", status)
        self.assertIn("circuit_breakers", status)
        self.assertIn("metrics", status)
        self.assertIn("health_summary", status)

        # Verify metrics
        metrics = status["metrics"]
        self.assertEqual(metrics["total_requests"], 5)  # 3 + 2 from failover
        self.assertEqual(metrics["successful_requests"], 2)
        self.assertEqual(metrics["failed_requests"], 3)

        # Verify circuit breaker status
        for provider in ["chatgpt", "gemini", "claude"]:
            self.assertIn(provider, status["circuit_breakers"])

    def test_manual_circuit_breaker_reset(self):
        """Test manual circuit breaker reset functionality"""
        # Open a circuit breaker
        chatgpt_breaker = self.gateway.circuit_breakers["chatgpt"]
        chatgpt_breaker.state = "open"
        chatgpt_breaker.failure_count = 5
        chatgpt_breaker.next_attempt_time = datetime.now() + timedelta(minutes=5)

        # Reset it
        self.gateway.reset_circuit_breaker("chatgpt")

        # Verify it's reset
        self.assertEqual(chatgpt_breaker.state, "closed")
        self.assertEqual(chatgpt_breaker.failure_count, 0)
        self.assertIsNone(chatgpt_breaker.next_attempt_time)

    def test_reset_all_circuit_breakers(self):
        """Test resetting all circuit breakers"""
        # Open all circuit breakers
        for provider in self.gateway.provider_priority:
            breaker = self.gateway.circuit_breakers[provider]
            breaker.state = "open"
            breaker.failure_count = 5
            breaker.next_attempt_time = datetime.now() + timedelta(minutes=5)

        # Reset all
        self.gateway.reset_all_circuit_breakers()

        # Verify all are reset
        for provider in self.gateway.provider_priority:
            breaker = self.gateway.circuit_breakers[provider]
            self.assertEqual(breaker.state, "closed")
            self.assertEqual(breaker.failure_count, 0)
            self.assertIsNone(breaker.next_attempt_time)

    def test_session_error_detection(self):
        """Test specific session error detection and handling"""
        # Mock the client to return session error
        mock_client = Mock()
        mock_client.chat_completion.side_effect = [
            WebRequestError("Session not found for ChatGPT"),
            "Recovery response from Gemini",
        ]
        self.gateway.client = mock_client

        response = self.gateway.chat_completion("Test prompt")

        self.assertEqual(response, "Recovery response from Gemini")

        # Verify session error was detected and circuit breaker updated
        chatgpt_breaker = self.gateway.circuit_breakers["chatgpt"]
        self.assertEqual(chatgpt_breaker.failure_count, 1)

    def test_mock_client_behavior(self):
        """Test the mock client behavior for different scenarios"""
        # Test with actual mock client (when WebAIClient import fails)
        gateway = ResilientAIGateway()

        # Test quantum prompt (should trigger ChatGPT failure)
        try:
            response = gateway.chat_completion("Explain quantum computing")
            # Should get response from Gemini or Claude
            self.assertIn("response to:", response)
        except ConnectionError:
            # All providers might fail in some test scenarios
            pass

        # Test non-quantum prompt (should succeed with ChatGPT)
        response = gateway.chat_completion("Hello world")
        self.assertIn("ChatGPT response to:", response)


class TestCircuitBreakerState(unittest.TestCase):
    """Test suite for CircuitBreakerState dataclass"""

    def test_circuit_breaker_initialization(self):
        """Test circuit breaker state initialization"""
        breaker = CircuitBreakerState(provider="test_provider")

        self.assertEqual(breaker.provider, "test_provider")
        self.assertEqual(breaker.failure_count, 0)
        self.assertIsNone(breaker.last_failure_time)
        self.assertEqual(breaker.state, "closed")
        self.assertIsNone(breaker.next_attempt_time)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for real-world scenarios"""

    def test_high_load_scenario(self):
        """Test gateway behavior under high load"""
        gateway = ResilientAIGateway()

        # Mock intermittent failures
        mock_client = Mock()
        responses = []
        for i in range(100):
            if i % 10 == 0:  # Every 10th request fails
                responses.append(WebRequestError(f"Failure {i}"))
            else:
                responses.append(f"Success {i}")

        mock_client.chat_completion.side_effect = responses
        gateway.client = mock_client

        successful_responses = 0
        failed_responses = 0

        for i in range(50):  # Make 50 requests
            try:
                response = gateway.chat_completion(f"Request {i}")
                successful_responses += 1
            except ConnectionError:
                failed_responses += 1

        # Most requests should succeed due to failover
        self.assertGreater(successful_responses, failed_responses)

    def test_cascading_failure_recovery(self):
        """Test recovery from cascading failures"""
        gateway = ResilientAIGateway()

        # Simulate all providers failing, then recovering
        mock_client = Mock()

        # First 9 calls fail (3 failures per provider to open circuits)
        failure_responses = [WebRequestError("Service down")] * 9
        # Then all succeed
        success_responses = ["Recovery response"] * 10

        mock_client.chat_completion.side_effect = failure_responses + success_responses
        gateway.client = mock_client

        # Make initial requests that will fail
        for i in range(3):
            try:
                gateway.chat_completion(f"Failing request {i}")
            except ConnectionError:
                pass

        # All circuits should be open now
        for provider in gateway.provider_priority:
            breaker = gateway.circuit_breakers[provider]
            self.assertEqual(breaker.state, "open")

        # Reset circuits to simulate time passing
        gateway.reset_all_circuit_breakers()

        # Now requests should succeed
        response = gateway.chat_completion("Recovery request")
        self.assertEqual(response, "Recovery response")


if __name__ == "__main__":
    # Configure test logging
    import logging

    logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestResilientAIGateway,
        TestCircuitBreakerState,
        TestIntegrationScenarios,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print(f"\n{'=' * 60}")
    print("TEST SUMMARY")
    print(f"{'=' * 60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            error_msg = traceback.split("AssertionError: ")[-1].split("\n")[0]
            print(f"- {test}: {error_msg}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            error_msg = traceback.split("\n")[-2]
            print(f"- {test}: {error_msg}")

    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
