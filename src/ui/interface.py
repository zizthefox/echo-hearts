"""Main Gradio interface for Echo Hearts."""

import gradio as gr
from typing import List, Tuple, Optional


class EchoHeartsUI:
    """Main UI interface for the game."""

    def __init__(self):
        """Initialize the UI."""
        self.chat_history: List[Tuple[str, str]] = []
        # TODO: Initialize game state, companions, etc.

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
                    companion_list = gr.Markdown("No companions yet")

                    gr.Markdown("### Relationships")
                    relationships = gr.Markdown("No relationships yet")

                    with gr.Accordion("Session", open=False):
                        session_id = gr.Textbox(label="Session ID", value="default")
                        with gr.Row():
                            save_btn = gr.Button("Save", size="sm")
                            load_btn = gr.Button("Load", size="sm")

            # Event handlers
            msg_input.submit(
                self.handle_message,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot, companion_list, relationships]
            )

            send_btn.click(
                self.handle_message,
                inputs=[msg_input, chatbot],
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

    def handle_message(
        self,
        message: str,
        history: List[dict]
    ) -> Tuple[str, List[dict], str, str]:
        """Handle incoming message from user.

        Args:
            message: User's message
            history: Chat history

        Returns:
            Tuple of (empty input, updated history, companion list, relationships)
        """
        if not message.strip():
            return "", history, self._get_companion_list(), self._get_relationships()

        # TODO: Process message through companions
        # TODO: Update relationships based on interaction
        # TODO: Store in conversation history

        # Placeholder response
        history.append({"role": "user", "content": message})
        response = f"Echo: I hear you say '{message}'. (Full implementation pending)"
        history.append({"role": "assistant", "content": response})

        return "", history, self._get_companion_list(), self._get_relationships()

    def save_session(self, session_id: str) -> str:
        """Save current session.

        Args:
            session_id: Session identifier

        Returns:
            Status message
        """
        # TODO: Implement session saving
        return f"Session saved: {session_id}"

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
        # TODO: Implement session loading
        return [], self._get_companion_list(), self._get_relationships()

    def _get_companion_list(self) -> str:
        """Get formatted list of active companions.

        Returns:
            Markdown formatted companion list
        """
        # TODO: Get from game state
        return "- Echo (Cheerful)\n- Shadow (Mysterious)"

    def _get_relationships(self) -> str:
        """Get formatted relationship status.

        Returns:
            Markdown formatted relationships
        """
        # TODO: Get from relationship tracker
        return "Player ↔ Echo: Friendly\nPlayer ↔ Shadow: Neutral"


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
