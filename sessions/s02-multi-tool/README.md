# Session 02: Multi-Tool Architecture

> **"Adding a tool means adding one handler — the loop stays the same"**

Now that you understand the core loop, let's make it **extensible**. In this session, you'll build an agent that can handle any number of tools without changing the loop code.

## 🎯 What You'll Build

An agent with **4 tools** that can:
- Check the weather
- Do math calculations  
- Tell you the time
- Search the web (simulated)

**The magic:** Adding a new tool only requires adding 3 lines of code. The loop never changes.

---

## 🚀 Quick Start

### Run It

```bash
cd sessions/s02-multi-tool
python agent.py
```

### Try These Commands

```
You: What's the weather in Paris?
Agent: The weather in Paris is cloudy, 18°C

You: Calculate 15 * 7 + 3
Agent: Result: 108

You: What time is it?
Agent: Current time (UTC): 2026-03-06 14:30:45

You: Search for Python tutorials
Agent: Search results for 'Python tutorials': [Simulated result 1, Simulated result 2]
```

---

## 📖 The Architecture

### The Problem with Session 01

In Session 01, if statements decided which tool to use:

```python
# Session 01 approach (bad for scaling)
if "weather" in message:
    use_weather_tool()
elif "math" in message:
    use_calculator()
elif "time" in message:
    use_time_tool()
# ... this gets messy fast!
```

**Problem:** Every new tool = more if statements. The code grows, gets messy, and breaks.

### The Solution: Tool Registry

```python
# Tool implementations (just functions)
def get_weather(city): ...
def calculator(expr): ...
def get_time(): ...

# Registry (just a dictionary)
TOOL_HANDLERS = {
    "get_weather": get_weather,
    "calculate": calculator,
    "get_time": get_time,
}

# Execution (one line, never changes!)
handler = TOOL_HANDLERS[tool_name]
result = handler(**parameters)
```

**Benefits:**
- ✅ Add tools without touching the loop
- ✅ Clean, organized code
- ✅ Easy to test each tool separately
- ✅ Tools can be in separate files

---

## 🔍 Code Walkthrough

### Step 1: Tool Implementations

Each tool is just a Python function:

```python
def get_weather(city: str) -> str:
    """Get weather for a city."""
    conditions = ["sunny", "cloudy", "rainy"]
    temp = random.randint(15, 30)
    condition = random.choice(conditions)
    return f"The weather in {city} is {condition}, {temp}°C"


def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        # Only allow safe characters
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters"
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
    return f"Search results for '{query}': [Result 1, Result 2]"
```

**Key insight:** Each tool is just a function that takes inputs and returns a string.

### Step 2: Tool Registry

```python
# Map tool names to functions
TOOL_HANDLERS: Dict[str, Callable] = {
    "get_weather": get_weather,
    "calculate": calculator,
    "get_time": get_time,
    "search_web": search_web,
}
```

**Why this is powerful:**
- The LLM returns `"get_weather"` as a string
- We look it up in the dictionary
- We call the function automatically

### Step 3: Tool Definitions (for the LLM)

```python
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
    # ... more tools
]
```

**Why this matters:** The LLM uses these descriptions to decide which tool to call. Good descriptions = better tool selection.

### Step 4: Tool Execution (The Magic)

```python
def execute_tools(tool_calls: List[Dict]) -> List[Dict]:
    """Execute tools using the registry."""
    results = []
    
    for call in tool_calls:
        name = call.get("name")           # "get_weather"
        handler = TOOL_HANDLERS.get(name)  # Look up function
        
        if handler:
            try:
                # Call the function with parameters
                output = handler(**call.get("input", {}))
                results.append({
                    "type": "tool_result",
                    "content": output
                })
            except Exception as e:
                results.append({
                    "type": "tool_result", 
                    "content": f"Error: {str(e)}"
                })
    
    return results
```

**Notice:** This code doesn't change no matter how many tools you add!

---

## 🛠️ Exercises

### Exercise 1: Add a Translate Tool

```python
def translate(text: str, target_language: str = "Spanish") -> str:
    """Simulate translation."""
    translations = {
        "hello": {"Spanish": "hola", "French": "bonjour"},
        "goodbye": {"Spanish": "adiós", "French": "au revoir"},
    }
    word = text.lower()
    if word in translations:
        return f"'{text}' in {target_language}: {translations[word].get(target_language, 'unknown')}"
    return f"Translation not available for '{text}'"

# Add to registry
TOOL_HANDLERS["translate"] = translate

# Add definition
{
    "name": "translate",
    "description": "Translate text to another language",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "target_language": {"type": "string", "enum": ["Spanish", "French"]}
        },
        "required": ["text"]
    }
}
```

Test it:
```
You: Translate 'hello' to Spanish
Agent: 'hello' in Spanish: hola
```

### Exercise 2: Tools in Separate Files

For larger projects, move tools to their own file:

```python
# tools.py
def get_weather(city): ...
def calculator(expr): ...

# agent.py
from tools import get_weather, calculator

TOOL_HANDLERS = {
    "get_weather": get_weather,
    "calculate": calculator,
}
```

### Exercise 3: Connect to Real APIs

Make the weather tool real:

```bash
pip install requests
```

```python
import requests

def get_weather(city: str) -> str:
    """Real weather using OpenWeatherMap API."""
    API_KEY = "your-api-key"  # Get from openweathermap.org
    
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    
    return f"Weather in {city}: {temp}°C, {condition}"
```

---

## 🎓 Key Concepts

### 1. Separation of Concerns

| Component | Responsibility | Changes When... |
|-----------|---------------|-----------------|
| Tool Functions | Do the actual work | You add a new capability |
| Tool Registry | Maps names to functions | You add a new tool |
| Tool Definitions | Describe tools to LLM | You add a new tool |
| Agent Loop | Orchestrates everything | Never (it's done!) |

### 2. Error Handling

Always handle tool failures gracefully:

```python
try:
    output = handler(**parameters)
except Exception as e:
    output = f"Error: {str(e)}"
```

The LLM can then decide what to do with the error.

### 3. Tool Design Best Practices

**Good tool:**
- Clear name (`get_weather` not `tool1`)
- Good description
- Specific parameters
- Returns string (easy for LLM to understand)

**Bad tool:**
- Vague name
- Poor description
- Ambiguous parameters
- Returns complex objects

---

## 📊 Comparison: Session 01 vs Session 02

| Aspect | Session 01 | Session 02 |
|--------|-----------|------------|
| Tools | 1 (hardcoded) | Unlimited (registry) |
| Adding tools | Edit loop | Edit registry |
| Code lines for new tool | ~10 | 3 |
| Error handling | None | Built-in |
| Maintainability | Poor | Excellent |

---

## 🚀 Next Steps

Ready for planning? Go to [Session 03: Planning](../s03-planning/)

There you'll learn:
- How to break big tasks into steps
- How to get user approval before acting
- How to handle task dependencies

---

<p align="center">
  <i>Session 02 of 12 ⚔️</i><br>
  <a href="../s01-tool-loop/">← Previous</a> •
  <a href="../../">Home</a> •
  <a href="../s03-planning/">Next →</a>
</p>
