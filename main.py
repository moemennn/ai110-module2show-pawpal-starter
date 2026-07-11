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

    dog.add_task(morning_walk)
    cat.add_task(feeding)
    cat.add_task(grooming)

    scheduler = Scheduler(available_time=45, constraints=["priority", "duration"])
    plan = scheduler.build_daily_plan(owner)

    print("Today's Schedule")
    print("=" * 16)
    for index, task in enumerate(plan.tasks, start=1):
        print(f"{index}. {task.description} ({task.duration_minutes} min) [priority={task.priority}]")


if __name__ == "__main__":
    main()
