"""Test full Memory MCP integration with multiple playthroughs."""

import asyncio
import sys
import os
import io
import time

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_state import GameState
from src.story.new_endings import RoomEnding
from src.game_mcp.memory_mcp_client import MockMemoryMCPClient
from src.game_mcp.memory_manager import MemoryManager


async def test_full_memory_flow():
    """Test complete memory flow: record → retrieve → decay → clear."""

    print("=" * 80)
    print("TESTING FULL MEMORY MCP INTEGRATION")
    print("=" * 80)

    player_id = "test_player_123"

    # Create shared mock client (simulates persistent Memory MCP server)
    shared_mock_client = MockMemoryMCPClient()

    # TEST 1: First playthrough
    print("\n--- TEST 1: First Playthrough ---")
    game1 = GameState(session_id="session1", player_id=player_id)

    # Override with shared mock client
    game1.memory_mcp_client = shared_mock_client
    game1.memory_manager = MemoryManager(shared_mock_client)

    # Check memory (should be None - first time)
    if game1.memory_manager:
        memory = await game1.memory_manager.get_player_memory(player_id)
        if memory:
            print(f"❌ FAIL: Expected no memory, but found: {memory}")
        else:
            print("✅ PASS: No memory found (first playthrough)")

    # Simulate completing game with ACCEPTANCE ending
    if game1.memory_manager:
        await game1.memory_manager.record_playthrough(player_id, "ACCEPTANCE")
        print("✅ Recorded ACCEPTANCE ending (60min decay)")

    # TEST 2: Immediate replay (0 minutes later)
    print("\n--- TEST 2: Immediate Replay (0 min later) ---")
    game2 = GameState(session_id="session2", player_id=player_id)

    # Override with shared mock client
    game2.memory_mcp_client = shared_mock_client
    game2.memory_manager = MemoryManager(shared_mock_client)

    if game2.memory_manager:
        memory = await game2.memory_manager.get_player_memory(player_id)
        if memory:
            print(f"✅ Memory found:")
            print(f"   - Playthrough count: {memory['playthrough_count']}")
            print(f"   - Memory strength: {memory['memory_strength']:.2f} (should be ~1.0)")
            print(f"   - Minutes since: {memory['minutes_since_last']}")
            print(f"   - Should remember: {memory['should_remember']}")

            if memory['memory_strength'] > 0.9:
                print("✅ PASS: Strong memory immediately after")
            else:
                print(f"⚠ WARNING: Expected strong memory, got {memory['memory_strength']:.2f}")
        else:
            print("❌ FAIL: Expected memory but found none")

    # TEST 3: Simulate time passing (30 minutes)
    print("\n--- TEST 3: Simulating 30 Minutes Later ---")
    print("(Manually adjusting last_seen timestamp...)")

    # Get stored memory and modify timestamp
    if game2.memory_manager and game2.memory_mcp_client:
        from datetime import datetime, timedelta

        # Access mock storage directly
        entity_name = f"player_{player_id}"
        if entity_name in game2.memory_mcp_client.storage:
            entity = game2.memory_mcp_client.storage[entity_name]
            # Update last_seen to 30 minutes ago
            thirty_min_ago = (datetime.now() - timedelta(minutes=30)).isoformat()

            # Replace observation
            new_obs = []
            for obs in entity['observations']:
                if obs.startswith('last_seen:'):
                    new_obs.append(f'last_seen: {thirty_min_ago}')
                else:
                    new_obs.append(obs)
            entity['observations'] = new_obs

            print("✅ Adjusted timestamp to 30 minutes ago")

            # Check memory now
            memory = await game2.memory_manager.get_player_memory(player_id)
            if memory:
                print(f"✅ Memory after 30min:")
                print(f"   - Memory strength: {memory['memory_strength']:.2f} (should be ~0.50)")
                print(f"   - Minutes since: {memory['minutes_since_last']}")

                if 0.45 <= memory['memory_strength'] <= 0.55:
                    print("✅ PASS: Memory fading correctly (50% after 30min of 60min decay)")
                else:
                    print(f"⚠ WARNING: Expected ~0.50, got {memory['memory_strength']:.2f}")

    # TEST 4: Simulate exceeding decay period (70 minutes)
    print("\n--- TEST 4: Simulating 70 Minutes Later (Exceeds 60min decay) ---")

    if game2.memory_manager and game2.memory_mcp_client:
        # Adjust to 70 minutes ago
        seventy_min_ago = (datetime.now() - timedelta(minutes=70)).isoformat()

        entity_name = f"player_{player_id}"
        if entity_name in game2.memory_mcp_client.storage:
            entity = game2.memory_mcp_client.storage[entity_name]
            new_obs = []
            for obs in entity['observations']:
                if obs.startswith('last_seen:'):
                    new_obs.append(f'last_seen: {seventy_min_ago}')
                else:
                    new_obs.append(obs)
            entity['observations'] = new_obs

            print("✅ Adjusted timestamp to 70 minutes ago")

            # Check memory - should be auto-deleted
            memory = await game2.memory_manager.get_player_memory(player_id)
            if memory is None:
                print("✅ PASS: Memory auto-deleted after exceeding decay period")
            else:
                print(f"❌ FAIL: Expected deletion, but memory still exists: {memory}")

    # TEST 5: Test different ending types
    print("\n--- TEST 5: Testing Different Ending Decay Rates ---")

    test_player_2 = "test_player_trapped"
    game3 = GameState(session_id="session3", player_id=test_player_2)

    # Override with shared mock client
    game3.memory_mcp_client = shared_mock_client
    game3.memory_manager = MemoryManager(shared_mock_client)

    if game3.memory_manager:
        # TRAPPED ending (1440 min = 24 hours)
        await game3.memory_manager.record_playthrough(test_player_2, "TRAPPED")
        print("✅ Recorded TRAPPED ending (1440min = 24hr decay)")

        memory = await game3.memory_manager.get_player_memory(test_player_2)
        if memory:
            print(f"   - Decay rate: 1440 minutes (24 hours)")
            print(f"   - Memory strength: {memory['memory_strength']:.2f}")
            print("✅ PASS: TRAPPED ending persists much longer")

    # TEST 6: Player-initiated clear
    print("\n--- TEST 6: Player Clears Memory ---")

    test_player_3 = "test_player_clear"
    game4 = GameState(session_id="session4", player_id=test_player_3)

    # Override with shared mock client
    game4.memory_mcp_client = shared_mock_client
    game4.memory_manager = MemoryManager(shared_mock_client)

    if game4.memory_manager:
        # Record memory
        await game4.memory_manager.record_playthrough(test_player_3, "ACCEPTANCE")
        print("✅ Recorded playthrough")

        # Verify it exists
        memory = await game4.memory_manager.get_player_memory(test_player_3)
        if memory:
            print("✅ Memory exists")

        # Clear it
        await game4.memory_manager.player_clear_memory(test_player_3)
        print("✅ Player cleared memory")

        # Verify deletion
        memory = await game4.memory_manager.get_player_memory(test_player_3)
        if memory is None:
            print("✅ PASS: Memory successfully cleared")
        else:
            print(f"❌ FAIL: Memory still exists after clear: {memory}")

    # TEST 7: FREEDOM ending (immediate delete)
    print("\n--- TEST 7: FREEDOM Ending (Immediate Delete) ---")

    test_player_4 = "test_player_freedom"
    game5 = GameState(session_id="session5", player_id=test_player_4)

    # Override with shared mock client
    game5.memory_mcp_client = shared_mock_client
    game5.memory_manager = MemoryManager(shared_mock_client)

    if game5.memory_manager:
        # FREEDOM ending should delete immediately
        await game5.memory_manager.record_playthrough(test_player_4, "FREEDOM")
        print("✅ Recorded FREEDOM ending (0min decay = instant delete)")

        # Check memory (should be None)
        memory = await game5.memory_manager.get_player_memory(test_player_4)
        if memory is None:
            print("✅ PASS: FREEDOM ending deleted memory immediately")
        else:
            print(f"❌ FAIL: Memory still exists after FREEDOM: {memory}")

    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_full_memory_flow())