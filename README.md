# VECTRIS

**Patient Transport Coordination Platform**

**Senior Project: GIT 480**  
**Author:** Christian Ventura


## Project Overview

Vectris is a healthcare transportation coordination platform designed to streamline the process of requesting, assigning, tracking, and completing patient transport operations within a healthcare facility.

The project focuses on reducing communication delays, improving transport visibility, increasing operational efficiency, and creating a centralized workflow for transport coordinators, dispatchers, and transport personnel.

Rather than functioning as a simple scheduling application, Vectris is being designed as a complete operational system that models real-world hospital transport workflows from request creation through transport completion.

This repository contains all planning, research, architecture, documentation, development assets, and source code associated with the GIT 480 Senior Project.


## Project Information

| Item | Value |
|--------|--------|
| Project Name | Vectris |
| Author | Christian Ventura |
| Course | GIT 480 |
| Project Type | Senior Project |
| Focus Area | Backend Development |
| Development Methodology | Systems-First Design |
| Primary Goal | Healthcare Transportation Workflow Management |


## Problem Statement

Many healthcare transportation processes rely on fragmented communication methods, manual coordination, phone calls, and inconsistent tracking procedures.

These challenges often result in:

- Delayed patient movement
- Reduced operational visibility
- Increased administrative overhead
- Inconsistent reporting
- Poor resource utilization

Vectris aims to centralize these operations through a structured workflow-driven platform.


## Project Objectives

### Primary Objectives

- Model real-world patient transport operations
- Create a centralized request management system
- Improve transport visibility
- Provide transport status tracking
- Support operational reporting
- Design scalable backend architecture
- Demonstrate full software development lifecycle practices

### Technical Objectives

- Design a normalized relational database
- Create a RESTful API architecture
- Implement workflow state management
- Support audit and historical tracking
- Follow modern Git workflows
- Produce professional engineering documentation


# Repository Structure

```text
vectris/
│
├── api/
├── assets/
├── backend/
├── database/
├── deployment/
├── diagrams/
├── docs/
├── scripts/
├── tests/
│
├── README.md
└── CHANGELOG.md
```

# Directory Guide

## api/

Contains API-related documentation, specifications, and endpoint definitions.

### Expected Contents

```text
api/
├── openapi/
├── endpoint-specifications/
└── request-response-examples/
```

### Purpose

- Define API contracts
- Document endpoints
- Standardize communication between systems
- Support future frontend integration


## assets/

Stores project assets and supporting resources.

### Examples

```text
assets/
├── mockups/
├── wireframes/
├── icons/
├── branding/
└── screenshots/
```

### Purpose

- Visual references
- UI planning materials
- Presentation assets
- Demonstration materials


## backend/

Contains application source code.

### Expected Responsibilities

- Business logic
- Service layer
- Authentication
- Authorization
- Workflow processing
- API implementation

### Potential Structure

```text
backend/
├── controllers/
├── services/
├── models/
├── middleware/
├── routes/
└── utilities/
```

### Purpose

- Core application functionality
- Workflow orchestration
- Data processing


## database/

Contains all database-related artifacts.

### Examples

```text
database/
├── schemas/
├── migrations/
├── seed-data/
├── diagrams/
└── queries/
```

### Purpose

- Entity definitions
- Database planning
- Migration history
- Query optimization


## deployment/

Contains deployment and infrastructure resources.

### Examples

```text
deployment/
├── docker/
├── environment/
├── infrastructure/
└── deployment-guides/
```

### Purpose

- Environment configuration
- Infrastructure planning
- Deployment procedures
- Production readiness documentation

## diagrams/

Contains architectural and workflow visualizations.

### Examples

```text
diagrams/
├── workflow/
├── architecture/
├── database/
├── sequence/
└── network/
```

### Purpose

- System communication visualization
- Workflow analysis
- Architectural planning
- Stakeholder communication


## docs/

Central documentation repository.

```text
docs/
├── architecture/
├── decisions/
├── operations/
├── requirements/
├── research/
└── workflows/
```

### Purpose

Maintain project knowledge throughout the software development lifecycle.


### docs/architecture/

Contains technical architecture documentation.

Examples:

- System architecture
- Component diagrams
- Service interactions
- Technology stack decisions

---

### docs/decisions/

Architecture Decision Records (ADRs).

Examples:

- Database selection
- Framework selection
- Security decisions
- Infrastructure decisions

Purpose:

Document why decisions were made rather than only what was built.


### docs/operations/

Operational procedures and support documentation.

Examples:

- Deployment procedures
- Monitoring strategies
- Incident response planning
- Maintenance processes


### docs/requirements/

Business and technical requirements.

Examples:

- Functional requirements
- Non-functional requirements
- User stories
- Acceptance criteria

Purpose:

Defines what the system must accomplish.

### docs/research/

Research conducted during project planning.

Examples:

- Industry analysis
- Competitor analysis
- Workflow research
- Technical investigations

Purpose:

Provides evidence supporting design decisions.

### docs/workflows/

Business process documentation.

Examples:

- Patient transport lifecycle
- Request creation process
- Dispatch process
- Completion process

Purpose:

Translate real-world operations into system workflows.


## scripts/

Utility scripts used during development.

### Examples

```text
scripts/
├── database/
├── setup/
├── maintenance/
└── automation/
```

### Purpose

- Environment setup
- Data management
- Developer productivity
- Automation tasks


## tests/

Contains testing resources.

### Examples

```text
tests/
├── unit/
├── integration/
├── api/
└── performance/
```

### Purpose

- Validate functionality
- Prevent regressions
- Verify system behavior


# Documentation Standards

The project follows a documentation-first approach.

Major project decisions should be documented before implementation whenever possible.

Documentation categories include:

- Requirements
- Architecture
- Research
- Operational Procedures
- Workflow Analysis
- Decision Records


# Development Philosophy

This project follows a systems-first engineering approach.

Before implementation:

1. Understand the operational workflow.
2. Define system requirements.
3. Design entities and relationships.
4. Create architecture documentation.
5. Establish repository structure.
6. Build implementation plans.
7. Begin development.

The objective is to design a system before writing code.


# Planned Core Features

## Request Management

- Create transport requests
- Prioritize requests
- Track request lifecycle

## Dispatch Operations

- Assign transport personnel
- Manage active transports
- Monitor workloads

## Status Tracking

- Pending
- Assigned
- In Progress
- Completed
- Cancelled

## Reporting

- Operational metrics
- Transport completion data
- Utilization reporting

## Audit Tracking

- Historical activity records
- Status changes
- Assignment history


# Technology Focus

This project serves as a practical demonstration of:

- Python
- Backend Development
- REST API Design
- SQL Database Design
- System Architecture
- Git Workflows
- Documentation Practices
- Software Engineering Principles


# Change Management

Project changes are tracked through:

```text
CHANGELOG.md
```

The changelog documents:

- Added features
- Modified functionality
- Documentation updates
- Architectural changes


# Current Project Phase

**Phase:** Planning and System Design

### Current Deliverables

- Workflow Analysis
- Entity Identification
- Requirements Definition
- Database Planning
- Architecture Design
- Repository Structure
- Documentation Framework

Implementation will begin after foundational planning artifacts have been completed and reviewed.


## Author

**Christian Ventura**  
GIT 480 Senior Project

**Vectris __ Patient Transport Coordination Platform**
