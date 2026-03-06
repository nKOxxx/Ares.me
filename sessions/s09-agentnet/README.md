# Session 09: AgentNet

> **"No agent is an island"**

## What You Build

Multiple agents collaborating via a shared protocol.

## The Pattern

```python
class AgentNet:
    """Network of collaborating agents."""
    
    def register(self, agent: Agent):
        """Add agent to network."""
        
    def send(self, from: str, to: str, message: str):
        """Inter-agent messaging."""
        
    def broadcast(self, from: str, message: str):
        """Message all agents."""
```

## Use Cases

- **Ares (Strategy)** coordinates with **Ares Dev** and **Ares Daily**
- **Security Agent** audits **Code Agent**'s output
- **Scheduler Agent** triggers **Executor Agents**

## Protocol

```json
{
  "from": "agent-id",
  "to": "agent-id",
  "type": "request|response|event",
  "payload": {},
  "timestamp": "..."
}
```

## Next: Session 10

Governance → [s10-governance](../s10-governance/)
