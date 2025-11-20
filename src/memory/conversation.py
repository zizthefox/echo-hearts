"""Conversation history management."""

from typing import List, Dict, Any
from datetime import datetime


class ConversationHistory:
    """Manages conversation history for a session."""

    def __init__(self, session_id: str):
        """Initialize conversation history.

        Args:
            session_id: Unique identifier for the session
        """
        self.session_id = session_id
        self.messages: List[Dict[str, Any]] = []
        self.created_at = datetime.now()

    def add_message(self, speaker: str, content: str, metadata: dict = None) -> None:
        """Add a message to the conversation history.

        Args:
            speaker: Who spoke (user, companion name, system)
            content: The message content
            metadata: Additional metadata for the message
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "content": content,
            "metadata": metadata or {}
        }
        self.messages.append(message)

    def get_messages(self, limit: int = None, speaker: str = None) -> List[Dict[str, Any]]:
        """Retrieve messages from history.

        Args:
            limit: Maximum number of messages to return (most recent)
            speaker: Filter by speaker (optional)

        Returns:
            List of messages
        """
        filtered = self.messages
        if speaker:
            filtered = [m for m in self.messages if m["speaker"] == speaker]

        if limit:
            return filtered[-limit:]
        return filtered

    def get_context_window(self, max_messages: int = 20) -> str:
        """Get recent conversation as a formatted string.

        Args:
            max_messages: Maximum number of recent messages to include

        Returns:
            Formatted conversation context
        """
        recent = self.get_messages(limit=max_messages)
        return "\n".join([f"{m['speaker']}: {m['content']}" for m in recent])

    def clear(self) -> None:
        """Clear all messages from history."""
        self.messages = []
