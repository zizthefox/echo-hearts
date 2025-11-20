"""MCP server setup and configuration."""

from typing import Optional


class MCPServer:
    """MCP server for managing character contexts and memory."""

    def __init__(self):
        """Initialize the MCP server."""
        self.contexts = {}

    def create_context(self, character_id: str) -> dict:
        """Create a new context for a character.

        Args:
            character_id: Unique identifier for the character

        Returns:
            The created context dictionary
        """
        context = {
            "character_id": character_id,
            "memory": [],
            "relationships": {},
            "personality_state": {}
        }
        self.contexts[character_id] = context
        return context

    def get_context(self, character_id: str) -> Optional[dict]:
        """Retrieve context for a character.

        Args:
            character_id: Unique identifier for the character

        Returns:
            The character's context or None if not found
        """
        return self.contexts.get(character_id)

    def update_context(self, character_id: str, updates: dict) -> bool:
        """Update a character's context.

        Args:
            character_id: Unique identifier for the character
            updates: Dictionary of updates to apply

        Returns:
            True if successful, False if character not found
        """
        if character_id not in self.contexts:
            return False

        self.contexts[character_id].update(updates)
        return True
