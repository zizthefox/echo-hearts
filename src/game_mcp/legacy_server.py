"""MCP server setup and configuration."""

from typing import Optional, Dict, Any, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json


class EchoHeartsMCPServer:
    """Real MCP server that exposes game state tools to AI agents."""

    def __init__(self, game_state, name: str = "echo-hearts"):
        """Initialize the MCP server.

        Args:
            game_state: Reference to GameState instance
            name: Name of the MCP server
        """
        self.server = Server(name)
        self.game_state = game_state
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools with the server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available MCP tools."""
            return [
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
                                "description": "Your companion ID (echo or shadow)"
                            }
                        },
                        "required": ["player_message", "companion_id"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Execute a tool call and return results."""
            from ..mcp.tools import MCPTools

            # Get MCPTools instance from game state
            mcp_tools = MCPTools(self.game_state)

            # Execute the tool
            result = mcp_tools.call_tool(name, arguments)

            # Return as TextContent
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

    async def run(self):
        """Run the MCP server via stdio."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )
