#!/usr/bin/env python3
"""
Session 06: Heartbeats
Proactive execution with scheduled tasks.
"""

import schedule
import time
import threading
from datetime import datetime
from typing import List, Dict, Callable
from dataclasses import dataclass
from enum import Enum


class TaskPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class HeartbeatTask:
    """A scheduled proactive task."""
    name: str
    schedule: str  # "every 30 minutes", "daily at 09:00", etc.
    action: Callable
    priority: TaskPriority = TaskPriority.NORMAL
    enabled: bool = True
    last_run: datetime = None
    run_count: int = 0


class HeartbeatScheduler:
    """
    Proactive task scheduler.
    
    Runs tasks automatically without user prompting.
    """
    
    def __init__(self):
        self.tasks: List[HeartbeatTask] = []
        self.running = False
        self.scheduler_thread = None
    
    def add_task(self, task: HeartbeatTask):
        """Add a task to the scheduler."""
        self.tasks.append(task)
        
        # Parse schedule and add to schedule library
        if "every" in task.schedule and "minutes" in task.schedule:
            minutes = int(task.schedule.split()[1])
            schedule.every(minutes).minutes.do(self._run_task, task)
        elif "every" in task.schedule and "hours" in task.schedule:
            hours = int(task.schedule.split()[1])
            schedule.every(hours).hours.do(self._run_task, task)
        elif "daily at" in task.schedule:
            time_str = task.schedule.replace("daily at ", "").strip()
            schedule.every().day.at(time_str).do(self._run_task, task)
        elif "hourly" in task.schedule:
            schedule.every().hour.do(self._run_task, task)
    
    def _run_task(self, task: HeartbeatTask):
        """Execute a task and track it."""
        if not task.enabled:
            return
        
        print(f"\n[HEARTBEAT] Running: {task.name} ({task.priority.value})")
        try:
            result = task.action()
            task.last_run = datetime.now()
            task.run_count += 1
            print(f"[HEARTBEAT] ✓ {task.name} completed: {result}")
        except Exception as e:
            print(f"[HEARTBEAT] ✗ {task.name} failed: {e}")
    
    def start(self):
        """Start the scheduler in a background thread."""
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        print("[HEARTBEAT] Scheduler started")
    
    def _run_scheduler(self):
        """Main scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        print("[HEARTBEAT] Scheduler stopped")
    
    def get_status(self) -> str:
        """Get scheduler status."""
        lines = ["Scheduled Tasks:"]
        for task in self.tasks:
            status = "✓" if task.enabled else "✗"
            last = task.last_run.strftime("%H:%M") if task.last_run else "Never"
            lines.append(f"  {status} {task.name} ({task.schedule}) - Last: {last}, Runs: {task.run_count}")
        return "\n".join(lines)


# Example task functions
def check_email():
    """Simulate checking email."""
    return "No urgent emails"


def check_calendar():
    """Simulate checking calendar."""
    return "No meetings in next 2 hours"


def memory_cleanup():
    """Simulate cleaning old memories."""
    return "Cleaned 5 old entries"


def daily_summary():
    """Generate daily summary."""
    return "Summary: 3 tasks completed today"


def main():
    print("⚔️ Ares Session 06: Heartbeats")
    print("Proactive execution with scheduled tasks.\n")
    
    # Create scheduler
    scheduler = HeartbeatScheduler()
    
    # Add example tasks
    scheduler.add_task(HeartbeatTask(
        name="Check Email",
        schedule="every 30 minutes",
        action=check_email,
        priority=TaskPriority.HIGH
    ))
    
    scheduler.add_task(HeartbeatTask(
        name="Check Calendar",
        schedule="every 2 hours",
        action=check_calendar,
        priority=TaskPriority.NORMAL
    ))
    
    scheduler.add_task(HeartbeatTask(
        name="Memory Cleanup",
        schedule="daily at 02:00",
        action=memory_cleanup,
        priority=TaskPriority.LOW
    ))
    
    scheduler.add_task(HeartbeatTask(
        name="Daily Summary",
        schedule="daily at 18:00",
        action=daily_summary,
        priority=TaskPriority.NORMAL
    ))
    
    print(scheduler.get_status())
    print()
    
    # Start scheduler
    scheduler.start()
    
    print("\nHeartbeat scheduler is running...")
    print("Type 'status' to see task status")
    print("Type 'stop' to stop scheduler")
    print("Type 'exit' to quit\n")
    
    try:
        while True:
            user_input = input("> ").strip()
            
            if user_input.lower() == "exit":
                scheduler.stop()
                break
            
            if user_input.lower() == "stop":
                scheduler.stop()
                print("Scheduler stopped. Type 'start' to resume.")
                continue
            
            if user_input.lower() == "start":
                scheduler.start()
                continue
            
            if user_input.lower() == "status":
                print(f"\n{scheduler.get_status()}\n")
                continue
            
            if user_input:
                print(f"You: {user_input}")
                print("Agent: I'm monitoring tasks in the background...")
    
    except KeyboardInterrupt:
        print("\n\nStopping scheduler...")
        scheduler.stop()
        print("Goodbye!")


if __name__ == "__main__":
    main()
