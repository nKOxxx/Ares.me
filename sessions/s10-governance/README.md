# Session 10: Governance

> **"Freedom within fences"**

## What You Build

Rules and boundaries that keep agents safe and useful.

## The Rules

```yaml
permissions:
  read: always      # Safe
  write: ask        # Confirm first
  execute: ask      # Dangerous
  network: ask      # External actions
  
boundaries:
  family_time: 21:00-08:00  # Don't interrupt
  critical: always          # Unless critical
```

## Enforcement

```python
class Governance:
    def check(self, action: Action) -> Result:
        """Check if action is allowed."""
        
        # Check permissions
        if not self.has_permission(action):
            return Denied("No permission")
        
        # Check boundaries
        if self.in_quiet_hours() and not action.critical:
            return Queued("Will run at 08:00")
        
        return Allowed()
```

## Next: Session 11

Skills → [s11-skills](../s11-skills/)
