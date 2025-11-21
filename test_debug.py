"""Debug script to test GameState initialization and message processing."""

import asyncio
from src.game_state import GameState


async def test_game_state():
    """Test creating GameState and processing a message."""
    try:
        print("Creating GameState...")
        game_state = GameState("test-session")
        print("OK - GameState created successfully")

        print("\nProcessing test message with trust trigger...")
        response, memory_fragment, ending, tool_calls = await game_state.process_message(
            "I trust you Echo, we're in this together!",
            "echo"
        )

        print(f"\nOK - Message processed successfully")
        print(f"Response: {response[:100]}...")
        print(f"Memory Fragment: {memory_fragment}")
        print(f"Ending: {ending}")
        print(f"Tool Calls: {len(tool_calls)} made")

        # Check if room progressed
        current_room = game_state.room_progression.get_current_room()
        print(f"\nCurrent Room: {current_room.name} (Room {current_room.room_number})")

    except Exception as e:
        print(f"\nERROR occurred: {type(e).__name__}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_game_state())
