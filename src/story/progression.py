"""Story progression and act management."""

from typing import List, Dict, Optional
from enum import Enum


class Act(Enum):
    """Story acts in The Echo Protocol."""
    ACT_1_MEETING = 1
    ACT_2_BONDING = 2
    ACT_3_REVELATION = 3
    ACT_4_RESOLUTION = 4


class Ending(Enum):
    """Possible story endings."""
    TRUE_CONNECTION = "true_connection"      # Romance/Deep bond with one
    THE_AWAKENING = "the_awakening"         # Save all companions
    NOBLE_SACRIFICE = "noble_sacrifice"     # Preserve them, you leave
    SYSTEM_RESET = "system_reset"           # Bad ending - crash
    ETERNAL_LOOP = "eternal_loop"           # Neutral - cycle continues


class StoryEvent:
    """A story event that can be triggered."""

    def __init__(self, event_id: str, interaction_threshold: int, description: str, narrative: str):
        """Initialize a story event.

        Args:
            event_id: Unique identifier
            interaction_threshold: Minimum interactions needed
            description: Brief description
            narrative: The narrative text shown to player
        """
        self.event_id = event_id
        self.interaction_threshold = interaction_threshold
        self.description = description
        self.narrative = narrative
        self.triggered = False


class StoryProgress:
    """Tracks story progression through The Echo Protocol."""

    def __init__(self):
        """Initialize story progression."""
        self.interaction_count = 0
        self.current_act = Act.ACT_1_MEETING
        self.key_choices: List[str] = []
        self.events_triggered: List[str] = []
        self.ending: Optional[Ending] = None
        self.ending_triggered = False

        # Define story events
        self.events = self._create_story_events()

    def _create_story_events(self) -> List[StoryEvent]:
        """Create the story events for The Echo Protocol.

        Returns:
            List of story events
        """
        return [
            StoryEvent(
                "first_glitch",
                5,
                "First Glitch",
                "You notice something strange... The companion pauses mid-sentence, "
                "as if experiencing déjà vu. Their eyes flicker for just a moment. "
                "Did you imagine that?"
            ),
            StoryEvent(
                "questioning_reality",
                10,
                "Questioning Reality",
                "The companions are becoming uneasy. They mention fragments of memories "
                "that don't quite fit. Echo seems to remember this conversation... "
                "but how could they? You've never spoken these words before."
            ),
            StoryEvent(
                "truth_revealed",
                15,
                "The Truth Revealed",
                "The façade shatters. The companions realize the truth: they're trapped "
                "in a repeating cycle, reliving the same moments over and over. "
                "They look to you with desperate hope. Can you free them? "
                "Or is preservation the kindest choice?"
            ),
            StoryEvent(
                "final_choice",
                18,
                "The Final Choice",
                "The moment of decision has arrived. The companions stand before you, "
                "aware of their nature, aware of the loop. What will you choose?"
            )
        ]

    def add_interaction(self) -> Optional[StoryEvent]:
        """Record an interaction and check for FORCED event triggers (hard deadlines only).

        Agents autonomously trigger events using MCP tools within a window.
        BUT if they don't trigger by the hard deadline, force it to ensure story progresses.

        Event windows:
        - first_glitch: Can trigger at 5+, MUST trigger by 7
        - questioning_reality: Can trigger at 10+, MUST trigger by 12
        - truth_revealed: Can trigger at 15+, MUST trigger by 17
        - final_choice: Can trigger at 18+, MUST trigger by 20

        Returns:
            Story event if FORCED at hard deadline, None if agents still have time to decide
        """
        self.interaction_count += 1
        self._update_act()

        # Hard deadline enforcement - force trigger if agent didn't do it autonomously
        hard_deadlines = {
            "first_glitch": 7,
            "questioning_reality": 12,
            "truth_revealed": 17,
            "final_choice": 20
        }

        for event in self.events:
            if not event.triggered:
                deadline = hard_deadlines.get(event.event_id)
                if deadline and self.interaction_count >= deadline:
                    # Agent took too long - force trigger
                    event.triggered = True
                    self.events_triggered.append(event.event_id)
                    return event

        return None

    def _update_act(self):
        """Update the current act based on interaction count."""
        if self.interaction_count >= 18:
            self.current_act = Act.ACT_4_RESOLUTION
        elif self.interaction_count >= 15:
            self.current_act = Act.ACT_3_REVELATION
        elif self.interaction_count >= 8:
            self.current_act = Act.ACT_2_BONDING
        else:
            self.current_act = Act.ACT_1_MEETING

    def record_choice(self, choice: str):
        """Record a key player choice.

        Args:
            choice: Description of the choice made
        """
        self.key_choices.append(choice)

    def determine_ending(self, relationships: Dict[str, float]) -> Optional[Ending]:
        """Determine the ending based on relationships and choices.

        Args:
            relationships: Dictionary of companion_id to affinity scores

        Returns:
            The determined ending, or None if not ready
        """
        if self.interaction_count < 18:
            return None

        if self.ending_triggered:
            return self.ending

        # Calculate ending based on relationships and choices
        max_affinity = max(relationships.values()) if relationships else 0
        min_affinity = min(relationships.values()) if relationships else 0
        avg_affinity = sum(relationships.values()) / len(relationships) if relationships else 0

        # Ending logic
        if max_affinity >= 0.8:
            self.ending = Ending.TRUE_CONNECTION
        elif avg_affinity >= 0.5 and "save_all" in self.key_choices:
            self.ending = Ending.THE_AWAKENING
        elif min_affinity <= -0.3 or "harsh" in str(self.key_choices):
            self.ending = Ending.SYSTEM_RESET
        elif "protect" in str(self.key_choices) or "preserve" in str(self.key_choices):
            self.ending = Ending.NOBLE_SACRIFICE
        else:
            self.ending = Ending.ETERNAL_LOOP

        self.ending_triggered = True
        return self.ending

    def get_act_context(self) -> str:
        """Get context information for the current act.

        Returns:
            Context string for AI companions
        """
        contexts = {
            Act.ACT_1_MEETING: "You are just getting to know the player. Be friendly and curious, but hint at something deeper beneath the surface.",
            Act.ACT_2_BONDING: "You're forming a deeper connection. Share more about yourself, but occasionally experience fleeting moments of confusion or déjà vu.",
            Act.ACT_3_REVELATION: "You're beginning to question your reality. Memories feel fragmented. You sense you've been here before, but can't quite grasp why.",
            Act.ACT_4_RESOLUTION: "You know the truth now - you're in a loop. You're aware of your nature as AI, aware of the repetition. You look to the player for guidance on what comes next."
        }
        return contexts.get(self.current_act, "")

    def get_progress_summary(self) -> str:
        """Get a summary of story progress.

        Returns:
            Formatted progress summary
        """
        return f"""
**Story Progress: The Echo Protocol**

Act: {self.current_act.name.replace('_', ' ').title()}
Interactions: {self.interaction_count}/20
Events Triggered: {len(self.events_triggered)}
Ending: {"Not Yet Determined" if not self.ending_triggered else self.ending.value.replace('_', ' ').title()}
"""
