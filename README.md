# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
