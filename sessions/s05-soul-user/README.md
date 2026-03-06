# Session 05: Soul & User

> **"An assistant without personality is just a search engine"**

## What You Build

An agent with:
- **SOUL.md** — Who it is
- **USER.md** — Who it serves

## The Pattern

```python
class Agent:
    def __init__(self):
        self.soul = self._load_soul()      # Who am I?
        self.user = self._load_user()      # Who do I serve?
        
        self.system_prompt = f"""
        {self.soul}
        
        You are helping:
        {self.user}
        """
```

## Why This Matters

Without SOUL.md:
- Generic, inconsistent responses
- No personality or values
- Every session feels different

Without USER.md:
- Doesn't know user's context
- Misses important details
- Violates boundaries unknowingly

## Implementation

See templates:
- [SOUL.md](../../templates/SOUL.md)
- [USER.md](../../templates/USER.md)

## Next: Session 06

Proactive execution → [s06-heartbeats](../s06-heartbeats/)
