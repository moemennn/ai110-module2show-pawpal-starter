# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

PawPal+ is designed to make pet-care planning easier for a busy owner by combining a simple Streamlit UI with a small scheduling engine.

### Core features

- Sorting by preferred time: tasks can be organized chronologically so the day starts with the most time-sensitive work.
- Filtering by pet or completion state: the scheduler can isolate tasks for one pet or focus only on pending work.
- Conflict warnings: if multiple tasks share the same preferred time slot, the system raises a visible warning instead of failing.
- Daily and weekly recurrence: recurring tasks can be marked complete and the next occurrence is automatically created with the correct due date.
- Daily plan generation: the app chooses a feasible set of tasks, explains the plan, and presents the final schedule clearly.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Verified terminal output from running the demo script in `main.py`:

```text
Today's Schedule
================
1. Feeding (10 min) [priority=high]
2. Morning walk (20 min) [priority=high]
3. Grooming (15 min) [priority=low]
```

## 🧪 Testing PawPal+

Run the full automated test suite with:

```bash
python -m pytest
```

These tests cover the most important scheduling behaviors for PawPal+: chronological sorting, recurring task rollover, conflict detection for duplicate preferred times, and basic owner/pet task collection and completion flows.

Verified terminal output from a successful run:

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/moemen/Desktop/AI110/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 17 items

tests/test_owner_pet_scheduler.py ......                                 [ 35%]
tests/test_pawpal.py .....                                               [ 64%]
tests/test_task.py ......                                                [100%]

============================== 17 passed in 0.01s ==============================
```

Confidence Level: ★★★★★

## 📐 Smarter Scheduling

The scheduler now includes a small set of lightweight but useful behaviors that make the demo more realistic and more adaptive.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` and `Scheduler.sort_tasks()` | Orders tasks by preferred time, then by urgency and duration. This lets the plan reflect a schedule-friendly ordering instead of only a raw list. |
| Filtering behavior | `Scheduler.filter_tasks_by_pet()` and `Scheduler.filter_tasks_by_status()` | Supports small view-level filtering such as showing only the tasks for one pet or only pending tasks. |
| Conflict detection logic | `Scheduler.detect_conflicts()` | Checks whether multiple tasks share the same preferred time slot and emits a warning message instead of crashing the program. |
| Recurring task logic | `Task._next_due_date()` and `Task.mark_complete()` | When a recurring daily or weekly task is completed, the model creates the next occurrence automatically using `timedelta`. |

## Demo Walkthrough

Use PawPal+ in the following way:

1. Open the Streamlit app in `app.py` and enter the owner's name.
2. Add one or more pets to the household.
3. Add care tasks for each pet, including duration, priority, and an optional preferred time.
4. Click **Generate schedule** to let the scheduler build a plan from the current owner-wide task list.
5. Review the schedule table and the scheduler explanation to see how the day was prioritized.

### Example workflow

A typical workflow looks like this:

- Add a pet such as Mochi.
- Add a task such as Morning walk with a preferred time of 09:15.
- Add another pet or task for the same time slot to trigger a conflict warning.
- Generate the schedule and inspect the sorted, pending, and recurring task views.

### Key scheduler behaviors shown in the UI

- Sorting by time ensures the tasks appear in chronological order.
- Conflict warnings use `st.warning()` to clearly surface overlapping time slots.
- Filtered pending tasks help the owner focus on what still needs to be scheduled.
- Recurring tasks use the same daily/weekly pattern to produce the next scheduled occurrence when complete.

### Sample CLI output from `main.py`

```text
Today's Schedule
================
1. Feeding (10 min) [priority=high]
2. Morning walk (20 min) [priority=high]
3. Grooming (15 min) [priority=low]

Sorted by preferred time
------------------------
1. Feeding @ 09:15 [high]
2. Morning walk @ 09:15 [high]
3. Grooming @ 11:45 [low]

Pending tasks
--------------
1. Feeding (Luna)
2. Morning walk (Mochi)
3. Grooming (Luna)

Mochi task list
----------------
1. Morning walk @ 09:15

Recurring tasks
----------------
1. Grooming [daily]

Conflict warnings
------------------
Warning: overlapping tasks at 09:15 for different pets: Morning walk, Feeding.
```
