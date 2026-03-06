# Session 01: Tool Loop

> **"One loop & bash is all you need"**

## What You Build

A minimal AI agent in **~50 lines of Python** that can:
- Accept user input
- Call tools (functions)
- Loop until done

This is the atomic unit of every AI agent. Master this, and you understand the foundation.

## The Core Pattern

```python
def agent_loop(messages):
    while True:
        response = llm.chat(messages)
        messages.append({"role": "assistant", "content": response})
        
        if not response.has_tool_calls():
            return response.text
        
        results = execute_tools(response.tool_calls)
        messages.append({"role": "user", "content": results})
```

That's it. Every production agent builds on this loop.

## The Code

### `agent.py`

```python
#!/usr/bin/env python3
"""
Session 01: Tool Loop
The minimal AI agent pattern.
"""

import json
import os
from typing import List, Dict, Any

# Minimal "LLM" — replace with real API
def mock_llm(messages: List[Dict], tools: List[Dict]) -> Dict:
    """
    Simulates an LLM that can use tools.
    In production: call OpenAI, Anthropic, or your provider.
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


# Tool implementations
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
    
    1. Add user message
    2. Get LLM response
    3. If no tool calls → return response
    4. Execute tools → add results → loop to step 2
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to tools."},
        {"role": "user", "content": user_input}
    ]
    
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

## Running It

```bash
python agent.py
```

**Example interaction:**
```
⚔️ Ares Session 01: Tool Loop
Type 'exit' to quit

You: What's the weather in London?
Agent: The weather in London is sunny, 22°C

You: Thanks!
Agent: I processed your message: Thanks!
```

## Key Insights

### 1. The Loop is Everything
Every agent, from Claude Code to GPT-4, uses this same pattern:
- User message in
- LLM decides
- If tools needed → execute → loop
- If done → return result

### 2. Tools Are Just Functions
```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {...}
}]
```

The LLM uses descriptions to decide when to call them.

### 3. Messages Array is State
The `messages` array holds the entire conversation:
- System prompt (who the agent is)
- User inputs (what they want)
- Assistant responses (what the agent said)
- Tool results (what happened)

This is your agent's "memory" — for this session.

## Homework

1. **Replace the mock LLM** with a real API call (OpenAI, Anthropic)
2. **Add a new tool** (e.g., `get_time`, `calculator`)
3. **Add error handling** (what if weather API fails?)

## Production Notes

Real agents add:
- **Retries** (LLMs occasionally fail)
- **Timeouts** (don't loop forever)
- **Rate limiting** (don't hammer APIs)
- **Logging** (debug what happened)

But the **core loop never changes**.

## Next: Session 02

Learn how to add tools without touching the loop → [s02-multi-tool](../s02-multi-tool/)

---

<p align="center">
  <i>Session 01 of 12 ⚔️</i>
</p>
