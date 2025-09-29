#!/usr/bin/env python3
"""
TRAE.AI Model Context Protocol (MCP) Implementation

Provides standardized AI model communication and context sharing
for the autonomous AI CEO framework. Enables seamless integration
between different AI models, agents, and external services.

Features:
- Standardized message protocol for AI model communication
- Context sharing and state management
- Tool registration and discovery
- Resource management and access control
- Real-time bidirectional communication
- Multi-model orchestration
- Context persistence and retrieval

Author: TRAE.AI System
Version: 1.0.0
"""

import json
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional, Union

try:
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


class MCPMessageType(Enum):
    """MCP message types."""

    # Core protocol messages
    INITIALIZE = "initialize"
    INITIALIZED = "initialized"
    PING = "ping"
    PONG = "pong"

    # Tool management
    LIST_TOOLS = "tools/list"
    CALL_TOOL = "tools/call"
    TOOL_RESULT = "tools/result"

    # Resource management
    LIST_RESOURCES = "resources/list"
    READ_RESOURCE = "resources/read"
    SUBSCRIBE_RESOURCE = "resources/subscribe"
    UNSUBSCRIBE_RESOURCE = "resources/unsubscribe"
    RESOURCE_UPDATED = "resources/updated"

    # Context management
    GET_CONTEXT = "context/get"
    SET_CONTEXT = "context/set"
    UPDATE_CONTEXT = "context/update"
    CLEAR_CONTEXT = "context/clear"

    # Prompt management
    LIST_PROMPTS = "prompts/list"
    GET_PROMPT = "prompts/get"

    # Notifications
    NOTIFICATION = "notification"
    ERROR = "error"

    # Custom extensions
    AGENT_REGISTER = "agent/register"
    AGENT_UNREGISTER = "agent/unregister"
    WORKFLOW_START = "workflow/start"
    WORKFLOW_STATUS = "workflow/status"
    WORKFLOW_COMPLETE = "workflow/complete"


class MCPCapability(Enum):
    """MCP server capabilities."""

    TOOLS = "tools"
    RESOURCES = "resources"
    PROMPTS = "prompts"
    LOGGING = "logging"
    SAMPLING = "sampling"
    CONTEXT = "context"
    WORKFLOWS = "workflows"
    AGENTS = "agents"


class MCPResourceType(Enum):
    """MCP resource types."""

    TEXT = "text"
    BINARY = "binary"
    JSON = "json"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    DATABASE = "database"
    API = "api"


@dataclass
class MCPMessage:
    """Base MCP message structure."""

    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: Optional[str] = None
    params: Optional[dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = {"jsonrpc": self.jsonrpc}

        if self.id is not None:
            data["id"] = self.id
        if self.method is not None:
            data["method"] = self.method
        if self.params is not None:
            data["params"] = self.params
        if self.result is not None:
            data["result"] = self.result
        if self.error is not None:
            data["error"] = self.error

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MCPMessage":
        """Create from dictionary."""
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            id=data.get("id"),
            method=data.get("method"),
            params=data.get("params"),
            result=data.get("result"),
            error=data.get("error"),
        )


@dataclass
class MCPTool:
    """MCP tool definition."""

    name: str
    description: str
    inputSchema: dict[str, Any]
    outputSchema: Optional[dict[str, Any]] = None
    handler: Optional[Callable] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class MCPResource:
    """MCP resource definition."""

    uri: str
    name: str
    description: str
    mimeType: str
    resourceType: MCPResourceType
    metadata: Optional[dict[str, Any]] = None
    content: Optional[Any] = None
    lastModified: Optional[datetime] = None


@dataclass
class MCPPrompt:
    """MCP prompt definition."""

    name: str
    description: str
    template: str
    arguments: Optional[list[dict[str, Any]]] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class MCPContext:
    """MCP context data."""

    id: str
    name: str
    data: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class MCPServerInfo:
    """MCP server information."""

    name: str
    version: str
    capabilities: list[MCPCapability]
    description: Optional[str] = None
    author: Optional[str] = None
    homepage: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class MCPServer:
    """
    Model Context Protocol (MCP) Server implementation.
    Provides standardized AI model communication and context sharing.
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        host: str = "localhost",
        port: int = 8765,
        capabilities: Optional[list[MCPCapability]] = None,
    ):
        # Import logger here to avoid circular imports
        try:
            from utils.logger import setup_logger

            self.logger = setup_logger(f"mcp_server_{name}")
        except ImportError:
            import logging

            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(f"mcp_server_{name}")

        # Server configuration
        self.info = MCPServerInfo(
            name=name,
            version=version,
            capabilities=capabilities
            or [MCPCapability.TOOLS, MCPCapability.RESOURCES, MCPCapability.CONTEXT],
            description=f"TRAE.AI MCP Server - {name}",
            author="TRAE.AI System",
        )

        self.host = host
        self.port = port

        # Registry for tools, resources, and prompts
        self.tools: dict[str, MCPTool] = {}
        self.resources: dict[str, MCPResource] = {}
        self.prompts: dict[str, MCPPrompt] = {}

        # Context storage
        self.contexts: dict[str, MCPContext] = {}

        # Client connections
        self.clients: dict[str, Any] = {}

        # Message handlers
        self.handlers: dict[str, Callable] = {
            MCPMessageType.INITIALIZE.value: self._handle_initialize,
            MCPMessageType.PING.value: self._handle_ping,
            MCPMessageType.LIST_TOOLS.value: self._handle_list_tools,
            MCPMessageType.CALL_TOOL.value: self._handle_call_tool,
            MCPMessageType.LIST_RESOURCES.value: self._handle_list_resources,
            MCPMessageType.READ_RESOURCE.value: self._handle_read_resource,
            MCPMessageType.LIST_PROMPTS.value: self._handle_list_prompts,
            MCPMessageType.GET_PROMPT.value: self._handle_get_prompt,
            MCPMessageType.GET_CONTEXT.value: self._handle_get_context,
            MCPMessageType.SET_CONTEXT.value: self._handle_set_context,
            MCPMessageType.UPDATE_CONTEXT.value: self._handle_update_context,
            MCPMessageType.CLEAR_CONTEXT.value: self._handle_clear_context,
        }

        # Server state
        self.running = False
        self.server = None

        # Thread pool for blocking operations
        self.executor = ThreadPoolExecutor(max_workers=10)

        self.logger.info(f"MCP Server '{name}' initialized")

    def register_tool(self, tool: MCPTool):
        """Register a tool with the server."""
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")

    def register_resource(self, resource: MCPResource):
        """Register a resource with the server."""
        self.resources[resource.uri] = resource
        self.logger.info(f"Registered resource: {resource.uri}")

    def register_prompt(self, prompt: MCPPrompt):
        """Register a prompt with the server."""
        self.prompts[prompt.name] = prompt
        self.logger.info(f"Registered prompt: {prompt.name}")

    async def start(self):
        """Start the MCP server."""
        self.running = True
        self.logger.info(f"MCP Server started on {self.host}:{self.port}")

    async def stop(self):
        """Stop the MCP server."""
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        self.executor.shutdown(wait=True)
        self.logger.info("MCP Server stopped")

    # Message handlers
    async def _handle_initialize(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle initialization request."""
        return MCPMessage(
            id=message.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": [cap.value for cap in self.info.capabilities],
                "serverInfo": {"name": self.info.name, "version": self.info.version},
            },
        )

    async def _handle_ping(self, client_id: str, message: MCPMessage) -> MCPMessage:
        """Handle ping request."""
        return MCPMessage(id=message.id, result={"pong": True})

    async def _handle_list_tools(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle list tools request."""
        tools = []
        for tool in self.tools.values():
            tool_data = {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema,
            }
            if tool.outputSchema:
                tool_data["outputSchema"] = tool.outputSchema
            tools.append(tool_data)

        return MCPMessage(id=message.id, result={"tools": tools})

    async def _handle_call_tool(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle tool call request."""
        params = message.params or {}
        tool_name = params.get("name")

        if not tool_name or tool_name not in self.tools:
            return MCPMessage(
                id=message.id,
                error={"code": -32602, "message": f"Tool '{tool_name}' not found"},
            )

        tool = self.tools[tool_name]

        try:
            if tool.handler:
                result = await tool.handler(params.get("arguments", {}))
                return MCPMessage(id=message.id, result=result)
            else:
                return MCPMessage(
                    id=message.id,
                    error={"code": -32603, "message": "Tool handler not implemented"},
                )
        except Exception as e:
            return MCPMessage(id=message.id, error={"code": -32603, "message": str(e)})

    async def _handle_list_resources(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle list resources request."""
        resources = []
        for resource in self.resources.values():
            resources.append(
                {
                    "uri": resource.uri,
                    "name": resource.name,
                    "description": resource.description,
                    "mimeType": resource.mimeType,
                }
            )

        return MCPMessage(id=message.id, result={"resources": resources})

    async def _handle_read_resource(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle read resource request."""
        params = message.params or {}
        uri = params.get("uri")

        if not uri or uri not in self.resources:
            return MCPMessage(
                id=message.id,
                error={"code": -32602, "message": f"Resource '{uri}' not found"},
            )

        resource = self.resources[uri]

        return MCPMessage(
            id=message.id,
            result={
                "contents": [
                    {
                        "uri": resource.uri,
                        "mimeType": resource.mimeType,
                        "text": (
                            resource.content
                            if isinstance(resource.content, str)
                            else json.dumps(resource.content)
                        ),
                    }
                ]
            },
        )

    async def _handle_list_prompts(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle list prompts request."""
        prompts = []
        for prompt in self.prompts.values():
            prompt_data = {"name": prompt.name, "description": prompt.description}
            if prompt.arguments:
                prompt_data["arguments"] = prompt.arguments
            prompts.append(prompt_data)

        return MCPMessage(id=message.id, result={"prompts": prompts})

    async def _handle_get_prompt(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle get prompt request."""
        params = message.params or {}
        name = params.get("name")

        if not name or name not in self.prompts:
            return MCPMessage(
                id=message.id,
                error={"code": -32602, "message": f"Prompt '{name}' not found"},
            )

        prompt = self.prompts[name]

        return MCPMessage(
            id=message.id,
            result={
                "description": prompt.description,
                "messages": [
                    {
                        "role": "user",
                        "content": {"type": "text", "text": prompt.template},
                    }
                ],
            },
        )

    async def _handle_get_context(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle get context request."""
        params = message.params or {}
        context_id = params.get("id")

        if context_id and context_id in self.contexts:
            context = self.contexts[context_id]
            return MCPMessage(
                id=message.id,
                result={
                    "context": {
                        "id": context.id,
                        "name": context.name,
                        "data": context.data,
                        "created_at": context.created_at.isoformat(),
                        "updated_at": context.updated_at.isoformat(),
                    }
                },
            )
        else:
            return MCPMessage(
                id=message.id, result={"contexts": list(self.contexts.keys())}
            )

    async def _handle_set_context(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle set context request."""
        params = message.params or {}
        context_id = params.get("id", str(uuid.uuid4()))
        name = params.get("name", f"context_{context_id}")
        data = params.get("data", {})

        now = datetime.now()
        context = MCPContext(
            id=context_id, name=name, data=data, created_at=now, updated_at=now
        )

        self.contexts[context_id] = context

        return MCPMessage(
            id=message.id, result={"success": True, "context_id": context_id}
        )

    async def _handle_update_context(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle update context request."""
        params = message.params or {}
        context_id = params.get("id")

        if not context_id or context_id not in self.contexts:
            return MCPMessage(
                id=message.id,
                error={"code": -32602, "message": f"Context '{context_id}' not found"},
            )

        context = self.contexts[context_id]

        if "name" in params:
            context.name = params["name"]
        if "data" in params:
            context.data.update(params["data"])

        context.updated_at = datetime.now()

        return MCPMessage(id=message.id, result={"success": True})

    async def _handle_clear_context(
        self, client_id: str, message: MCPMessage
    ) -> MCPMessage:
        """Handle clear context request."""
        params = message.params or {}
        context_id = params.get("id")

        if context_id:
            if context_id in self.contexts:
                del self.contexts[context_id]
                return MCPMessage(id=message.id, result={"success": True})
            else:
                return MCPMessage(
                    id=message.id,
                    error={
                        "code": -32602,
                        "message": f"Context '{context_id}' not found",
                    },
                )
        else:
            # Clear all contexts
            self.contexts.clear()
            return MCPMessage(id=message.id, result={"success": True})
