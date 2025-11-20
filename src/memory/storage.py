"""Persistence layer for saving and loading game state."""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class StorageManager:
    """Manages saving and loading of game state."""

    def __init__(self, data_dir: str = "data"):
        """Initialize the storage manager.

        Args:
            data_dir: Directory to store save files
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save a game session.

        Args:
            session_id: Unique session identifier
            session_data: Session data to save

        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = os.path.join(self.data_dir, f"{session_id}.json")
            session_data["last_saved"] = datetime.now().isoformat()

            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a game session.

        Args:
            session_id: Unique session identifier

        Returns:
            Session data if found, None otherwise
        """
        try:
            filepath = os.path.join(self.data_dir, f"{session_id}.json")

            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r') as f:
                return json.load(f)

        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def list_sessions(self) -> list:
        """List all saved sessions.

        Returns:
            List of session IDs
        """
        try:
            files = os.listdir(self.data_dir)
            return [f.replace('.json', '') for f in files if f.endswith('.json')]
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []

    def delete_session(self, session_id: str) -> bool:
        """Delete a saved session.

        Args:
            session_id: Unique session identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = os.path.join(self.data_dir, f"{session_id}.json")

            if os.path.exists(filepath):
                os.remove(filepath)
                return True

            return False
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
