# Workout Tracker Backend — Simple Scope

## Purpose

Build a backend API where a registered user can plan workouts, schedule them, record what they completed, view workout history, and see basic progress reports.

This is a backend-only learning project, not a polished SaaS.

## Main user flow

1. Register and log in with JWT.
2. View the exercise catalog.
3. Create a reusable workout plan with exercises and planned sets, reps, and weight.
4. Schedule the plan for a date and time.
5. Start the scheduled workout and record the actual results.
6. Complete the workout and view it in history.
7. View progress reports based on completed workouts.

## Required features

- Exercise catalog with repeatable seed data.
- Registration, JWT login, refresh, and logout/revocation.
- Create, read, update, and delete workout plans.
- Schedule, start, and complete workout sessions.
- Record actual sets, reps, weight, and an optional comment.
- List pending workouts and completed history.
- Paginate list endpoints.
- Allow users to access only their own data.
- Validate input and return clear API errors.
- Automated tests and OpenAPI/Swagger documentation.
- One production deployment using PostgreSQL and HTTPS.

## Important decisions

- A **workout plan** is a reusable template.
- A **workout session** is one scheduled use of that plan on a specific date.
- Session statuses are `scheduled`, `in_progress`, `cancelled`, and `completed`.
- Plans store intended targets; sessions store actual results.
- Editing a plan affects future sessions, not completed workout history.
- A comment belongs to a specific workout session.
- Completed sessions may be edited to correct mistakes.
- Deleting a plan must not delete completed history.
- Weight is recorded in kilograms.
- Date-times are stored in UTC using timezone-aware values.

## Progress reports

For a selected date range, return:

1. Number of completed workouts.
2. Total training volume per exercise.
3. Highest recorded weight per exercise.

Only completed sessions count toward reports.

## Not included

No frontend, Stripe, coaches, teams, social features, AI recommendations, nutrition tracking, reminders, uploads, WebSockets, microservices, Kubernetes, autoscaling, or advanced analytics.

## Finished when

The full user flow works, users cannot access one another's data, important behavior is tested and documented, and the API is deployed securely with production settings.
