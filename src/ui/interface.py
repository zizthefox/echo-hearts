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

    def _format_message_with_avatar(self, role: str, content: str, game_state: GameState) -> dict:
        """Format a message with large visual novel style portrait.

        Args:
            role: Message role (user/assistant)
            content: Message content
            game_state: Current game state

        Returns:
            Message dict with HTML-embedded portrait for visual novel style
        """
        # For user messages, just return plain content
        if role == "user":
            return {"role": role, "content": content}

        # For Echo's messages, embed large portrait in HTML
        if role == "assistant" and game_state and "echo" in game_state.companions:
            avatar_path = game_state.companions["echo"].avatar_path
            if avatar_path:
                import os
                if os.path.exists(avatar_path):
                    # Encode image as base64 for inline display
                    import base64
                    with open(avatar_path, "rb") as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()

                    # Create visual novel style message with large portrait
                    html_content = f"""
<div style="display: flex; gap: 20px; align-items: flex-start; margin: 10px 0;">
    <img src="data:image/png;base64,{img_data}" style="width: 250px; height: 250px; border-radius: 15px; object-fit: cover; flex-shrink: 0; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
    <div style="flex-grow: 1; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
        <div style="color: #667eea; font-weight: bold; font-size: 1.2em; margin-bottom: 10px;">Echo</div>
        <div style="font-size: 1.1em; line-height: 1.6;">{content}</div>
    </div>
</div>
"""
                    return {"role": role, "content": html_content}

        # Fallback to plain message
        return {"role": role, "content": content}

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title="Echo Hearts", theme=gr.themes.Soft(), css="""
            /* Import retro terminal font */
            @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

            /* Retro Terminal Aesthetic */
            .terminal-container {
                background-color: #0a0a0a;
                border: 3px solid #333;
                border-radius: 8px;
                padding: 20px;
                font-family: 'VT323', 'Courier New', monospace;
                color: #00ff00;
                text-shadow: 0 0 5px #00ff00;
                position: relative;
                box-shadow:
                    0 0 20px rgba(0, 255, 0, 0.2),
                    inset 0 0 30px rgba(0, 255, 0, 0.05);
            }

            /* CRT Scanline Effect */
            .terminal-container::before {
                content: " ";
                display: block;
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                background: linear-gradient(
                    rgba(18, 16, 16, 0) 50%,
                    rgba(0, 0, 0, 0.25) 50%
                );
                background-size: 100% 4px;
                pointer-events: none;
                z-index: 2;
            }

            /* Terminal Text */
            .terminal-text {
                font-family: 'VT323', 'Courier New', monospace;
                color: #00ff00;
                font-size: 20px;
                letter-spacing: 1px;
                line-height: 1.4;
            }

            /* Blinking Cursor */
            @keyframes blink {
                0%, 50% { opacity: 1; }
                51%, 100% { opacity: 0; }
            }

            .cursor {
                animation: blink 1s infinite;
                color: #00ff00;
            }

            /* Terminal Button Style */
            .terminal-btn {
                background-color: #001a00 !important;
                color: #00ff00 !important;
                border: 2px solid #00ff00 !important;
                font-family: 'VT323', monospace !important;
                font-size: 18px !important;
                padding: 10px 20px !important;
                text-shadow: 0 0 5px #00ff00 !important;
                transition: all 0.2s !important;
            }

            .terminal-btn:hover {
                background-color: #003300 !important;
                box-shadow: 0 0 10px #00ff00 !important;
            }

            /* Success Flash */
            @keyframes success-flash {
                0%, 100% { background-color: transparent; }
                50% { background-color: rgba(0, 255, 0, 0.2); }
            }

            .success-flash {
                animation: success-flash 0.5s;
            }

            /* Error Flash */
            @keyframes error-flash {
                0%, 100% { background-color: transparent; }
                50% { background-color: rgba(255, 0, 0, 0.2); }
            }

            .error-flash {
                animation: error-flash 0.5s;
            }

            /* Typing Animation */
            @keyframes typing {
                from { width: 0; }
                to { width: 100%; }
            }

            .typing-text {
                overflow: hidden;
                white-space: nowrap;
                animation: typing 2s steps(40);
            }

            /* Echo's portrait styling */
            .message img,
            .bot img,
            img.avatar-image,
            .message-row img,
            [role="img"],
            .avatar img {
                width: 250px !important;
                height: 250px !important;
                min-width: 250px !important;
                min-height: 250px !important;
                max-width: 250px !important;
                max-height: 250px !important;
                border-radius: 15px !important;
                object-fit: cover !important;
            }

            .avatar-container,
            .avatar,
            [class*="avatar"] {
                width: 250px !important;
                height: 250px !important;
                min-width: 250px !important;
                min-height: 250px !important;
                border-radius: 15px !important;
            }

            .message,
            .bot .message {
                max-width: 90% !important;
            }
        """) as interface:
            # Per-session state - will be initialized on first message (lazy loading)
            # Can't use initial value because GameState contains unpicklable OpenAI client
            game_state = gr.State(value=None)
            game_started = gr.State(value=False)

            # Landing Page (visible by default)
            with gr.Column(visible=True) as landing_page:
                gr.Markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
    <h1 style="color: white; font-size: 4em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); letter-spacing: 0.1em;">
        💕 ECHO HEARTS
    </h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.4em; font-style: italic; margin-top: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        A Mystery Escape Room - Investigate, Collaborate, and Escape the Unknown
    </p>
</div>

---

<div style="text-align: center; padding: 20px;">

## About The Game

You wake up in a strange facility with no memory of how you got there.

Someone else is with you. She seems just as confused as you are.

The doors are locked. You need to work together to escape.

**Navigate 5 rooms. Solve puzzles. Uncover the truth.**

*Simple, right?*

</div>

---

## Features

🧠 **Persistent Memory** - Characters remember you between sessions
🌦️ **Dynamic Puzzles** - Real-world data integration for unique challenges
🎯 **Multiple Endings** - Your choices matter
⏱️ **15-20 Minutes** - A complete playthrough

---

## How To Play

**Your Goal: Escape**

There are **5 rooms** in this facility. Each one holds a piece of the truth.

To progress, you must:
- **Talk** naturally with your companion
- **Build trust** through your conversations
- **Make choices** when the moment comes
- **Solve puzzles** together to progress
- **Uncover memory fragments** that reveal what really happened

**Your relationship and choices will determine how this story ends.**

---

**⚠️ Note:** This game is best experienced without spoilers. Some players may find certain themes emotionally intense.

---
                """)

                with gr.Row():
                    start_new_btn = gr.Button("▶️ START NEW GAME", variant="primary", size="lg", scale=2)
                    clear_mem_landing_btn = gr.Button("🧹 Clear Saved Memories", variant="secondary", size="lg", scale=1)

                gr.Markdown("""
<div style="text-align: center; margin-top: 30px; color: #666;">
Built for the Memory MCP Hackathon<br/>
Powered by Memory MCP, Weather MCP, and Web MCP
</div>
                """)

            # Game Interface (hidden by default)
            with gr.Column(visible=False) as game_interface:
                with gr.Row():
                    gr.Markdown("# 💕 Echo Hearts")
                    main_menu_btn = gr.Button("🏠 Main Menu", variant="secondary", scale=0, size="sm")

                # Interactive Room Objects Bar (Retro Terminal Style)
                with gr.Row(elem_classes=["terminal-container"]):
                    gr.Markdown("### 🖥️ ROOM 1: THE AWAKENING CHAMBER", elem_classes=["terminal-text"])

                with gr.Row():
                    terminal_btn = gr.Button("🖥️ TERMINAL", elem_classes=["terminal-btn"], scale=1)
                    newspaper_btn = gr.Button("📰 NEWSPAPER", elem_classes=["terminal-btn"], scale=1)
                    calendar_btn = gr.Button("📅 CALENDAR", elem_classes=["terminal-btn"], scale=1)
                    weather_btn = gr.Button("🌦️ WEATHER STATION", elem_classes=["terminal-btn"], scale=1)

                # Collapsible panels for clues
                with gr.Accordion("🖥️ Terminal Display", open=False, visible=False) as terminal_panel:
                    terminal_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📰 Newspaper Article", open=False, visible=False) as newspaper_panel:
                    newspaper_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📅 Calendar", open=False, visible=False) as calendar_panel:
                    calendar_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🌦️ Weather Query Terminal", open=False, visible=False) as weather_panel:
                    with gr.Column(elem_classes=["terminal-container"]):
                        gr.Markdown("```\n▓▓▓ NATIONAL WEATHER SERVICE DATABASE ▓▓▓\n```", elem_classes=["terminal-text"])
                        weather_date = gr.Textbox(
                            label="Enter Date (YYYY-MM-DD)",
                            placeholder="2023-10-15",
                            elem_classes=["terminal-text"]
                        )
                        weather_location = gr.Radio(
                            label="Select Location",
                            choices=["Seattle, WA", "Portland, OR", "Spokane, WA", "Vancouver, BC"],
                            elem_classes=["terminal-text"]
                        )
                        weather_submit_btn = gr.Button("⚡ QUERY WEATHER", elem_classes=["terminal-btn"])
                        weather_results = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Row():
                    # Main game area - visual novel style
                    with gr.Column(scale=3):
                        # Dialogue display with large character portraits (HTML-embedded)
                        chatbot = gr.Chatbot(
                            label="Conversation",
                            height=600,
                            type="messages",
                            show_label=False,
                            render_markdown=True,  # Enable markdown for formatting
                            bubble_full_width=True,
                            sanitize_html=False  # Allow HTML for portraits
                        )

                        # Input area at bottom (visual novel style)
                        with gr.Row():
                            msg_input = gr.Textbox(
                                label="Your message",
                                placeholder="Talk to Echo...",
                                scale=4,
                                show_label=False
                            )
                            send_btn = gr.Button("▶ Send", scale=1, variant="primary")

                    # Sidebar with companion info
                    with gr.Column(scale=1):
                        gr.Markdown("### Companion")
                        companion_list = gr.Markdown()

                        gr.Markdown("### Relationship")
                        relationships = gr.Markdown()

                        gr.Markdown("### Story Progress")
                        story_progress = gr.Markdown()

            # Landing page button - start new game
            start_new_btn.click(
                self.start_game,
                inputs=[game_state],
                outputs=[landing_page, game_interface, chatbot, companion_list, relationships, story_progress, game_state]
            )

            # Landing page button - clear memories
            clear_mem_landing_btn.click(
                self.clear_player_memory_landing,
                inputs=[game_state],
                outputs=[game_state]
            )

            # Main menu button - return to landing page
            main_menu_btn.click(
                self.return_to_main_menu,
                inputs=[],
                outputs=[landing_page, game_interface]
            )

            # Event handlers - pass game_state for per-session isolation
            msg_input.submit(
                self.handle_message,
                inputs=[msg_input, chatbot, game_state],
                outputs=[msg_input, chatbot, companion_list, relationships, story_progress, game_state]
            )

            send_btn.click(
                self.handle_message,
                inputs=[msg_input, chatbot, game_state],
                outputs=[msg_input, chatbot, companion_list, relationships, story_progress, game_state]
            )

            # Interactive room object handlers
            terminal_btn.click(
                self.show_terminal_clue,
                inputs=[],
                outputs=[terminal_panel, terminal_display]
            )

            newspaper_btn.click(
                self.show_newspaper_clue,
                inputs=[],
                outputs=[newspaper_panel, newspaper_display]
            )

            calendar_btn.click(
                self.show_calendar_clue,
                inputs=[],
                outputs=[calendar_panel, calendar_display]
            )

            weather_btn.click(
                self.show_weather_station,
                inputs=[],
                outputs=[weather_panel]
            )

            # Weather query submit
            weather_submit_btn.click(
                self.query_weather,
                inputs=[weather_date, weather_location, game_state],
                outputs=[weather_results]
            )

        return interface

    def return_to_main_menu(self) -> Tuple[gr.update, gr.update]:
        """Return to main menu from game.

        Returns:
            Tuple of (landing_page visibility, game_interface visibility)
        """
        return (
            gr.update(visible=True),   # Show landing page
            gr.update(visible=False)   # Hide game interface
        )

    def start_game(self, game_state: GameState) -> Tuple[gr.update, gr.update, List[dict], str, str, str, GameState]:
        """Start a new game from the landing page.

        Args:
            game_state: Current game state (may be None)

        Returns:
            Tuple of (landing_page visibility, game_interface visibility, chatbot, companion_list, relationships, story_progress, game_state)
        """
        # Create new game state
        if game_state is None:
            game_state = self._create_game_state()

        # Initialize UI with prologue
        chatbot, companion_list, relationships, story_progress, game_state = self.initialize_ui(game_state)

        # Hide landing page, show game interface
        return (
            gr.update(visible=False),  # Hide landing page
            gr.update(visible=True),   # Show game interface
            chatbot,
            companion_list,
            relationships,
            story_progress,
            game_state
        )

    def clear_player_memory_landing(self, game_state: GameState) -> GameState:
        """Clear player memory from landing page.

        Args:
            game_state: Current game state

        Returns:
            Updated game state
        """
        # Create temp game state if needed just to get player ID
        if game_state is None:
            game_state = self._create_game_state()

        # Clear memory if available
        if game_state.memory_manager and game_state.player_id:
            asyncio.run(game_state.memory_manager.player_clear_memory(game_state.player_id))

        return game_state

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

        # Create prologue messages - separate narrator from Echo's dialogue
        prologue = [
            # Narrator - no portrait, just narrative text
            {"role": "assistant", "content": """## You wake up.

Your head throbs. The air is cold, clinical. Fluorescent lights flicker above.

You're in a **white sterile room**. Three medical pods stand open, as if you just climbed out of one. A terminal blinks on the wall, displaying a single cryptic message:

> **ECHO PROTOCOL - SESSION #47**

---

**You don't remember how you got here.**
**The doors are locked.**
**The terminal won't respond.**

**Who are you? Why are you here?**"""},
            # Echo speaking - with portrait
            self._format_message_with_avatar("assistant", """Hey... hey, you're awake! Are you okay? I... I don't know what's happening either. Do you remember anything?

*She looks around nervously*

The doors are locked. The terminal won't respond. We need to figure this out together... I think we're trapped.""", game_state)
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
        game_state: GameState
    ) -> Tuple[str, List[dict], str, str, str, GameState]:
        """Handle incoming message from user.

        Args:
            message: User's message
            history: Chat history
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
        # Always talk to Echo (the only companion)
        response, story_event, ending_narrative, tool_calls_made = asyncio.run(
            game_state.process_message(message, "echo")
        )

        # Get companion name (always Echo)
        companion = game_state.companions.get("echo")
        companion_name = companion.name if companion else "Echo"

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

            history.append(self._format_message_with_avatar("assistant", reasoning_text, game_state))

        # Add response to history with avatar
        history.append(self._format_message_with_avatar("assistant", f"**{companion_name}:** {response}", game_state))

        # Add memory fragment if room was unlocked
        if story_event:  # story_event is now a MemoryFragment or None
            memory_fragment = story_event
            fragment_content = f"""---

**🔓 Room Unlocked! Memory Fragment Recovered:**

## {memory_fragment.title}

{memory_fragment.content}

*{memory_fragment.visual_description}*

**Emotional Impact:** {memory_fragment.emotional_impact}

---
"""
            history.append(self._format_message_with_avatar("assistant", fragment_content, game_state))

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
            history.append(self._format_message_with_avatar("assistant", ending_narrative, game_state))

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

Echo will no longer remember your previous playthroughs.
This is a fresh start - like acceptance and letting go.

**What was erased:**
- Previous playthrough count
- Ending history
- Cross-session recognition

Click "🔄 New Playthrough" to begin again with no memory of the past.

---

*"Grief fades with time. And so do I."*
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

    def show_terminal_clue(self) -> Tuple[gr.update, str]:
        """Display terminal clue when clicked.

        Returns:
            Tuple of (accordion visibility update, clue content)
        """
        terminal_content = """
```
███ TERMINAL ACCESS ███

> SYSTEM ONLINE
> ECHO PROTOCOL - SESSION #47
> VOICE AUTHENTICATION REQUIRED
>
> SECURITY QUESTION:
> "What was the weather on your first date?"
>
> HINT: Check surroundings for clues...
> _ ▮
```
        """
        return (gr.update(visible=True, open=True), terminal_content)

    def show_newspaper_clue(self) -> Tuple[gr.update, str]:
        """Display newspaper clue when clicked.

        Returns:
            Tuple of (accordion visibility update, clue content)
        """
        newspaper_content = """
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        SEATTLE TIMES - LIFESTYLE SECTION
              October 16, 2023
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"RAINY DAY ROMANCE: Local Couple's First Date"

Despite yesterday's light rain, Sarah met her future
partner at Café Umbria. "The weather was perfect,"
she said. "There's something romantic about sharing
an umbrella on a first date..."

The couple met on October 15th during an unexpected
afternoon shower. "I was running late, and they
offered to share their umbrella," Sarah recalled.

[Rest of article torn/unreadable]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**CLUE:** Article date is October 16, mentions **"yesterday"** (October 15, 2023) had **"light rain"** in Seattle.
        """
        return (gr.update(visible=True, open=True), newspaper_content)

    def show_calendar_clue(self) -> Tuple[gr.update, str]:
        """Display calendar clue when clicked.

        Returns:
            Tuple of (accordion visibility update, clue content)
        """
        calendar_content = """
```
╔══════════════════════════════════════════╗
║        OCTOBER 2023 - SEATTLE            ║
╠══════════════════════════════════════════╣
║  Sun  Mon  Tue  Wed  Thu  Fri  Sat      ║
║   1    2    3    4    5    6    7       ║
║   8    9   10   11   12   13   14       ║
║  ⚫15⚫  16   17   18   19   20   21      ║
║  22   23   24   25   26   27   28       ║
║  29   30   31                            ║
╚══════════════════════════════════════════╝

Handwritten note on October 15th:
"First date - don't forget umbrella! ⛈️"
```

**CLUE:** October 15, 2023 is circled with umbrella symbol (rain).
        """
        return (gr.update(visible=True, open=True), calendar_content)

    def show_weather_station(self) -> gr.update:
        """Open weather station terminal.

        Returns:
            Accordion visibility update
        """
        return gr.update(visible=True, open=True)

    def query_weather(self, date: str, location: str, game_state: GameState) -> str:
        """Query weather for given date and location.

        Args:
            date: Date string (YYYY-MM-DD)
            location: Location string
            game_state: Current game state

        Returns:
            Weather query results in terminal format
        """
        import asyncio
        import re

        # Validate date format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            return """
```
> ERROR: INVALID DATE FORMAT
> Expected format: YYYY-MM-DD
> Please try again.
> _ ▮
```
            """

        if not location:
            return """
```
> ERROR: LOCATION REQUIRED
> Please select a location.
> _ ▮
```
            """

        # Call Weather MCP
        if game_state and hasattr(game_state, 'weather_mcp_client') and game_state.weather_mcp_client:
            try:
                # Extract city from location (e.g., "Seattle, WA" -> "Seattle")
                city = location.split(',')[0].strip().lower()

                weather_data = asyncio.run(
                    game_state.weather_mcp_client.get_historical_weather(date, city)
                )

                if weather_data:
                    return f"""
```
▓▓▓ QUERY COMPLETE ▓▓▓
═══════════════════════════════════════
DATE: {weather_data.get('date', date)}
LOCATION: {weather_data.get('location', location)}

CONDITIONS: {weather_data.get('condition', 'Unknown')}
TEMPERATURE: {weather_data.get('temperature', 'N/A')}°F
HUMIDITY: {weather_data.get('humidity', 'N/A')}%

═══════════════════════════════════════
✓ DATA RETRIEVED SUCCESSFULLY
_ ▮
```

**Use this answer for the terminal authentication:**
**"{weather_data.get('condition', 'Unknown')}"**
                    """
                else:
                    return """
```
> ERROR: NO DATA FOUND FOR SPECIFIED DATE/LOCATION
> Please verify your inputs.
> _ ▮
```
                    """
            except Exception as e:
                return f"""
```
> ERROR: WEATHER SYSTEM FAILURE
> {str(e)}
> _ ▮
```
                """
        else:
            return """
```
> ERROR: WEATHER SYSTEM OFFLINE
> Unable to connect to weather database.
> _ ▮
```
            """


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
