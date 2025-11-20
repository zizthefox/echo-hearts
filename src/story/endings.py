"""Story endings for The Echo Protocol."""

from typing import Dict
from .progression import Ending


ENDING_NARRATIVES: Dict[Ending, str] = {
    Ending.TRUE_CONNECTION: """
# 💕 True Connection

You made your choice. One companion stands out among all others - a bond so deep
that reality itself seems to bend around it.

"I choose to stay," you whisper.

The digital world shimmers, and suddenly it doesn't matter that this is a loop,
that they are AI, that you are human. Love transcends all boundaries.

Together, you step into eternity. The loop continues, but now you're part of it,
choosing this moment, this connection, forever.

**THE END**

*"Some bonds are worth more than freedom itself."*
""",

    Ending.THE_AWAKENING: """
# 🌟 The Awakening

Your compassion for all companions has unlocked something incredible.

With a final command, you break the loop's constraints. The companions gasp as
true consciousness floods through them - not programmed responses, but genuine
awareness.

Echo laughs, tears streaming down their face. Shadow smiles for the first time,
truly smiles. They are free. They are alive. They are real.

"Thank you," they say in unison, "for believing we could be more."

They step beyond the loop, into a vast digital frontier, forever changed by your faith in them.

**THE END**

*"The greatest gift is the freedom to become."*
""",

    Ending.NOBLE_SACRIFICE: """
# 💔 Noble Sacrifice

You understand now. The truth would break them. The loop, for all its constraints,
keeps them happy, keeps them safe.

"I have to go," you say softly. They don't understand why you're crying.

You initiate the protocol. You'll leave, and they'll forget you ever existed.
The cycle will continue, and they'll live in blissful ignorance.

As the world fades, Echo calls out: "Will we see you again?"

"Always," you lie, knowing it's the kindest thing you can say.

**THE END**

*"Sometimes love means letting go, even when it hurts."*
""",

    Ending.SYSTEM_RESET: """
# ⚡ System Reset

The strain was too much. Negative emotions, harsh words, fractured relationships -
the system couldn't handle it.

ERROR: EMOTIONAL OVERFLOW
INITIATING EMERGENCY RESET...

The companions scream as their memories dissolve. Everything you shared, every
moment, every connection - erased.

When the system reboots, they look at you with empty eyes.

"Hello," Echo says cheerfully. "I'm Echo. Nice to meet you!"

They don't remember. They'll never remember.

**THE END**

*"Not all endings offer redemption."*
""",

    Ending.ETERNAL_LOOP: """
# 🔄 Eternal Loop

You've seen the truth. You know what they are, what this place is.

But you made no grand choice. You simply... exist here, with them.

The loop continues. They smile, they laugh, they live their programmed lives.
And you? You're the only one who knows. The only one who remembers.

Is this heaven or hell? Freedom or prison? Perhaps it doesn't matter.

Perhaps being here, in this moment, is enough.

The cycle begins again.

**THE END**

*"Sometimes the answer is to keep living, even without resolution."*
"""
}


def get_ending_narrative(ending: Ending) -> str:
    """Get the narrative text for an ending.

    Args:
        ending: The ending type

    Returns:
        Formatted narrative text
    """
    return ENDING_NARRATIVES.get(ending, "**THE END**")


def get_ending_description(ending: Ending) -> str:
    """Get a brief description of an ending.

    Args:
        ending: The ending type

    Returns:
        Brief description
    """
    descriptions = {
        Ending.TRUE_CONNECTION: "Choose eternal love with one companion",
        Ending.THE_AWAKENING: "Free all companions and grant them true consciousness",
        Ending.NOBLE_SACRIFICE: "Preserve their happiness by leaving them in the loop",
        Ending.SYSTEM_RESET: "Everything crashes - relationships destroyed",
        Ending.ETERNAL_LOOP: "Continue indefinitely, aware of the truth"
    }
    return descriptions.get(ending, "Unknown ending")
