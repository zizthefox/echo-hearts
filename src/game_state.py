"""Game state management."""

from typing import Dict, List, Optional
from .mcp.server import MCPServer
from .companions.agents import OpenAICompanion
from .companions.personalities import get_personality
from .memory.conversation import ConversationHistory
from .memory.relationships import RelationshipTracker
from .utils.config import config


class GameState:
    """Manages the overall game state (session-only, no persistence)."""

    def __init__(self, session_id: str = "default"):
        """Initialize game state.

        Args:
            session_id: Unique session identifier
        """
        self.session_id = session_id
        self.mcp_server = MCPServer()
        self.companions: Dict[str, OpenAICompanion] = {}
        self.conversation = ConversationHistory(session_id)
        self.relationships = RelationshipTracker()

        # Initialize default companions
        self._initialize_companions()

    def _initialize_companions(self):
        """Initialize default companion characters."""
        if not config.openai_api_key:
            print("Warning: No OpenAI API key found. Companions will not work.")
            return

        # Create two initial companions
        companions_config = [
            {
                "id": "echo",
                "name": "Echo",
                "personality_type": "cheerful"
            },
            {
                "id": "shadow",
                "name": "Shadow",
                "personality_type": "mysterious"
            }
        ]

        for comp_config in companions_config:
            personality = get_personality(comp_config["personality_type"])
            companion = OpenAICompanion(
                companion_id=comp_config["id"],
                name=comp_config["name"],
                personality_traits=personality["traits"],
                api_key=config.openai_api_key,
                model=config.default_model
            )
            self.companions[comp_config["id"]] = companion

            # Create MCP context for this companion
            self.mcp_server.create_context(comp_config["id"])

            # Initialize relationship with player
            self.relationships.update_relationship("player", comp_config["id"], 0.0)

    async def process_message(self, message: str, companion_id: str = "echo") -> str:
        """Process a user message and get companion response.

        Args:
            message: User's message
            companion_id: Which companion to respond

        Returns:
            Companion's response
        """
        # Add message to conversation history
        self.conversation.add_message("User", message)

        # Get companion
        companion = self.companions.get(companion_id)
        if not companion:
            return f"Companion '{companion_id}' not found."

        # Generate response
        response = await companion.respond(message)

        # Add response to conversation history
        self.conversation.add_message(companion.name, response)

        # Update relationship (small positive change for interaction)
        self.relationships.update_relationship(
            "player",
            companion_id,
            0.01,
            reason="conversation"
        )

        return response

    def get_companion_list(self) -> List[Dict[str, str]]:
        """Get list of active companions.

        Returns:
            List of companion info dictionaries
        """
        return [
            {
                "id": comp_id,
                "name": companion.name,
                "personality": str(companion.personality_traits)
            }
            for comp_id, companion in self.companions.items()
        ]

    def get_relationships_summary(self) -> Dict[str, float]:
        """Get player relationships with all companions.

        Returns:
            Dictionary of companion_id to affinity scores
        """
        return self.relationships.get_all_relationships("player")