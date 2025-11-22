"""Test if GameState persists correctly in Gradio's gr.State."""

import sys
import os
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_state import GameState
from src.story.rooms import RoomProgression

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_state_persistence():
    """Test if GameState attributes persist correctly."""

    logger.info("=" * 80)
    logger.info("TESTING GAMESTATE PERSISTENCE")
    logger.info("=" * 80)

    # Create GameState
    game_state = GameState("test-session")
    logger.info(f"✓ Created GameState with ID: {id(game_state)}")
    logger.info(f"✓ RoomProgression ID: {id(game_state.room_progression)}")

    # Set last_scenario_shown (simulating room unlock)
    test_scenario = "Test scenario content for Room 2"
    game_state.room_progression.last_scenario_shown = test_scenario
    logger.info(f"✓ Set last_scenario_shown (length: {len(test_scenario)} chars)")

    # Check if it's still there (simulating next Gradio request with SAME object)
    if game_state.room_progression.last_scenario_shown == test_scenario:
        logger.info("✅ SUCCESS: Scenario persists in same GameState object")
    else:
        logger.error("❌ FAIL: Scenario lost in same GameState object")

    # Now test what Gradio does: simulate pickling/unpickling
    logger.info("\n--- Testing Pickle Serialization (what Gradio does) ---")

    try:
        import pickle

        # Try to pickle GameState
        serialized = pickle.dumps(game_state)
        logger.info("✓ GameState can be pickled")

        # Unpickle it
        restored_state = pickle.loads(serialized)
        logger.info(f"✓ GameState unpickled, new ID: {id(restored_state)}")

        # Check if scenario persists after pickle/unpickle
        if restored_state.room_progression.last_scenario_shown == test_scenario:
            logger.info("✅ SUCCESS: Scenario persists after pickle/unpickle")
        else:
            logger.error("❌ FAIL: Scenario lost after pickle/unpickle")
            logger.info(f"Value: {restored_state.room_progression.last_scenario_shown}")

    except Exception as e:
        logger.error(f"❌ FAIL: Cannot pickle GameState: {type(e).__name__}: {e}")
        logger.info("This means Gradio gr.State may not persist GameState properly!")

    logger.info("\n" + "=" * 80)
    logger.info("TEST COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    test_state_persistence()