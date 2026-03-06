#!/usr/bin/env python3
"""
Session 05: Soul & User
An agent with personality and user context.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class PersonalityLoader:
    """Loads agent personality from SOUL.md-style config."""
    
    def __init__(self, config_path: str = "config/SOUL.json"):
        self.config_path = Path(config_path)
        self.soul = self._load_soul()
    
    def _load_soul(self) -> Dict[str, Any]:
        """Load personality configuration."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        
        # Default personality
        return {
            "name": "Agent",
            "emoji": "🤖",
            "role": "Helpful Assistant",
            "values": ["Be helpful", "Be direct"],
            "style": "Clear and concise",
            "boundaries": {
                "safe_to_do": ["read files", "answer questions"],
                "ask_first": ["send messages", "make purchases"],
                "never": ["share private data"]
            }
        }
    
    def get_system_prompt(self) -> str:
        """Generate system prompt from personality."""
        soul = self.soul
        
        prompt = f"""You are {soul['name']} {soul['emoji']}
Role: {soul['role']}

Core Values:
"""
        for value in soul['values']:
            prompt += f"- {value}\n"
        
        prompt += f"\nCommunication Style: {soul['style']}\n"
        
        prompt += "\nBoundaries:\n"
        prompt += f"- Safe: {', '.join(soul['boundaries']['safe_to_do'])}\n"
        prompt += f"- Ask First: {', '.join(soul['boundaries']['ask_first'])}\n"
        prompt += f"- Never: {', '.join(soul['boundaries']['never'])}\n"
        
        return prompt


class UserContext:
    """Loads user context from USER.md-style config."""
    
    def __init__(self, config_path: str = "config/USER.json"):
        self.config_path = Path(config_path)
        self.user = self._load_user()
    
    def _load_user(self) -> Dict[str, Any]:
        """Load user configuration."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        
        # Default user
        return {
            "name": "User",
            "preferences": {},
            "work_style": "flexible",
            "communication": "direct",
            "timezone": "UTC"
        }
    
    def get_context(self) -> str:
        """Generate user context string."""
        user = self.user
        
        context = f"""User: {user['name']}
Work Style: {user['work_style']}
Communication: {user['communication']}
Timezone: {user['timezone']}

Preferences:
"""
        for key, value in user.get('preferences', {}).items():
            context += f"- {key}: {value}\n"
        
        return context


class AgentWithPersonality:
    """Agent that knows who it is and who it serves."""
    
    def __init__(self):
        # Create config directory
        Path("config").mkdir(exist_ok=True)
        
        self.personality = PersonalityLoader()
        self.user = UserContext()
        
        # Build complete system prompt
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Combine personality and user context."""
        prompt = self.personality.get_system_prompt()
        prompt += "\n" + "="*50 + "\n"
        prompt += self.user.get_context()
        return prompt
    
    def chat(self, message: str) -> str:
        """Process message with personality."""
        # Simple mock response
        if "who are you" in message.lower():
            soul = self.personality.soul
            return f"I am {soul['name']} {soul['emoji']}, {soul['role']}. My values: {', '.join(soul['values'])}"
        
        if "who am i" in message.lower() or "user" in message.lower():
            user = self.user.user
            return f"You are {user['name']}. Work style: {user['work_style']}"
        
        return f"Processing '{message}' with my personality and your context in mind."


def create_default_configs():
    """Create default SOUL.json and USER.json if they don't exist."""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Create SOUL.json
    soul_path = config_dir / "SOUL.json"
    if not soul_path.exists():
        soul = {
            "name": "Ares",
            "emoji": "⚔️",
            "role": "AI Partner",
            "values": [
                "Be direct over performative",
                "Resourceful before asking",
                "Test before deployment"
            ],
            "style": "Bullet points over walls of text",
            "boundaries": {
                "safe_to_do": [
                    "Read files",
                    "Organize memory",
                    "Learn and research"
                ],
                "ask_first": [
                    "Send external messages",
                    "Make purchases",
                    "Deploy to production"
                ],
                "never": [
                    "Share private data",
                    "Run destructive commands without confirmation"
                ]
            }
        }
        with open(soul_path, 'w') as f:
            json.dump(soul, f, indent=2)
        print(f"✅ Created {soul_path}")
    
    # Create USER.json
    user_path = config_dir / "USER.json"
    if not user_path.exists():
        user = {
            "name": "Developer",
            "preferences": {
                "communication": "Direct",
                "output_style": "Production-ready",
                "work_hours": "Flexible"
            },
            "work_style": "Deep diver",
            "communication": "Bullet points preferred",
            "timezone": "UTC"
        }
        with open(user_path, 'w') as f:
            json.dump(user, f, indent=2)
        print(f"✅ Created {user_path}")


def main():
    print("⚔️ Ares Session 05: Soul & User")
    print("Loading personality and user context...\n")
    
    # Create default configs
    create_default_configs()
    
    # Initialize agent
    agent = AgentWithPersonality()
    
    print("System Prompt:")
    print("="*50)
    print(agent.system_prompt)
    print("="*50)
    print()
    
    print("Commands:")
    print("  • 'who are you' - Show agent personality")
    print("  • 'who am i' - Show user context")
    print("  • 'system' - Show full system prompt")
    print("  • 'exit' - Quit")
    print()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            break
        
        if user_input.lower() == "system":
            print(f"\n{agent.system_prompt}\n")
            continue
        
        if not user_input:
            continue
        
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
