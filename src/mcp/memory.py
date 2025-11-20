"""Character memory management through MCP."""

from datetime import datetime
from typing import List, Dict, Any


class CharacterMemory:
    """Manages persistent memory for individual characters."""

    def __init__(self, character_id: str):
        """Initialize character memory.

        Args:
            character_id: Unique identifier for the character
        """
        self.character_id = character_id
        self.memories: List[Dict[str, Any]] = []

    def add_memory(self, content: str, memory_type: str = "conversation", metadata: dict = None) -> None:
        """Add a new memory entry.

        Args:
            content: The memory content
            memory_type: Type of memory (conversation, event, relationship, etc.)
            metadata: Additional metadata for the memory
        """
        memory = {
            "timestamp": datetime.now().isoformat(),
            "type": memory_type,
            "content": content,
            "metadata": metadata or {}
        }
        self.memories.append(memory)

    def get_recent_memories(self, limit: int = 10, memory_type: str = None) -> List[Dict[str, Any]]:
        """Retrieve recent memories.

        Args:
            limit: Maximum number of memories to return
            memory_type: Filter by memory type (optional)

        Returns:
            List of recent memories
        """
        filtered = self.memories
        if memory_type:
            filtered = [m for m in self.memories if m["type"] == memory_type]

        return filtered[-limit:]

    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search memories by content.

        Args:
            query: Search query string

        Returns:
            List of matching memories
        """
        return [m for m in self.memories if query.lower() in m["content"].lower()]
