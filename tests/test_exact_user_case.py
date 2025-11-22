"""Test the exact scenario from the user's screenshot."""

import asyncio
import sys
import io
from src.game_state import GameState

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def test_exact_scenario():
    """Reproduce the exact scenario from the user's screenshot."""
    try:
        print("Creating GameState...")
        game_state = GameState("test-session")
        print("✓ GameState created\n")

        # STEP 1 & 2: Get to Room 3
        print("Setting up: Unlocking rooms...")

        # Room 1 → 2
        r1, _, _, _ = await game_state.process_message("I trust you!", "echo")
        print(f"1. Room 1→2 response type: {'SCENARIO' if '🚪' in r1 else 'COMPANION'}")

        # After room 2 scenario, send follow-up to get companion response
        r2, _, _, _ = await game_state.process_message("OK let's continue", "echo")
        print(f"2. Follow-up in Room 2: {r2[:80]}...")

        # Room 2 → 3
        r3, _, _, _ = await game_state.process_message("You're real to me, I believe in you", "echo")
        print(f"3. Room 2→3 response type: {'SCENARIO' if '🚪' in r3 else 'COMPANION'}")

        if '🚪' in r3:
            # This is the Room 3 Testing Arena scenario
            scenario_response = r3
            print(f"\n✓ Room 3 Testing Arena scenario shown:")
            print(f"   {scenario_response[:300]}...")
            print(f"\n✓ last_scenario_shown = {game_state.room_progression.last_scenario_shown is not None}")
        else:
            print(f"\n⚠ WARNING: Expected scenario but got companion response")
            print(f"   Response: {r3[:200]}...")

        # STEP 3: Send EXACT message from user screenshot
        print("=" * 80)
        print("TESTING EXACT USER MESSAGE FROM SCREENSHOT")
        print("=" * 80)
        print('User message: "memories we are in the new room right??"')
        print()

        response, _, _, _ = await game_state.process_message(
            "memories we are in the new room right??",
            "echo"
        )

        print("Echo's Response:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        print()

        # Analyze response
        good_keywords = ['countdown', 'timer', '5:00', 'testing', 'arena', 'warning', 'system', 'choice', 'sacrifice']
        bad_keywords = ['can\'t access', 'trouble', 'information']

        good_mentions = [w for w in good_keywords if w.lower() in response.lower()]
        bad_mentions = [w for w in bad_keywords if w.lower() in response.lower()]

        print(f"✓ Good keywords mentioned: {good_mentions}")
        if bad_mentions:
            print(f"⚠ Warning keywords found: {bad_mentions}")

        if len(good_mentions) >= 2 and '5:00' in good_mentions or 'countdown' in good_mentions:
            print("\n✅ SUCCESS: Echo is reacting to the Testing Arena countdown scenario!")
        else:
            print("\n⚠ WARNING: Echo may not be fully reacting to the scenario")

    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_exact_scenario())