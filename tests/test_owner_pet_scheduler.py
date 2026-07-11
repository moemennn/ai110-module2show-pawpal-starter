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


def test_scheduler_sort_by_time_orders_tasks_using_preferred_time():
    scheduler = Scheduler(available_time=45, constraints=["priority", "duration"])

    walk = Task(description="Morning walk", duration_minutes=20, priority="high")
    walk.set_preferred_time("09:30")
    feed = Task(description="Feeding", duration_minutes=10, priority="medium")
    feed.set_preferred_time("08:00")
    groom = Task(description="Grooming", duration_minutes=15, priority="low")
    groom.set_preferred_time("07:45")

    ordered = scheduler.sort_by_time([walk, feed, groom])

    assert [task.description for task in ordered] == ["Grooming", "Feeding", "Morning walk"]


def test_scheduler_filters_tasks_by_pet_and_completion_status():
    owner = Owner(name="Jordan", daily_time_limit=60)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task(description="Morning walk", duration_minutes=20, priority="high")
    walk.set_preferred_time("08:00")
    feed = Task(description="Feeding", duration_minutes=10, priority="medium")
    feed.set_preferred_time("18:00")
    grooming = Task(description="Grooming", duration_minutes=15, priority="low")
    grooming.set_preferred_time("10:00")

    dog.add_task(walk)
    cat.add_task(feed)
    cat.add_task(grooming)

    scheduler = Scheduler(available_time=60, constraints=["priority", "duration"])
    tasks = owner.get_all_tasks()

    filtered_by_pet = scheduler.filter_tasks_by_pet(tasks, pet_name="Mochi")
    filtered_by_status = scheduler.filter_tasks_by_status(tasks, completed=False)

    assert [task.description for task in filtered_by_pet] == ["Morning walk"]
    assert [task.description for task in filtered_by_status] == ["Morning walk", "Feeding", "Grooming"]


def test_scheduler_detect_conflicts_returns_warning_messages_for_same_time_slots():
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
