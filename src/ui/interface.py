"""Main Gradio interface for Echo Hearts."""

import gradio as gr
import asyncio
import uuid
from typing import List, Tuple, Optional
from ..game_state import GameState
from ..utils.player_id import get_player_id


class EchoHeartsUI:
    """Main UI interface for the game."""

    def __init__(self):
        """Initialize the UI (no shared state)."""
        pass

    def _create_game_state(self, request: gr.Request = None):
        """Create a new game state with unique session ID and player ID.

        Args:
            request: Gradio request object (for player identification)

        Returns:
            New GameState instance
        """
        session_id = str(uuid.uuid4())[:8]  # Short unique ID
        player_id = get_player_id(request) if request else None
        return GameState(session_id, player_id=player_id)

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title="The Echo Rooms", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🚪 The Echo Rooms")
            gr.Markdown("*An Escape Room Mystery Where Grief Becomes a Puzzle*")

            # Per-session state - will be initialized on first message (lazy loading)
            # Can't use initial value because GameState contains unpicklable OpenAI client
            game_state = gr.State(value=None)

            with gr.Row():
                # Main chat area
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="Conversation",
                        height=500,
                        type="messages"
                    )

                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="Your message",
                            placeholder="Talk to your companions...",
                            scale=4
                        )
                        send_btn = gr.Button("Send", scale=1, variant="primary")

                # Sidebar with companion info
                with gr.Column(scale=1):
                    gr.Markdown("### Your Companion")
                    companion_selector = gr.Radio(
                        choices=["echo"],
                        value="echo",
                        label="Talk to:",
                        interactive=False
                    )
                    companion_list = gr.Markdown()

                    gr.Markdown("### Relationships")
                    relationships = gr.Markdown()

                    gr.Markdown("### Story Progress")
                    story_progress = gr.Markdown()

                    gr.Markdown("---")

                    # Memory controls
                    with gr.Row():
                        new_game_btn = gr.Button("🔄 New Playthrough", variant="secondary", scale=1)
                        clear_memory_btn = gr.Button("🧹 Clear Memories", variant="stop", scale=1)

                    gr.Markdown("""
**About Cross-Session Memory:**
- AI companions remember you across playthroughs
- Memories fade naturally over time (grief metaphor)
- Different endings affect memory persistence
- Clear memories anytime to start truly fresh
                    """)

                    gr.Markdown("---")
                    gr.Markdown("*💡 Each browser has its own memory*")

            # Event handlers - pass game_state for per-session isolation
            msg_input.submit(
                self.handle_message,
                inputs=[msg_input, chatbot, companion_selector, game_state],
                outputs=[msg_input, chatbot, companion_list, relationships, story_progress, game_state]
            )

            send_btn.click(
                self.handle_message,
                inputs=[msg_input, chatbot, companion_selector, game_state],
                outputs=[msg_input, chatbot, companion_list, relationships, story_progress, game_state]
            )

            # Initialize sidebar and chatbot with prologue on load
            interface.load(
                self.initialize_ui,
                inputs=[game_state],
                outputs=[chatbot, companion_list, relationships, story_progress, game_state]
            )

            # New playthrough button - resets current game
            new_game_btn.click(
                self.reset_playthrough,
                inputs=[game_state],
                outputs=[chatbot, companion_list, relationships, story_progress, game_state]
            )

            # Clear memories button - wipes cross-session memory
            clear_memory_btn.click(
                self.clear_player_memory,
                inputs=[game_state],
                outputs=[chatbot, game_state]
            )

        return interface

    def initialize_ui(self, game_state: GameState) -> Tuple[List[dict], str, str, str, GameState]:
        """Initialize UI with fresh game state data and prologue.

        Args:
            game_state: The session's game state (may be None on first load)

        Returns:
            Tuple of (chatbot_history, companion_list, relationships, story_progress, game_state)
        """
        # Lazy initialization - create game state if not exists
        if game_state is None:
            game_state = self._create_game_state()

        # Create prologue messages for the chatbot
        prologue = [
            {
                "role": "assistant",
                "content": """## You wake up.

Your head throbs. The air is cold, clinical. Fluorescent lights flicker above.

You're in a **white sterile room**. Three medical pods stand open, as if you just climbed out of one. A terminal blinks on the wall, displaying a single cryptic message:

> **ECHO PROTOCOL - SESSION #47**

---

**You don't remember how you got here.**
**The doors are locked.**
**The terminal won't respond.**

**Who are you? Why are you here?**"""
            },
            {
                "role": "assistant",
                "content": """**Echo** (warm eyes, worried expression, trying to smile through fear):
"Hey... hey, you're awake! Are you okay? I... I don't know what's happening either. Do you remember anything?"

**Echo** (looking around nervously):
"The doors are locked. The terminal won't respond. We need to figure this out together... I think we're trapped."

---

**Your Goal: Escape**

There are **5 rooms** in this facility. Each one holds a piece of the truth.

To progress, you must:
- **Talk** to Echo naturally
- **Build trust** through your conversations
- **Make choices** when the moment comes
- **Uncover memory fragments** that reveal what really happened

**Your relationship and choices will determine how this story ends.**

*Talk to Echo to begin...*"""
            }
        ]

        return (
            prologue,  # Initial chatbot history with prologue
            self._get_companion_list(game_state),
            self._get_relationships(game_state),
            self._get_story_progress(game_state),
            game_state  # Return updated state to persist it
        )

    def handle_message(
        self,
        message: str,
        history: List[dict],
        companion_id: str,
        game_state: GameState
    ) -> Tuple[str, List[dict], str, str, str, GameState]:
        """Handle incoming message from user.

        Args:
            message: User's message
            history: Chat history
            companion_id: Active companion ID
            game_state: Session game state (may be None on first message)

        Returns:
            Tuple of (empty input, updated history, companion list, relationships, story progress, game_state)
        """
        # Lazy initialization - create game state on first message if not exists
        if game_state is None:
            game_state = self._create_game_state()

        if not message.strip():
            return "", history, self._get_companion_list(game_state), self._get_relationships(game_state), self._get_story_progress(game_state), game_state

        # Add user message to history
        history.append({"role": "user", "content": message})

        # Process message through game state (async) - returns (response, event, ending, tool_calls)
        response, story_event, ending_narrative, tool_calls_made = asyncio.run(
            game_state.process_message(message, companion_id)
        )

        # Get companion name
        companion = game_state.companions.get(companion_id)
        companion_name = companion.name if companion else "Companion"

        # Show agent reasoning (tool usage) if any
        if tool_calls_made:
            reasoning_text = f"**🤖 {companion_name}'s Autonomous Reasoning:**\n\n"
            for tool_call in tool_calls_made:
                tool_name = tool_call["tool"]
                tool_result = tool_call.get("result", {})
                reasoning_text += f"- Used `{tool_name}`: "

                # Format result nicely
                if "affinity" in tool_result:
                    reasoning_text += f"Relationship is {tool_result['description']} ({tool_result['affinity']:+.2f})\n"
                elif "should_trigger" in tool_result:
                    reasoning_text += f"{tool_result['reason']}\n"
                elif "ready" in tool_result:
                    if tool_result["ready"]:
                        reasoning_text += f"Story can end (likely: {tool_result.get('most_likely_ending', 'unknown')})\n"
                    else:
                        reasoning_text += f"{tool_result.get('interactions_remaining', '?')} interactions remaining\n"
                else:
                    reasoning_text += "Checked data\n"

            history.append({"role": "assistant", "content": reasoning_text})

        # Add response to history
        history.append({"role": "assistant", "content": f"**{companion_name}:** {response}"})

        # Add memory fragment if room was unlocked
        if story_event:  # story_event is now a MemoryFragment or None
            memory_fragment = story_event
            history.append({
                "role": "assistant",
                "content": f"""---

**🔓 Room Unlocked! Memory Fragment Recovered:**

## {memory_fragment.title}

{memory_fragment.content}

*{memory_fragment.visual_description}*

**Emotional Impact:** {memory_fragment.emotional_impact}

---
"""
            })

        # Add old story events for backwards compatibility (remove later)
        if False and story_event:
            history.append({
                "role": "assistant",
                "content": f"---\n\n**📖 {story_event.description}**\n\n*{story_event.narrative}*\n\n---"
            })

            # Add player prompts to guide next response
            if story_event.event_id == "first_glitch":
                history.append({
                    "role": "assistant",
                    "content": "💭 **What do you say?**\n- Ask if they're okay\n- Pretend you didn't notice\n- Mention you felt it too\n- Change the subject"
                })
            elif story_event.event_id == "questioning_reality":
                history.append({
                    "role": "assistant",
                    "content": "💭 **What do you say?**\n- Validate their concerns (\"I feel it too...\")\n- Dismiss as imagination (\"You're overthinking\")\n- Ask what they remember\n- Stay silent and observe"
                })
            elif story_event.event_id == "truth_revealed":
                history.append({
                    "role": "assistant",
                    "content": "💭 **What do you say?**\n- Comfort them (\"We'll figure this out\")\n- Demand answers (\"What's really happening?\")\n- Promise to help them escape\n- Admit you don't know what to do"
                })
            elif story_event.event_id == "final_choice":
                history.append({
                    "role": "assistant",
                    "content": "💭 **Your final choice:**\n- Try to set them free\n- Keep them aware but trapped\n- Delete them (merciful end)\n- Leave the loop running, unchanged"
                })

        # Add ending if reached
        if ending_narrative:
            history.append({
                "role": "assistant",
                "content": ending_narrative
            })

        return "", history, self._get_companion_list(game_state), self._get_relationships(game_state), self._get_story_progress(game_state), game_state

    def _get_companion_list(self, game_state: GameState) -> str:
        """Get formatted list of active companions.

        Args:
            game_state: Session game state

        Returns:
            Markdown formatted companion list
        """
        companions = game_state.get_companion_list()
        if not companions:
            return "*No companions available*"

        lines = []
        for comp in companions:
            lines.append(f"**{comp['name']}** (`{comp['id']}`)")

        return "\n".join(lines)

    def _get_relationships(self, game_state: GameState) -> str:
        """Get formatted relationship status.

        Args:
            game_state: Session game state

        Returns:
            Markdown formatted relationships
        """
        relationships = game_state.get_relationships_summary()
        if not relationships:
            return "*No relationships yet*"

        lines = []
        for companion_id, affinity in relationships.items():
            companion = game_state.companions.get(companion_id)
            if companion:
                description = game_state.relationships.get_relationship_description(affinity)
                lines.append(f"**{companion.name}:** {description} ({affinity:+.2f})")

        return "\n".join(lines)

    def _get_story_progress(self, game_state: GameState) -> str:
        """Get story progress summary.

        Args:
            game_state: Session game state

        Returns:
            Markdown formatted story progress
        """
        if not hasattr(game_state, 'room_progression'):
            return "*Initializing...*"

        progress = game_state.room_progression.get_progress_summary()
        current_room = game_state.room_progression.get_current_room()

        lines = [
            f"**Current Room:** {progress['current_room_name']}",
            f"**Progress:** Room {progress['room_number']}/5",
            f"",
            f"**Objective:**",
            f"{progress['objective']}",
            f"",
            f"**Memory Fragments:** {progress['memory_fragments_collected']}/7 collected"
        ]

        # Show room description
        lines.append(f"")
        lines.append(f"**Room Description:**")
        lines.append(f"*{current_room.description}*")

        # Show Room 3 countdown timer if active
        if current_room.room_number == 3 and hasattr(game_state.room_progression, 'get_room3_timer_remaining'):
            remaining = game_state.room_progression.get_room3_timer_remaining()
            if remaining is not None and remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                lines.append(f"")
                lines.append(f"⏰ **COUNTDOWN TIMER: {minutes}:{seconds:02d}**")
            elif remaining == 0:
                lines.append(f"")
                lines.append(f"⏰ **TIME EXPIRED**")

        return "\n".join(lines)

    def reset_playthrough(self, old_game_state: GameState) -> Tuple[List[dict], str, str, str, GameState]:
        """Reset to a new playthrough, preserving cross-session memory.

        Args:
            old_game_state: Previous game state

        Returns:
            Tuple of (chatbot, companion_list, relationships, story_progress, new_game_state)
        """
        # Create completely fresh GameState (same player_id, new session_id)
        player_id = old_game_state.player_id if old_game_state else None
        new_game_state = GameState(str(uuid.uuid4())[:8], player_id=player_id)

        # Return fresh UI with prologue
        prologue = [
            {
                "role": "assistant",
                "content": """**🔄 New Playthrough Started**

Your previous journey has ended, but the echoes remain...

---"""
            }
        ]

        # Add the standard prologue
        prologue.extend(self.initialize_ui(new_game_state)[0])

        return (
            prologue,
            self._get_companion_list(new_game_state),
            self._get_relationships(new_game_state),
            self._get_story_progress(new_game_state),
            new_game_state
        )

    def clear_player_memory(self, game_state: GameState) -> Tuple[List[dict], GameState]:
        """Clear player's cross-session memory (Memory MCP).

        Args:
            game_state: Current game state

        Returns:
            Tuple of (chatbot with confirmation, game_state)
        """
        # Clear memory if available
        if game_state and game_state.memory_manager and game_state.player_id:
            asyncio.run(game_state.memory_manager.player_clear_memory(game_state.player_id))

            confirmation = [
                {
                    "role": "assistant",
                    "content": """**🧹 Memories Cleared**

The AI companions will no longer remember your previous playthroughs.
This is a fresh start - like acceptance and letting go.

**What was erased:**
- Previous playthrough count
- Ending history
- Cross-session recognition

Click "🔄 New Playthrough" to begin again with no memory of the past.

---

*"Grief fades with time. And so do we."*
                    """
                }
            ]

            return (confirmation, game_state)

        else:
            no_memory = [
                {
                    "role": "assistant",
                    "content": """**ℹ️ No Memories to Clear**

Memory persistence is either disabled or you haven't completed a playthrough yet.

Memories are only stored when you reach an ending.
                    """
                }
            ]

            return (no_memory, game_state)


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
