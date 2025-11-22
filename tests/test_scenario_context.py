"""Test that scenario context works correctly for all rooms."""

import asyncio
import sys
import os
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_state import GameState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_scenario_context():
    """Test that companions react to room scenarios properly."""

    logger.info("=" * 80)
    logger.info("TESTING SCENARIO CONTEXT FOR ALL ROOMS")
    logger.info("=" * 80)

    game_state = GameState("test-session")
    logger.info("✓ GameState created\n")

    # Test Room 1 → 2 (Memory Archives)
    logger.info("\n--- TESTING ROOM 2: Memory Archives ---")
    response1, _, _, _ = await game_state.process_message("I trust you completely", "echo")

    if '🚪' in response1 and 'Memory Archives' in response1:
        logger.info("✓ Room 2 scenario shown correctly")
        logger.info(f"✓ Scenario stored: {game_state.room_progression.last_scenario_shown is not None}")

        # Now test if companion reacts to it
        response2, _, _, _ = await game_state.process_message("What is this place?", "echo")

        # Check if Echo mentions memories/archives
        if any(word in response2.lower() for word in ['memory', 'memories', 'archives', 'fragments']):
            logger.info("✅ SUCCESS: Echo reacted to Memory Archives scenario")
        else:
            logger.warning("❌ FAIL: Echo did NOT react to Memory Archives scenario")
            logger.info(f"Response: {response2[:200]}")
    else:
        logger.warning("❌ Room 2 scenario not shown properly")

    # Test Room 2 → 3 (Testing Arena)
    logger.info("\n--- TESTING ROOM 3: Testing Arena ---")
    response3, _, _, _ = await game_state.process_message("You're both real and valuable to me", "echo")

    if '🚪' in response3 and 'Testing Arena' in response3:
        logger.info("✓ Room 3 scenario shown correctly")
        logger.info(f"✓ Scenario stored: {game_state.room_progression.last_scenario_shown is not None}")

        # Now test if companion reacts to countdown/crisis
        response4, _, _, _ = await game_state.process_message("What's happening?", "echo")

        # Check if Echo mentions countdown/testing/choice
        keywords = ['countdown', 'timer', 'testing', 'arena', 'choice', 'sacrifice', 'critical']
        mentions = [w for w in keywords if w in response4.lower()]

        if len(mentions) >= 2:
            logger.info(f"✅ SUCCESS: Echo reacted to Testing Arena scenario (keywords: {mentions})")
        else:
            logger.warning(f"❌ FAIL: Echo did NOT react to Testing Arena scenario (only found: {mentions})")
            logger.info(f"Response: {response4[:300]}")
    else:
        logger.warning("❌ Room 3 scenario not shown properly")

    logger.info("\n" + "=" * 80)
    logger.info("TEST COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_scenario_context())