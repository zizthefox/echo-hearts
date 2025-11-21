"""Base companion class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..game_mcp.memory import CharacterMemory


class Companion(ABC):
    """Base class for AI companions."""

    def __init__(self, companion_id: str, name: str, personality_traits: Dict[str, Any]):
        """Initialize a companion.

        Args:
            companion_id: Unique identifier
            name: Companion's name
            personality_traits: Dictionary of personality characteristics
        """
        self.companion_id = companion_id
        self.name = name
        self.personality_traits = personality_traits
        self.memory = CharacterMemory(companion_id)
        self.relationships: Dict[str, float] = {}  # companion_id -> affinity score

    @abstractmethod
    async def respond(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response to a message.

        Args:
            message: The input message
            context: Additional context for the response

        Returns:
            The companion's response
        """
        pass

    def update_relationship(self, other_companion_id: str, change: float) -> None:
        """Update relationship affinity with another companion.

        Args:
            other_companion_id: ID of the other companion
            change: Change in affinity (-1.0 to 1.0)
        """
        current = self.relationships.get(other_companion_id, 0.0)
        self.relationships[other_companion_id] = max(-1.0, min(1.0, current + change))

    def get_relationship(self, other_companion_id: str) -> float:
        """Get relationship affinity with another companion.

        Args:
            other_companion_id: ID of the other companion

        Returns:
            Affinity score (-1.0 to 1.0)
        """
        return self.relationships.get(other_companion_id, 0.0)
