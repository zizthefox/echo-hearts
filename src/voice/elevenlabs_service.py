"""ElevenLabs voice synthesis service for Echo."""

import os
import base64
import logging
from typing import Optional
from elevenlabs import ElevenLabs, VoiceSettings

logger = logging.getLogger(__name__)


class EchoVoiceService:
    """Service for generating Echo's voice using ElevenLabs."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize ElevenLabs voice service.

        Args:
            api_key: ElevenLabs API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.client = None
        self.voice_enabled = False

        logger.info(f"[VOICE INIT] API key present: {bool(self.api_key)}, key starts with: {self.api_key[:10] if self.api_key else 'None'}")

        if self.api_key and self.api_key != "your_elevenlabs_key_here":
            try:
                self.client = ElevenLabs(api_key=self.api_key)
                self.voice_enabled = True
                logger.info("✓ [VOICE INIT] ElevenLabs voice service initialized successfully")
                print("✓ ElevenLabs voice service initialized")
            except Exception as e:
                logger.error(f"⚠ [VOICE INIT] ElevenLabs initialization failed: {e}", exc_info=True)
                print(f"⚠ ElevenLabs initialization failed: {e}")
                self.voice_enabled = False
        else:
            logger.warning("ℹ [VOICE INIT] ElevenLabs API key not configured - voice disabled")
            print("ℹ ElevenLabs API key not configured - voice disabled")

    def generate_speech(
        self,
        text: str,
        expression: str = "neutral",
        model: str = "eleven_turbo_v2_5"
    ) -> Optional[bytes]:
        """Generate speech audio from text.

        Args:
            text: Text to convert to speech
            expression: Echo's current expression (affects voice emotion)
            model: ElevenLabs model to use

        Returns:
            Audio bytes (MP3 format) or None if voice disabled
        """
        logger.info(f"[VOICE] generate_speech called: enabled={self.voice_enabled}, expression={expression}, text_length={len(text)}")

        if not self.voice_enabled or not self.client:
            logger.warning(f"[VOICE] Voice generation skipped: enabled={self.voice_enabled}, client={bool(self.client)}")
            return None

        try:
            # Map Echo's expressions to voice settings
            voice_settings = self._get_voice_settings_for_expression(expression)
            logger.info(f"[VOICE] Voice settings: stability={voice_settings.stability}, style={voice_settings.style}")

            # Use a feminine, warm voice (Rachel is good for emotional range)
            # You can customize this to any ElevenLabs voice ID
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice

            logger.info(f"[VOICE] Calling ElevenLabs API: voice_id={voice_id}, model={model}")

            # Generate audio
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model,
                voice_settings=voice_settings
            )

            # Collect audio bytes
            audio_bytes = b"".join(audio_generator)
            logger.info(f"[VOICE] ✓ Audio generated successfully: {len(audio_bytes)} bytes")
            return audio_bytes

        except Exception as e:
            logger.error(f"⚠ [VOICE] Voice generation failed: {e}", exc_info=True)
            print(f"⚠ Voice generation failed: {e}")
            return None

    def _get_voice_settings_for_expression(self, expression: str) -> VoiceSettings:
        """Get voice settings based on Echo's emotional expression.

        Args:
            expression: Echo's current expression

        Returns:
            VoiceSettings configured for the expression
        """
        # Map expressions to voice characteristics
        # stability: 0-1 (lower = more emotional variation)
        # similarity_boost: 0-1 (higher = more like original voice)
        # style: 0-1 (higher = more exaggerated)
        # use_speaker_boost: bool (enhance voice clarity)

        settings_map = {
            "happy": VoiceSettings(
                stability=0.4,
                similarity_boost=0.8,
                style=0.6,
                use_speaker_boost=True
            ),
            "sad": VoiceSettings(
                stability=0.7,
                similarity_boost=0.9,
                style=0.4,
                use_speaker_boost=True
            ),
            "worried": VoiceSettings(
                stability=0.5,
                similarity_boost=0.85,
                style=0.5,
                use_speaker_boost=True
            ),
            "surprised": VoiceSettings(
                stability=0.3,
                similarity_boost=0.75,
                style=0.7,
                use_speaker_boost=True
            ),
            "neutral": VoiceSettings(
                stability=0.6,
                similarity_boost=0.85,
                style=0.5,
                use_speaker_boost=True
            ),
        }

        return settings_map.get(expression, settings_map["neutral"])

    def audio_to_base64(self, audio_bytes: bytes) -> str:
        """Convert audio bytes to base64 for embedding in HTML.

        Args:
            audio_bytes: Audio data in bytes

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(audio_bytes).decode('utf-8')
