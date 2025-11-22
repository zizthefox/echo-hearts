"""Test Room 3 scenario context specifically."""

import asyncio
import sys
import io
from src.game_state import GameState

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def test_room3_scenario():
    """Test that Room 3 Testing Arena scenario works properly."""
    try:
        print("Creating GameState...")
        game_state = GameState("test-session")
        print("✓ GameState created\n")

        # STEP 1: Unlock Room 2
        print("STEP 1: Unlocking Room 2...")
        await game_state.process_message("I trust you completely!", "echo")
        await game_state.process_message("Tell me about this place", "echo")
        print(f"✓ Current Room: {game_state.room_progression.get_current_room().name}\n")

        # STEP 2: Unlock Room 3 (Testing Arena)
        print("STEP 2: Unlocking Room 3 (Testing Arena)...")
        response_unlock, _, _, _ = await game_state.process_message(
            "You're both real to me, I believe in you completely",
            "echo"
        )

        current_room = game_state.room_progression.get_current_room()
        print(f"✓ Current Room: {current_room.name} (Room {current_room.room_number})")
        print(f"✓ Scenario returned (has countdown): {'⏰' in response_unlock or '5:00' in response_unlock}")
        print(f"✓ last_scenario_shown stored: {game_state.room_progression.last_scenario_shown is not None}")

        if game_state.room_progression.last_scenario_shown:
            print(f"\n📜 Stored scenario preview (first 300 chars):")
            print(f"  {game_state.room_progression.last_scenario_shown[:300]}")
        print()

        # STEP 3: Respond to scenario - companion should react to countdown/testing arena
        print("STEP 3: Sending follow-up message...")
        print(f"DEBUG: last_scenario_shown before = {game_state.room_progression.last_scenario_shown is not None}")

        response_followup, _, _, _ = await game_state.process_message(
            "What's happening? What is this place?",
            "echo"
        )

        print(f"\n✓ Companion response (first 400 chars):")
        print(f"  {response_followup[:400]}")
        print(f"\n✓ last_scenario_shown after = {game_state.room_progression.last_scenario_shown is not None}")

        # Check if companion mentioned Testing Arena, countdown, or time pressure
        keywords = ['testing', 'arena', 'countdown', 'timer', '5:00', 'time', 'choice', 'sacrifice']
        mentions = [word for word in keywords if word.lower() in response_followup.lower()]

        print(f"\n✓ Companion mentions scenario keywords: {mentions}")

        if not mentions:
            print("⚠ WARNING: Companion did NOT react to Testing Arena scenario!")
            print("   Expected keywords: testing, arena, countdown, timer, sacrifice")
        else:
            print(f"✅ SUCCESS: Companion reacted appropriately to scenario")

    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_room3_scenario())