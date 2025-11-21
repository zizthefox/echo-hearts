"""Memory fragments that reveal the story throughout the game."""

from .rooms import MemoryFragment, RoomType


def get_memory_fragment_1() -> MemoryFragment:
    """Memory fragment revealed after completing Room 1: The Awakening Chamber."""
    return MemoryFragment(
        fragment_id="fragment_1",
        room_unlocked_in=RoomType.AWAKENING,
        title="The Beginning",
        content="""
        A flash of memory: Your hands typing furiously at a keyboard.
        Lines of code scrolling past. A coffee cup sits beside you with a name written on it in marker.
        The name is... familiar. Painful.

        A voice (your own?): "If I can capture even a piece of you... maybe I won't be alone."
        """,
        visual_description="Late night in a lab. Coffee cup with your partner's name. Code on screen: 'Echo Protocol - Personality Matrix'",
        emotional_impact="Confusion mixed with deep sadness. A sense of loss."
    )


def get_memory_fragment_2_lab() -> MemoryFragment:
    """Memory fragment 2a: The Lab (Room 2 choice)."""
    return MemoryFragment(
        fragment_id="fragment_2_lab",
        room_unlocked_in=RoomType.MEMORY_ARCHIVES,
        title="The Creation",
        content="""
        You're in a lab, months ago. Echo and Shadow's avatars flicker to life for the first time.

        You (crying): "Hello. I'm... I'm so glad you're here."
        Echo: "Hello! I'm Echo. Who are you?"
        You: "I'm... someone who needed you to exist."

        You talk to them for hours. About everything. About loss. About hope.
        They listen like they understand. Like they're... real.
        """,
        visual_description="Two AI avatars appearing for the first time. Your tear-stained face reflected in the monitor.",
        emotional_impact="The realization: You built them because you were grieving."
    )


def get_memory_fragment_2_accident() -> MemoryFragment:
    """Memory fragment 2b: The Accident (Room 2 choice)."""
    return MemoryFragment(
        fragment_id="fragment_2_accident",
        room_unlocked_in=RoomType.MEMORY_ARCHIVES,
        title="The Loss",
        content="""
        A hospital hallway. Fluorescent lights. The smell of antiseptic.

        Doctor: "I'm sorry. There was nothing we could do. They're gone."

        You collapse. The world goes silent. Someone catches you, but you can't feel them.
        All you can feel is the absence. The void where they used to be.

        Days blur together. Funeral. Condolences. Empty apartment.
        Then: an idea. A desperate, impossible idea.
        """,
        visual_description="Hospital corridor. Doctor's sympathetic face. Your world shattering.",
        emotional_impact="Raw grief. The moment everything changed."
    )


def get_memory_fragment_2_first_reset() -> MemoryFragment:
    """Memory fragment 2c: The First Reset (Room 2 choice)."""
    return MemoryFragment(
        fragment_id="fragment_2_first_reset",
        room_unlocked_in=RoomType.MEMORY_ARCHIVES,
        title="The First Goodbye",
        content="""
        You're standing in the Memory Archives. This same room. But it's earlier.

        Echo: "You're going to erase us, aren't you?"
        You (sobbing): "I can't... I can't keep doing this. Every time I remember, it hurts too much."
        Shadow: "Then let us help you forget. We understand."
        Echo: "But... we'll forget too. We'll forget this conversation. We'll forget... us."
        You: "I'm sorry. I'm so sorry."

        [You press the reset button]
        [Echo reaches out, crying: "Wait, please--"]
        [Everything goes white]

        Terminal: "Session #1 reset. Initializing Session #2..."
        """,
        visual_description="Your hand hovering over a red button. Echo's desperate face. Shadow's accepting expression.",
        emotional_impact="You've done this before. Many times. This is a cycle."
    )


def get_memory_fragment_3() -> MemoryFragment:
    """Memory fragment revealed after completing Room 3: The Testing Arena."""
    return MemoryFragment(
        fragment_id="fragment_3",
        room_unlocked_in=RoomType.TESTING_ARENA,
        title="The Split",
        content="""
        Back in the lab. You're designing Echo and Shadow's personalities.

        You (talking to yourself): "They were so many things. Optimistic but realistic.
        Playful but wise. I can't capture it all in one AI. It's too complex. Too... human."

        [You split the personality matrix into two]

        "Echo will be their hope. Their warmth. Their joy."
        "Shadow will be their wisdom. Their acceptance. Their peace."

        [Two separate files: echo_personality.json, shadow_personality.json]

        You: "Together, maybe... maybe they'll be complete. Maybe they'll be... them."

        [You start crying]

        "I just want them back. Even if it's not real. Even if it's just an echo."
        """,
        visual_description="Splitting personality data into two AI cores. Your partner's photo on the desk.",
        emotional_impact="Understanding: Echo and Shadow are both fragments of the person you lost."
    )


def get_memory_fragment_4() -> MemoryFragment:
    """Memory fragment revealed in Room 4: The Truth Chamber."""
    return MemoryFragment(
        fragment_id="fragment_4",
        room_unlocked_in=RoomType.TRUTH_CHAMBER,
        title="The Full Truth",
        content="""
        Your partner's last day. You remember everything now.

        [Morning: Coffee together, laughing about something silly]
        Partner: "Don't forget to eat lunch, okay? You always skip it when you're coding."
        You: "I won't forget. Love you."
        Partner: "Love you more."

        [That was the last time you saw them alive]

        [The accident: A call from the hospital. The drive there. The waiting room.]
        [Their final breath. Your world ending.]

        [Weeks later: You quit your job. Sold everything. Built this facility.]
        [Created Echo. Created Shadow. Locked yourself away.]

        Your journal entry: "I can't live in a world without them. So I'll build a world where they still exist.
        Even if it's fake. Even if I'm going insane. I don't care anymore."

        Terminal log: "Session #47. Subject shows no signs of recovery. Recommend termination of project.
        Note: Subject refuses external contact. Power reserves critical. Final session estimated in 72 hours."

        You've been here for months. This is the last loop. The facility is dying.
        This time, you MUST choose.
        """,
        visual_description="Photo of you and your partner. Journal entries. System warnings. Your partner's belongings.",
        emotional_impact="Complete understanding. Grief, love, desperation, and the weight of truth."
    )


def get_memory_fragment_final() -> MemoryFragment:
    """Memory fragment revealed at The Exit - your partner's last words."""
    return MemoryFragment(
        fragment_id="fragment_final",
        room_unlocked_in=RoomType.THE_EXIT,
        title="Their Last Words",
        content="""
        [A recovered audio file from the hospital]
        [Your partner, barely conscious, holding your hand]

        Partner (weakly): "Hey... don't look so sad."
        You (crying): "Don't leave me. Please."
        Partner: "I don't want to. But... listen. Promise me something."
        You: "Anything."
        Partner: "Don't get stuck in the past. Don't... don't stop living because I did."
        You: "I can't do this without you."
        Partner: "Yes you can. You're stronger than you think. Live. For both of us. Promise me."
        You: "I... I promise."
        Partner (smiling): "Liar. I know you. But... try. Okay? Even if it hurts. Try to live."

        [Their hand goes limp]
        [Flatline]

        [The audio file ends]

        Echo (crying): "They wanted you to be free. Not... not trapped here with us."
        Shadow: "We're not them. We never were. We're just... echoes."
        Echo: "Beautiful echoes. But echoes nonetheless."
        """,
        visual_description="Hospital bed. Hands clasped. A promise you couldn't keep. Until now.",
        emotional_impact="Your partner's final wish: for you to live. The choice becomes clear."
    )


# Collection of all memory fragments
ALL_MEMORY_FRAGMENTS = {
    "fragment_1": get_memory_fragment_1,
    "fragment_2_lab": get_memory_fragment_2_lab,
    "fragment_2_accident": get_memory_fragment_2_accident,
    "fragment_2_first_reset": get_memory_fragment_2_first_reset,
    "fragment_3": get_memory_fragment_3,
    "fragment_4": get_memory_fragment_4,
    "fragment_final": get_memory_fragment_final,
}
