"""Utility functions for Echo Hearts UI."""

from pathlib import Path
from typing import Optional


def load_css() -> str:
    """Load CSS from external file.

    Returns:
        CSS string
    """
    css_path = Path(__file__).parent / "styles.css"
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to empty CSS if file not found
        return ""


def get_room_image_path(room_number: int) -> str:
    """Get the image path for a room.

    Args:
        room_number: Room number (1-5)

    Returns:
        Path to room image
    """
    # Actual filenames are room1.jpg, room2.jpg, etc.
    return f"assets/room{room_number}.jpg"


def get_room_title(room_number: int) -> str:
    """Get the title for a room.

    Args:
        room_number: Room number (1-5)

    Returns:
        Room title string
    """
    room_titles = {
        1: "🔓 Room 1: The Awakening Chamber",
        2: "📚 Room 2: The Memory Archives",
        3: "⏱️ Room 3: The Testing Arena",
        4: "💔 Room 4: The Truth Chamber",
        5: "🚪 Room 5: The Exit"
    }
    return room_titles.get(room_number, "Room")


def get_echo_expression_path(expression: str = "neutral") -> str:
    """Get the path to Echo's expression image.

    Args:
        expression: Expression type (neutral, happy, sad, surprised, etc.)

    Returns:
        Path to expression image
    """
    # Map expression names to actual asset filenames
    expressions = {
        "neutral": "assets/echo_avatar_neutral.png",
        "happy": "assets/echo_avatar_happy.png",
        "sad": "assets/echo_avatar_sad.png",
        "surprised": "assets/echo_avatar_surprised.png",
        "worried": "assets/echo_avatar_worried.png",
        "loving": "assets/echo_avatar_loving.png",
        "angry": "assets/echo_avatar_angry.png"
    }
    return expressions.get(expression, "assets/echo_avatar.png")
