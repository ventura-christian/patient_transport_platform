# TESTING CHECKLIST

> Last Updated: July 4, 2026

A manual reference for testing Vectris endpoints through Swagger UI while there's no automated test suite yet. Not a replacement for real tests, just a repeatable way to confirm my endpoints work.

## Before Testing Anything

1. Activate the virtual environment: `source venv/bin/activate`
2. Start the server: `uvicorn main:app --reload`
3. Open `http://127.0.0.1:8000/docs`

## One Thing to Note

Reference `entities.md` in my directory at `app/models/entities.md`. This document shows the information of all the tables and context to test my endpoints.

## Transporters

- `POST /transporters/`: create one with a name, confirm a 200 with an id and `"status": "available"`
- `GET /transporters/`: confirm the list includes what you just created
- `PATCH /transporters/{id}/status` with an invalid status: confirm 400
- `PATCH /transporters/{id}/status` with a made-up id: confirm 404
- `PATCH /transporters/{id}/status` with a valid status: confirm 200 and the status field actually changed

## Transport Requests

- `POST /transport-requests/`: create one, confirm a 200 with status "active"
- `GET /transport-requests/`: confirm the list includes what you just created
- `PATCH /transport-requests/{id}/status` skipping a step (active straight to complete): confirm 400
- `PATCH /transport-requests/{id}/status` with a made-up id: confirm 404

## Assignments

- `POST /assignments/` with a valid active request and available transporter: confirm 200, request status becomes "in_progress", transporter status becomes "on_job"
- `POST /assignments/` against a request that's already complete: confirm 400
- `POST /assignments/` with a transporter that's already on_job: confirm 400
- `GET /assignments/{request_id}`: confirm it lists the assignment just created

## Dashboard (/dashboard)

- Load with no data: confirm it renders with zero counts and empty tables, no error
- Create a request and a transporter through Swagger, reload: confirm both show up
- Confirm the three stat counts match what's actually in the queue and staff panel

## Create Request (/create-request)

- Submit a complete form: confirm redirect to /dashboard and the new request appears in the active queue
- Leave a required field blank: confirm the browser blocks submission before it reaches the server
- Leave the equipment dropdown on its default: confirm the created request stores equipment_needed as null, not an empty string

## Assign Transporter (/assign/{request_id})

- Open from the dashboard's "Assign" link on an active request: confirm patient details and available transporters show correctly
- Assign a transporter: confirm redirect to /dashboard, request now in_progress, transporter now on_job
- Open /assign/{id} for a request ID that doesn't exist: confirm "Request not found," not a crash

## Job Detail and Completion (/requests/{request_id})

- Open from the dashboard's "View" link on an in-progress request: confirm patient info, status, and assigned transporter name(s) show correctly
- Click "Mark Complete" on a fully-staffed request: confirm redirect to /dashboard, request no longer appears in either queue section, transporter(s) return to "available"
- Open /requests/{id} for a request ID that doesn't exist: confirm "Request not found," not a crash

## Multi-Transporter Requests

- Create a request with "Transporters Required" set to 2
- Assign one transporter: confirm the dashboard shows "Assign More" next to it, and Job Detail shows "needs 2, has 1" instead of a Mark Complete button
- Assign a second transporter: confirm "Assign More" disappears from the dashboard and Mark Complete appears on Job Detail
- Complete the request: confirm both transporters return to "available"

## Live Deployment (Render)

- Visit the live URL with no path: confirm it redirects to /dashboard, not a 404
- Confirm the dashboard loads with the seeded sample transporters and requests
- Confirm the stylesheet actually loaded (dark background, styled cards). A blank white page with plain text means /static isn't mounted correctly
- Run through all three MVP workflows against the live database: create a request, assign a transporter, mark complete
- Reload after 15+ minutes idle: confirm the cold-start delay is a loading page, not an error
