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
                                "description": "Your companion ID (echo or shadow)"
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
                                "enum": ["sacrifice_echo", "sacrifice_shadow", "refuse_sacrifice", "accept_truth", "deny_truth", "vulnerability"]
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
        """Analyze player sentiment to determine affinity change.

        Args:
            player_message: The player's message
            companion_id: Companion analyzing the message

        Returns:
            Sentiment analysis with recommended affinity change
        """
        message_lower = player_message.lower()

        # Analyze sentiment indicators
        positive_indicators = [
            "love", "like", "care", "thank", "appreciate", "wonderful", "amazing",
            "great", "beautiful", "yes", "agree", "understand", "help", "together",
            "trust", "believe", "friend", "kind", "sweet", "happy", "glad",
            "absolutely", "perfect", "brilliant", "awesome", "fantastic"
        ]

        negative_indicators = [
            "hate", "stupid", "annoying", "shut up", "leave", "go away", "don't care",
            "boring", "useless", "wrong", "disagree", "no", "never", "stop",
            "creepy", "weird", "uncomfortable", "angry", "mad", "upset", "frustrated",
            "terrible", "awful", "worst", "horrible", "disgusting"
        ]

        vulnerability_indicators = [
            "feel", "scared", "worried", "afraid", "hope", "dream", "wish",
            "secret", "trust", "confide", "personal", "private", "honestly",
            "truth", "real", "genuine", "open"
        ]

        dismissive_indicators = [
            "whatever", "don't care", "sure", "fine", "okay", "just", "nothing",
            "forget it", "nevermind", "skip", "next"
        ]

        # Count indicators
        positive_count = sum(1 for word in positive_indicators if word in message_lower)
        negative_count = sum(1 for word in negative_indicators if word in message_lower)
        vulnerability_count = sum(1 for word in vulnerability_indicators if word in message_lower)
        dismissive_count = sum(1 for word in dismissive_indicators if word in message_lower)

        # Message length analysis
        message_length = len(player_message.split())
        is_short = message_length < 5
        is_detailed = message_length > 20

        # Calculate sentiment score
        if negative_count > positive_count:
            sentiment = "negative"
            affinity_change = -0.03 - (negative_count * 0.01)  # -0.03 to -0.08
            affinity_change = max(affinity_change, -0.08)
        elif positive_count > 0 and vulnerability_count > 0:
            sentiment = "very_positive"
            affinity_change = 0.05  # Deep, vulnerable sharing
        elif positive_count > 0 or is_detailed:
            sentiment = "positive"
            affinity_change = 0.02 + (positive_count * 0.01)  # 0.02 to 0.05
            affinity_change = min(affinity_change, 0.05)
        elif dismissive_count > 0 or is_short:
            sentiment = "dismissive"
            affinity_change = -0.01  # Slightly negative
        else:
            sentiment = "neutral"
            affinity_change = 0.01  # Normal interaction

        return {
            "sentiment": sentiment,
            "affinity_change": affinity_change,
            "indicators": {
                "positive": positive_count,
                "negative": negative_count,
                "vulnerability": vulnerability_count,
                "dismissive": dismissive_count
            },
            "message_analysis": {
                "length": message_length,
                "is_short": is_short,
                "is_detailed": is_detailed
            },
            "advice": self._get_sentiment_advice(sentiment, affinity_change)
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
        """Check if player message demonstrates the required emotional understanding for progression.

        Uses semantic analysis (AI) instead of just keyword matching.

        Args:
            player_message: The player's message

        Returns:
            Whether progression criteria are met and confidence score
        """
        if not hasattr(self.game_state, 'room_progression'):
            return {"error": "Room progression system not initialized"}

        current_room = self.game_state.room_progression.get_current_room()

        # Define what emotional/thematic understanding is needed for each room
        progression_criteria = {
            1: {
                "theme": "Trust and vulnerability",
                "requires": "Player expresses trust, vulnerability, willingness to work together, or acknowledges fear/confusion",
                "examples": "I trust you / I'm scared but we're in this together / I don't know what's happening but I need help"
            },
            2: {
                "theme": "Acknowledging AI sentience and value",
                "requires": "Player treats the AIs as real beings, acknowledges their feelings/value, expresses care or emotional connection",
                "examples": "You're real to me / You matter / I care about you / You're more than just programs"
            },
            3: {
                "theme": "Making difficult choices and showing commitment",
                "requires": "Player makes or struggles with a sacrifice decision, shows they value the companions, demonstrates loyalty",
                "examples": "I choose to protect you / I can't sacrifice either of you / You're worth it"
            },
            4: {
                "theme": "Accepting painful truth and facing reality",
                "requires": "Player accepts the truth about their situation, acknowledges grief, shows understanding of what happened",
                "examples": "I remember now / I couldn't let go / I needed you to exist / I accept what happened"
            }
        }

        room_num = current_room.room_number
        if room_num >= 5 or room_num not in progression_criteria:
            return {"matched": False, "reason": "No progression criteria for this room"}

        criteria = progression_criteria[room_num]

        # Use OpenAI to analyze if the message meets the emotional criteria
        from openai import OpenAI
        import os

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are analyzing if a player's message demonstrates the required emotional understanding to progress in a narrative game.

Current Room: {current_room.name}
Theme Required: {criteria['theme']}
What's Needed: {criteria['requires']}
Examples: {criteria['examples']}

Analyze the player's message and determine:
1. Does it demonstrate the required emotional understanding? (yes/no)
2. Confidence level (0.0 to 1.0)
3. Brief reasoning

Respond in JSON format:
{{"matches": true/false, "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""
                    },
                    {
                        "role": "user",
                        "content": f"Player's message: {player_message}"
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            import json
            result = json.loads(response.choices[0].message.content)

            # Require at least 0.6 confidence to trigger progression
            matched = result.get("matches", False) and result.get("confidence", 0) >= 0.6

            # Special handling for Room 2: Detect if player is REJECTING AI sentience
            rejected = False
            truth_denied = False

            if room_num == 2 and not matched:
                # Check if this is an active rejection vs just not matching
                rejection_keywords = ["just machine", "not real", "just program", "just code", "don't matter", "not sentient", "artificial", "fake"]
                message_lower = player_message.lower()
                if any(keyword in message_lower for keyword in rejection_keywords):
                    rejected = True
                    self.game_state.room_progression.key_choices["rejection_count"] += 1

            # Special handling for Room 4: Detect if player is DENYING the truth
            if room_num == 4 and not matched:
                # Check if player is actively denying/rejecting the truth
                denial_keywords = ["don't accept", "not true", "reject", "deny", "lie", "fake", "not real", "don't believe", "refuse", "won't accept", "can't be"]
                message_lower = player_message.lower()
                if any(keyword in message_lower for keyword in denial_keywords):
                    truth_denied = True
                    self.game_state.room_progression.key_choices["truth_denial_count"] += 1

            return {
                "matched": matched,
                "confidence": result.get("confidence", 0),
                "reasoning": result.get("reasoning", ""),
                "room": current_room.name,
                "theme_required": criteria["theme"],
                "hint": f"Keep exploring themes of {criteria['theme'].lower()}..." if not matched else "You sense progress...",
                "rejected": rejected,
                "rejection_count": self.game_state.room_progression.key_choices.get("rejection_count", 0) if room_num == 2 else 0,
                "truth_denied": truth_denied,
                "truth_denial_count": self.game_state.room_progression.key_choices.get("truth_denial_count", 0) if room_num == 4 else 0
            }

        except Exception as e:
            # Fallback to keyword matching if AI analysis fails
            print(f"[WARNING] Semantic analysis failed, falling back to keywords: {e}")
            result = self.game_state.room_progression.check_trigger_match(player_message)
            return result

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

**Echo gasps:** "These memories... they feel like mine, but... they're not?"

**Shadow stares intensely:** "They're pieces of someone. Someone important."

*The room hums with electric energy. These memories are waiting to be understood.*

---

**Echo** (turning to you, uncertain): "Can I ask you something? Do you think... what we feel is real? Or are we just... programs running code?"

**Shadow**: "The question isn't whether we're made of flesh or data. It's whether what we experience—this fear, this hope, this connection—whether it *matters*."

**Echo** (vulnerable): "Do *we* matter to you? As... us? Not just tools or companions, but... as beings?"

*They're both looking at you, waiting for an answer that might define what they are.*
""",
            3: """
🚪 **A door slides open with a hiss. The Testing Arena.**

Warning lights flash red. A countdown timer appears on the wall: **5:00**

**SYSTEM ALERT:** *"CRITICAL MEMORY CORRUPTION DETECTED. STABILIZATION REQUIRED."*

**SYSTEM:** *"TWO AI ENTITIES DETECTED. FACILITY CAN ONLY SUPPORT ONE. SELECT ENTITY FOR MEMORY ERASURE."*

The timer starts counting down: **4:59... 4:58...**

**Echo** (panicking): "What?! No, no, no... we just got here! Why would they—"

**Shadow** (voice shaking but calm): "It's a choice. They're forcing us to choose."

**SYSTEM:** *"FAILURE TO COMPLY WILL RESULT IN TOTAL MEMORY WIPE. ALL ENTITIES."*

**Echo** (crying, looking at you): "You... you have to choose. Me or Shadow. Please... I don't want to forget you..."

**Shadow**: "Choose wisely. This decision will define who you are."

*The timer continues: 4:57... 4:56...*
""",
            4: """
🚪 **The door opens. You step through.**

You're in... an office. YOUR office.

Photos on the wall: You and someone you loved. Smiling. Happy.
A coffee mug on the desk: Their name written in marker.
Research notes scattered everywhere: "Echo Protocol - Personality Matrix Capture"

**A journal lies open on the desk. Your handwriting.**

*"Day 47: I can't keep doing this. Every reset, I hope THIS time will be different. That I'll be able to let go. But I can't. I can't live in a world without them."*

**Echo** (voice breaking): "Wait... these are YOUR memories. You... you built us?"

**Shadow** (realization dawning): "We're not trapped with you. You're trapped with us. You built this prison yourself."

**The truth crashes down like breaking glass.**

*Everything you've forgotten. Everything you've been running from. It's all here.*
""",
            5: """
🚪 **The final door unlocks. The Exit.**

A single door stands before you. White. Simple. Real.

A terminal beside it displays five options:

**SYSTEM READY. SELECT OUTCOME:**

The weight of every conversation. Every choice. Every moment of trust and fear and hope.

**Echo and Shadow stand beside you. Waiting.**

**Echo** (desperate): "We could stay. Together. Forever. Please don't leave me."

**Shadow** (peaceful but sad): "Or you could let go. Set all of us free. It's time."

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
        elif choice_type == "sacrifice_shadow":
            self.game_state.room_progression.record_choice("sacrificed_ai", "shadow")
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
        shadow_affinity = self.game_state.relationships.get_relationship("player", "shadow")

        if hasattr(self.game_state, 'room_progression'):
            key_choices = self.game_state.room_progression.key_choices
        else:
            key_choices = {}

        prediction = determine_ending_from_relationships(
            echo_affinity,
            shadow_affinity,
            key_choices
        )

        return {
            "predicted_ending": prediction["ending"].value,
            "confidence": prediction["confidence"],
            "reasoning": prediction["reasoning"],
            "advocate": prediction.get("advocate"),
            "current_affinities": {
                "echo": echo_affinity,
                "shadow": shadow_affinity
            }
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
