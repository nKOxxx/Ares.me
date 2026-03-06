#!/usr/bin/env python3
"""
Session 03: Planning
An agent that breaks tasks into steps before executing.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Step:
    """A single step in a plan."""
    id: int
    description: str
    status: StepStatus = StepStatus.PENDING
    result: Optional[str] = None
    depends_on: List[int] = None
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []


@dataclass
class Plan:
    """A task broken into steps."""
    goal: str
    steps: List[Step]
    
    def get_ready_steps(self) -> List[Step]:
        """Get steps that can be executed (dependencies met)."""
        completed = {s.id for s in self.steps if s.status == StepStatus.COMPLETED}
        return [
            s for s in self.steps 
            if s.status == StepStatus.PENDING 
            and all(dep in completed for dep in s.depends_on)
        ]
    
    def is_complete(self) -> bool:
        """Check if all steps are done."""
        return all(s.status in (StepStatus.COMPLETED, StepStatus.FAILED) for s in self.steps)


class Planner:
    """Agent that plans before executing."""
    
    def __init__(self):
        self.current_plan: Optional[Plan] = None
    
    def create_plan(self, goal: str) -> Plan:
        """
        Create a plan for the goal.
        In production: Use LLM to generate steps.
        """
        # Simulated planning for "build a website"
        if "website" in goal.lower():
            steps = [
                Step(1, "Clarify requirements with user", depends_on=[]),
                Step(2, "Design site structure", depends_on=[1]),
                Step(3, "Set up project files", depends_on=[2]),
                Step(4, "Build HTML/CSS", depends_on=[3]),
                Step(5, "Add JavaScript interactivity", depends_on=[4]),
                Step(6, "Test and deploy", depends_on=[5]),
            ]
        elif "research" in goal.lower():
            steps = [
                Step(1, "Define research scope", depends_on=[]),
                Step(2, "Search for sources", depends_on=[1]),
                Step(3, "Read and summarize", depends_on=[2]),
                Step(4, "Compile findings", depends_on=[3]),
            ]
        else:
            steps = [
                Step(1, f"Analyze: {goal}", depends_on=[]),
                Step(2, "Execute task", depends_on=[1]),
                Step(3, "Verify completion", depends_on=[2]),
            ]
        
        return Plan(goal=goal, steps=steps)
    
    def display_plan(self, plan: Plan) -> str:
        """Display plan for user approval."""
        lines = [f"📋 Plan: {plan.goal}", ""]
        for step in plan.steps:
            deps = f" (depends on: {step.depends_on})" if step.depends_on else ""
            lines.append(f"  {step.id}. {step.description}{deps}")
        lines.append("")
        lines.append("Approve this plan? (yes/no/modify)")
        return "\n".join(lines)
    
    def execute_step(self, step: Step) -> str:
        """Execute a single step."""
        step.status = StepStatus.IN_PROGRESS
        print(f"  ▶️ Executing: {step.description}")
        
        # Simulate work
        import time
        time.sleep(0.5)
        
        # Simulate success/failure
        step.status = StepStatus.COMPLETED
        step.result = f"Completed: {step.description}"
        print(f"  ✅ Done: {step.description}")
        return step.result
    
    def execute_plan(self, plan: Plan) -> str:
        """Execute the approved plan."""
        print(f"\n🚀 Executing plan: {plan.goal}\n")
        
        while not plan.is_complete():
            ready = plan.get_ready_steps()
            
            if not ready:
                # Check if we have failed dependencies
                failed = [s for s in plan.steps if s.status == StepStatus.FAILED]
                if failed:
                    return f"❌ Plan failed at step(s): {[s.id for s in failed]}"
                break
            
            for step in ready:
                self.execute_step(step)
        
        return f"✅ Plan completed: {plan.goal}"
    
    def chat(self, user_input: str) -> str:
        """Main interaction loop with planning."""
        
        # Check if user is responding to plan approval
        if self.current_plan and user_input.lower() in ("yes", "y", "approve"):
            return self.execute_plan(self.current_plan)
        
        if self.current_plan and user_input.lower() in ("no", "n", "reject"):
            self.current_plan = None
            return "❌ Plan rejected. What would you like to do instead?"
        
        # Create new plan for the goal
        plan = self.create_plan(user_input)
        self.current_plan = plan
        
        return self.display_plan(plan)


def main():
    print("⚔️ Ares Session 03: Planning")
    print("I break tasks into steps before executing.")
    print("Type 'exit' to quit\n")
    
    planner = Planner()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ("exit", "quit"):
            break
        
        if not user_input:
            continue
        
        response = planner.chat(user_input)
        print(f"\n{response}\n")


if __name__ == "__main__":
    main()
