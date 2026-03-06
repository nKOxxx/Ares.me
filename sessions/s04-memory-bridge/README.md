# Session 04: Memory Bridge

> **"I wake up fresh each session. Files are my continuity."**

This is where we solve the biggest problem in AI agents: **amnesia**. By the end of this session, your agent will remember things across restarts.

## 🎯 What You'll Build

An agent with **persistent memory** that:
- Remembers your name even after you close the program
- Stores facts in files (survives crashes)
- Distinguishes between short-term and long-term memory
- Forgets things when you tell it to

---

## 🚨 The Problem

### Try This in a Regular Chatbot

```python
# Run 1
You: My name is Nikola
Agent: Nice to meet you, Nikola!
[You close the program]

# Run 2 (after restart)
You: What's my name?
Agent: I don't have that information.
```

**Why this happens:** The agent stores everything in RAM (variables). When the program exits, RAM is cleared. Everything is lost.

### The Real-World Impact

Imagine a personal assistant that:
- ❌ Forgets your dietary restrictions every morning
- ❌ Doesn't remember you have a meeting at 2pm
- ❌ Can't recall that you prefer email over Slack
- ❌ Starts fresh every single day

That's useless. We need **persistence**.

---

## 💡 The Solution: File-Based Memory

### Memory Hierarchy

```
┌─────────────────────────────────────────┐
│           AGENT MEMORY                  │
├─────────────────────────────────────────┤
│                                         │
│  🧠 SHORT-TERM (RAM)                    │
│     • This session only                 │
│     • Fast access                       │
│     • Lost on exit                      │
│                                         │
│  💾 LONG-TERM (Files)                   │
│     • Survives restarts                 │
│     • Slower (disk I/O)                 │
│     • JSON storage                      │
│                                         │
└─────────────────────────────────────────┘
```

### The Magic

```python
# Instead of this (lost on exit):
user_name = "Nikola"  # Gone!

# Do this (saved forever):
with open("memory.json", "w") as f:
    json.dump({"user_name": "Nikola"}, f)

# Later, load it back:
with open("memory.json", "r") as f:
    data = json.load(f)
    user_name = data["user_name"]  # "Nikola" restored!
```

---

## 🚀 Quick Start

### Run It

```bash
cd sessions/s04-memory-bridge
python agent.py
```

### The Memory Test

**Step 1:** Tell the agent your name
```
You: My name is Alice
Agent: Nice to meet you, Alice!
  [Memory: stored user_name = Alice]
```

**Step 2:** Ask what it knows
```
You: What is my name?
Agent: Your name is Alice.
```

**Step 3:** Exit and restart
```
You: exit

[Run python agent.py again]
```

**Step 4:** Check if it remembers
```
📚 Previous memories loaded:
  - user_name: Alice

You: What is my name?
Agent: Your name is Alice.
```

🎉 **It remembers!** Even though you restarted the program.

---

## 📖 Code Walkthrough

### The MemoryBridge Class

```python
class MemoryBridge:
    """
    Simple file-based memory system.
    
    Every session starts fresh, but we persist
    the important stuff to files.
    """
    
    def __init__(self, memory_dir: str = "memory"):
        # Create memory folder
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Two types of memory
        self.short_term: Dict[str, Any] = {}  # This session only
        self.long_term: Dict[str, Any] = {}   # Persisted to disk
        
        # Load any existing memories
        self._load()
```

**What it does:**
- Creates a `memory/` folder to store data
- Sets up two memory types (short and long term)
- Automatically loads previous memories

### Storing Memories

```python
def remember(self, key: str, value: Any, persistent: bool = True):
    """
    Store a memory.
    
    Args:
        key: What to remember (e.g., "user_name")
        value: The data (e.g., "Alice")
        persistent: If True, survives restarts
    """
    if persistent:
        # Save to file
        self.long_term[key] = {
            "value": value,
            "stored_at": datetime.now().isoformat()
        }
        self._save()  # Write to disk immediately
    else:
        # Keep in RAM only
        self.short_term[key] = value
```

**Usage examples:**

```python
# Persistent (survives restart)
memory.remember("user_name", "Alice")        # Saved to file
memory.remember("preferences", {"theme": "dark"})  # Saved to file

# Temporary (lost on exit)
memory.remember("draft_email", "Hi...", persistent=False)  # RAM only
memory.remember("temp_calculation", 42, persistent=False)  # RAM only
```

### Retrieving Memories

```python
def recall(self, key: str) -> Optional[Any]:
    """Retrieve a memory."""
    # Check short-term first (faster)
    if key in self.short_term:
        return self.short_term[key]
    
    # Then check long-term (slower, from disk)
    if key in self.long_term:
        return self.long_term[key]["value"]
    
    return None  # Not found
```

**Why check short-term first?** It's faster (RAM vs disk).

### The Save/Load Mechanism

```python
def _save(self):
    """Save long-term memory to disk."""
    memory_file = self.memory_dir / "memory.json"
    with open(memory_file, 'w') as f:
        json.dump(self.long_term, f, indent=2)

def _load(self):
    """Load long-term memory from disk."""
    memory_file = self.memory_dir / "memory.json"
    if memory_file.exists():
        with open(memory_file, 'r') as f:
            self.long_term = json.load(f)
```

**Why JSON?**
- Human-readable
- Universal format
- Easy to debug
- Works with any programming language

---

## 🔍 The Full Memory Flow

```
┌──────────────────────────────────────────────────────┐
│                  USER SAYS:                          │
│            "My name is Alice"                        │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│              AGENT PROCESSES INPUT                   │
│                                                      │
│  1. Detects pattern "my name is [name]"             │
│  2. Extracts "Alice"                                 │
│  3. Calls: memory.remember("user_name", "Alice")    │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│              MEMORY BRIDGE SAVES                     │
│                                                      │
│  1. Stores in self.long_term["user_name"]            │
│  2. Adds timestamp                                   │
│  3. Calls _save() → writes to memory.json           │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│              FILE SYSTEM                             │
│                                                      │
│  memory.json now contains:                           │
│  {                                                   │
│    "user_name": {                                    │
│      "value": "Alice",                               │
│      "stored_at": "2026-03-06T10:30:00"             │
│    }                                                 │
│  }                                                   │
└──────────────────────────────────────────────────────┘
```

---

## 🛠️ Exercises

### Exercise 1: Add Memory Categories

Organize memories by type:

```python
def remember(self, key: str, value: Any, category: str = "general", persistent: bool = True):
    if persistent:
        self.long_term[key] = {
            "value": value,
            "category": category,  # NEW
            "stored_at": datetime.now().isoformat()
        }
        self._save()

# Usage:
memory.remember("user_name", "Alice", category="user")
memory.remember("favorite_color", "blue", category="preferences")
memory.remember("api_key", "secret", category="secrets")
```

### Exercise 2: Memory Search

Find memories by partial key:

```python
def search(self, query: str) -> List[Dict]:
    """Search memories by key."""
    results = []
    for key, data in self.long_term.items():
        if query.lower() in key.lower():
            results.append({
                "key": key,
                "value": data["value"],
                "stored_at": data["stored_at"]
            })
    return results

# Usage:
results = memory.search("user")
# Returns: [{"key": "user_name", "value": "Alice", ...}]
```

### Exercise 3: Daily Logs

Create a new memory file for each day:

```python
from datetime import date

def log_daily(self, event: str):
    """Log something that happened today."""
    today = date.today().isoformat()  # "2026-03-06"
    log_file = self.memory_dir / f"{today}.json"
    
    # Load existing log or create new
    if log_file.exists():
        with open(log_file) as f:
            log = json.load(f)
    else:
        log = {"events": []}
    
    # Add event
    log["events"].append({
        "time": datetime.now().isoformat(),
        "event": event
    })
    
    # Save
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)

# Usage:
memory.log_daily("User mentioned preferring email")
# Creates: memory/2026-03-06.json
```

---

## 🎓 Production Patterns

### Pattern 1: The Memory Directory Structure

```
memory/
├── memory.json          # Core long-term memories
├── 2026-03-06.json      # Today's log
├── 2026-03-05.json      # Yesterday's log
├── SOUL.json            # Agent personality
└── USER.json            # User preferences
```

### Pattern 2: Memory with Context Injection

```python
class Agent:
    def __init__(self):
        self.memory = MemoryBridge()
        
        # Load memories into system prompt
        memories = self.memory.get_all()
        context = self._format_context(memories)
        
        self.system_prompt = f"""
        You are a helpful assistant.
        
        CONTEXT FROM PREVIOUS CONVERSATIONS:
        {context}
        """
    
    def _format_context(self, memories):
        lines = []
        for key, value in memories.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
```

**Why this works:** The LLM "remembers" by reading the context you provide.

### Pattern 3: Memory Cleanup

```python
def cleanup_old_memories(self, days: int = 30):
    """Remove memories older than N days."""
    cutoff = datetime.now() - timedelta(days=days)
    
    to_delete = []
    for key, data in self.long_term.items():
        stored = datetime.fromisoformat(data["stored_at"])
        if stored < cutoff:
            to_delete.append(key)
    
    for key in to_delete:
        del self.long_term[key]
    
    self._save()
```

---

## 🚨 Common Pitfalls

### Pitfall 1: Saving Everything

**Don't:**
```python
# Bad: Saving every message
memory.remember(f"msg_{len(messages)}", message)
# Creates huge files, slows everything down
```

**Do:**
```python
# Good: Only save important facts
memory.remember("user_name", extracted_name)
memory.remember("meeting_time", extracted_time)
```

### Pitfall 2: Blocking on Save

**Don't:**
```python
# Bad: Save after every memory (slow)
for fact in facts:
    memory.remember(fact)  # Writes to disk every time!
```

**Do:**
```python
# Good: Batch saves
for fact in facts:
    memory.long_term[fact] = value
memory._save()  # One write at the end
```

### Pitfall 3: No Backup

**Don't:** Rely on a single file

**Do:**
```python
# Make backups
import shutil
from datetime import datetime

def backup_memory(self):
    backup_name = f"memory_backup_{datetime.now().isoformat()}.json"
    shutil.copy(self.memory_file, self.memory_dir / backup_name)
```

---

## 🚀 Next Steps

Ready for personality? Go to [Session 05: Soul & User](../s05-soul-user/)

There you'll learn:
- How to give your agent a consistent personality
- How to define who it serves
- How to use SOUL.md and USER.md

---

<p align="center">
  <i>Session 04 of 12 ⚔️</i><br>
  <a href="../s03-planning/">← Previous</a> •
  <a href="../../">Home</a> •
  <a href="../s05-soul-user/">Next →</a>
</p>
