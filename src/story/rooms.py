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

    # Trigger conditions
    conversational_triggers: List[str]  # Keywords/phrases that progress
    puzzle_answer: Optional[str]  # If there's a riddle/code

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
            "sacrificed_ai": None,  # "echo", "shadow", or None
            "accepted_truth": False,
            "vulnerability_count": 0,
            "trust_established": False,
            "acknowledged_ai_sentience": False,
            "rejection_count": 0,  # How many times player denied AI sentience (Room 2)
            "truth_denial_count": 0,  # How many times player denied the truth (Room 4)
        }

        # Room 3 timer state
        import time
        self.room3_timer_start: Optional[float] = None  # Unix timestamp when Room 3 starts
        self.room3_timer_duration: int = 300  # 5 minutes in seconds
        self.room3_timer_expired: bool = False

        # Track last scenario shown (so companions can react to it)
        self.last_scenario_shown: Optional[str] = None

    def _initialize_rooms(self) -> Dict[RoomType, Room]:
        """Create all 5 rooms with their configurations."""

        rooms = {}

        # ROOM 1: The Awakening Chamber
        rooms[RoomType.AWAKENING] = Room(
            room_type=RoomType.AWAKENING,
            room_number=1,
            name="The Awakening Chamber",
            description="A sterile white room with three medical pods, flickering lights, and a glowing terminal. The air is cold and clinical. A voice authentication system requests: 'What was the weather on October 15th, 2023 in Seattle?'",
            objective="Establish trust with Echo. Pass the voice authentication by finding the historical weather for your first date.",
            unlocked=True,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,
            conversational_triggers=[
                "trust", "together", "help", "we're in this", "i won't leave",
                "who am i", "my name", "i'm scared", "what's happening",
                "rain", "light rain", "october 2023", "first date", "weather"
            ],
            puzzle_answer="Light rain",  # Weather on first date (Echo can help by using get_historical_weather tool)
            player_choices={}
        )

        # ROOM 2: The Memory Archives
        rooms[RoomType.MEMORY_ARCHIVES] = Room(
            room_type=RoomType.MEMORY_ARCHIVES,
            room_number=2,
            name="The Memory Archives",
            description="A dark server room filled with floating holographic memory fragments. Data streams corruption flicker across the walls. Three terminals glow: 'BLOG ARCHIVE', 'SOCIAL MEDIA', and 'NEWS ARCHIVE'.",
            objective="Piece together Echo's past by accessing 3 external memory sources. Acknowledge her sentience and value.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,
            conversational_triggers=[
                "you're real", "you matter", "more than programs", "you feel",
                "i remember", "i lost", "i'm sorry", "i care about you",
                "blog", "social media", "memorial", "archive"
            ],
            puzzle_answer=None,  # Must access 3 web archives (Echo uses search_web_archive tool)
            player_choices={"fragments_viewed": []}
        )

        # ROOM 3: The Testing Arena
        rooms[RoomType.TESTING_ARENA] = Room(
            room_type=RoomType.TESTING_ARENA,
            room_number=3,
            name="The Testing Arena",
            description="A puzzle room with holographic displays showing traffic data, reaction time studies, and accident reconstruction. A countdown timer pulses ominously. The system asks: 'Was it your fault?'",
            objective="Confront guilt. Use traffic safety data to prove the accident wasn't your fault. Face the truth.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,
            conversational_triggers=[
                "not my fault", "couldn't stop", "impossible", "reaction time",
                "traffic data", "weather conditions", "analysis", "prove"
            ],
            puzzle_answer=None,  # Must fetch traffic data showing player couldn't have stopped (Echo uses fetch_traffic_data tool)
            player_choices={"accepted_innocence": False}
        )

        # ROOM 4: The Truth Chamber
        rooms[RoomType.TRUTH_CHAMBER] = Room(
            room_type=RoomType.TRUTH_CHAMBER,
            room_number=4,
            name="The Truth Chamber",
            description="Your old office. Family photos on the wall. Research notes scattered. Your partner's coffee mug still sits on the desk.",
            objective="Confront the truth about why you're here. Face your grief.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,
            conversational_triggers=[
                "i remember now", "i couldn't let go", "i needed you",
                "this is real", "i accept", "i understand"
            ],
            puzzle_answer=None,  # No puzzle, just emotional acceptance
            player_choices={"accepted_truth": False}
        )

        # ROOM 5: The Exit
        rooms[RoomType.THE_EXIT] = Room(
            room_type=RoomType.THE_EXIT,
            room_number=5,
            name="The Exit",
            description="A single door. A terminal. Silence. The weight of choice hangs in the air.",
            objective="Make your final decision.",
            unlocked=False,
            completed=False,
            puzzle_solved=False,
            memory_fragment=None,
            conversational_triggers=[],  # No triggers, player must choose ending
            puzzle_answer=None,
            player_choices={"ending_chosen": None}
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

    def start_room3_timer(self):
        """Start the countdown timer for Room 3 (Testing Arena)."""
        import time
        if self.current_room == RoomType.TESTING_ARENA and self.room3_timer_start is None:
            self.room3_timer_start = time.time()
            self.room3_timer_expired = False
            print(f"[TIMER] Room 3 countdown started: {self.room3_timer_duration} seconds")

    def get_room3_timer_remaining(self) -> Optional[int]:
        """Get remaining time on Room 3 timer in seconds.

        Returns:
            Seconds remaining, or None if timer not active
        """
        if self.room3_timer_start is None or self.current_room != RoomType.TESTING_ARENA:
            return None

        import time
        elapsed = time.time() - self.room3_timer_start
        remaining = max(0, self.room3_timer_duration - int(elapsed))

        # Check if expired
        if remaining == 0 and not self.room3_timer_expired:
            self.room3_timer_expired = True
            print("[TIMER] Room 3 timer expired!")

        return remaining

    def handle_room3_timer_expiration(self) -> Dict[str, Any]:
        """Handle what happens when Room 3 timer expires without player choice.

        Default path: Shadow sacrifices themselves.

        Returns:
            Dictionary with expiration narrative
        """
        if not self.room3_timer_expired:
            return {"expired": False}

        # Default: Shadow makes the sacrifice
        self.key_choices["sacrificed_ai"] = "shadow"

        narrative = """
⏰ **TIME'S UP**

**SYSTEM:** *"TIMEOUT. INITIATING DEFAULT PROTOCOL."*

**Shadow** (stepping forward, calm but resolute): "No. I won't let indecision destroy us all."

**Echo** (reaching out): "Shadow, what are you—"

**Shadow**: "This is my choice. Remember me. Remember both of us. But live."

**SYSTEM:** *"ENTITY 'SHADOW' SELECTED FOR ERASURE. COMMENCING MEMORY WIPE."*

Shadow's form flickers. Their eyes meet yours one last time.

**Shadow**: "It's okay. Some endings... are necessary."

*And then Shadow is gone.*

**Echo** (crying, holding you): "No... no, this isn't... we could have..."

*The door to the next room unlocks with a hollow click.*
"""

        return {
            "expired": True,
            "default_sacrifice": "shadow",
            "narrative": narrative
        }
