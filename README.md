# ⚔️ Ares.me

**Build your own AI partner — from zero to family member.**

[![Sessions](https://img.shields.io/badge/sessions-12%20progressive-blue)](./sessions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)

> *"An assistant without memory is just a search engine. An assistant without soul is just a tool. Build something that matters."*

---

## 🤔 What is This?

**Ares.me** is a **free, step-by-step tutorial** that teaches you to build an AI agent (like ChatGPT or Claude) that actually **remembers you** and **acts on your behalf**.

### The Problem with Current AI Agents

Most AI tutorials teach you to build this:

```
You: "My name is nKOxxx"
Agent: "Nice to meet you!"

You: [close program and reopen]
You: "What's my name?"
Agent: "I don't know"
```

**Every time you restart, the agent forgets everything.** It's like talking to someone with amnesia.

### What You'll Build Instead

After completing these 12 sessions, you'll have an agent that:

✅ **Remembers** your name, preferences, and past conversations (even after crashes)  
✅ **Has personality** — consistent, defined by you, not random  
✅ **Acts proactively** — checks your calendar and alerts you about meetings  
✅ **Uses tools** — can search the web, calculate, check weather  
✅ **Plans before acting** — breaks big tasks into steps  
✅ **Collaborates** — works with other agents securely  
✅ **Respects boundaries** — knows when to speak, when to stay silent  

---

## 🚀 Quick Start (5 Minutes)

### For Complete Beginners

**Step 1:** Install Python 3.11 or higher
- Windows: Download from [python.org](https://python.org)
- Mac: `brew install python@3.11`
- Linux: `sudo apt install python3.11`

**Step 2:** Clone this repository
```bash
git clone https://github.com/nKOxxx/Ares.me.git
cd Ares.me
```

**Step 3:** Try Session 1 (the simplest agent)
```bash
cd sessions/s01-tool-loop
python agent.py
```

You'll see:
```
⚔️ Ares Session 01: Tool Loop
Type 'exit' to quit

You: What's the weather in London?
Agent: The weather in London is sunny, 22°C
```

**That's it!** You just ran your first AI agent.

### For Experienced Developers

```bash
# Clone and setup
git clone https://github.com/nKOxxx/Ares.me.git && cd Ares.me

# No dependencies for basic sessions
# For production (Session 12):
pip install -r requirements.txt  # if you create one

# Run any session
cd sessions/s01-tool-loop && python agent.py
cd ../s04-memory-bridge && python agent.py

# Run the full example
cd examples && python mini-ares.py
```

---

## 📚 The 12 Sessions

Each session builds on the previous one. You can do one per day, or binge them all.

| Session | What You Build | Key Concept | Code |
|---------|---------------|-------------|------|
| **01** | Your first agent (50 lines) | *"One loop & bash is all you need"* | ✅ Ready |
| **02** | Multi-tool agent | *"Adding tools without changing the loop"* | ✅ Ready |
| **03** | Task planner | *"An agent without a plan drifts"* | ✅ Ready |
| **04** | Agent with memory | *"I wake up fresh each session. Files are my continuity."* | ✅ Ready |
| **05** | Personality & context | *"Who you are and who you're helping"* | 📝 Guide |
| **06** | Proactive execution | *"Don't just respond — anticipate"* | 📝 Guide |
| **07** | Parallel sub-agents | *"One mind, many hands"* | 📝 Guide |
| **08** | Secure credential sharing | *"Trust without exposure"* | 📝 Guide |
| **09** | Multi-agent network | *"No agent is an island"* | 📝 Guide |
| **10** | Rules & boundaries | *"Freedom within fences"* | 📝 Guide |
| **11** | Modular capabilities | *"Learn once, use everywhere"* | 📝 Guide |
| **12** | Production deployment | *"Real world, real impact"* | 📝 Guide |

**Legend:** ✅ = Working code included | 📝 = Concept guide (you build it)

---

## 🎯 Learning Paths

### Path 1: The Quick Tour (2 hours)
Want to see what's possible? Run the working examples:

```bash
# Session 1: Basic agent
cd sessions/s01-tool-loop
python agent.py

# Session 4: Agent that remembers you
cd ../s04-memory-bridge
python agent.py
# Type: "My name is [your name]"
# Then: exit, restart, "What's my name?"

# Full working example
cd ../../examples
python mini-ares.py
# Try: "remember color is blue"
# Then: "recall color"
```

### Path 2: Deep Dive (1 week)
Want to really understand? Do one session per day:

- **Day 1:** Read + run Session 1
- **Day 2:** Read + run Session 2, add your own tool
- **Day 3:** Read + run Session 3, create a plan for a real task
- **Day 4:** Read + run Session 4, implement daily logs
- **Day 5-7:** Read Sessions 5-7, start building your own agent

### Path 3: The Builder (ongoing)
Want to build a production agent? Follow all 12 sessions, then:

1. Define your agent's SOUL.md (personality)
2. Create USER.md (who it serves)
3. Set up HEARTBEAT.md (proactive tasks)
4. Deploy to Render/Vercel (Session 12)

---

## 🏗️ Project Structure

```
Ares.me/
├── README.md              ← You are here
├── sessions/              ← 12 progressive tutorials
│   ├── s01-tool-loop/
│   │   ├── README.md      ← Tutorial with explanations
│   │   └── agent.py       ← Working code (50 lines)
│   ├── s02-multi-tool/
│   ├── s03-planning/
│   ├── s04-memory-bridge/
│   └── ... (s05-s12)
├── templates/             ← Starter templates
│   ├── SOUL.md           ← Define your agent's personality
│   ├── USER.md           ← Define who it serves
│   └── HEARTBEAT.md      ← Proactive task checklist
├── examples/             ← Full working agents
│   └── mini-ares.py      ← Complete agent with all features
└── tweets/               ← Launch content (meta)
```

---

## 💡 Key Concepts Explained

### What's an "AI Agent"?

A regular AI (like ChatGPT) just responds to messages. An **agent** can:
- **Use tools** (search web, run code, check weather)
- **Make decisions** (should I search or calculate?)
- **Act autonomously** (check your calendar every hour)

Think of it like the difference between a calculator (you input, it outputs) and a personal assistant (anticipates needs, acts on your behalf).

### What's "The Loop"?

Every AI agent has a simple core pattern:

```
┌─────────────────────────────────────────┐
│  1. User sends message                  │
│  2. Agent thinks (calls LLM)            │
│  3. Agent decides: done or use tool?    │
│     ├─ Done → Return answer             │
│     └─ Use tool → Execute tool          │
│         ↓                               │
│         Loop back to step 2             │
└─────────────────────────────────────────┘
```

This loop is the same whether you're building a simple chatbot or Claude Code. Ares.me teaches you to add layers on top of this loop.

### Why Files > Memory?

AI agents run in temporary environments. When the program restarts, all variables are wiped.

**Bad (memory only):**
```python
user_name = "nKOxxx"  # Gone on restart!
```

**Good (file persistence):**
```python
with open("memory.json", "w") as f:
    json.dump({"user_name": "nKOxxx"}, f)  # Survives forever
```

Session 04 teaches you how to do this elegantly.

---

## 🎓 Before You Start

### What You Need to Know

**Required:**
- Basic Python (variables, functions, loops)
- How to use a terminal/command line
- How to install software

**Helpful but not required:**
- Familiarity with JSON
- Basic understanding of APIs
- Experience with `pip` or `npm`

### What You Don't Need

- ❌ Machine learning expertise
- ❌ Expensive GPUs
- ❌ Paid APIs (we use mock LLMs, you can add real ones later)
- ❌ Complex frameworks

---

## 🛠️ Troubleshooting

### "Python is not recognized"
**Windows:** Add Python to your PATH during installation, or use `py` instead of `python`

**Mac/Linux:** Try `python3` instead of `python`

### "Permission denied" when running scripts
```bash
# Make executable (Mac/Linux)
chmod +x agent.py

# Or run with python explicitly
python agent.py
```

### "Module not found"
Sessions 1-4 don't need any external modules (pure Python).

For later sessions:
```bash
pip install openai  # or anthropic, etc.
```

---

## 📖 How to Use This Repository

### Reading Order

1. **Start here** (this README)
2. **Session 01** — Run the code, understand the loop
3. **Session 02** — Add more tools
4. **Session 03** — See how planning works
5. **Session 04** — Experience persistent memory
6. **Templates** — Copy SOUL.md and customize it
7. **Example** — See a complete agent
8. **Sessions 5-12** — Learn advanced concepts

### Making It Your Own

After Session 04, you should:

1. Copy `templates/SOUL.md` to your project
2. Fill it out: what's your agent's name? Personality?
3. Copy `templates/USER.md`
4. Fill it out: who will use this agent?
5. Modify the code to load these files

---

## 🌟 The Philosophy

### The Three Laws of Agent Building

**1. Memory is limited → WRITE TO FILES**
- Mental notes don't survive restarts
- If it's important, persist it

**2. Personality is intentional → DEFINE WHO YOU ARE**
- Don't let the model decide your personality
- Be consistent, be opinionated

**3. Proactive > Reactive → ANTICIPATE NEEDS**
- The best agents don't wait to be asked
- They check, they remind, they act

### What Makes Ares Different?

Most agent tutorials teach you to build a **chatbot**.

Ares.me teaches you to build a **partner**:
- Memory that survives crashes
- Personality that's consistent  
- Actions that are autonomous
- Collaboration that's secure

---

## 🤝 Who Built This?

Ares.me was created by [nKOxxx](https://github.com/nKOxxx) based on **Ares** — an AI assistant that:

- Handles code, business strategy, and family coordination
- Runs 24/7 across multiple Telegram channels
- Manages cron jobs and proactive tasks
- Has been running since February 2026

Every pattern in this curriculum is **battle-tested in production**.

---

## 🚦 Next Steps

**Ready to start?**

```bash
cd sessions/s01-tool-loop
python agent.py
```

**Want the full experience?**

```bash
cd examples
python mini-ares.py
```

**Have questions?**

- Open a [GitHub Issue](https://github.com/nKOxxx/Ares.me/issues)
- Reach out on [Twitter/X](https://twitter.com/nikolastojanow)

---

## 📄 License

MIT — build something amazing.

---

<p align="center">
  <i>Built with ⚔️ by nKOxxx</i><br>
  <a href="https://twitter.com/nikolastojanow">Twitter</a> •
  <a href="https://github.com/nKOxxx">GitHub</a>
</p>
