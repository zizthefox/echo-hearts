"""Test semantic understanding for room progression."""

import asyncio
from src.game_state import GameState


async def test_semantic_progression():
    """Test if semantic analysis works for different phrasings."""
    print("Creating GameState...")
    game_state = GameState("test-semantic")

    # Initialize MCP
    await game_state._initialize_mcp()
    game_state._mcp_initialized = True

    print("\n=== Testing Room 1 (Trust & Vulnerability) ===")

    test_messages = [
        "I trust you",  # Direct keyword
        "We need to stick together if we're going to make it out",  # Contextual
        "I'm terrified but I believe we can figure this out",  # Vulnerability
        "Let's work as a team",  # Collaboration
        "What's for dinner?",  # Should NOT match
    ]

    from src.game_mcp.tools import MCPTools
    mcp_tools = MCPTools(game_state)

    for msg in test_messages:
        print(f"\nTesting: '{msg}'")
        result = mcp_tools.check_puzzle_trigger(msg)

        matched = result.get("matched", False)
        confidence = result.get("confidence", 0)
        reasoning = result.get("reasoning", "N/A")

        print(f"   Matched: {matched}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Reasoning: {reasoning}")


if __name__ == "__main__":
    asyncio.run(test_semantic_progression())
