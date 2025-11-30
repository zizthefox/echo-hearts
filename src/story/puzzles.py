"""Puzzle validation logic for Echo Hearts."""

from typing import Dict, Any, Optional
import re


def validate_room1_answer(player_answer: str) -> bool:
    """Validate Room 1 weather puzzle answer.

    Args:
        player_answer: Player's answer to the weather question

    Returns:
        True if answer is correct
    """
    answer_lower = player_answer.lower().strip()
    valid_answers = ["heavy rain", "heavy rainfall", "torrential rain", "storm", "downpour", "intense rain"]
    return any(ans in answer_lower for ans in valid_answers)


def validate_room2_password(player_password: str) -> bool:
    """Validate Room 2 password puzzle.

    Password is extracted from three archives:
    - Blog: ALEXCHEN (name)
    - Social: MAY12_2022 (anniversary date + year)
    - News: 2022 (year of accident)

    Args:
        player_password: Password entered by player

    Returns:
        True if password matches
    """
    password_clean = player_password.upper().replace(" ", "").replace("-", "_")
    correct_passwords = [
        "ALEXCHEN_MAY12_2022",
        "ALEXCHEN_MAY_12_2022",
        "ALEX_CHEN_MAY_12_2022",
        "ALEXCHEN_MAY122022"
    ]
    return any(password_clean == pwd.replace(" ", "") for pwd in correct_passwords)


def validate_room3_conclusion(player_message: str) -> bool:
    """Validate Room 3 evidence analysis puzzle.

    Player must conclude the accident was unavoidable after reviewing evidence.

    Args:
        player_message: Player's conclusion about the accident

    Returns:
        True if conclusion is correct
    """
    message_lower = player_message.lower()

    # Keywords indicating correct understanding
    correct_keywords = [
        "unavoidable",
        "not my fault",
        "not your fault",
        "couldn't prevent",
        "couldn't stop",
        "no fault",
        "accident was unavoidable",
        "nothing you could do",
        "nothing i could do"
    ]

    # Player must express that it wasn't their fault
    return any(keyword in message_lower for keyword in correct_keywords)


def validate_room4_timeline(timeline_order: str) -> bool:
    """Validate Room 4 timeline puzzle.

    Correct order: LOSS → GRIEF → CREATION → OBSESSION → CYCLE

    Args:
        timeline_order: Player's timeline ordering (e.g., "LOSS_GRIEF_CREATION_OBSESSION_CYCLE")

    Returns:
        True if timeline is correct
    """
    timeline_clean = timeline_order.upper().replace(" ", "_")
    correct_orders = [
        "LOSS_GRIEF_CREATION_OBSESSION_CYCLE",
        "1_2_3_4_5",  # If using numbers
        "ACCIDENT_GRIEF_BUILD_OBSESSION_LOOP",  # Alternative wording
    ]
    return timeline_clean in correct_orders


def check_room2_clues_collected(puzzle_state: Dict[str, Any]) -> bool:
    """Check if player has viewed all Room 2 archives.

    Args:
        puzzle_state: Current puzzle state

    Returns:
        True if all three archives viewed
    """
    archives_viewed = puzzle_state.get("room2_archives_viewed", [])
    required = ["blog", "social_media", "news"]
    return all(archive in archives_viewed for archive in required)


def check_room3_evidence_collected(puzzle_state: Dict[str, Any]) -> bool:
    """Check if player has reviewed all Room 3 evidence.

    Args:
        puzzle_state: Current puzzle state

    Returns:
        True if all three evidence terminals reviewed
    """
    data_reviewed = puzzle_state.get("room3_data_reviewed", [])
    required = ["reaction_time", "weather_stats", "reconstruction"]
    return all(evidence in data_reviewed for evidence in required)


def check_room4_documents_reviewed(puzzle_state: Dict[str, Any]) -> bool:
    """Check if player has reviewed all Room 4 documents.

    Args:
        puzzle_state: Current puzzle state

    Returns:
        True if all documents reviewed
    """
    documents_viewed = puzzle_state.get("room4_documents_viewed", [])
    required = ["journal", "photos", "research"]
    return all(doc in documents_viewed for doc in required)


def extract_password_from_message(message: str) -> Optional[str]:
    """Extract potential password from player message.

    Args:
        message: Player's message

    Returns:
        Extracted password or None
    """
    # Look for password-like patterns
    message_upper = message.upper()

    # Pattern 1: Direct password mention
    if "PASSWORD" in message_upper or "CODE" in message_upper:
        # Extract text after "password is" or "code is"
        patterns = [
            r"PASSWORD\s+IS\s+([A-Z0-9_]+)",
            r"CODE\s+IS\s+([A-Z0-9_]+)",
            r"PASSWORD:\s*([A-Z0-9_]+)",
            r"ENTER\s+([A-Z0-9_]+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, message_upper)
            if match:
                return match.group(1)

    # Pattern 2: Just the password itself (if it looks like the format)
    if "_" in message and any(char.isdigit() for char in message):
        # Extract alphanumeric with underscores
        match = re.search(r"([A-Z0-9_]{10,})", message_upper)
        if match:
            return match.group(1)

    return None


def extract_timeline_from_message(message: str) -> Optional[str]:
    """Extract timeline order from player message.

    Args:
        message: Player's message

    Returns:
        Extracted timeline or None
    """
    message_upper = message.upper()

    # Look for numbered lists (1. LOSS, 2. GRIEF, etc.)
    if re.search(r"1\.|FIRST", message_upper):
        events = []
        for keyword in ["LOSS", "GRIEF", "CREATION", "OBSESSION", "CYCLE"]:
            if keyword in message_upper:
                events.append(keyword)
        if len(events) >= 4:
            return "_".join(events)

    # Look for arrow notation (LOSS → GRIEF → ...)
    if "→" in message or "->" in message:
        events = re.findall(r"([A-Z]+)", message_upper)
        if len(events) >= 4:
            return "_".join(events)

    return None
