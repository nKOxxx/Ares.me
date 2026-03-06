# Session 02: Multi-Tool Architecture

> **"Adding a tool means adding one handler — the loop stays the same"**

## What You Build

An agent with **extensible tools** that can:
- Register new tools without touching the core loop
- Handle multiple tools per conversation
- Route tool calls to the right handler automatically

## The Pattern

```python
# Register tools in a dictionary
TOOL_HANDLERS = {
    "get_weather": get_weather,
    "calculate": calculator,
    "search_web": web_search,
}

# Execute dynamically
def execute_tools(calls):
    return [TOOL_HANDLERS[c["name"]](**c["input"]) for c in calls]
```

## The Code

### `agent.py`

```python
#!/usr/bin/env python3
"""
Session 02: Multi-Tool Architecture
Extensible tool system.
"""

from typing import List, Dict, Callable
from datetime import datetime
import random


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def get_weather(city: str) -> str:
    """Get weather for a city."""
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.randint(15, 30)
    condition = random.choice(conditions)
    return f"The weather in {city} is {condition}, {temp}°C"


def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        # Only allow safe characters
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


def get_time(timezone: str = "UTC") -> str:
    """Get current time."""
    now = datetime.now()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"


def search_web(query: str) -> str:
    """Simulate web search."""
    return f"Search results for '{query}': [Simulated result 1, Simulated result 2]"


# ============================================================================
# TOOL REGISTRY
# ============================================================================

TOOL_HANDLERS: Dict[str, Callable] = {
    "get_weather": get_weather,
    "calculate": calculator,
    "get_time": get_time,
    "search_web": search_web,
}

TOOL_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression (e.g., '2 + 2', '10 * 5')",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_time",
        "description": "Get current date and time",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {"type": "string", "description": "Timezone (default: UTC)"}
            }
        }
    },
    {
        "name": "search_web",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]


# ============================================================================
# AGENT LOOP (UNCHANGED FROM S01!)
# ============================================================================

def mock_llm(messages: List[Dict], tools: List[Dict]) -> Dict:
    """Simulates LLM with tool detection."""
    last_message = messages[-1]["content"].lower()
    
    # Simple pattern matching
    if "weather" in last_message:
        city = "London" if "london" in last_message else "New York"
        return {
            "role": "assistant",
            "content": [{"type": "tool_use", "name": "get_weather", "input": {"city": city}}]
        }
    elif any(op in last_message for op in ["+", "-", "*", "/", "calculate", "math"]):
        # Extract expression (simplified)
        return {
            "role": "assistant",
            "content": [{"type": "tool_use", "name": "calculate", "input": {"expression": "2 + 2"}}]
        }
    elif "time" in last_message:
        return {
            "role": "assistant",
            "content": [{"type": "tool_use", "name": "get_time", "input": {}}]
        }
    
    return {
        "role": "assistant",
        "content": [{"type": "text", "text": "I can help with weather, calculations, time, or web search!"}]
    }


def execute_tools(tool_calls: List[Dict]) -> List[Dict]:
    """Execute tools using the registry."""
    results = []
    
    for call in tool_calls:
        name = call.get("name")
        handler = TOOL_HANDLERS.get(name)
        
        if handler:
            try:
                output = handler(**call.get("input", {}))
                results.append({
                    "type": "tool_result",
                    "tool_use_id": call.get("id"),
                    "content": output
                })
            except Exception as e:
                results.append({
                    "type": "tool_result",
                    "tool_use_id": call.get("id"),
                    "content": f"Error: {str(e)}"
                })
        else:
            results.append({
                "type": "tool_result",
                "tool_use_id": call.get("id"),
                "content": f"Error: Unknown tool '{name}'"
            })
    
    return results


def agent_loop(user_input: str) -> str:
    """The core agent loop — identical to S01!"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to multiple tools."},
        {"role": "user", "content": user_input}
    ]
    
    while True:
        response = mock_llm(messages, TOOL_DEFINITIONS)
        messages.append({"role": "assistant", "content": response["content"]})
        
        tool_calls = [c for c in response["content"] if c.get("type") == "tool_use"]
        
        if not tool_calls:
            text_parts = [c.get("text", "") for c in response["content"] if c.get("type") == "text"]
            return "".join(text_parts)
        
        results = execute_tools(tool_calls)
        messages.append({"role": "user", "content": results})


def main():
    print("⚔️ Ares Session 02: Multi-Tool Architecture")
    print("Available tools: weather, calculate, time, search")
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

## Key Insights

### 1. The Loop Never Changes
Look at `agent_loop()` — it's **identical** to Session 01. We just:
- Added more tools to the registry
- The loop handles them automatically

### 2. Registration Pattern
```python
TOOL_HANDLERS = {
    "tool_name": function_impl,
}
```

Add a tool? Just add to this dict. No loop changes.

### 3. Error Handling
```python
def execute_tools(calls):
    for call in calls:
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return error("Unknown tool")
        try:
            return handler(**args)
        except Exception as e:
            return error(str(e))
```

Tools can fail. Handle it gracefully.

## Homework

1. **Add 2 new tools** (e.g., `translate`, `random_fact`)
2. **Add tool descriptions** that the LLM can use
3. **Connect to real APIs** (OpenWeather, Wolfram Alpha)

## Next: Session 03

Learn planning → [s03-planning](../s03-planning/)
