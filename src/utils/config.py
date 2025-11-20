"""Configuration management."""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration."""

    def __init__(self):
        """Initialize configuration by loading .env file."""
        load_dotenv()

        # API Keys
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Application settings
        self.data_dir = os.getenv("DATA_DIR", "data")
        self.default_model = os.getenv("DEFAULT_MODEL", "claude-3-5-sonnet-20241022")
        self.max_conversation_history = int(os.getenv("MAX_CONVERSATION_HISTORY", "50"))

    def validate(self) -> bool:
        """Validate that required configuration is present.

        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.anthropic_api_key:
            print("Warning: ANTHROPIC_API_KEY not set")
            return False

        return True

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service.

        Args:
            service: Service name (anthropic, elevenlabs, openai, gemini)

        Returns:
            API key if available, None otherwise
        """
        keys = {
            "anthropic": self.anthropic_api_key,
            "elevenlabs": self.elevenlabs_api_key,
            "openai": self.openai_api_key,
            "gemini": self.gemini_api_key
        }
        return keys.get(service.lower())


# Global config instance
config = Config()
