"""Debug script to test GameState initialization and message processing."""

import asyncio
import sys
import io
from src.game_state import GameState

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def test_scenario_context():
    """Test that scenario context is passed to companions properly."""
    try:
        print("Creating GameState...")
        game_state = GameState("test-session")
        print("✓ GameState created successfully\n")

        # STEP 1: Trigger Room 1 unlock (move to Room 2)
        print("STEP 1: Triggering Room 1 unlock...")
        response1, memory1, ending1, tools1 = await game_state.process_message(
            "I trust you Echo, we're in this together!",
            "echo"
        )

        current_room = game_state.room_progression.get_current_room()
        print(f"✓ Current Room: {current_room.name} (Room {current_room.room_number})")
        print(f"✓ Response type: {'Scenario only' if '🚪' in response1 else 'Companion response'}")
        print(f"✓ last_scenario_shown stored: {game_state.room_progression.last_scenario_shown is not None}")
        print()

        # STEP 2: Send follow-up message - companion should react to scenario
        print("STEP 2: Sending follow-up message...")
        print(f"DEBUG: last_scenario_shown before message = {game_state.room_progression.last_scenario_shown is not None}")

        response2, memory2, ending2, tools2 = await game_state.process_message(
            "What's happening? Where are we?",
            "echo"
        )

        print(f"✓ Companion response (first 200 chars):")
        print(f"  {response2[:200]}")
        print(f"✓ last_scenario_shown after response: {game_state.room_progression.last_scenario_shown is not None}")
        print()

        # Check if companion mentioned Memory Archives or memories
        mentions_scenario = any(word in response2.lower() for word in ['memory archives', 'fragments', 'pictures', 'screens'])
        print(f"✓ Companion mentions scenario context: {mentions_scenario}")

        if not mentions_scenario:
            print("⚠ WARNING: Companion may not have received scenario context!")

    except Exception as e:
        print(f"\n❌ ERROR occurred: {type(e).__name__}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_scenario_context())
