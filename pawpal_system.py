from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Owner:
    """Represents the pet owner and their scheduling constraints."""

    name: str
    availability_windows: List[str] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    daily_time_limit: int = 0
    pets: List["Pet"] = field(default_factory=list)

    def add_preference(self, preference: str) -> None:
        """Add an owner preference that may affect scheduling."""
        pass

    def update_availability(self, availability_windows: List[str]) -> None:
        """Replace the owner's availability windows."""
        pass

    def set_time_limit(self, minutes: int) -> None:
        """Set the daily time budget available for pet care."""
        pass


@dataclass
class Pet:
    """Represents a pet profile and its care needs."""

    name: str
    species: str
    age: Optional[int] = None
    special_needs: List[str] = field(default_factory=list)
    routine: List[str] = field(default_factory=list)
    care_tasks: List["CareTask"] = field(default_factory=list)

    def update_profile(
        self,
        *,
        species: Optional[str] = None,
        age: Optional[int] = None,
        routine: Optional[List[str]] = None,
    ) -> None:
        """Update basic pet profile details."""
        pass

    def add_special_need(self, need: str) -> None:
        """Append a new special need for the pet."""
        pass

    def get_care_requirements(self) -> List[str]:
        """Return the pet's care requirements summary."""
        return []


@dataclass
class CareTask:
    """Represents a single pet-care task that may be scheduled."""

    title: str
    category: str = "general"
    duration_minutes: int = 0
    priority: str = "medium"
    required: bool = True
    recurring: bool = False
    preferred_time: Optional[str] = None
    notes: str = ""
    completed: bool = False

    def update_priority(self, priority: str) -> None:
        """Update the task's priority."""
        pass

    def change_duration(self, duration_minutes: int) -> None:
        """Change how long the task takes."""
        pass

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass

    def set_preferred_time(self, preferred_time: str) -> None:
        """Set a preferred time for the task."""
        pass


Task = CareTask


@dataclass
class DailyPlan:
    """Stores the final daily schedule and its explanation."""

    date: Optional[date] = None
    total_planned_time: int = 0
    explanation: str = ""
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a task to the plan."""
        pass

    def remove_task(self, task: CareTask) -> None:
        """Remove a task from the plan."""
        pass

    def calculate_total_time(self) -> int:
        """Return the sum of planned task durations."""
        return 0

    def generate_explanation(self) -> str:
        """Describe why the plan looks the way it does."""
        return ""


@dataclass
class Scheduler:
    """Builds and explains a daily care schedule from constraints and tasks."""

    available_time: int = 0
    constraints: List[str] = field(default_factory=list)

    def sort_tasks(self, tasks: List[CareTask]) -> List[CareTask]:
        """Return tasks ordered by priority and other scheduling rules."""
        return []

    def filter_tasks(self, tasks: List[CareTask]) -> List[CareTask]:
        """Remove tasks that are not feasible under the current constraints."""
        return []

    def resolve_conflicts(self, tasks: List[CareTask]) -> List[CareTask]:
        """Resolve overlapping or contradictory task requirements."""
        return []

    def build_daily_plan(self, owner: Owner, pet: Pet) -> DailyPlan:
        """Create a DailyPlan for the owner's pet."""
        return DailyPlan()

    def explain_plan(self, plan: DailyPlan) -> str:
        """Return a short explanation for why the final plan was chosen."""
        return ""
