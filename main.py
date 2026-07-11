from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", daily_time_limit=90)

    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    morning_walk = Task(description="Morning walk", duration_minutes=20, priority="high", required=True)
    feeding = Task(description="Feeding", duration_minutes=10, priority="high", required=True)
    grooming = Task(description="Grooming", duration_minutes=15, priority="low", required=False)

    morning_walk.set_preferred_time("09:15")
    feeding.set_preferred_time("09:15")
    grooming.set_preferred_time("11:45")
    grooming.recurring = True
    grooming.frequency = "daily"

    dog.add_task(morning_walk)
    cat.add_task(feeding)
    cat.add_task(grooming)

    scheduler = Scheduler(available_time=45, constraints=["priority", "duration", "time"])
    all_tasks = owner.get_all_tasks()
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    pending_tasks = scheduler.filter_tasks_by_status(sorted_by_time, completed=False)
    dog_only_tasks = scheduler.filter_tasks_by_pet(sorted_by_time, pet_name="Mochi")
    recurring_tasks = scheduler.filter_recurring_tasks(sorted_by_time)
    conflicts = scheduler.detect_conflicts(all_tasks)
    plan = scheduler.build_daily_plan(owner)

    print("Today's Schedule")
    print("=" * 16)
    for index, task in enumerate(plan.tasks, start=1):
        print(f"{index}. {task.description} ({task.duration_minutes} min) [priority={task.priority}]")

    print("\nSorted by preferred time")
    print("-" * 24)
    for index, task in enumerate(sorted_by_time, start=1):
        print(f"{index}. {task.description} @ {task.preferred_time} [{task.priority}]")

    print("\nPending tasks")
    print("-" * 14)
    for index, task in enumerate(pending_tasks, start=1):
        print(f"{index}. {task.description} ({task.pet.name if task.pet else 'unknown'})")

    print("\nMochi task list")
    print("-" * 16)
    for index, task in enumerate(dog_only_tasks, start=1):
        print(f"{index}. {task.description} @ {task.preferred_time}")

    print("\nRecurring tasks")
    print("-" * 16)
    for index, task in enumerate(recurring_tasks, start=1):
        print(f"{index}. {task.description} [{task.frequency}]")

    print("\nConflict warnings")
    print("-" * 18)
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No overlap detected.")


if __name__ == "__main__":
    main()
