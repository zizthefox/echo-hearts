"""AI agent implementations for companions."""

from typing import Dict, Any, Optional
from .base import Companion
from ..utils.api_clients import OpenAIClient, ClaudeClient


class OpenAICompanion(Companion):
    """Companion powered by OpenAI."""

    def __init__(self, companion_id: str, name: str, personality_traits: Dict[str, Any], api_key: str, model: str = "gpt-4o"):
        """Initialize an OpenAI-powered companion.

        Args:
            companion_id: Unique identifier
            name: Companion's name
            personality_traits: Dictionary of personality characteristics
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
        """
        super().__init__(companion_id, name, personality_traits)
        self.client = OpenAIClient(api_key=api_key, model=model)

    async def respond(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response using OpenAI.

        Args:
            message: The input message
            context: Additional context for the response

        Returns:
            The companion's response
        """
        # Store the message in memory
        self.memory.add_memory(f"User: {message}", memory_type="conversation")

        # Build personality prompt with story context
        system_prompt = self._build_personality_prompt(context)

        # Get recent memories for context
        recent_memories = self.memory.get_recent_memories(limit=5)
        memory_context = "\n".join([m["content"] for m in recent_memories[:-1]])  # Exclude current message

        # Build messages for API
        messages = []
        if memory_context:
            messages.append({"role": "system", "content": f"Recent conversation:\n{memory_context}"})
        messages.append({"role": "user", "content": message})

        # Generate response
        response = await self.client.generate_response(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.8
        )

        # Store response in memory
        self.memory.add_memory(f"{self.name}: {response}", memory_type="conversation")

        return response

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

        # Add story context if provided
        if context and "act_context" in context:
            base_prompt += f"\n\n--- STORY CONTEXT ---\n{context['act_context']}"
            base_prompt += f"\n(This is interaction {context.get('interaction_count', 0)}/20 in The Echo Protocol)"

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
