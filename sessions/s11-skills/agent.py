#!/usr/bin/env python3
"""
Session 11: Skills
Modular capabilities that agents can use.
"""

import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass


@dataclass
class Skill:
    """A modular capability that agents can use."""
    name: str
    description: str
    version: str
    functions: Dict[str, Callable]
    config: dict
    
    def execute(self, function_name: str, *args, **kwargs) -> Any:
        """Execute a skill function."""
        if function_name not in self.functions:
            raise ValueError(f"Function '{function_name}' not found in skill '{self.name}'")
        
        func = self.functions[function_name]
        return func(*args, **kwargs)


class SkillRegistry:
    """
    Registry for loading and managing skills.
    
    Skills are modular capabilities that can be:
    - Loaded dynamically
    - Shared between agents
    - Versioned
    - Hot-swapped
    """
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(exist_ok=True)
        self.skills: Dict[str, Skill] = {}
        self.skill_configs: Dict[str, dict] = {}
    
    def register(self, skill: Skill):
        """Register a skill."""
        self.skills[skill.name] = skill
        print(f"[SKILLS] Registered: {skill.name} v{skill.version}")
    
    def load_from_directory(self):
        """Load all skills from the skills directory."""
        if not self.skills_dir.exists():
            return
        
        for skill_file in self.skills_dir.glob("*/skill.py"):
            skill_name = skill_file.parent.name
            try:
                skill = self._load_skill_module(skill_file, skill_name)
                if skill:
                    self.register(skill)
            except Exception as e:
                print(f"[SKILLS] Failed to load {skill_name}: {e}")
    
    def _load_skill_module(self, file_path: Path, skill_name: str) -> Optional[Skill]:
        """Load a skill from a Python file."""
        # Load module dynamically
        spec = importlib.util.spec_from_file_location(skill_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Read SKILL.md for metadata
        skill_md = file_path.parent / "SKILL.md"
        config = {}
        if skill_md.exists():
            config = self._parse_skill_md(skill_md)
        
        # Extract functions marked as @skill_function
        functions = {}
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and hasattr(attr, '_is_skill_function'):
                functions[attr_name] = attr
        
        # If no decorated functions, export all callables
        if not functions:
            functions = {
                name: getattr(module, name)
                for name in dir(module)
                if callable(getattr(module, name)) and not name.startswith('_')
            }
        
        return Skill(
            name=config.get('name', skill_name),
            description=config.get('description', 'No description'),
            version=config.get('version', '0.1.0'),
            functions=functions,
            config=config
        )
    
    def _parse_skill_md(self, md_path: Path) -> dict:
        """Parse SKILL.md file for metadata."""
        config = {}
        with open(md_path) as f:
            content = f.read()
            
        # Simple parsing - in production use a proper markdown parser
        if "## " in content:
            sections = content.split("## ")
            for section in sections:
                if section.startswith("Capabilities"):
                    config['capabilities'] = section.strip()
                elif section.startswith("Setup"):
                    config['setup'] = section.strip()
        
        # Extract first line as description
        lines = content.strip().split('\n')
        if lines:
            config['description'] = lines[0].lstrip('# ')
        
        return config
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self.skills.get(name)
    
    def list_skills(self) -> List[str]:
        """List all available skills."""
        return list(self.skills.keys())
    
    def get_skill_info(self, name: str) -> dict:
        """Get information about a skill."""
        skill = self.skills.get(name)
        if not skill:
            return {}
        
        return {
            "name": skill.name,
            "description": skill.description,
            "version": skill.version,
            "functions": list(skill.functions.keys()),
            "config": skill.config
        }


def skill_function(func: Callable) -> Callable:
    """Decorator to mark a function as a skill function."""
    func._is_skill_function = True
    return func


# Example built-in skills
class WeatherSkill:
    """Built-in weather skill."""
    
    @staticmethod
    @skill_function
    def get_current(city: str) -> dict:
        """Get current weather for a city."""
        # In production, call real weather API
        return {
            "city": city,
            "temperature": 22,
            "condition": "sunny",
            "humidity": 65
        }
    
    @staticmethod
    @skill_function
    def get_forecast(city: str, days: int = 3) -> list:
        """Get weather forecast."""
        forecast = []
        for i in range(days):
            forecast.append({
                "day": i + 1,
                "temperature": 20 + i,
                "condition": "sunny" if i % 2 == 0 else "cloudy"
            })
        return forecast


class CalculatorSkill:
    """Built-in calculator skill."""
    
    @staticmethod
    @skill_function
    def calculate(expression: str) -> float:
        """Safely evaluate a math expression."""
        # Only allow safe characters
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            raise ValueError("Invalid characters in expression")
        return eval(expression)
    
    @staticmethod
    @skill_function
    def add(a: float, b: float) -> float:
        return a + b
    
    @staticmethod
    @skill_function
    def multiply(a: float, b: float) -> float:
        return a * b


def create_example_skill(skill_name: str = "weather"):
    """Create an example skill directory."""
    skill_dir = Path("skills") / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Create skill.py
    skill_py = skill_dir / "skill.py"
    if not skill_py.exists():
        skill_py.write_text('''"""
Weather Skill

A skill for fetching weather data.
"""

import requests

API_KEY = "your-api-key"  # Set in environment or config

def get_current(city: str) -> dict:
    """Get current weather for a city."""
    # Example implementation
    # In production: call OpenWeatherMap or similar
    return {
        "city": city,
        "temp": 22,
        "condition": "sunny"
    }

def get_forecast(city: str, days: int = 3) -> list:
    """Get weather forecast."""
    forecast = []
    for i in range(days):
        forecast.append({
            "day": i + 1,
            "temp": 20 + i,
            "condition": "sunny"
        })
    return forecast
''')
        print(f"Created {skill_py}")
    
    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        skill_md.write_text(f'''# {skill_name.title()} Skill

A skill for {skill_name} operations.

## Capabilities

- Get current {skill_name} data
- Historical {skill_name} data
- Forecasts

## Setup

1. Set API key in environment: `{skill_name.upper()}_API_KEY`
2. Import and use

## Usage

```python
from skills import {skill_name}

result = {skill_name}.get_current("London")
```

## Functions

- `get_current(city: str) -> dict`
- `get_forecast(city: str, days: int) -> list`
''')
        print(f"Created {skill_md}")


class AgentWithSkills:
    """An agent that can use skills."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.registry = SkillRegistry()
        self.registry.load_from_directory()
        
        # Register built-in skills
        self._register_builtin_skills()
    
    def _register_builtin_skills(self):
        """Register built-in skills."""
        self.registry.register(Skill(
            name="weather",
            description="Weather information",
            version="1.0.0",
            functions={
                "get_current": WeatherSkill.get_current,
                "get_forecast": WeatherSkill.get_forecast
            },
            config={}
        ))
        
        self.registry.register(Skill(
            name="calculator",
            description="Math calculations",
            version="1.0.0",
            functions={
                "calculate": CalculatorSkill.calculate,
                "add": CalculatorSkill.add,
                "multiply": CalculatorSkill.multiply
            },
            config={}
        ))
    
    def use_skill(self, skill_name: str, function: str, *args, **kwargs):
        """Use a skill function."""
        skill = self.registry.get_skill(skill_name)
        if not skill:
            raise ValueError(f"Skill '{skill_name}' not found")
        
        return skill.execute(function, *args, **kwargs)
    
    def list_skills(self) -> List[str]:
        """List available skills."""
        return self.registry.list_skills()


def main():
    print("⚔️ Ares Session 11: Skills")
    print("Modular capabilities that agents can use.\n")
    
    # Create example skill
    create_example_skill("weather")
    
    # Create agent with skills
    agent = AgentWithSkills("agent-1")
    
    print(f"Available skills: {agent.list_skills()}\n")
    
    # Use weather skill
    print("Using weather skill:")
    weather = agent.use_skill("weather", "get_current", "London")
    print(f"  London weather: {weather}")
    
    forecast = agent.use_skill("weather", "get_forecast", "Paris", days=3)
    print(f"  Paris forecast: {forecast}\n")
    
    # Use calculator skill
    print("Using calculator skill:")
    result = agent.use_skill("calculator", "add", 5, 3)
    print(f"  5 + 3 = {result}")
    
    result = agent.use_skill("calculator", "multiply", 4, 7)
    print(f"  4 * 7 = {result}\n")
    
    # Show skill info
    print("Skill info:")
    for skill_name in agent.list_skills():
        info = agent.registry.get_skill_info(skill_name)
        print(f"  • {info['name']} v{info['version']}")
        print(f"    Functions: {', '.join(info['functions'])}")


if __name__ == "__main__":
    main()
