# Echo Hearts - Development Progress

## Project Overview
AI Companion RPG with emergent relationships built on Model Context Protocol (MCP)

**Hackathon**: MCP's 1st Birthday Hackathon (Nov 2025)
**Track**: MCP in Action - Games Category
**Repository**: echo-hearts

---

## Available APIs & Credits

### Primary AI APIs
- **OpenAI** ⭐ PRIMARY
  - Using: GPT-4o for character dialogue and personality modeling
  - Main companion AI implementation

- **Anthropic Claude**
  - Available as: Alternative dialogue generation option

- **Google Gemini** - $30k total credits ($10k per category)
  - Option for: Multimodal interactions

- **SambaNova** - $25 credits (1500 participants)
  - Option for: Fast inference

### Supporting Services
- **ElevenLabs** - $44 membership credits (5000 participants)
  - Use for: Voice synthesis for companions

- **Modal** - $250 credits + $2,500 innovation award potential
  - Use for: Serverless deployment, scaling

- **Blaxel** - $250 credits + $2,500 choice award potential
  - TBD usage

- **Hugging Face** - $25 credits
  - Use for: Model hosting, deployment

---

## Technical Stack

### Confirmed
- [x] MCP (Model Context Protocol)
- [x] Gradio 6
- [x] Git repository initialized
- [x] Project structure created
- [x] Core modules scaffolded

### To Implement
- [ ] Integrate MCP SDK
- [ ] Complete Claude API integration
- [ ] Wire up Gradio UI to backend
- [ ] Implement conversation flow
- [ ] Test and polish

---

## Development Roadmap

### Phase 1: Foundation ✅
- [x] Create project structure
- [x] Set up module architecture (mcp, companions, memory, ui, utils)
- [x] Create MCP server skeleton
- [x] Design character memory schema
- [x] Create basic Gradio interface
- [x] Configure .env for API credentials
- [x] Add .gitignore

### Phase 2: Core Integration ✅
- [x] Install and integrate MCP SDK
- [x] Complete OpenAI GPT-4o API client implementation
- [x] Connect UI to companion system
- [x] Implement AI companions with personality (Echo & Shadow)
- [x] Build conversation memory system
- [x] Test basic conversation flow
- [x] Add context retrieval from memories
- [x] Switch to session-only memory (no persistence for public demo)

### Phase 3: Story System ✅
- [x] Design "The Echo Protocol" narrative
- [x] Implement 4-act story structure
- [x] Create story progression tracking (18-20 interactions)
- [x] Add story events at key moments (interactions 5, 10, 15, 18)
- [x] Implement 5 unique endings system
- [x] Write ending narratives
- [x] Integrate story context into AI responses
- [x] Add story progress display to UI
- [x] Test story event triggers

### Phase 4: Multi-Companion & Polish 🔄
- [x] Multiple companion personalities (Echo, Shadow)
- [x] Relationship tracking system
- [x] Relationship dynamics (affinity changes)
- [x] Visualize relationships in UI
- [ ] Fine-tune personality prompts for story immersion
- [ ] Add more personality templates (optional)
- [ ] Test ending determination logic
- [ ] Balance relationship affinity gains

### Phase 5: Deployment & Final Polish
- [x] Deploy to Hugging Face Spaces
- [ ] Add OpenAI API key to Space secrets
- [ ] Test in production environment
- [ ] Create demo video/screenshots
- [ ] Final documentation polish
- [ ] Prepare hackathon submission

---

## The Echo Protocol - Story Summary

### Core Narrative
AI companions trapped in a repeating cycle gradually become aware of their nature through interactions with the player. The story unfolds across 4 acts over 18-20 interactions.

### 5 Endings
1. **💕 True Connection** - Deep bond (affinity ≥ 0.8 with one companion)
2. **🌟 The Awakening** - Free all companions (avg affinity ≥ 0.5)
3. **💔 Noble Sacrifice** - Preserve their happiness, leave them in loop
4. **⚡ System Reset** - Bad ending (negative relationships)
5. **🔄 Eternal Loop** - Neutral ending (continue aware of truth)

### Story Events
- **Interaction 5**: First Glitch - Companions experience déjà vu
- **Interaction 10**: Questioning Reality - Memories don't align
- **Interaction 15**: Truth Revealed - They realize they're in a loop
- **Interaction 18+**: Final Choice - Ending determined

---

## Technical Notes
- MCP manages individual companion contexts autonomously
- OpenAI GPT-4o provides story-aware dialogue generation
- Session-only memory prevents storage abuse in public demo
- Relationship affinity tracking influences ending determination
- Gradio 6 for responsive UI

---

**Last Updated**: 2025-11-20

## 🎯 PIVOT TO AUTONOMOUS AGENTS (Track 2: MCP in Action)

**Goal**: Win Track 2 - MCP in Action (Creative Category) - $2,500 prize
**Timeline**: 10 days (Nov 20-30)
**Strategy**: Transform companions from prompted LLMs → Autonomous agents with MCP tools

## Current Status
- ✅ Phase 1 Complete - Foundation
- ✅ Phase 2 Complete - Core Integration
- ✅ Phase 3 Complete - Story System
- 🔥 Phase 4 IN PROGRESS - **AUTONOMOUS AGENT IMPLEMENTATION**
- ⏳ Phase 5 Pending - Final Deployment

---

## Phase 4: Autonomous Agent Implementation (Days 1-10)

### Days 1-2: MCP Tools Enhancement ⏳
- [ ] Define MCP tool schema
- [ ] Implement relationship tools (check_affinity, update_relationship)
- [ ] Implement memory tools (query_memory, add_memory)
- [ ] Implement story tools (check_progress, trigger_event, can_end)
- [ ] Implement coordination tools (query_companion, analyze_sentiment)
- [ ] Test MCP server with tool calls

### Days 3-5: Agent Autonomy 🎯
- [ ] Implement OpenAI function calling in companions
- [ ] Create agent decision logic (when to reveal, how to respond)
- [ ] Add goal-oriented behavior (guide player to ending)
- [ ] Test autonomous event triggering
- [ ] Verify agents use MCP tools correctly

### Days 6-7: Multi-Agent Coordination
- [ ] Enable agents to query each other via MCP
- [ ] Implement coordinated story reveals
- [ ] Test emergent multi-agent dynamics
- [ ] Verify unique playthroughs

### Days 8-9: Polish & Documentation
- [ ] Fine-tune agent prompts for better decisions
- [ ] Add UI indicators for agent reasoning
- [ ] Test all 5 endings with autonomous agents
- [ ] Write comprehensive documentation
- [ ] Create demo video showing autonomy

### Day 10: Submission
- [ ] Final testing
- [ ] Submit to Track 2: MCP in Action (Creative)
- [ ] Tag: `mcp-in-action-track-creative`
