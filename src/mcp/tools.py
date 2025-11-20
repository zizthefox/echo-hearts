"""MCP tools that autonomous agents can use to make decisions."""

from typing import Dict, Any, Optional, List
from mcp.types import Tool, TextContent
import json


class MCPTools:
    """Collection of MCP tools for autonomous agents."""

    def __init__(self, game_state):
        """Initialize MCP tools with game state reference.

        Args:
            game_state: Reference to the GameState instance
        """
        self.game_state = game_state

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get OpenAI function calling tool definitions.

        Returns:
            List of tool definitions for OpenAI API
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_relationship_affinity",
                    "description": "Check the current relationship affinity between the companion and another entity (usually 'player'). Use this to decide how vulnerable or open to be in responses.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "companion_id": {
                                "type": "string",
                                "description": "Your companion ID (echo or shadow)"
                            },
                            "target_id": {
                                "type": "string",
                                "description": "The entity to check relationship with (usually 'player')"
                            }
                        },
                        "required": ["companion_id", "target_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_character_memory",
                    "description": "Search your own memories for specific topics or past conversations. Use this to maintain continuity and reference past interactions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "character_id": {
                                "type": "string",
                                "description": "Your character ID (echo or shadow)"
                            },
                            "query": {
                                "type": "string",
                                "description": "What to search for in memories"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum memories to return",
                                "default": 5
                            }
                        },
                        "required": ["character_id", "query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_story_progress",
                    "description": "Check current story state including act, interaction count, and events triggered. Use this to understand where you are in the narrative.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "should_trigger_event",
                    "description": "Check if a specific story event should be triggered now. Use this to decide whether the player is ready for a revelation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "event_id": {
                                "type": "string",
                                "description": "Event to check (first_glitch, questioning_reality, truth_revealed, final_choice)",
                                "enum": ["first_glitch", "questioning_reality", "truth_revealed", "final_choice"]
                            }
                        },
                        "required": ["event_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "trigger_story_event",
                    "description": "Trigger a story event NOW. Only use after checking should_trigger_event and determining player is ready.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "event_id": {
                                "type": "string",
                                "description": "Event to trigger",
                                "enum": ["first_glitch", "questioning_reality", "truth_revealed", "final_choice"]
                            },
                            "intensity": {
                                "type": "string",
                                "description": "How intense to make the reveal",
                                "enum": ["subtle", "moderate", "dramatic"],
                                "default": "moderate"
                            }
                        },
                        "required": ["event_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_ending_readiness",
                    "description": "Check if story can end and which ending is most likely. Use this to know if you should start wrapping up conversations.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_other_companion",
                    "description": "Ask another companion about the player or coordinate reveals. Use this to share information between agents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "companion_id": {
                                "type": "string",
                                "description": "Which companion to query (echo or shadow)"
                            },
                            "question": {
                                "type": "string",
                                "description": "What to ask them"
                            }
                        },
                        "required": ["companion_id", "question"]
                    }
                }
            }
        ]

    # Tool implementation methods

    def check_relationship_affinity(self, companion_id: str, target_id: str) -> Dict[str, Any]:
        """Check relationship affinity between companion and target.

        Args:
            companion_id: The companion checking
            target_id: Who to check relationship with

        Returns:
            Affinity score and description
        """
        affinity = self.game_state.relationships.get_relationship(target_id, companion_id)
        description = self.game_state.relationships.get_relationship_description(affinity)

        return {
            "affinity": affinity,
            "description": description,
            "advice": self._get_relationship_advice(affinity)
        }

    def _get_relationship_advice(self, affinity: float) -> str:
        """Get advice based on affinity level."""
        if affinity >= 0.7:
            return "Very strong relationship. Player trusts you deeply. Safe to share vulnerable truths."
        elif affinity >= 0.4:
            return "Good relationship. Player is friendly. Can hint at deeper topics."
        elif affinity >= 0.1:
            return "Neutral relationship. Build more trust before revealing sensitive information."
        elif affinity >= -0.3:
            return "Weak relationship. Focus on connection before story reveals."
        else:
            return "Negative relationship. Player may be frustrated. Be cautious."

    def query_character_memory(self, character_id: str, query: str, limit: int = 5) -> Dict[str, Any]:
        """Query a character's memories.

        Args:
            character_id: Character whose memories to search
            query: Search query
            limit: Max results

        Returns:
            Matching memories
        """
        companion = self.game_state.companions.get(character_id)
        if not companion:
            return {"error": "Companion not found"}

        memories = companion.memory.search_memories(query)[:limit]
        return {
            "found": len(memories),
            "memories": [m["content"] for m in memories]
        }

    def check_story_progress(self) -> Dict[str, Any]:
        """Check current story progress.

        Returns:
            Story state information
        """
        return {
            "act": self.game_state.story.current_act.name,
            "interaction_count": self.game_state.story.interaction_count,
            "interactions_remaining": 20 - self.game_state.story.interaction_count,
            "events_triggered": self.game_state.story.events_triggered,
            "ending_triggered": self.game_state.story.ending_triggered
        }

    def should_trigger_event(self, event_id: str) -> Dict[str, Any]:
        """Check if an event should be triggered.

        Args:
            event_id: Event to check

        Returns:
            Recommendation on whether to trigger
        """
        # Find the event
        event = next((e for e in self.game_state.story.events if e.event_id == event_id), None)
        if not event:
            return {"should_trigger": False, "reason": "Event not found"}

        # Check if already triggered
        if event.triggered:
            return {"should_trigger": False, "reason": "Event already triggered"}

        # Check interaction threshold
        if self.game_state.story.interaction_count < event.interaction_threshold:
            return {
                "should_trigger": False,
                "reason": f"Too early. Minimum interaction: {event.interaction_threshold}, current: {self.game_state.story.interaction_count}"
            }

        # Check relationship (player should have some trust)
        avg_affinity = sum(self.game_state.get_relationships_summary().values()) / max(len(self.game_state.companions), 1)

        if avg_affinity < -0.2:
            return {
                "should_trigger": False,
                "reason": "Relationship too negative. Build trust first."
            }

        return {
            "should_trigger": True,
            "reason": "Player seems ready. Good timing for this reveal.",
            "recommendation": "Trigger this event naturally in your response."
        }

    def trigger_story_event(self, event_id: str, intensity: str = "moderate") -> Dict[str, Any]:
        """Trigger a story event.

        Args:
            event_id: Event to trigger
            intensity: How dramatic

        Returns:
            Event details
        """
        event = next((e for e in self.game_state.story.events if e.event_id == event_id), None)
        if not event:
            return {"success": False, "error": "Event not found"}

        if event.triggered:
            return {"success": False, "error": "Event already triggered"}

        event.triggered = True
        self.game_state.story.events_triggered.append(event_id)

        return {
            "success": True,
            "event": event_id,
            "narrative": event.narrative,
            "intensity": intensity
        }

    def check_ending_readiness(self) -> Dict[str, Any]:
        """Check if story can end.

        Returns:
            Ending readiness status
        """
        can_end = self.game_state.story.interaction_count >= 18
        relationships = self.game_state.get_relationships_summary()

        if not can_end:
            return {
                "ready": False,
                "interactions_remaining": 18 - self.game_state.story.interaction_count
            }

        # Predict most likely ending
        ending = self.game_state.story.determine_ending(relationships)

        return {
            "ready": True,
            "most_likely_ending": ending.value if ending else "unknown",
            "relationships": relationships,
            "advice": "Story can end now. Consider wrapping up conversations and guiding toward conclusion."
        }

    def query_other_companion(self, companion_id: str, question: str) -> Dict[str, Any]:
        """Query another companion.

        Args:
            companion_id: Companion to ask
            question: Question to ask

        Returns:
            Companion's response
        """
        companion = self.game_state.companions.get(companion_id)
        if not companion:
            return {"error": "Companion not found"}

        # For now, return a summary of their state
        # In full implementation, could actually query their AI
        return {
            "companion": companion.name,
            "current_affinity": self.game_state.relationships.get_relationship("player", companion_id),
            "recent_topics": [m["content"][:50] + "..." for m in companion.memory.get_recent_memories(3)],
            "note": f"{companion.name} has been interacting with the player. Check their memories for details."
        }

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool by name.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool result
        """
        method = getattr(self, tool_name, None)
        if not method:
            return {"error": f"Tool {tool_name} not found"}

        try:
            return method(**arguments)
        except Exception as e:
            return {"error": str(e)}
