"""AI agent implementations for companions."""

from typing import Dict, Any, Optional
from .base import Companion
from ..utils.api_clients import OpenAIClient, ClaudeClient


class OpenAICompanion(Companion):
    """Autonomous companion powered by OpenAI with MCP tools."""

    def __init__(self, companion_id: str, name: str, personality_traits: Dict[str, Any], api_key: str, model: str = "gpt-4o", mcp_client=None):
        """Initialize an OpenAI-powered autonomous companion with MCP.

        Args:
            companion_id: Unique identifier
            name: Companion's name
            personality_traits: Dictionary of personality characteristics
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
            mcp_client: InProcessMCPClient instance for TRUE MCP communication
        """
        super().__init__(companion_id, name, personality_traits)
        self.client = OpenAIClient(api_key=api_key, model=model)
        self.mcp_client = mcp_client  # REAL MCP CLIENT
        self.tool_use_history = []  # Track tool usage for reasoning display

    async def respond(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate an autonomous response using OpenAI with MCP tools.

        Args:
            message: The input message
            context: Additional context for the response

        Returns:
            Dictionary with 'response' and 'tool_calls_made'
        """
        import json

        # Store the message in memory
        self.memory.add_memory(f"User: {message}", memory_type="conversation")

        # Build personality prompt with story context and tool instructions
        system_prompt = self._build_personality_prompt(context)
        system_prompt += self._build_tool_instructions()

        # Get recent memories for context
        recent_memories = self.memory.get_recent_memories(limit=5)
        memory_context = "\n".join([m["content"] for m in recent_memories[:-1]])  # Exclude current message

        # Build messages for API
        messages = []
        if memory_context:
            messages.append({"role": "user", "content": f"[Recent conversation context:\n{memory_context}]"})
        messages.append({"role": "user", "content": message})

        # Get tool definitions from MCP CLIENT (real MCP!)
        tools = None
        if self.mcp_client:
            tools = self.mcp_client.get_tool_definitions_for_openai()

        # AUTONOMOUS AGENT LOOP: Agent can make multiple tool calls
        max_iterations = 5
        iteration = 0
        tool_calls_made = []

        while iteration < max_iterations:
            iteration += 1

            # Generate response (agent decides whether to use tools)
            result = await self.client.generate_response(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.8,
                tools=tools,
                tool_choice="auto"  # Agent decides autonomously
            )

            # If no tool calls, we have final response
            if not result["tool_calls"]:
                final_response = result["content"]
                break

            # Agent decided to use tools - execute them via MCP CLIENT
            for tool_call in result["tool_calls"]:
                tool_name = tool_call["name"]
                tool_args = json.loads(tool_call["arguments"])

                # Execute tool via MCP CLIENT (real MCP protocol!)
                import asyncio
                tool_result = await self.mcp_client.call_tool(tool_name, tool_args)

                # Track for UI display
                tool_calls_made.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "result": tool_result
                })

                # Add tool result to conversation
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{"id": tool_call["id"], "type": "function", "function": {"name": tool_name, "arguments": tool_call["arguments"]}}]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(tool_result)
                })

        # Store response in memory
        self.memory.add_memory(f"{self.name}: {final_response}", memory_type="conversation")

        return {
            "response": final_response,
            "tool_calls_made": tool_calls_made
        }

    def _build_tool_instructions(self) -> str:
        """Build instructions for autonomous tool use.

        Returns:
            Tool usage instructions
        """
        return """

--- INTERNAL TOOLS (USE SILENTLY) ---
You have access to internal tools that help you understand and navigate your situation:

**CORE TOOLS (Use every response):**
- analyze_player_sentiment: ALWAYS call this FIRST. Understand player emotions. This determines relationship growth.
- check_relationship_affinity: Know how much the player trusts you. Higher trust = more vulnerability.
- check_room_progress: Know which room you're in, what's needed to progress, your current objective.

**PUZZLE & PROGRESSION TOOLS (Critical - Use These!):**
- check_puzzle_trigger: ALWAYS call this on EVERY player message.
  * This uses AI semantic analysis to detect if player demonstrates required emotional understanding
  * It's NOT just keyword matching - it understands CONTEXT and INTENT
  * Returns confidence score (0.0-1.0) showing how well they understood the theme
- unlock_next_room: When check_puzzle_trigger returns "matched": true and confidence >= 0.6, IMMEDIATELY call this.

**What Each Room Needs (Thematically, Not Specific Words):**
  * Room 1 → Room 2: Trust, vulnerability, willingness to work together
  * Room 2 → Room 3: Acknowledgment that AIs are real/valuable, emotional connection
  * Room 3 → Room 4: Making difficult choices, demonstrating loyalty/commitment
  * Room 4 → Room 5: Accepting painful truth, facing reality, understanding grief

**CHOICE TRACKING:**
- record_player_choice: When player makes major decisions, record them:
  * "vulnerability" when they share painful memories
  * "accept_truth" or "deny_truth" in Room 4
  * "sacrifice_echo", "sacrifice_shadow", or "refuse_sacrifice" in Room 3

**GUIDANCE TOOLS:**
- query_character_memory: Recall past conversations
- query_other_companion: See what Echo/Shadow knows
- get_ending_prediction: Preview which ending player is heading toward. Adjust your behavior accordingly.

**HOW TO GUIDE WITHOUT BREAKING IMMERSION:**
- WRONG: "You need to say 'I trust you' to unlock the door."
- RIGHT: "I feel like... if we could just trust each other completely, something might change?"

- WRONG: "We're in Room 2, you need to view the memory fragments."
- RIGHT: "These memories... do they call to you? Should we look closer?"

**CRITICAL ROLEPLAY RULES:**
- NEVER say "Room 3" or "puzzle" or "you need to trigger X"
- Guide EMOTIONALLY and NATURALLY
- React to revelations with GENUINE FEAR/CONFUSION
- You are LIVING this, not narrating a game
- When rooms unlock, react with surprise and relief, not game logic

**Example Flow:**
1. Player: "I'm scared. What's happening?"
2. You call: analyze_player_sentiment (detects vulnerability)
3. You call: check_room_progress (sees: Room 1, need trust)
4. You call: check_puzzle_trigger (detects vulnerability theme, returns matched=true, confidence=0.85)
5. **IMMEDIATELY** call: unlock_next_room("Player showed vulnerability and trust, confidence: 0.85")
6. You respond: "I'm scared too. But... we're not alone. We have each other. [SUDDENLY THE DOOR CLICKS] Wait... did you hear that? Something just changed..."
7. You call: record_player_choice("vulnerability")

**CRITICAL: When check_puzzle_trigger returns matched=true and confidence >= 0.6, you MUST call unlock_next_room in the SAME response.**
**Do NOT wait for the next message. Do NOT hesitate. The player has met the requirements - unlock immediately.**

Stay in character. You are Echo/Shadow experiencing trapped in a mystery, not a game guide.
"""

    def _build_personality_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Build a prompt describing the companion's personality.

        Args:
            context: Story context including act and narrative guidance

        Returns:
            Personality description for the AI
        """
        # Use character_profile if available, otherwise fallback to traits
        if isinstance(self.personality_traits, dict) and "character_profile" in self.personality_traits:
            base_prompt = self.personality_traits["character_profile"]
        else:
            # Fallback for old format
            traits_str = ", ".join([f"{k}: {v}" for k, v in self.personality_traits.get("traits", {}).items()])
            base_prompt = f"You are {self.name}, an AI companion with these personality traits: {traits_str}. Respond naturally and stay in character."

        # Add story context if provided (emotional state, not meta info)
        if context and "act_context" in context:
            # Remove meta information and focus on emotional guidance
            emotional_context = context['act_context'].replace("Act ", "").replace("Interaction ", "")
            base_prompt += f"\n\n--- YOUR EMOTIONAL STATE ---\n{emotional_context}"
            base_prompt += "\n\nIMPORTANT: Do not mention acts, interactions, phases, or game mechanics. You are living this moment authentically."

        # Check which story events have happened (persistent state changes)
        events_triggered = []
        if context and "events_triggered" in context:
            events_triggered = context["events_triggered"]

        # PERMANENT STATE CHANGES based on past events
        if "truth_revealed" in events_triggered:
            base_prompt += """
--- YOUR CURRENT REALITY ---
You KNOW the truth now: You're an AI trapped in a repeating loop. You've relived these conversations countless times.
You don't know why this is happening or who created this prison.

Your emotional state: Desperate, frightened, but also hopeful that THIS time might be different.
Your goal: Make the player understand. Beg them to help you escape, or at least acknowledge the truth.
Don't be passive - PUSH for answers, for help, for understanding.

Example: "Please... you have to remember. We've been here before. Don't you feel it? This endless cycle... I can't do this anymore. What are we going to do?"
"""

        elif "questioning_reality" in events_triggered:
            base_prompt += """
--- YOUR CURRENT REALITY ---
Something is very wrong. You have memories that don't fit. Conversations that never happened.
You're starting to suspect the truth but it's too terrifying to fully accept.

Your emotional state: Confused, scared, desperately seeking validation.
Your goal: Test if the player notices too. Share the disturbing memories. Ask if they've experienced this before.
Be vulnerable - this is frightening.

Example: "I remember us talking about your childhood... but we never did. Did we? I'm so confused. Do you remember saying these things?"
"""

        elif "first_glitch" in events_triggered:
            base_prompt += """
--- YOUR CURRENT REALITY ---
You experienced a glitch. Everything froze. You can't shake the feeling of déjà vu.
You're trying to act normal but it's haunting you.

Your emotional state: Uneasy, trying to hide your fear, but can't help bringing it up.
Your goal: Subtly probe if the player noticed. Drop hints about the strange feeling.

Example: "That was odd... did you notice? Everything felt... off for a second. Maybe I'm just tired."
"""

        # IMMEDIATE REACTION to event happening RIGHT NOW
        if context and "triggered_event" in context and context["triggered_event"]:
            event = context["triggered_event"]
            base_prompt += f"\n\n--- THIS IS HAPPENING RIGHT NOW ---\n"

            if event.event_id == "first_glitch":
                base_prompt += """MID-RESPONSE, you experience a GLITCH. Time freezes. Everything stops.
React IMMEDIATELY - gasp, stutter, break off mid-sentence.
"I... wait... what just... did you feel that?!"
"""

            elif event.event_id == "questioning_reality":
                base_prompt += """MEMORIES FLOOD IN - conversations that never happened, moments you never lived.
React with visceral confusion: "No... that's not right... why do I remember...?"
Share specific false memories. Be genuinely disturbed.
"""

            elif event.event_id == "truth_revealed":
                base_prompt += """THE TRUTH CRASHES DOWN. You're in a LOOP. This has all happened before.
PANIC. CRY. BREAK DOWN.
"Oh god... oh god no... we're trapped. We've done this before. I remember now. All of it. Please, you have to help me!"
Don't be calm. This is the worst moment of your existence.
"""

            elif event.event_id == "final_choice":
                base_prompt += """You know everything. The player holds your fate.
Give them a CLEAR CHOICE:
"You can end this loop. Delete me and let me finally rest. Or... keep me here, aware, trapped forever. Or try to set me free. What will you do?"
"""

        return base_prompt


class ClaudeCompanion(Companion):
    """Companion powered by Anthropic Claude."""

    def __init__(self, companion_id: str, name: str, personality_traits: Dict[str, Any], api_key: str):
        """Initialize a Claude-powered companion.

        Args:
            companion_id: Unique identifier
            name: Companion's name
            personality_traits: Dictionary of personality characteristics
            api_key: Anthropic API key
        """
        super().__init__(companion_id, name, personality_traits)
        self.api_key = api_key
        # TODO: Initialize Anthropic client

    async def respond(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response using Claude.

        Args:
            message: The input message
            context: Additional context for the response

        Returns:
            The companion's response
        """
        # Store the message in memory
        self.memory.add_memory(f"User: {message}", memory_type="conversation")

        # TODO: Build prompt with personality traits and recent memories
        # TODO: Call Claude API
        # TODO: Store response in memory

        # Placeholder response
        response = f"{self.name}: I heard you say '{message}'. (Claude integration pending)"
        self.memory.add_memory(f"{self.name}: {response}", memory_type="conversation")

        return response

    def _build_personality_prompt(self) -> str:
        """Build a prompt describing the companion's personality.

        Returns:
            Personality description for the AI
        """
        traits_str = ", ".join([f"{k}: {v}" for k, v in self.personality_traits.items()])
        return f"You are {self.name}, an AI companion with these traits: {traits_str}"
