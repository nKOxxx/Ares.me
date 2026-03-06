# Session 06: Heartbeats

> **"Don't just respond — anticipate"**

## What You Build

An agent that runs **proactive checks** without being asked.

## The Pattern

```python
import schedule
import time

def heartbeat():
    """Run periodic checks."""
    # Check emails
    # Check calendar
    # Check services
    # Alert if needed

schedule.every(30).minutes.do(heartbeat)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Key Insight

Reactive agent:
```
User: "Check my email" → Agent checks
```

Proactive agent:
```
Agent: "You have an urgent email from CEO"
```

## Implementation

See [HEARTBEAT.md](../../templates/HEARTBEAT.md) for checklist template.

## Next: Session 07

Sub-agents → [s07-sub-agents](../s07-sub-agents/)
