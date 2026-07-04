# PROJECT_STATE

> Last Updated: July 4, 2026

## Current Phase

Deployment and Submission Prep

## Project Summary

Vectris is a hospital patient transport operations platform focused on:

1. Creating transport requests
2. Assigning transport requests
3. Tracking request completion

## MVP Scope

Included:

- Request creation
- Assignment workflow
- Status Tracking
- Dispatcher dashboard
- Database persistence
- REST API

## Current Status

Completed:

- Project scope
- User identification
- Workflow analysis
- MVP definition
- Technology direction
- Workflow stated defined (active, in_progress, complete)
- Entities identified (transport_requests, transporters, request_assignment)
- Data model fields defined
- Junction table pattern decided for multi-transporter support
- System design complete
- architecture.md documented (all 7 sections)
- Frontend technology direction decided (Jinja2 server-side templates)
- decisions.md updated with frontend technology decision
- PostgreSQL installed, running, and added to PATH
- Vectris database created
- completed_at column added to transport_requests schema
- Python virtual environment created and activated
- .gitignore created
- requirements.txt populated and all dependencies installed
- .env file created with database connection URL
- Database connection verified through virtual environment
- SQLAlchemy models written for all three entities
- Alembic initialized and first migration applied
- All three tables verified in PostgreSQL
- Pydantic schemas written for transport requests and transporters
- main.py created — FastAPI app boots and serves /docs
- get_db() dependency injection added to session.py
- transport_request_service.py written — create and status update
- Jinja2 wired into FastAPI through a new app/web/ package
- Dashboard screen: request queue, transporter staff panel, stat counts
- Create Request screen, including HTML form parsing with Form()
- Assign Transporter screen
- Job Detail screen with request completion
- All three MVP workflows (create, assign, complete) reachable end to end through the dashboard
- Multiple transporters per request now enforced, not just stored
- Dashboard, Create Request, Assign, and Job Detail screens restyled with a shared dark-theme design system
- Static file serving added via FastAPI's StaticFiles mount
- seed.py created for reproducible sample data
- alembic/env.py fixed to read DATABASE_URL from the environment instead of a hardcoded ini value
- Deployed live on Render with a working web service and Postgres database
- Root URL redirects to /dashboard
- Short on-page instructions added to the dashboard for first-time visitors

In Progress:

(none)

Descoped:

- Dashboard delayed panel and transporter current-assignment display were dropped deliberately. Neither is one of the three MVP workflows, and the remaining time before submission was worth more spent on the visual design and live deployment, which map to actual graded criteria.

Not Started:

- Automated tests
- Deployment

## Technology Direction

Backend:

- Python
- FastAPI

Database:

- PostgreSQL

Frontend:

- Jinja2 server-side templates (rendered by FastAPI)

Architecture:

- Monolithic application

## Current Risks

- Scope creep
- Learning curve
- Limited timeline
- Overthinking/over estimating my abilities

## Next Actions

1. Full manual pass through docs/testing_checklist.md
2. Presentation materials
3. Final proofread of all docs before submission
