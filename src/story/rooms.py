"""Room-based progression system for The Echo Rooms."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class RoomType(Enum):
    """Types of rooms in the facility."""
    AWAKENING = "awakening"
    MEMORY_ARCHIVES = "memory_archives"
    TESTING_ARENA = "testing_arena"
    TRUTH_CHAMBER = "truth_chamber"
    THE_EXIT = "the_exit"


@dataclass
class MemoryFragment:
    """A memory fragment that gets revealed during progression."""
    fragment_id: str
    room_unlocked_in: RoomType
    title: str
    content: str
    visual_description: str
    emotional_impact: str  # How this affects the player


@dataclass
class Room:
    """Represents a room in the facility."""
    room_type: RoomType
    room_number: int
    name: str
    description: str
    objective: str
    unlocked: bool
    completed: bool
    puzzle_solved: bool
    memory_fragment: Optional[MemoryFragment]

    # Puzzle requirements (MANDATORY for progression)
    puzzle_type: str  # "answer", "multi_clue", "choice", "acceptance"
    puzzle_answer: Optional[str]  # Exact answer needed (if puzzle_type == "answer")
    required_clues: Optional[List[str]]  # Clues that must be viewed (if puzzle_type == "multi_clue")

    # Emotional/conversational triggers (OPTIONAL - builds relationship, not progression)
    emotional_themes: List[str]  # Themes for relationship building
    hint_keywords: List[str]  # Keywords Echo uses to give hints

    # What happened in this room
    player_choices: Dict[str, Any]


class RoomProgression:
    """Manages progression through the 5 rooms."""

    def __init__(self):
        """Initialize room progression system."""
        self.current_room: RoomType = RoomType.AWAKENING
        self.rooms: Dict[RoomType, Room] = self._initialize_rooms()
        self.memory_fragments: List[MemoryFragment] = []
        self.key_choices: Dict[str, Any] = {
            "sacrificed_ai": None,  # "echo" or None (refused sacrifice)
            "accepted_truth": False,
            "vulnerability_count": 0,
            "trust_established": False,
            "acknowledged_ai_sentience": False,
            "rejection_count": 0,  # How many times player denied AI sentience (Room 2)
            "truth_denial_count": 0,  # How many times player denied the truth (Room 4)
        }

        # Puzzle state tracking (what player has actually done)
        self.puzzle_state: Dict[str, Any] = {
            "room1_answer_attempts": 0,
            "room1_clues_found": [],  # ["newspaper", "calendar", "weather"]
            "room2_archives_viewed": [],  # ["blog", "social", "news"]
            "room3_data_reviewed": [],  # ["reaction_time", "weather_stats", "reconstruction"]
            "room4_acceptance_expressed": False
        }

        # Room 3 timer state - REMOVED (now puzzle-based)
        # Timer mechanic removed in favor of evidence analysis puzzle

        # Track last scenario shown (so companions can react to it)
        self.last_scenario_shown: Optional[str] = None

    def _initialize_rooms(self) -> Dict[RoomType, Room]:
        """Create all 5 rooms with their configurations."""

        rooms = {}

        # ROOM 1: The Awakening Chamber
        # PUZZLE: Find weather for October 15, 2023 in Seattle (investigate room clues)
        # Echo guides exploration but doesn't solve it
        rooms[RoomType.AWAKENING] = Room(
            room_type=RoomType.AWAKENING,
            room_number=1,
            name="The Awakening Chamber",
            description="A sterile white room with three medical pods, flickering lights, and a glowing terminal. The air is cold and clinical. A voice authentication system requests: 'What was the weather on October 15th, 2023 in Seattle?'",
            objective="Find the answer to the voice authentication puzzle by investigating clues in the room.",
            unlocked=True,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,

            # PUZZLE REQUIREMENTS (mandatory)
            puzzle_type="answer",
            puzzle_answer="Light rain",  # Must say "light rain" or "rainy" to unlock
            required_clues=None,  # Optional - can solve without viewing all clues

            # EMOTIONAL THEMES (optional - builds relationship only)
            emotional_themes=["trust", "vulnerability", "working_together", "fear", "confusion"],
            hint_keywords=["terminal", "newspaper", "calendar", "weather", "clues", "investigate"],

            player_choices={}
        )

        # ROOM 2: The Memory Archives
        # PUZZLE: Extract password from 3 archive terminals and enter it
        # Blog has name, Social has date, News has year → combine into password
        rooms[RoomType.MEMORY_ARCHIVES] = Room(
            room_type=RoomType.MEMORY_ARCHIVES,
            room_number=2,
            name="The Memory Archives",
            description="A dark server room filled with floating holographic memory fragments. A locked door pulses with energy. Three terminals glow: 'BLOG ARCHIVE', 'SOCIAL MEDIA', and 'NEWS ARCHIVE'. A keypad waits for input.",
            objective="Extract the password from the three archive terminals to unlock the door.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,

            # PUZZLE REQUIREMENTS (mandatory)
            puzzle_type="password",
            puzzle_answer="ALEXCHEN_MAY12_2023",  # Must extract and combine from all 3 archives
            required_clues=["blog", "social_media", "news"],  # MUST view all 3 to get pieces

            # EMOTIONAL THEMES (optional)
            emotional_themes=["ai_sentience", "empathy", "acknowledgment", "connection", "discovery"],
            hint_keywords=["password", "terminals", "archives", "blog", "social", "news", "keypad", "unlock"],

            player_choices={"fragments_viewed": [], "password_attempts": 0}
        )

        # ROOM 3: The Testing Arena
        # PUZZLE: Make sacrifice choice (timer forces decision)
        # Can optionally review traffic data first (Echo suggests it for comfort/clarity)
        rooms[RoomType.TESTING_ARENA] = Room(
            room_type=RoomType.TESTING_ARENA,
            room_number=3,
            name="The Testing Arena",
            description="A testing facility with three evidence terminals. The door is locked. A screen reads: 'ANALYZE THE EVIDENCE. WHAT IS THE TRUTH?'",
            objective="Review all evidence terminals and determine the truth about the accident to unlock the door.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,

            # PUZZLE REQUIREMENTS (mandatory)
            puzzle_type="evidence_analysis",
            puzzle_answer="unavoidable",  # Must conclude accident was unavoidable
            required_clues=["reaction_time", "weather_stats", "reconstruction"],  # Must view all 3

            # EMOTIONAL THEMES (optional)
            emotional_themes=["sacrifice", "difficult_choice", "loyalty", "commitment"],
            hint_keywords=["choice", "sacrifice", "decide", "timer", "system"],

            player_choices={"accepted_innocence": False, "sacrifice_made": None}
        )

        # ROOM 4: The Truth Chamber
        # PUZZLE: Reconstruct the timeline by ordering events correctly
        # Journal entries, photos, research notes must be put in chronological order
        rooms[RoomType.TRUTH_CHAMBER] = Room(
            room_type=RoomType.TRUTH_CHAMBER,
            room_number=4,
            name="The Truth Chamber",
            description="Your old office. Scattered documents everywhere. A screen shows: 'RECONSTRUCT THE TIMELINE'. Five fragments of your past need to be ordered.",
            objective="Arrange the timeline fragments in the correct chronological order.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,

            # PUZZLE REQUIREMENTS (mandatory)
            puzzle_type="timeline",
            puzzle_answer="LOSS_GRIEF_CREATION_OBSESSION_CYCLE",  # Correct order
            required_clues=["journal", "photos", "research"],  # Must view all evidence

            # EMOTIONAL THEMES (mandatory here - understanding the journey)
            emotional_themes=["acceptance", "grief", "truth", "letting_go", "understanding", "self_awareness"],
            hint_keywords=["timeline", "order", "sequence", "chronological", "events", "reconstruct"],

            player_choices={"accepted_truth": False, "timeline_attempts": 0}
        )

        # ROOM 5: The Exit
        # PUZZLE: Choose the right door based on lessons learned from all previous rooms
        # Three doors representing different philosophies - must justify choice with evidence
        rooms[RoomType.THE_EXIT] = Room(
            room_type=RoomType.THE_EXIT,
            room_number=5,
            name="The Exit",
            description="Three doors stand before you. Each has an inscription describing its path. You must choose wisely based on everything you've learned.",
            objective="Choose the door that reflects your understanding of the journey.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,

            # PUZZLE REQUIREMENTS (choice must be justified with prior room knowledge)
            puzzle_type="ethical_choice",
            puzzle_answer=None,  # Multiple valid answers depending on player's journey
            required_clues=None,  # Knowledge from all previous rooms

            # EMOTIONAL THEMES (all culminate here)
            emotional_themes=["final_choice", "ending", "resolution", "wisdom", "growth"],
            hint_keywords=["door", "choice", "path", "forward", "decide"],

            player_choices={"ending_chosen": None, "justification": None}
        )

        return rooms

    def get_current_room(self) -> Room:
        """Get the currently active room.

        Returns:
            The current Room object
        """
        return self.rooms[self.current_room]

    def check_room_unlock_conditions(self, room_type: RoomType) -> Dict[str, Any]:
        """Check if conditions are met to unlock a room.

        Args:
            room_type: The room to check

        Returns:
            Dict with unlock status and requirements
        """
        room = self.rooms[room_type]

        # Can't unlock if already unlocked
        if room.unlocked:
            return {"can_unlock": True, "already_unlocked": True}

        # Check if previous room is completed
        if room.room_number > 1:
            prev_room_type = list(RoomType)[room.room_number - 2]
            prev_room = self.rooms[prev_room_type]

            if not prev_room.completed:
                return {
                    "can_unlock": False,
                    "reason": f"Must complete {prev_room.name} first",
                    "required_room": prev_room.name
                }

        return {"can_unlock": True, "already_unlocked": False}

    def unlock_room(self, room_type: RoomType) -> bool:
        """Unlock a room if conditions are met.

        Args:
            room_type: The room to unlock

        Returns:
            True if unlocked, False otherwise
        """
        check = self.check_room_unlock_conditions(room_type)

        if check["can_unlock"]:
            self.rooms[room_type].unlocked = True
            self.current_room = room_type
            return True

        return False

    def complete_room(self, room_type: RoomType, memory_fragment: Optional[MemoryFragment] = None):
        """Mark a room as completed and reveal its memory fragment.

        Args:
            room_type: The room that was completed
            memory_fragment: The memory fragment to reveal
        """
        room = self.rooms[room_type]
        room.completed = True

        if memory_fragment:
            room.memory_fragment = memory_fragment
            self.memory_fragments.append(memory_fragment)

        # Unlock next room
        if room.room_number < 5:
            next_room_type = list(RoomType)[room.room_number]
            self.unlock_room(next_room_type)

    def check_trigger_match(self, message: str, room_type: Optional[RoomType] = None) -> Dict[str, Any]:
        """Check if a message matches any conversational triggers for progression.

        Args:
            message: The player's message
            room_type: Which room to check (default: current room)

        Returns:
            Dict with match status and which trigger was matched
        """
        if room_type is None:
            room_type = self.current_room

        room = self.rooms[room_type]
        message_lower = message.lower()

        # Check each trigger
        for trigger in room.conversational_triggers:
            if trigger.lower() in message_lower:
                return {
                    "matched": True,
                    "trigger": trigger,
                    "room": room.name,
                    "hint": f"You sense progress in your words..."
                }

        return {"matched": False}

    def check_puzzle_solution(self, answer: str, room_type: Optional[RoomType] = None) -> bool:
        """Check if a puzzle answer is correct.

        Args:
            answer: The player's answer
            room_type: Which room to check (default: current room)

        Returns:
            True if correct, False otherwise
        """
        if room_type is None:
            room_type = self.current_room

        room = self.rooms[room_type]

        if room.puzzle_answer is None:
            return False

        return answer.upper().strip() == room.puzzle_answer.upper().strip()

    def record_choice(self, choice_key: str, choice_value: Any):
        """Record a key player choice for ending determination.

        Args:
            choice_key: The choice identifier
            choice_value: The value of the choice
        """
        self.key_choices[choice_key] = choice_value

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of overall progression.

        Returns:
            Dict with current room, completion status, and choices
        """
        completed_rooms = sum(1 for room in self.rooms.values() if room.completed)

        return {
            "current_room": self.current_room.value,
            "current_room_name": self.rooms[self.current_room].name,
            "room_number": self.rooms[self.current_room].room_number,
            "total_rooms": 5,
            "rooms_completed": completed_rooms,
            "objective": self.rooms[self.current_room].objective,
            "memory_fragments_collected": len(self.memory_fragments),
            "key_choices": self.key_choices
        }

    def get_all_memory_fragments(self) -> List[MemoryFragment]:
        """Get all collected memory fragments.

        Returns:
            List of MemoryFragment objects
        """
        return self.memory_fragments

    # TIMER METHODS REMOVED - Room 3 is now puzzle-based, not timer-based
