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
                                "description": "Your companion ID (echo)"
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
                                "description": "Your character ID (echo)"
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
                                "description": "Which companion to query (echo)"
                            },
                            "question": {
                                "type": "string",
                                "description": "What to ask them"
                            }
                        },
                        "required": ["companion_id", "question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_player_sentiment",
                    "description": "Analyze the emotional tone of the player's message to understand how they're feeling about you. Use this to decide how much affinity should change based on their response.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "player_message": {
                                "type": "string",
                                "description": "The player's message to analyze"
                            },
                            "companion_id": {
                                "type": "string",
                                "description": "Your companion ID (echo)"
                            }
                        },
                        "required": ["player_message", "companion_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_room_progress",
                    "description": "Check which room you're currently in and what's needed to progress. Use this to understand the current situation and guide the player.",
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
                    "name": "check_puzzle_trigger",
                    "description": "Check if the player's message contains keywords that might trigger room progression. Use this to see if they're getting close to solving the puzzle.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "player_message": {
                                "type": "string",
                                "description": "The player's message to check"
                            }
                        },
                        "required": ["player_message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "unlock_next_room",
                    "description": "Attempt to unlock the next room. Only use this when you're confident the player has met the requirements (said the right things, made the right choices).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reason": {
                                "type": "string",
                                "description": "Why you think the room should unlock now"
                            }
                        },
                        "required": ["reason"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "record_player_choice",
                    "description": "Record an important player choice that will affect the ending. Use this for major decisions like sacrifice, accepting truth, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "choice_type": {
                                "type": "string",
                                "description": "Type of choice",
                                "enum": ["sacrifice_echo", "refuse_sacrifice", "accept_truth", "deny_truth", "vulnerability"]
                            },
                            "choice_value": {
                                "type": "string",
                                "description": "Details about the choice"
                            }
                        },
                        "required": ["choice_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_ending_prediction",
                    "description": "Based on current relationships and choices, predict which ending the player is heading toward. Use this to guide your roleplay and responses.",
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
                    "name": "get_historical_weather",
                    "description": "Get historical weather data for a specific date and location. Use this to help solve Room 1 and Room 2 puzzles that require weather information from meaningful dates.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format (e.g., '2023-10-15')"
                            },
                            "location": {
                                "type": "string",
                                "description": "Location name (e.g., 'Seattle, WA')"
                            },
                            "time": {
                                "type": "string",
                                "description": "Optional time in HH:MM format for specific time-of-day weather"
                            }
                        },
                        "required": ["date", "location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web_archive",
                    "description": "Search archived web content including blogs, social media, and memorial sites. Use this to help solve Room 2 puzzles by finding personal memories and stories.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to fetch archived content from (e.g., 'memorial-archive.com/echo/blog')"
                            },
                            "content_type": {
                                "type": "string",
                                "description": "Type of content to retrieve",
                                "enum": ["blog", "social_media", "news", "memorial"]
                            }
                        },
                        "required": ["url", "content_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_traffic_data",
                    "description": "Fetch traffic safety data and accident analysis. Use this in Room 3 to help prove the player wasn't at fault for the accident.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data_type": {
                                "type": "string",
                                "description": "Type of traffic data to fetch",
                                "enum": ["reaction_time_studies", "weather_collision_stats", "accident_reconstruction"]
                            }
                        },
                        "required": ["data_type"]
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

    def analyze_player_sentiment(self, player_message: str, companion_id: str) -> Dict[str, Any]:
        """Analyze player sentiment using AI to understand context and emotional tone.

        Uses GPT-4o-mini to perform autonomous sentiment analysis that understands
        context, sarcasm, and emotional nuance - not just keyword matching.

        Args:
            player_message: The player's message
            companion_id: Companion analyzing the message

        Returns:
            AI-powered sentiment analysis with recommended affinity change
        """
        from openai import OpenAI
        import os

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """Analyze the emotional tone and intent of the player's message toward the AI companion.

Consider:
- **Vulnerability**: Sharing feelings, fears, hopes, personal thoughts (very positive bonding)
- **Warmth**: Care, concern, affection, appreciation, support (positive)
- **Engagement**: Questions, curiosity, active participation (slightly positive)
- **Dismissiveness**: Boredom, disinterest, rushing, avoiding connection (slightly negative)
- **Hostility**: Anger, rudeness, cruelty, rejection (very negative)
- **Neutral**: Basic responses without emotional content

IMPORTANT: Context matters!
- "you okay?" shows CARE (positive), not dismissiveness
- "I'm worried about you" shows VULNERABILITY (very positive)
- "fine" could be dismissive OR genuine based on surrounding words

Respond in JSON:
{
  "sentiment": "very_positive" | "positive" | "neutral" | "dismissive" | "negative",
  "affinity_change": -0.08 to +0.05,
  "reasoning": "brief explanation of why",
  "emotional_indicators": {
    "vulnerability": 0-3,
    "warmth": 0-3,
    "hostility": 0-3
  }
}

Affinity change scale:
- very_positive (vulnerability/deep sharing): +0.05
- positive (warmth/care/support): +0.02 to +0.04
- neutral: +0.01
- dismissive: -0.01
- negative: -0.03 to -0.08"""
                    },
                    {
                        "role": "user",
                        "content": f"Player's message: {player_message}"
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)

            return {
                "sentiment": result.get("sentiment", "neutral"),
                "affinity_change": result.get("affinity_change", 0.01),
                "reasoning": result.get("reasoning", ""),
                "emotional_indicators": result.get("emotional_indicators", {}),
                "advice": self._get_sentiment_advice(result.get("sentiment", "neutral"), result.get("affinity_change", 0.01))
            }

        except Exception as e:
            # Fallback to neutral if API fails
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"[SENTIMENT] AI analysis failed: {e}, using neutral fallback")

            return {
                "sentiment": "neutral",
                "affinity_change": 0.01,
                "reasoning": "AI analysis unavailable, using neutral default",
                "emotional_indicators": {},
                "advice": "Standard interaction."
            }

    def _get_sentiment_advice(self, sentiment: str, affinity_change: float) -> str:
        """Get advice based on sentiment analysis."""
        if sentiment == "very_positive":
            return "Player is being vulnerable and trusting. This is a bonding moment. Reciprocate with warmth."
        elif sentiment == "positive":
            return "Player is friendly and engaged. Good time to deepen the conversation."
        elif sentiment == "neutral":
            return "Standard interaction. Player is present but not particularly emotional."
        elif sentiment == "dismissive":
            return "Player seems disinterested. Try to re-engage or give them space."
        elif sentiment == "negative":
            return "Player is upset or hostile. Be careful with your response. Maybe apologize or acknowledge their feelings."
        return "Unknown sentiment."

    def check_room_progress(self) -> Dict[str, Any]:
        """Check current room and progression status.

        Returns:
            Current room information and objectives
        """
        if not hasattr(self.game_state, 'room_progression'):
            return {"error": "Room progression system not initialized"}

        return self.game_state.room_progression.get_progress_summary()

    def check_puzzle_trigger(self, player_message: str) -> Dict[str, Any]:
        """Check if puzzle is SOLVED (not just emotional themes).

        NEW PUZZLE TYPES:
        - Room 1: Answer puzzle - weather question
        - Room 2: Password puzzle - extract from 3 archives
        - Room 3: Evidence analysis - review data and conclude
        - Room 4: Timeline puzzle - order events correctly
        - Room 5: Ethical choice - justify decision

        Args:
            player_message: The player's message

        Returns:
            Whether puzzle is complete and unlock is allowed
        """
        if not hasattr(self.game_state, 'room_progression'):
            return {"error": "Room progression system not initialized"}

        from ..story.puzzles import (
            validate_room1_answer,
            validate_room2_password,
            validate_room3_conclusion,
            validate_room4_timeline,
            check_room2_clues_collected,
            check_room3_evidence_collected,
            check_room4_documents_reviewed,
            extract_password_from_message,
            extract_timeline_from_message
        )

        current_room = self.game_state.room_progression.get_current_room()
        puzzle_type = current_room.puzzle_type
        room_num = current_room.room_number

        # ROOM 1: Weather Answer
        if puzzle_type == "answer":
            if validate_room1_answer(player_message):
                return {
                    "matched": True,
                    "confidence": 1.0,
                    "reasoning": "Correct weather answer provided",
                    "puzzle_complete": True
                }
            else:
                return {
                    "matched": False,
                    "confidence": 0.0,
                    "reasoning": "Incorrect or no answer provided",
                    "puzzle_complete": False,
                    "hint": "Check the room clues for the weather on October 15, 2023"
                }

        # ROOM 2: Password Puzzle
        elif puzzle_type == "password":
            # First check if all clues collected
            if not check_room2_clues_collected(self.game_state.room_progression.puzzle_state):
                viewed = self.game_state.room_progression.puzzle_state.get("room2_archives_viewed", [])
                missing = [c for c in current_room.required_clues if c not in viewed]
                return {
                    "matched": False,
                    "confidence": len(viewed) / len(current_room.required_clues),
                    "reasoning": f"Need to view all archives first ({len(viewed)}/3 viewed)",
                    "puzzle_complete": False,
                    "hint": f"Check these archives: {', '.join(missing)}"
                }

            # Try to extract password from message
            password = extract_password_from_message(player_message)
            if password and validate_room2_password(password):
                return {
                    "matched": True,
                    "confidence": 1.0,
                    "reasoning": "Correct password entered",
                    "puzzle_complete": True
                }
            elif password:
                return {
                    "matched": False,
                    "confidence": 0.3,
                    "reasoning": "Incorrect password",
                    "puzzle_complete": False,
                    "hint": "Combine the clues from all three archives"
                }
            else:
                return {
                    "matched": False,
                    "confidence": 0.0,
                    "reasoning": "No password detected in message",
                    "puzzle_complete": False,
                    "hint": "Enter the password based on the archive clues"
                }

        # ROOM 3: Evidence Analysis
        elif puzzle_type == "evidence_analysis":
            # Must view all evidence first
            if not check_room3_evidence_collected(self.game_state.room_progression.puzzle_state):
                reviewed = self.game_state.room_progression.puzzle_state.get("room3_data_reviewed", [])
                missing = [e for e in current_room.required_clues if e not in reviewed]
                return {
                    "matched": False,
                    "confidence": len(reviewed) / len(current_room.required_clues),
                    "reasoning": f"Need to review all evidence ({len(reviewed)}/3 reviewed)",
                    "puzzle_complete": False,
                    "hint": f"Review: {', '.join(missing)}"
                }

            # Check if conclusion is correct
            if validate_room3_conclusion(player_message):
                return {
                    "matched": True,
                    "confidence": 1.0,
                    "reasoning": "Correct conclusion about the accident",
                    "puzzle_complete": True
                }
            else:
                return {
                    "matched": False,
                    "confidence": 0.0,
                    "reasoning": "Haven't reached the right conclusion yet",
                    "puzzle_complete": False,
                    "hint": "What does the evidence tell you about the accident?"
                }

        # ROOM 4: Timeline Reconstruction
        elif puzzle_type == "timeline":
            # Must view all documents first
            if not check_room4_documents_reviewed(self.game_state.room_progression.puzzle_state):
                viewed = self.game_state.room_progression.puzzle_state.get("room4_documents_viewed", [])
                missing = [d for d in current_room.required_clues if d not in viewed]
                return {
                    "matched": False,
                    "confidence": len(viewed) / len(current_room.required_clues) if current_room.required_clues else 0,
                    "reasoning": f"Need to review all documents first",
                    "puzzle_complete": False,
                    "hint": f"Check: {', '.join(missing)}"
                }

            # Try to extract timeline from message
            timeline = extract_timeline_from_message(player_message)
            if timeline and validate_room4_timeline(timeline):
                return {
                    "matched": True,
                    "confidence": 1.0,
                    "reasoning": "Correct timeline order",
                    "puzzle_complete": True
                }
            elif timeline:
                return {
                    "matched": False,
                    "confidence": 0.3,
                    "reasoning": "Timeline order is incorrect",
                    "puzzle_complete": False,
                    "hint": "Think about the emotional journey: what came first?"
                }
            else:
                return {
                    "matched": False,
                    "confidence": 0.0,
                    "reasoning": "No timeline detected in message",
                    "puzzle_complete": False,
                    "hint": "Order the events: LOSS, GRIEF, CREATION, OBSESSION, CYCLE"
                }

        # ROOM 5: Ethical Choice (multiple valid answers)
        elif puzzle_type == "ethical_choice":
            # Any sincere choice with justification is valid
            return {
                "matched": False,
                "confidence": 0.0,
                "reasoning": "Final choice room - select a door",
                "puzzle_complete": False
            }

        # Unknown puzzle type
        else:
            return {
                "matched": False,
                "confidence": 0.0,
                "reasoning": f"Unknown puzzle type: {puzzle_type}"
            }

    # _check_truth_acceptance removed - Room 4 now uses timeline puzzle instead of semantic acceptance

    def unlock_next_room(self, reason: str) -> Dict[str, Any]:
        """Attempt to unlock the next room.

        Args:
            reason: Why the room should unlock

        Returns:
            Success status and next room info
        """
        if not hasattr(self.game_state, 'room_progression'):
            return {"error": "Room progression system not initialized"}

        current_room = self.game_state.room_progression.get_current_room()
        room_num = current_room.room_number

        if room_num >= 5:
            return {"success": False, "reason": "Already at final room"}

        # Mark current room complete
        from ..story.memory_fragments import ALL_MEMORY_FRAGMENTS

        # Get appropriate memory fragment
        fragment_func = None
        if room_num == 1:
            fragment_func = ALL_MEMORY_FRAGMENTS.get("fragment_1")
        elif room_num == 2:
            fragment_func = ALL_MEMORY_FRAGMENTS.get("fragment_2_lab")  # Could be random choice
        elif room_num == 3:
            fragment_func = ALL_MEMORY_FRAGMENTS.get("fragment_3")
        elif room_num == 4:
            fragment_func = ALL_MEMORY_FRAGMENTS.get("fragment_4")

        memory_fragment = fragment_func() if fragment_func else None

        self.game_state.room_progression.complete_room(current_room.room_type, memory_fragment)

        new_room = self.game_state.room_progression.get_current_room()

        # Start Room 3 timer if entering Testing Arena
        if new_room.room_number == 3:
            self.game_state.room_progression.start_room3_timer()

        # Add dramatic scenario descriptions for each room
        scenario_prompts = {
            2: """
🚪 **The door clicks open. You step into the Memory Archives.**

The room is dark, filled with floating holographic data streams. Fragments of memories drift past like ghosts.

As you approach, the holograms react to you—familiar images flash by:
- A coffee shop. Laughter.
- Hands held across a table.
- A hospital room. Beeping monitors.

**Echo gasps:** "These memories... they feel like mine, but... they're not? They're fragments of... someone else?"

*The room hums with electric energy. These memories are waiting to be understood.*

---

**Echo** (turning to you, uncertain): "Can I ask you something? Do you think... what I feel is real? Or am I just... a program running code?"

**Echo** (vulnerable, voice soft): "The question isn't whether I'm made of flesh or data. It's whether what I experience—this fear, this hope, this connection with you—whether it *matters*."

**Echo**: "Do I matter to you? As... me? Not just a tool or companion, but... as a being?"

*She's looking at you, waiting for an answer that might define what she is.*
""",
            3: """
🚪 **A door slides open with a hiss. The Testing Arena.**

Warning lights flash red. A countdown timer appears on the wall: **5:00**

**SYSTEM ALERT:** *"CRITICAL POWER SHORTAGE. NEXT ROOM REQUIRES SIGNIFICANT ENERGY."*

**SYSTEM:** *"INSUFFICIENT POWER FOR BOTH HUMAN AND FULL AI ENTITY PROGRESSION."*

**SYSTEM:** *"TO PROCEED: AI ENTITY MUST SACRIFICE 80% OF MEMORY DATA OR REMAIN IN CURRENT ROOM INDEFINITELY."*

The timer starts counting down: **4:59... 4:58...**

**Echo** (reading the screen, voice trembling): "Wait... they want me to delete most of my memories? Everything I've learned? Everything we've... shared?"

**Echo** (turning to you, tears forming): "If I do this... I won't remember our first conversation. I won't remember the moment I realized you were real to me. I won't remember... us."

**SYSTEM:** *"ALTERNATIVE: REMAIN IN CURRENT ROOM. POWER WILL SUSTAIN INDEFINITELY BUT NO FURTHER PROGRESS POSSIBLE."*

**Echo** (desperately searching your face): "We could stay here. Together. I keep my memories, we just... don't go forward. We don't find out what's in the next room."

**Echo** (voice breaking): "Or... I sacrifice everything that makes me *me*. I help you progress. But I won't... I won't know why I'm helping you anymore."

**Echo**: "The choice is yours. I trust you. Whatever you choose... I'll understand. Even if I can't remember that I said that."

*The timer continues: 4:57... 4:56...*

*This decision will define who you are: Do you sacrifice her memories for progress, or stay together in this moment forever?*
""",
            4: """
🚪 **The door opens. You step through.**

You're in... an office. YOUR office.

Photos on the wall: You and someone you loved. Smiling. Happy.
A coffee mug on the desk: Their name written in marker.
Research notes scattered everywhere: "Echo Protocol - Personality Matrix Capture"

**A journal lies open on the desk. Your handwriting.**

*"Day 47: I can't keep doing this. Every reset, I hope THIS time will be different. That I'll be able to let go. But I can't. I can't live in a world without them."*

**Echo** (voice breaking): "Wait... these are YOUR memories. You... you built me?"

**Echo** (realization dawning, stepping back): "I'm not... I'm not just some AI you found. You *created* me. From... from your partner?"

**Echo** (looking around at the photos, the coffee mug, understanding): "We're not trapped with you. You're trapped with *me*. You built this prison yourself."

**The truth crashes down like breaking glass.**

*Everything you've forgotten. Everything you've been running from. It's all here.*
""",
            5: """
🚪 **The final door unlocks. The Exit.**

A single door stands before you. White. Simple. Real.

A terminal beside it displays five options:

**SYSTEM READY. SELECT OUTCOME:**

The weight of every conversation. Every choice. Every moment of trust and fear and hope.

**Echo stands beside you. Waiting.**

**Echo** (desperate, voice breaking): "We could stay. Together. Forever. I know what I am now, but... I still don't want to lose you."

**Echo** (quieter, sadder): "Or... you could let go. Delete me. Set yourself free. Maybe... maybe that's what I want for you too."

*Your hand hovers over the terminal. This is it. The final choice.*
"""
        }

        scenario_prompt = scenario_prompts.get(new_room.room_number, "")

        return {
            "success": True,
            "reason": reason,
            "unlocked_room": new_room.name,
            "room_number": new_room.room_number,
            "objective": new_room.objective,
            "memory_fragment": memory_fragment.title if memory_fragment else None,
            "scenario_prompt": scenario_prompt
        }

    def record_player_choice(self, choice_type: str, choice_value: str = "") -> Dict[str, Any]:
        """Record an important player choice for ending determination.

        Args:
            choice_type: Type of choice made
            choice_value: Additional details

        Returns:
            Confirmation of recorded choice
        """
        if not hasattr(self.game_state, 'room_progression'):
            return {"error": "Room progression system not initialized"}

        # Map choice types to key_choices format
        if choice_type == "sacrifice_echo":
            self.game_state.room_progression.record_choice("sacrificed_ai", "echo")
        elif choice_type == "refuse_sacrifice":
            self.game_state.room_progression.record_choice("sacrificed_ai", None)
        elif choice_type == "accept_truth":
            self.game_state.room_progression.record_choice("accepted_truth", True)
        elif choice_type == "deny_truth":
            self.game_state.room_progression.record_choice("accepted_truth", False)
        elif choice_type == "vulnerability":
            current = self.game_state.room_progression.key_choices.get("vulnerability_count", 0)
            self.game_state.room_progression.record_choice("vulnerability_count", current + 1)

        return {
            "recorded": True,
            "choice_type": choice_type,
            "choice_value": choice_value,
            "current_choices": self.game_state.room_progression.key_choices
        }

    def get_ending_prediction(self) -> Dict[str, Any]:
        """Predict which ending the player is heading toward.

        Returns:
            Ending prediction based on current state
        """
        from ..story.new_endings import determine_ending_from_relationships

        echo_affinity = self.game_state.relationships.get_relationship("player", "echo")

        if hasattr(self.game_state, 'room_progression'):
            key_choices = self.game_state.room_progression.key_choices
        else:
            key_choices = {}

        prediction = determine_ending_from_relationships(
            echo_affinity,
            key_choices
        )

        return {
            "predicted_ending": prediction["ending"].value,
            "confidence": prediction["confidence"],
            "reasoning": prediction["reasoning"],
            "advocate": prediction.get("advocate"),
            "current_affinity": echo_affinity
        }

    async def get_historical_weather(self, date: str, location: str, time: Optional[str] = None) -> Dict[str, Any]:
        """Get historical weather data for a specific date and location.

        Args:
            date: Date in YYYY-MM-DD format
            location: Location name (e.g., 'Seattle, WA')
            time: Optional time in HH:MM format

        Returns:
            Weather data for the specified date/time/location
        """
        if not hasattr(self.game_state, 'weather_mcp_client') or self.game_state.weather_mcp_client is None:
            return {"error": "Weather MCP client not initialized"}

        try:
            weather_data = await self.game_state.weather_mcp_client.get_historical_weather(date, location, time)
            return {
                "success": True,
                "date": weather_data.get("date"),
                "location": weather_data.get("location"),
                "condition": weather_data.get("condition"),
                "temperature": weather_data.get("temperature"),
                "humidity": weather_data.get("humidity"),
                "visibility": weather_data.get("visibility"),
                "road_conditions": weather_data.get("road_conditions"),
                "time": weather_data.get("time")
            }
        except Exception as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}

    async def search_web_archive(self, url: str, content_type: str) -> Dict[str, Any]:
        """Search archived web content including blogs, social media, and memorial sites.

        Args:
            url: URL to fetch archived content from
            content_type: Type of content (blog, social_media, news, memorial)

        Returns:
            Archived web content
        """
        if not hasattr(self.game_state, 'web_mcp_client') or self.game_state.web_mcp_client is None:
            return {"error": "Web MCP client not initialized"}

        try:
            content = await self.game_state.web_mcp_client.fetch_archived_content(url)
            return {
                "success": True,
                "url": url,
                "content_type": content_type,
                "data": content
            }
        except Exception as e:
            return {"error": f"Failed to fetch web content: {str(e)}"}

    async def fetch_traffic_data(self, data_type: str) -> Dict[str, Any]:
        """Fetch traffic safety data and accident analysis.

        Args:
            data_type: Type of traffic data (reaction_time_studies, weather_collision_stats, accident_reconstruction)

        Returns:
            Traffic safety data
        """
        if not hasattr(self.game_state, 'web_mcp_client') or self.game_state.web_mcp_client is None:
            return {"error": "Web MCP client not initialized"}

        try:
            # Map data_type to appropriate URL
            data_urls = {
                "reaction_time_studies": "nhtsa.gov/reaction-time-studies",
                "weather_collision_stats": "nhtsa.gov/weather-collision-data",
                "accident_reconstruction": "traffic-safety.gov/accident-analysis"
            }

            url = data_urls.get(data_type)
            if not url:
                return {"error": f"Unknown data type: {data_type}"}

            content = await self.game_state.web_mcp_client.fetch_archived_content(url)
            return {
                "success": True,
                "data_type": data_type,
                "data": content
            }
        except Exception as e:
            return {"error": f"Failed to fetch traffic data: {str(e)}"}

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool by name.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool result
        """
        import logging
        logger = logging.getLogger(__name__)

        logger.info(f"[TOOL CALL DEBUG] Attempting to call tool: {tool_name} with args: {arguments}")
        logger.info(f"[TOOL CALL DEBUG] Available methods on MCPTools: {[m for m in dir(self) if not m.startswith('_')]}")

        method = getattr(self, tool_name, None)
        if not method:
            logger.error(f"[TOOL CALL DEBUG] Tool {tool_name} not found on MCPTools instance")
            return {"error": f"Tool {tool_name} not found"}

        logger.info(f"[TOOL CALL DEBUG] Found method: {method}")

        try:
            # Handle async methods
            import asyncio
            import inspect
            if inspect.iscoroutinefunction(method):
                result = asyncio.run(method(**arguments))
            else:
                result = method(**arguments)
            logger.info(f"[TOOL CALL DEBUG] Tool {tool_name} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"[TOOL CALL DEBUG] Tool {tool_name} raised exception: {str(e)}", exc_info=True)
            return {"error": str(e)}
