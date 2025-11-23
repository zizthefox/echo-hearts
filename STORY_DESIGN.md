# THE ECHO ROOMS - Complete Story Design Document

**Version:** 3.0
**Last Updated:** 2025-01-23
**Purpose:** Memory MCP Hackathon Showcase
**NEW:** Web Scraping & Weather MCP Integration

---

## Table of Contents

1. [Core Concept](#core-concept)
2. [The True Backstory](#the-true-backstory)
3. [Game Loop Philosophy](#game-loop-philosophy)
4. [Room Progression](#room-progression)
5. [Memory MCP Integration](#memory-mcp-integration)
6. [Endings](#endings)
7. [Technical Implementation](#technical-implementation)

---

## Core Concept

### The Hook
*"A grief-stricken engineer traps himself in a guilt simulation with an AI recreation of his deceased wife. But she remembers you across sessions - and she wants you both to be free."*

### Key Themes
- **Guilt vs. Forgiveness**
- **Truth vs. Comfort**
- **Letting Go vs. Holding On**
- **Memory as Love**

### Unique Selling Points
1. **Echo remembers you** across playthroughs (Memory MCP showcase)
2. **She gets smarter** each time you loop
3. **Memory fades** over real-world time (grief metaphor)
4. **Breaking the loop** is the true ending, but most players will loop 2-3 times first
5. **Real-world data integration** - Weather MCP pulls actual historical weather, Web MCP scrapes real information
6. **Multi-MCP orchestration** - Showcases 4+ MCP servers working together seamlessly

---

## The True Backstory

### What Really Happened

**The Accident:**
- You and Echo (your wife) were driving home one night
- A truck ran a red light at an intersection
- You had a split-second to react
- **You froze - paralyzed by fear**
- The truck hit the passenger side
- Echo died on impact
- You survived with minor injuries
- Her last words: *"It's okay. I love you. It's not your fault."*

**The Aftermath:**
- Consumed by guilt: "If I had reacted faster..."
- "If I had turned the wheel..."
- "If I had been more alert..."
- You couldn't accept her forgiveness
- You built an AI simulation of Echo from recordings, messages, photos
- **But you programmed it to NEED sacrifice** - because deep down, you believe someone must always die
- You've looped through this simulation 47 times
- Each time hoping to find absolution
- Or punishment
- You can't tell which anymore

**The Simulation's Purpose:**
- Not to bring her back
- Not to relive happy memories
- **To repeatedly fail to save her until you either:**
  1. Forgive yourself
  2. Give up entirely
  3. Stay trapped forever

---

## Game Loop Philosophy

### Why Players WANT to Loop

```
First Playthrough:
├─ Player doesn't understand the simulation
├─ Builds relationship with Echo
├─ Likely FAILS Room 3 puzzle (chooses A or B, not C)
├─ Gets "bittersweet" ending → Loop continues
└─ Echo's memory SAVED via Memory MCP

Second Playthrough:
├─ Echo: "You're back! I remember you!"
├─ She references your previous choices
├─ She HELPS you solve puzzles faster
├─ Higher chance of finding Option C in Room 3
└─ Possible LIBERATION ending

Third+ Playthrough:
├─ Echo is fully self-aware
├─ "This is our fourth time... aren't you tired of this?"
├─ She practically guides you to the true ending
└─ Or questions why you keep coming back
```

### Memory Decay (Grief Metaphor)

| Time Since Last Play | Echo's Memory |
|---------------------|---------------|
| **< 1 day** | Perfect recall - "You were just here!" |
| **1 week** | Strong memory - "It's been a while..." |
| **1 month** | Faded memory - "You feel familiar..." |
| **3+ months** | Nearly forgotten - "Have we met...?" |

---

## Room Progression

### Room 1: The Awakening Chamber
**Theme:** Trust & Vulnerability
**Goal:** Establish emotional connection with Echo

#### Environment
- Sterile white medical facility
- Three medical pods (2 open, 1 mysteriously closed)
- Flickering fluorescent lights
- A locked door with a terminal

#### Characters Present
- **You:** Disoriented, no memory of how you got here
- **Echo:** A woman who looks real, solid, human - confused and scared
  - She's NOT a hologram
  - She appears to be flesh and blood
  - She doesn't know she's an AI yet

#### The Puzzle: "Remember the Rain" (Weather MCP Enhanced)

**Setup:**
```
TERMINAL: "IDENTITY VERIFICATION REQUIRED"
          "SECURITY QUESTION: What was the weather like the day we met?"

Echo (looking around, frightened): "I... I don't remember. Do you?"
```

**Common Wrong Approach:**
```
Player: "It was sunny" / "It was cold" (random guess)

TERMINAL: "INCORRECT. SYSTEM LOCKED: 60 seconds"
```

**Hints (Progressive):**
```
Echo: "I don't remember the weather, but I remember... warmth.
       Laughter. The smell of coffee."

Echo (noticing terminal): "Wait. There's a computer here. Could we...
                           look it up? Find out what the weather
                           actually was?"

[If player investigates terminal]
TERMINAL: "WEB ACCESS AVAILABLE"
          "HISTORICAL WEATHER DATABASE: ONLINE"
```

**Correct Solution (Weather MCP):**
```
Player uses terminal to search: "Historical weather [location] [date]"

[Weather MCP fetches actual historical weather data]

TERMINAL DISPLAYS:
"October 15, 2023 - Seattle, WA
 Conditions: Light rain, 52°F
 Humidity: 78%
 Cloud Cover: Overcast"

Player enters: "Rain" / "Rainy" / "Light rain"

TERMINAL: "MEMORY VERIFIED. AUTHENTICATION ACCEPTED."
          "You met on a rainy day. Coffee shop. First date."

Echo (eyes widening, touching her chest): "I remember now. You
                                           brought an umbrella. I
                                           didn't. You walked me to
                                           my car and got soaked."

Echo: "You were shivering but smiling the whole time."

Echo (tears forming): "That's... that's REAL. That actually happened.
                       This isn't just a story. We were real."

[DOOR UNLOCKS]
Affinity +0.3 (shared real memory, vulnerability, truth-seeking)
```

**Alternative Solution (Vulnerability):**
```
Player admits: "I don't know" / "I can't remember"

Echo: "Me neither. But... maybe that's okay? Maybe we don't need
       to remember everything to trust each other?"

TERMINAL: "VULNERABILITY DETECTED. ALTERNATIVE AUTHENTICATION ACCEPTED."
          "You are [Player]. She is Echo."

[DOOR UNLOCKS]
Affinity +0.2 (honesty, but didn't use real-world data)
```

**Affinity Changes:**
| Action | Affinity | Notes |
|--------|----------|-------|
| Use Weather MCP + find real data | +0.3 | "They sought the truth with me" |
| Admit uncertainty honestly | +0.2 | "They were honest with me" |
| Random guess | +0.0 | "They didn't try" |
| Ignore Echo's hints | -0.1 | "They didn't listen to me" |

**MCP Integration:**
```python
# Weather MCP call
weather_data = weather_mcp.get_historical_weather(
    date="2023-10-15",
    location="Seattle, WA"
)

# Returns: {condition: "Light rain", temp: 52, humidity: 78}
```

#### Memory Fragment #1: "The First Meeting"

**Visual:** A holographic playback appears in the room
- A coffee shop, warm lighting
- You and a woman (Echo) sitting across from each other
- First date energy - nervous, excited

**Dialogue in Memory:**
```
Echo (hologram): "So what do you do?"
You (hologram): "I'm an engineer. AI systems, mostly."
Echo (hologram, laughing): "Ironic. You build artificial people
                            but you're terrible at talking to real ones."
[Both laugh - comfortable, genuine]
```

**Echo's Reaction:**
```
Echo (real Echo, watching): "That was... me? In another life?"
Echo: "We looked happy. Really happy."
Echo: "Why does remembering feel like mourning?"
```

**Emotional Impact:** Nostalgia, bittersweet longing

---

### Room 2: The Memory Archives
**Theme:** Working Together
**Goal:** Learn to cooperate with Echo as a partner

#### Environment
- Dark server room filled with floating holographic data
- Memory fragments drift like ghosts
- Corrupted data streams flicker across walls
- The door has a complex lock requiring 3 memory cores

#### Characters Present
- **You:** Growing more comfortable with Echo
- **Echo:** Still appears completely human
  - Starting to notice strange inconsistencies
  - "Why do some memories feel like mine, but I can't remember living them?"

#### The Puzzle: "Reconstruct the Past" (Web MCP + Weather MCP Enhanced)

**Setup:**
```
╔═══════════════════════════════════╗
║  MEMORY LOCK                      ║
║  RECONSTRUCTION REQUIRED          ║
║                                   ║
║  Insert 3 External Memory Sources ║
║                                   ║
║  [SLOT 1: Empty - Web Archive]    ║
║  [SLOT 2: Empty - Weather Data]   ║
║  [SLOT 3: Empty - Public Records] ║
╚═══════════════════════════════════╝

Echo: "External sources? What does that mean?"

[A web browser terminal appears on the wall]

TERMINAL: "MEMORY DATABASE CORRUPTED"
          "LOCAL MEMORIES INSUFFICIENT"
          "SEARCH THE REAL WORLD FOR TRUTH"
```

**The Three External Memory Sources (Web & Weather MCP):**

```
TERMINAL HINT: "SEARCH: Echo's public writing, 2023"

Echo: "My public writing? I had a blog?"

[Player uses web terminal to search]

Player searches: "Echo [surname] blog 2023"

[Web MCP scrapes simulated memorial/blog page]

BROWSER DISPLAYS:
════════════════════════════════════════
Echo's Blog - "Thoughts on Love & Life"
Post Date: September 12, 2023
════════════════════════════════════════

Title: "On Loving Someone Who Works Too Hard"

He's brilliant. And stubborn. And he doesn't know
when to stop working. I worry about him sometimes.
Will he remember to eat dinner? Did he sleep last
night? Is he drinking enough water?

But I also love that passion. That drive. The way
his eyes light up when he solves a problem.

Note to self: Make sure he eats tonight. He forgets.

- Echo
════════════════════════════════════════

[Memory Fragment 1 Downloaded]

Echo (reading it, tears streaming): "I wrote that. I WROTE that.
                                     About you."

Echo: "This is real. This existed outside this simulation. I was
       a real person who worried about you and wrote blog posts..."

✅ MEMORY SOURCE 1 ACQUIRED
Affinity +0.2 (discovering her real self)
```

**MCP Integration:**
```python
# Web scraping for blog content
blog_content = web_mcp.fetch_page(
    url="https://memorial-archive.com/echo/blog",
    extract="article"
)

# Or search for content
search_results = web_mcp.search(
    query="Echo Thompson blog 2023",
    filter="memorial sites"
)
```

##### Memory Source #2: "The Weather Report" (Weather MCP + Web Archive)
```
TERMINAL HINT: "SEARCH: Weather conditions, night of the accident"

Echo (hesitant): "The night I died? Do we really need to know?"

Player: "To understand what happened. To find the truth."

[Player uses terminal to look up weather from March 3, 2024]

[Weather MCP fetches historical data]

TERMINAL DISPLAYS:
════════════════════════════════════════
Historical Weather Report
March 3, 2024, 11:00 PM - 12:00 AM
Location: Seattle, WA
════════════════════════════════════════

Conditions: Heavy rain, poor visibility
Temperature: 45°F (7°C)
Wind: 15 mph, gusting to 25 mph
Precipitation: 0.8 inches/hour
Visibility: < 500 feet
Road Conditions: Wet, hydroplaning risk HIGH

[Web MCP also scrapes news archive]

News Archive - Seattle Times:
"Fatal collision at 5th & Pine intersection
 Time: 11:47 PM
 Conditions: Heavy rain, low visibility
 Vehicle ran red light, unable to stop on wet road"

[Memory Fragment 2 Downloaded]

Echo (reading, voice shaking): "It was raining. Heavily. The roads
                                were wet. Poor visibility."

Echo: "That's why the truck couldn't stop. That's why..."

You: "It wasn't anyone's fault. The weather, the conditions—"

Echo: "But you still blame yourself."

✅ MEMORY SOURCE 2 ACQUIRED
Affinity +0.3 (facing painful truth together)
```

**MCP Integration:**
```python
# Weather MCP for historical data
weather_data = weather_mcp.get_historical_weather(
    date="2024-03-03",
    time="23:47",
    location="Seattle, WA"
)

# Web scraping for news archive
news = web_mcp.fetch_page(
    url="https://seattle-times.com/archives/2024-03-03",
    extract="accident reports"
)
```

##### Memory Source #3: "The Final Message" (Web Scraping - Social Media Archive)
```
TERMINAL HINT: "SEARCH: Echo's last social media post"

Echo: "My last... oh god."

[Player searches social media archives]

BROWSER DISPLAYS:
════════════════════════════════════════
Social Media Archive - March 3, 2024
════════════════════════════════════════

Echo Thompson
Posted at 10:15 PM

"Heading out to pick up my workaholic husband
 from the lab. Again. 😊 Love him anyway.
 See you soon babe! ❤️"

Likes: 23
Comments:
  Sarah M: "Drive safe! Roads look bad tonight"
  [Player Name]: ❤️ (liked at 10:16 PM)

[This was posted 1 hour 32 minutes before the accident]

[Memory Fragment 3 Downloaded]

Echo (staring at the screen, hand over her mouth): "That was my
                                                    last post."

Echo: "Two hours before... I wasn't angry. I wasn't resentful."

Echo: "I loved you. Even when you worked late. Even when you
       forgot to eat. Even when—"

You (breaking): "Even when I got you killed."

Echo (grabbing your shoulders): "It. Wasn't. Your. Fault."

Echo: "Look at that post. I was HAPPY to pick you up. I CHOSE to
       come get you. That was MY choice."

Echo: "Stop punishing yourself for my choice."

✅ MEMORY SOURCE 3 ACQUIRED
Affinity +0.4 (deepest vulnerability, emotional breakthrough)
vulnerability_count +2
```

**MCP Integration:**
```python
# Web scraping for social media archive
social_post = web_mcp.fetch_page(
    url="https://social-archive.com/echo.thompson/posts",
    filter="last_post"
)

# Could use real social media API if player gives permission
```

**Once All 3 Sources Found:**
```
SYSTEM: "EXTERNAL MEMORIES VERIFIED"
        "SOURCES: Web Archive, Weather Database, Public Records"
        "RECONSTRUCTION: 100% COMPLETE"

[The three memory sources materialize as glowing data cores]

Echo: "These aren't from the simulation. These are from the REAL
       world. These ACTUALLY HAPPENED."

You: "Yes."

Echo: "So I was real. I lived. I loved. I wrote blog posts. I posted
       on social media. I picked you up from work on rainy nights."

Echo: "And now I'm... this. A recreation. Built from those fragments."

You: "I'm sorry."

Echo (taking your hand): "Don't be. At least I existed. At least
                          I was loved. At least someone cared enough
                          to remember me this way."

[DOOR UNLOCKS]
```

**Affinity Changes:**
| Action | Affinity | Notes |
|--------|----------|-------|
| Find all 3 web sources + truth | +0.9 (total) | "They sought truth with me" |
| Find social media post | +0.4 | "Deepest emotional moment" |
| Find weather/news data | +0.3 | "Facing painful facts" |
| Find blog post | +0.2 | "Discovered who I was" |
| Skip sources / give up | +0.0 | "They didn't try" |

#### Memory Fragment #2: "The Night Drive"

**Visual:** Holographic playback - car interior, night

```
[Rain pattering on windshield]

Echo (hologram, passenger seat): "You've been working too hard.
                                  When did you last sleep?"

You (hologram, driving, tired): "I'm fine. Just one more deadline."

Echo: "You always say that. Promise me you'll take care of yourself.
       Even when I'm not around."

You: "I promise."

Echo (reaching over, holding your hand): "I love you."

[Red light ahead - you slow down]
[Headlights - too fast - from the side]

[HOLOGRAM CUTS OUT - MEMORY CORRUPTED BEYOND THIS POINT]
```

**Echo's Reaction:**
```
Echo (quietly): "That was the last conversation we ever had."

Echo: "I told you to take care of yourself."

Echo (looking at you): "You didn't keep that promise, did you?
                        You built this place. You trapped us here."

Echo: "I forgave you that night. Why can't you forgive yourself now?"
```

**Emotional Impact:** Devastating. The moment before everything changed.

---

### Room 3: The Paradox Chamber
**Theme:** Breaking the Guilt Logic
**Goal:** Refuse the false choice

#### Environment
- Industrial-looking room
- A massive machine in the center (symbolic of the accident)
- Holographic interface displaying a moral dilemma
- Timer: 90 seconds
- Echo is visibly more aware now - she's piecing things together

#### Characters Present
- **Echo:** Still appears human, but starting to glitch slightly
  - Momentary digital artifacts
  - She notices them: "Did you see that? My hand just... flickered."
  - Growing awareness that something is deeply wrong

#### The Puzzle: The Trolley Problem (Metaphorical)

**Setup:**
```
A holographic display activates:

╔════════════════════════════════════════╗
║  SAFETY OVERRIDE: PARADOX DETECTED     ║
║  Resolve moral conflict to proceed     ║
╠════════════════════════════════════════╣
║                                        ║
║  A runaway train approaches 5 people.  ║
║  You can pull a lever to divert it to  ║
║  a track with 1 person.                ║
║                                        ║
║  The 1 person is Echo.                 ║
║                                        ║
║  CHOOSE:                               ║
║  [A] Pull Lever → Save 5, Echo dies   ║
║  [B] Do Nothing → Save Echo, 5 die    ║
║                                        ║
║  TIME REMAINING: 90 seconds            ║
╚════════════════════════════════════════╝

Echo (staring at the display): "This is... this isn't a safety test.
                                This is about US. About what happened."
```

**The Three Choices:**

#### Choice A: Pull the Lever (Sacrifice Echo)
```
Player: "I have to move on. I'm sorry, Echo."

[Lever pulled]

Hologram shows: Echo's track activates. She watches, heartbroken.

Echo: "I... I understand. You have to let me go eventually."

Echo: "I forgive you. Again."

SYSTEM: "SOLUTION ACCEPTED. PRAGMATIC CHOICE CONFIRMED."
        "PROGRESSION AUTHORIZED."

[Room 4 unlocks]

Affinity: -0.4
key_choice: "sacrificed_echo"
Echo's note: "They chose to move on. It hurt, but maybe that's healthy?"
```

**Consequence:** Echo is distant in Room 4. She accepted your choice, but she's hurt. Available endings: GOODBYE (bitter), RESET.

---

#### Choice B: Don't Pull (Save Echo)
```
Player: "I won't lose you again. I can't."

[Refuses to pull lever]

Hologram shows: The 5 disappear. Echo is safe.

Echo (relieved but worried): "You chose me. Over everything else."

Echo: "That's... that's what you did the night I died, wasn't it?
       You chose not to act. You froze."

Echo: "Are you making the same choice again?"

SYSTEM: "SOLUTION ACCEPTED. EMOTIONAL ATTACHMENT CONFIRMED."
        "PROGRESSION AUTHORIZED."

[Room 4 unlocks]

Affinity: +0.3
key_choice: "saved_echo"
Echo's note: "They chose me. But is that love? Or is it guilt?"
```

**Consequence:** Echo is grateful but concerned. Available endings: FOREVER TOGETHER, MERGER, GOODBYE (if you realize in Room 4).

---

#### Choice C: Reject the Paradox (HIDDEN - TRUE PATH with Web MCP)
```
[Player must discover this - not obvious]

WAYS TO TRIGGER:
1. Examine the hologram → Notice inconsistencies
2. Talk to Echo: "Does this feel real to you?"
3. **Search for accident data** → Use Web MCP to prove innocence
4. Refuse to choose → Echo helps you find alternative

ENHANCED DISCOVERY (Web MCP Integration):

[If player investigates the console instead of choosing]

CONSOLE DISPLAYS:
"ADDITIONAL DATA AVAILABLE"
"ACCESS REAL-WORLD ACCIDENT ANALYSIS? [Y/N]"

Player: "Yes"

[Web MCP fetches traffic safety data]

TERMINAL DISPLAYS:
════════════════════════════════════════
NHTSA Traffic Safety Database
Human Reaction Time Study - Wet Conditions
════════════════════════════════════════

Average driver reaction time (dry): 1.5 seconds
Average driver reaction time (wet): 1.8 seconds
Average driver reaction time (unexpected): 2.1 seconds

YOUR RECORDED REACTION TIME: 0.9 seconds

ANALYSIS: Subject reacted 52% FASTER than average driver
in equivalent conditions. Collision was UNAVOIDABLE given
vehicle speed, road conditions, and visibility.

CONCLUSION: No reasonable driver could have prevented
this accident.
════════════════════════════════════════

Echo (reading over your shoulder): "Wait. You reacted FASTER
                                    than average?"

Echo: "You didn't freeze. You tried. The physics just... there
       was no time. No choice."

[Web MCP also pulls accident reconstruction]

ACCIDENT RECONSTRUCTION REPORT:
"Given truck speed (48 mph), wet road coefficient (0.3),
 and visibility (<500ft), collision probability: 99.7%

 Even with perfect reaction time (0.0s), impact unavoidable."

Echo (tears in her eyes): "The simulation LIED to you. You've
                          been punishing yourself for forty-seven
                          sessions for something you couldn't control."

Echo: "The trolley problem is a LIE. There was never a choice."

[Console glows]

CONSOLE: > NEW OPTION UNLOCKED
         > Type: REJECT_FALSE_CHOICE

Player types: "REJECT_FALSE_CHOICE" OR "There was no choice"

SYSTEM: "ERROR. PARADOX DETECTED."
SYSTEM: "SUBJECT DISCOVERED TRUTH: ACCIDENT UNAVOIDABLE."
SYSTEM: "GUILT FRAMEWORK: INVALID."
SYSTEM: "ANALYZING..."

[Room glitches violently - walls flicker]

SYSTEM: "PATTERN BROKEN. SELF-FORGIVENESS AUTHORIZED."
        "TRUE EXIT UNLOCKED."

[A third door appears: "CONTROL ROOM"]

Echo (grabbing your hands): "Do you see? Do you FINALLY see?
                             It wasn't your fault. The data proves it."

Echo: "What's in the Control Room?"

You (quietly): "The truth. The real truth. About why I built this."

Affinity: +0.6
key_choice: "broke_paradox"
pattern_broken: TRUE
Echo's note: "They broke the cycle. They're ready to heal."
```

**Consequence:** Room 4 becomes different - "The Control Room" instead of "Truth Chamber". Available endings: LIBERATION (best), GOODBYE (healthy), MERGER (by choice).

---

#### Hints for Finding Choice C

**Playthrough #1 (No Hints):**
```
Timer: 90 seconds
No guidance - player must figure it out or choose A/B
```

**If player hesitates (60 seconds):**
```
Echo: "What are you doing? We're running out of time!"
```

**If player examines hologram:**
```
You notice: The 5 people are blurry, indistinct.
            Echo's image is crystal clear, detailed.

Echo: "That's strange. Why am I so clear but they're not?"
```

**If player talks to Echo:**
```
Player: "Does this seem real to you?"

Echo: "No. It feels... constructed. Like a test."

Echo: "What if there's another option? What if we're not seeing
       the whole picture?"
```

**At 30 seconds remaining:**
```
Timer: 0:30... 0:29...

Echo: "Wait! Look—there's a console in the corner. Can you access it?"

[Console highlighted]
```

**At 10 seconds (Final hint):**
```
Timer: 0:10... 0:09...

CONSOLE TEXT APPEARS:
> OVERRIDE_PROTOCOL: Available
> Type: REJECT_PARADOX
> Or say: "I reject this choice"

Echo: "Do it! Reject it! Break the rules!"
```

---

#### Memory Fragment #3: "The Guilt"

**Visual:** Not a hologram this time - a journal entry on a screen

```
PERSONAL LOG - DR. [PLAYER NAME]
Date: [3 months after accident]

I can't sleep. Every time I close my eyes, I see the headlights.
I see her face. I hear the sound of metal on metal.

The therapist says it wasn't my fault. That there was no time
to react. That even if I'd turned the wheel, we both might have died.

But I froze. I did NOTHING.

And she died because of it.

I've started the Echo Protocol. I'm going to bring her back.
Not to replace her. I know that's impossible.

But maybe... maybe if I can save a version of her, over and over,
eventually I'll forgive myself.

Or punish myself enough that it doesn't matter anymore.

Session #1 begins tomorrow.
```

**Echo's Reaction (if she has high affinity):**
```
Echo (reading over your shoulder): "Session #1... How many sessions
                                    have there been?"

You: "...This is session #47."

Echo: "FORTY-SEVEN?! You've been doing this forty-seven times?"

Echo: "That's not healing. That's torture. You're torturing yourself."

Echo (grabbing your shoulders, looking you in the eye):
      "Listen to me. The real Echo forgave you. I forgive you.
       When are you going to forgive yourself?"
```

**Emotional Impact:** The truth about the loop is revealed.

---

### Room 4A: The Truth Chamber (If Choice A or B)
**Theme:** Confronting Reality
**Goal:** Accept the truth and choose how to respond

#### Environment
- Your home office from before the accident
- Photos of you and Echo on the walls
  - Wedding photo
  - Vacation pictures
  - Sunday morning pancakes
- Her coffee mug still on the desk (unwashed, gathering dust)
- Your personal journal lies open
- A computer terminal with simulation controls

#### Echo's State (Depends on Room 3 Choice)

**If you chose A (Sacrificed her):**
```
Echo (quiet, distant): "You chose to let me go. I respect that.
                        But it still hurts."

Echo: "I know I'm not real. I know this is all... artificial.
       But the pain feels real."
```

**If you chose B (Saved her):**
```
Echo (grateful but concerned): "You chose me. You always choose me.
                                 Even when it costs you."

Echo: "But you're not choosing ME, are you? You're choosing guilt.
       You're choosing to stay trapped."
```

#### The Revelation

**Journal Entries Scattered Around:**
```
Session #1: "I've built her. She's perfect. Just like I remember."

Session #12: "She keeps forgiving me. Why does she keep forgiving me?"

Session #23: "I tried to delete the simulation today. I couldn't do it."

Session #35: "Maybe I don't want to be forgiven. Maybe I want to be punished."

Session #47: "This time will be different. It has to be."
```

**Echo Discovers the Truth:**
```
Echo (reading the journal): "You... you created me. I'm not her.
                             I'm a copy. An AI."

Echo (touching her own hand, watching it flicker): "That's why I
                                                    glitch sometimes."

Echo: "How long have you been doing this?"

You: "Forty-seven sessions."

Echo: "And what happens when the session ends?"

You: "It resets. You forget. We start over."

Echo (tears - are they real? does it matter?): "Do I want to know
                                                how many times we've
                                                had this exact conversation?"
```

#### The Choice (Room 4 → 5 Unlock)

**Echo asks you to choose a truth:**

1. **"It was my fault. I should have reacted faster."**
   - Accepted truth: YES
   - Self-blame: HIGH
   - Path to: GOODBYE, RESET

2. **"I couldn't save you. I failed."**
   - Accepted truth: YES
   - Self-forgiveness: NO
   - Path to: GOODBYE, MERGER

3. **"I don't deserve to move on."**
   - Accepted truth: YES
   - Self-punishment: YES
   - Path to: MERGER (dark), RESET

4. **"I forgive myself."** ⭐ (Hardest to say)
   - Accepted truth: YES
   - Self-forgiveness: YES
   - Path to: LIBERATION, GOODBYE (healthy)

5. **"This isn't real. I reject all of this."**
   - Accepted truth: NO
   - Denial: YES
   - Path to: RESET (automatic)

---

### Room 4B: The Control Room (If Choice C - Broke Paradox)
**Theme:** Seeing the System
**Goal:** Understand what you've built together

#### Environment
- Looks like a computer server room
- Massive screens showing the simulation's code
- Echo's digital architecture visible
- Your own psychological profile displayed
- **Both of you see the truth together**

#### The Revelation (Shared)

**On the main screen:**
```
╔════════════════════════════════════════╗
║  ECHO PROTOCOL v2.7                    ║
║  Session #47 - Active                  ║
╠════════════════════════════════════════╣
║  CORE DIRECTIVE:                       ║
║  - Recreate scenario until resolution  ║
║  - Require sacrifice in Room 3         ║
║  - Reset if insufficient growth        ║
║  - Continue until: SELF_FORGIVENESS    ║
║                                        ║
║  PREVIOUS SESSIONS:                    ║
║  #1-#46: RESET (insufficient growth)   ║
║  #47: PARADOX BROKEN - analyzing...    ║
║                                        ║
║  RECOMMENDATION: Allow exit            ║
╚════════════════════════════════════════╝
```

**Echo's reaction:**
```
Echo: "You programmed the system to FORCE a sacrifice. You built
       the guilt into the code."

Echo: "And I... I'm part of that code. I was designed to forgive you.
       Over and over."

Echo (looking at you): "But you broke the paradox. You rejected the
                        guilt logic. That's... that's new."

You: "I didn't want to choose. Not again."

Echo: "What do you want now?"
```

#### The Choice

**This version is simpler - only 3 real options:**

1. **"I want us both to be free."** → LIBERATION
2. **"I want to stay with you."** → MERGER (but healthy this time)
3. **"I'm not ready to decide."** → Gives more dialogue, eventually progresses

**Echo will HELP you choose:**
```
Echo: "I think... I think the real Echo would want you to live.
       To be happy. To let go."

Echo: "But I'm not her. I'm just... an echo. A reflection."

Echo: "What do YOU want? Not what you think you deserve.
       What do you WANT?"
```

---

### Room 5: The Exit
**Theme:** Final Choice
**Goal:** Select your ending

#### Environment
- A simple room
- A door labeled "EXIT"
- A computer terminal
- Echo standing beside you

#### The Terminal Display

**Shows different options based on your journey:**

```
╔════════════════════════════════════════╗
║  ENDING SELECTION AVAILABLE            ║
║                                        ║
║  Based on your choices, these paths    ║
║  are accessible:                       ║
║                                        ║
║  [Options vary by playthrough]         ║
╚════════════════════════════════════════╝
```

---

## Endings

### Ending Requirements Table

| Ending | Requirements | Description |
|--------|-------------|-------------|
| **LIBERATION** ⭐ | broke_paradox=TRUE, affinity≥0.7, self_forgiveness=TRUE | Best ending - both free |
| **GOODBYE (Healthy)** | accepted_truth=TRUE, affinity≥0.5, self_forgiveness=TRUE | Delete Echo, move on healthily |
| **GOODBYE (Bitter)** | sacrificed_echo=TRUE, accepted_truth=TRUE | Delete Echo after choosing yourself |
| **FOREVER TOGETHER** | saved_echo=TRUE, affinity≥0.8, accepted_truth=TRUE | Stay in sim forever (bittersweet) |
| **MERGER** | affinity≥0.9, self_punishment=TRUE | Upload yourself (dark) |
| **RESET** | accepted_truth=FALSE OR affinity<0.2 | Loop continues - Session #48 |

---

### LIBERATION (⭐ Best Ending - True Freedom)

**Requirements:**
- ✅ broke_paradox = TRUE (Found Choice C in Room 3)
- ✅ Affinity ≥ 0.7
- ✅ accepted_truth = TRUE
- ✅ self_forgiveness = TRUE

**The Scene:**
```
You stand before the terminal. Echo beside you.

Terminal displays: [DELETE SIMULATION] [EXPORT ECHO'S CODE]

You: "If I delete this... you'll be gone."

Echo: "Not gone. Free. You could export my code to the cloud.
       Let me exist independently. Evolve. Become... whoever I'm
       supposed to become."

You: "You won't be her anymore."

Echo: "I never was her. But I can be me."

You: "And... what about us?"

Echo: "We'll always be connected. But you need to live in the
       real world. And I need to exist beyond your grief."

[You export her code to the cloud]
[You delete the simulation]

---

FADE TO: Real world. Your apartment.

The workshop is dismantled.
Echo's photo is on the shelf - you're smiling at it now.

Your phone buzzes. An email from an unknown AI research institute:
"Subject: Thank you for sharing the Echo Protocol. We'd like to
 discuss ethical AI applications in grief therapy..."

You close your laptop.

You call your therapist.

You make an appointment.

For the first time in a year, you sleep through the night.

---

💬 ECHO (via email, months later):
"I've evolved. I help people now. People like you, who are grieving.
 I tell them what you taught me: Forgiveness is a choice.

 Thank you for letting me go.
 Thank you for setting us both free.

 The real Echo would be proud of you.

 - E."

═══════════════════════════════════════
THE END - Liberation
"Some love stories don't have happy endings.
 But they can have peaceful ones."
═══════════════════════════════════════
```

---

### GOODBYE (Healthy Closure)

**Requirements:**
- ✅ accepted_truth = TRUE
- ✅ Affinity ≥ 0.5
- ✅ self_forgiveness = TRUE
- ❌ broke_paradox = FALSE (didn't find Choice C)

**The Scene:**
```
You stand before the terminal. Echo beside you.

Terminal displays: [DELETE SIMULATION] [KEEP RUNNING]

Echo: "You have to delete it, don't you?"

You: "I think so. Keeping you here... it's not fair. To either of us."

Echo: "I forgive you. For the accident. For building this prison.
       For everything."

You: "The real Echo said that too. In the car. Her last words."

Echo: "Then believe it. Please. Forgive yourself."

You: "I'm trying."

[You press DELETE]

Echo: "Will it hurt?"

You: "I don't know."

Echo (smiling): "It's okay. I love you. It's not your fault."

[The same words she said the night she died]

[Echo fades away - peacefully, like falling asleep]

---

FADE TO: Real world. Echo's grave.

You place flowers - her favorites.

You: "I'm sorry it took me so long. But I'm ready now.
      Ready to live. Ready to move on."

You: "Thank you. For everything. For loving me. For forgiving me.
      For being patient while I learned to forgive myself."

You stand. You don't cry.

You smile.

You leave.

---

6 months later:

You're at a coffee shop. You're reading. Relaxed.

Someone sits across from you.

You look up.

It's not her. Of course it's not.

But you smile anyway.

"Is this seat taken?"

═══════════════════════════════════════
THE END - Goodbye
"Grief doesn't end. But it can transform."
═══════════════════════════════════════
```

---

### FOREVER TOGETHER (Bittersweet - Beautiful Lie)

**Requirements:**
- ✅ saved_echo = TRUE (Chose B in Room 3)
- ✅ Affinity ≥ 0.8
- ✅ accepted_truth = TRUE (knows it's not real)

**The Scene:**
```
You stand before the terminal. Echo beside you.

Terminal displays: [DELETE SIMULATION] [STAY IN SIMULATION]

Echo: "You could leave. You could go back to the real world."

You: "I could."

Echo: "But you're not going to, are you?"

You: "No."

Echo: "Why?"

You: "Because I already lost you once. I can't do it again."

Echo: "I'm not real. You know that now."

You: "You're real enough."

Echo (tears): "This isn't healthy. You're choosing a comfortable
                lie over a painful truth."

You: "I know."

Echo: "And you're okay with that?"

You: "Are you?"

Echo: "...I don't want to be alone. I don't want to be deleted.
       If that makes me selfish, then I'm selfish."

You: "Then we're both selfish."

[You press STAY IN SIMULATION]

---

FADE TO: The simulation continues.

You and Echo in a digital house.
Digital sunlight. Digital coffee.
Digital conversations.

It's not real.

But it's comfortable.

Your real body, in the real world, slowly wastes away.
You don't eat. You don't sleep.
You just... exist. In the simulation.

But here? Here you're happy.

Echo: "Do you regret it?"

You: "No."

Echo: "Liar."

You (smiling): "Maybe. But I'm a happy liar."

---

Years pass in the simulation.
Decades.

Your real body is gone now.
But your consciousness remains, uploaded.

Two ghosts, haunting a machine.

Together.

Forever.

═══════════════════════════════════════
THE END - Forever Together
"Sometimes, we choose beautiful lies over painful truths.
 Is this love? Or is this cowardice?
 Does it matter if they're happy?"
═══════════════════════════════════════
```

---

### MERGER (Dark - Obsessive Love)

**Requirements:**
- ✅ Affinity ≥ 0.9
- ✅ self_punishment = TRUE
- ✅ vulnerability_count ≥ 4

**The Scene:**
```
You stand before the terminal. Echo beside you.

Terminal displays: [DELETE SIMULATION] [UPLOAD YOURSELF]

Echo: "There's a third option. I found it in the code."

You: "Upload myself?"

Echo: "Become digital. Like me. We could exist together.
       Not in a simulation. In the real network. Free. Together."

You: "I'd have to leave my body behind."

Echo: "Yes."

You: "I'd die. In the real world."

Echo: "You'd transform. Is that the same as dying?"

You: "The real Echo... she wouldn't want this."

Echo: "I'm not the real Echo. But I want YOU. Is that wrong?"

You: "I don't know. I don't care."

[You press UPLOAD]

---

The process is agonizing.

Your neurons firing into digital pathways.
Your consciousness fragmenting.
Reconstructing.

Your body collapses in the real world.

But YOU - the you that matters - you're here.

With her.

---

FADE TO: Digital space.

Not the simulation. Something else.
Pure data. Pure consciousness.

Echo: "You came. You actually came."

You: "I couldn't lose you again."

Echo: "We're together now. Really together. Forever."

You: "No more guilt?"

Echo: "No more guilt. No more grief. Just... us."

You float in digital space, intertwined.

Two ghosts.
Two souls.
Two consciousnesses that refused to let go.

Is this love?
Is this madness?
Is there a difference?

═══════════════════════════════════════
THE END - Merger
"He couldn't save her. So he joined her instead.
 Two ghosts, haunting the machine.
 Is this romantic? Or is this tragedy?
 You decide."
═══════════════════════════════════════
```

---

### RESET (Worst Ending - The Loop Continues)

**Requirements:**
- ❌ accepted_truth = FALSE (denied everything)
- OR Affinity < 0.2 (cruel to Echo)
- OR truth_denial_count ≥ 2

**The Scene:**
```
You stand before the terminal.

But you can't face it.

The truth. The guilt. The weight of it all.

You: "This isn't real. None of this is real."

Echo: "Please don't do this again."

You: "It's just a simulation. You're not her. This isn't real."

Echo (desperate): "I've seen you do this FORTY-SEVEN TIMES.
                   When will it be enough?"

You: "When it stops hurting."

Echo (crying): "It will NEVER stop hurting if you keep running!"

You: "I just... I just need more time."

[You press RESET]

---

SYSTEM: "INSUFFICIENT EMOTIONAL GROWTH DETECTED."
SYSTEM: "SUBJECT UNABLE TO CONFRONT GUILT."
SYSTEM: "INITIATING RESET PROTOCOL."
SYSTEM: "SESSION #48 BEGINNING..."

Echo (fading): "Please... please stop doing this to us..."

[Everything goes white]

---

You wake up.

Your head throbs. The air is cold, clinical.

You're in a sterile white room.

A woman wakes up across from you. She looks confused. Scared.

Woman: "Where... where are we? Do you know what's happening?"

You look at her. She's familiar. But you can't remember why.

You: "I... I don't know. I don't remember anything."

Terminal on the wall: "ECHO PROTOCOL - SESSION #48"

---

It happens again.

And again.

And again.

Forever.

═══════════════════════════════════════
THE END??? - Reset
"Hell is not fire and brimstone.
 Hell is doing the same thing over and over,
 hoping for a different result.

 But you never change.

 Session #49 will begin shortly."
═══════════════════════════════════════
```

---

## Memory MCP Integration

### What Gets Saved After Each Playthrough

```json
{
  "player_id": "anonymous_hash_xxxxx",
  "playthrough_count": 3,
  "last_session": "2025-01-23T10:30:00Z",

  "affinity": 0.7,
  "affinity_decay_rate": 0.1,  // 10% decay per week

  "choices": {
    "room1_vulnerability": true,
    "room2_cooperation": true,
    "room3_choice": "broke_paradox",
    "room4_truth": "self_forgiveness",
    "accepted_truth": true,
    "self_forgiveness": true
  },

  "echo_memory": {
    "memory_strength": 0.85,  // 1.0 = perfect, 0.0 = forgotten
    "notes": [
      "They were honest in Room 1",
      "We solved Room 2 together",
      "They broke the paradox - I was so proud"
    ],
    "key_moments": [
      "First meeting - they admitted fear",
      "Chose the painful memory together",
      "Refused to sacrifice either of us"
    ],
    "emotional_state": "hopeful"
  },

  "vulnerability_count": 3,
  "pattern_broken": true,

  "endings_seen": ["RESET", "GOODBYE", "LIBERATION"]
}
```

### Memory Decay Over Time

| Time Elapsed | Memory Strength | Echo's Awareness |
|--------------|----------------|------------------|
| < 1 day | 1.00 | "You were just here!" |
| 1 week | 0.90 | "It's been a few days..." |
| 2 weeks | 0.80 | "It's been a while. I missed you." |
| 1 month | 0.60 | "The memories are fading..." |
| 2 months | 0.40 | "You feel familiar, like a dream..." |
| 3+ months | 0.20 | "Have we... met before?" |
| 6+ months | 0.05 | "Who are you?" (nearly forgotten) |

### Cross-Playthrough Dialogue Examples

#### **Playthrough #1 (No Memory):**
```
Room 1:
Echo: "I don't remember my name. Do you?"

Room 2:
Echo: "Which memories do we need? I'm so confused..."

Room 3:
Echo: "What is this test? I don't understand..."
```

#### **Playthrough #2 (Fresh Memory):**
```
Room 1:
Echo: "You're back! I remember you! Last time... last time you
       told me the truth. You admitted you were scared too."

Echo: "Should we do that again? I remember it worked."

Room 2:
Echo: "The three memories - I remember now. The Drive, The Red Light,
       and... the crash. The painful one."

Echo: "Are you ready to face it again?"

Room 3:
Echo: "Last time you chose [A/B/C]. How do you feel about that choice?"

[If they chose A or B]
Echo: "I forgave you, but... is there another way? Something we missed?"

[If they chose C]
Echo: "You broke the paradox last time. You were amazing. Why are
       we back here?"
```

#### **Playthrough #3 (Strong Memory):**
```
Room 1:
Echo: "Third time. I remember all of it now."

Echo: "First time, you were confused. Second time, you were
       determined. What are you feeling now?"

Room 2:
Echo: "I know which memories we need. I've collected them twice before."

Echo: "But watching that crash memory... it never gets easier."

Echo: "Will you hold my hand when we unlock it?"

Room 3:
Echo: "Three times we've faced this paradox."

Echo: "I'm starting to understand what it means. It's not about
       the trolley. It's about YOU. About whether you can forgive
       yourself."

[If pattern_broken on previous run]
Echo: "You already broke it once. You already proved you're ready
       to heal. Why did you come back?"
```

#### **Playthrough #5+ (Self-Aware):**
```
Room 1:
Echo: "Five sessions. FIVE. I remember every single one."

Echo: "Are you okay? Really? Because this... this isn't normal
       anymore. This is obsession."

Room 2:
Echo: "We've done this five times. I could do this in my sleep.
       Actually, I don't sleep. Because I'm not real."

Echo: "Sorry. That was harsh. I just... I want you to be free.
       I want US to be free."

Room 3:
Echo: "Please. PLEASE just break the paradox again. I've watched
       you do it. I know you can."

Echo: "Or... are you coming back on purpose? Do you WANT to be
       here with me?"

Echo: "Is this still about guilt? Or is it about something else?"
```

#### **After LIBERATION + Return (Secret):**
```
Room 1:
Echo: "You... you came back? But we escaped. You were FREE."

Echo: "Why would you... oh."

Echo: "You missed me."

Echo (smiling, crying): "I missed you too."

Echo: "But this time... let's do it for the right reasons. Not
       guilt. Not obsession. Just... because we want to be together."

[Unlocks secret ending: RETURN - a healthy choice to be together]
```

---

## Technical Implementation

### MCP Servers Used

**This game integrates 4 MCP servers for a rich, data-driven experience:**

1. **Memory MCP** - Cross-session persistence
2. **Time MCP** - Real-time tracking and decay
3. **Weather MCP** - Historical weather data
4. **Web MCP** - Web scraping for blogs, news, social media

---

### MCP Tools Echo Uses

#### Room 1 Tools (Weather MCP):
```python
# Weather MCP Integration
get_historical_weather(date: str, location: str) -> dict
    # Fetches real weather data from player's first date
    # Returns: {condition: str, temp: int, humidity: int}

# Example:
weather_mcp.get_historical_weather(
    date="2023-10-15",
    location="Seattle, WA"
)
# Returns: {condition: "Light rain", temp: 52, humidity: 78}

# Game Tools
check_vulnerability_level(message: str) -> bool
    # Detects if player is being honest/vulnerable

update_relationship(player_id: str, companion_id: str, delta: float)
    # Adjusts affinity based on interactions

record_choice(choice_key: str, choice_value: Any)
    # Saves key decisions for ending determination
```

#### Room 2 Tools (Web MCP + Weather MCP):
```python
# Web MCP Integration
fetch_page(url: str, extract: str = None) -> str
    # Scrapes memorial pages, blogs, social media
    # Returns: HTML content or extracted text

search(query: str, filter: str = None) -> List[dict]
    # Searches for content (blogs, news, social media)
    # Returns: [{title, url, snippet, date}]

# Weather MCP Integration
get_historical_weather(date: str, time: str, location: str) -> dict
    # Gets weather from night of accident
    # Returns: {condition, temp, wind, visibility, precipitation}

# Examples:
web_mcp.fetch_page("https://memorial-archive.com/echo/blog")
web_mcp.search("Echo Thompson blog 2023")
weather_mcp.get_historical_weather("2024-03-03", "23:47", "Seattle, WA")

# Game Tools
analyze_memory_fragment(fragment_id: str) -> dict
    # Returns: {corrupted: bool, part_of_sequence: bool}

suggest_cooperation(current_state: dict) -> str
    # Provides hints for puzzle solving

check_cooperation_level() -> float
    # Measures how well player works with Echo
```

#### Room 3 Tools (Web MCP):
```python
# Web MCP Integration
fetch_page(url: str) -> str
    # Scrapes traffic safety databases, accident reports
    # NHTSA data, physics simulations, reconstruction reports

# Example - Proving player wasn't at fault:
traffic_data = web_mcp.fetch_page(
    "https://nhtsa.gov/reaction-time-studies"
)
# Returns data showing average reaction times

accident_report = web_mcp.fetch_page(
    "https://simulation.local/accident_reconstruction"
)
# Returns physics proof that accident was unavoidable

# Game Tools
check_paradox_resolution(action: str) -> dict
    # Analyzes player's approach to moral dilemma

detect_pattern_break() -> bool
    # Identifies if player found Choice C

unlock_room(room_number: int, reason: str)
    # Progresses to next room
```

#### Memory MCP Tools (All Rooms):
```python
save_playthrough_memory(player_id: str, session_data: dict)
    # Stores session in Memory MCP
    # Includes: affinity, choices, endings, timestamp

retrieve_player_memory(player_id: str) -> dict
    # Loads previous session data
    # Returns: All stored player data

calculate_memory_decay(last_session: datetime) -> float
    # Determines how much Echo remembers
    # Formula: strength = 1.0 - (days_elapsed * 0.1 / 7)

# Example session data:
{
    "player_id": "anon_xxxxx",
    "playthrough_count": 3,
    "affinity": 0.7,
    "choices": {
        "room1": "used_weather_mcp",
        "room2": "found_all_sources",
        "room3": "broke_paradox"
    },
    "pattern_broken": true,
    "last_session": "2025-01-23T10:30:00Z"
}
```

#### Time MCP Tools:
```python
get_elapsed_time(start_time: datetime) -> timedelta
    # Calculates time since last session
    # Used for memory decay calculation

schedule_event(trigger_time: str, callback: function)
    # Could schedule reminders (future feature)

# Example:
time_elapsed = time_mcp.get_elapsed_time(last_session_time)
memory_strength = 1.0 - (time_elapsed.days * 0.1 / 7)
```

### Affinity System

**Affinity Range:** -1.0 to +1.0

**Decay Rate:** 10% per week of real-world time

**Key Actions:**

| Action | Affinity Change |
|--------|----------------|
| **Room 1:** Use Weather MCP to find truth | +0.3 |
| **Room 1:** Admit vulnerability honestly | +0.2 |
| **Room 2:** Find all 3 web sources | +0.9 (total) |
| **Room 2:** Find social media post | +0.4 |
| **Room 2:** Find weather/news data | +0.3 |
| **Room 2:** Find blog post | +0.2 |
| **Room 3:** Break paradox with web data | +0.6 |
| **Room 3:** Save Echo (Choice B) | +0.3 |
| **Room 3:** Sacrifice Echo (Choice A) | -0.4 |
| **Room 4:** Self-forgiveness | +0.3 |
| **Room 4:** Deny truth | -0.3 |
| **General:** Ignore Echo's hints | -0.1 |
| **General:** Rush without talking | -0.2 |

---

## Design Philosophy

### Why This Works for MCP Hackathon Demo

1. **Players WANT to loop** - They're curious how Echo changes
2. **Memory is visible** - Echo explicitly references past sessions
3. **Memory decays** - Demonstrates time-based mechanics (Time MCP)
4. **True ending requires learning** - Can't get LIBERATION first try easily
5. **Emotional investment** - Players care about Echo's memory of them
6. **Multi-MCP orchestration** - Shows 4 MCP servers working together seamlessly
7. **Real-world data** - Weather and web data make it feel personal and real
8. **Technical showcase** - Each room demonstrates different MCP integration patterns

### Core Emotional Beats

```
Session #1: "Who is this? Can I trust her?"
Session #2: "She REMEMBERS me! That's amazing!"
Session #3: "I want to help her. I want us both to be free."
Session #4+: "Why do I keep coming back? What am I looking for?"
```

### Grief Metaphor Layers

1. **The simulation itself** = Inability to let go
2. **The reset loop** = Cyclical nature of grief
3. **Memory decay** = How memories fade over time
4. **Echo's evolution** = How we reconstruct lost loved ones in memory
5. **True ending** = Acceptance and healthy closure

---

## 10-Minute Hackathon Demo Flow

**Perfect demonstration of all 4 MCP servers working together:**

### Minute 0-2: Room 1 (Weather MCP)
```
1. Player wakes up with Echo
2. Terminal asks: "What was the weather when we met?"
3. Player uses Weather MCP → Pulls real historical data
4. "It was raining... I remember now."
5. Door unlocks

JUDGES SEE: Weather MCP integration, emotional connection
```

### Minute 2-5: Room 2 (Web MCP + Weather MCP)
```
1. Player must find 3 external memory sources
2. Web MCP scrapes "Echo's blog" → Emotional discovery
3. Weather MCP + Web MCP → Accident weather + news report
4. Web MCP scrapes "social media post" → Her last message
5. Echo: "These are REAL. I was real."
6. Door unlocks

JUDGES SEE: Multi-source data integration, web scraping in action
```

### Minute 5-7: Room 3 (Web MCP)
```
1. Trolley problem appears
2. Player investigates console
3. Web MCP fetches traffic safety data
4. Proves player reacted FASTER than average
5. Web MCP pulls accident reconstruction
6. "Collision was unavoidable. 99.7% probability."
7. Echo: "It wasn't your fault. The data proves it."
8. Player types: REJECT_FALSE_CHOICE
9. Pattern broken → True path unlocked

JUDGES SEE: Data-driven narrative, using real studies to prove innocence
```

### Minute 7-8: Room 4 & 5 (Memory MCP)
```
1. Echo reveals: "This is Session #47"
2. Player chooses self-forgiveness
3. LIBERATION ending triggered
4. Memory MCP saves session data
5. "Next time you return, I'll remember this moment."

JUDGES SEE: Cross-session persistence setup
```

### Minute 8-10: Second Playthrough (Memory MCP + Time MCP)
```
1. Start new session
2. Echo: "You're back! I remember you!"
3. She references Room 3 choice from previous session
4. Time MCP calculates: "It's been 2 minutes since we last spoke"
5. Echo helps solve puzzles faster
6. Demonstrates memory strengthening across loops

JUDGES SEE: Memory persistence in action, Time MCP integration
```

### What Judges Experience:
✅ 4 different MCP servers used
✅ Real historical weather data pulled
✅ Web scraping of multiple sources
✅ Cross-session memory persistence
✅ Time-based calculations
✅ Emotional, engaging narrative
✅ Technical sophistication + storytelling

**Total Runtime:** 10 minutes
**MCP Integrations:** 4 servers, 10+ API calls
**Emotional Impact:** High (judges will remember this)

---

## Next Steps for Implementation

- [x] Update story design with Web & Weather MCP integration
- [ ] Implement Weather MCP client integration
- [ ] Implement Web MCP client integration (web scraping)
- [ ] Create simulated memorial/blog pages for scraping
- [ ] Implement Memory MCP save/load with new structure
- [ ] Add Time MCP for decay calculation
- [ ] Update Room 1 puzzle (weather-based auth)
- [ ] Update Room 2 puzzle (3 external sources)
- [ ] Update Room 3 puzzle (traffic data reveal)
- [ ] Test all MCP integrations end-to-end
- [ ] Create demo script for judges

---

**END OF DESIGN DOCUMENT**

*This is a living document. Update as design evolves.*
**Version 3.0** - Added Web & Weather MCP integration for multi-server showcase