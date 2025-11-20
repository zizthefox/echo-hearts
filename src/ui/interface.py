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

                    gr.Markdown("---")
                    gr.Markdown("*💡 Memories persist during your session only*")

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
