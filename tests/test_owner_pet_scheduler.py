from pawpal_system import Owner, Pet, Scheduler, Task


def test_owner_collects_all_tasks_from_all_pets():
    owner = Owner(name="Jordan", daily_time_limit=60)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    walk = Task(description="Morning walk", duration_minutes=20, priority="high")
    feed = Task(description="Evening feed", duration_minutes=10, priority="medium")

    dog.add_task(walk)
    cat.add_task(feed)

    owner.add_pet(dog)
    owner.add_pet(cat)

    tasks = owner.get_all_tasks()

    assert tasks == [walk, feed]


def test_pet_add_task_links_the_task_to_the_pet():
    pet = Pet(name="Mochi", species="dog")
    walk = Task(description="Morning walk", duration_minutes=20, priority="high")

    pet.add_task(walk)

    assert walk.pet is pet
    assert pet.care_tasks == [walk]


def test_scheduler_builds_daily_plan_from_owner_tasks():
    owner = Owner(name="Jordan", daily_time_limit=60)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    walk = Task(description="Morning walk", duration_minutes=20, priority="high")
    feed = Task(description="Feeding", duration_minutes=10, priority="medium")
    groom = Task(description="Grooming", duration_minutes=15, priority="low")

    pet.add_task(walk)
    pet.add_task(feed)
    pet.add_task(groom)

    scheduler = Scheduler(available_time=45, constraints=["priority", "duration"])
    plan = scheduler.build_daily_plan(owner)

    assert [task.description for task in plan.tasks] == ["Morning walk", "Feeding", "Grooming"]
    assert plan.calculate_total_time() == 45
