"""Relationship tracking between companions and with the player."""

from typing import Dict, List, Tuple
from datetime import datetime


class RelationshipTracker:
    """Tracks relationships and dynamics between entities."""

    def __init__(self):
        """Initialize the relationship tracker."""
        # Store relationships as (entity1, entity2) -> affinity_score
        self.relationships: Dict[Tuple[str, str], float] = {}
        self.relationship_history: List[Dict] = []

    def update_relationship(
        self,
        entity1: str,
        entity2: str,
        change: float,
        reason: str = None
    ) -> float:
        """Update relationship between two entities.

        Args:
            entity1: First entity ID
            entity2: Second entity ID
            change: Change in affinity (-1.0 to 1.0)
            reason: Optional reason for the change

        Returns:
            New affinity score
        """
        # Normalize the key (always store alphabetically)
        key = tuple(sorted([entity1, entity2]))

        current = self.relationships.get(key, 0.0)
        new_affinity = max(-1.0, min(1.0, current + change))
        self.relationships[key] = new_affinity

        # Record the change in history
        self.relationship_history.append({
            "timestamp": datetime.now().isoformat(),
            "entity1": entity1,
            "entity2": entity2,
            "change": change,
            "new_affinity": new_affinity,
            "reason": reason
        })

        return new_affinity

    def get_relationship(self, entity1: str, entity2: str) -> float:
        """Get relationship affinity between two entities.

        Args:
            entity1: First entity ID
            entity2: Second entity ID

        Returns:
            Affinity score (-1.0 to 1.0), 0.0 if no relationship exists
        """
        key = tuple(sorted([entity1, entity2]))
        return self.relationships.get(key, 0.0)

    def get_all_relationships(self, entity_id: str) -> Dict[str, float]:
        """Get all relationships for a specific entity.

        Args:
            entity_id: Entity to get relationships for

        Returns:
            Dictionary mapping other entity IDs to affinity scores
        """
        result = {}
        for (e1, e2), affinity in self.relationships.items():
            if e1 == entity_id:
                result[e2] = affinity
            elif e2 == entity_id:
                result[e1] = affinity
        return result

    def get_relationship_description(self, affinity: float) -> str:
        """Convert affinity score to a descriptive label.

        Args:
            affinity: Affinity score (-1.0 to 1.0)

        Returns:
            Descriptive label
        """
        if affinity >= 0.8:
            return "Very Close"
        elif affinity >= 0.5:
            return "Friends"
        elif affinity >= 0.2:
            return "Friendly"
        elif affinity >= -0.2:
            return "Neutral"
        elif affinity >= -0.5:
            return "Tense"
        elif affinity >= -0.8:
            return "Hostile"
        else:
            return "Enemies"
