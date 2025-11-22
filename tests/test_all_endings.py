"""Test all 5 affinity-based endings are reachable with single companion (Echo only)."""

import sys
import os
import io

# Fix UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.story.new_endings import (
    RoomEnding,
    determine_ending_from_relationships
)


def test_all_endings():
    """Test that all 5 endings can be reached with single companion (Echo only)."""

    print("=" * 80)
    print("TESTING ALL 5 ENDINGS (SINGLE COMPANION: ECHO)")
    print("=" * 80)

    # TEST 1: MERGER (Transcendence) - Highest affinity + vulnerability
    print("\n--- TEST 1: MERGER (Transcendence) ---")
    result = determine_ending_from_relationships(
        echo_affinity=0.8,       # High Echo affinity
        key_choices={
            "accepted_truth": True,
            "vulnerability_count": 3,  # High vulnerability
            "sacrificed_ai": None
        }
    )

    if result["ending"] == RoomEnding.MERGER:
        print(f"✅ PASS: MERGER ending reached")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Advocate: {result['advocate']}")
    else:
        print(f"❌ FAIL: Expected MERGER, got {result['ending'].value}")

    # TEST 2: FOREVER_TOGETHER (Comfort) - High affinity, low vulnerability
    print("\n--- TEST 2: FOREVER_TOGETHER (Comfort) ---")
    result = determine_ending_from_relationships(
        echo_affinity=0.7,       # High Echo affinity
        key_choices={
            "accepted_truth": True,
            "vulnerability_count": 2,  # Low vulnerability
            "sacrificed_ai": None
        }
    )

    if result["ending"] == RoomEnding.FOREVER_TOGETHER:
        print(f"✅ PASS: FOREVER_TOGETHER ending reached")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Advocate: {result['advocate']}")
    else:
        print(f"❌ FAIL: Expected FOREVER_TOGETHER, got {result['ending'].value}")

    # TEST 3: LIBERATION (Freedom) - Moderate affinity, selfless
    print("\n--- TEST 3: LIBERATION (Freedom) ---")
    result = determine_ending_from_relationships(
        echo_affinity=0.5,       # Moderate Echo affinity
        key_choices={
            "accepted_truth": True,
            "vulnerability_count": 2,  # Selfless choices
            "sacrificed_ai": None
        }
    )

    if result["ending"] == RoomEnding.LIBERATION:
        print(f"✅ PASS: LIBERATION ending reached")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Advocate: {result['advocate']}")
    else:
        print(f"❌ FAIL: Expected LIBERATION, got {result['ending'].value}")

    # TEST 4: GOODBYE (Healing) - Lower affinity, accepted truth
    print("\n--- TEST 4: GOODBYE (Healing) ---")
    result = determine_ending_from_relationships(
        echo_affinity=0.4,       # Lower Echo affinity
        key_choices={
            "accepted_truth": True,
            "vulnerability_count": 1,
            "sacrificed_ai": None
        }
    )

    if result["ending"] == RoomEnding.GOODBYE:
        print(f"✅ PASS: GOODBYE ending reached")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Advocate: {result['advocate']}")
    else:
        print(f"❌ FAIL: Expected GOODBYE, got {result['ending'].value}")

    # TEST 5: RESET (Denial) - Low affinity or denied truth
    print("\n--- TEST 5: RESET (Denial) ---")
    result = determine_ending_from_relationships(
        echo_affinity=0.2,       # Low Echo affinity
        key_choices={
            "accepted_truth": False,  # Denied truth
            "vulnerability_count": 0,
            "sacrificed_ai": None
        }
    )

    if result["ending"] == RoomEnding.RESET:
        print(f"✅ PASS: RESET ending reached")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Advocate: {result['advocate']}")
    else:
        print(f"❌ FAIL: Expected RESET, got {result['ending'].value}")

    # TEST 6: Edge case - Denied truth forces RESET regardless of affinity
    print("\n--- TEST 6: Edge Case - Denied Truth Forces RESET ---")
    result = determine_ending_from_relationships(
        echo_affinity=0.9,       # High affinity
        key_choices={
            "accepted_truth": False,  # But denied truth
            "vulnerability_count": 5,
            "sacrificed_ai": None
        }
    )

    if result["ending"] == RoomEnding.RESET:
        print(f"✅ PASS: Denied truth correctly forces RESET ending")
        print(f"   Reasoning: {result['reasoning']}")
    else:
        print(f"❌ FAIL: Expected RESET (denied truth), got {result['ending'].value}")

    print("\n" + "=" * 80)
    print("ALL ENDING TESTS COMPLETE (SINGLE COMPANION)")
    print("=" * 80)


if __name__ == "__main__":
    test_all_endings()