# Echo Hearts: Puzzle-First Revamp Plan

## Problem Identified
Currently, players can bypass puzzles by just talking emotionally. Echo solves puzzles FOR the player using MCP tools. This defeats the purpose of an escape room game.

## Solution: Puzzle-First Design

### ✅ COMPLETED

1. **Room Dataclass Updated** ([rooms.py:28-51](rooms.py:28-51))
   - Added `puzzle_type` field (answer/multi_clue/choice/acceptance)
   - Added `required_clues` field (for multi-step puzzles)
   - Separated `emotional_themes` (relationship) from `hint_keywords` (guidance)
   - Removed old `conversational_triggers` (was causing bypass)

2. **Puzzle State Tracking** ([rooms.py:72-79](rooms.py:72-79))
   - New `puzzle_state` dict tracks actual player actions:
     - `room1_clues_found`: ["newspaper", "calendar", "weather"]
     - `room2_archives_viewed`: ["blog", "social_media", "news"]
     - `room3_data_reviewed`: traffic data viewed (optional)
     - `room4_acceptance_expressed`: semantic detection

3. **Room Configurations Rewritten** ([rooms.py:95-223](rooms.py:95-223))
   ```
   Room 1: puzzle_type="answer", answer="Light rain"
   Room 2: puzzle_type="multi_clue", required_clues=["blog", "social_media", "news"]
   Room 3: puzzle_type="choice", timer-based sacrifice
   Room 4: puzzle_type="acceptance", semantic grief detection
   Room 5: puzzle_type="choice", ending selection
   ```

4. **Echo's Personality Updated** ([personalities.py:47-76](personalities.py:47-76))
   - Changed from "solve puzzles" to "guide exploration"
   - Examples:
     - ❌ OLD: "Let me check weather... it was light rain!"
     - ✅ NEW: "That terminal is asking about weather... maybe check that newspaper?"
   - Hints toward unexplored clues, doesn't provide answers

---

## 🚧 NEEDS IMPLEMENTATION

### 1. New MCP Tools

Create these tools in [tools.py](tools.py):

```python
def check_puzzle_state(room_number: int) -> Dict[str, Any]:
    """Check what clues/progress player has made in current room.

    Returns:
        {
            "room": 1,
            "puzzle_type": "answer",
            "clues_found": ["newspaper", "calendar"],
            "required_clues": 3,
            "puzzle_solved": false,
            "hint_suggestion": "Player hasn't checked weather terminal yet"
        }
    """
    pass

def validate_puzzle_answer(room_number: int, answer: str) -> Dict[str, Any]:
    """Check if player's answer is correct.

    Returns:
        {
            "correct": true/false,
            "exact_match": "Light rain",
            "attempts": 2
        }
    """
    pass

def record_clue_found(room_number: int, clue_id: str) -> Dict[str, Any]:
    """Track that player viewed a clue (newspaper, terminal, etc).

    Returns:
        {
            "recorded": true,
            "clue": "newspaper",
            "total_found": 2,
            "remaining": ["weather"]
        }
    """
    pass
```

### 2. Update `check_puzzle_trigger` Logic

Modify [tools.py:622-748](tools.py:622-748):

```python
def check_puzzle_trigger(player_message: str) -> Dict[str, Any]:
    """Check if puzzle is SOLVED (not just emotional themes).

    Room 1 (Answer Type):
        - Check if message contains puzzle_answer
        - Fuzzy match: "light rain", "rainy", "it rained"
        - Return matched=true ONLY if answer is correct
        - Emotional themes DON'T unlock (just build relationship)

    Room 2 (Multi-Clue Type):
        - Check puzzle_state["room2_archives_viewed"]
        - Return matched=true ONLY if len(archives_viewed) == 3
        - Saying "you're real" doesn't unlock

    Room 3 (Choice Type):
        - Return matched=true when timer expires OR choice made
        - Detect: "sacrifice echo", "sacrifice shadow", "refuse"

    Room 4 (Acceptance Type):
        - Use semantic analysis (keep current AI logic)
        - Detect grief acceptance themes
        - Require confidence >= 0.7 (higher than before)
    """

    current_room = self.game_state.room_progression.get_current_room()
    puzzle_type = current_room.puzzle_type

    if puzzle_type == "answer":
        # Check exact answer match
        answer_match = self._check_answer_match(
            player_message,
            current_room.puzzle_answer
        )
        if answer_match:
            return {
                "matched": True,
                "confidence": 1.0,
                "reasoning": f"Correct answer provided: '{current_room.puzzle_answer}'"
            }

    elif puzzle_type == "multi_clue":
        # Check if all required clues viewed
        viewed = self.game_state.room_progression.puzzle_state.get(
            f"room{current_room.room_number}_archives_viewed",
            []
        )
        required = current_room.required_clues
        if set(required).issubset(set(viewed)):
            return {
                "matched": True,
                "confidence": 1.0,
                "reasoning": "All required archives accessed"
            }

    # ... etc for other types

    # IMPORTANT: Emotional themes analyzed separately!
    # They affect relationship, NOT progression
    emotional_analysis = self._analyze_emotional_themes(
        player_message,
        current_room.emotional_themes
    )

    return {
        "matched": False,
        "puzzle_complete": False,
        "emotional_resonance": emotional_analysis,
        "hint": f"Puzzle not solved. Try investigating the room."
    }
```

### 3. Update UI Clue Click Handlers

Modify [interface.py:905-1087](interface.py:905-1087):

When player clicks newspaper/calendar/weather, call new MCP tool:

```python
def show_newspaper_clue(game_state):
    # Record that clue was found
    game_state.room_progression.puzzle_state["room1_clues_found"].append("newspaper")

    # Show newspaper content
    content = "..."
    return content
```

### 4. Update Agents Prompt

Modify [agents.py:120-187](agents.py:120-187):

```markdown
**CRITICAL: Puzzle Validation Rules**

Room 1:
- Player MUST say "light rain" or "rainy" to unlock
- Saying "I trust you" does NOT unlock (builds relationship only)
- Use `check_puzzle_state` to see if they've found clues
- Hint: "Have you checked the [clue they haven't found] yet?"

Room 2:
- Player MUST click all 3 archive terminals
- Saying "you're real" does NOT unlock
- Use `check_puzzle_state` to see viewed archives
- Hint: "We still need to check the [missing archive]"

Room 3:
- Auto-unlocks when timer expires OR choice made
- You can't manually unlock this one

Room 4:
- Semantic analysis (current system works)
- Require higher confidence (0.7 instead of 0.6)
```

---

## Testing Checklist

After implementation, test:

- [ ] Room 1: Saying "I trust you" → relationship up, room DOESN'T unlock
- [ ] Room 1: Saying "light rain" → room unlocks
- [ ] Room 1: Saying "rainy" → room unlocks (fuzzy match)
- [ ] Room 2: Saying "you're real" → relationship up, room DOESN'T unlock
- [ ] Room 2: Viewing all 3 archives → room unlocks
- [ ] Room 2: Viewing only 2 archives → Echo hints at missing one
- [ ] Room 3: Timer expires → default sacrifice, room unlocks
- [ ] Room 3: Making choice before timer → room unlocks
- [ ] Echo gives HINTS, not ANSWERS throughout

---

## Migration Notes

**Breaking Changes:**
- Room dataclass has new fields (existing saves will break)
- `conversational_triggers` removed (code using it will error)
- `check_puzzle_trigger` returns different schema

**Backwards Compatibility:**
- Need migration for existing `Room` objects
- Add default values for new fields in `__init__`

---

## Rationale

**Why This Design?**

1. **Escape Room Feel**: Players must actually solve puzzles, not bypass with emotion
2. **Echo as Guide**: She helps you think, doesn't think FOR you
3. **Relationship Separate**: Trust/emotion affects ENDING, not progression
4. **Clear Requirements**: Each room has explicit completion criteria
5. **MCP Showcase**: Tools track state, validate answers, provide hints

**Player Experience:**
- More engaging (actually solving puzzles)
- Echo feels more like a companion (collaborative exploration)
- Clearer objectives (know what you need to do)
- Rewarding (unlocking through effort, not just talking)

**Developer Experience:**
- Easier to balance difficulty
- Clearer separation of concerns (puzzle vs. emotion)
- Better telemetry (track exactly what players do)
- MCP tools have clear, testable responsibilities