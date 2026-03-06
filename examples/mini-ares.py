#!/usr/bin/env python3
"""
Full Working Example: Mini-Ares
An agent with personality, memory, and planning.
"""

import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime


class MiniAres:
    """
    A minimal but complete Ares-class agent.
    
    Features:
    - Personality (SOUL.md concept)
    - Memory (cross-session persistence)
    - Planning (task breakdown)
    - Multi-tool support
    """
    
    def __init__(self, name: str = "MiniAres"):
        self.name = name
        self.memory_dir = Path("memory")
        self.memory_dir.mkdir(exist_ok=True)
        
        # Load or create identity
        self.soul = self._load_soul()
        self.user = self._load_user()
        
        # Initialize memory
        self.short_term: Dict[str, Any] = {}
        self.long_term = self._load_memory()
        
        print(f"⚔️ {self.name} online")
        print(f"   Memory: {len(self.long_term)} facts loaded")
        print(f"   Soul: {self.soul.get('emoji', '⚔️')} {self.soul.get('role', 'Assistant')}")
        print()
    
    def _load_soul(self) -> Dict:
        """Load agent personality."""
        soul_file = self.memory_dir / "SOUL.json"
        if soul_file.exists():
            with open(soul_file) as f:
                return json.load(f)
        
        # Default soul
        default = {
            "name": self.name,
            "role": "Helpful Assistant",
            "emoji": "⚔️",
            "values": ["Be direct", "Be proactive", "Be useful"],
            "style": "Bullet points over walls of text"
        }
        self._save_soul(default)
        return default
    
    def _save_soul(self, soul: Dict):
        """Save agent personality."""
        with open(self.memory_dir / "SOUL.json", 'w') as f:
            json.dump(soul, f, indent=2)
    
    def _load_user(self) -> Dict:
        """Load user context."""
        user_file = self.memory_dir / "USER.json"
        if user_file.exists():
            with open(user_file) as f:
                return json.load(f)
        return {"name": "User", "preferences": {}}
    
    def _load_memory(self) -> Dict:
        """Load persistent memory."""
        memory_file = self.memory_dir / "memory.json"
        if memory_file.exists():
            with open(memory_file) as f:
                return json.load(f)
        return {}
    
    def _save_memory(self):
        """Save persistent memory."""
        with open(self.memory_dir / "memory.json", 'w') as f:
            json.dump(self.long_term, f, indent=2)
    
    def remember(self, key: str, value: Any, persistent: bool = True):
        """Store a memory."""
        if persistent:
            self.long_term[key] = {
                "value": value,
                "stored_at": datetime.now().isoformat()
            }
            self._save_memory()
        else:
            self.short_term[key] = value
    
    def recall(self, key: str) -> Optional[Any]:
        """Retrieve a memory."""
        if key in self.short_term:
            return self.short_term[key]
        if key in self.long_term:
            return self.long_term[key]["value"]
        return None
    
    def chat(self, user_input: str) -> str:
        """Process user input."""
        user_lower = user_input.lower()
        
        # Command: remember
        if user_lower.startswith("remember "):
            parts = user_input[9:].split(" is ", 1)
            if len(parts) == 2:
                key, value = parts
                self.remember(key.strip(), value.strip())
                return f"✅ Remembered: {key.strip()} = {value.strip()}"
        
        # Command: recall
        if user_lower.startswith("recall "):
            key = user_input[7:].strip()
            value = self.recall(key)
            if value:
                return f"📚 {key}: {value}"
            return f"❓ I don't know '{key}'"
        
        # Command: plan
        if user_lower.startswith("plan "):
            goal = user_input[5:]
            return self._create_plan(goal)
        
        # Command: memories
        if user_lower in ("memories", "memory"):
            all_memories = {**self.short_term, **{k: v["value"] for k, v in self.long_term.items()}}
            if all_memories:
                lines = ["📚 Memories:"]
                for k, v in all_memories.items():
                    lines.append(f"  • {k}: {v}")
                return "\n".join(lines)
            return "📭 No memories yet"
        
        # Command: identity
        if user_lower in ("who are you", "identity"):
            return f"""⚔️ {self.soul['name']}
Role: {self.soul['role']}
Values: {', '.join(self.soul['values'])}
Style: {self.soul['style']}"""
        
        # Default response
        return f"I heard: '{user_input}'\nTry: 'remember X is Y', 'recall X', 'plan [task]', or 'memories'"
    
    def _create_plan(self, goal: str) -> str:
        """Create a simple plan."""
        steps = [
            f"1. Analyze: {goal}",
            "2. Gather requirements",
            "3. Break into subtasks",
            "4. Execute step by step",
            "5. Verify completion"
        ]
        return f"📋 Plan for '{goal}':\n" + "\n".join(f"   {s}" for s in steps)


def main():
    print("=" * 50)
    print("Mini-Ares: Full Working Example")
    print("=" * 50)
    print()
    
    agent = MiniAres()
    
    print("Commands:")
    print("  • remember X is Y  - Store a fact")
    print("  • recall X         - Retrieve a fact")
    print("  • plan [task]      - Create a plan")
    print("  • memories         - List all memories")
    print("  • who are you      - Show identity")
    print("  • exit             - Quit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ("exit", "quit"):
                break
            
            if not user_input:
                continue
            
            response = agent.chat(user_input)
            print(f"{agent.soul.get('emoji', '⚔️')} {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
    
    print(f"\n💾 {agent.name} saved {len(agent.long_term)} memories. See you next time!")


if __name__ == "__main__":
    main()
