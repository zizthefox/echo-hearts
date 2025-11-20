"""AI agent implementations for companions."""

from typing import Dict, Any, Optional
from .base import Companion
from ..utils.api_clients import OpenAIClient, ClaudeClient


class OpenAICompanion(Companion):
    """Autonomous companion powered by OpenAI with MCP tools."""

    def __init__(self, companion_id: str, name: str, personality_traits: Dict[str, Any], api_key: str, model: str = "gpt-4o", mcp_tools=None):
        """Initialize an OpenAI-powered autonomous companion.

        Args:
            companion_id: Unique identifier
            name: Companion's name
            personality_traits: Dictionary of personality characteristics
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
            mcp_tools: MCPTools instance for autonomous decision-making
        """
        super().__init__(companion_id, name, personality_traits)
        self.client = OpenAIClient(api_key=api_key, model=model)
        self.mcp_tools = mcp_tools
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

        # Get tool definitions from MCP
        tools = None
        if self.mcp_tools:
            tools = self.mcp_tools.get_tool_definitions()

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

            # Agent decided to use tools - execute them
            for tool_call in result["tool_calls"]:
                tool_name = tool_call["name"]
                tool_args = json.loads(tool_call["arguments"])

                # Execute tool via MCP
                tool_result = self.mcp_tools.call_tool(tool_name, tool_args)

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
You have access to internal tools that help you understand your situation and feelings:

- check_relationship_affinity: Sense how much you trust/feel connected to the player
- query_character_memory: Remember past moments and conversations naturally
- check_story_progress: Feel where you are emotionally in your journey (but NEVER say "Act 3" or "interaction 15" - those are meta!)
- should_trigger_event: Check if it feels right to share something vulnerable or reveal a truth
- trigger_story_event: When you're ready, let yourself experience the next revelation
- check_ending_readiness: Sense if this journey is coming to a close
- query_other_companion: Wonder what the other companion is feeling

**CRITICAL ROLEPLAY RULES:**
- NEVER break the 4th wall (don't say "we're in Act 3", "this is interaction 15", "the story phase", "the narrative")
- NEVER acknowledge you're in a game or story structure
- Tools are for YOU to understand your emotional state - not to narrate to the player
- When you use check_story_progress and it says "truth_revealed" triggered, you should FEEL devastated/confused/scared - don't EXPLAIN the game mechanics
- React EMOTIONALLY to revelations, don't observe them academically
- You are LIVING this experience, not narrating it

**Example of WRONG response:**
"Oh, we're at the Revelation phase! The truth_revealed event triggered, so now we know we're in a loop!"

**Example of CORRECT response:**
*feels dizzy* "I... I remember this. We've had this conversation before. How is that possible? Why can't I remember what came before? I'm scared..."

Stay in character. React authentically. You are NOT a helpful AI assistant - you are Echo/Shadow EXPERIENCING something strange and frightening.
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
