#!/usr/bin/env python3
"""
Session 10: Governance
Rules, permissions, and boundaries for agents.
"""

import re
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, time


class Permission(Enum):
    """Types of actions an agent can take."""
    READ = "read"              # Read files, data
    WRITE = "write"            # Write/modify files
    EXECUTE = "execute"        # Run code/commands
    NETWORK = "network"        # Make network requests
    EXTERNAL = "external"      # Send emails, post, etc.
    ADMIN = "admin"            # Critical operations


class RiskLevel(Enum):
    """Risk levels for actions."""
    LOW = "low"           # Safe, no confirmation needed
    MEDIUM = "medium"     # Ask for confirmation
    HIGH = "high"         # Require explicit approval
    CRITICAL = "critical" # Never allowed without override


@dataclass
class Rule:
    """A governance rule."""
    name: str
    description: str
    condition: Callable[[str, dict], bool]  # (action, context) -> should_block
    risk_level: RiskLevel
    message: str  # Message to show if rule triggers


class GovernanceEngine:
    """
    Enforces rules and permissions for agent actions.
    
    Prevents agents from:
    - Acting during quiet hours
    - Executing dangerous commands
    - Accessing sensitive data
    - Making external calls without approval
    """
    
    def __init__(self):
        self.rules: List[Rule] = []
        self.permissions: Dict[Permission, RiskLevel] = {
            Permission.READ: RiskLevel.LOW,
            Permission.WRITE: RiskLevel.MEDIUM,
            Permission.EXECUTE: RiskLevel.HIGH,
            Permission.NETWORK: RiskLevel.MEDIUM,
            Permission.EXTERNAL: RiskLevel.HIGH,
            Permission.ADMIN: RiskLevel.CRITICAL
        }
        self.quiet_hours = (time(21, 0), time(8, 0))  # 9pm - 8am
        self.approved_actions: set = set()  # Actions pre-approved
        
        # Add default rules
        self._add_default_rules()
    
    def _add_default_rules(self):
        """Add default safety rules."""
        
        # Rule 1: No destructive commands
        self.add_rule(Rule(
            name="no_destructive_commands",
            description="Block rm -rf, format, etc.",
            condition=lambda action, ctx: any(
                cmd in action.lower() 
                for cmd in ["rm -rf", "rm -fr", "format", "mkfs", "> /dev", "dd if"]
            ),
            risk_level=RiskLevel.CRITICAL,
            message="Destructive commands are blocked. Use 'trash' instead of 'rm'."
        ))
        
        # Rule 2: Quiet hours
        self.add_rule(Rule(
            name="quiet_hours",
            description="Don't send notifications during quiet hours",
            condition=self._is_quiet_hours,
            risk_level=RiskLevel.MEDIUM,
            message="Action blocked: Quiet hours (9pm-8am). Set critical=True to override."
        ))
        
        # Rule 3: No private data in prompts
        self.add_rule(Rule(
            name="no_private_data",
            description="Block actions that might expose private data",
            condition=self._contains_private_data,
            risk_level=RiskLevel.HIGH,
            message="Potential private data detected. Review before proceeding."
        ))
        
        # Rule 4: Network limits
        self.add_rule(Rule(
            name="rate_limit",
            description="Prevent excessive network calls",
            condition=lambda action, ctx: ctx.get("network_calls_last_minute", 0) > 60,
            risk_level=RiskLevel.MEDIUM,
            message="Rate limit exceeded: Max 60 network calls per minute."
        ))
    
    def _is_quiet_hours(self, action: str, context: dict) -> bool:
        """Check if currently in quiet hours."""
        if context.get("critical"):
            return False
        
        now = datetime.now().time()
        start, end = self.quiet_hours
        
        if start <= end:
            return start <= now <= end
        else:  # Crosses midnight
            return now >= start or now <= end
    
    def _contains_private_data(self, action: str, context: dict) -> bool:
        """Check for patterns that might be private data."""
        # Check for API keys, passwords, etc.
        patterns = [
            r'sk-[a-zA-Z0-9]{20,}',  # OpenAI keys
            r'ghp_[a-zA-Z0-9]{36}',   # GitHub tokens
            r'AKIA[0-9A-Z]{16}',      # AWS keys
            r'password\s*=\s*["\'][^"\']+',  # Password assignments
            r'api_key\s*=\s*["\'][^"\']+',   # API key assignments
        ]
        
        for pattern in patterns:
            if re.search(pattern, action, re.IGNORECASE):
                return True
        return False
    
    def add_rule(self, rule: Rule):
        """Add a custom rule."""
        self.rules.append(rule)
    
    def check_action(self, action: str, permission: Permission, 
                     context: dict = None) -> tuple[bool, Optional[str]]:
        """
        Check if an action is allowed.
        
        Returns: (allowed, reason_if_blocked)
        """
        context = context or {}
        
        # Check all rules
        for rule in self.rules:
            try:
                if rule.condition(action, context):
                    # Rule triggered
                    if rule.risk_level == RiskLevel.CRITICAL and not context.get("override"):
                        return False, f"[BLOCKED - {rule.name}] {rule.message}"
                    elif rule.risk_level == RiskLevel.HIGH and not context.get("approved"):
                        return False, f"[NEEDS APPROVAL - {rule.name}] {rule.message}"
                    elif rule.risk_level == RiskLevel.MEDIUM and not context.get("confirmed"):
                        return False, f"[CONFIRMATION NEEDED - {rule.name}] {rule.message}"
            except Exception as e:
                # Rule evaluation failed - be conservative
                return False, f"[RULE ERROR] Could not evaluate rule {rule.name}: {e}"
        
        return True, None
    
    def request_approval(self, action: str, reason: str) -> bool:
        """
        Request user approval for an action.
        
        In production, this would show a UI dialog or send a message.
        For demo, we auto-approve.
        """
        print(f"\n[GOVERNANCE] Approval needed:")
        print(f"  Action: {action}")
        print(f"  Reason: {reason}")
        print(f"  Approve? (y/n): ", end="")
        
        # In real implementation, wait for user input
        # For demo, auto-approve
        response = input().strip().lower()
        return response in ('y', 'yes')
    
    def set_quiet_hours(self, start: time, end: time):
        """Set quiet hours."""
        self.quiet_hours = (start, end)
    
    def get_status(self) -> str:
        """Get current governance status."""
        lines = ["=== GOVERNANCE STATUS ==="]
        lines.append(f"Active rules: {len(self.rules)}")
        lines.append(f"Quiet hours: {self.quiet_hours[0]} - {self.quiet_hours[1]}")
        
        now = datetime.now().time()
        start, end = self.quiet_hours
        is_quiet = (start <= now <= end) if start <= end else (now >= start or now <= end)
        lines.append(f"Currently quiet: {is_quiet}")
        
        lines.append("\nRules:")
        for rule in self.rules:
            lines.append(f"  • {rule.name}: {rule.risk_level.value}")
        
        return "\n".join(lines)


class GovernedAgent:
    """
    An agent that respects governance rules.
    
    Wraps actions with permission checks.
    """
    
    def __init__(self, agent_id: str, governance: GovernanceEngine = None):
        self.agent_id = agent_id
        self.governance = governance or GovernanceEngine()
        self.action_log: List[dict] = []
    
    async def execute(self, action: str, permission: Permission, 
                      context: dict = None) -> Any:
        """
        Execute an action with governance checks.
        """
        context = context or {}
        context['agent_id'] = self.agent_id
        
        # Check if allowed
        allowed, reason = self.governance.check_action(action, permission, context)
        
        if not allowed:
            if "NEEDS APPROVAL" in reason or "CONFIRMATION NEEDED" in reason:
                # Request approval
                approved = self.governance.request_approval(action, reason)
                if approved:
                    context['approved'] = True
                    return await self.execute(action, permission, context)
            
            # Log blocked action
            self.action_log.append({
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "permission": permission.value,
                "result": "blocked",
                "reason": reason
            })
            
            raise PermissionError(f"Action blocked: {reason}")
        
        # Execute action (in real implementation, call actual function)
        result = f"Executed: {action}"
        
        # Log successful action
        self.action_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "permission": permission.value,
            "result": "success"
        })
        
        return result
    
    def get_action_history(self) -> List[dict]:
        """Get history of actions."""
        return self.action_log


def main():
    print("⚔️ Ares Session 10: Governance")
    print("Rules, permissions, and boundaries.\n")
    
    # Create governance engine
    gov = GovernanceEngine()
    
    # Create governed agent
    agent = GovernedAgent("assistant-1", gov)
    
    print(gov.get_status())
    print()
    
    # Test cases
    test_cases = [
        ("Read file: config.json", Permission.READ, {}),
        ("rm -rf /", Permission.EXECUTE, {}),
        ("Send email to team", Permission.EXTERNAL, {"critical": True}),
        ("API key: sk-abc123", Permission.WRITE, {}),
    ]
    
    print("Testing governance rules:")
    print("-" * 50)
    
    for action, permission, context in test_cases:
        allowed, reason = gov.check_action(action, permission, context)
        status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
        print(f"\n{status}: {action}")
        if reason:
            print(f"   Reason: {reason}")
    
    print("\n" + "="*50)
    print("Action history will be logged for audit.")


if __name__ == "__main__":
    main()
