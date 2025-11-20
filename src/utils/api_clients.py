"""API client wrappers for external services."""

from typing import Optional, List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic


class OpenAIClient:
    """Wrapper for OpenAI API."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            model: Model to use
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto"
    ) -> Dict[str, Any]:
        """Generate a response using OpenAI with optional function calling.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            tools: Optional list of tool definitions for function calling
            tool_choice: When to use tools ("auto", "none", or specific function)

        Returns:
            Dictionary with 'content' and optionally 'tool_calls'
        """
        try:
            # Prepend system message if provided
            formatted_messages = []
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})
            formatted_messages.extend(messages)

            # Build API call parameters
            params = {
                "model": self.model,
                "messages": formatted_messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }

            # Add tools if provided
            if tools:
                params["tools"] = tools
                params["tool_choice"] = tool_choice

            response = self.client.chat.completions.create(**params)
            message = response.choices[0].message

            result = {
                "content": message.content or "",
                "tool_calls": []
            }

            # Extract tool calls if any
            if hasattr(message, 'tool_calls') and message.tool_calls:
                result["tool_calls"] = [
                    {
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                    for tc in message.tool_calls
                ]

            return result

        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "content": "I'm having trouble responding right now.",
                "tool_calls": []
            }


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


def create_openai_client(api_key: str, model: str = "gpt-4o") -> OpenAIClient:
    """Factory function to create an OpenAI client.

    Args:
        api_key: OpenAI API key
        model: Model to use

    Returns:
        Configured OpenAIClient instance
    """
    return OpenAIClient(api_key=api_key, model=model)


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
