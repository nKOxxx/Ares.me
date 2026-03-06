# Examples

This folder contains complete, working AI agents that demonstrate the concepts from the sessions.

## 🚀 Quick Start

### Mini-Ares (Recommended First)

A complete agent with personality, memory, and planning in one file.

```bash
cd examples
python mini-ares.py
```

**What to try:**
```
You: remember color is blue
Agent: ✅ Remembered: color = blue

You: recall color
Agent: 📚 color: blue

You: plan build a website
Agent: 📋 Plan for 'build a website':
   1. Analyze: build a website
   2. Gather requirements
   ...

You: who are you
Agent: ⚔️ MiniAres
   Role: Helpful Assistant
   Values: Be direct, Be proactive, Be useful
```

**Why it's useful:**
- Shows how Session 4 (memory) works in practice
- Demonstrates command parsing
- Simple enough to understand, complex enough to be useful

---

## 📁 Available Examples

| Example | Sessions Used | Complexity | Best For |
|---------|--------------|------------|----------|
| **mini-ares.py** | 1, 2, 3, 4, 5 | Medium | Understanding the full picture |

---

## 🛠️ Creating Your Own

Want to build on these examples?

### Step 1: Copy the File
```bash
cp mini-ares.py my-agent.py
```

### Step 2: Customize the Soul

Edit the `SOUL.json` that gets created:

```json
{
  "name": "MyBot",
  "role": "Code Assistant",
  "emoji": "🤖",
  "values": ["Write clean code", "Explain clearly"]
}
```

### Step 3: Add Your Tools

Add new functions to the agent:

```python
def read_file(path: str) -> str:
    """Read a file's contents."""
    with open(path) as f:
        return f.read()

# Register it
self.tools["read_file"] = read_file
```

### Step 4: Run It

```bash
python my-agent.py
```

---

## 🎓 Learning Path

**Beginners:** Start with mini-ares.py to see what's possible, then go back to Session 01 to understand how it works.

**Experienced:** Use mini-ares.py as a template and extend it with features from Sessions 5-12.

---

<p align="center">
  <i>Examples folder ⚔️</i><br>
  <a href="../">← Back to Ares.me</a>
</p>
