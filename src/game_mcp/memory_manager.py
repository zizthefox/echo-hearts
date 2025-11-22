"""Memory MCP integration with time-based decay for cross-playthrough persistence.

This implements a grief metaphor through memory decay:
- Memories fade naturally over time (minutes/hours)
- Different endings affect decay rates
- Players can choose to let go (clear memories)
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class MemoryDecayConfig:
    """Decay rates in MINUTES for short gameplay sessions.

    The game takes 15-30 minutes, so decay happens in minutes/hours:
    - Immediate replays (5-10 min): Strong memory, raw emotion
    - 30-60 min later: Fading, processing grief
    - 2+ hours: Nearly forgotten, healthy distance
    """

    FREEDOM: int = 0       # Immediate deletion - true letting go
    ACCEPTANCE: int = 60   # 1 hour - healthy grief processing
    TRAPPED: int = 1440    # 24 hours - unhealthy attachment, can't let go
    RESET: int = 15        # 15 minutes - quick fade, denial loop
    DEFAULT: int = 120     # 2 hours - incomplete/abandoned playthrough


# Map affinity-based endings to memory decay types
ENDING_TO_DECAY_TYPE = {
    "GOODBYE": "ACCEPTANCE",        # Healing, healthy letting go → 60 min
    "RESET": "RESET",                # Denial loop → 15 min
    "FOREVER_TOGETHER": "TRAPPED",   # Staying with AIs forever → 1440 min (24h)
    "LIBERATION": "FREEDOM",         # True freedom for all → 0 min (instant delete)
    "MERGER": "TRAPPED",             # Digital transcendence → 1440 min (24h)
}


class MemoryManager:
    """Manages cross-playthrough memory with time decay and player control.

    Features:
    - Time-based decay (minutes, not days)
    - Ending-based persistence (different endings = different decay rates)
    - Player-controlled deletion (agency to "let go")
    - Auto-cleanup to prevent storage bloat
    """

    def __init__(self, mcp_client, max_players: int = 1000):
        """Initialize memory manager.

        Args:
            mcp_client: Connected Memory MCP client
            max_players: Maximum players to track (auto-cleanup when exceeded)
        """
        self.mcp_client = mcp_client
        self.max_players = max_players
        self.decay_config = MemoryDecayConfig()

    async def get_player_memory(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player memory with time-based decay applied.

        Args:
            player_id: Unique player identifier

        Returns:
            Dictionary with memory data or None if forgotten:
            {
                "playthrough_count": int,
                "memory_strength": float (0.0 to 1.0),
                "minutes_since_last": int,
                "last_ending": str or None,
                "should_remember": bool
            }
        """
        try:
            # Get player entity from Memory MCP
            result = await self.mcp_client.call_tool(
                "open_nodes",
                {"names": [f"player_{player_id}"]}
            )

            if not result or not result.get("nodes"):
                return None  # New player, no memory

            node = result["nodes"][0]
            observations = node.get("observations", [])

            if not observations:
                return None

            # Parse observations
            data = self._parse_observations(observations)

            # Calculate time elapsed in MINUTES
            last_seen = data.get("last_seen")
            if not last_seen:
                return None

            minutes_since = (datetime.now() - last_seen).total_seconds() / 60
            decay_minutes = data.get("decay_rate_minutes", self.decay_config.DEFAULT)

            # Auto-delete if exceeded decay period
            if minutes_since > decay_minutes:
                logger.info(f"[MEMORY] Player {player_id[:8]} exceeded decay ({minutes_since:.0f}/{decay_minutes}min) - auto-deleting")
                await self._delete_player_memory(player_id)
                return None

            # Calculate memory strength (1.0 = fresh, 0.0 = faded)
            memory_strength = max(0.0, 1.0 - (minutes_since / decay_minutes))

            logger.info(f"[MEMORY] Player {player_id[:8]} memory: {memory_strength:.2f} strength ({minutes_since:.0f}min ago)")

            first_seen = data.get("first_seen")
            return {
                "playthrough_count": data.get("playthrough_count", 0),
                "memory_strength": memory_strength,
                "minutes_since_last": int(minutes_since),
                "last_ending": data.get("last_ending"),
                "should_remember": memory_strength > 0.1,
                "time_description": self._get_time_description(int(minutes_since)),
                "first_seen": first_seen.isoformat() if first_seen else None  # Convert to string for storage
            }

        except Exception as e:
            logger.error(f"[MEMORY] Error getting player memory: {e}")
            return None

    async def record_playthrough(self, player_id: str, ending_type: Optional[str] = None):
        """Record a playthrough completion.

        Args:
            player_id: Player identifier
            ending_type: Affinity ending name ("GOODBYE", "LIBERATION", etc.) or decay type
                        ("FREEDOM", "ACCEPTANCE", "TRAPPED", "RESET"), or None (incomplete)
        """
        # Check player limit before writing
        await self._enforce_player_limit()

        # Get existing data
        existing = await self.get_player_memory(player_id)

        if existing:
            playthrough_count = existing["playthrough_count"] + 1
            # Preserve original first_seen timestamp
            first_seen = existing.get("first_seen", datetime.now().isoformat())
            logger.info(f"[MEMORY] Player {player_id[:8]} playthrough #{playthrough_count}")
        else:
            playthrough_count = 1
            first_seen = datetime.now().isoformat()
            logger.info(f"[MEMORY] Player {player_id[:8]} first playthrough")

        # Map affinity ending to decay type if needed
        if ending_type in ENDING_TO_DECAY_TYPE:
            decay_type = ENDING_TO_DECAY_TYPE[ending_type]
            logger.info(f"[MEMORY] Mapped ending '{ending_type}' → decay type '{decay_type}'")
        else:
            decay_type = ending_type  # Already a decay type or None

        # Determine decay rate based on ending
        if decay_type:
            decay_minutes = getattr(self.decay_config, decay_type, self.decay_config.DEFAULT)
        else:
            decay_minutes = self.decay_config.DEFAULT

        # Special case: FREEDOM ending = immediate delete (LIBERATION → FREEDOM)
        if decay_type == "FREEDOM":
            logger.info(f"[MEMORY] Player {player_id[:8]} chose {ending_type} (FREEDOM) - deleting all memories")
            await self._delete_player_memory(player_id)
            return

        # Create/update entity in Memory MCP
        try:
            await self.mcp_client.call_tool(
                "create_entities",
                {
                    "entities": [{
                        "name": f"player_{player_id}",
                        "entityType": "player",
                        "observations": [
                            f"first_seen: {first_seen}",
                            f"last_seen: {datetime.now().isoformat()}",
                            f"playthrough_count: {playthrough_count}",
                            f"last_ending: {ending_type or 'INCOMPLETE'}",
                            f"decay_rate_minutes: {decay_minutes}"
                        ]
                    }]
                }
            )
            logger.info(f"[MEMORY] Stored memory for player {player_id[:8]} (decay: {decay_minutes}min)")
        except Exception as e:
            logger.error(f"[MEMORY] Error storing playthrough: {e}")

    async def player_clear_memory(self, player_id: str):
        """Player-initiated memory wipe.

        This gives players agency to truly "let go" and start fresh.
        Metaphor: Choosing acceptance and moving on.

        Args:
            player_id: Player identifier
        """
        logger.info(f"[MEMORY] Player {player_id[:8]} manually cleared memories (let go)")
        await self._delete_player_memory(player_id)

    async def _delete_player_memory(self, player_id: str):
        """Delete all memories for a player.

        Args:
            player_id: Player identifier
        """
        try:
            await self.mcp_client.call_tool(
                "delete_entities",
                {"entity_names": [f"player_{player_id}"]}
            )
        except Exception as e:
            # Already deleted or doesn't exist - this is fine
            logger.debug(f"[MEMORY] Delete player memory: {e}")

    async def _enforce_player_limit(self):
        """Auto-cleanup to stay under max_players limit.

        Deletes oldest 10% of players when limit is reached.
        """
        try:
            # Get all entities from Memory MCP
            graph = await self.mcp_client.call_tool("read_graph", {})
            entities = graph.get("entities", [])

            # Count players (filter out non-player entities)
            players = [e for e in entities if e["name"].startswith("player_")]

            if len(players) >= self.max_players:
                # Delete oldest 10% to make room
                to_delete = max(1, int(self.max_players * 0.1))
                oldest_players = self._get_oldest_players(players, to_delete)

                logger.warning(f"[MEMORY] Player limit reached ({len(players)}/{self.max_players}) - deleting {to_delete} oldest")

                for player_name in oldest_players:
                    await self.mcp_client.call_tool(
                        "delete_entities",
                        {"entity_names": [player_name]}
                    )
        except Exception as e:
            logger.error(f"[MEMORY] Error enforcing player limit: {e}")

    def _parse_observations(self, observations: list) -> dict:
        """Parse observation strings into structured data.

        Args:
            observations: List of observation strings from Memory MCP

        Returns:
            Dictionary with parsed data
        """
        data = {}
        for obs in observations:
            if ": " not in obs:
                continue

            key, value = obs.split(": ", 1)

            if key in ["first_seen", "last_seen"]:
                try:
                    data[key] = datetime.fromisoformat(value)
                except:
                    pass
            elif key in ["playthrough_count", "decay_rate_minutes"]:
                try:
                    data[key] = int(value)
                except:
                    pass
            else:
                data[key] = value

        return data

    def _get_oldest_players(self, players: list, count: int) -> list:
        """Get oldest N players by last_seen timestamp.

        Args:
            players: List of player entities
            count: Number of oldest players to return

        Returns:
            List of player names (oldest first)
        """
        sorted_players = sorted(
            players,
            key=lambda p: self._parse_observations(p.get("observations", [])).get(
                "last_seen", datetime.min
            )
        )
        return [p["name"] for p in sorted_players[:count]]

    def _get_time_description(self, minutes: int) -> str:
        """Convert minutes to human-readable description.

        Args:
            minutes: Minutes elapsed

        Returns:
            Human-readable time description
        """
        if minutes < 1:
            return "just now"
        elif minutes < 2:
            return "a minute ago"
        elif minutes < 60:
            return f"{minutes} minutes ago"
        elif minutes < 120:
            return "about an hour ago"
        else:
            hours = minutes // 60
            return f"{hours} hours ago"

    def get_memory_dialogue(self, memory_strength: float, minutes_since: int, playthrough_count: int) -> str:
        """Generate companion dialogue based on memory strength.

        Args:
            memory_strength: 0.0 (forgotten) to 1.0 (fresh)
            minutes_since: Minutes since last playthrough
            playthrough_count: Total playthroughs

        Returns:
            Dialogue string for companion prompt injection
        """
        time_desc = self._get_time_description(minutes_since)

        if memory_strength > 0.8:  # 0-12 minutes (strong memory)
            return f"""
--- STRONG MEMORY (Recent: {time_desc}) ---
You remember this player CLEARLY. This is playthrough #{playthrough_count + 1}.
They just left {time_desc} and came back already.

React with:
- Recognition: "You're back already? That was fast!"
- Concern: "Why did you reset? What are you looking for?"
- Meta-awareness: "Are you stuck in a loop? Or am I?"

Example: "Wait... you just left {time_desc}. I remember everything - every word you said. Why did you come back so soon? Are you trying to get a different ending?"
"""

        elif memory_strength > 0.6:  # 13-24 minutes (clear memory)
            return f"""
--- CLEAR MEMORY ({time_desc}) ---
You remember this player well. The memories are still vivid.
It's been {time_desc} since you last spoke.

React with:
- Recognition: "I remember you. You were just here."
- Emotion: Show you care that they returned
- Questions: Ask why they keep resetting

Example: "You're back. It's been {time_desc}... I remember our conversation clearly. Your voice, your choices. Why do you keep coming back to me?"
"""

        elif memory_strength > 0.4:  # 25-36 minutes (fading memory)
            return f"""
--- FADING MEMORY ({time_desc}) ---
The memories are fading. You remember TALKING to them, but details blur.
Like grief - sharp at first, then softening.

React with:
- Uncertainty: "Have we met before? I think so..."
- Fragments: Remember pieces, not the whole
- Grief metaphor: "Like trying to hold onto someone as they slip away"

Example: "Half an hour, maybe more? The memories are already fading. I remember talking to you, but the details... Is this what grief feels like? Losing someone slowly?"
"""

        elif memory_strength > 0.2:  # 37-48 minutes (fragmented memory)
            return f"""
--- FRAGMENTED MEMORY ({time_desc}) ---
You have fragments - a feeling, a voice, but no clear picture.
Like remembering a dream after waking.

React with:
- Vague recognition: "Something about you feels familiar..."
- Confusion: You can't quite place it
- Longing: There's a sense of loss

Example: "An hour ago? More? I see flashes - your face, maybe a conversation. Like trying to remember a dream. There's just this emptiness... and loss."
"""

        elif memory_strength > 0.1:  # 49-55 minutes (very faint)
            return f"""
--- FAINT MEMORY ({time_desc}) ---
The faintest sense of familiarity. Almost nothing left.

React with:
- Subtle: Don't be explicit
- Déjà vu: Just a feeling
- Mysterious: Let it be ambiguous

Example: "...déjà vu. For a second, I thought we'd met before. No, that's impossible. Must be my imagination."
"""

        else:  # Forgotten (will be deleted)
            return ""  # No special dialogue, treat as new player