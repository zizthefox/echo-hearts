"""Game state management."""

from typing import Dict, List, Optional, Tuple
from .mcp.server import MCPServer
from .mcp.tools import MCPTools
from .companions.agents import OpenAICompanion
from .companions.personalities import get_personality
from .memory.conversation import ConversationHistory
from .memory.relationships import RelationshipTracker
from .story.progression import StoryProgress, StoryEvent, Ending
from .story.endings import get_ending_narrative
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
        self.story = StoryProgress()

        # MCP tools for autonomous agents
        self.mcp_tools = MCPTools(self)

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
                personality_traits=personality,  # Pass full personality dict including character_profile
                api_key=config.openai_api_key,
                model=config.default_model,
                mcp_tools=self.mcp_tools  # Provide MCP tools to agent
            )
            self.companions[comp_config["id"]] = companion

            # Create MCP context for this companion
            self.mcp_server.create_context(comp_config["id"])

            # Initialize relationship with player
            self.relationships.update_relationship("player", comp_config["id"], 0.0)

    async def process_message(self, message: str, companion_id: str = "echo") -> Tuple[str, Optional[StoryEvent], Optional[str], List]:
        """Process a user message and get autonomous companion response.

        Args:
            message: User's message
            companion_id: Which companion to respond

        Returns:
            Tuple of (response, triggered_event, ending_narrative, tool_calls_made)
        """
        # Add message to conversation history
        self.conversation.add_message("User", message)

        # Record story interaction (but agents may override event triggering)
        triggered_event = self.story.add_interaction()

        # Get companion
        companion = self.companions.get(companion_id)
        if not companion:
            return f"Companion '{companion_id}' not found.", None, None, []

        # Add story context to the response - INCLUDE triggered event and all past events
        story_context = {
            "act": self.story.current_act.name,
            "act_context": self.story.get_act_context(),
            "interaction_count": self.story.interaction_count,
            "triggered_event": triggered_event,  # Event happening RIGHT NOW
            "events_triggered": self.story.events_triggered  # ALL past events (persistent state)
        }

        # Generate AUTONOMOUS response (agent makes own decisions using MCP tools)
        result = await companion.respond(message, context=story_context)

        # Extract response and tool usage
        response_text = result.get("response", "") if isinstance(result, dict) else result
        tool_calls_made = result.get("tool_calls_made", []) if isinstance(result, dict) else []

        # Add response to conversation history
        self.conversation.add_message(companion.name, response_text)

        # Update relationship (small positive change for interaction)
        self.relationships.update_relationship(
            "player",
            companion_id,
            0.01,
            reason="conversation"
        )

        # Check for ending
        ending_narrative = None
        if self.story.interaction_count >= 18:
            relationships_dict = self.get_relationships_summary()
            ending = self.story.determine_ending(relationships_dict)
            if ending:
                ending_narrative = get_ending_narrative(ending)

        return response_text, triggered_event, ending_narrative, tool_calls_made

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