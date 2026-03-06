# Session 03: Planning

> **"An agent without a plan drifts"**

## What You Build

An agent that breaks tasks into steps before executing.

## The Problem

```python
User: "Build me a website"
Agent: *immediately starts coding*
# ... 3 hours later ...
Agent: "Done!" 
User: "That's not what I wanted"
```

**No plan = wasted effort.**

## The Solution

```python
User: "Build me a website"
Agent: "Here's my plan:
  1. Clarify requirements
  2. Design structure  
  3. Build backend
  4. Build frontend
  5. Deploy
  
  Approve?"
User: "Approved" → Agent executes step by step
```

## Key Pattern

```python
def plan_task(goal: str) -> List[Step]:
    """Generate execution plan."""
    return llm.plan(goal)

def execute_plan(steps: List[Step]):
    """Execute with checkpointing."""
    for step in steps:
        result = execute(step)
        if not result.success:
            replan()
```

## Code Structure

```python
class Planner:
    def plan(self, goal: str) -> Plan:
        """Break goal into steps."""
        
    def execute(self, plan: Plan):
        """Execute step by step."""
        
    def replan(self, failed_step: Step):
        """Adjust when things go wrong."""
```

## Next: Session 04

Add memory → [s04-memory-bridge](../s04-memory-bridge/)
