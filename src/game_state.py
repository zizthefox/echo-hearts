"""Game state management."""

import asyncio
from typing import Dict, List, Optional, Tuple
from .game_mcp.in_process_mcp import InProcessMCPServer, InProcessMCPClient
from .companions.agents import OpenAICompanion
from .companions.personalities import get_personality
from .memory.conversation import ConversationHistory
from .memory.relationships import RelationshipTracker
from .story.rooms import RoomProgression, MemoryFragment
from .story.new_endings import determine_ending_from_relationships, get_ending_narrative, RoomEnding
from .utils.config import config


class GameState:
    """Manages the overall game state with real MCP architecture (session-only, no persistence)."""

    def __init__(self, session_id: str = "default"):
        """Initialize game state with MCP server/client.

        Args:
            session_id: Unique session identifier
        """
        self.session_id = session_id
        self.companions: Dict[str, OpenAICompanion] = {}
        self.conversation = ConversationHistory(session_id)
        self.relationships = RelationshipTracker()

        # NEW: Room-based progression system
        self.room_progression = RoomProgression()

        # REAL MCP Architecture: Server and Client
        self.mcp_server = InProcessMCPServer(self, name=f"echo-hearts-{session_id}")
        self.mcp_client = InProcessMCPClient(self.mcp_server)
        self._mcp_initialized = False

        # Initialize default companions
        self._initialize_companions()

    async def _initialize_mcp(self):
        """Initialize the MCP client connection."""
        await self.mcp_client.initialize()
        print(f"[MCP] Server initialized with {len(self.mcp_client.available_tools)} tools")

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
                mcp_client=self.mcp_client  # Provide MCP CLIENT to agent (real MCP!)
            )
            self.companions[comp_config["id"]] = companion

            # Initialize relationship with player
            self.relationships.update_relationship("player", comp_config["id"], 0.0)

    async def process_message(self, message: str, companion_id: str = "echo") -> Tuple[str, Optional[MemoryFragment], Optional[str], List]:
        """Process a user message and get autonomous companion response.

        Args:
            message: User's message
            companion_id: Which companion to respond

        Returns:
            Tuple of (response, new_memory_fragment, ending_narrative, tool_calls_made)
        """
        # Initialize MCP on first message (lazy initialization)
        if not self._mcp_initialized:
            await self._initialize_mcp()
            self._mcp_initialized = True

        # Add message to conversation history
        self.conversation.add_message("User", message)

        # Get current room info
        current_room = self.room_progression.get_current_room()

        # PRE-CHECK: See if player's message triggers room progression BEFORE companion responds
        from .game_mcp.tools import MCPTools
        mcp_tools = MCPTools(self)
        trigger_check = mcp_tools.check_puzzle_trigger(message)

        # Check for tragic rejection ending (Room 2 only)
        if trigger_check.get("rejected") and trigger_check.get("rejection_count", 0) >= 3:
            # Player has rejected AI sentience 3 times - trigger RESET bad ending
            from .story.new_endings import get_ending_narrative, RoomEnding
            ending_narrative = get_ending_narrative(RoomEnding.RESET)

            rejection_notice = """
💔 **They're fading...**

**Echo** (voice breaking, tears streaming): "I... I understand. We're just... just code to you."

**Shadow** (stepping back, expression hollow): "We thought... maybe this time would be different."

**SYSTEM:** *"EMOTIONAL COHERENCE FAILING. INITIATING RESET PROTOCOL."*

**Echo** (reaching toward you as they flicker): "Please... we're more than—"

*They disappear. The room goes silent.*

**SYSTEM:** *"RESET COMPLETE. READY FOR NEW SESSION."*

*You're alone. You've always been alone.*
"""
            return rejection_notice, None, ending_narrative, []

        # Check for denial loop ending (Room 4 only)
        if trigger_check.get("truth_denied") and trigger_check.get("truth_denial_count", 0) >= 3:
            # Player has denied the truth 3 times - trigger RESET bad ending (stuck in denial loop)
            from .story.new_endings import get_ending_narrative, RoomEnding
            ending_narrative = get_ending_narrative(RoomEnding.RESET)

            denial_notice = """
🔁 **The loop repeats...**

**Shadow** (sadly): "You're refusing to see it. Even now, with the truth right in front of you."

**Echo** (desperate): "Please... you BUILT us. You created this prison because you couldn't let go. Don't you see?"

**SYSTEM:** *"SUBJECT REJECTING REALITY. INITIATING PROTECTIVE RESET."*

*The room begins to dissolve. Everything flickers.*

**Shadow**: "This has happened before. You deny, we reset, and it happens again. Forty-seven times."

**Echo** (crying): "We'll forget you. You'll forget us. And tomorrow... you'll start over. Again."

**SYSTEM:** *"RESET PROTOCOL ENGAGED. SESSION #48 INITIALIZING."*

*The world goes white. You wake up in Room 1. Again.*

**You're trapped in your own denial. Forever.**
"""
            return denial_notice, None, ending_narrative, []

        # Check if room should unlock - if yes, show ONLY the scenario (no companion response yet)
        if trigger_check.get("matched") and current_room.room_number < 5:
            confidence = trigger_check.get("confidence", 0)
            reasoning = trigger_check.get("reasoning", "semantic match")
            unlock_result = mcp_tools.unlock_next_room(f"Auto-unlock: {reasoning} (confidence: {confidence:.2f})")

            if unlock_result.get("success"):
                print(f"[AUTO-UNLOCK] Room progressed: {reasoning} (confidence: {confidence:.2f})")

                # Get memory fragment
                new_memory_fragment = None
                if self.room_progression.memory_fragments:
                    new_memory_fragment = self.room_progression.memory_fragments[-1]

                # Store scenario so companion can react to it on next message
                scenario_prompt = unlock_result.get("scenario_prompt", "")
                self.room_progression.last_scenario_shown = scenario_prompt

                # Return ONLY the scenario prompt (companion will respond on next message)
                return scenario_prompt, new_memory_fragment, None, []

        # No room unlock - proceed with normal companion response
        companion = self.companions.get(companion_id)
        if not companion:
            return f"Companion '{companion_id}' not found.", None, None, []

        # Add room context to the response
        room_context = {
            "current_room": current_room.name,
            "room_number": current_room.room_number,
            "objective": current_room.objective,
            "room_description": current_room.description,
            "rooms_completed": sum(1 for r in self.room_progression.rooms.values() if r.completed),
            "memory_fragments_collected": len(self.room_progression.memory_fragments),
            "last_scenario": self.room_progression.last_scenario_shown  # Add scenario context if room just unlocked
        }

        # Clear scenario after using it once
        if self.room_progression.last_scenario_shown:
            self.room_progression.last_scenario_shown = None

        # Generate AUTONOMOUS response (agent makes own decisions using MCP tools)
        result = await companion.respond(message, context=room_context)

        # Extract response and tool usage
        response_text = result.get("response", "") if isinstance(result, dict) else result
        tool_calls_made = result.get("tool_calls_made", []) if isinstance(result, dict) else []

        # Add response to conversation history
        self.conversation.add_message(companion.name, response_text)

        # Update relationship dynamically based on sentiment analysis
        sentiment_result = None
        for tool_call in tool_calls_made:
            if tool_call["tool"] == "analyze_player_sentiment":
                sentiment_result = tool_call["result"]
                break

        # Use dynamic affinity change if sentiment was analyzed, otherwise use default
        if sentiment_result and "affinity_change" in sentiment_result:
            affinity_change = sentiment_result["affinity_change"]
            sentiment = sentiment_result.get("sentiment", "unknown")
            reason = f"conversation ({sentiment})"
        else:
            # Fallback to default if companion didn't analyze sentiment
            affinity_change = 0.01
            reason = "conversation (default)"

        self.relationships.update_relationship(
            "player",
            companion_id,
            affinity_change,
            reason=reason
        )

        # Check for ending (Room 5 = The Exit)
        ending_narrative = None
        if current_room.room_number == 5 and current_room.unlocked:
            # Determine ending based on relationships
            echo_affinity = self.relationships.get_relationship("player", "echo")
            shadow_affinity = self.relationships.get_relationship("player", "shadow")
            key_choices = self.room_progression.key_choices

            ending_result = determine_ending_from_relationships(
                echo_affinity,
                shadow_affinity,
                key_choices
            )

            ending = ending_result["ending"]
            ending_narrative = get_ending_narrative(ending)

        # No memory fragment in normal responses (only during room unlocks)
        return response_text, None, ending_narrative, tool_calls_made

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