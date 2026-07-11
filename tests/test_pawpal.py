from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, Task


def test_task_completion_changes_status():
    task = Task(description="Morning walk", duration_minutes=20, priority="high")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Feeding", duration_minutes=10, priority="medium")

    assert len(pet.care_tasks) == 0

    pet.add_task(task)

    assert len(pet.care_tasks) == 1
    assert pet.care_tasks[0] is task


def test_scheduler_returns_tasks_in_chronological_order():
    scheduler = Scheduler(available_time=45, constraints=["priority", "duration"])

    walk = Task(description="Morning walk", duration_minutes=20, priority="high")
    walk.set_preferred_time("09:30")
    feed = Task(description="Feeding", duration_minutes=10, priority="medium")
    feed.set_preferred_time("08:00")
    groom = Task(description="Grooming", duration_minutes=15, priority="low")
    groom.set_preferred_time("07:45")

    ordered = scheduler.sort_by_time([walk, feed, groom])

    assert [task.description for task in ordered] == ["Grooming", "Feeding", "Morning walk"]


def test_marking_daily_task_complete_creates_next_day_task():
    pet = Pet(name="Luna", species="cat")
    task = Task(
        description="Feed cat",
        duration_minutes=10,
        frequency="daily",
        recurring=True,
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert len(pet.care_tasks) == 2


def test_scheduler_flags_duplicate_time_slots_as_conflict():
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    walk = Task(description="Morning walk", duration_minutes=20, priority="high")
    walk.set_preferred_time("08:00")
    walk.pet = dog

    feed = Task(description="Feeding", duration_minutes=10, priority="medium")
    feed.set_preferred_time("08:00")
    feed.pet = cat

    dog.add_task(walk)
    cat.add_task(feed)

    scheduler = Scheduler(available_time=60, constraints=["priority", "duration"])
    warnings = scheduler.detect_conflicts([walk, feed])

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
