#!/usr/bin/env python3
"""Standalone MCP server for Echo Hearts.

This script runs the MCP server as a separate process that agents can connect to.
It communicates via stdio using the Model Context Protocol.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.game_mcp.server import EchoHeartsMCPServer


class StandaloneGameState:
    """Minimal game state implementation for standalone MCP server.

    In production, this would connect to a shared state store (Redis, etc.)
    For now, it maintains local state that will be synchronized via tool calls.
    """

    def __init__(self):
        """Initialize standalone game state."""
        from src.memory.relationships import RelationshipTracker
        from src.story.progression import StoryProgression
        from src.companions.base import Companion
        from src.memory.conversation import ConversationMemory

        self.relationships = RelationshipTracker()
        self.story = StoryProgression()
        self.conversation = ConversationMemory()
        self.companions = {}

        # Initialize basic companions for querying
        # These will be populated as the game runs
        self._initialize_companions()

    def _initialize_companions(self):
        """Initialize companion placeholders."""
        from src.companions.base import Companion

        # Create basic companion objects
        echo = Companion(
            companion_id="echo",
            name="Echo",
            personality_traits={"archetype": "optimistic"}
        )

        self.companions = {
            "echo": echo
        }

        # Initialize relationships
        self.relationships.update_relationship("player", "echo", 0.0)

    def get_relationships_summary(self):
        """Get relationship summary."""
        return {
            "echo": self.relationships.get_relationship("player", "echo")
        }


async def main():
    """Run the standalone MCP server."""
    # Create minimal game state
    game_state = StandaloneGameState()

    # Create and run MCP server
    server = EchoHeartsMCPServer(game_state)

    print("Echo Hearts MCP Server started", file=sys.stderr)
    print("Waiting for client connections...", file=sys.stderr)

    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
