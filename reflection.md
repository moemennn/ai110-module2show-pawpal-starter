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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

One tradeoff my scheduler makes is that it currently checks for exact `preferred_time` matches when it detects conflicts, instead of calculating whether two tasks overlap by duration. This keeps the conflict logic lightweight, easy to explain, and reliable for a small demo app, but it can miss cases where tasks are genuinely overlapping even if their preferred start times differ. For example, two tasks could both be assigned to a morning window but still span different durations in a way that creates a real overlap. That tradeoff is reasonable here because the current goal is to catch obvious scheduling collisions quickly without adding more complex duration-interval logic to the model.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
