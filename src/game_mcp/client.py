"""MCP client for connecting agents to the MCP server."""

import asyncio
import json
from typing import Dict, Any, List, Optional
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """Client for connecting to Echo Hearts MCP server."""

    def __init__(self):
        """Initialize the MCP client."""
        self.session: Optional[ClientSession] = None
        self.available_tools: List[Dict[str, Any]] = []

    async def connect(self, server_script_path: str):
        """Connect to the MCP server.

        Args:
            server_script_path: Path to the MCP server script
        """
        # Start server process via stdio
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session

                # Initialize the connection
                await session.initialize()

                # List available tools
                tools_result = await session.list_tools()
                self.available_tools = [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema
                    }
                    for tool in tools_result.tools
                ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments for the tool

        Returns:
            Tool result as dictionary
        """
        if not self.session:
            raise RuntimeError("MCP client not connected. Call connect() first.")

        # Call the tool via MCP
        result = await self.session.call_tool(tool_name, arguments)

        # Parse the result
        if result.content and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return json.loads(content.text)

        return {"error": "No result from tool"}

    def get_tool_definitions_for_openai(self) -> List[Dict[str, Any]]:
        """Get tool definitions in OpenAI function calling format.

        Returns:
            List of tool definitions for OpenAI API
        """
        openai_tools = []

        for tool in self.available_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["inputSchema"]
                }
            })

        return openai_tools

    async def close(self):
        """Close the MCP client connection."""
        if self.session:
            await self.session.__aexit__(None, None, None)
            self.session = None


class MCPClientSync:
    """Synchronous wrapper for MCPClient to use in sync contexts."""

    def __init__(self):
        """Initialize the sync MCP client wrapper."""
        self.client = MCPClient()
        self.loop = None

    def connect(self, server_script_path: str):
        """Connect to the MCP server synchronously.

        Args:
            server_script_path: Path to the MCP server script
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.client.connect(server_script_path))

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool synchronously.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool result
        """
        if not self.loop:
            raise RuntimeError("Client not connected")

        return self.loop.run_until_complete(
            self.client.call_tool(tool_name, arguments)
        )

    def get_tool_definitions_for_openai(self) -> List[Dict[str, Any]]:
        """Get tool definitions for OpenAI.

        Returns:
            List of tool definitions
        """
        return self.client.get_tool_definitions_for_openai()

    def close(self):
        """Close the connection."""
        if self.loop:
            self.loop.run_until_complete(self.client.close())
            self.loop.close()
            self.loop = None
