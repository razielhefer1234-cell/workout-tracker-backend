# Workout Tracker Backend — Practical Build Plan

## Purpose

Build a complete Django REST Framework backend that proves you can design a database, create a secure API, test important behavior, and deploy it.

This plan is intentionally in the middle: it gives you enough direction to keep moving, but it does not require a large document before you start coding.

**Suggested pace:** 10 focused sessions of about 3 hours each. Taking longer when you meet a new concept is completely fine.

---

## Version 1 scope

The finished API should let a user:

1. Register and log in with JWT.
2. Browse a reusable exercise catalog.
3. Create a workout containing multiple exercises.
4. Edit or delete their workouts.
5. Schedule a workout for a date and time.
6. Mark a scheduled workout as completed and record actual performance.
7. View their workout history.
8. View two or three simple progress reports.
9. Access only their own private data.

Do not add a frontend, payments, AI, social features, coaches, notifications, Celery, Redis, or microservices in version 1.

## Five decisions to make before coding

Spend no more than 30 minutes on these decisions and write the answers in `docs/scope.md`:

- A workout is a reusable plan; a workout session is one scheduled or completed occurrence of that plan.
- Decide which statuses a session can have. A simple choice is `scheduled`, `completed`, and `cancelled`.
- Decide whether users record planned values, actual values, or both. This plan recommends both.
- Decide whether completed history should remain unchanged when the original workout is edited. This plan recommends preserving it.
- Choose the reports you will build. Good version 1 reports are completed workouts per week, total training volume, and progress for one exercise.

After those decisions, begin coding. You do not need to answer every possible future question.

---

## Session 1 — Project foundation

### Build

- Create or clean up the Git repository.
- Create and activate a virtual environment.
- Install Django, Django REST Framework, PostgreSQL support, JWT support, environment configuration, testing tools, and OpenAPI documentation support.
- Create the Django project and the necessary apps.
- Connect local development to PostgreSQL.
- Add `.gitignore`, `.env.example`, `requirements.txt` or another dependency lock file, and a short README.
- Configure the custom user model before making the first real migration.

### Check

- Secrets and the real `.env` file are ignored by Git.
- Dependencies can be installed from the recorded dependency file.
- Django starts and can connect to PostgreSQL.
- `python manage.py check` succeeds.

### Finished when

A fresh development environment can install the dependencies, connect to the database, and start Django.

---

## Session 2 — Database models

### Recommended concepts

- **User:** account and authentication information.
- **Exercise:** reusable catalog entry such as Bench Press or Squat.
- **Workout:** a reusable workout definition owned by one user.
- **WorkoutExercise:** connects a workout to an exercise and stores planned sets, reps, weight, and position.
- **WorkoutSession:** one scheduled or completed occurrence of a workout.
- **ExerciseResult:** the actual performance of an exercise in a completed session.

`WorkoutExercise` should be a real model instead of a plain many-to-many field because the relationship itself has information: sets, reps, target weight, and order.

### Build

- Add fields and relationships for the concepts above.
- Add timestamps where they are useful.
- Add choices for session status.
- Add ordering for exercises inside a workout and for scheduled sessions.
- Prevent obviously invalid numeric values.
- Decide deletion behavior deliberately.
- Create migrations and apply them.
- Register useful models in Django admin.

### Essential rules

- Every private workout and session belongs to a user, directly or through a clear relationship.
- Sets and reps must be positive; weight cannot be negative.
- The same position should not appear twice within one workout.
- For version 1, do not allow the same exercise twice in one workout unless you have a real reason.
- Completed results must not silently change when the reusable workout is edited later. Store the required snapshot or result information with the completed session.

### Finished when

You can create a user, exercises, a workout with ordered exercises, and a scheduled session from Django admin or the Django shell without breaking the rules.

---

## Session 3 — Authentication

### Build

- User registration.
- JWT login.
- JWT refresh.
- A current-user endpoint.
- A meaningful logout method, such as refresh-token blacklisting.
- Password validation and safe password hashing through Django.

### Check

- Duplicate email registration fails cleanly.
- Passwords are never returned by the API or stored as plain text.
- Incorrect credentials do not reveal whether a particular email exists.
- Protected endpoints reject unauthenticated requests.
- Refresh and logout behave as documented.

### Finished when

A new user can register, log in, access a protected endpoint, refresh the token, and log out.

---

## Session 4 — Exercise catalog and workout CRUD

### Build

- Seed the database with a small, useful exercise catalog.
- Make the seed command safe to run more than once without creating duplicates.
- Add exercise list and detail endpoints.
- Add workout create, list, retrieve, update, and delete endpoints.
- Automatically assign the authenticated user as the workout owner.
- Filter every workout queryset to the current user.

### Check

- A user cannot choose another user as the owner in request data.
- User A cannot list, retrieve, update, or delete User B's workouts.
- Missing objects return a clear `404` response.
- Invalid input returns a useful `400` response.
- List endpoints are paginated.

### Finished when

Two test users can create workouts, but neither user can see or change the other user's records.

---

## Session 5 — Exercises inside workouts

### Build

- Allow exercises to be added to a workout.
- Allow planned sets, reps, weight, and order to be changed.
- Allow an exercise to be removed from a workout.
- Choose a clean response shape for a workout and its exercises.
- Use transactions when one request changes several related records and partial saving would be incorrect.

### Check

- The selected exercise exists.
- The workout belongs to the authenticated user.
- Duplicate exercises or positions are handled consistently.
- Invalid sets, reps, weight, and ordering values are rejected.
- A failed multi-record update does not leave half of the changes saved.

### Finished when

A user can build and edit a complete ordered workout through the API.

---


## Session 6 — Scheduling and status changes

### Build

- Create a workout session from one of the user's workouts.
- Accept a scheduled date and time.
- List sessions in chronological order.
- Filter sessions by status or date when useful.
- Allow valid status changes such as scheduled to completed or scheduled to cancelled.

### Rules

- A session must reference a workout owned by the current user.
- Invalid dates should be rejected according to your written rule.
- A completed session should not return to scheduled unless you intentionally support corrections.
- Cancelling an already completed session should be rejected.
- Store timezone-aware datetimes and document the API timezone behavior.

### Finished when

A user can schedule workouts, see upcoming sessions in the correct order, and perform only allowed status changes.

---
#I'm now here
## Session 7 — Completion, results, and history

### Build

- Add an operation for completing a workout session.
- Record actual sets, reps, weight, duration, or other values you selected.
- Store enough historical information so later workout edits do not rewrite old results.
- Add history endpoints for completed sessions.
- Allow comments in one clearly defined place, preferably on the session if the comment describes that occurrence.

### Check

- Completion is atomic: all valid results are saved or none are.
- A session cannot accidentally be completed twice.
- Results can only reference exercises belonging to that session.
- History is ordered and paginated.
- Editing the reusable workout does not change previously completed results.

### Finished when

A user can complete a scheduled workout, record results for its exercises, and later view accurate history.

---

## Session 8 — Progress reports

### Build

Implement only two or three useful reports:

- Number of completed workouts per week or month.
- Total training volume over a date range, using a clearly documented calculation.
- Progress for one exercise over time, such as best weight or total volume.

Use database queries and aggregation where appropriate. Do not create a large analytics system.

### Check

- Reports use only the authenticated user's data.
- Date filters are validated.
- Empty data returns a valid empty result rather than a server error.
- Create known test data and calculate expected totals by hand.
- Confirm the API result matches the hand calculation.

### Finished when

Each report answers a clear question and returns correct results for known data.

---

## Session 9 — Testing and API documentation

### Minimum automated test coverage

- Registration, login, refresh, and logout.
- Workout creation and editing.
- Adding, updating, and removing workout exercises.
- Scheduling and completing a session.
- Invalid numeric values and invalid status changes.
- Cross-user access attempts for every private resource type.
- Historical data remaining accurate after a workout edit.
- Report calculations.

You do not need to test Django itself. Focus on your rules, permissions, calculations, and workflows.

### Documentation

- Generate an OpenAPI schema and interactive documentation.
- Include authentication instructions.
- Add useful request and response examples for the important endpoints.
- Update the README with setup, environment variables, migrations, seeding, tests, and local run commands.

### Finished when

The full user journey passes in automated tests, and another developer can understand and call the API without reading your source code first.

---

## Session 10 — Production preparation and deployment

### Build

- Use environment variables for secrets and environment-specific settings.
- Set production `DEBUG` to false and configure allowed hosts.
- Use PostgreSQL in production.
- Run with a production application server rather than Django's development server.
- Use Docker if it is part of your learning goal or deployment method.
- Put HTTPS in front of the application using the host's managed proxy or Nginx.
- Add a simple health endpoint.
- Make logs available without recording passwords, JWTs, or other secrets.
- Write down a basic database backup and restore procedure.
- Run migrations and seed exercises during the deployment process deliberately, not from every web worker.

### Final checks

- Run Django's deployment checks.
- Test the deployed API over HTTPS.
- Repeat the complete user journey against production.
- Confirm User A still cannot access User B's data.
- Restart the service and confirm data remains available.
- Confirm no secret was committed to Git.

### Finished when

The deployed API securely completes the same critical workflow that passed locally.

---

## Working method for every session

Use this small loop instead of a giant checklist:

1. Choose one concrete result for the session.
2. Read only the documentation needed for that result.
3. Implement the smallest complete version.
4. Test success, invalid input, unauthenticated access, and access by another user.
5. Clean up names and remove temporary debugging output.
6. Commit the working state with a clear message.
7. Write one sentence describing the next task.

Do not wait until the end to test permissions or validation. Those are part of each feature.

## Final definition of done

The project is complete when all of the following work:

- A new developer can install and run it from the README.
- Migrations create the database from an empty PostgreSQL database.
- The exercise seed command is repeatable.
- A user can register, authenticate, and log out.
- A user can create a workout with ordered exercises.
- A user can schedule, complete, and review a workout session.
- Reports return correct results for known test data.
- Users cannot access one another's private information.
- Important rules and workflows have automated tests.
- API documentation matches the actual endpoints.
- The production deployment uses HTTPS, production settings, and persistent PostgreSQL data.

Once these are true, stop adding features. Record optional ideas in a version 2 list and move to your next project.
