"""Find what makes GameState unpicklable."""

import sys
import os
import pickle

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_state import GameState


def test_picklability(obj, name):
    """Test if an object can be pickled."""
    try:
        pickle.dumps(obj)
        print(f"[OK] {name} is picklable")
        return True
    except Exception as e:
        print(f"[FAIL] {name} is NOT picklable: {type(e).__name__}")
        return False


def main():
    print("=" * 80)
    print("FINDING UNPICKLABLE COMPONENTS IN GAMESTATE")
    print("=" * 80)

    game_state = GameState("test-session")

    # Test each component
    print("\nTesting components:")
    test_picklability(game_state.session_id, "session_id")
    test_picklability(game_state.conversation, "conversation")
    test_picklability(game_state.relationships, "relationships")
    test_picklability(game_state.room_progression, "room_progression")

    print("\nTesting MCP components:")
    test_picklability(game_state.mcp_server, "mcp_server")
    test_picklability(game_state.mcp_client, "mcp_client")

    print("\nTesting companions:")
    for comp_id, companion in game_state.companions.items():
        test_picklability(companion, f"companion[{comp_id}]")

        # Test companion's internal components
        if hasattr(companion, 'client'):
            test_picklability(companion.client, f"companion[{comp_id}].client (OpenAI)")
        if hasattr(companion, 'mcp_client'):
            test_picklability(companion.mcp_client, f"companion[{comp_id}].mcp_client")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()