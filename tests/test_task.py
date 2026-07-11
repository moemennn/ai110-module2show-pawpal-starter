from datetime import date, timedelta

import pytest

from pawpal_system import Pet, Task


def test_task_initializes_core_fields():
    task = Task(description="Morning walk", duration_minutes=20, frequency="daily")

    assert task.description == "Morning walk"
    assert task.duration_minutes == 20
    assert task.frequency == "daily"
    assert task.completed is False


def test_task_completion_helpers():
    task = Task(description="Feed cat", duration_minutes=10, frequency="daily")

    task.mark_complete()
    assert task.completed is True

    task.mark_incomplete()
    assert task.completed is False


def test_task_updates_duration_and_frequency():
    task = Task(description="Leash walk", duration_minutes=15, frequency="once")

    task.update_duration(25)
    task.update_frequency("daily")

    assert task.duration_minutes == 25
    assert task.frequency == "daily"


def test_task_rejects_invalid_duration():
    task = Task(description="Feed cat", duration_minutes=10, frequency="daily")

    with pytest.raises(ValueError):
        task.update_duration(0)


def test_mark_complete_creates_next_daily_occurrence():
    pet = Pet(name="Luna", species="cat")
    task = Task(
        description="Feed cat",
        duration_minutes=10,
        frequency="daily",
        recurring=True,
    )
    pet.add_task(task)

    task.mark_complete()

    assert task.completed is True
    assert len(pet.care_tasks) == 2

    next_task = pet.care_tasks[1]
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_mark_complete_creates_next_weekly_occurrence():
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        description="Brush coat",
        duration_minutes=15,
        frequency="weekly",
        recurring=True,
    )
    pet.add_task(task)

    task.mark_complete()

    assert task.completed is True
    assert len(pet.care_tasks) == 2

    next_task = pet.care_tasks[1]
    assert next_task.completed is False
    assert next_task.frequency == "weekly"
    assert next_task.due_date == date.today() + timedelta(days=7)
