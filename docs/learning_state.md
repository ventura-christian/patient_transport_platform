# LEARNING STATE

> Last Updated: July 4, 2026

Understood:

- Project scoping and MVP thinking
- Systems analysis and workflow-first design
- Layered architecture fundamentals
- Relational schema design — tables, columns, types, constraints
- Primary keys and foreign keys
- Junction tables and why they exist
- Derived values vs stored values
- Column naming conventions
- Nullable vs required fields
- Status lifecycle modeling
- Why business logic belongs in the service layer
- Monolithic vs microservices architecture and why monolith fits Vectris
- Separation of concerns and the four system layers
- The dependency direction rule (layers only call downward)
- HTTP request-response cycle
- Server-side rendering vs client-side rendering
- What Jinja2 is and how it integrates with FastAPI
- What an ORM is and why SQLAlchemy exists
- What database migrations are and why Alembic is needed
- FastAPI vs Flask vs Django tradeoffs
- PostgreSQL vs MySQL vs SQLite vs MongoDB tradeoffs
- PostgreSQL installation and service management on macOS
- Creating a PostgreSQL database from the terminal
- What PATH is and why tools need to be on it
- What pip is and how it differs from pip3 outside a virtual environment
- What a virtual environment is and why it isolates project dependencies
- What .gitignore is and how Git uses it to exclude files
- ACID guarantees and why they matter in a hospital context
- SQLAlchemy Declarative Base pattern and how Python classes map to tables
- Alembic migration workflow — init, autogenerate, upgrade, version tracking
- FastAPI dependency injection using Depends()
- FastAPI type hint validation and 422 error responses
- Async versus sync in FastAPI at a conceptual level
- The difference between SQLAlchemy models and Pydantic schemas
- Which fields to exclude from a Pydantic input schema and why
- SQLAlchemy models — writing Python classes that map to database tables
- Alembic migrations — init, autogenerate, upgrade workflow
- Database sessions — engine, SessionLocal, Base pattern
- Pydantic — schemas vs SQLAlchemy models, input/output separation, which fields to exclude
- FastAPI dependency injection using Depends() and the get_db() generator pattern
- Pydantic input vs output schema separation and why both are needed
- Service layer implementation — separating business logic from API handlers
- Resource management with Python generators (yield + finally)
- SQLAlchemy session lifecycle — add, commit, refresh
- State machine enforcement in the service layer
- State diagrams and why they catch invalid status transitions before code does
- Entity relationship diagrams using Mermaid syntax
- Checking a UI mockup against an already-decided schema instead of building straight from the mockup
- Deriving a second UI signal (delayed) from the same time-based pattern used for priority
- A service function that reaches into more than one table in a single operation
- Jinja2 template inheritance with {% extends %} and {% block %}
- Why HTML form submissions need Form() parameters instead of a Pydantic request body, and why that requires python-multipart
- The difference between an unchecked checkbox (field missing entirely) and an empty dropdown (field present as an empty string), and converting the empty string to None before it reaches a Pydantic schema
- The POST-redirect-GET pattern: returning a 303 after a form submission so a page refresh doesn't resubmit it
- Catching a service-layer ValueError inside a web route and re-rendering the same page with an error, instead of letting FastAPI return an unhandled 500
- Jinja2 and Django use the same {% %} template syntax by design, but Jinja2 is a separate library with no Django dependency
- Attaching a computed value directly to a SQLAlchemy object in a route handler so a template can read it, without saving it or writing a new service function
- Reading a raw traceback to diagnose a library version-compatibility bug, not a mistake in my own code
- Telling the difference between a business-rule gap worth fixing now and one worth only documenting
- Resolving a stale git index.lock file
- FastAPI's StaticFiles mount and why serving CSS requires it explicitly
- CSS custom properties as design tokens, and why one :root block beats scattered hex values
- Why Alembic's env.py has its own separate database config from the app's runtime code, and why a bug there can hide for weeks if your local environment happens to match the hardcoded fallback
- Deploying a FastAPI + Postgres app to a PaaS: build commands vs. start commands, environment variables in production, free-tier constraints (spin-down, storage limits, no shell access)
- Database seeding as an idempotent script, separate from schema migrations
- HTTP redirects via RedirectResponse

Partially Understood:

- Database normalization
- REST API design
- Translating a schema into Python model classes

Not Learned Yet:

- Testing

Current Learning Objective:

- Full manual testing pass, then presentation materials
