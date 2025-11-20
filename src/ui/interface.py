"""Main Gradio interface for Echo Hearts."""

import gradio as gr
import asyncio
from typing import List, Tuple, Optional
from ..game_state import GameState


class EchoHeartsUI:
    """Main UI interface for the game."""

    def __init__(self, session_id: str = "default"):
        """Initialize the UI.

        Args:
            session_id: Session identifier
        """
        self.game_state = GameState(session_id)
        self.current_companion = "echo"  # Default active companion

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title="Echo Hearts", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 💕 Echo Hearts")
            gr.Markdown("*An AI Companion RPG with Emergent Relationships*")

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
                    gr.Markdown("### Active Companions")
                    companion_selector = gr.Radio(
                        choices=["echo", "shadow"],
                        value="echo",
                        label="Talk to:",
                        interactive=True
                    )
                    companion_list = gr.Markdown(self._get_companion_list())

                    gr.Markdown("### Relationships")
                    relationships = gr.Markdown(self._get_relationships())

                    with gr.Accordion("Session", open=False):
                        session_id = gr.Textbox(label="Session ID", value="default")
                        with gr.Row():
                            save_btn = gr.Button("Save", size="sm")
                            load_btn = gr.Button("Load", size="sm")

            # Event handlers
            companion_selector.change(
                self.change_companion,
                inputs=[companion_selector],
                outputs=[]
            )

            msg_input.submit(
                self.handle_message,
                inputs=[msg_input, chatbot, companion_selector],
                outputs=[msg_input, chatbot, companion_list, relationships]
            )

            send_btn.click(
                self.handle_message,
                inputs=[msg_input, chatbot, companion_selector],
                outputs=[msg_input, chatbot, companion_list, relationships]
            )

            save_btn.click(
                self.save_session,
                inputs=[session_id],
                outputs=[gr.Markdown()]
            )

            load_btn.click(
                self.load_session,
                inputs=[session_id],
                outputs=[chatbot, companion_list, relationships]
            )

        return interface

    def change_companion(self, companion_id: str):
        """Change the active companion.

        Args:
            companion_id: ID of the companion to switch to
        """
        self.current_companion = companion_id

    def handle_message(
        self,
        message: str,
        history: List[dict],
        companion_id: str
    ) -> Tuple[str, List[dict], str, str]:
        """Handle incoming message from user.

        Args:
            message: User's message
            history: Chat history
            companion_id: Active companion ID

        Returns:
            Tuple of (empty input, updated history, companion list, relationships)
        """
        if not message.strip():
            return "", history, self._get_companion_list(), self._get_relationships()

        # Add user message to history
        history.append({"role": "user", "content": message})

        # Process message through game state (async)
        response = asyncio.run(self.game_state.process_message(message, companion_id))

        # Get companion name
        companion = self.game_state.companions.get(companion_id)
        companion_name = companion.name if companion else "Companion"

        # Add response to history
        history.append({"role": "assistant", "content": f"**{companion_name}:** {response}"})

        return "", history, self._get_companion_list(), self._get_relationships()

    def save_session(self, session_id: str) -> str:
        """Save current session.

        Args:
            session_id: Session identifier

        Returns:
            Status message
        """
        success = self.game_state.save_game()
        return f"✅ Session saved: {session_id}" if success else f"❌ Failed to save session"

    def load_session(
        self,
        session_id: str
    ) -> Tuple[List[dict], str, str]:
        """Load a saved session.

        Args:
            session_id: Session identifier

        Returns:
            Tuple of (chat history, companion list, relationships)
        """
        success = self.game_state.load_game(session_id)
        if not success:
            return [], self._get_companion_list(), self._get_relationships()

        # Rebuild chat history from conversation
        history = []
        for msg in self.game_state.conversation.messages:
            role = "user" if msg["speaker"] == "User" else "assistant"
            content = msg["content"] if role == "user" else f"**{msg['speaker']}:** {msg['content']}"
            history.append({"role": role, "content": content})

        return history, self._get_companion_list(), self._get_relationships()

    def _get_companion_list(self) -> str:
        """Get formatted list of active companions.

        Returns:
            Markdown formatted companion list
        """
        companions = self.game_state.get_companion_list()
        if not companions:
            return "*No companions available*"

        lines = []
        for comp in companions:
            lines.append(f"**{comp['name']}** (`{comp['id']}`)")

        return "\n".join(lines)

    def _get_relationships(self) -> str:
        """Get formatted relationship status.

        Returns:
            Markdown formatted relationships
        """
        relationships = self.game_state.get_relationships_summary()
        if not relationships:
            return "*No relationships yet*"

        lines = []
        for companion_id, affinity in relationships.items():
            companion = self.game_state.companions.get(companion_id)
            if companion:
                description = self.game_state.relationships.get_relationship_description(affinity)
                lines.append(f"**{companion.name}:** {description} ({affinity:+.2f})")

        return "\n".join(lines)


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
