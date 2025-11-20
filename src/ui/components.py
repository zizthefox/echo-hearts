"""Reusable UI components."""

import gradio as gr
from typing import List, Dict, Any


def create_companion_card(companion_name: str, personality: str, affinity: float) -> str:
    """Create a companion info card.

    Args:
        companion_name: Name of the companion
        personality: Personality type
        affinity: Relationship affinity score

    Returns:
        Markdown formatted card
    """
    affinity_bar = "█" * int(abs(affinity) * 10)
    affinity_label = "Positive" if affinity >= 0 else "Negative"

    return f"""
### {companion_name}
**Personality:** {personality}
**Affinity:** {affinity_label} {affinity_bar} ({affinity:.2f})
"""


def create_relationship_graph(relationships: Dict[str, float]) -> str:
    """Create a text-based relationship visualization.

    Args:
        relationships: Dictionary of entity pairs to affinity scores

    Returns:
        Markdown formatted relationship display
    """
    if not relationships:
        return "*No relationships yet*"

    lines = []
    for (entity1, entity2), affinity in relationships.items():
        symbol = "❤️" if affinity > 0.5 else "💔" if affinity < -0.5 else "🤝"
        lines.append(f"{entity1} {symbol} {entity2} ({affinity:+.2f})")

    return "\n".join(lines)


def create_memory_display(memories: List[Dict[str, Any]], limit: int = 5) -> str:
    """Create a formatted display of recent memories.

    Args:
        memories: List of memory dictionaries
        limit: Maximum number of memories to show

    Returns:
        Markdown formatted memory list
    """
    if not memories:
        return "*No memories yet*"

    recent = memories[-limit:]
    lines = ["### Recent Memories\n"]

    for memory in recent:
        timestamp = memory.get("timestamp", "")[:10]  # Just the date
        content = memory.get("content", "")
        memory_type = memory.get("type", "")

        lines.append(f"**{timestamp}** [{memory_type}]: {content}")

    return "\n".join(lines)
