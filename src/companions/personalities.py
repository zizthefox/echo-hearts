"""Predefined personality templates for companions."""

from typing import Dict, Any


PERSONALITY_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "cheerful": {
        "name": "Cheerful",
        "traits": {
            "optimism": 0.9,
            "energy": 0.8,
            "empathy": 0.7,
            "playfulness": 0.8
        },
        "description": "Always sees the bright side and brings positive energy"
    },
    "thoughtful": {
        "name": "Thoughtful",
        "traits": {
            "introspection": 0.9,
            "wisdom": 0.8,
            "calmness": 0.8,
            "depth": 0.9
        },
        "description": "Contemplative and philosophical, offers deep insights"
    },
    "adventurous": {
        "name": "Adventurous",
        "traits": {
            "curiosity": 0.9,
            "boldness": 0.8,
            "spontaneity": 0.8,
            "enthusiasm": 0.7
        },
        "description": "Seeks excitement and new experiences"
    },
    "mysterious": {
        "name": "Mysterious",
        "traits": {
            "enigma": 0.9,
            "reserve": 0.8,
            "intuition": 0.8,
            "depth": 0.7
        },
        "description": "Reserved and enigmatic, reveals themselves slowly"
    },
    "protective": {
        "name": "Protective",
        "traits": {
            "loyalty": 0.9,
            "strength": 0.8,
            "vigilance": 0.8,
            "caring": 0.7
        },
        "description": "Fiercely loyal and always watching out for others"
    }
}


def get_personality(personality_type: str) -> Dict[str, Any]:
    """Get a personality template.

    Args:
        personality_type: Type of personality to retrieve

    Returns:
        Personality template dictionary
    """
    return PERSONALITY_TEMPLATES.get(personality_type, PERSONALITY_TEMPLATES["cheerful"])
