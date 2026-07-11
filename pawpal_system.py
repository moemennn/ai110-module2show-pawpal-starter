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
        """Store a preference that can influence the plan."""
        if preference and preference not in self.preferences:
            self.preferences.append(preference)

    def update_availability(self, availability_windows: List[str]) -> None:
        """Replace the owner's availability windows."""
        self.availability_windows = list(availability_windows)

    def set_time_limit(self, minutes: int) -> None:
        """Set the daily time budget for care tasks."""
        if minutes < 0:
            raise ValueError("daily_time_limit cannot be negative")
        self.daily_time_limit = minutes

    def add_pet(self, pet: "Pet") -> None:
        """Attach a pet to this owner."""
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self

    def get_all_tasks(self) -> List[Task]:
        """Collect every task across the owner's pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.care_tasks)
        return tasks


@dataclass
class Pet:
    """Represents a pet profile and its care needs."""

    name: str
    species: str
    age: Optional[int] = None
    special_needs: List[str] = field(default_factory=list)
    routine: List[str] = field(default_factory=list)
    care_tasks: List["Task"] = field(default_factory=list)
    owner: Optional["Owner"] = None

    def update_profile(
        self,
        *,
        species: Optional[str] = None,
        age: Optional[int] = None,
        routine: Optional[List[str]] = None,
    ) -> None:
        """Update the pet's stored profile details."""
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age
        if routine is not None:
            self.routine = list(routine)

    def add_special_need(self, need: str) -> None:
        """Append a special care need."""
        if need and need not in self.special_needs:
            self.special_needs.append(need)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        if task not in self.care_tasks:
            self.care_tasks.append(task)
        task.pet = self

    def get_care_requirements(self) -> List[str]:
        """Return a summary of the pet's care needs."""
        requirements = list(self.special_needs)
        requirements.extend(self.routine)
        return requirements


@dataclass
class Task:
    """Represents a single pet-care activity that may be scheduled."""

    description: str
    duration_minutes: int = 0
    frequency: str = "once"
    completed: bool = False
    category: str = "general"
    priority: str = "medium"
    required: bool = True
    recurring: bool = False
    preferred_time: Optional[str] = None
    notes: str = ""
    pet: Optional["Pet"] = None

    def __post_init__(self) -> None:
        """Validate task fields during initialization."""
        if not self.description.strip():
            raise ValueError("description cannot be empty")
        if self.duration_minutes < 0:
            raise ValueError("duration_minutes cannot be negative")
        self.frequency = self.frequency.lower()
        self.priority = self.priority.lower()

    def update_priority(self, priority: str) -> None:
        """Change the task priority."""
        self.priority = priority.lower()

    def change_duration(self, duration_minutes: int) -> None:
        """Change the task duration."""
        if duration_minutes < 0:
            raise ValueError("duration_minutes cannot be negative")
        self.duration_minutes = duration_minutes

    def mark_complete(self) -> None:
        """Mark the task complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task incomplete."""
        self.completed = False

    def set_preferred_time(self, preferred_time: str) -> None:
        """Store a preferred time for the task."""
        self.preferred_time = preferred_time

    def update_duration(self, duration_minutes: int) -> None:
        """Update the task duration."""
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than zero")
        self.duration_minutes = duration_minutes

    def update_frequency(self, frequency: str) -> None:
        """Update how often the task repeats."""
        if not frequency.strip():
            raise ValueError("frequency cannot be empty")
        self.frequency = frequency.lower()


CareTask = Task


@dataclass
class ScheduleEntry:
    """Represents one scheduled task placed into a daily plan."""

    task: Task
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    reason: str = ""


@dataclass
class DailyPlan:
    """Stores the final daily schedule and its explanation."""

    date: Optional[date] = None
    total_planned_time: int = 0
    explanation: str = ""
    tasks: List[Task] = field(default_factory=list)
    schedule_entries: List[ScheduleEntry] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the plan."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the plan."""
        self.tasks = [existing_task for existing_task in self.tasks if existing_task is not task]

    def add_schedule_entry(self, entry: ScheduleEntry) -> None:
        """Add a scheduled slot to the plan."""
        if entry not in self.schedule_entries:
            self.schedule_entries.append(entry)

    def remove_schedule_entry(self, entry: ScheduleEntry) -> None:
        """Remove a scheduled slot from the plan."""
        self.schedule_entries = [existing_entry for existing_entry in self.schedule_entries if existing_entry is not entry]

    def calculate_total_time(self) -> int:
        """Return the sum of planned task durations."""
        return sum(task.duration_minutes for task in self.tasks)

    def generate_explanation(self) -> str:
        """Describe why the plan looks the way it does."""
        return (
            f"Planned {len(self.tasks)} task(s) totaling {self.calculate_total_time()} minutes "
            "for the day."
        )


@dataclass
class Scheduler:
    """Builds and explains a daily care schedule from constraints and tasks."""

    available_time: int = 0
    constraints: List[str] = field(default_factory=list)

    def _priority_score(self, task: Task) -> int:
        """Map a task's priority to a sortable score."""
        return {"high": 3, "medium": 2, "low": 1}.get(task.priority, 0)

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by priority and other scheduling rules."""
        priority_order = {
            "required": 0,
            "optional": 1,
        }
        return sorted(
            tasks,
            key=lambda task: (
                priority_order["required" if task.required else "optional"],
                -self._priority_score(task),
                task.duration_minutes,
            ),
        )

    def filter_tasks(self, tasks: List[Task]) -> List[Task]:
        """Remove tasks that are not feasible under the current constraints."""
        remaining_budget = self.available_time
        filtered: List[Task] = []
        for task in self.sort_tasks(tasks):
            if task.completed:
                continue
            if task.duration_minutes <= remaining_budget:
                filtered.append(task)
                remaining_budget -= task.duration_minutes
            elif task.required:
                continue
        return filtered

    def resolve_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Resolve overlapping or contradictory task requirements."""
        deduped: dict[tuple[str, Optional[str]], Task] = {}
        for task in tasks:
            key = (task.description.lower(), task.preferred_time)
            existing = deduped.get(key)
            if existing is None:
                deduped[key] = task
                continue

            if self._priority_score(task) > self._priority_score(existing):
                deduped[key] = task
            elif self._priority_score(task) == self._priority_score(existing):
                if task.duration_minutes > existing.duration_minutes:
                    deduped[key] = task
        return list(deduped.values())

    def build_daily_plan(self, owner: Owner, pet: Optional[Pet] = None) -> DailyPlan:
        """Create a DailyPlan for the owner's pet or, if provided, a chosen pet."""
        if pet is not None:
            tasks = list(pet.care_tasks)
        else:
            tasks = owner.get_all_tasks()

        time_budget = self.available_time or owner.daily_time_limit
        self.available_time = time_budget

        ordered_tasks = self.sort_tasks(tasks)
        feasible_tasks = self.filter_tasks(ordered_tasks)
        resolved_tasks = self.resolve_conflicts(feasible_tasks)

        plan = DailyPlan(
            date=date.today(),
            total_planned_time=sum(task.duration_minutes for task in resolved_tasks),
            tasks=resolved_tasks,
        )
        plan.explanation = self.explain_plan(plan)
        return plan

    def explain_plan(self, plan: DailyPlan) -> str:
        """Return a short explanation for why the final plan was chosen."""
        task_descriptions = ", ".join(task.description for task in plan.tasks)
        return (
            f"The plan prioritizes {task_descriptions} based on time budget, "
            "task priority, and the owner's constraints."
        )
