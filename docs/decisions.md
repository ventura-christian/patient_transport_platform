# DECISIONS

> Last Updated: July 4, 2026

---

**This file tracks the decisions I made while designing Vectris and why I made them.**

## Column Naming Convention

I originally named variables things like `current_location_of_patient` and `patient_destination_for_current_task`. These are too verbose for database column names and I realized that they read more like sentences and less like variables. I renamed everything to standard snake_case following Python and PostgreSQL conventions.

Examples:

- `current_location_of_patient` → `origin_department`
- `patient_destination_for_current_task` → `destination_department`
- `current_patient_biohazard_status` → `biohazard`
- `time_request_task_generated` → `created_at`

Short, readable names are easier to query and easier to understand in code. If a name needs more explanation, that belongs in documentation and not in the column name itself.

---

## Destination Field: Single Department Field

I considered three options for storing where the patient is going:

1. A single combined text string like `"ICU - Room 204"`
2. Two fields: `destination_department` + `destination_room`
3. One field: `destination_department` only

I went with option 3. The transporter's job is to deliver the patient to a department. The staff at that department handle the patient from there. The dispatcher doesn't need extra details but simply where to send them. Adding a room field would be extra complexity that the MVP (minimum viable product) workflow doesn't require.

---

## Origin Fields: Split Into Department and Room

For the pickup side I went the opposite direction. Origin uses two fields: `origin_department` and `origin_room`.

The transporter physically has to find the patient to pick them up. A department name alone (`"ICU"`) isn't enough — they need the room. Having two clean separate fields is better than one combined string because you don't have to parse or split anything if the system ever needs to use those values separately.

---

## total_time Is Not Stored

I originally planned to store `total_time` as a column that would be calculated when a request is completed. I decided against it.

`total_time` can always be derived from `completed_at - created_at`. Both of those values are already in the database. If I stored `total_time` separately and `completed_at` ever got corrected, the stored total time would be wrong. Storing a value that can be calculated from other values in the same row creates two sources of truth, which is a risk. The calculation happens at query time instead.

---

## Assignment Data Lives in request_assignment, Not transport_requests

Early on I had `transporter_id` as a column on the `transport_requests` table. I moved it to its own junction table.

The reason is that some jobs require more than one transporter. A single `transporter_id` column can only hold one value. If you need to assign two transporters to a request there's no clean way to do that with a single column. The junction table solves this — each row in `request_assignment` is one assignment, so a request needing two transporters just has two rows.

---

## equipment_needed Is Nullable

Not every transport requires equipment. A patient who can walk just needs staff guidance. If I made this field required I'd have to store a placeholder value like `"none"` for every unequipped transport, which isn't meaningful data. Null correctly represents "no equipment needed for this request."

---

## Status Values Are Enforced by the Application, Not the Database

Both `transport_requests` and `transporters` have status fields stored as VARCHAR strings. The valid values are defined and enforced in the application code (service layer), not as a database-level ENUM.

Using PostgreSQL ENUMs would require a database migration every time a status value needs to change. For an MVP where things might still shift, a VARCHAR with application-level validation is faster to work with. The tradeoff is that the database itself won't reject an invalid string — the application has to catch that.

---

## Three Tables Only — No Locations Table, No Audit Log

I considered adding a `locations` table so department names would be validated foreign keys instead of free text. I also considered a `dispatch_events` table for logging state changes.

I decided against both for MVP. A locations table would mean I have to build and populate a list of all hospital departments before any requests can be created. That's extra infrastructure before the core workflows even exist. Free-text is good enough for the scope and user base of this project. Same reasoning for the audit log, it's useful but not required for the three workflows to function.

Both are reasonable things to add in a future version.

## Dashboard Visualization Technology Determination

I had several options for displaying my dashboard. For simplicity and clarity's sake, I went with Jinja2 as it has a native library built into Python and allows me to keep my project in a monolithic structure.

### Frontend: Jinja2 Server-Side Templates

What it is?

- FastAPI renders HTML on the server using Python data and sends complete pages to the browser.

Benefits

- Native FastAPI support, no extra tooling
- Everything lives in one Python codebase which follows the monolithic architecture
- No JavaScript build pipeline
- Browser receives complete HTML ,nothing to "fetch" after load
- Easier to understand for a backend focused learner
- It's fast to prototype

Tradeoffs

- Page refreshes to update data (no live updates without JavaScript)
- Less interactive than a JS driven frontend
- Tightly coupled to the backend which allows the frontend and backend to live together

Why it fits my project

- The dispatcher dashboard is a read heavy operational view. It doesn't need real-time reactivity or complex client side state. A full page refresh when assigning a transporter is acceptable. Jinja2 keeps the entire system in one place, which aligns with the monolithic architecture decision for my project.

---

These were the options I considered:

### Plain HTML/JS as Static Files

What it is?

- FastAPI serves an index.html file. JavaScript in the browser calls your REST API endpoint and renders the results dynamically.

Benefits

- Clean separation between frontend and backend
- Frontend can be built and tested independently
- More "modern" architecture pattern

Tradeoffs

- Requires JavaScript knowledge to fetch and render data
- Two layers to debug (frontend JS + backend API)
- More moving parts for my minimum viable product
- Still requires understanding REST (representational state transfer) API (application program interface) design before building anything visible

Why this stack didn't fit my project

- The added complexity of managing client-side JavaScript data fetching is not justified for a dashboard that three users will interact with. It also delays having anything visible until the API if fully functional.

---

### JavaScript Framework (React, Vue, Angular)

What it is?

- A dedicated frontend application, written in JavaScript, that communicates with your backend via API and gets deployed separately.

Benefits

- Industry standard for production web applications
- Highly interactive, no page refreshes
- Strong ecosystem and job market relevance

Tradeoffs

- Requires Node.js, npm, a build pipeline
- Separate deployment from the backend (breaks the monolithic architecture design choice I made)
- Steep learning curve on top of an already full backend build
- Complete overkill for a 3 workflow dispatcher dashboard

Why this stack didn't fit my project

- The scope of this stack would require learning an entirely separate ecosystem and I wanted to make an application with Python. The monolithic architecture decision ruled it out completely and a JavaScript framework implies a separate frontend application, which is the opposite of a monolith.

## requirements.txt Content

Why each entry?

- fastapi: This is the web framework. Handles routing, validation, and serving your API and HTML pages.
- uvicorn: This is the server that will run FastAPI. Uvicorn listens for incoming HTTP requests and hands them to FastAPI.
- sqlalchemy: This is the object relation mapper. It lets me write Python classes instead of raw SQL.
- alembic: This is the migration tool. It tracks and applies changes to my database schema.
- psycopg2-binary: This is the driver that lets Python talk to PostgreSQL. SQLAlchemy knows how to generate SQL, but it needs this library to actually send it to a PostgreSQL database. The "-binary" version includes everything pre-compiled so I don't need extra system dependencies.
- pydantic: This is the data validation. FastAPI uses this to validate incoming request data.
- python-dotenv: This reads the .env file and loads its values into the environment. This will allow Vectris to read the database URL without it being hardcoded.
- jinja2: This is the templating engine for the frontend.

## Why I chose to use SQLAlchemy vs Raw SQL: the tradeoff

- I will use SQLAlchemy to generate the SQL to inject into my queries and this allows my queries to use the Base class and inherit all of the information contained within that pattern.
- I can then run a simple SQLAlchemy script that will generate all the necessary information when adding things into my tables.
- For most situations, this may not be the preferred method for debugging purposes (I won't be able to explicitly see  where bugs might originate from because I didn't write the raw SQL). But for my project and the simple queries, this makes the process seamless and simple to use.
- The ORM (object relational mapping) version is less error prone that writing raw SQL.

## Dependency Injection: Why should I care?

- This pattern allows database sessions to be provided to my application without the developer having to hardcode them for every request.
- The information is provided to the developer and removes friction from having to manage all that data each time.
- Every API endpoint that touches the database needs a database session which is the connection to PostgreSQL that it uses to run queries. The dependency injection handles this for me and removes the friction I explained in the previous two sentences.

## Alembic Configuration — Models Imported in env.py

To enable autogenerate, all three SQLAlchemy models are explicitly imported in
migrations/env.py and target_metadata is set to Base.metadata. Without these
imports the models are never registered and Alembic generates an empty migration.

---

## Dashboard Mockup Checked Against Existing Decisions

I built a wireframe for the dashboard before locking in the schema decisions, so a few things in it didn't match what I'd already decided.

The wireframe had a priority field on the create-request form and on the assignment screen. I'd already decided against priority scoring when I chose time-in-queue as the ordering signal, so I dropped the field. The queue sorts oldest request first, and that's the only priority signal Vectris has.

The wireframe also showed a department dropdown, but my department fields are plain free text because I didn't want to build a locations table before a single request could get created. I kept the free text decision and added a hardcoded list of about eight department names inside the template, so the dropdown works without touching the database. The column stays a plain VARCHAR with no foreign key.

The wireframe's job detail screen showed a status history timeline listing every stage a request passed through. I don't store that anywhere. I ruled out an audit log table for the same reason earlier in this file, so I dropped the timeline and left the job detail screen showing only the current status.

Three fields were just missing from the wireframe that the schema already requires: origin room, transporters required, and biohazard. I added all three back into the create-request form.

---

## Transporter Status Resets When a Request Completes

Nothing in my code returned a transporter to available once their request was marked complete. Once assigned, a transporter stayed on_job until a dispatcher reset them by hand through the transporter endpoint.

I considered leaving that manual, where the dispatcher confirms someone's back and flips their status themselves. I chose automatic instead. Completing a request now looks up who was assigned to it and sets their status back to available in the same action. A dispatcher already tracks enough without remembering a second step for every finished job.

The tradeoff: a dispatcher can't hold someone back right after a job, say if they need a break immediately. That takes a second manual update through the transporter endpoint for now. Good enough for three users and an MVP.

---

## Delayed Requests Are Derived From Time in Queue

The dashboard needs a panel showing requests that need attention, but nothing in my schema flags a request as delayed.

I considered a stored column for this, something like is_delayed or flagged, set manually or by a background check. Instead I derive it the same way I derive priority: a request counts as delayed once it's been active past a fixed time threshold, calculated from created_at. No new column, no new place for the data to drift out of sync.

The limitation is that this only measures how long something's been waiting, not why. A request stuck because equipment isn't available looks identical to one stuck because nobody's picked it up yet. A stored reason field would fix that, but it's not something the three MVP workflows need.

## Frontend Routes Live in app/web/, Not app/api/

repository_map.md already defines app/api/ as the JSON REST layer. Rather than mixing HTML-rendering routes into it, I created a parallel app/web/ package that follows the exact same pattern: a router, calling the service layer directly, no business logic in the route itself. The only difference is what it returns. app/api/ routes return a response_model. app/web/ routes return a rendered Jinja2 template or a redirect.

---

## HTML Forms Use FastAPI's Form(), Not the Pydantic Request Body

My API routes take a Pydantic model as the request body, because Swagger and any JSON client send JSON. A browser `<form>` doesn't send JSON. It sends application/x-www-form-urlencoded data, and FastAPI reads that through individual Form() parameters instead, which requires the python-multipart package.

Two form quirks came out of this. An unchecked checkbox sends nothing at all, not "false" — the biohazard field relies on that absence to default to False, and I set the checkbox's value to "true" so a checked box sends something FastAPI can convert to a real boolean. An unselected dropdown sends an empty string, not null. The create-request route converts that empty string to None by hand before building the TransportRequestCreate schema, since the database column expects null for "no equipment," not an empty string.

---

## Every Form Submission Redirects With a 303, Not a Direct Render

After a successful POST on the create-request, assign, or complete-request routes, the handler returns a redirect to /dashboard with a 303 status instead of rendering a page directly. A 303 specifically tells the browser to re-fetch the next page with GET. Without it, refreshing the confirmation page would resubmit the same form and create a duplicate transport request or assignment.

---

## Web Routes Catch Service-Layer Errors Instead of Crashing

My API layer already turns a service-layer ValueError into a clean 400 response. The web layer needed the same protection for a human instead of a client library: the assign and complete-request POST handlers wrap the service call in try/except ValueError and re-render the same screen with the error shown inline, rather than letting FastAPI return its default unhandled-exception page. Given how much a demo depends on nothing crashing in front of faculty, the extra few lines on every form-submitting route were worth it.

---

## Multiple Transporters Per Request: Fixing assignment_service.py

**Problem:** transporters_required already existed as a schema field, but create_assignment rejected any request that wasn't status active, and the very first assignment flipped status to in_progress. A request needing 2 or more transporters could only ever receive one — the field was stored but never enforced.

**Alternatives Considered:** Leave it alone and document it as a known limitation, since the default is 1 transporter and none of the three MVP workflows strictly require more. Or fix the underlying logic properly.

**Chosen Approach:** Fixed it. create_assignment now accepts a request that's active or already in_progress, and rejects a new assignment once the request already has enough transporters. update_status adds a guard before allowing the in_progress → complete transition: the assignment count has to meet transporters_required, or the transition gets rejected with a message naming exactly how many are still needed.

**Advantages:** transporters_required is a real constraint now, not just a display field. A dispatcher can't close out an understaffed job by mistake.

**Disadvantages / Tradeoffs:** Touches five files across the service and web layers instead of staying contained to one. The dashboard now runs one query per in-progress request to know whether it still needs staff, a loop rather than a single join.

**Risks:** Low. The change is additive to logic already exercised by the default single-transporter case, and that case got retested after the change.

**Future Improvements:** Collapse the per-row assignment-count query in the dashboard route into a single join if the request queue ever grows large enough to matter.

**One-Sentence Defense:** The schema already promised multi-transporter support, so I closed the gap between what the data model allowed and what the business logic actually enforced.

---

## Computed Display Values Get Attached to the Object, Not Given Their Own Service Function

The dashboard needs to know, for each in-progress request, whether it still needs more staff. Instead of writing a new service function to answer one boolean question, the dashboard route attaches it directly to the already-fetched SQLAlchemy object as a plain attribute — req.needs_more_staff — right before passing it to the template. Nothing about this touches the database. It only exists for the life of that one request. Fine for a single screen. If a second screen needed the same value, that's the point where it should become a real service function instead of a copy-pasted loop.

## Deploying to Render Instead of GitHub Pages or Staying Local-Only

**Problem:** A README with setup instructions asks a grader to install Python, PostgreSQL, and run six commands correctly before seeing anything. I wanted a link that just works.

**Alternatives Considered:** GitHub Pages (ruled out immediately because it only serves static files, it can't run a Python process or connect to a database, this isn't a difficulty question, it's a category mismatch). GitHub Codespaces (technically possible, but still requires a GitHub account and manual setup steps, not meaningfully simpler than the README path). Staying local-only and doing a live demo in person.

**Chosen Approach:** Deployed to Render because it's a free web service running the FastAPI app plus a free managed Postgres database, connected through an environment variable.

**Advantages:** A single URL that works from any device, no install required. Doubles as the live demo and the fallback if an in-person demo has technical issues.

**Disadvantages:** Free-tier web services spin down after 15 minutes idle (roughly a minute to wake back up on the next visit). Free Postgres expires 30 days after creation.

**Tradeoffs:** Traded some polish (the cold-start delay) for something no local setup could offer: a link that works for anyone, on any machine, with zero configuration.

**Risks:** Low for submission timing — the 30-day database window comfortably covers the deadline. Longer-term, the live link isn't permanent without upgrading the database to a paid instance.

**Future Improvements:** A custom domain, or moving to a paid instance if the project needs to stay live past 30 days.

**One-Sentence Defense:** A link a grader can open on their phone is worth more than a perfectly documented local setup nobody has to actually use.

---

## seed.py for Reproducible Demo Data

**Problem:** A freshly deployed database has empty tables. Cloning the repo copies code and schema migrations, not rows — the dashboard would load with nothing in it, which looks broken even though every workflow underneath works.

**Alternatives Considered:** A SQL dump of my local database (fragile, versions have to match, more manual steps). Manually creating sample data through Swagger every time (not repeatable, easy to forget).

**Chosen Approach:** A small script that inserts a fixed set of sample transporters and transport requests, checking row counts first so it's safe to run more than once.

**Advantages:** One command gets any fresh database (local or deployed) into a usable demo state. Doesn't touch the application code or add any new endpoint.

**Disadvantages:** Not a real feature. If someone actually assigns and completes the seeded requests (which is expected, normal use of the app), the sample requests disappear from the active queue, since completed requests are correctly filtered out of the dashboard view.

**Tradeoffs:** Chose a one-time idempotent script over an automatic per-visit reset. An automatic reset would mean nothing anyone does through the real assign/complete workflow actually persists, which undermines the entire point of demonstrating a working, stateful system.

**Risks:** Low. It only inserts rows, and only when tables are empty.

**Future Improvements:** A manual reset command that clears and re-seeds on demand, for restoring a clean demo state before a specific presentation.

**One-Sentence Defense:** A database with no data doesn't prove the app works, rather a database with realistic sample data does.

---

## Alembic env.py Wasn't Reading DATABASE_URL From the Environment

**Problem:** The Render deploy failed during `alembic upgrade head` with "connection to server at localhost... Connection refused," despite DATABASE_URL being set correctly in Render's environment.

**Root Cause:** `migrations/env.py` built its database connection entirely from `alembic.ini`'s `sqlalchemy.url` line, hardcoded to `postgresql://localhost/vectris`. It never read the environment at all. This worked locally purely by coincidence because my own machine happens to run Postgres at localhost too, so the hardcoded value and the real one were identical, and the bug never had a chance to show up.

**Alternatives Considered:** Editing alembic.ini directly per environment (fragile, means a different ini file per machine, works against the entire point of environment variables).

**Chosen Approach:** Added three lines to env.py that read `DATABASE_URL` from the environment and override whatever alembic.ini has, before the migration engine gets built.

**Advantages:** Migrations now always target the same database the running app connects to, on any machine.

**Disadvantages:** There aren't any at this time, this is a bug fix, not a new capability.

**Risks:** None. The override only applies when DATABASE_URL is actually set; without it, the old ini-based behavior is unchanged.

**Future Improvements:** None needed.

**One-Sentence Defense:** A migration tool that ignores your environment variables will always look correct on your own machine and fail everywhere else.

---

## Dashboard Visual Redesign

**Problem:** The original dashboard was plain HTML tables with no styling. Functional, but it didn't demonstrate any layout or design work, which are graded separately from backend logic.

**Alternatives Considered:** A CSS framework like Bootstrap or Tailwind (rejected because it would add a dependency and a build step that doesn't fit the no-build-pipeline decision already made for the frontend). Leaving it unstyled and relying entirely on the backend work to carry the grade.

**Chosen Approach:** A single hand-written CSS file using CSS custom properties for color and typography, applied consistently across all four screens: a dark background, a five-color palette mapped to specific meanings (myrtle green for available/positive states, auburn for requests waiting in the queue, scarlet reserved for biohazard flags only), and three typefaces split by role (a display font for the wordmark only, a heading font for labels, a monospace body font for everything else).

**Advantages:** Consistent look across every screen, no new dependencies, still just Jinja2 templates and one CSS file with no build step added.

**Disadvantages:** More CSS to maintain by hand than a framework would require.

**Tradeoffs:** Chose hand-written CSS and a bit more manual work over a framework, to keep the "no build pipeline" decision intact.

**Risks:** Low. Pure presentation layer, no route or service logic touched.

**Future Improvements:** A dark/light mode toggle, though not needed for the MVP.

**One-Sentence Defense:** The three MVP workflows already worked and this made them look like they were built on purpose.
