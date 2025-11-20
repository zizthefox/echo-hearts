"""API client wrappers for external services."""

from typing import Optional, List, Dict, Any
from anthropic import Anthropic


class ClaudeClient:
    """Wrapper for Anthropic Claude API."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize Claude client.

        Args:
            api_key: Anthropic API key
            model: Model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """Generate a response using Claude.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated response text
        """
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)
            return response.content[0].text

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble responding right now."


class ElevenLabsClient:
    """Wrapper for ElevenLabs voice synthesis API."""

    def __init__(self, api_key: str):
        """Initialize ElevenLabs client.

        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        # TODO: Initialize ElevenLabs client when needed

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str = "default"
    ) -> Optional[bytes]:
        """Synthesize speech from text.

        Args:
            text: Text to synthesize
            voice_id: Voice to use

        Returns:
            Audio data as bytes, or None if failed
        """
        # TODO: Implement ElevenLabs integration
        print(f"Voice synthesis requested: {text[:50]}...")
        return None


def create_claude_client(api_key: str, model: str = "claude-3-5-sonnet-20241022") -> ClaudeClient:
    """Factory function to create a Claude client.

    Args:
        api_key: Anthropic API key
        model: Model to use

    Returns:
        Configured ClaudeClient instance
    """
    return ClaudeClient(api_key=api_key, model=model)


def create_elevenlabs_client(api_key: str) -> ElevenLabsClient:
    """Factory function to create an ElevenLabs client.

    Args:
        api_key: ElevenLabs API key

    Returns:
        Configured ElevenLabsClient instance
    """
    return ElevenLabsClient(api_key=api_key)
