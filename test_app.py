"""Quick test to verify all imports and initialization work."""

import sys

print("Testing imports...")

try:
    from src.utils.config import config
    print("[OK] Config loaded")
    print(f"   OpenAI key present: {'Yes' if config.openai_api_key else 'No'}")

    from src.game_state import GameState
    print("[OK] GameState imported")

    game = GameState("test")
    print(f"[OK] GameState initialized with {len(game.companions)} companions")

    for comp_id, companion in game.companions.items():
        print(f"   - {companion.name} ({comp_id})")

    from src.ui.interface import EchoHeartsUI
    print("[OK] UI imported")

    print("\n[SUCCESS] All components working! Ready to launch.")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
