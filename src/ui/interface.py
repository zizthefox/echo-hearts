"""Main Gradio interface for Echo Hearts."""

import gradio as gr
import asyncio
import uuid
from typing import List, Tuple, Optional
from ..game_state import GameState


class EchoHeartsUI:
    """Main UI interface for the game."""

    def __init__(self):
        """Initialize the UI (no shared state)."""
        pass

    def _create_game_state(self):
        """Create a new game state with unique session ID.

        Returns:
            New GameState instance
        """
        session_id = str(uuid.uuid4())[:8]  # Short unique ID
        return GameState(session_id)

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title="Echo Hearts", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 💕 Echo Hearts")
            gr.Markdown("*An AI Companion RPG with Emergent Relationships*")

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
                    gr.Markdown("### Active Companions")
                    companion_selector = gr.Radio(
                        choices=["echo", "shadow"],
                        value="echo",
                        label="Talk to:",
                        interactive=True
                    )
                    companion_list = gr.Markdown()

                    gr.Markdown("### Relationships")
                    relationships = gr.Markdown()

                    gr.Markdown("### Story Progress")
                    story_progress = gr.Markdown()

                    gr.Markdown("---")
                    gr.Markdown("*💡 Each browser session starts a new story*")

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

            # Initialize sidebar on load
            interface.load(
                self.initialize_ui,
                inputs=[game_state],
                outputs=[companion_list, relationships, story_progress, game_state]
            )

        return interface

    def initialize_ui(self, game_state: GameState) -> Tuple[str, str, str, GameState]:
        """Initialize UI with fresh game state data.

        Args:
            game_state: The session's game state (may be None on first load)

        Returns:
            Tuple of (companion_list, relationships, story_progress, game_state)
        """
        # Lazy initialization - create game state if not exists
        if game_state is None:
            game_state = self._create_game_state()

        return (
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
        return game_state.story.get_progress_summary()


def launch_interface():
    """Launch the Gradio interface."""
    ui = EchoHeartsUI()
    interface = ui.create_interface()
    interface.launch()
