# Workout Tracker Backend

A backend-only REST API for creating reusable workout plans, scheduling workout sessions, recording completed exercise results, reviewing workout history, and viewing progress reports.

This is a Django REST Framework learning project. The API and its automated tests are implemented; production deployment is still pending.

## Features

- User registration and JWT login, refresh, and logout
- Read-only exercise catalog with repeatable seed data
- User-owned workout plans and workout exercises
- Scheduled, cancelled, and completed workout sessions
- Actual sets, repetitions, weight, duration, and notes
- Completed-workout history with pagination
- Completed-workout count, training-volume, and highest-weight reports
- Owner-only access to private workout data
- Input and workflow validation
- 36 automated API tests
- OpenAPI schema and interactive Swagger documentation

## Technology

- Python
- Django and Django REST Framework
- PostgreSQL
- Redis caching
- Simple JWT
- drf-spectacular / OpenAPI

## Local setup

### Prerequisites

- Python 3
- PostgreSQL
- Redis

### 1. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Configure PostgreSQL

Create a PostgreSQL database and user for the project. The names and credentials must match the values you add to `.env`.

The PostgreSQL user also needs permission to create a test database when running Django's test suite.

### 3. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Set the following values in `.env`:

```dotenv
SECRET_KEY=replace-with-a-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=workout_tracker
POSTGRES_USER=replace-with-your-postgres-user
POSTGRES_PASSWORD=replace-with-your-postgres-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Do not commit `.env` or real credentials.

### 4. Start Redis

Make sure Redis is available at `redis://127.0.0.1:6379/1`. It is used to cache the exercise list.

### 5. Apply migrations and seed exercises

```bash
python manage.py migrate
python manage.py seed_exercises
```

The seed command is safe to run repeatedly because it uses `get_or_create`.

### 6. Run the development server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

## Authentication

Register a user with `POST /accounts/sign-up/`, then log in with `POST /login` using the same email and password. The login response contains `access` and `refresh` tokens.

Send the access token with protected requests:

```http
Authorization: Bearer <access-token>
```

Use `POST /token/refresh/` to obtain a new access token. Use `POST /accounts/logout/` with the refresh token in the request body to blacklist it.

In Swagger, click **Authorize** and paste only the access token. Swagger adds the `Bearer` prefix automatically.

## Main endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/accounts/sign-up/` | Register a user |
| `POST` | `/login` | Obtain access and refresh tokens |
| `POST` | `/token/refresh/` | Refresh an access token |
| `POST` | `/accounts/logout/` | Blacklist a refresh token |
| `GET` | `/accounts/me-info/` | Get the authenticated user |
| `GET` | `/exercise/exercises/` | List seeded exercises |
| `GET`, `POST` | `/workout/workouts/` | List or create workout plans |
| `GET`, `PATCH`, `DELETE` | `/workout/workouts/{id}/` | Retrieve, update, or delete a workout |
| `GET`, `POST` | `/workout/workouts-exercises/` | List or add exercises to workouts |
| `GET`, `POST` | `/workout/workouts-sessions/` | List or schedule workout sessions |
| `POST` | `/workout/workouts-sessions/{id}/complete/` | Complete a session and record results |
| `GET` | `/workout/workouts-sessions/history/` | View paginated completed history |
| `GET` | `/workout/workouts-sessions/completed_workouts_report/` | Count completed workouts |
| `GET` | `/workout/workouts-sessions/training_volume_report/` | View total training volume per exercise |
| `GET` | `/workout/workouts-sessions/highest_weight_report/` | View the highest weight per exercise |

Report endpoints require `start_date` and `end_date` query parameters in `YYYY-MM-DD` format. For example:

```text
/workout/workouts-sessions/training_volume_report/?start_date=2026-10-01&end_date=2026-10-31
```

Training volume is calculated from completed results as:

```text
sets completed × repetitions completed × weight completed
```

## API documentation

When `DEBUG=True`, interactive documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

Generate and validate a schema file from the command line:

```bash
python manage.py spectacular --file schema.yml --validate
```

The schema and Swagger routes are intentionally disabled when `DEBUG=False`.

## Tests

Run the full automated test suite:

```bash
python manage.py test
```

The tests cover authentication, owner permissions, workout and workout-exercise operations, session workflows, completed history, validation rules, and report calculations.

## Project documentation

- [`docs/decisions.md`](docs/decisions.md) describes the project scope and important decisions.
- [`docs/workout_tracker_backend_build_plan.md`](docs/workout_tracker_backend_build_plan.md) contains the practical build plan.

## Project status

The local API, tests, and interactive documentation are implemented. A Django Admin interface is the next project session, followed by production deployment with secure settings and HTTPS.
