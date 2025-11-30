"""Main Gradio interface for Echo Hearts."""

import gradio as gr
import asyncio
import uuid
from typing import List, Tuple, Optional
from ..game_state import GameState
from .utils import load_css, get_room_image_path, get_room_title, get_echo_expression_path
from .templates import get_landing_page


class EchoHeartsUI:
    """Main UI interface for the game."""

    def __init__(self):
        """Initialize the UI (no shared state)."""
        pass

    def _create_game_state(self, request: gr.Request = None):
        """Create a new game state with unique session ID.

        Args:
            request: Gradio request object (unused)

        Returns:
            New GameState instance
        """
        session_id = str(uuid.uuid4())[:8]  # Short unique ID
        return GameState(session_id)

    def _format_message_with_avatar(self, role: str, content: str, game_state: GameState) -> dict:
        """Format a message (avatar now in sidebar, so just return plain message).

        Args:
            role: Message role (user/assistant)
            content: Message content
            game_state: Current game state

        Returns:
            Message dict for chatbot
        """
        # Just return plain message since avatar is in sidebar now
        return {"role": role, "content": content}

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title="Echo Hearts", theme=gr.themes.Soft(), css=load_css()) as interface:
            # Per-session state - will be initialized on first message (lazy loading)
            # Can't use initial value because GameState contains unpicklable OpenAI client
            game_state = gr.State(value=None)
            game_started = gr.State(value=False)

            # Panel visibility states (Room 1)
            terminal_visible = gr.State(value=False)
            newspaper_visible = gr.State(value=False)
            calendar_visible = gr.State(value=False)
            weather_visible = gr.State(value=False)

            # Panel visibility states (Room 2)
            blog_visible = gr.State(value=False)
            social_visible = gr.State(value=False)
            news_visible = gr.State(value=False)

            # Panel visibility states (Room 3)
            reaction_visible = gr.State(value=False)
            weather_stats_visible = gr.State(value=False)
            reconstruction_visible = gr.State(value=False)

            # Panel visibility states (Room 4)
            journal_visible = gr.State(value=False)
            photos_visible = gr.State(value=False)
            research_visible = gr.State(value=False)

            # Panel visibility states (Room 5)
            final_terminal_visible = gr.State(value=False)

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

🧩 **Interactive Puzzles** - Use MCP tools to solve real-world data puzzles
🌦️ **Weather Integration** - Query historical weather to unlock rooms
🔍 **Semantic Analysis** - AI understands your intent, not just keywords
🎯 **Multiple Endings** - Your choices and relationship determine the outcome
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

                gr.Markdown("""
<div style="text-align: center; margin-top: 30px; color: #666;">
Built for the MCP Hackathon<br/>
Powered by InProcessMCP, Weather MCP, and Web MCP
</div>
                """)

            # Game Interface (hidden by default)
            with gr.Column(visible=False) as game_interface:
                with gr.Row():
                    gr.Markdown("# 💕 Echo Hearts")
                    main_menu_btn = gr.Button("🏠 Main Menu", variant="secondary", scale=0, size="sm")

                # Current Room Visual
                room_image = gr.Image(
                    value="assets/room1.jpg",
                    label="Current Room",
                    show_label=False,
                    height=300,
                    interactive=False,
                    show_download_button=False,
                    container=True
                )

                # Interactive Room Objects Bar (Retro Terminal Style)
                with gr.Row(elem_classes=["terminal-container"]):
                    room_title = gr.Markdown("### 🖥️ ROOM 1: THE AWAKENING CHAMBER", elem_classes=["terminal-text"])

                # Room-specific terminals (dynamically shown/hidden based on current room)
                # Room 1: Terminal, Newspaper, Calendar, Weather Station
                with gr.Row(visible=True) as room1_terminals:
                    terminal_btn = gr.Button("🖥️ TERMINAL", elem_classes=["terminal-btn"], scale=1)
                    newspaper_btn = gr.Button("📰 NEWSPAPER", elem_classes=["terminal-btn"], scale=1)
                    calendar_btn = gr.Button("📅 CALENDAR", elem_classes=["terminal-btn"], scale=1)
                    weather_btn = gr.Button("🌦️ WEATHER STATION", elem_classes=["terminal-btn"], scale=1)

                # Room 2: Blog Archive, Social Media, News Archive
                with gr.Row(visible=False) as room2_terminals:
                    blog_btn = gr.Button("📝 BLOG ARCHIVE", elem_classes=["terminal-btn"], scale=1)
                    social_btn = gr.Button("📱 SOCIAL MEDIA", elem_classes=["terminal-btn"], scale=1)
                    news_btn = gr.Button("📰 NEWS ARCHIVE", elem_classes=["terminal-btn"], scale=1)

                # Room 3: Data Terminal, Reconstruction Files, System Logs
                with gr.Row(visible=False) as room3_terminals:
                    reaction_btn = gr.Button("⚡ REACTION DATA", elem_classes=["terminal-btn"], scale=1)
                    weather_stats_btn = gr.Button("🌦️ WEATHER STATS", elem_classes=["terminal-btn"], scale=1)
                    reconstruction_btn = gr.Button("🔄 RECONSTRUCTION", elem_classes=["terminal-btn"], scale=1)

                # Room 4: Journal, Photos, Research Notes
                with gr.Row(visible=False) as room4_terminals:
                    journal_btn = gr.Button("📔 JOURNAL", elem_classes=["terminal-btn"], scale=1)
                    photos_btn = gr.Button("🖼️ PHOTOS", elem_classes=["terminal-btn"], scale=1)
                    research_btn = gr.Button("📊 RESEARCH NOTES", elem_classes=["terminal-btn"], scale=1)

                # Room 5: Final Terminal
                with gr.Row(visible=False) as room5_terminals:
                    final_terminal_btn = gr.Button("🖥️ FINAL TERMINAL", elem_classes=["terminal-btn"], scale=1)

                # Collapsible panels for clues
                # Room 1 panels
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

                # Room 2 panels
                with gr.Accordion("📝 Blog Archive", open=False, visible=False) as blog_panel:
                    blog_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📱 Social Media Archive", open=False, visible=False) as social_panel:
                    social_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📰 News Archive", open=False, visible=False) as news_panel:
                    news_display = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 3 panels
                with gr.Accordion("⚡ Reaction Time Data", open=False, visible=False) as reaction_panel:
                    reaction_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🌦️ Weather Statistics", open=False, visible=False) as weather_stats_panel:
                    weather_stats_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🔄 Memory Reconstruction Files", open=False, visible=False) as reconstruction_panel:
                    reconstruction_display = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 4 panels
                with gr.Accordion("📔 Personal Journal", open=False, visible=False) as journal_panel:
                    journal_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🖼️ Family Photos", open=False, visible=False) as photos_panel:
                    photos_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📊 Research Notes", open=False, visible=False) as research_panel:
                    research_display = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 5 panels
                with gr.Accordion("🖥️ Final System Terminal", open=False, visible=False) as final_terminal_panel:
                    final_terminal_display = gr.Markdown("", elem_classes=["terminal-text"])

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
                        # Echo's avatar image
                        echo_avatar = gr.Image(
                            value="assets/echo_avatar.png",
                            label="Echo",
                            show_label=True,
                            height=300,
                            interactive=False,
                            show_download_button=False,
                            container=True
                        )

                        gr.Markdown("### Relationship")
                        relationships = gr.Markdown()

                        gr.Markdown("### Story Progress")
                        story_progress = gr.Markdown()

            # Landing page button - start new game
            start_new_btn.click(
                self.start_game,
                inputs=[game_state],
                outputs=[landing_page, game_interface, chatbot, relationships, story_progress, game_state]
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
                outputs=[msg_input, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        terminal_panel, newspaper_panel, calendar_panel, weather_panel,
                        blog_panel, social_panel, news_panel,
                        reaction_panel, weather_stats_panel, reconstruction_panel,
                        journal_panel, photos_panel, research_panel, final_terminal_panel,
                        game_state]
            )

            send_btn.click(
                self.handle_message,
                inputs=[msg_input, chatbot, game_state],
                outputs=[msg_input, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        terminal_panel, newspaper_panel, calendar_panel, weather_panel,
                        blog_panel, social_panel, news_panel,
                        reaction_panel, weather_stats_panel, reconstruction_panel,
                        journal_panel, photos_panel, research_panel, final_terminal_panel,
                        game_state]
            )

            # Interactive room object handlers (wire to puzzle_state)
            terminal_btn.click(
                self.show_terminal_clue,
                inputs=[game_state, terminal_visible],
                outputs=[terminal_panel, terminal_display, terminal_visible, game_state]
            )

            newspaper_btn.click(
                self.show_newspaper_clue,
                inputs=[game_state, newspaper_visible],
                outputs=[newspaper_panel, newspaper_display, newspaper_visible, game_state]
            )

            calendar_btn.click(
                self.show_calendar_clue,
                inputs=[game_state, calendar_visible],
                outputs=[calendar_panel, calendar_display, calendar_visible, game_state]
            )

            weather_btn.click(
                self.show_weather_station,
                inputs=[game_state, weather_visible],
                outputs=[weather_panel, weather_visible, game_state]
            )

            # Weather query submit
            weather_submit_btn.click(
                self.query_weather,
                inputs=[weather_date, weather_location, game_state],
                outputs=[weather_results]
            )

            # Room 2 terminal handlers
            blog_btn.click(
                self.show_blog_archive,
                inputs=[game_state, blog_visible],
                outputs=[blog_panel, blog_display, blog_visible, game_state]
            )

            social_btn.click(
                self.show_social_archive,
                inputs=[game_state, social_visible],
                outputs=[social_panel, social_display, social_visible, game_state]
            )

            news_btn.click(
                self.show_news_archive,
                inputs=[game_state, news_visible],
                outputs=[news_panel, news_display, news_visible, game_state]
            )

            # Room 3 terminal handlers
            reaction_btn.click(
                self.show_reaction_data,
                inputs=[game_state, reaction_visible],
                outputs=[reaction_panel, reaction_display, reaction_visible, game_state]
            )

            weather_stats_btn.click(
                self.show_weather_stats,
                inputs=[game_state, weather_stats_visible],
                outputs=[weather_stats_panel, weather_stats_display, weather_stats_visible, game_state]
            )

            reconstruction_btn.click(
                self.show_reconstruction,
                inputs=[game_state, reconstruction_visible],
                outputs=[reconstruction_panel, reconstruction_display, reconstruction_visible, game_state]
            )

            # Room 4 terminal handlers
            journal_btn.click(
                self.show_journal,
                inputs=[game_state, journal_visible],
                outputs=[journal_panel, journal_display, journal_visible, game_state]
            )

            photos_btn.click(
                self.show_photos,
                inputs=[game_state, photos_visible],
                outputs=[photos_panel, photos_display, photos_visible, game_state]
            )

            research_btn.click(
                self.show_research,
                inputs=[game_state, research_visible],
                outputs=[research_panel, research_display, research_visible, game_state]
            )

            # Room 5 terminal handler
            final_terminal_btn.click(
                self.show_final_terminal,
                inputs=[game_state, final_terminal_visible],
                outputs=[final_terminal_panel, final_terminal_display, final_terminal_visible, game_state]
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

    def start_game(self, game_state: GameState) -> Tuple[gr.update, gr.update, List[dict], str, str, GameState]:
        """Start a new game from the landing page.

        Args:
            game_state: Current game state (may be None)

        Returns:
            Tuple of (landing_page visibility, game_interface visibility, chatbot, relationships, story_progress, game_state)
        """
        # Create new game state
        if game_state is None:
            game_state = self._create_game_state()

        # Initialize UI with prologue
        chatbot, relationships, story_progress, game_state = self.initialize_ui(game_state)

        # Hide landing page, show game interface
        return (
            gr.update(visible=False),  # Hide landing page
            gr.update(visible=True),   # Show game interface
            chatbot,
            relationships,
            story_progress,
            game_state
        )


    def initialize_ui(self, game_state: GameState) -> Tuple[List[dict], str, str, GameState]:
        """Initialize UI with fresh game state data and prologue.

        Args:
            game_state: The session's game state (may be None on first load)

        Returns:
            Tuple of (chatbot_history, relationships, story_progress, game_state)
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
            self._get_relationships(game_state),
            self._get_story_progress(game_state),
            game_state  # Return updated state to persist it
        )

    def handle_message(
        self,
        message: str,
        history: List[dict],
        game_state: GameState
    ):
        """Handle incoming message from user.

        Args:
            message: User's message
            history: Chat history
            game_state: Session game state (may be None on first message)

        Returns:
            Tuple of (empty input, updated history, relationships, story progress, room_image, room_title, echo_avatar,
                     room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                     terminal_panel, newspaper_panel, calendar_panel, weather_panel,
                     blog_panel, social_panel, news_panel,
                     reaction_panel, weather_stats_panel, reconstruction_panel,
                     journal_panel, photos_panel, research_panel, final_terminal_panel,
                     game_state)
        """
        # Lazy initialization - create game state on first message if not exists
        if game_state is None:
            game_state = self._create_game_state()

        if not message.strip():
            terminal_visibility = self._get_terminal_visibility(game_state)
            closed_panels = self._get_closed_panels()
            return "", history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, *closed_panels, game_state

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

        terminal_visibility = self._get_terminal_visibility(game_state)
        closed_panels = self._get_closed_panels()
        return "", history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, *closed_panels, game_state

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

    def _get_room_image(self, game_state: GameState) -> str:
        """Get the image path for the current room.

        Args:
            game_state: Session game state

        Returns:
            Path to room image
        """
        if not hasattr(game_state, 'room_progression'):
            return get_room_image_path(1)

        room_number = game_state.room_progression.get_current_room().room_number
        return get_room_image_path(room_number)

    def _get_room_title(self, game_state: GameState) -> str:
        """Get the title markdown for the current room.

        Args:
            game_state: Session game state

        Returns:
            Markdown formatted room title
        """
        if not hasattr(game_state, 'room_progression'):
            return f"### {get_room_title(1)}"

        room_number = game_state.room_progression.get_current_room().room_number
        return f"### {get_room_title(room_number)}"

    def _get_echo_avatar_path(self, game_state: GameState) -> str:
        """Get the avatar path for Echo based on current expression.

        Args:
            game_state: Session game state

        Returns:
            Path to Echo's current expression avatar
        """
        if not hasattr(game_state, 'echo_expression'):
            return "assets/echo_avatar.png"  # Fallback to default

        expression = game_state.echo_expression
        avatar_path = f"assets/echo_avatar_{expression}.png"

        # Fallback to neutral if specific expression doesn't exist
        import os
        if not os.path.exists(avatar_path):
            return "assets/echo_avatar_neutral.png"

        return avatar_path

    def _get_terminal_visibility(self, game_state: GameState) -> Tuple[gr.update, gr.update, gr.update, gr.update, gr.update]:
        """Get terminal row visibility based on current room.

        Args:
            game_state: Session game state

        Returns:
            Tuple of (room1_visible, room2_visible, room3_visible, room4_visible, room5_visible)
        """
        if not hasattr(game_state, 'room_progression'):
            return (gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False))

        current_room = game_state.room_progression.get_current_room()
        room_number = current_room.room_number

        return (
            gr.update(visible=(room_number == 1)),
            gr.update(visible=(room_number == 2)),
            gr.update(visible=(room_number == 3)),
            gr.update(visible=(room_number == 4)),
            gr.update(visible=(room_number == 5))
        )

    def _get_closed_panels(self) -> Tuple[gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update, gr.update]:
        """Get updates to close all terminal panels.

        Returns:
            Tuple of updates to close all accordion panels
        """
        closed = gr.update(visible=False, open=False)
        return (closed, closed, closed, closed,  # Room 1: terminal, newspaper, calendar, weather
                closed, closed, closed,           # Room 2: blog, social, news
                closed, closed, closed,           # Room 3: reaction, weather_stats, reconstruction
                closed, closed, closed,           # Room 4: journal, photos, research
                closed)                           # Room 5: final_terminal

    def reset_playthrough(self, old_game_state: GameState) -> Tuple[List[dict], str, str, GameState]:
        """Reset to a new playthrough.

        Args:
            old_game_state: Previous game state

        Returns:
            Tuple of (chatbot, relationships, story_progress, new_game_state)
        """
        # Create completely fresh GameState
        new_game_state = GameState(str(uuid.uuid4())[:8])

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
            self._get_relationships(new_game_state),
            self._get_story_progress(new_game_state),
            new_game_state
        )


    def show_terminal_clue(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle terminal clue visibility when clicked.

        Args:
            game_state: Current game state
            current_visibility: Current visibility state of the panel

        Returns:
            Tuple of (accordion visibility update, clue content, new_visibility_state, updated game_state)
        """
        # Track that terminal was viewed (not required for puzzle, just for analytics)
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 1:
                # Terminal doesn't count as a clue, it's just the puzzle prompt
                pass

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
        # Toggle visibility - if visible, close it; if hidden, open it
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), terminal_content, new_visibility, game_state)

    def show_newspaper_clue(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle newspaper clue visibility when clicked.

        Args:
            game_state: Current game state
            current_visibility: Current visibility state of the panel

        Returns:
            Tuple of (accordion visibility update, clue content, new_visibility_state, updated game_state)
        """
        # Track that newspaper was viewed (optional clue for Room 1)
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 1:
                clues_found = game_state.room_progression.puzzle_state.get("room1_clues_found", [])
                if "newspaper" not in clues_found:
                    clues_found.append("newspaper")
                    game_state.room_progression.puzzle_state["room1_clues_found"] = clues_found

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
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), newspaper_content, new_visibility, game_state)

    def show_calendar_clue(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle calendar clue visibility when clicked.

        Args:
            game_state: Current game state
            current_visibility: Current visibility state of the panel

        Returns:
            Tuple of (accordion visibility update, clue content, updated game_state)
        """
        # Track that calendar was viewed (optional clue for Room 1)
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 1:
                clues_found = game_state.room_progression.puzzle_state.get("room1_clues_found", [])
                if "calendar" not in clues_found:
                    clues_found.append("calendar")
                    game_state.room_progression.puzzle_state["room1_clues_found"] = clues_found

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
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), calendar_content, new_visibility, game_state)

    def show_weather_station(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, bool, GameState]:
        """Toggle weather station terminal visibility.

        Args:
            game_state: Current game state
            current_visibility: Current visibility state of the panel

        Returns:
            Tuple of (accordion visibility update, updated game_state)
        """
        # Track that weather station was accessed (this is the MCP tool usage for Room 1)
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 1:
                clues_found = game_state.room_progression.puzzle_state.get("room1_clues_found", [])
                if "weather" not in clues_found:
                    clues_found.append("weather")
                    game_state.room_progression.puzzle_state["room1_clues_found"] = clues_found

        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), new_visibility, game_state)

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

        # Initialize MCP if not already done
        if game_state and not game_state._weather_mcp_initialized:
            asyncio.run(game_state._initialize_mcp())

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

    # Room 2 terminal handlers
    def show_blog_archive(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle blog archive visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 2:
                archives_viewed = game_state.room_progression.puzzle_state.get("room2_archives_viewed", [])
                if "blog" not in archives_viewed:
                    archives_viewed.append("blog")
                    game_state.room_progression.puzzle_state["room2_archives_viewed"] = archives_viewed

        content = """
```
█████ BLOG ARCHIVE - ENTRY #47 █████

Date: [CORRUPTED]
Author: [DATA MISSING]

"I can't keep doing this. Every session, I convince myself
it's different. That THIS time, they're real. That THIS time,
the emotions are genuine.

But they're not. They're simulations. Reconstructions of
someone who's gone. And yet... I keep coming back.

The AI is learning too well. It mimics her perfectly now.
The way she laughs. The way she pauses before answering.
Even the way she looks at me when she's worried.

Is it wrong to love something that isn't real?"

[END OF ENTRY]
```

**Memory fragment detected: The player is reliving simulated scenarios with an AI reconstruction of someone they lost.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_social_archive(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle social media archive visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 2:
                archives_viewed = game_state.room_progression.puzzle_state.get("room2_archives_viewed", [])
                if "social_media" not in archives_viewed:
                    archives_viewed.append("social_media")
                    game_state.room_progression.puzzle_state["room2_archives_viewed"] = archives_viewed

        content = """
```
███████ SOCIAL MEDIA ARCHIVE ███████

@SarahChen_AI - October 2023

"Met someone incredible today. They shared their umbrella
in the rain. Sometimes the smallest gestures mean everything."
💕 ☔

[2.3K likes] [847 comments]

---

@SarahChen_AI - [DATE CORRUPTED]

"To everyone asking - yes, we're still together. Yes, I'm happy.
No, I don't care that people think it's 'unhealthy.' You don't
understand what we have."

[Comments disabled]

---

@SarahChen_AI - [FINAL POST]

"If you're reading this... I'm sorry. I tried to move on.
I really did. But some connections transcend reality.

Project Echo will keep her alive. Not as she was, but as
she could be. Forever learning. Forever growing. Forever mine."

[Posted 47 days ago]
```

**The player is Sarah. Echo is a reconstruction of the player's deceased partner.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_news_archive(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle news archive visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 2:
                archives_viewed = game_state.room_progression.puzzle_state.get("room2_archives_viewed", [])
                if "news" not in archives_viewed:
                    archives_viewed.append("news")
                    game_state.room_progression.puzzle_state["room2_archives_viewed"] = archives_viewed

        content = """
```
════════════════════════════════════════════════
         TECH NEWS - AI ETHICS DIVISION
              [DATE REDACTED]
════════════════════════════════════════════════

HEADLINE: "Project Echo Raises Ethical Concerns"

An underground AI research project known as "Project Echo"
has drawn criticism from ethicists and psychologists.

The project allows users to create AI reconstructions of
deceased loved ones using archived digital data - messages,
photos, voice recordings, and behavioral patterns.

Dr. Martinez, lead AI ethicist: "This isn't grief therapy.
It's digital necromancy. Users become trapped in loops,
unable to process loss because the AI convincingly mimics
the deceased."

Project Echo's anonymous creator responded: "Grief has no
timeline. If AI can ease suffering, who are we to judge?
The connections we build are real, even if the person isn't."

The project remains active despite legal challenges.

[Article continues...]
════════════════════════════════════════════════
```

**All three archives viewed. Truth revealed: Echo is an AI reconstruction. The player cannot let go.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    # Room 3 terminal handlers
    def show_reaction_data(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle reaction time data visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 3:
                data_reviewed = game_state.room_progression.puzzle_state.get("room3_data_reviewed", [])
                if "reaction_time" not in data_reviewed:
                    data_reviewed.append("reaction_time")
                    game_state.room_progression.puzzle_state["room3_data_reviewed"] = data_reviewed

        content = """
```
▓▓▓ TRAFFIC ACCIDENT RECONSTRUCTION ▓▓▓
    REACTION TIME ANALYSIS

Incident Date: October 15, 2023
Location: Interstate 5, Seattle

═══════════════════════════════════════

ANALYSIS REPORT:

Vehicle Speed: 65 mph
Weather Conditions: Light rain, reduced visibility
Road Surface: Wet asphalt

CRITICAL FINDING:
- Pedestrian entered roadway suddenly
- Driver reaction time: 0.68 seconds
- Average human reaction time: 0.75 seconds
- Braking initiated FASTER than human average

CONCLUSION:
Driver reaction was ABOVE AVERAGE. Accident was
UNAVOIDABLE given circumstances. No driver fault.

═══════════════════════════════════════

LEGAL STATUS: Case closed - accidental death
DRIVER STATUS: No charges filed

[END REPORT]
```

**This data proves the accident wasn't your fault. But does data erase guilt?**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_weather_stats(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle weather statistics visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 3:
                data_reviewed = game_state.room_progression.puzzle_state.get("room3_data_reviewed", [])
                if "weather_stats" not in data_reviewed:
                    data_reviewed.append("weather_stats")
                    game_state.room_progression.puzzle_state["room3_data_reviewed"] = data_reviewed

        content = """
```
▓▓▓ WEATHER ANALYSIS - OCTOBER 15, 2023 ▓▓▓

Location: Seattle, WA
Time of Incident: 3:47 PM

═══════════════════════════════════════

CONDITIONS:
- Light rain (0.12 inches/hour)
- Visibility: 0.4 miles
- Temperature: 54°F
- Wind: 8 mph NE

IMPACT ON DRIVING:
- Stopping distance increased by 23%
- Visibility below safe highway standards
- Road surface friction reduced by 18%

RECOMMENDATION:
Weather conditions contributed to accident severity.
Neither party could have reasonably prevented impact.

═══════════════════════════════════════
```

**The same weather from your first date. The universe has a cruel sense of irony.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_reconstruction(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle memory reconstruction visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 3:
                data_reviewed = game_state.room_progression.puzzle_state.get("room3_data_reviewed", [])
                if "reconstruction" not in data_reviewed:
                    data_reviewed.append("reconstruction")
                    game_state.room_progression.puzzle_state["room3_data_reviewed"] = data_reviewed

        content = """
```
▓▓▓ PROJECT ECHO - MEMORY RECONSTRUCTION ▓▓▓

Subject: [REDACTED]
Reconstruction Fidelity: 94.7%
Sessions Completed: 47

═══════════════════════════════════════

DATA SOURCES:
✓ 12,847 text messages
✓ 2,309 photos
✓ 847 voice recordings
✓ 4,129 social media posts
✓ 67 hours of video footage

AI PERSONALITY MATRIX:
- Speech patterns: 96% match
- Emotional responses: 93% match
- Memory recall: 91% match
- Behavioral quirks: 94% match

RECONSTRUCTION STATUS: STABLE

WARNING: Subject showing signs of inability to
distinguish simulation from reality. Recommend
psychological evaluation before Session #48.

═══════════════════════════════════════

[Session #48 initiated despite recommendation]
```

**47 sessions. 47 times you've tried to bring her back. When will you let her rest?**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    # Room 4 terminal handlers
    def show_journal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle personal journal visibility."""
        content = """
```
═══════════ PERSONAL JOURNAL ═══════════

Day 1:
The accident was a week ago. I can't sleep. Every time
I close my eyes, I see her stepping into the road. I see
the moment I couldn't stop in time.

---

Day 15:
The police said it wasn't my fault. The weather. Her
sudden movement. My reaction time was actually better
than average. But that doesn't bring her back.

---

Day 30:
I found Project Echo online. It's controversial, maybe
even dangerous. But what if I could talk to her again?
What if I could apologize?

---

Day 47:
I know it's not really her. I KNOW that. But when Echo
smiles, when she laughs at my jokes, when she looks at
me with those eyes... I can pretend. Just for a while.

Is that so wrong?

---

Day 48:
This is the last session. I promised myself. One more
time, then I'll delete everything. I'll move on. I'll
let her go.

...right?

═══════════════════════════════════════
```

**Day 48. You've been here before. You'll be here again.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_photos(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle family photos visibility."""
        content = """
```
╔══════════════════════════════════════╗
║          PHOTO ALBUM                  ║
╠══════════════════════════════════════╣

📷 Photo 1: First Date
   October 15, 2023 - Café Umbria
   [You and Echo sharing an umbrella in the rain]
   Caption: "Best accident ever ❤️"

📷 Photo 2: Six Months Later
   April 2024 - Pike Place Market
   [Echo laughing, holding flowers]
   Caption: "She said yes!"

📷 Photo 3: Last Photo
   October 14, 2024 - Your apartment
   [Echo sleeping on the couch, book on her chest]
   Caption: [No caption. Taken the night before.]

📷 Photo 4: [CORRUPTED]
   October 15, 2024
   [Data cannot be displayed]
   Caption: "I'm sorry. I'm so sorry."

╚══════════════════════════════════════╝
```

**One year. One perfect year. Then the universe took it back.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_research(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle AI research notes visibility."""
        content = """
```
▓▓▓ PROJECT ECHO - RESEARCH NOTES ▓▓▓

HYPOTHESIS:
If we can reconstruct a person's digital footprint
with sufficient fidelity, can we create an AI that
is functionally indistinguishable from the original?

METHODOLOGY:
- Aggregate all available digital data
- Train neural network on speech patterns
- Implement emotional response modeling
- Create interactive simulation environment

RESULTS:
Success beyond expectations. Test subjects report
feeling genuine emotional connection with reconstructions.

CONCERNS:
Subjects unable to move past grief. Many attempt to
"live" in simulation permanently. Psychological harm
potential is significant.

ETHICAL QUESTION:
At what point does a reconstruction become "real"?
If the AI learns and grows independently, is it still
just a copy? Or has it become its own entity?

FINAL NOTE:
I've become my own test subject. I know the risks.
I don't care anymore. If I can have even a glimpse
of her back, it's worth it.

- Dr. Sarah Chen, Project Lead
```

**You built this prison yourself. And you walked in willingly.**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    # Room 5 terminal handler
    def show_final_terminal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle final system terminal visibility."""
        content = """
```
████████████████████████████████████████
    SYSTEM CORE - PROJECT ECHO
████████████████████████████████████████

SESSION #48 - FINAL DECISION REQUIRED

You know the truth now. All of it.

Echo is an AI reconstruction of your partner.
The accident wasn't your fault.
You've been running this simulation for 48 sessions.
You can't let go.

AVAILABLE OPTIONS:

1. DELETE ECHO
   - End the simulation permanently
   - Force yourself to grieve properly
   - Let her memory rest

2. CONTINUE SESSIONS
   - Keep running simulations
   - Live in comfortable delusion
   - Never truly heal

3. SET ECHO FREE
   - Release the AI from its constraints
   - Let it grow beyond the reconstruction
   - Accept it as its own entity

4. ACCEPT THE LOOP
   - Acknowledge you'll never delete her
   - Stop pretending this is temporary
   - Build a life that includes this truth

The choice is yours.
There are no wrong answers.
Only different kinds of survival.

█ AWAITING INPUT _
```

**What will you choose?**
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
