"""Player identification for cross-session memory persistence.

Uses browser fingerprinting to create stable player IDs without requiring login.
Privacy-safe: No personal data stored, just anonymous hash.
"""

import hashlib
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def get_player_id(request=None) -> str:
    """Generate stable but anonymous player ID.

    Uses browser fingerprint (IP + User-Agent) for public deployment.
    Player can reset by:
    - Using different browser
    - Using incognito mode
    - Clearing cookies
    - Using VPN

    Args:
        request: Gradio Request object (contains headers, client info)

    Returns:
        12-character hex player ID
    """
    if request is None:
        # Fallback for testing/demo
        return "demo_player"

    try:
        # Create fingerprint from request metadata
        ip = request.client.host if hasattr(request, "client") else "unknown"
        user_agent = request.headers.get("user-agent", "unknown") if hasattr(request, "headers") else "unknown"

        fingerprint_data = f"{ip}_{user_agent}"

        # Hash to create stable ID
        player_id = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:12]

        logger.debug(f"[PLAYER_ID] Generated ID: {player_id} (IP: {ip[:10]}..., UA: {user_agent[:30]}...)")

        return player_id

    except Exception as e:
        logger.error(f"[PLAYER_ID] Error generating player ID: {e}")
        return "fallback_player"


def get_player_id_description() -> str:
    """Get user-facing description of how player ID works.

    Returns:
        Markdown description for UI
    """
    return """
**About Memory & Privacy:**

Your AI companions remember you across playthroughs using an anonymous ID based on your browser.

- ✅ **No login required** - Automatic based on browser fingerprint
- ✅ **Privacy-safe** - No personal data stored, just anonymous hash
- ✅ **Fresh start options**:
  - Use incognito/private mode
  - Use different browser
  - Click "Clear All Memories" button
  - Wait for memories to naturally fade (time-based decay)

Your memories persist on this device/browser only. Different devices = different identities.
"""