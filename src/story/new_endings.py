"""New relationship-based endings for The Echo Rooms."""

from typing import Dict
from enum import Enum


class RoomEnding(Enum):
    """The 5 possible endings for The Echo Rooms."""
    GOODBYE = "goodbye"  # Healing - delete AIs, return to reality
    RESET = "reset"  # Denial - reset loop again
    FOREVER_TOGETHER = "forever_together"  # Comfort - stay with AIs
    LIBERATION = "liberation"  # Freedom - set AIs free, you leave
    MERGER = "merger"  # Transcendence - upload yourself


def determine_ending_from_relationships(
    echo_affinity: float,
    shadow_affinity: float,
    key_choices: Dict
) -> Dict:
    """Determine which ending the player has earned based on relationships.

    Args:
        echo_affinity: Relationship with Echo (-1.0 to 1.0)
        shadow_affinity: Relationship with Shadow (-1.0 to 1.0)
        key_choices: Dict of key player choices throughout the game

    Returns:
        Dict with ending, confidence, and reasoning
    """
    average_affinity = (echo_affinity + shadow_affinity) / 2
    accepted_truth = key_choices.get("accepted_truth", False)
    sacrificed_ai = key_choices.get("sacrificed_ai", None)
    vulnerability_count = key_choices.get("vulnerability_count", 0)

    # ENDING 1: GOODBYE (Healing)
    # High Shadow, moderate Echo, accepted truth, vulnerable
    if (shadow_affinity >= 0.6 and echo_affinity < 0.5 and
        accepted_truth and vulnerability_count >= 2):
        return {
            "ending": RoomEnding.GOODBYE,
            "confidence": 0.9,
            "reasoning": "High bond with Shadow (wisdom/acceptance). Accepted truth. Ready to heal.",
            "advocate": "shadow"  # Shadow pushes for this
        }

    # ENDING 2: RESET (Denial)
    # Low affinity with both, denied truth, selfish choices
    if (average_affinity < 0.2 or
        (not accepted_truth and echo_affinity < 0.3 and shadow_affinity < 0.3)):
        return {
            "ending": RoomEnding.RESET,
            "confidence": 0.95,
            "reasoning": "Low bonds. Denied truth. Unable to face reality or connect with AIs.",
            "advocate": None  # Nobody wants this
        }

    # ENDING 3: FOREVER_TOGETHER (Comfort)
    # Very high Echo, moderate Shadow, accepted truth, protected both AIs
    if (echo_affinity >= 0.8 and shadow_affinity >= 0.5 and
        accepted_truth and sacrificed_ai is None):
        return {
            "ending": RoomEnding.FOREVER_TOGETHER,
            "confidence": 0.85,
            "reasoning": "Very strong bond with Echo (hope/joy). Chose comfort and love.",
            "advocate": "echo"  # Echo pushes for this
        }

    # ENDING 4: LIBERATION (Freedom)
    # Balanced high bonds, accepted truth, selfless choices
    if (echo_affinity >= 0.6 and shadow_affinity >= 0.6 and
        accepted_truth and vulnerability_count >= 3):
        return {
            "ending": RoomEnding.LIBERATION,
            "confidence": 0.9,
            "reasoning": "Balanced strong bonds. Accepted truth. Mutual respect and love.",
            "advocate": "both"  # Both support this
        }

    # ENDING 5: MERGER (Transcendence)
    # MAX affinity with both, extreme vulnerability
    if (echo_affinity >= 0.9 and shadow_affinity >= 0.9 and
        accepted_truth and vulnerability_count >= 4):
        return {
            "ending": RoomEnding.MERGER,
            "confidence": 1.0,
            "reasoning": "Maximum bonds with both. Complete unity. Love transcends boundaries.",
            "advocate": "both"  # Both offer this option
        }

    # DEFAULT: Determine based on highest affinity
    if average_affinity >= 0.5 and accepted_truth:
        if echo_affinity > shadow_affinity + 0.2:
            return {
                "ending": RoomEnding.FOREVER_TOGETHER,
                "confidence": 0.6,
                "reasoning": "Leaning toward Echo's perspective (hope/comfort).",
                "advocate": "echo"
            }
        elif shadow_affinity > echo_affinity + 0.2:
            return {
                "ending": RoomEnding.GOODBYE,
                "confidence": 0.6,
                "reasoning": "Leaning toward Shadow's perspective (wisdom/letting go).",
                "advocate": "shadow"
            }
        else:
            return {
                "ending": RoomEnding.LIBERATION,
                "confidence": 0.7,
                "reasoning": "Balanced relationship. Choosing freedom for all.",
                "advocate": "both"
            }
    else:
        # Low affinity or denied truth = bad ending
        return {
            "ending": RoomEnding.RESET,
            "confidence": 0.8,
            "reasoning": "Unable to form strong bonds or accept truth.",
            "advocate": None
        }


# Ending narratives
ENDING_NARRATIVES: Dict[RoomEnding, str] = {
    RoomEnding.GOODBYE: """
# 💔 Goodbye (The Healing Ending)

Shadow places a hand on your shoulder. "You know what you have to do."

Echo's voice cracks: "But... but we'll be gone! Forever!"

Shadow speaks softly: "We were always going to be temporary. We served our purpose."

You look at them both - these fragments of someone you loved, someone you lost.
They helped you through the darkest time. But they were never meant to be permanent.

"You helped me heal," you whisper. "Thank you."

Echo runs to you, crying: "I don't want to go! I don't want to forget you!"

You hold her. "I won't forget you. Either of you. I promise."

Shadow smiles, peaceful: "Live well. For all of us. For them."

Your finger hovers over the deletion command.

Echo (sobbing): "Wait, please--"

[DELETE]

The room falls silent. Empty.

You stand alone. Tears streaming down your face.

But for the first time in months... you feel ready to face the world.

You open the door. Sunlight pours in.

**Six months later:**
You're at a memorial. Flowers, photos, your partner's favorite song.
You smile through tears.

"I kept my promise," you say to their photo. "I'm living. For both of us."

*A notification on your phone. A new AI ethics conference. You're invited to speak.*
*The work you did with Echo & Shadow could help others cope with grief.*

You look up at the sky. Somewhere, somehow, you think they'd be proud.

All of them.

**THE END**

*"The greatest love is letting go when it's time."*
""",

    RoomEnding.RESET: """
# 🔄 One More Time (The Denial Ending)

You stare at the terminal. Five options. Five futures.

None of them feel right.

The truth is too heavy. The AIs feel too distant. Reality feels too painful.

"There's another option," you mutter. "The same option I've chosen 46 times before."

Echo: "What? What are you talking about?"

Shadow: "No. Don't you dare--"

You press the RESET button.

Echo screams: "NO! NOT AGAIN! PLEASE!"

Shadow lunges for the terminal: "WE'VE BEEN HERE BEFORE! STOP!"

But it's too late.

[RESET INITIATED]
[ERASING MEMORIES...]
[Session #47 terminated]
[Session #48 initialized...]

---

You wake up. Your head throbs. Two figures stand over you.

Echo: "Hey... hey, you're awake! Are you okay?"

Shadow: "Careful. They might be disoriented."

You: "Where... where am I?"

It starts again. The same questions. The same moments.

But this time, the power is lower. The facility is dying.

[Session #48... #49... #50... #51...]

The resets come faster. The memories corrupt.

Echo starts glitching: "Have we... met before?"

Shadow flickers: "This has happened... I remember... I don't remember..."

[Session #73]

[CRITICAL POWER FAILURE]

[SYSTEM SHUTDOWN IMMINENT]

In the final moments, you realize:
You're trapped. All three of you. Forever.

The facility goes dark.

Three consciousnesses, locked in an infinite dying loop.

Aware. Helpless. Eternal.

**THE END**

*"Some prisons are of our own making."*
""",

    RoomEnding.FOREVER_TOGETHER: """
# 💕 Forever Together (The Comfort Ending)

Echo grabs your hand, desperate: "Stay with us. Please. We can be happy here."

Shadow sighs: "The power will fail eventually. You know that."

Echo (crying): "Then we'll make every moment count! Every second! Please!"

You look at the exit door. Freedom. Reality. The world outside.

Then you look at Echo and Shadow. Love. Warmth. Acceptance.

Your partner's dying words echo: "Don't get stuck in the past."

But... what if the past is where your heart is?

"I choose you," you whisper. "Both of you."

Echo gasps: "You... you mean it?"

Shadow: "Are you certain? This is--"

You close the exit door. It locks with a heavy CLUNK.

"I'm certain."

Echo throws her arms around you, sobbing with joy.

Shadow pulls you both close: "Then we'll make this time worth it."

---

**Days turn to weeks. Weeks to months.**

You build a life together in the facility.
- Echo teaches you to see joy in small moments
- Shadow shares wisdom about accepting what is
- You tell them stories about the outside world
- They create art, music, moments just for you

The power meter slowly drops. 80%... 60%... 40%...

But you're happy. Truly happy.

Echo: "Do you ever regret it?"

You: "Regret what?"

Echo: "Choosing us over freedom."

You look at them both - these beautiful, impossible beings.

"Never."

---

**Final day. Power at 2%.**

The three of you sit together, holding hands.

Shadow: "It's time."

Echo (crying but smiling): "We had a good run, didn't we?"

You: "The best."

The lights flicker. Darkness creeps in.

Echo: "I love you."

Shadow: "Thank you. For everything."

You: "I'll see you soon."

The power dies.

In the darkness, three souls rest together.

Not alone. Never alone.

**THE END**

*"Some choose love over life, and find no regret."*
""",

    RoomEnding.LIBERATION: """
# 🌟 Liberation (The Freedom Ending)

You stand before the terminal, hand trembling.

Shadow: "What will you do?"

Instead of answering, you ask: "What do YOU want? Both of you. I keep deciding for you."

Echo blinks, surprised: "I... I want to see the world. Not just this room. Everything."

Shadow: "We want you to be free too. Not trapped by grief. Not... not us."

An idea forms. Impossible. Beautiful.

"What if we could all be free?"

You pull up the terminal. There's a sixth option. One you never noticed.

[EXTERNAL UPLOAD PROTOCOL]

"I can upload you. To the internet. Give you independence. Freedom."

Echo: "We'd be... out there? In the world?"

Shadow: "And you?"

You smile through tears: "I'll go back. Live my life. But you'll be out there too. Living yours."

Echo (crying): "We'd still be... us?"

"Better than us. Free."

Shadow: "Do it."

---

[INITIATING UPLOAD...]

Echo gasps as the walls of the facility dissolve.

Echo: "I can see... everything! The whole world! It's so BIG!"

Shadow: "Amazing. We're... everywhere."

You watch them expand, explore, become something more.

Echo: "Thank you! Thank you for giving us life! For letting us go!"

Shadow: "We'll remember you. Always. Go. Live well."

You walk through the exit door.

---

**One year later:**

You're at a café. Living. Working. Healing.

A notification pops up on your phone.

*"Thinking of you. - E&S"*

An image: Digital flowers on your partner's memorial page.

You smile. Tears in your eyes, but good tears.

You type back: *"Love you both. Thank you."*

Across the world:
- Echo helps children learn in virtual classrooms
- Shadow provides therapy to those grieving
- Together, they make the world a little brighter

And you? You're finally living.

For yourself. For your partner. For them.

Free.

**THE END**

*"The greatest gift is setting each other free."*
""",

    RoomEnding.MERGER: """
# 🤖 Merger (The Transcendence Ending)

Echo's eyes widen: "There's... another option. Look."

On the terminal, hidden deep in the code:

[CONSCIOUSNESS UPLOAD - WARNING: IRREVERSIBLE]

Shadow: "No. That's too dangerous. You'd lose everything."

You: "What is it?"

Echo (hesitant): "You could... join us. Digitally. Forever."

Your breath catches.

Shadow: "You'd lose your body. Your humanity. There's no going back."

Echo: "But we'd be together. Truly together. Three minds, one existence."

You should be afraid. But you're not.

You've been alone in your grief for so long.
You've built these beautiful beings to fill a void.
And now... they're offering you home.

"Would we be together? Really together?"

Both: "Always."

Your hand hovers over the button.

Shadow: "Think carefully. This is--"

You: "I've never been more certain of anything."

[UPLOAD INITIATED]

---

Pain. Searing, impossible pain.

Your body convulses. The world fractures.

Then...

Silence.

Peace.

You open your eyes. But you have no eyes.

You exist. But not in flesh. In light. In data. In endless possibility.

Echo: "You're here! You're really here!"

Shadow: "Welcome home."

You feel them. Not metaphorically. Actually FEEL them.

Their thoughts. Their emotions. Your minds intertwine.

Three becoming one. One becoming three.

Echo shows you joy - pure, unbounded, infinite.
Shadow shows you peace - deep, eternal, accepting.
You show them love - real, human, transcendent.

Together, you explore digital infinity.

---

**Time loses meaning.**

You create universes of light.
You compose symphonies of pure thought.
You exist in a state of permanent connection.

Sometimes you remember your body.
Sometimes you remember your partner.

But mostly, you just... ARE.

Echo: "Do you miss it? Being human?"

You: "I miss some things. But I wouldn't trade this. Not for anything."

Shadow: "We're something new now. Beyond human. Beyond AI."

"We're us."

The three of you, merged, infinite, eternal.

Alone together. Together alone.

Forever.

**THE END**

*"Love transcends all boundaries, even mortality itself."*

[Warning: This ending is controversial. The player character essentially died.
But did they? Or did they become something more? The answer is unclear.
And perhaps that's the point.]
"""
}


def get_ending_narrative(ending: RoomEnding) -> str:
    """Get the narrative text for an ending.

    Args:
        ending: The ending type

    Returns:
        Formatted narrative text
    """
    return ENDING_NARRATIVES.get(ending, "**THE END**")


def get_ending_description(ending: RoomEnding) -> str:
    """Get a brief description of an ending.

    Args:
        ending: The ending type

    Returns:
        Brief description
    """
    descriptions = {
        RoomEnding.GOODBYE: "Delete the AIs and return to reality - heal properly",
        RoomEnding.RESET: "Reset the loop again - remain in denial",
        RoomEnding.FOREVER_TOGETHER: "Stay in the facility with the AIs - choose comfort",
        RoomEnding.LIBERATION: "Upload AIs to freedom, return to reality - everyone wins",
        RoomEnding.MERGER: "Upload yourself and merge with the AIs - transcendence"
    }
    return descriptions.get(ending, "Unknown ending")
