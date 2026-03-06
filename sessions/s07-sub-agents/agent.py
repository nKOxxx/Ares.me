#!/usr/bin/env python3
"""
Session 07: Sub-Agents
Parallel execution with isolated agent sessions.
"""

import asyncio
import uuid
from typing import List, Dict, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import time


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SubAgentResult:
    """Result from a sub-agent task."""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: str = None
    started_at: datetime = None
    completed_at: datetime = None
    duration_ms: int = 0


@dataclass
class SubAgentTask:
    """A task to be executed by a sub-agent."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = "Unnamed Task"
    action: Callable = None
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    priority: int = 1  # Higher = more important
    timeout_seconds: int = 60


class SubAgent:
    """
    Isolated agent that can execute tasks independently.
    
    Think of this as a 'worker' that handles one specific job.
    """
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or str(uuid.uuid4())[:8]
        self.memory: Dict[str, Any] = {}  # Isolated memory
        self.created_at = datetime.now()
    
    async def execute(self, task: SubAgentTask) -> SubAgentResult:
        """Execute a task and return result."""
        result = SubAgentResult(
            task_id=task.task_id,
            status=TaskStatus.RUNNING,
            started_at=datetime.now()
        )
        
        try:
            # Simulate isolated execution
            if asyncio.iscoroutinefunction(task.action):
                output = await asyncio.wait_for(
                    task.action(*task.args, **task.kwargs),
                    timeout=task.timeout_seconds
                )
            else:
                # Run sync function in executor for true isolation
                loop = asyncio.get_event_loop()
                output = await asyncio.wait_for(
                    loop.run_in_executor(None, task.action, *task.args, **task.kwargs),
                    timeout=task.timeout_seconds
                )
            
            result.status = TaskStatus.COMPLETED
            result.result = output
        
        except asyncio.TimeoutError:
            result.status = TaskStatus.FAILED
            result.error = f"Timeout after {task.timeout_seconds}s"
        
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
        
        result.completed_at = datetime.now()
        result.duration_ms = int(
            (result.completed_at - result.started_at).total_seconds() * 1000
        )
        
        return result


class SubAgentManager:
    """
    Manages multiple sub-agents for parallel task execution.
    """
    
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.agents: Dict[str, SubAgent] = {}
        self.results: Dict[str, SubAgentResult] = {}
    
    def spawn(self, name: str = None) -> SubAgent:
        """Create a new sub-agent."""
        agent = SubAgent(agent_id=name)
        self.agents[agent.agent_id] = agent
        return agent
    
    async def execute_single(self, task: SubAgentTask) -> SubAgentResult:
        """Execute one task with a fresh sub-agent."""
        agent = self.spawn(f"worker-{task.task_id}")
        result = await agent.execute(task)
        self.results[task.task_id] = result
        return result
    
    async def execute_parallel(self, tasks: List[SubAgentTask]) -> List[SubAgentResult]:
        """
        Execute multiple tasks in parallel.
        
        This is the key benefit - multiple agents working simultaneously.
        """
        print(f"[SUB-AGENTS] Spawning {len(tasks)} parallel tasks...")
        
        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def run_with_limit(task: SubAgentTask) -> SubAgentResult:
            async with semaphore:
                return await self.execute_single(task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(
            *[run_with_limit(task) for task in tasks],
            return_exceptions=True
        )
        
        # Convert exceptions to failed results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed = SubAgentResult(
                    task_id=tasks[i].task_id,
                    status=TaskStatus.FAILED,
                    error=str(result)
                )
                processed_results.append(failed)
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_summary(self) -> str:
        """Get execution summary."""
        completed = sum(1 for r in self.results.values() if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in self.results.values() if r.status == TaskStatus.FAILED)
        total_time = sum(r.duration_ms for r in self.results.values())
        
        return f"Tasks: {completed} completed, {failed} failed | Total time: {total_time}ms"


# Example task functions
async def research_topic(topic: str) -> str:
    """Simulate researching a topic."""
    await asyncio.sleep(1)  # Simulate work
    return f"Research on '{topic}': Found 5 key insights"


async def analyze_data(data_id: str) -> str:
    """Simulate data analysis."""
    await asyncio.sleep(1.5)
    return f"Analysis of {data_id}: 3 trends identified"


async def draft_email(recipient: str) -> str:
    """Simulate drafting an email."""
    await asyncio.sleep(0.8)
    return f"Draft email to {recipient}: Ready for review"


async def check_api_status(service: str) -> str:
    """Simulate API health check."""
    await asyncio.sleep(0.5)
    return f"{service} API: Operational"


def sync_task(name: str) -> str:
    """Example synchronous task."""
    time.sleep(1)
    return f"Sync task '{name}' completed"


async def main():
    print("⚔️ Ares Session 07: Sub-Agents")
    print("Parallel execution with isolated agent sessions.\n")
    
    manager = SubAgentManager(max_concurrent=3)
    
    # Example 1: Single task
    print("1. Single Task Execution")
    print("-" * 30)
    task = SubAgentTask(
        name="Research",
        action=research_topic,
        args=("AI agents",)
    )
    result = await manager.execute_single(task)
    print(f"Result: {result.result}")
    print(f"Duration: {result.duration_ms}ms\n")
    
    # Example 2: Parallel execution
    print("2. Parallel Task Execution")
    print("-" * 30)
    
    tasks = [
        SubAgentTask(name="Research AI", action=research_topic, args=("AI safety",)),
        SubAgentTask(name="Analyze Data", action=analyze_data, args=("sales_q1",)),
        SubAgentTask(name="Draft Email", action=draft_email, args=("team@company.com",)),
        SubAgentTask(name="Check API", action=check_api_status, args=("payment",)),
        SubAgentTask(name="Sync Task", action=sync_task, args=("cleanup",)),
    ]
    
    start_time = time.time()
    results = await manager.execute_parallel(tasks)
    total_time = (time.time() - start_time) * 1000
    
    print("\nResults:")
    for result in results:
        status_icon = "✓" if result.status == TaskStatus.COMPLETED else "✗"
        print(f"  {status_icon} {result.task_id}: {result.result or result.error} ({result.duration_ms}ms)")
    
    print(f"\nTotal wall-clock time: {total_time:.0f}ms")
    print(f"Sequential would take: ~{sum(r.duration_ms for r in results)}ms")
    print(f"Speedup: {sum(r.duration_ms for r in results) / total_time:.1f}x\n")
    
    print(manager.get_summary())


if __name__ == "__main__":
    asyncio.run(main())
