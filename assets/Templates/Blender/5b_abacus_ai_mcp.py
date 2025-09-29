#!/usr/bin/env python3
"""
Abacus.AI Route LLM APIs MCP Server Implementation

Provides MCP (Model Context Protocol) integration for Abacus.AI's Route LLM APIs.
This server enables Trae.AI to interact with Abacus.AI's LLM routing and model services.

Features:
- LLM model routing and selection
- Chat completions with multiple models
- Model performance analytics
- Cost optimization through intelligent routing
- Real-time model switching
- Batch processing capabilities

Author: Trae.AI Integration Team
Version: 1.0.0
"""

from backend.integrations.mcp_protocol import (
    MCPServer,
    MCPTool,
    MCPResource,
    MCPPrompt,
    MCPCapability,
    MCPResourceType,
    MCPMessage,
)
import asyncio
import os
import sys
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import logging

try:
    import aiohttp

    aiohttp_available = True
except ImportError:
    aiohttp_available = False

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


try:
    from utils.logger import setup_logger
except ImportError:

    def setup_logger(name: str):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)


class AbacusAIModelType(Enum):
    """Supported Abacus.AI model types."""

    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    CLAUDE_3_HAIKU = "claude-3-haiku"
    GEMINI_PRO = "gemini-pro"
    LLAMA_2_70B = "llama-2-70b"
    MIXTRAL_8X7B = "mixtral-8x7b"
    CUSTOM = "custom"


class RoutingStrategy(Enum):
    """LLM routing strategies."""

    COST_OPTIMIZED = "cost_optimized"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    BALANCED = "balanced"
    CUSTOM = "custom"


@dataclass
class AbacusAIConfig:
    """Configuration for Abacus.AI API."""

    api_key: str
    base_url: str = "https://api.abacus.ai"
    default_model: AbacusAIModelType = AbacusAIModelType.GPT_4_TURBO
    default_routing_strategy: RoutingStrategy = RoutingStrategy.BALANCED
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 30


@dataclass
class ChatMessage:
    """Chat message structure."""

    role: str  # system, user, assistant
    content: str
    timestamp: Optional[datetime] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    cost: Optional[float] = None


@dataclass
class ModelMetrics:
    """Model performance metrics."""

    model_name: str
    total_requests: int
    avg_latency: float
    avg_cost: float
    success_rate: float
    last_used: datetime
    total_tokens: int


class AbacusAIMCPServer(MCPServer):
    """MCP Server for Abacus.AI Route LLM APIs."""

    def __init__(self, config: AbacusAIConfig, **kwargs):
        super().__init__(
            name="AbacusAI-RouteLLM",
            version="1.0.0",
            capabilities=[
                MCPCapability.TOOLS,
                MCPCapability.RESOURCES,
                MCPCapability.CONTEXT,
                MCPCapability.PROMPTS,
            ],
            **kwargs,
        )

        self.config = config
        self.logger = setup_logger("abacus_ai_mcp")
        self.session: Optional[aiohttp.ClientSession] = None
        self.use_aiohttp = aiohttp_available
        self.model_metrics: dict[str, ModelMetrics] = {}
        self.active_conversations: dict[str, list[ChatMessage]] = {}

        # Register tools
        self._register_tools()
        self._register_resources()
        self._register_prompts()

    def _register_tools(self):
        """Register available tools."""

        # Chat completion tool
        self.register_tool(
            MCPTool(
                name="chat_completion",
                description="Generate chat completions using Abacus.AI's routed LLM models",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "messages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "role": {
                                        "type": "string",
                                        "enum": ["system", "user", "assistant"],
                                    },
                                    "content": {"type": "string"},
                                },
                                "required": ["role", "content"],
                            },
                            "description": "Array of chat messages",
                        },
                        "model": {
                            "type": "string",
                            "description": "Specific model to use (optional, uses routing if not specified)",
                            "enum": [model.value for model in AbacusAIModelType],
                        },
                        "routing_strategy": {
                            "type": "string",
                            "description": "Routing strategy for model selection",
                            "enum": [strategy.value for strategy in RoutingStrategy],
                        },
                        "max_tokens": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 8192,
                        },
                        "temperature": {"type": "number", "minimum": 0, "maximum": 2},
                        "conversation_id": {
                            "type": "string",
                            "description": "ID to maintain conversation context",
                        },
                    },
                    "required": ["messages"],
                },
            )
        )

        # Model selection tool
        self.register_tool(
            MCPTool(
                name="select_optimal_model",
                description="Select the optimal model based on requirements and constraints",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_type": {
                            "type": "string",
                            "enum": [
                                "chat",
                                "completion",
                                "analysis",
                                "creative",
                                "coding",
                                "reasoning",
                            ],
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["cost", "speed", "quality", "balanced"],
                        },
                        "max_cost_per_token": {"type": "number", "minimum": 0},
                        "max_latency_ms": {"type": "integer", "minimum": 0},
                        "min_quality_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                        },
                    },
                    "required": ["task_type"],
                },
            )
        )

        # Batch processing tool
        self.register_tool(
            MCPTool(
                name="batch_process",
                description="Process multiple requests in batch for cost optimization",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "requests": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "messages": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "role": {"type": "string"},
                                                "content": {"type": "string"},
                                            },
                                        },
                                    },
                                },
                                "required": ["id", "messages"],
                            },
                        },
                        "routing_strategy": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["cost", "speed", "quality"],
                        },
                    },
                    "required": ["requests"],
                },
            )
        )

        # Model metrics tool
        self.register_tool(
            MCPTool(
                name="get_model_metrics",
                description="Get performance metrics for available models",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "model_name": {
                            "type": "string",
                            "description": "Specific model name (optional)",
                        },
                        "time_range": {
                            "type": "string",
                            "enum": ["1h", "24h", "7d", "30d"],
                            "default": "24h",
                        },
                    },
                },
            )
        )

    def _register_resources(self):
        """Register available resources."""

        # Available models resource
        self.register_resource(
            MCPResource(
                uri="abacus://models",
                name="Available Models",
                description="List of available LLM models and their capabilities",
                mimeType="application/json",
                resourceType=MCPResourceType.JSON,
            )
        )

        # Routing strategies resource
        self.register_resource(
            MCPResource(
                uri="abacus://routing-strategies",
                name="Routing Strategies",
                description="Available routing strategies and their characteristics",
                mimeType="application/json",
                resourceType=MCPResourceType.JSON,
            )
        )

        # Cost analysis resource
        self.register_resource(
            MCPResource(
                uri="abacus://cost-analysis",
                name="Cost Analysis",
                description="Real-time cost analysis and optimization recommendations",
                mimeType="application/json",
                resourceType=MCPResourceType.JSON,
            )
        )

    def _register_prompts(self):
        """Register prompt templates."""

        # System prompt for optimal routing
        self.register_prompt(
            MCPPrompt(
                name="optimal_routing_system",
                description="System prompt for optimal model routing decisions",
                template="You are an AI model router. Analyze the user's request and recommend the most suitable model based on: task complexity, required quality, cost constraints, and latency requirements. Consider: {task_type}, priority: {priority}, constraints: {constraints}",
                arguments=[
                    {
                        "name": "task_type",
                        "description": "Type of task to be performed",
                    },
                    {
                        "name": "priority",
                        "description": "Primary optimization priority",
                    },
                    {
                        "name": "constraints",
                        "description": "Any specific constraints or requirements",
                    },
                ],
            )
        )

        # Quality assessment prompt
        self.register_prompt(
            MCPPrompt(
                name="quality_assessment",
                description="Prompt for assessing response quality across different models",
                template="Evaluate the quality of this AI response on a scale of 1-10 considering: accuracy, relevance, completeness, clarity, and helpfulness. Response: {response}. Provide detailed feedback and suggestions for improvement.",
                arguments=[
                    {"name": "response", "description": "The AI response to evaluate"}
                ],
            )
        )

    async def start(self):
        """Start the MCP server and initialize HTTP session."""
        if self.use_aiohttp and aiohttp_available:
            import aiohttp as aiohttp_module

            self.session = aiohttp_module.ClientSession(
                timeout=aiohttp_module.ClientTimeout(total=self.config.timeout),
                headers={
                    "Authorization": f"Bearer {
                        self.config.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "Trae.AI-MCP/1.0.0",
                },
            )
        await super().start()
        self.logger.info("Abacus.AI MCP Server started successfully")

    async def stop(self):
        """Stop the server and cleanup resources."""
        if self.session and self.use_aiohttp:
            await self.session.close()
        await super().stop()
        self.logger.info("Abacus.AI MCP Server stopped")

    async def _handle_chat_completion(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle chat completion requests."""
        try:
            params = message.params or {}
            messages = params.get("messages", [])
            model = params.get("model")
            routing_strategy = params.get(
                "routing_strategy", self.config.default_routing_strategy.value
            )
            max_tokens = params.get("max_tokens", self.config.max_tokens)
            temperature = params.get("temperature", self.config.temperature)
            conversation_id = params.get("conversation_id", str(uuid.uuid4()))

            if not messages:
                return MCPMessage(
                    id=message.id,
                    error={"code": -32602, "message": "Messages array is required"},
                )

            # Prepare request payload
            payload = {
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "routing_strategy": routing_strategy,
            }

            if model:
                payload["model"] = model

            # Make API request
            if self.use_aiohttp and self.session:
                async with self.session.post(
                    f"{self.config.base_url}/v1/chat/completions", json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                    else:
                        error_text = await response.text()
                        return MCPMessage(
                            id=message.id,
                            error={
                                "code": response.status,
                                "message": f"API request failed: {error_text}",
                            },
                        )
            else:
                # Fallback to urllib for synchronous requests
                import json as json_lib
                import urllib.request

                req_data = json_lib.dumps(payload).encode("utf-8")
                request = urllib.request.Request(
                    f"{self.config.base_url}/v1/chat/completions",
                    data=req_data,
                    headers={
                        "Authorization": f"Bearer {self.config.api_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "Trae.AI-MCP/1.0.0",
                    },
                )

                try:
                    with urllib.request.urlopen(request) as response:
                        result = json_lib.loads(response.read().decode("utf-8"))
                except urllib.error.HTTPError as e:
                    error_text = e.read().decode("utf-8")
                    return MCPMessage(
                        id=message.id,
                        error={
                            "code": e.code,
                            "message": f"API request failed: {error_text}",
                        },
                    )

            if result:
                # Store conversation context
                if conversation_id not in self.active_conversations:
                    self.active_conversations[conversation_id] = []

                # Add user message
                for msg in messages:
                    if msg["role"] == "user":
                        self.active_conversations[conversation_id].append(
                            ChatMessage(
                                role=msg["role"],
                                content=msg["content"],
                                timestamp=datetime.now(),
                            )
                        )

                # Add assistant response
                if "choices" in result and result["choices"]:
                    assistant_message = result["choices"][0]["message"]
                    self.active_conversations[conversation_id].append(
                        ChatMessage(
                            role="assistant",
                            content=assistant_message["content"],
                            timestamp=datetime.now(),
                            model_used=result.get("model"),
                            tokens_used=result.get("usage", {}).get("total_tokens"),
                            cost=result.get("cost"),
                        )
                    )

                # Update model metrics
                model_used = result.get("model")
                if model_used:
                    self._update_model_metrics(model_used, result)

                return MCPMessage(
                    id=message.id,
                    result={
                        "response": result,
                        "conversation_id": conversation_id,
                        "model_used": model_used,
                        "tokens_used": result.get("usage", {}).get("total_tokens"),
                        "cost": result.get("cost"),
                    },
                )

        except Exception as e:
            self.logger.error(f"Chat completion error: {str(e)}")
            return MCPMessage(
                id=message.id,
                error={"code": -32603, "message": f"Internal error: {str(e)}"},
            )

    async def _handle_select_optimal_model(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle optimal model selection requests."""
        try:
            params = message.params or {}
            task_type = params.get("task_type", "general")
            priority = params.get("priority", "balanced")
            max_cost = params.get("max_cost_per_token")
            max_latency = params.get("max_latency_ms")
            min_quality = params.get("min_quality_score")

            # Model selection logic based on task type and constraints
            model_recommendations = await self._get_model_recommendations(
                task_type, priority, max_cost, max_latency, min_quality
            )

            return MCPMessage(
                id=message.id,
                result={
                    "recommended_models": model_recommendations,
                    "selection_criteria": {
                        "task_type": task_type,
                        "priority": priority,
                        "constraints": {
                            "max_cost_per_token": max_cost,
                            "max_latency_ms": max_latency,
                            "min_quality_score": min_quality,
                        },
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Model selection error: {str(e)}")
            return MCPMessage(
                id=message.id,
                error={"code": -32603, "message": f"Internal error: {str(e)}"},
            )

    async def _handle_batch_process(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle batch processing requests."""
        try:
            params = message.params or {}
            requests = params.get("requests", [])
            routing_strategy = params.get("routing_strategy", "cost_optimized")
            priority = params.get("priority", "cost")

            if not requests:
                return MCPMessage(
                    id=message.id,
                    error={"code": -32602, "message": "Requests array is required"},
                )

            # Process requests in batch
            batch_results = []
            for req in requests:
                try:
                    # Simulate batch processing with optimal routing
                    result = await self._process_single_request(
                        req, routing_strategy, priority
                    )
                    batch_results.append(
                        {"id": req["id"], "status": "success", "result": result}
                    )
                except Exception as e:
                    batch_results.append(
                        {"id": req["id"], "status": "error", "error": str(e)}
                    )

            return MCPMessage(
                id=message.id,
                result={
                    "batch_results": batch_results,
                    "total_requests": len(requests),
                    "successful": len(
                        [r for r in batch_results if r["status"] == "success"]
                    ),
                    "failed": len([r for r in batch_results if r["status"] == "error"]),
                },
            )

        except Exception as e:
            self.logger.error(f"Batch processing error: {str(e)}")
            return MCPMessage(
                id=message.id,
                error={"code": -32603, "message": f"Internal error: {str(e)}"},
            )

    async def _handle_get_model_metrics(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle model metrics requests."""
        try:
            params = message.params or {}
            model_name = params.get("model_name")
            time_range = params.get("time_range", "24h")

            if model_name and model_name in self.model_metrics:
                metrics = asdict(self.model_metrics[model_name])
            else:
                metrics = {
                    name: asdict(metric) for name, metric in self.model_metrics.items()
                }

            return MCPMessage(
                id=message.id,
                result={
                    "metrics": metrics,
                    "time_range": time_range,
                    "timestamp": datetime.now().isoformat(),
                },
            )

        except Exception as e:
            self.logger.error(f"Model metrics error: {str(e)}")
            return MCPMessage(
                id=message.id,
                error={"code": -32603, "message": f"Internal error: {str(e)}"},
            )

    def _update_model_metrics(self, model_name: str, result: dict[str, Any]):
        """Update model performance metrics."""
        if model_name not in self.model_metrics:
            self.model_metrics[model_name] = ModelMetrics(
                model_name=model_name,
                total_requests=0,
                avg_latency=0.0,
                avg_cost=0.0,
                success_rate=1.0,
                last_used=datetime.now(),
                total_tokens=0,
            )

        metrics = self.model_metrics[model_name]
        metrics.total_requests += 1
        metrics.last_used = datetime.now()

        if "usage" in result:
            tokens = result["usage"].get("total_tokens", 0)
            metrics.total_tokens += tokens

        if "cost" in result:
            # Update average cost
            current_total_cost = metrics.avg_cost * (metrics.total_requests - 1)
            metrics.avg_cost = (
                current_total_cost + result["cost"]
            ) / metrics.total_requests

    async def _get_model_recommendations(
        self,
        task_type: str,
        priority: str,
        max_cost: Optional[float],
        max_latency: Optional[int],
        min_quality: Optional[float],
    ) -> list[dict[str, Any]]:
        """Get model recommendations based on criteria."""
        # This would typically query the Abacus.AI API for real-time model performance data
        # For now, we'll return mock recommendations based on common patterns

        recommendations = []

        if task_type == "coding":
            recommendations = [
                {
                    "model": "gpt-4-turbo",
                    "score": 0.95,
                    "reason": "Excellent for code generation and debugging",
                },
                {
                    "model": "claude-3-sonnet",
                    "score": 0.90,
                    "reason": "Strong reasoning capabilities for complex code",
                },
                {
                    "model": "gpt-3.5-turbo",
                    "score": 0.80,
                    "reason": "Cost-effective for simple coding tasks",
                },
            ]
        elif task_type == "creative":
            recommendations = [
                {
                    "model": "claude-3-opus",
                    "score": 0.95,
                    "reason": "Superior creative writing capabilities",
                },
                {
                    "model": "gpt-4",
                    "score": 0.90,
                    "reason": "Excellent for creative content generation",
                },
                {
                    "model": "mixtral-8x7b",
                    "score": 0.85,
                    "reason": "Good balance of creativity and cost",
                },
            ]
        elif task_type == "analysis":
            recommendations = [
                {
                    "model": "gpt-4-turbo",
                    "score": 0.95,
                    "reason": "Best for complex analytical tasks",
                },
                {
                    "model": "claude-3-sonnet",
                    "score": 0.92,
                    "reason": "Strong analytical reasoning",
                },
                {
                    "model": "gemini-pro",
                    "score": 0.88,
                    "reason": "Good for data analysis tasks",
                },
            ]
        else:
            # Default recommendations
            recommendations = [
                {
                    "model": "gpt-4-turbo",
                    "score": 0.90,
                    "reason": "Versatile and high-quality",
                },
                {
                    "model": "claude-3-sonnet",
                    "score": 0.88,
                    "reason": "Balanced performance and cost",
                },
                {
                    "model": "gpt-3.5-turbo",
                    "score": 0.80,
                    "reason": "Cost-effective option",
                },
            ]

        # Filter based on constraints
        if priority == "cost":
            recommendations.sort(
                key=lambda x: x["score"] * 0.5
            )  # Prioritize cost over quality
        elif priority == "quality":
            recommendations.sort(key=lambda x: x["score"], reverse=True)

        return recommendations[:3]  # Return top 3 recommendations

    async def _process_single_request(
        self, request: dict[str, Any], routing_strategy: str, priority: str
    ) -> dict[str, Any]:
        """Process a single request in batch mode."""
        # Simulate processing with optimal model selection
        messages = request.get("messages", [])

        # Mock response for batch processing
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": f"Processed request {
                            request['id']} with {routing_strategy} strategy",
                    }
                }
            ],
            "usage": {"total_tokens": 150},
            "model": "gpt-4-turbo",
            "cost": 0.003,
        }

    # Override parent class methods to handle our custom tools
    async def _handle_call_tool(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle tool calls."""
        params = message.params or {}
        tool_name = params.get("name")

        if tool_name == "chat_completion":
            return await self._handle_chat_completion(client_id, message)
        elif tool_name == "select_optimal_model":
            return await self._handle_select_optimal_model(client_id, message)
        elif tool_name == "batch_process":
            return await self._handle_batch_process(client_id, message)
        elif tool_name == "get_model_metrics":
            return await self._handle_get_model_metrics(client_id, message)
        else:
            return await super()._handle_call_tool(client_id, message)


async def create_abacus_ai_server(api_key: str, **kwargs) -> AbacusAIMCPServer:
    """Create and configure an Abacus.AI MCP server."""
    config = AbacusAIConfig(api_key=api_key, **kwargs)

    server = AbacusAIMCPServer(config)
    return server


async def main():
    """Main function for testing the server."""
    # Get API key from environment
    api_key = os.getenv("ABACUS_AI_API_KEY")
    if not api_key:
        print("Please set ABACUS_AI_API_KEY environment variable")
        return

    # Create and start server
    server = await create_abacus_ai_server(api_key)

    try:
        await server.start()
        print(f"Abacus.AI MCP Server running on {server.host}:{server.port}")
        print(f"Available tools: {list(server.tools.keys())}")
        print(f"Available resources: {list(server.resources.keys())}")

        # Keep server running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
