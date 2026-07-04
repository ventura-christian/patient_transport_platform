# DIAGRAMS

> Last Updated: July 4, 2026

This file holds the visual and structural references for how a transport request moves through Vectris, how the three tables relate to each other, and what each dashboard screen shows.

## Transport Request Status

A request only moves one direction. Nothing loops back once it starts.

```mermaid
stateDiagram-v2
    [*] --> active: Request created
    active --> in_progress: Transporter assigned
    in_progress --> complete: Transporter marks job done
    complete --> [*]
```

## Transporter Status

A transporter goes on a job and comes back automatically once that job is marked complete. A dispatcher can also pull someone into a break by hand.

```mermaid
stateDiagram-v2
    [*] --> available
    available --> on_job: Assigned to a request
    on_job --> available: Assigned request marked complete
    available --> on_break: Dispatcher marks break
    on_break --> available: Dispatcher marks back
```

## Entity Relationships

```mermaid
erDiagram
    TRANSPORT_REQUESTS ||--o{ REQUEST_ASSIGNMENT : "has"
    TRANSPORTERS ||--o{ REQUEST_ASSIGNMENT : "has"

    TRANSPORT_REQUESTS {
        int id PK
        string patient_name
        string origin_department
        string origin_room
        string destination_department
        string equipment_needed
        boolean biohazard
        int transporters_required
        string status
        timestamp created_at
        timestamp completed_at
    }

    TRANSPORTERS {
        int id PK
        string name
        string status
    }

    REQUEST_ASSIGNMENT {
        int id PK
        int transport_request_id FK
        int transporter_id FK
        timestamp assigned_at
    }
```

## Dashboard Screens

Four screens, drawn from the wireframe I built for this project and checked against entities.md and decisions.md.

- **Dashboard:** A header, three stat cards (waiting, in progress, available staff), then two panels: the request queue (active and in-progress requests together, oldest first) and the transport staff list. Visual design decisions (color, typography) are logged separately in decisions.md.

- **Create Request:** Patient name, origin department (dropdown), origin room (text), destination department (dropdown), equipment needed (dropdown), biohazard (checkbox), transporters required (number, defaults to 1), and a submit button.

- **Assign Transporter:** The selected request's patient information next to a list of available transporters, with a button to assign one.

- **Job Detail:** Patient name, department, assigned transporter, and current status, with a button to update the status.

No priority field anywhere. No status history timeline, no delayed panel. All three were cut once checked against decisions already made. The queue's sort order is the only priority signal Vectris has, and nothing tracks status changes over time.
