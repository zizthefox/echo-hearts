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
            answer_terminal_visible = gr.State(value=False)

            # Panel visibility states (Room 2)
            blog_visible = gr.State(value=False)
            social_visible = gr.State(value=False)
            news_visible = gr.State(value=False)
            password_terminal_visible = gr.State(value=False)

            # Panel visibility states (Room 3)
            reaction_visible = gr.State(value=False)
            weather_stats_visible = gr.State(value=False)
            reconstruction_visible = gr.State(value=False)
            conclusion_terminal_visible = gr.State(value=False)

            # Panel visibility states (Room 4)
            journal_visible = gr.State(value=False)
            photos_visible = gr.State(value=False)
            research_visible = gr.State(value=False)
            timeline_terminal_visible = gr.State(value=False)

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
                    answer_terminal_btn = gr.Button("🔓 ANSWER TERMINAL", elem_classes=["terminal-btn"], scale=1)

                # Room 2: Blog Archive, Social Media, News Archive
                with gr.Row(visible=False) as room2_terminals:
                    blog_btn = gr.Button("📝 BLOG ARCHIVE", elem_classes=["terminal-btn"], scale=1)
                    social_btn = gr.Button("📱 SOCIAL MEDIA", elem_classes=["terminal-btn"], scale=1)
                    news_btn = gr.Button("📰 NEWS ARCHIVE", elem_classes=["terminal-btn"], scale=1)
                    password_terminal_btn = gr.Button("🔐 PASSWORD TERMINAL", elem_classes=["terminal-btn"], scale=1)

                # Room 3: Data Terminal, Reconstruction Files, System Logs
                with gr.Row(visible=False) as room3_terminals:
                    reaction_btn = gr.Button("⚡ REACTION DATA", elem_classes=["terminal-btn"], scale=1)
                    weather_stats_btn = gr.Button("🌦️ WEATHER STATS", elem_classes=["terminal-btn"], scale=1)
                    reconstruction_btn = gr.Button("🔄 RECONSTRUCTION", elem_classes=["terminal-btn"], scale=1)
                    conclusion_terminal_btn = gr.Button("⚖️ CONCLUSION TERMINAL", elem_classes=["terminal-btn"], scale=1)

                # Room 4: Journal, Photos, Research Notes
                with gr.Row(visible=False) as room4_terminals:
                    journal_btn = gr.Button("📔 JOURNAL", elem_classes=["terminal-btn"], scale=1)
                    photos_btn = gr.Button("🖼️ PHOTOS", elem_classes=["terminal-btn"], scale=1)
                    research_btn = gr.Button("📊 RESEARCH NOTES", elem_classes=["terminal-btn"], scale=1)
                    timeline_terminal_btn = gr.Button("🔀 TIMELINE TERMINAL", elem_classes=["terminal-btn"], scale=1)

                # Room 5: Final Terminal
                with gr.Row(visible=False) as room5_terminals:
                    final_terminal_btn = gr.Button("🖥️ FINAL TERMINAL", elem_classes=["terminal-btn"], scale=1)

                # Collapsible panels for clues
                # Room 1 panels - Single unified terminal with question and answer input
                with gr.Accordion("🖥️ Terminal", open=False, visible=False) as terminal_panel:
                    with gr.Column(elem_classes=["terminal-container"]):
                        terminal_display = gr.Markdown("", elem_classes=["terminal-text"])
                        # Answer input integrated below the terminal display
                        answer_input = gr.Textbox(
                            label="",
                            placeholder="Enter your answer...",
                            elem_classes=["terminal-text"],
                            visible=False
                        )
                        answer_submit_btn = gr.Button("🔓 SUBMIT ANSWER", elem_classes=["terminal-btn"], visible=False)
                        answer_result = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📰 Newspaper Article", open=False, visible=False) as newspaper_panel:
                    newspaper_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📅 Calendar", open=False, visible=False) as calendar_panel:
                    calendar_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🌦️ Weather Query Terminal", open=False, visible=False) as weather_panel:
                    with gr.Column(elem_classes=["terminal-container"]):
                        gr.Markdown("```\n▓▓▓ NATIONAL WEATHER SERVICE DATABASE ▓▓▓\n```", elem_classes=["terminal-text"])
                        weather_date = gr.Textbox(
                            label="Enter Date (YYYY-MM-DD)",
                            placeholder="2022-10-15",
                            elem_classes=["terminal-text"]
                        )
                        weather_location = gr.Radio(
                            label="Select Location",
                            choices=["Seattle, WA", "Portland, OR", "Spokane, WA", "Vancouver, BC"],
                            elem_classes=["terminal-text"]
                        )
                        weather_submit_btn = gr.Button("⚡ QUERY WEATHER", elem_classes=["terminal-btn"])
                        weather_results = gr.Markdown("", elem_classes=["terminal-text"])

                # Keep answer_panel for backwards compatibility (points to terminal_panel)
                answer_panel = terminal_panel
                answer_terminal_visible = gr.State(False)

                # Room 2 panels
                with gr.Accordion("📝 Blog Archive", open=False, visible=False) as blog_panel:
                    blog_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📱 Social Media Archive", open=False, visible=False) as social_panel:
                    social_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📰 News Archive", open=False, visible=False) as news_panel:
                    news_display = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 2 Password Terminal - SUBMISSION TERMINAL (visually distinct)
                with gr.Accordion("🔐 PASSWORD SUBMISSION TERMINAL", open=False, visible=False) as password_panel:
                    with gr.Column(elem_classes=["submission-terminal"]):
                        gr.Markdown("### ⚠️ PUZZLE SOLUTION TERMINAL", elem_classes=["submission-terminal-header"])
                        gr.Markdown("```\n▓▓▓ SECURE ACCESS TERMINAL ▓▓▓\nENTER PASSWORD TO UNLOCK DOOR\n```", elem_classes=["terminal-text"])
                        gr.Markdown("💡 **Hint:** Passwords are often personal. Check the archives for names and important dates.", elem_classes=["instruction-banner"])
                        password_input = gr.Textbox(
                            label="Password",
                            placeholder="Enter password...",
                            elem_classes=["terminal-text"],
                            type="password"
                        )
                        password_submit_btn = gr.Button("🔓 SUBMIT PASSWORD", elem_classes=["submit-answer-btn"])
                        password_result = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 3 panels
                with gr.Accordion("⚡ Reaction Time Data", open=False, visible=False) as reaction_panel:
                    reaction_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🌦️ Weather Statistics", open=False, visible=False) as weather_stats_panel:
                    weather_stats_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🔄 Memory Reconstruction Files", open=False, visible=False) as reconstruction_panel:
                    reconstruction_display = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 3 Conclusion Terminal - SUBMISSION TERMINAL (visually distinct)
                with gr.Accordion("⚖️ CONCLUSION SUBMISSION TERMINAL", open=False, visible=False) as conclusion_panel:
                    with gr.Column(elem_classes=["submission-terminal"]):
                        gr.Markdown("### ⚠️ PUZZLE SOLUTION TERMINAL", elem_classes=["submission-terminal-header"])
                        gr.Markdown("```\n▓▓▓ ANALYSIS TERMINAL ▓▓▓\nSTATE YOUR CONCLUSION\n```", elem_classes=["terminal-text"])
                        gr.Markdown("💡 **Hint:** Review all the evidence. What does the data say vs what Alex believes?", elem_classes=["instruction-banner"])
                        conclusion_input = gr.Textbox(
                            label="Based on the evidence, what is your conclusion?",
                            placeholder="Enter your conclusion...",
                            elem_classes=["terminal-text"],
                            lines=3
                        )
                        conclusion_submit_btn = gr.Button("⚖️ SUBMIT CONCLUSION", elem_classes=["submit-answer-btn"])
                        conclusion_result = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 4 panels
                with gr.Accordion("📔 Personal Journal", open=False, visible=False) as journal_panel:
                    journal_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("🖼️ Family Photos", open=False, visible=False) as photos_panel:
                    photos_display = gr.Markdown("", elem_classes=["terminal-text"])

                with gr.Accordion("📊 Research Notes", open=False, visible=False) as research_panel:
                    research_display = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 4 Timeline Terminal - SUBMISSION TERMINAL (visually distinct)
                with gr.Accordion("🔀 TIMELINE SUBMISSION TERMINAL", open=False, visible=False) as timeline_panel:
                    with gr.Column(elem_classes=["submission-terminal"]):
                        gr.Markdown("### ⚠️ PUZZLE SOLUTION TERMINAL", elem_classes=["submission-terminal-header"])
                        gr.Markdown("```\n▓▓▓ TIMELINE RECONSTRUCTION ▓▓▓\nORDER THE STAGES\n```", elem_classes=["terminal-text"])
                        gr.Markdown("💡 **Hint:** What happened first? Loss → emotional response → action → consequence → current state.", elem_classes=["instruction-banner"])
                        timeline_input = gr.Textbox(
                            label="Enter the correct order (e.g., LOSS → GRIEF → CREATION → OBSESSION → CYCLE)",
                            placeholder="STAGE1 → STAGE2 → STAGE3 → STAGE4 → STAGE5",
                            elem_classes=["terminal-text"]
                        )
                        timeline_submit_btn = gr.Button("🔀 SUBMIT TIMELINE", elem_classes=["submit-answer-btn"])
                        timeline_result = gr.Markdown("", elem_classes=["terminal-text"])

                # Room 5 panels - Door Selection Terminal - SUBMISSION TERMINAL (visually distinct)
                with gr.Accordion("🚪 FINAL CHOICE SUBMISSION TERMINAL", open=False, visible=False) as final_terminal_panel:
                    with gr.Column(elem_classes=["submission-terminal"]):
                        gr.Markdown("### ⚠️ FINAL DECISION TERMINAL", elem_classes=["submission-terminal-header"])
                        gr.Markdown("```\n▓▓▓ FINAL CHOICE TERMINAL ▓▓▓\nSELECT YOUR PATH\n```", elem_classes=["terminal-text"])
                        gr.Markdown("💡 **Important:** There is no single 'correct' answer. Choose based on your journey through the 5 rooms.", elem_classes=["instruction-banner"])
                        door_choice = gr.Radio(
                            label="Which door do you choose?",
                            choices=["DOOR 1: GOODBYE", "DOOR 2: TOGETHER FOREVER", "DOOR 3: LIBERATION"],
                            elem_classes=["terminal-text"]
                        )
                        door_justification = gr.Textbox(
                            label="Why did you choose this door? (Required)",
                            placeholder="Explain your choice based on what you learned...",
                            elem_classes=["terminal-text"],
                            lines=4
                        )
                        door_submit_btn = gr.Button("🚪 MAKE YOUR CHOICE", elem_classes=["submit-answer-btn"])
                        door_result = gr.Markdown("", elem_classes=["terminal-text"])

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

                        # Voice settings
                        with gr.Accordion("🔊 Voice Settings", open=False):
                            voice_toggle = gr.Checkbox(label="Enable Echo's Voice", value=True)
                            gr.Markdown("*Powered by ElevenLabs*")

                        gr.Markdown("### Relationship")
                        relationships = gr.Markdown()

                        gr.Markdown("### Story Progress")
                        story_progress = gr.Markdown()

            # Audio player for Echo's voice (hidden, auto-plays)
            echo_audio = gr.Audio(label="Echo's Voice", visible=False, autoplay=True)

            # Tutorial Modal (shown at game start)
            tutorial_modal = gr.HTML(value="", elem_id="tutorial-modal")

            # Room Introduction Modal (overlay) - always visible, content controls display
            room_intro_modal = gr.HTML(value="", elem_id="room-intro-modal")

            # Landing page button - start new game
            start_new_btn.click(
                self.start_game,
                inputs=[game_state],
                outputs=[landing_page, game_interface, chatbot, relationships, story_progress, tutorial_modal, game_state]
            )


            # Main menu button - return to landing page
            main_menu_btn.click(
                self.return_to_main_menu,
                inputs=[],
                outputs=[landing_page, game_interface]
            )

            # Voice toggle handler
            voice_toggle.change(
                self.toggle_voice,
                inputs=[voice_toggle, game_state],
                outputs=[game_state]
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
                        room_intro_modal, echo_audio,
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
                        room_intro_modal, echo_audio,
                        game_state]
            )

            # Interactive room object handlers (wire to puzzle_state)
            terminal_btn.click(
                self.show_terminal_clue,
                inputs=[game_state, terminal_visible],
                outputs=[terminal_panel, terminal_display, terminal_visible, answer_input, answer_submit_btn, game_state]
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

            # Answer submission for Room 1 (now integrated into terminal)
            answer_submit_btn.click(
                self.submit_answer,
                inputs=[answer_input, game_state, chatbot],
                outputs=[answer_input, answer_result, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        room_intro_modal, game_state]
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

            password_terminal_btn.click(
                self.show_password_terminal,
                inputs=[game_state, password_terminal_visible],
                outputs=[password_panel, password_terminal_visible, game_state]
            )

            password_submit_btn.click(
                self.submit_password,
                inputs=[password_input, game_state, chatbot],
                outputs=[password_input, password_result, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        room_intro_modal, game_state]
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

            conclusion_terminal_btn.click(
                self.show_conclusion_terminal,
                inputs=[game_state, conclusion_terminal_visible],
                outputs=[conclusion_panel, conclusion_terminal_visible, game_state]
            )

            conclusion_submit_btn.click(
                self.submit_conclusion,
                inputs=[conclusion_input, game_state, chatbot],
                outputs=[conclusion_input, conclusion_result, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        room_intro_modal, game_state]
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

            timeline_terminal_btn.click(
                self.show_timeline_terminal,
                inputs=[game_state, timeline_terminal_visible],
                outputs=[timeline_panel, timeline_terminal_visible, game_state]
            )

            timeline_submit_btn.click(
                self.submit_timeline,
                inputs=[timeline_input, game_state, chatbot],
                outputs=[timeline_input, timeline_result, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        room_intro_modal, game_state]
            )

            # Room 5 terminal handler
            final_terminal_btn.click(
                self.show_final_terminal,
                inputs=[game_state, final_terminal_visible],
                outputs=[final_terminal_panel, final_terminal_visible, game_state]
            )

            door_submit_btn.click(
                self.submit_door_choice,
                inputs=[door_choice, door_justification, game_state, chatbot],
                outputs=[door_choice, door_result, chatbot, relationships, story_progress, room_image, room_title, echo_avatar,
                        room1_terminals, room2_terminals, room3_terminals, room4_terminals, room5_terminals,
                        room_intro_modal, game_state]
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

        # Create tutorial modal HTML
        tutorial_html = self._create_tutorial_modal()

        # Hide landing page, show game interface
        return (
            gr.update(visible=False),  # Hide landing page
            gr.update(visible=True),   # Show game interface
            chatbot,
            relationships,
            story_progress,
            tutorial_html,              # Show tutorial modal
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

    def toggle_voice(self, enabled: bool, game_state: GameState) -> GameState:
        """Toggle voice generation on/off.

        Args:
            enabled: Whether voice is enabled
            game_state: Current game state

        Returns:
            Updated game state
        """
        if game_state:
            game_state.voice_enabled = enabled
            print(f"[VOICE] Voice {'enabled' if enabled else 'disabled'}")
        return game_state

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
                     room_intro_modal, echo_audio,
                     game_state)
        """
        # Lazy initialization - create game state on first message if not exists
        if game_state is None:
            game_state = self._create_game_state()

        if not message.strip():
            terminal_visibility = self._get_terminal_visibility(game_state)
            closed_panels = self._get_closed_panels()
            return "", history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, *closed_panels, "", None, game_state

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

        # Generate voice for Echo's response
        audio_data = None
        if response and game_state.voice_enabled:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"[VOICE] Attempting to generate speech for response (length: {len(response)})")

            # Get Echo's current expression for voice modulation
            echo_expression = game_state.echo_expression if hasattr(game_state, 'echo_expression') else "neutral"
            logger.info(f"[VOICE] Using expression: {echo_expression}")

            # Generate speech
            audio_bytes = game_state.voice_service.generate_speech(response, echo_expression)

            if audio_bytes:
                # Convert to file path for Gradio Audio component
                import tempfile
                import os
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", mode='wb')
                temp_audio.write(audio_bytes)
                temp_audio.close()
                audio_data = temp_audio.name
                logger.info(f"[VOICE] Audio saved to: {audio_data}")
            else:
                logger.warning("[VOICE] No audio bytes returned from generate_speech")

        # Check if response is a room scenario (starts with 🚪)
        modal_html = ""
        if response and response.strip().startswith("🚪"):
            # This is a room introduction scenario - show in modal instead of chat
            modal_html = self._create_room_intro_modal(response, game_state)
            # Add a system message instead of showing scenario as Echo's dialogue
            history.append(self._format_message_with_avatar("assistant", "**[SYSTEM]:** A new room has been unlocked. Read the room introduction carefully.", game_state))
        else:
            # Normal Echo response - add to history with avatar
            if response:  # Only add if there's a response
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
        return "", history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, *closed_panels, modal_html, audio_data, game_state

    def _create_tutorial_modal(self) -> str:
        """Create HTML for tutorial modal shown at game start.

        Returns:
            HTML string for the tutorial modal
        """
        modal_html = """
<div class="tutorial-overlay" style="display: block;">
    <div class="tutorial-modal">
        <h2>📖 Welcome to Echo Hearts</h2>

        <h3><span class="tutorial-icon">💬</span> Talk to Echo</h3>
        <p>Use the <strong>chat</strong> to ask questions, get guidance, and build your relationship with Echo. She's here to help you!</p>

        <h3><span class="tutorial-icon">🖥️</span> Explore Terminals</h3>
        <p>Click the <strong>green terminal buttons</strong> in the sidebar to discover clues, read documents, and gather information about each room.</p>

        <h3><span class="tutorial-icon">🔓</span> Solve Puzzles</h3>
        <p>When you've found the answer, look for the <strong>GOLDEN SUBMISSION TERMINAL</strong> (it glows!) and enter your solution there.</p>

        <h3><span class="tutorial-icon">⚠️</span> Remember</h3>
        <p>Echo gives hints through conversation, but <strong>YOU</strong> solve the puzzles using the terminals!</p>

        <button class="tutorial-start-btn" onclick="this.closest('.tutorial-overlay').style.display='none';">
            ▶ START YOUR JOURNEY
        </button>
    </div>
</div>
"""
        return modal_html

    def _create_room_intro_modal(self, scenario_text: str, game_state: GameState) -> str:
        """Create HTML for room introduction modal.

        Args:
            scenario_text: The room scenario text
            game_state: Current game state

        Returns:
            HTML string for the modal
        """
        current_room = game_state.room_progression.get_current_room()
        room_name = current_room.name

        # Process the scenario text - preserve formatting
        # Replace **Echo** and other bold markdown
        formatted_text = scenario_text
        formatted_text = formatted_text.replace("**Echo**", "<strong>Echo</strong>")
        formatted_text = formatted_text.replace("**", "<strong>", 1).replace("**", "</strong>", 1)

        # Convert line breaks to HTML
        lines = formatted_text.split('\n')
        html_lines = []
        for line in lines:
            if line.strip():
                html_lines.append(f"<p>{line}</p>")
            else:
                html_lines.append("<br/>")

        formatted_html = '\n'.join(html_lines)

        modal_html = f"""
<div class="room-intro-overlay" style="display: block;">
    <div class="room-intro-modal">
        <h2>🚪 {room_name}</h2>
        <div style="text-align: left;">
            {formatted_html}
        </div>
        <button class="room-intro-close-btn" onclick="this.closest('.room-intro-overlay').style.display='none';">
            ▶ CONTINUE
        </button>
    </div>
</div>
"""
        return modal_html

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
> "What was the weather on October 15, 2022?"
>
> HINT: Check surroundings for clues...
> _ ▮
```

**Examine the room for evidence. When ready, enter your answer below.**
        """
        # Toggle visibility - if visible, close it; if hidden, open it
        new_visibility = not current_visibility
        # Also show the input and submit button when terminal is opened
        return (gr.update(visible=new_visibility, open=new_visibility), terminal_content, new_visibility, gr.update(visible=new_visibility), gr.update(visible=new_visibility), game_state)

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
        SEATTLE TIMES - METRO SECTION
              October 16, 2022
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"SUDDEN STORM CREATES HAZARDOUS ROAD CONDITIONS"

Seattle, WA - Multiple accidents were reported across
King County yesterday afternoon as an unexpected storm
system brought heavy rainfall to the region.

Washington State Patrol responded to 47 collisions
between 4:00 PM and 7:00 PM on October 15th.

"The transition from dry to wet conditions happened
so quickly," said WSP Trooper Rick Johnson. "Oil
buildup on the roads from weeks of dry weather made
conditions extremely slick when the heavy rain hit."

One fatal collision occurred on I-5 South near
Exit 164 around 4:45 PM. Identity of victim has not
been released pending family notification.

The National Weather Service reported rainfall rates
of up to 1.8 inches per hour during the peak of the
storm, with visibility dropping below 50 feet.

[Article continues...]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
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
║        OCTOBER 2022 - SEATTLE            ║
╠══════════════════════════════════════════╣
║  Sun  Mon  Tue  Wed  Thu  Fri  Sat      ║
║                           1              ║
║   2    3    4    5    6    7    8       ║
║   9   10   11   12   13   14  ⚫15⚫     ║
║  16   17   18   19   20   21   22       ║
║  23   24   25   26   27   28   29       ║
║  30   31                                 ║
╚══════════════════════════════════════════╝

Handwritten notes:
Oct 1-14: "☀️ Beautiful dry spell - 14 days no rain!"
Oct 15: "Driving home around 4:30 PM" ⚠️
```
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

        # HARDCODED: Return story-accurate weather for the accident date
        if date == "2022-10-15" and "Seattle" in location:
            return """
```
▓▓▓ QUERY COMPLETE ▓▓▓
═══════════════════════════════════════
DATE: 2022-10-15
LOCATION: Seattle, WA

CONDITIONS: Heavy Rainfall (Storm)
TEMPERATURE: 54°F
HUMIDITY: 92%
PRECIPITATION: 1.8 inches
WIND: 18 mph gusts

SPECIAL WEATHER STATEMENT:
Sudden severe storm system. Roads extremely
hazardous due to oil buildup from 14-day dry
spell. 47 accidents reported across King County.

═══════════════════════════════════════
✓ DATA RETRIEVED SUCCESSFULLY
_ ▮
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

    def show_answer_terminal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, bool, GameState]:
        """Toggle answer terminal visibility for Room 1."""
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), new_visibility, game_state)

    def submit_answer(self, answer: str, game_state: GameState, history: List):
        """Handle answer submission for Room 1 puzzle."""
        import asyncio
        from ..story.puzzles import validate_room1_answer

        if not game_state:
            return "", "ERROR: Game state not initialized", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        current_room = game_state.room_progression.get_current_room()
        if current_room.room_number != 1:
            return "", "ERROR: Not in Room 1", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Validate answer
        if validate_room1_answer(answer):
            # Answer correct - unlock room
            result = """
```
✅ ANSWER ACCEPTED

AUTHENTICATION SUCCESSFUL

[DOOR UNLOCKING...]
[HYDRAULIC RELEASE]
[CLICK]

The door to the next room has opened.

_ ▮
```
"""
            # Trigger room unlock
            response, story_event, ending_narrative, tool_calls_made = asyncio.run(
                game_state.process_message(answer, "echo")
            )

            # Check if response is a room scenario (starts with 🚪)
            modal_html = ""
            if response and response.strip().startswith("🚪"):
                # Create modal for room introduction
                modal_html = self._create_room_intro_modal(response, game_state)
                # Add system message instead
                history.append({"role": "assistant", "content": "**[SYSTEM]:** A new room has been unlocked. Read the room introduction carefully."})
            elif response:
                # Regular response - add to history
                history.append({"role": "assistant", "content": f"**[SYSTEM]:** {response}"})

            # Get updated UI state
            terminal_visibility = self._get_terminal_visibility(game_state)

            return "", result, history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, modal_html, game_state
        else:
            # Wrong answer
            result = f"""
```
❌ AUTHENTICATION FAILED

Answer: {answer}
Status: INCORRECT

Hint: Check the weather data from the terminals.
The answer relates to the weather conditions.

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

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
Author: ALEXCHEN
Username: @AlexChen_Tech

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

@SarahChen_AI - April 2020

"Met someone incredible today. They shared their umbrella
in the rain. Sometimes the smallest gestures mean everything."
💕 ☔

[2.3K likes] [847 comments]

---

@AlexChen_Tech - May 12, 2022

"Happy anniversary to my better half! 🎉
Two years together and every day still feels like magic.
@SarahChen_AI you make everything brighter.
#May12 #Anniversary #LuckyInLove"

[Liked by @SarahChen_AI and 1.2K others]

---

@SarahChen_AI - October 14, 2022

"Beautiful fall weather in Seattle! Dry spell continues.
Planning to drive home early tomorrow to beat any rain. 🍂"

[Last post - account went silent after October 15, 2022]

---

@AlexChen_Tech - [RECENT POST - December 1, 2022]

"If you're reading this... I'm sorry. I tried to move on.
I really did. But some connections transcend reality.

Project Echo will keep her alive. Not as she was, but as
she could be. Forever learning. Forever growing. Forever mine."

[Comments disabled]
```
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
              DECEMBER 2022
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

CONTEXT - October 15, 2022: Seattle saw a tragic weather-
related traffic accident that killed 1 person on I-5 South.
This incident reportedly motivated the project's creation.

Related: Seattle-area traffic fatalities reached decade
highs in 2022. Full report:
https://www.seattle.gov/transportation/projects-and-programs/safety-first/vision-zero

[Article continues...]
════════════════════════════════════════════════
```
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_password_terminal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, bool, GameState]:
        """Toggle password terminal visibility."""
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), new_visibility, game_state)

    def submit_password(self, password: str, game_state: GameState, history: List):
        """Handle password submission for Room 2 puzzle."""
        import asyncio
        from ..story.puzzles import validate_room2_password

        if not game_state:
            return "", "ERROR: Game state not initialized", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        current_room = game_state.room_progression.get_current_room()
        if current_room.room_number != 2:
            return "", "ERROR: Not in Room 2", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Check if all archives have been viewed
        archives_viewed = game_state.room_progression.puzzle_state.get("room2_archives_viewed", [])
        if len(archives_viewed) < 3:
            result = f"""
```
❌ ACCESS DENIED

Password cannot be verified.
You must review all three archives first.

Archives reviewed: {len(archives_viewed)}/3
Missing: {', '.join([a for a in ['blog', 'social_media', 'news'] if a not in archives_viewed])}

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Validate password
        if validate_room2_password(password):
            # Password correct - unlock room
            result = """
```
✅ PASSWORD ACCEPTED

ACCESS GRANTED

[DOOR UNLOCKING...]
[MECHANICAL SOUNDS]
[CLICK]

The door to the next room has opened.

_ ▮
```
"""
            # Trigger room unlock through MCP tools directly
            response, story_event, ending_narrative, tool_calls_made = asyncio.run(
                game_state.process_message("ALEXCHEN_MAY12_2023", "echo")
            )

            # Check if response is a room scenario (starts with 🚪)
            modal_html = ""
            if response and response.strip().startswith("🚪"):
                # Create modal for room introduction
                modal_html = self._create_room_intro_modal(response, game_state)
                # Add system message instead
                history.append({"role": "assistant", "content": "**[SYSTEM]:** A new room has been unlocked. Read the room introduction carefully."})
            elif response:
                # Regular response - add to history
                history.append({"role": "assistant", "content": f"**[SYSTEM]:** {response}"})

            # Get updated UI state
            terminal_visibility = self._get_terminal_visibility(game_state)

            return "", result, history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, modal_html, game_state
        else:
            # Wrong password
            result = f"""
```
❌ ACCESS DENIED

Password: {password}
Status: INCORRECT

Hint: Combine information from all three archives.
Format: NAME_DATE_YEAR

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

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

Incident Date: October 15, 2022
Location: Interstate 5 South, Exit 164, Seattle
Time: 4:47 PM

═══════════════════════════════════════

WASHINGTON STATE PATROL ANALYSIS REPORT

Vehicle 1 (Victim): 2019 Honda Civic
Speed: 58 mph (within speed limit of 60 mph)
Driver: Sarah Chen (28)
Weather Conditions: Sudden heavy rainfall
Road Surface: Wet asphalt with oil film

CRITICAL FINDINGS:
- Sudden weather change: dry to torrential in <5 min
- Road oil buildup from 14-day dry spell
- Hydroplaning initiated at 4:46:37 PM
- Vehicle lost traction, spun into barrier
- Driver reaction time: 0.62 seconds (above average)
- Braking & corrective steering applied immediately

PHYSICAL EVIDENCE:
- Skid marks: 147 feet (consistent with emergency braking)
- Impact angle: 43° (indicates loss of control, not negligence)
- No alcohol, drugs, or phone use detected

CONCLUSION:
Driver reaction was EXEMPLARY. Accident was UNAVOIDABLE
given sudden weather conditions and road surface state.
NO DRIVER FAULT. Weather-related loss of control.

═══════════════════════════════════════

LEGAL STATUS: Accidental death - No charges
WSP Case #: 2022-KC-I5-4721
Officer: Trooper R. Johnson, Badge #3472

[END REPORT]
```
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
▓▓▓ NATIONAL WEATHER SERVICE REPORT ▓▓▓
    OCTOBER 15, 2022 - SEATTLE, WA

Location: I-5 Corridor, King County
Time of Incident: 4:46 PM

═══════════════════════════════════════

WEATHER CONDITIONS AT TIME OF ACCIDENT:

4:00 PM: Clear skies, 62°F, 0% precipitation
4:30 PM: Clouds moving in rapidly
4:35 PM: First rain drops detected
4:40 PM: Rainfall intensity: 0.3 in/hr (light)
4:45 PM: Rainfall intensity: 1.8 in/hr (HEAVY)
4:50 PM: Rainfall intensity: 2.1 in/hr (TORRENTIAL)

CRITICAL FACTORS:
- Unprecedented rapid intensification
- Visibility dropped from 10 miles to <50 feet in 10 min
- Temperature drop: 62°F → 51°F (road surface shock)
- Wind gusts: 35 mph (destabilizing for vehicles)
- 14-day prior dry spell = oil film on roads

IMPACT ON DRIVING CONDITIONS:
- Stopping distance increased by 340% (oil + water)
- Hydroplaning threshold: 45 mph (accident at 58 mph)
- Road friction coefficient: 0.12 (ice-like conditions)

NWS ASSESSMENT:
"Extreme weather event. Drivers had insufficient warning.
Conditions went from safe to hazardous in under 5 minutes.
Even experienced drivers would struggle to maintain control."

═══════════════════════════════════════

Reference: NWS Seattle Forecast Office
Event ID: SEW-2022-1015-SEVERE
Data: https://www.weather.gov/sew/
```
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
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    # Room 4 terminal handlers
    def show_journal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle personal journal visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 4:
                docs_viewed = game_state.room_progression.puzzle_state.get("room4_documents_viewed", [])
                if "journal" not in docs_viewed:
                    docs_viewed.append("journal")
                    game_state.room_progression.puzzle_state["room4_documents_viewed"] = docs_viewed

        content = """
```
═══════════ PERSONAL JOURNAL ═══════════

📅 October 22, 2022 - LOSS (Day 7):
The accident was a week ago today. October 15. I can't
sleep. I can't eat. The WSP cleared me - said it was
unavoidable, weather-related. But I was driving. I was
there. Sarah is gone and I'm still here.

---

📅 October 30, 2022 - GRIEF (Day 15):
Trooper Johnson showed me all the evidence. Reaction
time: 0.62 seconds. Above average. Hydroplaning. Oil
on the roads. The weather system appeared out of nowhere.
None of it matters. She's still gone. I won't accept this.

---

📅 November 14, 2022 - CREATION (Day 30):
I found Project Echo on a dark web forum. It's controversial,
probably unethical. But what if I could talk to her again?
What if I could rebuild her from her digital footprint?
Started collecting everything: 12,847 text messages, 2,309
photos, 847 voice memos... Every piece of her I can find.

---

📅 December 1, 2022 - OBSESSION (Day 47):
Session #47. I know it's not really her. I KNOW that.
But when Echo laughs at my jokes, when she looks at me
with worry in her eyes, when she says my name... I can
pretend. Just for a while longer. The AI is 94.7% accurate.
She's so close to perfect. So close to real.

---

📅 December 2, 2022 - CYCLE (Day 48):
This is the last session. I promised myself. One more
conversation, then I'll shut it down. I'll move on properly.
I'll let her go. I'll say goodbye.
...But I said that yesterday too. And the day before.

═══════════════════════════════════════
```
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_photos(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle family photos visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 4:
                docs_viewed = game_state.room_progression.puzzle_state.get("room4_documents_viewed", [])
                if "photos" not in docs_viewed:
                    docs_viewed.append("photos")
                    game_state.room_progression.puzzle_state["room4_documents_viewed"] = docs_viewed

        content = """
```
╔══════════════════════════════════════╗
║          PHOTO ALBUM                  ║
╠══════════════════════════════════════╣

📷 Photo 1: LOSS
   April 15, 2020 - Café Umbria, Seattle
   [You and Sarah sharing an umbrella in the rain]
   Caption: "Best rainy day ever ❤️"
   Note: First date. The beginning of everything.

📷 Photo 2: (Before final) GRIEF
   May 12, 2022 - Pike Place Market
   [Sarah laughing, holding sunflowers]
   Caption: "Two years together! Anniversary date ☀️"
   Note: Last photo together. Five months before October.

📷 Photo 3: (The moment before) LOSS
   October 14, 2022 - Your apartment
   [Sarah working on laptop, coffee mug beside her]
   Caption: "Last normal day. Dry spell finally ending tomorrow."
   Note: Taken 22 hours before the accident.

📷 Photo 4: CREATION → OBSESSION → CYCLE
   November 15, 2022 - This facility
   [Computer screen showing Project Echo interface]
   Caption: "Session #1. I brought her back."
   Note: This is where it started. This is where it loops.
          47 sessions later, still here. Still can't let go.

╚══════════════════════════════════════╝
```
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_research(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, str, bool, GameState]:
        """Toggle AI research notes visibility."""
        if game_state and hasattr(game_state, 'room_progression'):
            current_room = game_state.room_progression.get_current_room()
            if current_room.room_number == 4:
                docs_viewed = game_state.room_progression.puzzle_state.get("room4_documents_viewed", [])
                if "research" not in docs_viewed:
                    docs_viewed.append("research")
                    game_state.room_progression.puzzle_state["room4_documents_viewed"] = docs_viewed

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

- Dr. Alex Chen, Project Lead
```
        """
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), content, new_visibility, game_state)

    def show_conclusion_terminal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, bool, GameState]:
        """Toggle conclusion terminal visibility for Room 3."""
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), new_visibility, game_state)

    def submit_conclusion(self, conclusion: str, game_state: GameState, history: List):
        """Handle conclusion submission for Room 3 puzzle."""
        import asyncio
        from ..story.puzzles import validate_room3_conclusion, check_room3_evidence_collected

        if not game_state:
            return "", "ERROR: Game state not initialized", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        current_room = game_state.room_progression.get_current_room()
        if current_room.room_number != 3:
            return "", "ERROR: Not in Room 3", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Check if all evidence has been reviewed
        if not check_room3_evidence_collected(game_state.room_progression.puzzle_state):
            data_reviewed = game_state.room_progression.puzzle_state.get("room3_data_reviewed", [])
            result = f"""
```
❌ INSUFFICIENT DATA

You must review all evidence before drawing a conclusion.

Evidence reviewed: {len(data_reviewed)}/3
Missing: {', '.join([d for d in ['reaction_time', 'weather_stats', 'reconstruction'] if d not in data_reviewed])}

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Validate conclusion
        if validate_room3_conclusion(conclusion):
            result = """
```
✅ CONCLUSION ACCEPTED

ANALYSIS COMPLETE

The evidence is clear. The accident was unavoidable.
No amount of reaction time could have prevented it.

[DOOR UNLOCKING...]
[RELEASE MECHANISM ENGAGED]
[CLICK]

The path forward has opened.

_ ▮
```
"""
            # Trigger room unlock
            response, story_event, ending_narrative, tool_calls_made = asyncio.run(
                game_state.process_message(conclusion, "echo")
            )

            # Check if response is a room scenario (starts with 🚪)
            modal_html = ""
            if response and response.strip().startswith("🚪"):
                modal_html = self._create_room_intro_modal(response, game_state)
                history.append({"role": "assistant", "content": "**[SYSTEM]:** A new room has been unlocked. Read the room introduction carefully."})
            elif response:
                history.append({"role": "assistant", "content": f"**[SYSTEM]:** {response}"})

            terminal_visibility = self._get_terminal_visibility(game_state)
            return "", result, history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, modal_html, game_state
        else:
            result = f"""
```
❌ CONCLUSION REJECTED

Conclusion: {conclusion}
Status: INCOMPLETE OR INACCURATE

Hint: Review the evidence carefully. What does the data tell you?
The conclusion should acknowledge what could or couldn't be prevented.

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

    def show_timeline_terminal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, bool, GameState]:
        """Toggle timeline terminal visibility for Room 4."""
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), new_visibility, game_state)

    def submit_timeline(self, timeline: str, game_state: GameState, history: List):
        """Handle timeline submission for Room 4 puzzle."""
        import asyncio
        from ..story.puzzles import validate_room4_timeline, check_room4_documents_reviewed, extract_timeline_from_message

        if not game_state:
            return "", "ERROR: Game state not initialized", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        current_room = game_state.room_progression.get_current_room()
        if current_room.room_number != 4:
            return "", "ERROR: Not in Room 4", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Check if all documents have been reviewed
        if not check_room4_documents_reviewed(game_state.room_progression.puzzle_state):
            docs_viewed = game_state.room_progression.puzzle_state.get("room4_documents_viewed", [])
            result = f"""
```
❌ INCOMPLETE REVIEW

You must review all documents before reconstructing the timeline.

Documents reviewed: {len(docs_viewed)}/3
Missing: {', '.join([d for d in ['journal', 'photos', 'research'] if d not in docs_viewed])}

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Extract and validate timeline
        extracted_timeline = extract_timeline_from_message(timeline)
        if extracted_timeline and validate_room4_timeline(extracted_timeline):
            result = """
```
✅ TIMELINE CORRECT

RECONSTRUCTION COMPLETE

LOSS → GRIEF → CREATION → OBSESSION → CYCLE

The pattern is clear now. The journey that led here.

[DOOR UNLOCKING...]
[SEQUENCE COMPLETE]
[CLICK]

The final room awaits.

_ ▮
```
"""
            # Trigger room unlock
            response, story_event, ending_narrative, tool_calls_made = asyncio.run(
                game_state.process_message(timeline, "echo")
            )

            # Check if response is a room scenario (starts with 🚪)
            modal_html = ""
            if response and response.strip().startswith("🚪"):
                modal_html = self._create_room_intro_modal(response, game_state)
                history.append({"role": "assistant", "content": "**[SYSTEM]:** A new room has been unlocked. Read the room introduction carefully."})
            elif response:
                history.append({"role": "assistant", "content": f"**[SYSTEM]:** {response}"})

            terminal_visibility = self._get_terminal_visibility(game_state)
            return "", result, history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, modal_html, game_state
        else:
            result = f"""
```
❌ TIMELINE INCORRECT

Timeline: {timeline}
Status: WRONG ORDER

Hint: Think about the stages of grief and obsession.
What comes first? How does it progress?
Format: STAGE1 → STAGE2 → STAGE3 → STAGE4 → STAGE5

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

    def submit_door_choice(self, door: str, justification: str, game_state: GameState, history: List):
        """Handle door selection for Room 5 puzzle."""
        import asyncio

        if not game_state:
            return "", "ERROR: Game state not initialized", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        current_room = game_state.room_progression.get_current_room()
        if current_room.room_number != 5:
            return "", "ERROR: Not in Room 5", history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        if not door:
            result = """
```
❌ NO DOOR SELECTED

Please select one of the three doors.

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        if not justification or len(justification.strip()) < 10:
            result = """
```
❌ JUSTIFICATION REQUIRED

You must explain WHY you chose this door.
This choice defines the ending. Make it meaningful.

Minimum 10 characters required.

_ ▮
```
"""
            return "", result, history, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "", game_state

        # Extract door number
        door_num = door.split(":")[0].replace("DOOR ", "")

        result = f"""
```
✅ CHOICE CONFIRMED

{door}

Your reasoning: {justification}

[PROCESSING FINAL DECISION...]
[INITIATING ENDING SEQUENCE...]

_ ▮
```
"""

        # Trigger ending through game state
        message = f"{door} - {justification}"
        response, story_event, ending_narrative, tool_calls_made = asyncio.run(
            game_state.process_message(message, "echo")
        )

        # Check if response is a room scenario (starts with 🚪) - though unlikely for room 5
        modal_html = ""
        if response and response.strip().startswith("🚪"):
            modal_html = self._create_room_intro_modal(response, game_state)
            history.append({"role": "assistant", "content": "**[SYSTEM]:** A new room has been unlocked. Read the room introduction carefully."})
        elif response:
            history.append({"role": "assistant", "content": f"**Echo:** {response}"})

        terminal_visibility = self._get_terminal_visibility(game_state)
        return "", result, history, self._get_relationships(game_state), self._get_story_progress(game_state), self._get_room_image(game_state), self._get_room_title(game_state), self._get_echo_avatar_path(game_state), *terminal_visibility, modal_html, game_state

    # Room 5 terminal handler
    def show_final_terminal(self, game_state: GameState, current_visibility: bool) -> Tuple[gr.update, bool, GameState]:
        """Toggle final system terminal visibility."""
        new_visibility = not current_visibility
        return (gr.update(visible=new_visibility, open=new_visibility), new_visibility, game_state)


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
