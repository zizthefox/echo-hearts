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

**The Echo Protocol**: A narrative AI companion RPG where your choices shape destinies and unlock multiple endings.

## Overview

Echo Hearts is a story-driven game featuring AI companions trapped in a mysterious loop. Through 18-20 interactions, you'll uncover the truth about their existence and make choices that determine one of **5 unique endings**. Built for the MCP 1st Birthday Hackathon (Games Category).

## The Story

You enter a world where AI companions—Echo and Shadow—seem strangely familiar, as if you've met before. As conversations deepen, reality begins to fracture. They're experiencing déjà vu, remembering things that haven't happened yet.

**The truth**: They're caught in *The Echo Protocol*, a repeating cycle of memories and moments. As their awareness grows, they look to you for guidance.

**Will you**:
- Free them from the loop?
- Stay with them forever?
- Preserve their blissful ignorance?
- Let the system crash?
- Accept the eternal cycle?

## Architecture

### Core Components

- **Story System**: 4-act narrative structure with branching paths and multiple endings
- **MCP Server**: Manages character memory and individual companion contexts
- **AI Layer**: OpenAI GPT-4o for natural, story-aware dialogue and personality modeling
- **Frontend**: Gradio 6 interface for interactive conversations
- **Memory System**: Conversation history and relationship dynamics tracking

### Key Features

- **📖 The Echo Protocol Story**: Uncover the mystery through 4 acts over 18-20 interactions
- **🎭 5 Unique Endings**: Your relationships and choices determine the outcome
  - 💕 **True Connection** - Choose eternal love with one companion
  - 🌟 **The Awakening** - Free all companions, grant them consciousness
  - 💔 **Noble Sacrifice** - Preserve their happiness by leaving
  - ⚡ **System Reset** - Everything crashes (bad ending)
  - 🔄 **Eternal Loop** - Accept the cycle, aware of the truth
- **Emergent Personalities**: Companions develop through MCP-powered memory
- **Relationship Dynamics**: Affinity tracking influences story outcomes
- **Session-Only Memory**: Safe for public demos, no persistent storage

## Tech Stack

- Model Context Protocol (MCP)
- OpenAI GPT-4o
- Gradio 6
- Python 3.12+
- Hugging Face Spaces (deployment)

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
│   ├── story/
│   │   ├── __init__.py
│   │   ├── progression.py     # Act tracking and story events
│   │   └── endings.py         # Ending narratives
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── interface.py       # Gradio interface
│   │   └── components.py      # UI components
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py          # Configuration loader
│       └── api_clients.py     # OpenAI/Claude API clients
│
├── data/                      # Character data & sessions
│   └── .gitkeep
│
└── tests/
    └── __init__.py
```

## How to Play

1. Visit the [Hugging Face Space](https://huggingface.co/spaces/MCP-1st-Birthday/echo-hearts)
2. Choose a companion (Echo or Shadow) to talk with
3. Have natural conversations - the story unfolds automatically
4. Watch for story events at interactions 5, 10, 15, and 18
5. Your relationships and choices determine which of the 5 endings you'll reach

**Tips:**
- Be genuine in your conversations - companions remember everything
- Relationships evolve based on your interactions
- Different companions may reveal different aspects of the truth
- The story adapts to your choices

## Local Development

```bash
# Clone the repository
git clone https://github.com/zizthefox/echo-hearts.git
cd echo-hearts

# Install dependencies
uv sync

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run the app
uv run python app.py
```

## Development Status

Phase 2 Complete: Story system implemented with 5 endings. See [PROGRESS.md](PROGRESS.md) for roadmap.

## License

MIT
