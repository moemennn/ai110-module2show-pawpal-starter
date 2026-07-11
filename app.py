from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, daily_time_limit=120)
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner

st.markdown("### Add a pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} to {owner.name}'s household.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "tasks": len(pet.care_tasks)}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to a pet and let the scheduler use the owner-wide task list.")

if owner.pets:
    pet_options = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Assign task to pet", pet_options)
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        preferred_time = st.time_input("Preferred time (optional)", value=time(8, 0))
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        task = Task(
            description=task_title,
            duration_minutes=int(duration),
            priority=priority,
            required=True,
            preferred_time=preferred_time.strftime("%H:%M"),
        )
        selected_pet.add_task(task)
        st.success(f"Added '{task.description}' to {selected_pet.name}.")

    task_rows = []
    for pet in owner.pets:
        for task in pet.care_tasks:
            task_rows.append(
                {
                    "pet": pet.name,
                    "task": task.description,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                    "completed": task.completed,
                }
            )

    if task_rows:
        st.markdown("### Scheduler Preview")
        scheduler = Scheduler(available_time=owner.daily_time_limit, constraints=["priority", "duration"])
        pending_tasks = scheduler.filter_tasks_by_status(owner.get_all_tasks(), completed=False)
        sorted_tasks = scheduler.sort_by_time(pending_tasks)
        warnings = scheduler.detect_conflicts(sorted_tasks)

        if warnings:
            st.warning("⚠️ Conflict warning: " + " ".join(warnings))
        else:
            st.success("No duplicate time-slot conflicts were found.")

        st.write("Sorted pending tasks:")
        st.table(
            [
                {
                    "task": task.description,
                    "pet": task.pet.name if task.pet else "unknown",
                    "preferred_time": task.preferred_time or "unscheduled",
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                }
                for task in sorted_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first so you can attach tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Use the session-backed owner object to generate a plan from all pets and tasks.")

if st.button("Generate schedule"):
    scheduler = Scheduler(available_time=owner.daily_time_limit, constraints=["priority", "duration"])
    plan = scheduler.build_daily_plan(owner)
    pending_tasks = scheduler.filter_tasks_by_status(owner.get_all_tasks(), completed=False)
    warnings = scheduler.detect_conflicts(pending_tasks)

    st.success(plan.explanation)

    if warnings:
        st.warning("⚠️ Conflict warning: " + " ".join(warnings))

    st.table(
        [
            {
                "task": task.description,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "pet": task.pet.name if task.pet else "unknown",
                "preferred_time": task.preferred_time or "unscheduled",
            }
            for task in plan.tasks
        ]
    )
