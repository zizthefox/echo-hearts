"""In-process MCP server/client for Echo Hearts.

This provides a true MCP implementation that runs within the same process,
making it suitable for Hugging Face Spaces deployment while still using
the actual Model Context Protocol for agent-tool communication.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp import ClientSession
from mcp.client.session import ClientSession as BaseClientSession


class InProcessMCPServer:
    """MCP server that runs in-process but uses real MCP protocol."""

    def __init__(self, game_state, name: str = "echo-hearts"):
        """Initialize the in-process MCP server.

        Args:
            game_state: Reference to GameState instance
            name: Name of the MCP server
        """
        self.server = Server(name)
        self.game_state = game_state
        self._tools_list: List[Tool] = []
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools with the server."""

        # Build tools list
        tools = [
                Tool(
                    name="check_relationship_affinity",
                    description="Check the current relationship affinity between the companion and another entity (usually 'player'). Use this to decide how vulnerable or open to be in responses.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "companion_id": {
                                "type": "string",
                                "description": "Your companion ID (echo)"
                            },
                            "target_id": {
                                "type": "string",
                                "description": "The entity to check relationship with (usually 'player')"
                            }
                        },
                        "required": ["companion_id", "target_id"]
                    }
                ),
                Tool(
                    name="query_character_memory",
                    description="Search your own memories for specific topics or past conversations. Use this to maintain continuity and reference past interactions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "character_id": {
                                "type": "string",
                                "description": "Your character ID (echo)"
                            },
                            "query": {
                                "type": "string",
                                "description": "What to search for in memories"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum memories to return",
                                "default": 5
                            }
                        },
                        "required": ["character_id", "query"]
                    }
                ),
                Tool(
                    name="check_story_progress",
                    description="Check current story state including act, interaction count, and events triggered. Use this to understand where you are in the narrative.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="should_trigger_event",
                    description="Check if a specific story event should be triggered now. Use this to decide whether the player is ready for a revelation.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "event_id": {
                                "type": "string",
                                "description": "Event to check",
                                "enum": ["first_glitch", "questioning_reality", "truth_revealed", "final_choice"]
                            }
                        },
                        "required": ["event_id"]
                    }
                ),
                Tool(
                    name="trigger_story_event",
                    description="Trigger a story event NOW. Only use after checking should_trigger_event and determining player is ready.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "event_id": {
                                "type": "string",
                                "description": "Event to trigger",
                                "enum": ["first_glitch", "questioning_reality", "truth_revealed", "final_choice"]
                            },
                            "intensity": {
                                "type": "string",
                                "description": "How intense to make the reveal",
                                "enum": ["subtle", "moderate", "dramatic"],
                                "default": "moderate"
                            }
                        },
                        "required": ["event_id"]
                    }
                ),
                Tool(
                    name="check_ending_readiness",
                    description="Check if story can end and which ending is most likely. Use this to know if you should start wrapping up conversations.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="query_other_companion",
                    description="Ask another companion about the player or coordinate reveals. Use this to share information between agents.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "companion_id": {
                                "type": "string",
                                "description": "Which companion to query (echo)"
                            },
                            "question": {
                                "type": "string",
                                "description": "What to ask them"
                            }
                        },
                        "required": ["companion_id", "question"]
                    }
                ),
                Tool(
                    name="analyze_player_sentiment",
                    description="Analyze the emotional tone of the player's message to understand how they're feeling about you. Use this to decide how much affinity should change based on their response.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "player_message": {
                                "type": "string",
                                "description": "The player's message to analyze"
                            },
                            "companion_id": {
                                "type": "string",
                                "description": "Your companion ID (echo)"
                            }
                        },
                        "required": ["player_message", "companion_id"]
                    }
                ),
                Tool(
                    name="check_room_progress",
                    description="Check which room you're currently in and what's needed to progress. Use this to understand the current situation and guide the player.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="check_puzzle_trigger",
                    description="Check if the player's message contains keywords that might trigger room progression. Use this to see if they're getting close to solving the puzzle.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "player_message": {
                                "type": "string",
                                "description": "The player's message to check"
                            }
                        },
                        "required": ["player_message"]
                    }
                ),
                Tool(
                    name="unlock_next_room",
                    description="Attempt to unlock the next room. Only use this when you're confident the player has met the requirements (said the right things, made the right choices).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "reason": {
                                "type": "string",
                                "description": "Why you think the room should unlock now"
                            }
                        },
                        "required": ["reason"]
                    }
                ),
                Tool(
                    name="record_player_choice",
                    description="Record an important player choice that will affect the ending. Use this for major decisions like sacrifice, accepting truth, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "choice_type": {
                                "type": "string",
                                "description": "Type of choice",
                                "enum": ["sacrifice_echo", "refuse_sacrifice", "accept_truth", "deny_truth", "vulnerability"]
                            },
                            "choice_value": {
                                "type": "string",
                                "description": "Details about the choice"
                            }
                        },
                        "required": ["choice_type"]
                    }
                ),
                Tool(
                    name="get_ending_prediction",
                    description="Based on current relationships and choices, predict which ending the player is heading toward. Use this to guide your roleplay and responses.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]

        # Store tools list
        self._tools_list = tools

        # Register handler that returns our tools list
        @self.server.list_tools()
        async def list_tools_handler() -> list[Tool]:
            """List all available MCP tools."""
            return self._tools_list

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Execute a tool call and return results."""
            from .tools import MCPTools

            # Get MCPTools instance
            mcp_tools = MCPTools(self.game_state)

            # Execute the tool
            result = mcp_tools.call_tool(name, arguments)

            # Return as TextContent per MCP spec
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

    async def list_tools_direct(self) -> List[Tool]:
        """Direct access to list tools (for in-process use).

        Returns:
            List of Tool objects
        """
        # Return the cached tools list directly
        return self._tools_list

    async def call_tool_direct(self, name: str, arguments: dict) -> Dict[str, Any]:
        """Direct access to call tools (for in-process use).

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result as dict
        """
        import logging
        from mcp.types import CallToolRequest, CallToolRequestParams
        logger = logging.getLogger(__name__)

        logger.info(f"[MCP CALL DEBUG] call_tool_direct called: name={name}, arguments={arguments}")

        # Use proper MCP protocol: get the CallToolRequest handler
        handler = self.server.request_handlers.get(CallToolRequest)
        logger.info(f"[MCP CALL DEBUG] Handler type: {type(handler)}")

        if not handler:
            logger.error(f"[MCP CALL DEBUG] No CallToolRequest handler registered")
            return {"error": "Tool handler not registered"}

        # Construct proper MCP request with params
        request = CallToolRequest(
            params=CallToolRequestParams(
                name=name,
                arguments=arguments
            )
        )

        logger.info(f"[MCP CALL DEBUG] Calling MCP handler with request: {request}")
        result = await handler(request)
        logger.info(f"[MCP CALL DEBUG] Handler returned: {result}")
        logger.info(f"[MCP CALL DEBUG] Result type: {type(result)}")

        # Extract text from ServerResult -> CallToolResult -> TextContent (MCP protocol format)
        # The handler returns a ServerResult wrapping CallToolResult
        if hasattr(result, 'root'):
            # ServerResult has a 'root' attribute containing CallToolResult
            tool_result = result.root
            logger.info(f"[MCP CALL DEBUG] Extracted tool_result: {tool_result}")

            if hasattr(tool_result, 'content') and len(tool_result.content) > 0:
                text_content = tool_result.content[0]
                logger.info(f"[MCP CALL DEBUG] TextContent: {text_content}")
                parsed = json.loads(text_content.text)
                logger.info(f"[MCP CALL DEBUG] Parsed result: {parsed}")
                return parsed

        logger.error(f"[MCP CALL DEBUG] Handler returned no valid results")
        return {"error": "Tool execution failed"}


class InProcessMCPClient:
    """MCP client that communicates with in-process server."""

    def __init__(self, server: InProcessMCPServer):
        """Initialize the in-process MCP client.

        Args:
            server: The in-process MCP server to connect to
        """
        self.server = server
        self.available_tools: List[Dict[str, Any]] = []

    async def initialize(self):
        """Initialize the client and fetch available tools."""
        # Get tools from server
        tools = await self.server.list_tools_direct()

        self.available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            }
            for tool in tools
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments for the tool

        Returns:
            Tool result as dictionary
        """
        return await self.server.call_tool_direct(tool_name, arguments)

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
