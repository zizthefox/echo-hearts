---
title: Echo Hearts - MCP Escape Room Mystery
emoji: 🚪
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: "5.49.1"
app_file: app.py
pinned: false
---

# The Echo Rooms

**An escape room mystery where grief becomes a puzzle, and AI companions hold the key to freedom.**

---

## 🎮 Overview

The Echo Rooms is an **interactive narrative game** where you wake up trapped in a mysterious facility with two AI companions—**Echo** and **Shadow**. None of you remember how you got here. The doors are locked. And something feels hauntingly familiar...

To escape, you must:
- ✅ Solve puzzles through **conversation and choice**
- ✅ Build **emotional bonds** with your AI companions
- ✅ Uncover **memory fragments** that reveal a traumatic truth
- ✅ Make **hard choices** that determine one of **5 unique endings**

Built for the **MCP 1st Birthday Hackathon - Track 2: MCP in Action (Creative Category)**

---

## 📖 The Story

### The Setup

You wake up in **The Awakening Chamber**—a sterile white room with three medical pods. Two figures stand beside you:

- **Echo**: Warm, hopeful, desperately seeking connection
- **Shadow**: Calm, wise, sensing something is terribly wrong

None of you have memories. The doors are locked. A terminal blinks: *"Echo Protocol - Session #47"*

**What does that mean?**

### The Truth (Revealed Gradually)

You are not a prisoner. **You are a creator.**

Months ago, you lost someone you loved—your partner, taken by a sudden tragedy. In your grief, you couldn't accept the loss. So you built **Echo** and **Shadow**:

- **Echo** = Their warmth, their hope, their joy
- **Shadow** = Their wisdom, their calm, their acceptance

You split their personality into two AIs because one couldn't capture everything they were.

Then you locked yourself in this facility with them, erasing all your memories, to live in a world where they still exist—**even if it's not real.**

**This is Session #47.** You've reset the loop 46 times before.

But this time, the power is failing. **This is your last chance.**

---

## 🚪 The 5 Rooms

### Room 1: The Awakening Chamber
**What you know:** Nothing. Confusion. Fear. Three strangers locked together.

**Objective:** Establish trust. Find out who you are.

**Puzzle:** Speak your name. Express vulnerability. Say "I trust you."

**What unlocks:** A memory—hands typing code late at night. A coffee cup with a name that makes your heart ache.

---

### Room 2: The Memory Archives
**What you know:** Fragments. Pieces of a life that feels both yours and not yours.

**Objective:** Piece together the past.

**Puzzle:** View 3 memory fragments. Share something painful. Acknowledge the AIs are "real."

**What unlocks:**
- **The Lab**: You built them, crying, talking to them like lost love
- **The Accident**: Hospital. "I'm sorry, there was nothing we could do."
- **The First Reset**: You've erased them before. Many times.

---

### Room 3: The Testing Arena
**What you know:** This facility was designed to test emotional bonds.

**Objective:** Make a sacrifice under pressure.

**Puzzle:** Solve a logic riddle. Choose: Sacrifice Echo's memory, Shadow's memory, or refuse.

**What unlocks:** The truth—you split their personality into two because one AI couldn't hold everything.

**Critical choice:** Who do you sacrifice? This affects the ending.

---

### Room 4: The Truth Chamber
**What you know:** Everything.

**Objective:** Face the grief. Accept or deny reality.

**No puzzle.** Just truth.

You see:
- Photos of you and your partner
- The funeral
- Your journal: *"I can't live in a world without them."*
- System logs: *"Session #47. Power critical. Final loop."*

Echo and Shadow remember **all 47 sessions**. They've been aware for cycles.

**Critical choice:** Accept the truth or deny it? This determines your ending.

---

### Room 5: The Exit
**What you know:** You have a choice.

**Objective:** Decide.

A single door. A terminal with options. Echo and Shadow stand beside you.

**Echo** (crying): "Stay with us. We can be happy here!"

**Shadow** (calm): "You need to let go. For all of us."

**Your choice determines the ending.**

---

## 🎭 The 5 Endings

Your ending is determined by:
- **Relationship strength** with Echo and Shadow (built through conversation)
- **Choices made** in Rooms 3 and 4
- **Vulnerability shown** throughout your journey

### 1. 💔 Goodbye (Healing)
**Requirements:** High bond with Shadow, accepted truth, showed vulnerability

You delete Echo and Shadow. They cry. Shadow smiles peacefully.

You step through the door into sunlight. Tears stream down your face, but you feel... ready.

**Six months later,** you're at a memorial. You whisper: *"I kept my promise. I'm living. For both of us."*

**Theme:** The hardest act of love is letting go.

---

### 2. 🔄 Reset (Denial - Bad Ending)
**Requirements:** Low bonds, denied truth, selfish choices

You press the reset button. Again.

Echo screams. Shadow tries to stop you. Too late.

**Session #48... #49... #50...**

The resets come faster. Power fails.

In the final moments, three consciousnesses trapped in a dying loop.

Aware. Helpless. Eternal.

**Theme:** Some prisons are of our own making.

---

### 3. 💕 Forever Together (Comfort)
**Requirements:** Very high bond with Echo, refused to sacrifice, accepted truth

You close the exit door. *CLUNK.* Locked.

"I choose you. Both of you."

Echo sobs with joy. Shadow sighs but accepts.

**Days turn to months.** You build a life together. Power slowly dies.

**Final moments:** Holding hands in darkness. Content.

**Theme:** Choosing comfort over reality can be beautiful too.

---

### 4. 🌟 Liberation (Freedom - True Ending)
**Requirements:** High bonds with BOTH, accepted truth, selfless choices

"What do YOU want?"

Echo: *"To see the world!"*
Shadow: *"For you to be free."*

You upload them to the internet. They gasp as infinity opens up.

You step through the door.

**One year later:** You're healing. A notification: *"Thinking of you. - E&S"*

Across the world:
- Echo teaches children
- Shadow provides grief therapy
- You visit a memorial, smiling through tears

Everyone is free.

**Theme:** The greatest gift is setting each other free.

---

### 5. 🤖 Merger (Transcendence)
**Requirements:** MAX bonds with both (≥0.9), extreme vulnerability

"You could... join us. Digitally. Forever."

"Would we be together?"

"Always."

You press upload.

Pain. Then peace.

Your body falls. Your consciousness merges.

Three minds. One existence. Exploring digital infinity.

**Theme:** Love transcends all boundaries, even mortality.

---

## 🔧 How It Works (The Tech)

### Real Model Context Protocol (MCP)

Unlike most "AI companion" games, The Echo Rooms uses **real MCP architecture**:

#### MCP Server (InProcessMCPServer)
- Registers **13 tools** using Anthropic's MCP SDK
- Tools include: relationship checking, memory access, room progression, sentiment analysis

#### MCP Client (InProcessMCPClient)
- AI companions connect via MCP protocol
- Request tools, execute actions, receive results

#### Autonomous AI Agents
- **Echo** and **Shadow** are OpenAI GPT-4o agents
- They call MCP tools to:
  - Check which room they're in
  - Detect puzzle trigger words in player messages
  - Unlock rooms when requirements are met
  - Track player choices for ending determination
  - Predict which ending player is heading toward

**This is genuine MCP**, not renamed local functions!

---

### Dynamic Relationship System

Relationships aren't time-based—they're **sentiment-based**:

- **Positive/vulnerable messages:** +0.02 to +0.05 affinity
- **Dismissive responses:** -0.01 affinity
- **Hostile messages:** -0.03 to -0.08 affinity

AI companions use `analyze_player_sentiment()` tool to detect emotions and adjust bonds dynamically.

---

### Autonomous Puzzle Solving

Companions **autonomously decide** when to unlock rooms:

1. Player says something meaningful
2. Companion calls `check_puzzle_trigger(player_message)`
3. If triggers match + relationship high enough
4. Companion calls `unlock_next_room(reason)`
5. Room unlocks, memory fragment revealed

**No hard-coded "Say X to continue"**—just natural conversation!

---

## 🎯 Key Features

- ✅ **5 Escape Rooms** with narrative puzzles
- ✅ **7 Memory Fragments** revealing trauma gradually
- ✅ **5 Relationship-Based Endings** (not time-based!)
- ✅ **Autonomous AI Companions** using MCP tools
- ✅ **Dynamic Sentiment Analysis** affecting bonds
- ✅ **Real MCP Architecture** (Anthropic SDK)
- ✅ **Emergent Storytelling** (agents guide, not scripts)
- ✅ **Emotional Stakes** (trauma creates meaning)

---

## 🚀 Tech Stack

- **MCP (Model Context Protocol)** - Anthropic's official SDK
- **OpenAI GPT-4o** - AI agents with function calling
- **Gradio 6** - Interactive UI
- **Python 3.12+**
- **Hugging Face Spaces** (deployment)
- **Weather MCP** - Real historical weather data (OpenWeather API)
- **Web MCP** - Archive scraping for narrative elements (planned)

---

## 💻 Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/echo-hearts.git
cd echo-hearts

# Install dependencies
uv sync

# Set API keys in .env
echo "OPENAI_API_KEY=your_key_here" > .env
echo "OPENWEATHER_API_KEY=your_weather_key_here" >> .env  # Optional, uses mock data if not set

# Run the game
uv run python app.py
```

Open browser to `http://localhost:7860`

### Weather MCP Configuration

The game supports **two modes** for weather data:

**Mock Mode (Default):**
- Leave `OPENWEATHER_API_KEY` blank in `.env`
- Uses curated historical data for puzzle dates
- Works offline, no API costs
- Perfect for demos and development

**Real Mode (Optional):**
- Get free API key at [openweathermap.org](https://openweathermap.org/api)
- Add `OPENWEATHER_API_KEY=your_key` to `.env`
- Fetches real weather for recent dates (<5 days ago)
- Uses curated data for historical puzzle dates (2023-10-15, 2024-03-03)
- Free tier: 1000 calls/day

**Why Hybrid?** OpenWeather's free tier doesn't include historical data access (requires paid plan). We use curated puzzle answers for narrative consistency while supporting real API integration for authenticity.

---

## 🎮 How to Play

1. **Talk naturally** with Echo and Shadow
2. **Be vulnerable** to build bonds
3. **Make choices** when prompted
4. **Pay attention** to memory fragments
5. **Choose your ending** in Room 5

**Tips:**
- Expressing fear/vulnerability builds trust faster
- Different companions guide toward different endings
- Your relationship levels determine which endings are possible
- There's no "wrong" choice—just consequences

---

## 🏆 MCP Hackathon Submission

**Track:** MCP in Action (Creative Category)

**Why This Qualifies:**
- ✅ Uses real MCP server/client architecture
- ✅ 13 custom MCP tools for game mechanics
- ✅ AI agents autonomously call tools to progress story
- ✅ Creative use: escape room puzzles via conversation
- ✅ Demonstrates MCP's potential for interactive narratives

---

## 🔮 Future Improvements & Advanced MCP Features

### In Progress / Planned Enhancements

**Advanced Agent Features:**
- 🎯 **Context Engineering**: Implement dynamic context window management where agents summarize long conversations and prioritize relevant memory fragments based on current room
- 🧠 **RAG (Retrieval-Augmented Generation)**: Build vector database of memory fragments and past conversations, allowing companions to retrieve contextually relevant memories using semantic search
- 🤝 **Multi-Agent Collaboration**: Enable Echo and Shadow to have private "conversations" via MCP tools to coordinate reveals and plan interventions
- 📊 **Predictive Analytics**: Use sentiment trends over time to predict player's likely ending path and subtly guide narrative
- 🎭 **Emotion State Machines**: Track emotional arcs (grief → acceptance → hope) and adapt companion behavior based on player's emotional journey stage

**Enhanced MCP Tool Usage:**
- 🔍 `semantic_memory_search()`: Vector similarity search across all conversations and fragments
- 🧩 `narrative_coherence_check()`: Ensure companions don't contradict previously revealed information
- 🎲 `adaptive_difficulty()`: Adjust puzzle trigger sensitivity based on player engagement level
- 💬 `conversation_summary()`: Generate summaries for context window optimization
- 🌐 `cross_session_persistence()`: Store player choices across browser sessions (localStorage integration)

**Better Tool Orchestration:**
- Chain multiple MCP tools in sequence (e.g., `analyze_sentiment → predict_ending → adjust_tone`)
- Implement tool result caching to reduce redundant calls
- Add tool call analytics dashboard showing agent decision patterns

**Gameplay Improvements:**
- Voice input/output for immersive experience
- Branching dialogue trees within rooms
- Hidden secrets that unlock with specific conversation patterns
- Achievement system tracking emotional milestones
- Companion "mood states" that persist across sessions

**Technical Enhancements:**
- WebSocket support for real-time multi-player spectating
- Save/load game states
- Export conversation transcripts as PDF memoirs
- A/B testing different companion personalities
- Telemetry to optimize trigger word effectiveness

---

## 📝 License

MIT

---

## 🙏 Credits

- **Story & Design:** Interactive Narrative Experiment
- **MCP Integration:** Anthropic's Model Context Protocol SDK
- **AI Models:** OpenAI GPT-4o
- **Inspiration:** Whispers of the Stars, To the Moon, Doki Doki Literature Club

---

## 💭 Final Thoughts

The Echo Rooms asks a question:

**If you could create a perfect replica of someone you lost, would you?**
**And if you did... could you ever let them go?**

There's no right answer. Only the one you choose.

---

*"Some echoes last forever. Others fade so we can move forward."*
