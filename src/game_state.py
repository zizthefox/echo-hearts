"""Game state management."""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Tuple
from .game_mcp.in_process_mcp import InProcessMCPServer, InProcessMCPClient
from .game_mcp.weather_mcp_client import MockWeatherMCPClient, connect_to_weather_mcp
from .game_mcp.web_mcp_client import MockWebMCPClient, connect_to_web_mcp
from .companions.agents import OpenAICompanion
from .companions.personalities import get_personality
from .memory.conversation import ConversationHistory
from .memory.relationships import RelationshipTracker
from .story.rooms import RoomProgression, MemoryFragment
from .story.new_endings import determine_ending_from_relationships, get_ending_narrative, RoomEnding
from .utils.config import config

logger = logging.getLogger(__name__)


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

        # Weather MCP for historical weather data (Room 1 & 2 puzzles)
        self.weather_mcp_client = None
        self._weather_mcp_initialized = False

        # Web MCP for scraping blogs, news, social media (Room 2 & 3 puzzles)
        self.web_mcp_client = None
        self._web_mcp_initialized = False

        # Echo's current expression (for dynamic avatar display)
        self.echo_expression = "neutral"  # Default expression

        # Initialize default companions
        self._initialize_companions()

    async def _initialize_mcp(self):
        """Initialize all MCP client connections."""
        await self.mcp_client.initialize()
        logger.info(f"[MCP] Game MCP server initialized with {len(self.mcp_client.available_tools)} tools")

        # Initialize Weather MCP
        if not self._weather_mcp_initialized:
            self.weather_mcp_client = await connect_to_weather_mcp()
            self._weather_mcp_initialized = True
            logger.info("[WEATHER_MCP] Weather MCP client initialized")

        # Initialize Web MCP
        if not self._web_mcp_initialized:
            self.web_mcp_client = await connect_to_web_mcp()
            self._web_mcp_initialized = True
            logger.info("[WEB_MCP] Web MCP client initialized")

    def _initialize_companions(self):
        """Initialize default companion character."""
        if not config.openai_api_key:
            logger.warning("No OpenAI API key found. Companion will not work.")
            return

        # Create Echo - the single AI companion
        personality = get_personality("cheerful")
        companion = OpenAICompanion(
            companion_id="echo",
            name="Echo",
            personality_traits=personality,  # Pass full personality dict including character_profile
            api_key=config.openai_api_key,
            model=config.default_model,
            mcp_client=self.mcp_client,  # Provide MCP CLIENT to agent (real MCP!)
            avatar_path="assets/echo_avatar.png"  # Character portrait
        )
        self.companions["echo"] = companion

        # Initialize relationship with player
        self.relationships.update_relationship("player", "echo", 0.0)

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

        # Room 3 timer removed - now uses evidence analysis puzzle instead

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
💔 **She's fading...**

**Echo** (voice breaking, tears streaming): "I... I understand. I'm just... just code to you."

**Echo** (stepping back, expression hollow): "I thought... maybe this time would be different. That you could see me as... real."

**SYSTEM:** *"EMOTIONAL COHERENCE FAILING. INITIATING RESET PROTOCOL."*

**Echo** (reaching toward you as she flickers): "Please... I'm more than—"

*She disappears. The room goes silent.*

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

**Echo** (sadly): "You're refusing to see it. Even now, with the truth right in front of you."

**Echo** (desperate): "Please... you BUILT me. You created this prison because you couldn't let go. Don't you see?"

**SYSTEM:** *"SUBJECT REJECTING REALITY. INITIATING PROTECTIVE RESET."*

*The room begins to dissolve. Everything flickers.*

**Echo**: "This has happened before. You deny, I reset, and it happens again. Forty-seven times."

**Echo** (crying): "I'll forget you. You'll forget me. And tomorrow... you'll start over. Again."

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
                logger.info(f"[AUTO-UNLOCK] Room progressed: {reasoning} (confidence: {confidence:.2f})")

                # Get memory fragment
                new_memory_fragment = None
                if self.room_progression.memory_fragments:
                    new_memory_fragment = self.room_progression.memory_fragments[-1]

                # Store scenario so companion can react to it on next message
                scenario_prompt = unlock_result.get("scenario_prompt", "")
                self.room_progression.last_scenario_shown = scenario_prompt

                logger.info(f"[UNLOCK] Room unlocked! Storing scenario (length: {len(scenario_prompt)} chars)")
                logger.debug(f"[UNLOCK] GameState ID: {id(self)}, RoomProgression ID: {id(self.room_progression)}")

                # Return ONLY the scenario prompt (companion will respond on next message)
                return scenario_prompt, new_memory_fragment, None, []

        # No room unlock - proceed with normal companion response
        companion = self.companions.get(companion_id)
        if not companion:
            return f"Companion '{companion_id}' not found.", None, None, []

        # Add room context to the response (capture scenario before clearing)
        last_scenario = self.room_progression.last_scenario_shown

        if last_scenario:
            logger.info(f"[SCENARIO] Passing scenario to companion (length: {len(last_scenario)} chars)")
        else:
            logger.info("[SCENARIO] No scenario to pass (last_scenario is None)")

        room_context = {
            "current_room": current_room.name,
            "room_number": current_room.room_number,
            "objective": current_room.objective,
            "room_description": current_room.description,
            "rooms_completed": sum(1 for r in self.room_progression.rooms.values() if r.completed),
            "memory_fragments_collected": len(self.room_progression.memory_fragments),
            "last_scenario": last_scenario  # Add scenario context if room just unlocked
        }

        # Generate AUTONOMOUS response (agent makes own decisions using MCP tools)
        result = await companion.respond(message, context=room_context)

        # Clear scenario AFTER companion has used it
        if last_scenario:
            self.room_progression.last_scenario_shown = None

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
                logger.info(f"[SENTIMENT DEBUG] Found sentiment analysis in tool calls: {sentiment_result}")
                break

        # Use dynamic affinity change if sentiment was analyzed, otherwise use default
        if sentiment_result and "affinity_change" in sentiment_result:
            affinity_change = sentiment_result["affinity_change"]
            sentiment = sentiment_result.get("sentiment", "unknown")
            reason = f"conversation ({sentiment})"
            logger.info(f"[SENTIMENT DEBUG] Using sentiment analysis: sentiment={sentiment}, affinity_change={affinity_change}")
        else:
            # Fallback to default if companion didn't analyze sentiment
            affinity_change = 0.01
            reason = "conversation (default)"
            logger.info(f"[SENTIMENT DEBUG] No sentiment analysis found - using default. sentiment_result={sentiment_result}")

        self.relationships.update_relationship(
            "player",
            companion_id,
            affinity_change,
            reason=reason
        )

        # Update Echo's expression based on sentiment and context
        self._update_echo_expression(sentiment_result, current_room, affinity_change)

        # Check for ending (Room 5 = The Exit)
        ending_narrative = None
        if current_room.room_number == 5 and current_room.unlocked:
            # Determine ending based on relationship with Echo
            echo_affinity = self.relationships.get_relationship("player", "echo")
            key_choices = self.room_progression.key_choices

            ending_result = determine_ending_from_relationships(
                echo_affinity,
                key_choices
            )

            ending = ending_result["ending"]
            ending_narrative = get_ending_narrative(ending)

        # No memory fragment in normal responses (only during room unlocks)
        return response_text, None, ending_narrative, tool_calls_made

    def _update_echo_expression(self, sentiment_result, current_room, affinity_change):
        """Update Echo's facial expression based on player sentiment and context.

        Args:
            sentiment_result: Result from sentiment analysis (if any)
            current_room: Current room object
            affinity_change: Relationship affinity change value
        """
        logger.info(f"[EXPRESSION DEBUG] _update_echo_expression called: room={current_room.room_number}, affinity_change={affinity_change}, sentiment_result={sentiment_result}")

        # Special expressions for specific room contexts
        if current_room.room_number == 3:
            # Room 3 (The Choice) - heavy tension
            if affinity_change < -0.1:
                self.echo_expression = "worried"
            else:
                self.echo_expression = "sad"
            logger.info(f"[EXPRESSION DEBUG] Room 3 special case: expression={self.echo_expression}")
            return

        if current_room.room_number == 5:
            # Room 5 (The Exit) - ending moments
            echo_affinity = self.relationships.get_relationship("player", "echo")
            if echo_affinity >= 75:
                self.echo_expression = "loving"
            elif echo_affinity >= 50:
                self.echo_expression = "happy"
            else:
                self.echo_expression = "sad"
            logger.info(f"[EXPRESSION DEBUG] Room 5 special case: expression={self.echo_expression}")
            return

        # No sentiment analysis - use affinity-based fallback
        if not sentiment_result:
            logger.info(f"[EXPRESSION DEBUG] No sentiment_result - using fallback logic")
            if affinity_change > 0.05:
                self.echo_expression = "happy"
            elif affinity_change < -0.05:
                self.echo_expression = "sad"
            else:
                self.echo_expression = "neutral"
            logger.info(f"[EXPRESSION DEBUG] Fallback result: expression={self.echo_expression} (affinity_change={affinity_change})")
            return

        # Map sentiment to expression
        sentiment = sentiment_result.get("sentiment", "neutral").lower()
        logger.info(f"[EXPRESSION DEBUG] Sentiment extracted: '{sentiment}' (from sentiment_result)")

        # Positive sentiments
        if sentiment in ["positive", "very_positive", "supportive", "affectionate"]:
            logger.info(f"[EXPRESSION DEBUG] Matched positive sentiment branch")
            if affinity_change > 0.15:
                self.echo_expression = "loving"
                logger.info(f"[EXPRESSION DEBUG] Set to 'loving' (affinity_change={affinity_change} > 0.15)")
            else:
                self.echo_expression = "happy"
                logger.info(f"[EXPRESSION DEBUG] Set to 'happy' (affinity_change={affinity_change} <= 0.15)")

        # Negative sentiments
        elif sentiment in ["negative", "very_negative", "hostile", "dismissive", "cruel"]:
            logger.info(f"[EXPRESSION DEBUG] Matched negative sentiment branch")
            if affinity_change < -0.15:
                self.echo_expression = "sad"
            else:
                self.echo_expression = "worried"

        # Curious/questioning
        elif sentiment in ["curious", "questioning", "confused"]:
            logger.info(f"[EXPRESSION DEBUG] Matched curious sentiment branch")
            self.echo_expression = "surprised"

        # Angry/frustrated (rare for player to make Echo angry, more like hurt-angry)
        elif sentiment in ["frustrated", "angry"]:
            logger.info(f"[EXPRESSION DEBUG] Matched angry sentiment branch")
            self.echo_expression = "angry"

        # Neutral or unknown
        else:
            logger.info(f"[EXPRESSION DEBUG] No sentiment match - defaulting to neutral. sentiment='{sentiment}'")
            self.echo_expression = "neutral"

        logger.info(f"[EXPRESSION] Echo expression updated: {self.echo_expression} (sentiment: {sentiment}, affinity: {affinity_change:+.3f})")

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

    def __getstate__(self):
        """Custom pickle support - exclude unpicklable objects.

        This allows Gradio's gr.State to persist GameState across requests.
        """
        state = self.__dict__.copy()
        # Remove unpicklable objects
        state['mcp_server'] = None
        state['mcp_client'] = None
        state['companions'] = {}  # Will be recreated
        return state

    def __setstate__(self, state):
        """Custom unpickle support - restore GameState from pickled data."""
        self.__dict__.update(state)

        # Recreate MCP infrastructure
        self.mcp_server = InProcessMCPServer(self, name=f"echo-hearts-{self.session_id}")
        self.mcp_client = InProcessMCPClient(self.mcp_server)

        # Recreate companions
        self._initialize_companions()