# VECTRIS

Hospital Patient Transport Operations Platform

> Last Project Update: July 3, 2026

## Project Overview

Vectris is a healthcare transportation coordination platform designed to streamline the process of requesting, assigning, tracking, and completing patient transport operations within a healthcare facility.

## Project Information

| Item                    | Value                                         |
| ----------------------- | --------------------------------------------- |
| Project Name            | Vectris                                       |
| Author                  | Christian Ventura                             |
| Course                  | GIT 480                                       |
| Project Type            | Senior Project                                |
| Focus Area              | Backend Development                           |
| Development Methodology | Systems-First Design                          |
| Primary Goal            | Healthcare Transportation Workflow Management |

## Problem Statement

Hospital transport operations often rely on fragmented communication methods such as:

- Phone calls
- Verbal requests
- Manual tracking
- Multiple disconnected systems

These processes often result in:

- Delayed patient movement
- Reduced operational visibility
- Increased administrative overhead
- Inconsistent reporting
- Poor resource utilization

Vectris aims to centralize these operations through a structured workflow-driven platform.

## Project Objectives

### Operational Goals

- Receive transport requests
- Assign requests to transport staff
- Track request progress
- Complete transport requests
- Improve transport visibility
- Monitor operation metrics

### Learning Goals

This project demonstrates:

- Systems thinking
- Backend engineering fundamentals
- Database design (relational modeling)
- REST API design
- State management
- Software architecture
- GIT-based development workflow
- Documentation-driven development

## Core Product Vision

Vectris is **dispatch operations console**.

It is designed around operational decision-making rather than data entry.

The dispatcher should be able to answer, within seconds:

- What requests are waiting?
- What transporters are available?
- What transporters are currently busy?
- Which requests require immediate attention?

The system priorities **clarity over complexity** and **operational awareness over feature depth**.

## Users

### Dispatcher (Primary User)

Responsible for:

- Monitoring incoming transport requests
- Assigning transporters
- managing workflow state
- Handling delays or exceptions
- Maintaining operational flow

### Transporter

Responsible for:

- Receiving assigned transport tasks
- updating task status
- Completing transport requests

### Supervisor

Key roles:

- Monitoring overall operations
- Reviewing performance metrics
- Evaluating system efficiency

## Minimum Viable Product (MVP)

Vectris is successful if it completes only three workflows:

### 1. Receive Requests

Departments submit transport requests into the system.

### 2. Assign Requests

Dispatchers assign available transporters to requests.

### 3. Complete Requests

Transporters complete assigned requests and update status.

> If these workflows function correctly, the MVP is complete.

Everything else is optional.

## Core Entities

### Transport Request

Represents a unit of work to be completed.

**Fields:**

- Patient Name

- Origin Department

- Destination Department

- Equipment Requirements

- Current Status

- Time Created

- Time in Queue

### Transporter(staff entity)

Represents hospital transport staff.

**Fields:**

- Name / ID

- Availability Status

- Current Assignment

- Break Status

- Workload State

### Assignment

Represents the relationship between a request and a transporter.

**Fields:**

- Transport Request ID

- Transporter ID

- Assignment Time

- Assignment Status

### Dispatch Event

Represents system activity and state changes.

**Examples:**

- Request Created

- Request Assigned

- Status Updated

- Request Completed

- Delay Logged

## System Design Principles

### Systems First

Workflow → Entities → Database → API → UI

### Operational Simplicity

Only build features that directly support:

- Receiving requests

- Assigning requests

- Completing requests

Everything else is secondary.

### Time-Based Priority (NOT Algorithmic Priority)

Vectris does not implement priority scoring.

Instead, it relies on:

- Time in queue

- Request age

- Status visibility

This avoids complexity and removes subjective prioritization logic.

## Current Project Status

### Phase

Frontend Verification & Polish

### Current Focus

All three MVP workflows work end to end through the dispatcher dashboard: create a request, assign a transporter, complete a request. Remaining work is the dashboard's delayed panel, a full testing pass, and presentation materials.

## Running Locally

Vectris needs Python 3.11+ and a running PostgreSQL instance.

Clone the repo and set up a virtual environment:

```bash
   python -m venv venv
```

Activate it — the command depends on your shell:

| Shell                    | Command                     |
| ------------------------ | --------------------------- |
| macOS/Linux (bash/zsh)   | `source venv/bin/activate`  |
| Windows (Command Prompt) | `venv\Scripts\activate.bat` |
| Windows (PowerShell)     | `venv\Scripts\Activate.ps1` |

---

Then install dependencies:

```bash
   pip install -r requirements.txt
```

Create the PostgreSQL database:

```bash
   createdb vectris
```

   If `createdb` isn't on your PATH or you get a role/permission error, connect with `psql` and run it manually instead:

```bash
   psql -U postgres -c "CREATE DATABASE vectris;"
```

Create a `.env` file with your database connection string:

```env
   DATABASE_URL=postgresql://localhost/vectris
```

   If your PostgreSQL setup requires a username and password, use
   `postgresql://user:password@localhost/vectris` instead.

Apply the database migrations:

```bash
   alembic upgrade head
```

Start the server:

```bash
   uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in a browser to reach the dispatcher dashboard, or `http://127.0.0.1:8000/docs` for the Swagger API reference.

### Current Status

All three MVP workflows are functional through the dashboard. See `docs/build_state.md` for exactly what's working right now.

## Repository Structure

```text
vectris/
│
├── app/
    ├── api/
    ├── database/
    ├── models/
        ├── entities.md
    ├── services/
├── archive/
    ├── project_state_v1.md
├── docs/
    ├── architecture.md
    ├── backlog.md
    ├── build_state.md
    ├── decisions.md
    ├── diagrams.md
    ├── learning_state.md
    ├── project_state.md
    ├── repository_map.md
├── frontend/
├── tests/
├── README.md
├── requirements.txt
```

---

***Vectris*** | Patient Transport Coordination Platform | christianVenturaDesigns 2026
