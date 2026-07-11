# PawPal+ Project Reflection

## 1. System Design

Three core actions the user should be able to perform:

1- Add and manage a pet profile
The user should be able to add each pet’s basic information, such as name, species, age, care needs, feeding schedule, medication requirements, exercise level, and preferences.
Add or schedule pet care tasks
2- The user should be able to create tasks like walks, feeding, medication, grooming, playtime, enrichment, vet appointments, or cleaning. Each task should include details like priority, preferred time, duration, frequency, and any special instructions.
3- View and adjust today’s care plan
The user should be able to see a recommended daily plan that organizes tasks based on available time, importance, deadlines, and owner preferences. They should also be able to mark tasks complete, reschedule them, or ask why the assistant prioritized certain tasks.

**a. Initial design**

My initial UML design centered on five main classes to separate the problem into a clear data model and scheduling flow. The `Owner` class represents the person using the app, storing their name, availability windows, preferences, and daily time limit. The `Pet` class represents the animal being cared for, including its name, species, age, special needs, and routine. The `CareTask` class models one care activity, such as a walk, feeding, medication, grooming, or enrichment, with fields for duration, priority, recurrence, preferred time, and completed status. The `DailyPlan` class represents the final schedule for a day, holding the selected tasks, total planned time, and an explanation of why the plan was chosen. Finally, the `Scheduler` class is responsible for taking the owner, pet, and task data, ordering and filtering tasks by constraints, resolving conflicts, and generating the resulting daily plan. This structure keeps the app organized by separating the user context, pet context, task details, and the planning logic.

**b. Design changes**

Yes, my design changed slightly during implementation to make the model more realistic and easier to extend. I added an explicit back-reference from `Pet` to its `Owner` and from `CareTask` to its owning `Pet`, so the ownership relationship is no longer only implied by the `Owner` class holding a list of pets. I also introduced a `ScheduleEntry` dataclass to represent an actual scheduled slot in a `DailyPlan`, including start time, end time, and the reason that task was placed there. This change was necessary because the original skeleton only stored a list of tasks, which would make conflict resolution and explanation logic harder once the scheduler started assigning real times. These additions keep the UML closer to the way the Python code will actually behave during scheduling.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler currently considers the following constraints:

- available time budget from the owner's `daily_time_limit`
- task priority (`high`, `medium`, `low`)
- preferred time for chronological ordering
- completion status so only pending tasks are considered for the active plan
- recurrence/frequency so recurring tasks can be rolled forward automatically

I prioritized time and priority first because those are the most visible and actionable factors for a pet owner trying to create a practical daily care plan. Preferred time matters next because it provides a meaningful schedule order for the day. The other constraints, like recurrence and completion state, influence whether a task should remain in the planning flow or create the next future occurrence.

**b. Tradeoffs**

One tradeoff my scheduler makes is that it currently checks for exact `preferred_time` matches when it detects conflicts, instead of calculating whether two tasks overlap by duration. This keeps the conflict logic lightweight, easy to explain, and reliable for a small demo app, but it can miss cases where tasks are genuinely overlapping even if their preferred start times differ. For example, two tasks could both be assigned to a morning window but still span different durations in a way that creates a real overlap. That tradeoff is reasonable here because the current goal is to catch obvious scheduling collisions quickly without adding more complex duration-interval logic to the model.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant in several phases: first to help brainstorm the class structure for the scheduler and data model, then to refine the implementation details while building `Task`, `Scheduler`, and recurrence logic, and later to verify architectural consistency when the UI needed to reflect the backend behavior.

The most effective prompts were the ones that asked for concrete, implementation-aware guidance: for example, asking what methods should live on `Scheduler` to support sorting, filtering, and conflict detection; asking how to keep the recurrence behavior clean and testable; and asking whether the Mermaid UML needed to be updated after the final methods were added.

**b. Judgment and verification**

One example was when the AI suggested expanding the scheduler with a more complex overlap algorithm based on time intervals and duration ranges. I rejected that idea for the current version because it would add unnecessary complexity to a lightweight demo-oriented scheduler and would make the design harder to explain. Instead, I kept the conflict detection focused on duplicate preferred-time slots and made the warning visible, which matches the project's current goals.

I verified the AI's suggestions by writing or checking real tests, running the affected code paths, and comparing the results to the behavior described in the prompt. In practice, the strongest validation came from the automated test suite and by exercising the CLI demo so the final behavior was grounded in evidence rather than only in an AI-generated plan.

---

## 4. Testing and Verification

**a. What you tested**

I tested the behaviors that are most important for a pet-care scheduler:

- chronological sorting of tasks by preferred time
- filtering by pet and completion state
- conflict detection when two tasks occupy the same preferred time slot
- recurrence rollover for daily and weekly recurring tasks
- task completion and task count updates as the pet's care list grows

These tests were important because they protect the core user-facing behaviors: the app must be able to order tasks sensibly, warn the owner about obvious collisions, and actually carry recurring scheduling forward instead of only storing descriptive metadata.

**b. Confidence**

I am confident in the current implementation for the scope of this project because the behavior has been exercised through both real tests and a working demo run. The test suite passes cleanly and validates the most important scheduler features.

If I had more time, the next edge cases I would test are malformed or missing preferred times, tasks that exceed the owner's time budget, and more realistic overlap scenarios where two tasks share a window but do not have identical start times. I would also want to test the UI flow directly to confirm that the warning messages are understandable from a pet owner's perspective.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the way the scheduling engine became clearer as the project matured. The final code separates ownership, pet data, task state, and planning logic in a way that is easy to reason about, and the scheduler now shows visible behavior that the UI can expose directly.

**b. What you would improve**

If I had another iteration, I would improve the scheduling model by adding a more precise time-overlap engine, such as duration-based interval conflict detection instead of only checking identical preferred times. I would also add more explicit explanation metadata to `DailyPlan` so the scheduler can justify why certain tasks were selected or skipped.

**c. Key takeaway**

One important lesson is that being the lead architect means you cannot simply accept AI-generated structure uncritically. The AI is very good at proposing plausible abstractions and code, but the final system still needs a human to decide what is clean, minimal, and aligned with the actual product goal. Separating the work into clear phases, verifying the assumptions with tests, and keeping the architecture grounded in real behavior made the collaboration far more productive.
