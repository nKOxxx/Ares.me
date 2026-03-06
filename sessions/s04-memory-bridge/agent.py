#!/usr/bin/env python3
"""
Session 04: Memory Bridge
Cross-session persistence.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class MemoryBridge:
    """
    Simple file-based memory system.
    
    Every session starts fresh, but we persist
    the important stuff to files.
    """
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        self.short_term: Dict[str, Any] = {}  # This session only
        self.long_term: Dict[str, Any] = {}   # Persisted to disk
        
        self._load()
    
    def _load(self):
        """Load long-term memory from disk."""
        memory_file = self.memory_dir / "memory.json"
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                self.long_term = json.load(f)
    
    def _save(self):
        """Save long-term memory to disk."""
        memory_file = self.memory_dir / "memory.json"
        with open(memory_file, 'w') as f:
            json.dump(self.long_term, f, indent=2)
    
    def remember(self, key: str, value: Any, persistent: bool = True):
        """
        Store a memory.
        
        Args:
            key: What to remember
            value: The data
            persistent: If True, survives restarts
        """
        if persistent:
            self.long_term[key] = {
                "value": value,
                "stored_at": datetime.now().isoformat()
            }
            self._save()
        else:
            self.short_term[key] = value
    
    def recall(self, key: str) -> Optional[Any]:
        """Retrieve a memory."""
        # Check short-term first
        if key in self.short_term:
            return self.short_term[key]
        
        # Then long-term
        if key in self.long_term:
            return self.long_term[key]["value"]
        
        return None
    
    def forget(self, key: str):
        """Remove a memory."""
        self.short_term.pop(key, None)
        self.long_term.pop(key, None)
        self._save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all memories (for context injection)."""
        memories = {}
        memories.update(self.short_term)
        memories.update({k: v["value"] for k, v in self.long_term.items()})
        return memories


class AgentWithMemory:
    """Agent that persists across sessions."""
    
    def __init__(self):
        self.memory = MemoryBridge()
        self.messages = []
        
        # Inject memories into system prompt
        memories = self.memory.get_all()
        context = self._format_memories(memories)
        
        self.messages.append({
            "role": "system",
            "content": f"You are a helpful assistant.\n\nCONTEXT:\n{context}"
        })
    
    def _format_memories(self, memories: Dict) -> str:
        """Format memories for LLM context."""
        if not memories:
            return "No previous context."
        
        lines = []
        for key, value in memories.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
    def chat(self, user_input: str) -> str:
        """Process user input with memory."""
        self.messages.append({"role": "user", "content": user_input})
        
        # Simulate LLM (replace with real API)
        response = self._mock_llm()
        
        # Extract memories from conversation
        self._extract_memories(user_input, response)
        
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def _mock_llm(self) -> str:
        """Simple mock that uses memory."""
        last_msg = self.messages[-1]["content"].lower()
        
        # Check if we know user's name
        name = self.memory.recall("user_name")
        
        if "my name" in last_msg and "what" in last_msg:
            if name:
                return f"Your name is {name}."
            return "I don't know your name yet. What is it?"
        
        if "name is" in last_msg:
            # Extract name (simplified)
            parts = last_msg.split("name is")
            if len(parts) > 1:
                extracted = parts[1].strip().strip(".!?")
                return f"Nice to meet you, {extracted}! I'll remember that."
        
        return f"I processed: '{last_msg}'. Current memories: {self.memory.get_all()}"
    
    def _extract_memories(self, user_input: str, response: str):
        """Extract key info to remember."""
        # Simple extraction: if user says "my name is X", remember it
        user_lower = user_input.lower()
        if "my name is" in user_lower:
            parts = user_input.split("name is")
            if len(parts) > 1:
                name = parts[1].strip().strip(".!?")
                self.memory.remember("user_name", name)
                print(f"  [Memory: stored user_name = {name}]")


def main():
    print("⚔️ Ares Session 04: Memory Bridge")
    print("I remember things across restarts!\n")
    print(f"Memory location: {Path('memory').absolute()}\n")
    
    agent = AgentWithMemory()
    
    # Show existing memories
    memories = agent.memory.get_all()
    if memories:
        print("📚 Previous memories loaded:")
        for key, value in memories.items():
            print(f"  - {key}: {value}")
        print()
    
    print("Type 'exit' to quit, 'forget' to clear memory\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ("exit", "quit"):
            break
        
        if user_input.lower() == "forget":
            # Clear all memories
            for key in list(agent.memory.get_all().keys()):
                agent.memory.forget(key)
            print("  [All memories cleared]\n")
            continue
        
        if not user_input:
            continue
        
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")
    
    print("\n💾 Memories saved. Restart me and I'll remember!")


if __name__ == "__main__":
    main()
