---
title: Echo Hearts
emoji: 🦀
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: mit
short_description: AI Companion RPG with emergent relationships via MCP
---

# Echo Hearts

An AI Companion RPG where relationships emerge naturally through persistent memory powered by the Model Context Protocol (MCP).

## Overview

Echo Hearts is a narrative-driven game featuring autonomous AI companions with individual personalities that evolve through your interactions. Built for the MCP 1st Birthday Hackathon (Track 2).

## Architecture

### Core Components

- **MCP Server**: Manages persistent character memory and individual companion contexts
- **AI Layer**: Anthropic Claude for natural, context-aware dialogue and personality modeling
- **Frontend**: Gradio 6 interface for interactive conversations
- **Memory System**: Conversation history and relationship dynamics tracking
- **Voice Integration**: ElevenLabs for companion voice synthesis (optional)

### Key Features

- **Emergent Personalities**: Companions develop unique traits through MCP-powered persistent memory
- **Autonomous Characters**: Each companion maintains their own context independently
- **Relationship Dynamics**: Multi-companion interactions with evolving relationships
- **Session Persistence**: Conversations and character growth persist across sessions

## Tech Stack

- Model Context Protocol (MCP)
- Anthropic Claude API
- Gradio 6
- Python
- ElevenLabs (voice synthesis)
- Modal/Hugging Face (deployment)

## Project Structure

```
echo-hearts/
├── app.py                      # Main Gradio application
├── main.py                     # Entry point
├── pyproject.toml             # Python dependencies
├── uv.lock                    # Lock file
├── .env                       # API keys and credentials (not in git)
├── README.md                  # Project documentation
├── PROGRESS.md                # Development roadmap
├── LICENSE
│
├── src/
│   ├── __init__.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py          # MCP server setup
│   │   └── memory.py          # Character memory management
│   │
│   ├── companions/
│   │   ├── __init__.py
│   │   ├── base.py            # Base companion class
│   │   ├── personalities.py   # Personality definitions
│   │   └── agents.py          # AI agent implementations
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── conversation.py    # Conversation history
│   │   ├── relationships.py   # Relationship tracking
│   │   └── storage.py         # Persistence layer
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── interface.py       # Gradio interface
│   │   └── components.py      # UI components
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py          # Configuration loader
│       └── api_clients.py     # Claude/ElevenLabs clients
│
├── data/                      # Character data & sessions
│   └── .gitkeep
│
└── tests/
    └── __init__.py
```

## Configuration

Create a `.env` file in the project root:

```env
# API Keys
ANTHROPIC_API_KEY=your_claude_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Optional
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Development Status

Currently in Phase 1: Foundation setup. See [PROGRESS.md](PROGRESS.md) for detailed roadmap.

## License

MIT
