# Session 07: Sub-Agents

> **"One mind, many hands"**

## What You Build

An agent that spawns **isolated sub-agents** for parallel tasks.

## The Pattern

```python
def spawn_subagent(task: str) -> Session:
    """Create isolated agent session."""
    return sessions.spawn(task=task)

# Main agent delegates
results = await asyncio.gather(
    spawn_subagent("Research competitors"),
    spawn_subagent("Check pricing"),
    spawn_subagent("Draft email"),
)
```

## Key Benefits

- **Parallel execution** — Multiple tasks at once
- **Clean context** — Each subagent has fresh memory
- **Fault isolation** — One fails, others continue
- **Cost tracking** — Separate billing per subagent

## Next: Session 08

Secure vault → [s08-secure-vault](../s08-secure-vault/)
