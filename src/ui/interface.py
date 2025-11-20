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

                    gr.Markdown("### Story Progress")
                    story_progress = gr.Markdown(self._get_story_progress())

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
                outputs=[msg_input, chatbot, companion_list, relationships, story_progress]
            )

            send_btn.click(
                self.handle_message,
                inputs=[msg_input, chatbot, companion_selector],
                outputs=[msg_input, chatbot, companion_list, relationships, story_progress]
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
    ) -> Tuple[str, List[dict], str, str, str]:
        """Handle incoming message from user.

        Args:
            message: User's message
            history: Chat history
            companion_id: Active companion ID

        Returns:
            Tuple of (empty input, updated history, companion list, relationships, story progress)
        """
        if not message.strip():
            return "", history, self._get_companion_list(), self._get_relationships(), self._get_story_progress()

        # Add user message to history
        history.append({"role": "user", "content": message})

        # Process message through game state (async) - returns (response, event, ending, tool_calls)
        response, story_event, ending_narrative, tool_calls_made = asyncio.run(
            self.game_state.process_message(message, companion_id)
        )

        # Get companion name
        companion = self.game_state.companions.get(companion_id)
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

        # Add story event if triggered
        if story_event:
            history.append({
                "role": "assistant",
                "content": f"---\n\n**📖 {story_event.description}**\n\n*{story_event.narrative}*\n\n---"
            })

        # Add ending if reached
        if ending_narrative:
            history.append({
                "role": "assistant",
                "content": ending_narrative
            })

        return "", history, self._get_companion_list(), self._get_relationships(), self._get_story_progress()

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

    def _get_story_progress(self) -> str:
        """Get story progress summary.

        Returns:
            Markdown formatted story progress
        """
        return self.game_state.story.get_progress_summary()


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
