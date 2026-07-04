# Repository Map

> Last Updated: July 4, 2026

## Purpose(repository map)

This document defines the responsibility of each directory within the Vectris project repository.

Vectris follows a layered monolithic architecture:

```text
Frontend
↓
API Layer
↓
Business Logic Layer
↓
Database Layer
```

Each directory has a single, clearly defined responsibility.

---

## Repository Structure

```text
vectris/
├── app/
│   ├── api/
│   ├── web/
│   ├── database/
│   ├── models/
│   └── services/
├── archive/
├── docs/
├── frontend/
├── tests/
├── README.md
└── requirements.txt
```

---

## app/

### Purpose(app)

Contains the application's source code and implements the backend architecture of Vectris.

### Responsibilities(app)

- Handle transport requests
- Manage assignment workflows
- Apply business rules
- Persist application data
- Coordinate communication between layers

### Guiding Principle

This directory represents the core application.

---

## app/api/

### Purpose(api)

Implements the API layer.

### Responsibilities(api)

- Define HTTP endpoints
- Receive client requests
- Validate incoming data
- Call business services
- Return API responses

### Examples

- Create transport request
- View transport requests
- Assign transporter
- Update request status

### Guiding Principle(api)

This layer should contain minimal business logic and primarily coordinate request and response handling.

---

## app/web/

### Purpose(web)

Implements the HTML-rendering layer for the dispatcher dashboard.

### Responsibilities(web)

- Render Jinja2 templates for the dashboard, create request, assign transporter, and job detail screens
- Parse HTML form submissions
- Call business services
- Redirect the browser after a successful form submission

### Examples(web)

- Show the dashboard
- Show and submit the create request form
- Show and submit the assign transporter form
- Show job detail and submit request completion

### Guiding Principle(web)

This layer mirrors app/api/ but returns rendered HTML instead of JSON. Like app/api/, it should carry minimal business logic and coordinate between the browser and the service layer, nothing more.

---

## app/models/

### Purpose(models)

Defines the application's domain entities and database models.

### Responsibilities(models)

- Represent business concepts
- Define data structures
- Define relationships between entities
- Define persistence schemas

### Core Entities

- TransportRequest
- Transporter

### Guiding Principle(models)

Models describe what the system knows about the business domain.

---

## app/services/

### Purpose(services)

Implements business logic and workflow rules.

### Responsibilities(services)

- Manage request lifecycle
- Handle assignments
- Update workflow states
- Enforce operational rules
- Coordinate interactions between models

### Examples(services)

- Assign transporter to request
- Transition request status
- Determine transporter availability

### Guiding Principle(services)

Business decisions belong here, not in the API layer.

---

## app/database/

### Purpose(database)

Implements the persistence layer.

### Responsibilities(database)

- Configure PostgreSQL connections
- Manage database sessions
- Initialize database resources
- Provide ORM configuration
- Support data persistence

## migrations/

### Purpose

Contains Alembic migration files that track database schema changes.

### Responsibilities

- Version control for database schema
- Apply and roll back schema changes safely

### Guiding Principle(migrations)

Every change to the database schema goes through a migration, never applied manually.

### Technology

- PostgreSQL
- SQLAlchemy (planned)

### Guiding Principle(database)

This layer manages how information is stored and retrieved.

---

## frontend/

### Purpose(frontend)

Implements the dispatcher dashboard.

### Responsibilities(frontend)

- Display transport queues
- Display transporter availability
- Display workflow status indicators
- Support operational visibility
- Enable rapid dispatcher decision-making

### Primary Views

- Needs Assignment
- In Progress
- Completed
- Issues / Roadblocks

### Guiding Principle(frontend)

The dashboard exists to support operational awareness rather than data entry.

- frontend/templates/ holds the Jinja2 template files: base.html, dashboard.html, create_request.html, assign.html, and job_detail.html.
- frontend/static/css/style.css holds the shared design system (colors, typography, spacing) applied across all four screens.

---

## docs/

### Purpose(docs)

Contains project documentation and project knowledge.

### Responsibilities(docs)

- Project state management
- Architecture documentation
- Build tracking
- Learning tracking
- Design decisions
- Presentation assets

### Documentation Files

- project_state.md
- architecture.md
- backlog.md
- build_state.md
- learning_state.md
- decisions.md
- repository_map.md
- claude_instructions.md

### Guiding Principle(docs)

Documentation is treated as part of the system and evolves alongside implementation.

---

## tests/

### Purpose(tests)

Contains verification and testing resources.

### Responsibilities(tests)

- Verify API behavior
- Verify business logic
- Verify workflow transitions
- Validate application correctness

### Examples(tests)

- Request creation tests
- Assignment workflow tests
- Status transition tests

### Guiding Principle(tests)

Testing provides confidence that workflows behave as intended.

---

## archive/

### Purpose(archive)

Stores historical project artifacts.

### Responsibilities(archive)

- Preserve previous documentation versions
- Preserve planning artifacts
- Preserve deprecated materials

### Examples(archive)

- project_state_v1.md

### Guiding Principle(archive)

Files in this directory are historical references and are not considered the source of truth.

---

## README.md

### Purpose(README.md)

Provides the high-level overview of Vectris.

### Responsibilities(README.md)

- Explain project goals
- Define project scope
- Describe the MVP
- Introduce system architecture
- Explain repository organization

### Guiding Principle(README.md)

The README is the project's public entry point.

---

## requirements.txt

### Purpose(requirements.txt)

Defines Python dependencies required by the application.

### Responsibilities(requirements.txt)

- Document project dependencies
- Support environment setup
- Enable reproducible development environments

### Guiding Principle(requirements.txt)

Dependencies should remain minimal and directly support the MVP.

## seed.py

### Purpose(seed.py)

A one-time script that loads sample transporters and transport requests into whatever database it's pointed at. Not part of the application itself but rather, it's run manually, once, against a fresh database (local or deployed).

### Guiding Principle(seed.py)

Keeps demo data out of the schema migrations, where it doesn't belong, while still making a fresh database usable immediately.
