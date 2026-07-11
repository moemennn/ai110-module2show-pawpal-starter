import pytest

from pawpal_system import Task


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
