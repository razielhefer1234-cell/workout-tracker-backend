# Workout Tracker Backend — Complete Learning-Project Build Plan

## 1. Purpose of this plan

This is a backend-only build plan for the roadmap.sh **Workout Tracker** project. It is deliberately detailed so you always know what to do next, but it does not give you implementation code, choose your database schema, or design your endpoints for you.

You will make the important engineering decisions yourself. The plan tells you:

- what questions to answer;
- what order to work in;
- what behavior must exist;
- what failure cases to handle;
- what to test;
- what “finished” means;
- what production work is appropriate for a learning project.

The target is a small, production-aware REST API—not a polished SaaS.

### Recommended learning stack

Use the stack you are currently learning:

- Python;
- Django;
- Django REST Framework;
- PostgreSQL;
- JWT authentication;
- an OpenAPI schema plus interactive API documentation;
- Git and GitHub;
- automated tests;
- Docker;
- a production application server;
- Nginx or an equivalent managed reverse proxy;
- HTTPS;
- one simple production deployment.

PostgreSQL is a technical choice, not a completed database design. You must still decide the tables, relationships, fields, constraints, and indexes.

## 2. Exact scope

The original brief requires a backend in which users can register, authenticate, manage workouts, schedule workouts, track completed workouts, and view progress reports. It also requires a relational database, tests, JWT security, seed exercise data, and OpenAPI documentation.

### Required functionality

Your finished API must support all of the following:

1. A reusable exercise catalog.
2. A repeatable data-seeding process for exercises.
3. User registration.
4. User login using JWT.
5. JWT refresh behavior.
6. A meaningful backend logout/revocation behavior.
7. Creation of a workout containing multiple exercises.
8. Reading a user's workouts.
9. Updating a workout.
10. Adding or updating workout comments.
11. Deleting a workout.
12. Scheduling a workout for a date and time.
13. Listing active or pending workouts in chronological order.
14. Recording enough information to identify past/completed workouts.
15. Generating at least a small set of useful progress reports.
16. Ensuring users can access only their own private workout data.
17. Input validation and consistent API errors.
18. Automated tests.
19. OpenAPI documentation with usable examples.
20. A deployed production instance using production settings.

### Explicit non-goals

Do **not** add these unless the required project is already completely finished and you intentionally start a separate version 2:

- frontend pages;
- React, Vue, mobile applications, or templates for users;
- subscriptions or Stripe;
- coaches, gyms, organizations, or teams;
- social feeds, likes, follows, or leaderboards;
- AI recommendations;
- meal or calorie tracking;
- wearable-device integrations;
- real-time features or WebSockets;
- email verification;
- password-reset email, unless you want one small optional exercise after completion;
- scheduled reminder emails or push notifications;
- Celery or Redis;
- file uploads or exercise videos;
- importing exercise data from a third-party API;
- data exports;
- microservices;
- Kubernetes;
- multi-region deployment;
- autoscaling;
- elaborate zero-downtime deployment;
- extensive analytics dashboards;
- perfect visual Swagger customization.

This exclusion list is important. “Production-ready learning project” means the API is safe, testable, documented, deployable, and recoverable. It does not mean building the operations department of a real fitness company.

## 3. Definition of done

The project is finished only when all of these statements are true:

- A new developer can clone the repository and understand how to run it.
- The application can start against a clean PostgreSQL database.
- Migrations build the schema without manual database editing.
- The exercise seeder can populate a clean database.
- Running the seeder again does not corrupt or unnecessarily duplicate data.
- A user can register and obtain JWT credentials.
- A user can refresh authentication and perform the defined logout action.
- An authenticated user can complete the entire workout workflow.
- Two different users never see or modify one another's private workout data.
- Invalid inputs produce clear 4xx responses rather than server errors.
- List endpoints cannot return unlimited data.
- Past-workout reports return correct results for known test data.
- Important behavior is covered by automated tests.
- The OpenAPI document describes the real API accurately.
- Interactive documentation can authenticate and call protected endpoints.
- No secret is committed to Git.
- The production deployment uses PostgreSQL, HTTPS, and a production server—not Django's development server.
- Production runs with debug mode disabled.
- Logs are available without exposing passwords or tokens.
- A health check and a basic database backup procedure exist.
- The complete critical user journey passes against the deployed API.

## 4. Timebox and working method

### Target duration

Use a target of **30–36 focused hours**:

- approximately 10–12 days at 3 hours per day;
- 7–8 days for the application itself;
- 2–3 days for production, documentation, and final testing;
- 1–2 buffer days for bugs and unfamiliar concepts.

Do not extend the project beyond roughly two weeks just to add features. If an essential feature is still broken, continue until it works. If the essential system works and you are merely polishing, stop and move to the next project.

### Structure every three-hour session

1. **First 10 minutes:** read yesterday's notes and select one concrete outcome.
2. **Next 20 minutes:** consult documentation for only the concepts needed today.
3. **Next 90 minutes:** implement one vertical slice.
4. **Next 40 minutes:** test success, failure, authentication, and ownership cases.
5. **Next 10 minutes:** clean names and remove temporary debugging output.
6. **Final 10 minutes:** commit the working state and write the next task.

Do not spend a full day rereading your course. Look things up while building. Documentation use is part of real development.

### Rule for every feature

Do not call a feature complete merely because the happy path works. For every feature, answer:

- What happens with valid input?
- What happens with invalid input?
- What happens without authentication?
- What happens when another user owns the object?
- What happens when the object does not exist?
- What happens at boundary values?
- Is the behavior documented?
- Is the important behavior tested?

## 5. Phase 0 — Convert the brief into your own specification

### Goal

Remove ambiguity before creating models or endpoints.

### Work to complete

Create a short `docs/scope.md` or equivalent planning note in your repository. In your own words, describe:

- the problem the backend solves;
- the single type of user in version 1;
- the complete journey from account creation to viewing progress;
- every required capability from the roadmap brief;
- the non-goals listed above;
- what will prove the project is finished.

### Product questions you must answer yourself

These questions affect your schema and API, so this plan intentionally does not answer them:

1. Is a reusable workout plan different from a scheduled workout occurrence?
2. What exactly makes a workout “pending,” “active,” “completed,” or “past”?
3. Does a user record planned performance, actual performance, or both?
4. What information must remain unchanged in historical records if a plan is edited later?
5. Is a comment attached to the reusable plan, a scheduled occurrence, or a completed occurrence?
6. Can a completed workout be edited?
7. What does deleting a workout mean when historical progress depends on it?
8. What two or three progress questions will the report feature answer?
9. Which unit or units are allowed for weight?
10. Which time zone is used for input and display, and what is stored in the database?

Write each answer as a small decision. Do not begin database modeling while these ideas are still unclear.

### Write acceptance scenarios

Write plain-language scenarios such as:

- Given a visitor with valid registration data, when they register, then an account is created safely.
- Given an authenticated user, when they create a valid workout, then it appears in their list.
- Given a second user, when they try to retrieve the first user's workout, then no private data is exposed.
- Given several pending workouts, when they are listed, then the order follows the defined scheduling rule.
- Given known completed-workout data, when a report is requested, then its totals match hand-calculated results.

Write scenarios for every required feature, including failure cases. These later become your test checklist.

### Completion gate

Do not leave this phase until:

- the meaning of every important domain word is written down;
- version 1 has a firm boundary;
- you can describe the full user journey without mentioning implementation details;
- reports have a clear purpose rather than merely “show some statistics.”

## 6. Phase 1 — Repository and development foundation

### Goal

Create a clean environment in which changes are reproducible and mistakes are easy to reverse.

### Repository tasks

- Create the Git repository.
- Add a Python-focused `.gitignore`.
- Ignore local environment files, virtual environments, caches, test artifacts, editor files, collected static files, and local database files.
- Add a starting README with the project name, purpose, current status, and chosen stack.
- Choose and record the supported Python version.
- Create a virtual environment.
- Install only the initial packages needed for Django, DRF, PostgreSQL connectivity, JWT, testing, environment configuration, and API schemas.
- Pin or lock dependency versions using one consistent dependency-management method.
- Separate runtime dependencies from development-only tools if your chosen workflow supports it cleanly.
- Make the first commit before application logic.

### Configuration tasks

- Decide whether to use one environment-driven settings file or a small base/development/production split.
- Do not create many settings files merely to appear professional.
- Make local settings convenient while ensuring production values come from environment variables.
- Create an example environment file containing key names and harmless placeholders only.
- Ensure the real environment file is ignored by Git.
- Configure local PostgreSQL from the beginning so development and production use the same database engine.
- Set an explicit time zone policy.
- Confirm Django's time-zone support is enabled.
- Configure DRF globally so authentication, default permissions, pagination, and error behavior are intentional rather than accidental defaults.

### Project-structure decisions

Decide for yourself:

- how many Django apps represent meaningful domain boundaries;
- where shared utilities belong;
- where tests live;
- where seed data lives;
- where API documentation configuration belongs;
- where environment-specific settings belong.

Avoid both extremes: one giant file and a complex enterprise folder tree. This is a small project.

### First smoke checks

- Start Django locally.
- Confirm it connects to PostgreSQL.
- Run initial migrations.
- Run the empty test suite successfully.
- Confirm the repository status contains no secret or generated junk.
- Confirm a fresh terminal can start the project by following the current README notes.

### Completion gate

- The repository is clean.
- Dependencies are reproducible.
- PostgreSQL works locally.
- Environment values are not hardcoded secrets.
- The application and test runner both start.

## 7. Phase 2 — Design the data model yourself

### Goal

Produce a deliberate relational design before writing Django models.

This is your design exercise. Do not copy a finished schema from a tutorial or ask an AI to generate all the models.

### Step 1: identify concepts

From your specification, identify the distinct domain concepts. For each candidate concept, ask:

- Does it have its own lifecycle?
- Can multiple other records refer to it?
- Does it belong to a user?
- Is it reusable or historical?
- Does it need to exist independently?
- Is it a real entity, or merely a field/value?

Do not create a table for every noun. Do not compress several different lifecycles into one record merely to reduce table count.

### Step 2: draw relationships

Draw an ER diagram yourself. For every relationship, label:

- one-to-one, one-to-many, or many-to-many;
- which side owns the relationship;
- whether the relationship is required;
- what should happen when the referenced record is deleted;
- whether ordering matters;
- whether duplicate relationships are allowed.

Pay special attention to the relationship between:

- the exercise catalog;
- a user's workout definition;
- exercises inside that workout;
- scheduled workout occurrences;
- completed performance/history;
- the user who owns private information.

The plan deliberately does not tell you how many tables those concepts should use.

### Step 3: define each field deliberately

For every proposed field, write down:

- purpose;
- data type;
- required versus optional;
- default, if one is meaningful;
- allowed range or choices;
- whether users may change it;
- whether it is public or private;
- whether it needs database uniqueness;
- whether it is frequently filtered or sorted;
- whether old records must preserve its old value.

Review numeric workout values carefully. Decide what zero means, whether negative values are ever valid, whether decimals are required, and what upper bounds prevent nonsense or abuse.

### Step 4: define integrity rules

List rules that must remain true even if future code calls the database incorrectly. For each rule, decide whether it belongs in:

- the database;
- model validation;
- serializer/input validation;
- a service/use-case layer;
- more than one layer.

Consider:

- required ownership;
- duplicate items;
- allowed state changes;
- valid dates;
- valid numeric ranges;
- required ordering;
- uniqueness of seeded exercises;
- historical records that should not disappear unexpectedly.

### Step 5: think about queries before indexes

Write the exact questions the database must answer frequently:

- Which private records belong to the current user?
- Which scheduled records are pending?
- Which records fall inside a date range?
- In what order are lists returned?
- Which relationships are loaded for detail output?
- Which values are grouped for reports?

Only after writing expected query patterns should you choose indexes. Do not add indexes to every field.

### Step 6: migration plan

- Create the initial models in small logical groups.
- Generate migrations and read them before applying them.
- Check that destructive operations are not present unexpectedly.
- Apply migrations to an empty local database.
- Reverse and reapply development migrations when safe, so you understand them.
- Never hand-edit the production database to avoid writing a migration.

### Schema review checklist

Before moving on, verify:

- every private record has an unambiguous ownership path;
- reusable definitions are distinguishable from historical occurrences if your requirements need that distinction;
- deleting a referenced item has an intentional outcome;
- units and time zones are not ambiguous;
- constraints protect the most important invariants;
- fields are not nullable without a reason;
- timestamps have a clear meaning;
- expected list/report queries are possible without parsing text blobs;
- naming reflects domain meaning rather than UI wording;
- the design is small enough to explain on one page.

### Completion gate

- You can explain the ER diagram aloud.
- You can justify every relationship and important constraint.
- You know how each required user action changes the data.
- You have not written endpoints to compensate for an unclear domain model.

## 8. Phase 3 — Design the API contract yourself

### Goal

Decide how clients interact with the domain before writing views.

### Create a resource/action inventory

For each required capability, identify:

- the resource or action involved;
- whether it creates, reads, replaces, partially updates, deletes, or calculates;
- whether it operates on one record or a collection;
- whether it changes persistent state;
- whether authentication is required;
- which ownership rule applies.

### Fill in an endpoint-planning table

Use this blank structure for every endpoint; fill it yourself:

| Question | Your decision |
|---|---|
| Purpose | |
| HTTP method | |
| URL shape | |
| Public or protected | |
| Ownership rule | |
| Request fields | |
| Success response | |
| Success status | |
| Validation failures | |
| Authentication failure | |
| Permission failure | |
| Not-found behavior | |
| Filters/order/pagination | |
| Side effects | |
| Transaction needed? | |
| Tests required | |

### Contract decisions you must make

- Choose one consistent API prefix and versioning approach.
- Decide whether compound workout creation uses one nested request or several smaller requests.
- Decide how clients reorder exercises, if ordering is supported.
- Decide whether deletion is permanent or preserves history.
- Decide how scheduling and completion are represented as API actions.
- Decide whether reports are collection endpoints, action endpoints, or a separate report resource.
- Decide how date ranges are passed.
- Decide which fields are read-only, writable, or derived.
- Decide how unknown fields are handled.
- Decide the response shape for validation errors.
- Decide whether unauthorized access to another user's object appears forbidden or not found, then use that decision consistently.

### HTTP behavior checklist

- Use methods according to their intended semantics.
- Return suitable success status codes for creation, reading, update, and deletion.
- Use 400-series responses for client mistakes.
- Never return a successful status with an error message hidden in the body.
- Keep response shapes stable.
- Return timestamps in an unambiguous format.
- Do not expose internal exception messages, stack traces, SQL, or secrets.
- Paginate collection endpoints.
- Make filtering and ordering fields explicit.
- Never accept the owner identity from the client when it can be derived from authentication.

### OpenAPI-first outline

At this point, write only a rough contract outline—not complete generated documentation. For each operation, record:

- summary;
- authentication requirement;
- input concept;
- output concept;
- main error cases.

This exposes missing decisions before implementation.

### Completion gate

- Every roadmap requirement maps to at least one planned API operation.
- Every operation has an authentication and ownership rule.
- Mutations have defined validation and error behavior.
- You have resolved nested-write versus separate-operation decisions.
- You have not yet written the endpoint implementation.

## 9. Phase 4 — Build the smallest running API skeleton

### Goal

Connect your project structure, database, and API framework without implementing all business behavior at once.

### Tasks

- Create the Django project and your chosen apps.
- Register apps intentionally.
- Configure DRF.
- Configure PostgreSQL through environment values.
- Decide whether the built-in user model is sufficient or whether you need a custom user model.
- Make that user-model decision before substantial migrations.
- Configure JWT authentication.
- Configure default permissions securely; prefer protected-by-default and explicitly open only public authentication operations.
- Configure pagination globally or deliberately per view.
- Wire a versioned API root.
- Add the schema and documentation routes.
- Add Django admin for development/inspection needs.
- Create a minimal health/readiness route later used by deployment checks.

### What not to do yet

- Do not implement every serializer at once.
- Do not add reports.
- Do not optimize queries prematurely.
- Do not build Docker before the basic API works locally.
- Do not create generic abstractions for one or two views.

### Smoke tests

- The API root responds.
- The schema generator runs.
- The docs UI opens.
- A protected placeholder rejects anonymous requests.
- The database connection works.
- The test runner works.

### Completion gate

You have a small, boring, running skeleton into which features can be added vertically.

## 10. Phase 5 — Exercise catalog and repeatable seeding

### Goal

Build the reference-data feature on which workouts depend.

### Decide the catalog rules

Answer these yourself:

- Are exercises globally shared or user-created in version 1?
- Who may create, edit, or delete catalog entries?
- What makes two exercises duplicates?
- Is category required, muscle group required, or may either be used?
- Are categories fixed choices or database-managed data?
- What fields are searchable or filterable?
- What happens if a referenced exercise is later changed or removed?

Keep the answer small. A learning version normally needs one curated catalog rather than a community content system.

### Prepare seed data

- Create a modest dataset large enough to exercise categories, muscle groups, search, and pagination.
- Use fictional/general exercise information rather than copying a proprietary dataset.
- Store seed source data in version control using a format you understand.
- Give each seed record a stable natural key or other deliberate identity.
- Validate all seed data before or during import.
- Ensure the seeding process is repeatable.
- Decide whether repeat execution skips, updates, or reconciles existing records.
- Print or log a useful summary of created, updated, skipped, and failed records.
- Fail clearly on malformed seed data.

### Implement catalog API behavior

- Return collection and detail representations.
- Add only useful search/filter choices.
- Paginate the collection.
- Ensure ordinary users cannot mutate global reference data unless your written requirements intentionally allow it.
- Ensure unavailable records fail cleanly.

### Test checklist

- Empty database seeds successfully.
- Running the seeder twice produces the intended result.
- Malformed data is rejected or reported clearly.
- Duplicate identity is handled according to your rule.
- Anonymous access matches your contract.
- Ordinary user write access matches your contract.
- Search and filters return expected records.
- Pagination behaves correctly.
- Detail lookup returns 404 for a missing record.

### Completion gate

The exercise catalog can be produced predictably on every new environment and safely consumed by later workout features.

## 11. Phase 6 — Authentication lifecycle

### Goal

Implement a complete, testable JWT authentication lifecycle without turning account management into its own product.

### Registration decisions

Before implementation, define:

- which credential identifies a user;
- which fields are required at registration;
- whether identifiers are case-sensitive;
- password requirements;
- whether registration immediately enables login;
- which fields a user may later update;
- whether a minimal current-user endpoint is necessary.

Do not add profiles full of fitness information unless a required report genuinely needs that information.

### Registration behavior

- Validate required fields.
- Normalize identifiers consistently.
- Enforce database uniqueness where appropriate.
- Use Django's password-hashing APIs rather than treating a password as an ordinary field.
- Apply configured password validators.
- Never return the raw password.
- Never log the password.
- Return a documented response and status.
- Handle duplicate registration predictably.

### Login behavior

- Accept only the documented credentials.
- Return the intended access and refresh tokens.
- Use a generic authentication failure that does not reveal too much about whether an account exists.
- Ensure inactive or otherwise disallowed accounts cannot log in.
- Decide and document token lifetimes.
- Keep access tokens reasonably short-lived.
- Do not place tokens in query strings.

### Refresh behavior

- Provide a supported refresh operation.
- Decide whether refresh-token rotation is enabled.
- If rotating, decide whether the used token is blacklisted.
- Confirm a valid refresh token produces the intended new token state.
- Confirm malformed, expired, or revoked refresh tokens fail cleanly.

### Logout behavior

JWT logout is not automatically the same as deleting a token on a client. Define what the backend guarantees:

- If logout means refresh-token revocation, enable and persist the required revocation mechanism.
- Decide what happens to an already-issued access token.
- Document that behavior honestly.
- Do not pretend a server has invalidated a stateless access token if it remains valid until expiration.

### Authentication test checklist

- Valid registration succeeds.
- Missing required registration data fails.
- Invalid identifiers fail.
- Weak or invalid passwords fail according to your policy.
- Duplicate identity fails safely.
- Password is stored hashed.
- Password never appears in the response.
- Correct credentials log in.
- Incorrect credentials fail generically.
- Valid access token reaches a protected operation.
- Missing access token is rejected.
- Malformed access token is rejected.
- Expired access token is rejected.
- Valid refresh succeeds.
- Invalid or expired refresh fails.
- Logout/revocation behaves exactly as documented.
- Revoked refresh token cannot be reused when revocation is part of your design.

### Completion gate

A test can create an account, authenticate, access a protected endpoint, refresh credentials, and exercise the documented logout behavior.

## 12. Phase 7 — Ownership and authorization foundation

### Goal

Prevent one authenticated user from reading or changing another user's data.

This is one of the most important learning goals in the project. Authentication answers “who is making the request?” Authorization answers “may that user perform this action on this object?”

### Build defense in depth

Use both of these ideas:

1. Collection/detail queries should begin from records visible to the current user.
2. Object-level permission checks should protect individual operations where appropriate.

Do not rely only on hiding records in the frontend; there is no frontend in this project, and any client can construct requests manually.

### Ownership rules

- Derive the owner from the authenticated request.
- Do not accept arbitrary owner IDs on creation.
- Make ownership read-only through the API.
- Ensure nested/related records cannot be attached across user boundaries.
- Trace ownership through every private relationship.
- Decide consistently whether another user's object produces 403 or behaves as 404.
- Ensure bulk/list/report operations apply the same owner restriction as detail operations.

### Two-user security test pattern

For every private resource, prepare User A and User B, then verify:

- A can create A's record.
- A can list A's record.
- B cannot see A's record in a list.
- B cannot retrieve A's record by guessing its identifier.
- B cannot update A's record.
- B cannot delete A's record.
- B cannot attach one of B's child records to A's parent record.
- A cannot submit B's identifier to steal or reassign ownership.

### Default access policy

- Keep the API protected by default.
- Explicitly mark registration, login, refresh, and any intentionally public exercise reads.
- Restrict exercise-catalog writes according to your catalog decision.
- Ensure documentation accurately displays which operations require JWT.

### Completion gate

All private-resource authorization is tested with at least two users before you expand the workout feature set.

## 13. Phase 8 — Workout creation and management

### Goal

Implement the core CRUD workflow for a workout containing multiple exercise entries.

### Build vertically

Implement in this order:

1. Create the smallest valid workout.
2. Retrieve that workout.
3. List the current user's workouts.
4. Add the exercise-related information required by your design.
5. Update simple workout properties.
6. Update the workout's exercise composition.
7. Add/update comments as defined in your specification.
8. Delete according to your written deletion rule.

After each step, add the relevant tests. Do not implement all serializers, views, permissions, and tests in separate large batches.

### Creation behavior

- Authenticate the caller.
- Assign ownership server-side.
- Validate every scalar field.
- Validate every referenced exercise.
- Validate the relationship between sets, repetitions, weights, and any other values you chose.
- Reject duplicates when your specification forbids them.
- Preserve item order if order is meaningful.
- Decide whether an empty workout is allowed.
- Decide whether the entire create operation must succeed or fail as one unit.
- Use a transaction when one API request writes several dependent records and partial creation would be invalid.
- Return a complete, documented representation after creation.

### Read behavior

- Scope all queries to the current user.
- Define a compact list representation and a useful detail representation if that improves clarity.
- Avoid returning secret/internal-only fields.
- Keep derived values read-only.
- Return related exercise information in a consistent shape.
- Paginate the list.

### Update behavior

- Support the update method or methods chosen in your contract.
- Make clear which fields are required for full replacement versus optional for partial update.
- Treat omitted values differently from explicitly empty/null values when the domain requires it.
- Prevent ownership changes.
- Validate the full final state, not only each submitted field in isolation.
- Make multi-record updates atomic when partial application would leave invalid data.
- Define what happens when an exercise entry is removed.
- Define how ordering changes are submitted and validated.
- Ensure editing a reusable definition does not silently corrupt historical meaning.

### Comment behavior

- Implement comments only at the level chosen in your specification.
- Set a reasonable maximum size.
- Decide whether blank comments are allowed.
- Treat comment text as untrusted input.
- Do not build threads, mentions, rich text, or moderation.

### Delete behavior

- Confirm the requester owns the target.
- Decide whether the API permanently deletes, archives, or blocks deletion when history exists.
- Make database cascading behavior match the product decision.
- Return the documented status.
- Verify reports do not become incorrect in an unexpected way.

### Query-quality pass

First make behavior correct. Then inspect database access for list and detail operations:

- Identify repeated queries for related objects.
- Use relationship-loading techniques deliberately.
- Avoid loading large unused relationships.
- Add query-count tests only for important paths where they provide learning value.
- Do not add caching to hide inefficient ORM use.

### Workout-management test checklist

- Minimal valid creation succeeds.
- Full valid creation succeeds.
- Missing required data fails.
- Invalid numeric boundaries fail.
- Invalid exercise reference fails.
- Duplicate exercise/item behavior matches the specification.
- Multi-record failure leaves no partial invalid workout.
- Owner can retrieve/list/update/delete.
- Anonymous caller is rejected.
- Second user is isolated for every method.
- Partial update preserves omitted values.
- Attempted owner change fails or is ignored according to the contract.
- Item removal/reordering behaves correctly.
- Comments respect length and blank/null rules.
- Missing workout returns the intended response.
- Delete behavior preserves or removes history exactly as designed.

### Completion gate

One authenticated user can manage a complete workout definition while a second user is fully isolated.

## 14. Phase 9 — Scheduling and status behavior

### Goal

Allow workouts to be scheduled and listed meaningfully by date/time.

### Define the state machine before coding

Write every allowed state and transition on paper. For each transition, define:

- who triggers it;
- required preconditions;
- data recorded during the transition;
- whether it can be reversed;
- effect on list results;
- effect on reports.

Do not create many statuses if time alone can derive the behavior. Also do not derive a status from time if the business meaning requires an explicit user action. Make the tradeoff yourself and document it.

### Date/time policy

- Accept timestamps in a documented ISO-compatible format.
- Require an offset or otherwise define how naive timestamps are interpreted.
- Store time-zone-aware values consistently.
- Treat UTC storage and user-local presentation as separate concerns.
- Decide what “today” means for report/date filters.
- Validate impossible or disallowed dates according to your product rules.
- Do not compare naive and aware datetime values.

### Scheduling behavior

- Allow an owner to associate a workout with the scheduled date/time concept from your design.
- Validate required relationships.
- Decide whether the same plan can be scheduled multiple times.
- Decide whether duplicate schedule entries are permitted.
- Decide whether past scheduling is permitted.
- Decide what changing a plan means for already scheduled occurrences.
- Ensure a failed scheduling operation leaves no partial records.

### Pending/active list behavior

- Define the exact inclusion rule.
- Filter by the current user.
- Sort by date/time in the documented direction.
- Define a stable secondary ordering when timestamps are equal.
- Paginate results.
- Allow only the date/status filters that support the required use cases.
- Validate filter formats and invalid ranges.

### Scheduling test checklist

- Valid scheduling succeeds.
- Missing/invalid timestamp fails.
- Offset-aware timestamp is interpreted as expected.
- Boundary around the present time follows the written rule.
- Duplicate scheduling follows the written rule.
- Past scheduling follows the written rule.
- Multiple pending items are ordered predictably.
- Equal timestamps have deterministic ordering.
- Completed/past items are included or excluded correctly.
- User isolation applies to scheduling and list filters.
- Invalid date ranges fail cleanly.

### Completion gate

Scheduling rules can be explained as a small state diagram, and automated tests prove sorting, ownership, and time-zone behavior.

## 15. Phase 10 — Completion, history, and progress data

### Goal

Record past workout activity in a form that reports can query correctly.

### Decide what “tracking progress” means in version 1

Define the minimum data a user records after performing a workout. Consider, but decide yourself:

- whether actual values may differ from planned values;
- whether completion is all-or-nothing or per exercise;
- whether skipped exercises need representation;
- whether a completion timestamp differs from the scheduled timestamp;
- whether the user can add completion notes;
- whether historical records retain snapshots of changeable definitions.

Keep the workflow small enough to complete. You do not need timers, live workout sessions, rest counters, personal records, or body measurements unless they are essential to the two or three reports you already defined.

### Completion behavior

- Permit completion only for records owned by the current user.
- Validate that the transition is allowed.
- Validate actual performance values according to the same domain rules as planned values where appropriate.
- Record completion time deliberately.
- Make the transition atomic if it writes several records.
- Decide whether completing twice is rejected or idempotent.
- Decide whether completion may be corrected later.
- Ensure completed history remains queryable even if reusable plans change.

### History behavior

- Provide a paginated way to retrieve past/completed items.
- Filter by the current user before applying date filters.
- Define default sorting.
- Define inclusive/exclusive date boundaries.
- Avoid mixing scheduled-future items into history accidentally.
- Ensure detail output represents what actually happened rather than silently showing current plan values when that would be misleading.

### History test checklist

- Allowed completion succeeds.
- Disallowed state transition fails.
- Completing another user's record fails.
- Invalid actual values fail.
- Partial write rolls back on failure.
- Repeated completion follows the defined rule.
- Completion time is recorded correctly.
- History order and pagination are deterministic.
- Date-range filters handle boundaries correctly.
- Editing a plan produces the intended historical behavior.
- Deletion behavior produces the intended historical behavior.

### Completion gate

You can create known completed-workout data whose meaning will remain stable enough to calculate reports.

## 16. Phase 11 — Reports and progress queries

### Goal

Implement a small number of correct, useful server-side reports and practice ORM aggregation.

### Limit the report scope

Choose **two or three** questions from your phase-0 specification. Do not build a general analytics engine. A valid report question must state:

- what is measured;
- over which records;
- for which user;
- over what date range;
- how results are grouped;
- how empty results behave;
- which unit the result uses.

Possible categories to think about—not completed product decisions—include frequency, volume, exercise usage, or change over time. Select only questions that your own data model can answer honestly.

### Define a report contract on paper

For each report, document:

- required and optional inputs;
- default date range, if any;
- allowed maximum range, if needed;
- grouping/granularity;
- output labels and units;
- ordering;
- treatment of deleted/changed definitions;
- treatment of missing data;
- expected result for one hand-written example dataset.

### Query implementation process

1. Create a very small known dataset.
2. Calculate the expected answer manually.
3. Write the simplest correct ORM query.
4. Compare the result with the manual answer.
5. Add ownership and date-range filtering.
6. Add grouping/annotation only as needed.
7. Inspect the SQL and query count.
8. Optimize only if the first correct query is wasteful.

### Report-safety rules

- Always begin from the current user's visible records.
- Use completed/history records rather than planned data when the report claims to measure completed performance.
- Validate start/end dates.
- Reject an inverted range.
- Define time-zone boundaries consistently.
- Avoid returning an unlimited number of data points.
- Return zero/empty output consistently.
- Never calculate totals in Python after loading an unbounded table when the database can aggregate safely.
- Do not cache reports in version 1 unless measurement proves it necessary.

### Report test checklist

- Known dataset matches the hand-calculated result.
- Empty dataset returns the documented empty shape.
- One-record dataset works.
- Date-range boundaries work.
- Invalid/inverted ranges fail.
- Another user's data never contributes to the result.
- Changed or deleted definitions follow the documented historical rule.
- Numeric precision and units are correct.
- Ordering/grouping is deterministic.
- Query count is reasonable for the chosen design.

### Completion gate

Every report has a written meaning, known-data test, ownership test, and documented response.

## 17. Phase 12 — Cross-cutting API quality pass

### Goal

Make behavior consistent across features after the main vertical slices work.

### Validation review

Review every writable field and relationship:

- required versus optional;
- blank versus null;
- minimum and maximum lengths;
- numeric minimum/maximum;
- decimal precision;
- accepted choices;
- valid timestamps;
- cross-field rules;
- cross-record rules;
- read-only values;
- ownership-derived values;
- behavior for unknown fields.

Ensure validation failures are attributed clearly enough for a client developer to fix the request.

### Error-response review

Create a small error policy covering:

- malformed JSON;
- field validation errors;
- authentication errors;
- permission errors;
- missing objects;
- method not allowed;
- unsupported media type;
- throttling;
- unexpected server errors.

You do not need a complicated custom exception framework. Consistency is the goal.

### Filtering and ordering review

- Allow only documented filter fields.
- Validate dates and ranges.
- Scope ownership before filtering.
- Allow only documented ordering fields.
- Use a deterministic default ordering.
- Prevent clients from ordering/filtering by sensitive internal fields.
- Ensure filters do not bypass “pending,” “past,” or other domain rules.

### Pagination review

- Paginate every potentially growing collection.
- Choose a modest default page size.
- Set a reasonable maximum client-selectable size if clients can select it.
- Document the response envelope.
- Test first, middle, final, empty, and out-of-range pages.
- Ensure stable ordering prevents items from appearing unpredictably between pages.

### Transaction review

Identify requests that perform multiple dependent writes. For each:

- define the invariant that must not be partially applied;
- define the transaction boundary;
- keep slow external work outside the transaction;
- catch database integrity failures at a level where the transaction is usable;
- return a safe client response rather than raw database details;
- test rollback using a deliberate failure halfway through the workflow.

Do not wrap every read-only request in a transaction merely because transactions are available.

### Performance review

For the most important endpoints:

- record approximate query counts for a small and larger fixture;
- look for one-query-per-related-record patterns;
- choose related-object loading deliberately;
- select only necessary data when reports would otherwise load large objects;
- ensure common ownership/date filters are supported by sensible indexes;
- keep response sizes bounded through pagination;
- do not add Redis or application caching without evidence.

### Throttling review

Add modest API throttling suitable for a public learning deployment:

- stricter consideration for registration and login;
- reasonable anonymous and authenticated limits;
- a documented throttled response;
- at least one test of configured behavior where practical.

Remember that application throttling is not complete denial-of-service protection and may not be perfectly race-free. It is one layer.

### Completion gate

Endpoints feel like one coherent API rather than separate exercises written on different days.

## 18. Phase 13 — Full testing strategy

### Goal

Create a focused suite that proves important behavior without testing every line mechanically.

### Testing layers

#### 1. Domain/model tests

Use these for important behavior that exists independently of HTTP:

- constraints;
- defaults;
- important methods/properties;
- allowed values;
- deletion behavior;
- state transitions when implemented below the API layer.

Do not test Django itself, such as whether a basic field stores a value.

#### 2. Validation/serializer tests

Use these where request data is transformed and cross-field rules are enforced:

- valid representations;
- required/optional fields;
- numeric and date boundaries;
- nested/related validation;
- read-only ownership;
- multi-record validation;
- clear errors.

#### 3. API integration tests

Use DRF's API testing tools to call the API as a client would:

- URL routing;
- request parsing;
- authentication;
- permissions;
- status codes;
- response bodies;
- database side effects;
- pagination, filtering, and ordering.

Most project value comes from these tests because this is an API project.

#### 4. Production smoke tests

Use a small set after deployment:

- health route;
- schema/docs availability according to your policy;
- registration/login or a safe test-account login;
- one protected read;
- database connectivity;
- HTTPS redirect;
- no debug traceback on an error.

### Test-data strategy

- Use small, readable factories/helpers or fixtures.
- Keep test ownership explicit.
- Use known timestamps rather than “now” everywhere.
- Freeze or control time where boundary behavior depends on it.
- Make report datasets small enough to verify manually.
- Avoid shared mutable test data.
- Keep tests independent and order-insensitive.

### Required test matrix

For every endpoint, include the relevant rows:

| Area | Cases to cover |
|---|---|
| Authentication | anonymous, valid token, malformed token, expired token where relevant |
| Authorization | owner, different user, privileged user if applicable |
| Input | minimum valid, typical valid, missing, wrong type, invalid range, unknown relation |
| Resource | exists, missing, deleted/archived if applicable |
| Method | expected methods and at least one disallowed method if useful |
| Output | status, structure, important values, no secret fields |
| Side effects | correct records written, no partial writes, no unintended records |
| Collection | filtering, ordering, pagination, empty results |

### Feature-specific minimums

#### Exercise catalog

- seed success and idempotency;
- read permissions;
- write restrictions;
- search/filter/pagination.

#### Authentication

- registration validation;
- password hashing;
- login success/failure;
- access and refresh behavior;
- logout/revocation behavior.

#### Workouts

- full CRUD;
- nested or related item handling;
- transaction rollback;
- two-user isolation;
- comments;
- deletion/history interaction.

#### Scheduling/history

- allowed state transitions;
- chronological sorting;
- time-zone boundary;
- date filters;
- repeated completion behavior.

#### Reports

- manually verified values;
- empty data;
- boundary dates;
- other-user exclusion;
- stable units/precision.

### Coverage policy

Use coverage as a missing-test detector, not as the purpose of testing. A reasonable learning target is good coverage of your own business and API code, but do not write meaningless assertions solely to reach a percentage. Prioritize authentication, authorization, multi-record writes, state transitions, and reports.

### Test-suite quality checks

- The suite starts from a test database.
- Tests never depend on production or development data.
- Tests can run with one documented command.
- Failure messages make the broken behavior identifiable.
- There are no random sleeps.
- External network calls are absent because version 1 needs none.
- The full suite passes twice consecutively.

### Completion gate

The suite would catch the most dangerous likely mistakes: data leakage, broken authentication, partial writes, bad state transitions, and incorrect reports.

## 19. Phase 14 — OpenAPI and developer documentation

### Goal

Make the backend usable without reading its source code.

### OpenAPI setup

- Use a maintained OpenAPI generator compatible with your DRF version.
- Expose the raw schema at a predictable route.
- Expose one interactive documentation UI.
- Define the JWT bearer authentication scheme.
- Ensure protected operations display their authentication requirement.
- Ensure request and response schemas match actual behavior.
- Resolve schema warnings rather than ignoring them blindly.

### Document every operation

For each endpoint, document:

- concise purpose;
- authentication requirement;
- permissions/ownership behavior where useful;
- path parameters;
- query parameters;
- request body;
- success response and status;
- important error statuses;
- pagination shape;
- date/time format;
- units;
- at least one safe example.

Examples must use fictional data and fake tokens. Never paste a real secret or production credential.

### Verify documentation manually

- Open the docs from a clean browser session.
- Register or use a dedicated test user.
- Authenticate in the docs UI.
- Call at least one public endpoint.
- Call at least one protected list endpoint.
- Create one valid record.
- deliberately send one invalid request and compare the documented error.
- compare generated schemas with actual JSON responses.

### README sections

Your final README should include:

1. Project purpose.
2. Scope and non-goals.
3. Main features.
4. Chosen stack.
5. Prerequisites.
6. Local setup.
7. Environment-variable reference without secret values.
8. Database migration instructions.
9. Exercise-seeding instructions.
10. How to run the server.
11. How to run tests.
12. How to generate/view API documentation.
13. Docker instructions.
14. Production/deployment overview.
15. Important design decisions and tradeoffs.
16. Known limitations.

### Additional small documents

Keep documentation useful but small:

- `docs/decisions.md`: the few major choices and why;
- `docs/deployment.md`: exact deployment and rollback steps;
- `docs/backup-restore.md`: how backup and restoration work;
- optional API client collection only if it helps you verify the API.

Do not write dozens of architectural documents for this project.

### Completion gate

A developer unfamiliar with the source can start the application and exercise the API by following the documentation.

## 20. Phase 15 — Security hardening

### Goal

Protect accounts, private workout data, secrets, and the deployed service using appropriate controls for a small production API.

### Secrets and settings

- Generate a strong, unique production secret key.
- Load secrets from production environment/secrets configuration.
- Never commit the production environment file.
- Keep debug mode disabled in production.
- Set allowed hosts to exact production hostnames.
- Configure trusted origins only when required.
- Use a separate production database credential.
- Do not expose database credentials in logs, images, screenshots, or documentation.
- Run Django's deployment checks against the production settings.

### HTTPS and proxy configuration

- Obtain a valid TLS certificate.
- Redirect HTTP to HTTPS at the reverse proxy or platform.
- Configure Django to understand the original HTTPS scheme only when behind a trusted proxy.
- Configure secure session and CSRF cookies for admin or any session-authenticated routes.
- Introduce HSTS carefully after confirming HTTPS works everywhere.
- Begin with a conservative HSTS period before considering a long duration.
- Do not enable HSTS preload for a learning project unless you fully understand the permanent operational commitment.

### Authentication security

- Use Django's password hashers and validators.
- Keep JWT access tokens short-lived enough to limit damage.
- Give refresh tokens an intentional lifetime.
- Rotate/revoke refresh tokens according to your documented design.
- Avoid putting authentication tokens in URLs.
- Do not log authorization headers or token bodies.
- Use generic login failures.
- Add basic throttling to authentication endpoints.

### Authorization and data isolation

- Use authenticated-user scoping on every private queryset.
- Enforce object permissions on detail mutations.
- Ignore/reject client-supplied ownership.
- Test nested relationships for cross-user attachment.
- Test reports for cross-user data leakage.
- Test predictable identifiers as if an attacker guesses them.
- Check admin permissions separately from API permissions.

### Input and output safety

- Validate types, ranges, lengths, choices, timestamps, and relationships.
- Limit comment/body sizes.
- Paginate lists and cap page size.
- Limit reverse-proxy request body size to something suitable for JSON-only requests.
- Return generic server errors in production.
- Never serialize password hashes, tokens, secret settings, or private internals.
- Treat comments and names as untrusted text even if this API does not render HTML.

### CORS and CSRF

- Because there is no browser frontend, do not enable permissive CORS by default.
- If you later test with a separate browser client, allow only the specific development/production origins required.
- Never use “allow every origin” with credentials.
- Understand that bearer-token APIs and session-authenticated admin pages have different CSRF behavior.
- Keep Django admin protected by normal session/CSRF mechanisms.

### Dependency and server safety

- Pin/lock dependencies.
- Check for known dependency vulnerabilities before the final deploy.
- Use maintained supported framework versions.
- Run the application container/process as a non-root user.
- Expose only the reverse proxy to the public internet.
- Keep PostgreSQL on a private/container network or managed private connection.
- Configure host firewall rules.
- Keep the server operating system and container base image patched.

### Logging privacy

Do not log:

- passwords;
- raw tokens;
- authorization headers;
- secret keys;
- database URLs with passwords;
- full environment dumps;
- unnecessary personal information.

Log enough to diagnose:

- timestamp;
- severity;
- route/method;
- status;
- request/correlation identifier if you add one simply;
- unexpected exception details in protected server logs;
- startup and migration failures.

### Security verification checklist

- Repository search finds no real secret.
- Production debug is false.
- Invalid hostnames are rejected.
- HTTP redirects to HTTPS.
- TLS certificate validates.
- Deployment checks show no unexplained serious warning.
- Anonymous requests cannot reach private data.
- User B cannot access User A's resources or reports.
- Login is throttled at the configured layer.
- Database port is not publicly exposed.
- Error responses contain no traceback.
- Logs contain no submitted passwords or tokens.

### Completion gate

You can explain the threat controlled by every enabled security setting. Remove cargo-cult settings you cannot explain, research them, then enable only when configured correctly.

## 21. Phase 16 — Production containerization

### Goal

Build one reproducible application image and a small production topology.

### Container image requirements

- Use a supported slim base suitable for your Python version.
- Pin the base image to an intentional version family.
- Install only required operating-system packages.
- Copy dependency metadata before application source to benefit from build caching.
- Install production dependencies reproducibly.
- Exclude Git data, local environments, secrets, caches, tests artifacts, and unnecessary files using a container ignore file.
- Use a multi-stage build if it materially reduces build tools/runtime size; understand each stage rather than copying a template blindly.
- Copy application files with suitable ownership.
- Create and run as a non-root application user.
- Set a clear working directory.
- Use production-safe Python environment behavior.
- Start a production WSGI/ASGI server, not Django's development server.
- Keep the startup command overrideable where useful.
- Add a health check that calls a cheap application health route.

### Dependency/build verification

- Build from a clean context.
- Confirm no local `.env` or secret exists inside the image.
- Confirm the image starts without the source directory bind-mounted.
- Confirm the installed dependency versions match the lock/pin file.
- Confirm the process runs as the intended non-root user.
- Run the test suite in a clean container or equivalent CI environment.

### Minimal service topology

For a VPS-style learning deployment, keep it to:

- reverse proxy;
- Django application;
- PostgreSQL;
- persistent database storage.

Do not add Redis, Celery, message brokers, monitoring clusters, or additional application replicas because the required feature set does not need them.

### Compose/orchestration concerns

- Give services clear names.
- Keep application and database on a private network.
- Do not publish the database port publicly.
- Persist database data outside the ephemeral container layer.
- Define database health/readiness behavior.
- Do not assume startup order alone means PostgreSQL is ready.
- Configure restart behavior.
- Pass configuration through environment/secrets rather than image layers.
- Add log limits/rotation at the host or container layer so logs cannot fill the disk.
- Keep development bind mounts out of production.
- Use explicit image tags rather than relying only on a mutable latest tag.

### Migrations and static files

- Treat migrations as an intentional release step.
- Do not allow several future replicas to race while applying migrations.
- Run migrations once before switching to the new application version.
- Collect static files needed for Django admin and API documentation.
- Serve static files through your selected production method.
- Do not ask Django's development server to serve production traffic.

### Application-server configuration

- Choose a small worker count suitable for the server's CPU and memory.
- Set sensible request/worker timeouts.
- Log access and errors to a place collected by the container/host.
- Bind only on the internal interface/network expected by the reverse proxy.
- Test graceful shutdown.
- Do not tune for thousands of users without measurements.

### Reverse-proxy configuration

- Terminate TLS or forward to the platform's TLS layer.
- Redirect HTTP to HTTPS.
- Proxy to the internal application service.
- Forward the host, real-client chain, and original scheme headers correctly.
- Trust forwarded headers only from the proxy you control.
- Apply a reasonable request-body limit.
- Apply reasonable proxy timeouts.
- Serve static assets if that is your chosen strategy.
- Return a harmless response for unknown hosts rather than proxying them to Django.

### Health-check design

Use at least two concepts if practical:

- **Liveness:** the web process can respond.
- **Readiness:** the application can perform essential work such as reaching the database.

Keep checks cheap. Do not mutate data or call outside services. Decide whether readiness is public or internal and avoid exposing system details.

### Completion gate

A clean machine can build the image and start the small stack using documented environment values, and the API works without development conveniences.

## 22. Phase 17 — Deploy one production environment

### Goal

Operate the API on one real HTTPS URL and learn the complete release lifecycle.

### Choose one deployment route

Choose either:

1. a small VPS running your containers and reverse proxy; or
2. a PaaS that supplies equivalent production application, managed PostgreSQL, secrets, logs, TLS, and health checks.

Do not deploy the same learning project to several providers. If you choose a PaaS, learn what it manages for you instead of pretending Nginx/Docker details are identical. If your learning goal includes Nginx and host administration, choose the VPS route.

### Server/account preparation

- Use a maintained Linux release.
- Create a non-root administration/deployment user.
- Use SSH keys.
- Disable unsafe password/root login when you understand and have verified access.
- Apply operating-system updates.
- Configure a basic firewall.
- Expose only SSH and web ports that are actually needed.
- Set the server time correctly.
- Install the container/runtime tools from trusted sources.
- Create a clear application directory owned by the correct user.

### DNS and TLS

- Point a domain/subdomain to the server.
- Wait for DNS resolution.
- Configure the exact hostname in the reverse proxy and Django settings.
- Obtain a trusted certificate.
- Verify automatic certificate renewal.
- Test both HTTP redirect and direct HTTPS.
- Verify the application generates correct absolute URLs/scheme when behind the proxy.

### Production configuration inventory

Prepare every required environment value before launch. Include categories such as:

- Django secret;
- production/debug mode;
- allowed host/origin values;
- database connection values;
- token/security values that differ from defaults;
- logging level;
- application server configuration if environment-driven.

Store values in the host/platform's protected configuration mechanism. Keep a list of variable names in documentation, but never store the real secret values in the repository.

### Database setup

- Create the production database/service.
- Use a dedicated application database user.
- Give only the privileges the application needs.
- Keep the database off the public internet where practical.
- Use persistent storage.
- Define a backup destination outside the live database volume/server when possible.
- Confirm time zone/encoding settings are appropriate.

### First deployment sequence

Use an explicit sequence:

1. Confirm the production configuration exists.
2. Build or pull the exact application image version.
3. Start/check PostgreSQL.
4. Confirm database readiness.
5. Run migrations once.
6. Seed the exercise catalog once using the repeatable command.
7. Collect static files if required by your approach.
8. Start/restart the application service.
9. Start/reload the reverse proxy.
10. Check application and proxy logs.
11. Run Django's production deployment checks.
12. Call health/readiness over HTTPS.
13. Run the manual production smoke journey.

If administration requires a superuser, create it through a one-time secure operation. Do not hardcode its password in an image, compose file, or repository.

### Manual production smoke journey

Use fake test data and verify:

- HTTP redirects to HTTPS.
- Health check returns the intended result.
- OpenAPI schema/docs are reachable according to your policy.
- Registration works.
- Login returns the expected tokens.
- JWT authorizes a protected request.
- Exercise data exists.
- A workout can be created and retrieved.
- A workout can be scheduled.
- The pending list is ordered.
- Completion/history works.
- A report returns the known test data.
- A second account cannot access the first account's objects.
- Invalid input returns 4xx without a traceback.
- Logs show the request but not its password/token.

Remove or clearly label disposable smoke-test data afterward.

### Logging and error visibility

- Ensure application stdout/stderr is collected.
- Ensure reverse-proxy access/error logs are available.
- Configure log rotation/size limits.
- Use production log severity intentionally.
- Confirm a deliberate harmless 404 appears where expected.
- Confirm an unexpected exception can be diagnosed privately without exposing details to the client.
- Optional: add one simple hosted error tracker only after core deployment works; it is not required to finish.

### Backup and restore

A backup that has never been restored is only a hope. For this learning project:

- choose a simple PostgreSQL backup method;
- schedule it at least daily if the deployment remains online;
- store more than one recent backup;
- keep a copy outside the live database volume;
- document the command/process;
- create a disposable database;
- restore a backup into it;
- verify key tables/record counts and a basic API query;
- record the date of the restore test.

You do not need enterprise point-in-time recovery, but you do need to understand how your data survives a container or server failure.

### Deployment update runbook

Document this small repeatable process:

1. Confirm tests pass.
2. Tag/identify the release commit and image.
3. Take/confirm a recent database backup before risky migrations.
4. Build/pull the new immutable image tag.
5. Review migrations.
6. Put the service into a safe update state if needed.
7. Apply migrations once.
8. Restart with the new image.
9. Run health and smoke tests.
10. Inspect logs.
11. Record the deployed version.

For a single learning server, a short maintenance window is acceptable. You do not need multiple servers or zero downtime.

### Rollback runbook

Before the first update, write what you will do if it fails:

- identify and start the previous image version;
- understand whether the new migration is backward-compatible;
- avoid blindly reversing a destructive migration;
- restore from backup only when required and after understanding data loss;
- verify health and the critical user journey after rollback.

Practice at least an application-image rollback with a harmless change. Do not deliberately destroy production data to practice.

### Completion gate

The deployed API survives a process restart, retains database data, uses HTTPS, produces useful logs, and has a tested backup/restore procedure.

## 23. Phase 18 — Minimal continuous integration

### Goal

Make every pushed change prove that it can install and pass core checks in a clean environment.

### CI workflow

On pushes and pull requests, run:

1. Checkout.
2. Set up the supported Python version.
3. Install pinned dependencies.
4. Start/provide a PostgreSQL test service.
5. Supply safe test-only environment values.
6. Check code formatting/linting using the tools you selected.
7. Check that model changes have migrations where appropriate.
8. Run framework/system checks.
9. Run the full test suite.
10. Generate/validate the OpenAPI schema if your tooling supports a useful failure check.
11. Optionally build the production image to catch Docker build failures.

### CI rules

- Never put production secrets in CI.
- Do not connect CI tests to the production database.
- Keep the workflow readable.
- Pin major action/tool versions deliberately.
- Treat a failing test/check as a failed build.
- Avoid a large matrix of operating systems and Python versions; test the version you actually support.
- Do not implement automatic production deployment until you are comfortable deploying manually.

### Completion gate

A clean CI run gives confidence that the repository is installable, migrations are present, tests pass, and the production image can build.

## 24. Phase 19 — Final end-to-end quality assurance

### Goal

Verify the entire project as a user, attacker, developer, and operator.

### Fresh-install rehearsal

Use a clean database and clean environment, then follow only the README:

- install dependencies;
- configure environment;
- migrate;
- seed exercises;
- run tests;
- start the application;
- open schema/docs;
- complete the critical user journey.

Write down every missing instruction and fix the documentation.

### Critical user journey

Complete this using only HTTP/API tools, not Django admin or shell shortcuts:

1. Register User A.
2. Log in User A.
3. Refresh authentication.
4. Browse/filter exercise data.
5. Create a complete workout.
6. Retrieve and list it.
7. Update it and its comment.
8. Schedule it.
9. Confirm it appears in the correctly ordered pending list.
10. Record completion/history data.
11. Confirm it leaves/changes lists according to your state rules.
12. Retrieve history.
13. Request each required report and compare with expected values.
14. Exercise the documented logout/revocation behavior.

### Adversarial journey

1. Register User B.
2. Guess/use User A's identifiers.
3. Try every read, update, delete, nested attachment, completion, and report path relevant to User A.
4. Submit ownership fields manually.
5. Submit invalid related IDs.
6. Submit negative, zero, huge, blank, null, wrong-type, and overly long values where relevant.
7. Submit invalid timestamps and inverted ranges.
8. Submit malformed/missing/expired tokens.
9. Request very large pages.
10. Try disallowed HTTP methods.

The expected result is safe 4xx handling with no leaked private data and no 500 errors for ordinary bad input.

### Operator journey

- Restart application service; data remains.
- Restart database/container safely; data remains.
- Re-run seeding; data remains correct.
- View logs.
- Identify running release version.
- Run deployment checks.
- Create a database backup.
- Restore it to a disposable database.
- Deploy a harmless new image version.
- Roll back to the prior image version.

### Final cleanup

- Remove dead code and commented-out experiments.
- Remove temporary debug prints.
- Remove unused dependencies.
- Remove unused settings and environment keys.
- Verify migrations are committed.
- Verify seed data is committed.
- Verify no generated secret or local environment file is committed.
- Run formatter/linter.
- Run all tests twice.
- Build the production image once more.
- Run production deployment checks.
- Update known limitations honestly.
- Create a final tagged release.

### Completion gate

Every item in the original definition of done is checked, the final test suite is green, and the deployed critical journey succeeds.

## 25. Suggested 12-day schedule

This schedule assumes roughly three focused hours per day. Move unfinished essential work forward; do not cut tests or authorization to protect the calendar.

### Day 1 — Requirements and foundation

- Rewrite the brief.
- Set version-1 non-goals.
- Resolve domain vocabulary.
- Write acceptance scenarios.
- Create repository/environment.
- Connect local PostgreSQL.
- Make the first clean commit.

**End-of-day output:** running project skeleton plus written scope.

### Day 2 — Your data and API design

- Draw your ER diagram.
- Decide ownership, lifecycle, deletion, units, timestamps, and constraints.
- List frequent queries and possible indexes.
- Fill the endpoint-planning table.
- Map every requirement to an operation and test idea.
- Create/read/apply the initial migrations.

**End-of-day output:** your own reviewed schema and API contract; no copied solution.

### Day 3 — Exercise catalog and seeder

- Prepare modest seed data.
- Build repeatable seeding.
- Test first and repeated seed runs.
- Add exercise read/list behavior.
- Add access restrictions, filters, and pagination.
- Document the seed process.

**End-of-day output:** reliable reference catalog.

### Day 4 — Authentication and permissions

- Implement registration.
- Implement JWT login and refresh.
- Implement the defined logout/revocation behavior.
- Configure protected-by-default API access.
- Build reusable ownership policy.
- Write authentication and two-user security tests.

**End-of-day output:** complete authentication lifecycle and verified isolation foundation.

### Day 5 — Core workout CRUD

- Create a workout with related exercise information.
- Make compound writes atomic if required.
- Implement retrieve/list.
- Implement updates/comments.
- Implement deletion rule.
- Add validation and ownership tests as each action is built.

**End-of-day output:** owner-only workout CRUD.

### Day 6 — Scheduling and history

- Write the state-transition rules.
- Implement scheduling.
- Implement pending/active sorted list.
- Implement completion/history behavior.
- Test time zones, boundaries, sorting, transitions, and second-user access.

**End-of-day output:** complete workout lifecycle.

### Day 7 — Reports and query quality

- Build small known report datasets.
- Implement only the selected reports.
- Verify calculations manually.
- Test empty/range/ownership cases.
- Inspect SQL/query counts.
- Fix obvious N+1 queries and add justified indexes.

**End-of-day output:** correct reports and reasonable ORM behavior.

### Day 8 — API consistency and full tests

- Review all validation.
- Review errors/status codes.
- Finish filtering, ordering, pagination.
- Add throttling.
- Fill missing endpoint matrix tests.
- Run coverage to identify meaningful gaps.

**End-of-day output:** coherent API and strong risk-focused test suite.

### Day 9 — OpenAPI and README

- Finish schema configuration.
- Document authentication, operations, errors, filters, units, and examples.
- Exercise operations from interactive docs.
- Write local setup, migration, seed, and test instructions.
- Record decisions and limitations.

**End-of-day output:** usable developer documentation.

### Day 10 — Security and containers

- Complete production settings.
- Run deployment/security checks.
- Review tokens, CORS, CSRF, allowed hosts, proxy/HTTPS settings, and logs.
- Build non-root production image.
- Start the minimal production stack locally.
- Test migrations, static assets, health, and API in containers.

**End-of-day output:** production-style local stack.

### Day 11 — Deploy and operate

- Provision one environment.
- Set DNS/TLS and secrets.
- Create database/storage.
- Migrate, seed, and launch.
- Run production smoke and adversarial checks.
- Configure logs and backup.
- Perform a test restore into a disposable database.

**End-of-day output:** live HTTPS backend with recoverable data.

### Day 12 — CI, clean install, and finish

- Add minimal CI.
- Rehearse setup from scratch using README.
- Run full user/adversarial/operator journeys.
- Fix only blocking defects.
- Remove debug/dead code.
- Run all checks.
- Tag the final release.
- Write a short retrospective.

**End-of-day output:** finished learning project.

### Buffer rule

If you need two extra days, use them only for:

- a required feature that does not work;
- security/ownership failures;
- incorrect reports;
- broken deployment;
- missing critical tests/documentation.

Do not use buffer days for new features.

## 26. Backlog structure

Create issues/tasks in this order. Each should be small enough to complete and verify in one focused block:

1. Write scope, terms, non-goals, and definition of done.
2. Write acceptance scenarios.
3. Set up project, PostgreSQL, environment configuration, and tests.
4. Create your ER diagram and integrity rules.
5. Create your API contract.
6. Add initial migrations and admin inspection.
7. Build exercise seed data/import.
8. Build exercise read/search/filter/pagination.
9. Build registration.
10. Build login/refresh/logout behavior.
11. Establish owner-only query and object rules.
12. Build minimal workout creation/retrieval.
13. Build full workout item management.
14. Build workout updates/comments/deletion.
15. Build scheduling and sorted pending list.
16. Build completion/history.
17. Build report 1.
18. Build report 2.
19. Optionally build report 3 only if time remains.
20. Complete validation/error/pagination/throttling review.
21. Complete authorization and transaction tests.
22. Complete OpenAPI/README.
23. Complete production security settings.
24. Build/test containers.
25. Deploy over HTTPS.
26. Configure/test backup restore.
27. Add CI.
28. Run final QA and tag release.

## 27. Feature completion template

For each backlog task, do not mark it done until you can fill this in:

- **Behavior:** What does the user/client gain?
- **Contract:** What request and response are promised?
- **Ownership:** Who may do it, and on whose data?
- **Validation:** What input is rejected?
- **Atomicity:** Could it leave partial data?
- **Queries:** Is the query bounded and reasonably efficient?
- **Tests:** Which success, failure, and security cases pass?
- **Documentation:** Can a client discover and use it?
- **Commit:** Is the repository left in a working state?

## 28. Git checkpoint plan

Commit working milestones, not every keystroke and not one giant final commit. Good checkpoint topics include:

- project foundation;
- domain migrations;
- exercise seeder/catalog;
- authentication lifecycle;
- ownership permissions;
- workout creation/read;
- workout update/delete;
- scheduling/history;
- each report;
- testing hardening;
- API docs;
- production settings;
- containerization;
- CI/deployment documentation.

Before each commit:

- review the diff;
- remove secrets/debug output;
- run the relevant focused tests;
- use a message explaining the behavior added or fixed.

Before merging/tagging the final state, run the entire suite.

## 29. When to consult documentation

You are expected to use documentation during the project. Look up concepts when you reach them rather than trying to memorize every keyword.

Useful official references:

- [Workout Tracker brief](https://roadmap.sh/projects/fitness-workout-tracker)
- [Django documentation](https://docs.djangoproject.com/)
- [Django deployment checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [Django REST Framework API guide](https://www.django-rest-framework.org/api-guide/)
- [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [DRF testing](https://www.django-rest-framework.org/api-guide/testing/)
- [DRF API documentation guidance](https://www.django-rest-framework.org/topics/documenting-your-api/)
- [Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- PostgreSQL documentation for the specific supported version you install.
- Documentation for your chosen OpenAPI package, application server, reverse proxy, container runtime, and hosting platform.

When reading a tutorial, compare it with current official documentation. Copying syntax without understanding ownership, transactions, settings, and failure behavior defeats the purpose of this project.

## 30. Stop conditions: when the project is truly finished

Stop adding features when:

- all required roadmap behavior works;
- two-user isolation has been proven;
- invalid input is handled safely;
- reports match known data;
- tests pass;
- docs describe the real API;
- a clean install works;
- the production URL uses HTTPS;
- production settings and server are appropriate;
- logs, health checks, and backup/restore work;
- the final end-to-end journey passes.

At that point, write a short retrospective:

- What did you understand better after building it?
- What bug took the longest and why?
- Which design decision would you change?
- Which security test caught a real mistake?
- Which ORM query did you improve?
- What will you practice in the next project?

Then move on. Finishing and reflecting will teach you more than endlessly polishing this small backend.

