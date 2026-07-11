from pawpal_system import Pet, Task


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
