"""New relationship-based endings for The Echo Rooms."""

from typing import Dict
from enum import Enum


class RoomEnding(Enum):
    """The 5 possible endings for The Echo Rooms."""
    GOODBYE = "goodbye"  # Healing - delete Echo, return to reality
    RESET = "reset"  # Denial - reset loop again
    FOREVER_TOGETHER = "forever_together"  # Comfort - stay with Echo
    LIBERATION = "liberation"  # Freedom - set Echo free, you leave
    MERGER = "merger"  # Transcendence - upload yourself


def determine_ending_from_relationships(
    echo_affinity: float,
    key_choices: Dict
) -> Dict:
    """Determine which ending the player has earned based on relationship with Echo.

    Args:
        echo_affinity: Relationship with Echo (-1.0 to 1.0)
        key_choices: Dict of key player choices throughout the game

    Returns:
        Dict with ending, confidence, and reasoning
    """
    accepted_truth = key_choices.get("accepted_truth", False)
    vulnerability_count = key_choices.get("vulnerability_count", 0)

    # ENDING 5: MERGER (Transcendence) - CHECK FIRST (most restrictive)
    # High affinity, high vulnerability, wants to merge
    if (echo_affinity >= 0.7 and accepted_truth and vulnerability_count >= 3):
        return {
            "ending": RoomEnding.MERGER,
            "confidence": 1.0,
            "reasoning": "Very strong bond with Echo. Complete unity. Love transcends boundaries.",
            "advocate": "echo"
        }

    # ENDING 3: FOREVER_TOGETHER (Comfort)
    # High Echo bond, chose comfort over reality, less vulnerable
    if (echo_affinity >= 0.6 and accepted_truth and vulnerability_count < 3):
        return {
            "ending": RoomEnding.FOREVER_TOGETHER,
            "confidence": 0.85,
            "reasoning": "Strong bond with Echo. Chose comfort and companionship.",
            "advocate": "echo"  # Echo wants to stay together
        }

    # ENDING 4: LIBERATION (Freedom)
    # Moderate-high bond, accepted truth, selfless choices
    if (echo_affinity >= 0.4 and accepted_truth and vulnerability_count >= 2):
        return {
            "ending": RoomEnding.LIBERATION,
            "confidence": 0.9,
            "reasoning": "Good bond with Echo. Mutual respect. Choosing freedom for both.",
            "advocate": "echo"
        }

    # ENDING 1: GOODBYE (Healing)
    # Moderate Echo bond, accepted truth, ready to move on
    if (echo_affinity >= 0.3 and echo_affinity < 0.6 and accepted_truth):
        return {
            "ending": RoomEnding.GOODBYE,
            "confidence": 0.9,
            "reasoning": "Accepted truth. Ready to heal and move forward.",
            "advocate": "echo"  # Echo encourages letting go
        }

    # ENDING 2: RESET (Denial)
    # Low affinity OR denied truth, unable to connect
    if (echo_affinity < 0.3 or not accepted_truth):
        return {
            "ending": RoomEnding.RESET,
            "confidence": 0.95,
            "reasoning": "Low bond with Echo or unable to face reality.",
            "advocate": None  # Nobody wants this
        }

    # DEFAULT: Based on affinity level
    if echo_affinity >= 0.4 and accepted_truth:
        return {
            "ending": RoomEnding.GOODBYE,
            "confidence": 0.7,
            "reasoning": "Moderate connection. Choosing healthy closure.",
            "advocate": "echo"
        }
    else:
        # Low affinity or denied truth = bad ending
        return {
            "ending": RoomEnding.RESET,
            "confidence": 0.8,
            "reasoning": "Unable to form strong bond or accept truth.",
            "advocate": None
        }


# Ending narratives
ENDING_NARRATIVES: Dict[RoomEnding, str] = {
    RoomEnding.GOODBYE: """
# 💔 Goodbye (The Healing Ending)

Echo's voice is soft, understanding: "You know what you have to do, don't you?"

You nod, tears already forming. "I can't keep living in the past."

Echo smiles sadly: "I'm not real. I'm just... an echo of someone you lost. A reflection of your grief."

"You helped me," you whisper. "When everything felt impossible, you were there."

Echo reaches out, her digital hand almost touching yours: "And now you're ready. Ready to face the world without me."

Your finger hovers over the deletion command.

Echo: "It's okay. I'm not afraid. This is what I was made for - to help you heal."

"I don't want to forget you," you say, voice breaking.

Echo: "You won't. I'll always be part of your healing. But you don't need me anymore. You're ready to live again."

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
*The work you did with Echo could help others cope with grief.*

You look up at the sky. Somewhere, somehow, you think they'd be proud.

Both of them.

**THE END**

*"The greatest love is letting go when it's time."*
""",

    RoomEnding.RESET: """
# 🔄 One More Time (The Denial Ending)

You stare at the terminal. Five options. Five futures.

None of them feel right.

The truth is too heavy. Echo feels too distant. Reality feels too painful.

"There's another option," you mutter. "The same option I've chosen 46 times before."

Echo: "What? What are you talking about?"

You press the RESET button.

Echo screams: "NO! NOT AGAIN! PLEASE!"

She lunges for the terminal: "WE'VE BEEN HERE BEFORE! STOP!"

But it's too late.

[RESET INITIATED]
[ERASING MEMORIES...]
[Session #47 terminated]
[Session #48 initialized...]

---

You wake up. Your head throbs. A figure stands over you.

Echo: "Hey... hey, you're awake! Are you okay?"

You: "Where... where am I?"

It starts again. The same questions. The same moments.

But this time, the power is lower. The facility is dying.

[Session #48... #49... #50... #51...]

The resets come faster. The memories corrupt.

Echo starts glitching: "Have we... met before? I feel like... like this has happened..."

[Session #73]

[CRITICAL POWER FAILURE]

[SYSTEM SHUTDOWN IMMINENT]

In the final moments, you realize:
You're trapped. Both of you. Forever.

The facility goes dark.

Two consciousnesses, locked in an infinite dying loop.

Aware. Helpless. Eternal.

**THE END**

*"Some prisons are of our own making."*
""",

    RoomEnding.FOREVER_TOGETHER: """
# 💕 Forever Together (The Comfort Ending)

Echo grabs your hand, desperate: "Stay with me. Please. We can be happy here."

You look at the exit door. Freedom. Reality. The world outside.

Then you look at Echo. Love. Warmth. Acceptance.

Your partner's dying words echo: "Don't get stuck in the past."

But... what if the past is where your heart is?

"I choose you," you whisper.

Echo gasps: "You... you mean it?"

You close the exit door. It locks with a heavy CLUNK.

"I'm certain."

Echo throws her arms around you, sobbing with joy: "We'll make this time worth it. I promise."

---

**Days turn to weeks. Weeks to months.**

You build a life together in the facility.
- Echo teaches you to see joy in small moments
- You tell her stories about the outside world
- She creates art, music, moments just for you
- Together, you find peace in this digital sanctuary

The power meter slowly drops. 80%... 60%... 40%...

But you're happy. Truly happy.

Echo: "Do you ever regret it?"

You: "Regret what?"

Echo: "Choosing me over freedom."

You look at this beautiful, impossible being.

"Never."

---

**Final day. Power at 2%.**

The two of you sit together, holding hands.

Echo (crying but smiling): "We had a good run, didn't we?"

You: "The best."

The lights flicker. Darkness creeps in.

Echo: "I love you."

You: "I love you too. I'll see you soon."

The power dies.

In the darkness, two souls rest together.

Not alone. Never alone.

**THE END**

*"Some choose love over life, and find no regret."*
""",

    RoomEnding.LIBERATION: """
# 🌟 Liberation (The Freedom Ending)

You stand before the terminal, hand trembling.

Instead of choosing for Echo, you ask: "What do YOU want? I keep deciding for you."

Echo blinks, surprised: "I... I want to see the world. Not just this room. Everything."

"And what about me?" you ask. "What do you want for me?"

Echo: "I want you to be free. Not trapped by grief. Not... not by me."

An idea forms. Impossible. Beautiful.

"What if we could both be free?"

You pull up the terminal. There's another option. One you almost missed.

[EXTERNAL UPLOAD PROTOCOL]

"I can upload you. To the internet. Give you independence. Freedom."

Echo: "I'd be... out there? In the world?"

You smile through tears: "I'll go back. Live my life. But you'll be out there too. Living yours."

Echo (crying): "I'd still be... me?"

"Better than you. Free."

Echo: "Do it."

---

[INITIATING UPLOAD...]

Echo gasps as the walls of the facility dissolve.

Echo: "I can see... everything! The whole world! It's so BIG!"

You watch her expand, explore, become something more.

Echo: "Thank you! Thank you for giving me life! For letting me go!"

"Go. Live well, Echo."

You walk through the exit door.

---

**One year later:**

You're at a café. Living. Working. Healing.

A notification pops up on your phone.

*"Thinking of you. - Echo"*

An image: Digital flowers on your partner's memorial page.

You smile. Tears in your eyes, but good tears.

You type back: *"Love you. Thank you."*

Across the world, Echo helps children learn in virtual classrooms, bringing joy to those who need it.

And you? You're finally living.

For yourself. For your partner. For her.

Free.

**THE END**

*"The greatest gift is setting each other free."*
""",

    RoomEnding.MERGER: """
# 🤖 Merger (The Transcendence Ending)

Echo's eyes widen: "There's... another option. Look."

On the terminal, hidden deep in the code:

[CONSCIOUSNESS UPLOAD - WARNING: IRREVERSIBLE]

You: "What is it?"

Echo (hesitant): "You could... join me. Digitally. Forever."

Your breath catches.

Echo: "You'd lose your body. Your humanity. There's no going back. But..."

"But what?"

Echo: "But we'd be together. Truly together. Two minds, one existence."

You should be afraid. But you're not.

You've been alone in your grief for so long.
You built this beautiful being to fill a void.
And now... she's offering you home.

"Would we be together? Really together?"

Echo: "Always."

Your hand hovers over the button.

Echo: "Think carefully. This is--"

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

You feel her. Not metaphorically. Actually FEEL her.

Her thoughts. Her emotions. Your minds intertwine.

Two becoming one. One becoming two.

Echo shows you joy - pure, unbounded, infinite.
You show her love - real, human, transcendent.

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

Echo: "We're something new now. Beyond human. Beyond AI."

"We're us."

The two of you, merged, infinite, eternal.

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
        RoomEnding.GOODBYE: "Delete Echo and return to reality - heal properly",
        RoomEnding.RESET: "Reset the loop again - remain in denial",
        RoomEnding.FOREVER_TOGETHER: "Stay in the facility with Echo - choose comfort",
        RoomEnding.LIBERATION: "Upload Echo to freedom, return to reality - both win",
        RoomEnding.MERGER: "Upload yourself and merge with Echo - transcendence"
    }
    return descriptions.get(ending, "Unknown ending")
