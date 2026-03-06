#!/usr/bin/env python3
"""
Session 09: AgentNet
Multi-agent collaboration protocol.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    BROADCAST = "broadcast"


@dataclass
class AgentMessage:
    """Standard message format for agent communication."""
    id: str
    from_agent: str
    to_agent: str  # "*" for broadcast
    type: MessageType
    payload: dict
    timestamp: str
    in_reply_to: Optional[str] = None
    
    def to_dict(self) -> dict:
        data = asdict(self)
        data['type'] = self.type.value
        return data
    
    @classmethod
    def create(cls, from_agent: str, to_agent: str, msg_type: MessageType, 
               payload: dict, in_reply_to: str = None) -> "AgentMessage":
        return cls(
            id=str(uuid.uuid4())[:8],
            from_agent=from_agent,
            to_agent=to_agent,
            type=msg_type,
            payload=payload,
            timestamp=datetime.now().isoformat(),
            in_reply_to=in_reply_to
        )


class Agent:
    """
    An agent that can participate in AgentNet.
    
    Each agent has:
    - A unique ID
    - A mailbox for receiving messages
    - Handlers for different message types
    """
    
    def __init__(self, agent_id: str, network: "AgentNet" = None):
        self.agent_id = agent_id
        self.network = network
        self.mailbox: asyncio.Queue = asyncio.Queue()
        self.handlers: Dict[str, Callable] = {}
        self.running = False
        
        # Register default handlers
        self.register_handler("ping", self._handle_ping)
        self.register_handler("get_status", self._handle_status)
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a handler for a specific message type."""
        self.handlers[message_type] = handler
    
    async def _handle_ping(self, msg: AgentMessage) -> dict:
        """Default ping handler."""
        return {"status": "alive", "agent_id": self.agent_id}
    
    async def _handle_status(self, msg: AgentMessage) -> dict:
        """Default status handler."""
        return {
            "agent_id": self.agent_id,
            "mailbox_size": self.mailbox.qsize(),
            "handlers": list(self.handlers.keys())
        }
    
    async def send(self, to_agent: str, msg_type: str, payload: dict) -> Optional[AgentMessage]:
        """Send a message to another agent."""
        if self.network:
            msg = AgentMessage.create(
                from_agent=self.agent_id,
                to_agent=to_agent,
                msg_type=MessageType.REQUEST,
                payload={"type": msg_type, "data": payload}
            )
            return await self.network.send_message(msg)
        return None
    
    async def broadcast(self, msg_type: str, payload: dict):
        """Broadcast a message to all agents."""
        if self.network:
            msg = AgentMessage.create(
                from_agent=self.agent_id,
                to_agent="*",
                msg_type=MessageType.BROADCAST,
                payload={"type": msg_type, "data": payload}
            )
            await self.network.broadcast(msg)
    
    async def run(self):
        """Main agent loop - processes incoming messages."""
        self.running = True
        print(f"[AGENT] {self.agent_id} started")
        
        while self.running:
            try:
                # Wait for message with timeout
                msg = await asyncio.wait_for(self.mailbox.get(), timeout=1.0)
                await self._process_message(msg)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"[AGENT] {self.agent_id} error: {e}")
    
    async def _process_message(self, msg: AgentMessage):
        """Process an incoming message."""
        payload_type = msg.payload.get("type", "unknown")
        
        if payload_type in self.handlers:
            try:
                handler = self.handlers[payload_type]
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(msg)
                else:
                    result = handler(msg)
                
                # Send response if it was a request
                if msg.type == MessageType.REQUEST and msg.from_agent != "*":
                    response = AgentMessage.create(
                        from_agent=self.agent_id,
                        to_agent=msg.from_agent,
                        msg_type=MessageType.RESPONSE,
                        payload={"type": "response", "data": result},
                        in_reply_to=msg.id
                    )
                    await self.network.send_message(response)
                    
            except Exception as e:
                print(f"[AGENT] Handler error: {e}")
        else:
            print(f"[AGENT] {self.agent_id}: No handler for {payload_type}")
    
    def stop(self):
        """Stop the agent."""
        self.running = False


class AgentNet:
    """
    Network for agent communication.
    
    Routes messages between agents and handles:
    - Message delivery
    - Broadcasts
    - Agent registration/deregistration
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_log: List[AgentMessage] = []
        self.running = False
    
    def register(self, agent: Agent):
        """Register an agent with the network."""
        self.agents[agent.agent_id] = agent
        agent.network = self
        print(f"[AGENTNET] Registered {agent.agent_id}")
    
    def unregister(self, agent_id: str):
        """Remove an agent from the network."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"[AGENTNET] Unregistered {agent_id}")
    
    async def send_message(self, msg: AgentMessage) -> Optional[AgentMessage]:
        """Route a message to its destination."""
        self.message_log.append(msg)
        
        if msg.to_agent == "*":
            # This shouldn't happen for direct messages
            await self.broadcast(msg)
            return msg
        
        if msg.to_agent in self.agents:
            await self.agents[msg.to_agent].mailbox.put(msg)
            return msg
        else:
            print(f"[AGENTNET] Agent {msg.to_agent} not found")
            return None
    
    async def broadcast(self, msg: AgentMessage):
        """Broadcast message to all agents."""
        self.message_log.append(msg)
        
        for agent_id, agent in self.agents.items():
            if agent_id != msg.from_agent:  # Don't send to self
                await agent.mailbox.put(msg)
    
    def list_agents(self) -> List[str]:
        """List all registered agents."""
        return list(self.agents.keys())
    
    def get_message_log(self) -> List[dict]:
        """Get all messages for debugging."""
        return [msg.to_dict() for msg in self.message_log]


# Specialized agent examples
class ResearchAgent(Agent):
    """Agent specialized in research tasks."""
    
    def __init__(self, agent_id: str, network: AgentNet = None):
        super().__init__(agent_id, network)
        self.register_handler("research", self._handle_research)
    
    async def _handle_research(self, msg: AgentMessage) -> dict:
        topic = msg.payload["data"].get("topic", "unknown")
        print(f"[RESEARCH] {self.agent_id} researching: {topic}")
        await asyncio.sleep(1)  # Simulate work
        return {"topic": topic, "findings": f"Key insights about {topic}", "sources": 5}


class CodeAgent(Agent):
    """Agent specialized in code tasks."""
    
    def __init__(self, agent_id: str, network: AgentNet = None):
        super().__init__(agent_id, network)
        self.register_handler("code_review", self._handle_code_review)
        self.register_handler("generate_code", self._handle_generate)
    
    async def _handle_code_review(self, msg: AgentMessage) -> dict:
        code = msg.payload["data"].get("code", "")
        print(f"[CODE] {self.agent_id} reviewing code")
        return {"issues": 2, "suggestions": ["Add type hints", "Add docstrings"]}
    
    async def _handle_generate(self, msg: AgentMessage) -> dict:
        spec = msg.payload["data"].get("spec", "")
        print(f"[CODE] {self.agent_id} generating code for: {spec}")
        return {"code": f"# Generated code for: {spec}\nprint('Hello')"}


async def main():
    print("⚔️ Ares Session 09: AgentNet")
    print("Multi-agent collaboration protocol.\n")
    
    # Create network
    network = AgentNet()
    
    # Create agents
    research = ResearchAgent("research-1", network)
    coder = CodeAgent("coder-1", network)
    coordinator = Agent("coordinator", network)
    
    # Register agents
    network.register(research)
    network.register(coder)
    network.register(coordinator)
    
    print(f"Agents registered: {network.list_agents()}\n")
    
    # Start all agents
    tasks = [
        asyncio.create_task(research.run()),
        asyncio.create_task(coder.run()),
        asyncio.create_task(coordinator.run())
    ]
    
    # Demonstrate communication
    print("Demo: Research request")
    await coordinator.send("research-1", "research", {"topic": "AI safety"})
    await asyncio.sleep(2)
    
    print("\nDemo: Code review request")
    await coordinator.send("coder-1", "code_review", {"code": "def foo(): pass"})
    await asyncio.sleep(2)
    
    print("\nDemo: Broadcast")
    await coordinator.broadcast("ping", {})
    await asyncio.sleep(2)
    
    # Show message log
    print("\n=== Message Log ===")
    for msg in network.get_message_log():
        print(f"  {msg['from_agent']} -> {msg['to_agent']}: {msg['payload'].get('type')}")
    
    # Cleanup
    research.stop()
    coder.stop()
    coordinator.stop()
    
    for task in tasks:
        task.cancel()
    
    print("\nAgentNet demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
