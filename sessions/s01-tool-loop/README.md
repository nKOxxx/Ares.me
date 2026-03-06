# Session 01: Tool Loop

> **"One loop & bash is all you need"**

Welcome to Session 01! This is where every AI agent begins — with a simple loop that can use tools.

## 🎯 What You'll Build

A minimal AI agent in **~50 lines of Python** that can:
- Accept messages from you (the user)
- Decide whether to respond directly or use a tool
- Execute tools (like checking weather)
- Loop back and continue the conversation

By the end of this session, you'll understand the **atomic unit** of every AI agent on Earth — from ChatGPT to Claude Code.

---

## 🤔 Why This Matters

Every AI agent, no matter how complex, uses this same pattern:

```
┌─────────────────────────────────────────┐
│           THE AGENT LOOP                │
├─────────────────────────────────────────┤
│                                         │
│  1. User sends a message                │
│     ↓                                   │
│  2. Agent sends to LLM (AI brain)       │
│     ↓                                   │
│  3. LLM responds:                       │
│     ├─ "Here's the answer" → DONE       │
│     └─ "Use the weather tool" →         │
│         ↓                               │
│  4. Execute the tool                    │
│     ↓                                   │
│  5. Send result back to LLM             │
│     ↓                                   │
│  6. Loop to step 2                      │
│                                         │
└─────────────────────────────────────────┘
```

This loop is everything. Master it, and you understand 80% of AI agents.

---

## 🚀 Quick Start

### For Beginners

**Step 1:** Open your terminal (Command Prompt on Windows, Terminal on Mac)

**Step 2:** Navigate to this folder
```bash
cd sessions/s01-tool-loop
```

**Step 3:** Run the agent
```bash
# Windows
python agent.py

# Mac/Linux (might need python3)
python3 agent.py
```

**Step 4:** Try these commands:
```
You: What's the weather in London?
Agent: The weather in London is sunny, 22°C

You: Hello
Agent: I processed your message: Hello

You: exit
```

### For Experienced Developers

```bash
cd sessions/s01-tool-loop
python agent.py
```

No dependencies required. Pure Python 3.11+.

---

## 📖 Code Walkthrough

### The Full Code (`agent.py`)

```python
#!/usr/bin/env python3
"""
Session 01: Tool Loop
The minimal AI agent pattern.
"""

import json
from typing import List, Dict, Any


def mock_llm(messages: List[Dict], tools: List[Dict]) -> Dict:
    """
    Simulates an LLM that can use tools.
    
    In production: Replace this with a real API call to OpenAI, 
    Anthropic, or your preferred provider.
    """
    last_message = messages[-1]["content"]
    
    # Simple pattern matching for demo
    if "weather" in last_message.lower():
        return {
            "role": "assistant",
            "content": [{"type": "tool_use", "name": "get_weather", "input": {"city": "London"}}]
        }
    
    return {
        "role": "assistant", 
        "content": [{"type": "text", "text": "I processed your message: " + last_message}]
    }


def get_weather(city: str) -> str:
    """Simulates getting weather."""
    return f"The weather in {city} is sunny, 22°C"


def execute_tools(tool_calls: List[Dict]) -> List[Dict]:
    """Execute tools and return results."""
    results = []
    handlers = {
        "get_weather": get_weather
    }
    
    for call in tool_calls:
        name = call.get("name")
        handler = handlers.get(name)
        if handler:
            output = handler(**call.get("input", {}))
            results.append({
                "type": "tool_result",
                "tool_use_id": call.get("id"),
                "content": output
            })
    
    return results


def agent_loop(user_input: str) -> str:
    """
    The core agent loop.
    
    This is the heart of every AI agent. It:
    1. Adds the user's message to the conversation
    2. Asks the LLM what to do
    3. If the LLM wants to use tools → execute them → loop back
    4. If the LLM is done → return the answer
    """
    # Initialize the conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to tools."},
        {"role": "user", "content": user_input}
    ]
    
    # Define available tools
    tools = [{
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }]
    
    # THE LOOP
    while True:
        # Get response from LLM
        response = mock_llm(messages, tools)
        messages.append({"role": "assistant", "content": response["content"]})
        
        # Check if we should stop
        tool_calls = [c for c in response["content"] if c.get("type") == "tool_use"]
        
        if not tool_calls:
            # No tool calls — return the text response
            text_parts = [c.get("text", "") for c in response["content"] if c.get("type") == "text"]
            return "".join(text_parts)
        
        # Execute tools and add results
        results = execute_tools(tool_calls)
        messages.append({"role": "user", "content": results})


def main():
    print("⚔️ Ares Session 01: Tool Loop")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ("exit", "quit"):
            break
        
        if not user_input:
            continue
        
        response = agent_loop(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
```

---

## 🔍 Understanding the Code

### 1. The `mock_llm()` Function

```python
def mock_llm(messages: List[Dict], tools: List[Dict]) -> Dict:
```

**What it does:** Pretends to be an AI (like ChatGPT)

**Why we mock it:** So you can run the code without API keys. In production, you'd replace this with:

```python
# Using OpenAI
import openai

def real_llm(messages, tools):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        tools=tools
    )
    return response
```

### 2. The `get_weather()` Function

```python
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny, 22°C"
```

**What it does:** Pretends to check the weather

**In production:** You'd call a real weather API:

```python
import requests

def get_weather(city: str) -> str:
    response = requests.get(f"https://api.weather.com/v1/current?city={city}")
    data = response.json()
    return f"{data['temp']}°C, {data['condition']}"
```

### 3. The `execute_tools()` Function

```python
def execute_tools(tool_calls: List[Dict]) -> List[Dict]:
    handlers = {"get_weather": get_weather}
    
    for call in tool_calls:
        handler = handlers.get(call["name"])
        output = handler(**call["input"])
        # ... return result
```

**What it does:** Looks up the tool by name and runs it

**Why it matters:** This is how the LLM "does things" in the real world

### 4. The `agent_loop()` Function — THE CORE

```python
def agent_loop(user_input: str) -> str:
    messages = [...]  # Initialize conversation
    
    while True:  # ← THE LOOP
        response = mock_llm(messages, tools)
        
        if no_tool_calls:
            return response  # Done!
        
        results = execute_tools(tool_calls)
        messages.append(results)  # ← Loop back
```

**What it does:**
1. Starts with your message
2. Asks the LLM "what should I do?"
3. If LLM says "use a tool" → runs the tool → asks again
4. If LLM says "here's the answer" → returns it to you

**The magic:** The loop keeps going until the agent is done. It might use 1 tool or 10 tools. The loop doesn't care.

---

## 🛠️ Try It Yourself

### Exercise 1: Add a Calculator

Add this tool to make your agent do math:

```python
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"

# Add to handlers
handlers = {
    "get_weather": get_weather,
    "calculator": calculator,  # ← Add this
}

# Add tool definition
tools = [
    # ... existing weather tool ...
    {
        "name": "calculator",
        "description": "Calculate math expressions",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    }
]
```

Then test it:
```
You: What is 2 + 2?
Agent: Result: 4
```

### Exercise 2: Connect to Real AI

Replace `mock_llm()` with a real API call:

```bash
# Install OpenAI
pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def real_llm(messages, tools):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return response.choices[0].message
```

Set your API key:
```bash
# Mac/Linux
export OPENAI_API_KEY="your-key-here"

# Windows
set OPENAI_API_KEY=your-key-here
```

---

## 🎓 Key Takeaways

### 1. The Loop is Everything
```
User → LLM → (Tool → LLM → Tool → LLM) → Answer
```

Every agent, from simple to complex, uses this pattern.

### 2. Tools = Superpowers
Without tools, an AI can only talk. With tools, it can:
- Search the web
- Run code
- Send emails
- Control your computer
- Order pizza (seriously)

### 3. Messages = Memory (for now)
The `messages` array holds the conversation. But when the program ends, it's gone! (We'll fix this in Session 04)

---

## ❓ Troubleshooting

### "NameError: name 'List' is not defined"
Make sure you have this import at the top:
```python
from typing import List, Dict, Any
```

### "ModuleNotFoundError: No module named 'openai'"
You don't need OpenAI for this session! The code uses `mock_llm()`. If you want to use real AI:
```bash
pip install openai
```

### "IndentationError: unexpected indent"
Python is picky about spaces. Make sure you're using 4 spaces per indent, not tabs.

---

## 🚀 Next Steps

Ready for more tools? Go to [Session 02: Multi-Tool Architecture](../s02-multi-tool/)

There you'll learn:
- How to add unlimited tools
- How to keep the loop unchanged
- How to handle tool errors

---

<p align="center">
  <i>Session 01 of 12 ⚔️</i><br>
  <a href="../../">Home</a> •
  <a href="../s02-multi-tool/">Next Session →</a>
</p>
