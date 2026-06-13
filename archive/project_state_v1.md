# PROJECT_STATE.md

## VECTRIS

### Hospital Transport Operations Platform

---

## PROJECT STATUS

**Last Updated:** June 10, 2026  
**Project Due Date:** July 5, 2026  
**Days Remaining:** 25

**Current Phase:** Planning & System Definition

**Project Health:** On Track

---

## SESSION CHECKPOINT

Update this section every time work is completed.

| Field                | Value                                            |
| -------------------- | ------------------------------------------------ |
| Date                 | June 10, 2026                                    |
| Day                  | Wednesday                                        |
| Last Working Session | Project Definition & Requirements                |
| Current Focus        | Dispatcher Operations Console                    |
| Next Task            | Define Main Operations Screen Layout             |
| Blockers             | None                                             |
| Notes                | MVP fully defined. Scope boundaries established. |

---

## PROJECT OVERVIEW

## Project Name

Vectris

## Project Type

AI-Powered Hospital Transport Operations Management Platform

## Primary Goal

Improve hospital transport operations by:

- Reducing bottlenecks
- Improving task visibility
- Tracking transporter workload
- Improving assignment efficiency
- Providing operational intelligence

---

## USERS

## Primary User

Dispatcher

Responsible for:

- Monitoring requests
- Assigning transporters
- Managing workflow
- Resolving delays

---

## Secondary User

Transporter

Responsible for:

- Receiving assignments
- Updating transport status
- Completing transports

---

## Tertiary User

Supervisor / Manager

Responsible for:

- Monitoring operations
- Reviewing performance
- Tracking metrics

---

## CORE PRODUCT VISION

Vectris is a centralized dispatch operations console designed to provide real-time visibility into hospital transport operations.

The system is designed around operational decision-making rather than data entry.

The dispatcher should be able to understand system status within seconds and make assignment decisions rapidly.

---

## MVP DEFINITION

The MVP succeeds if it can perform three actions:

## 1. Receive Transport Requests

Departments submit transport requests.

---

## 2. Assign Transport Requests

Dispatcher assigns requests to transporters.

---

## 3. Complete Transport Requests

Transporters complete assigned requests.

---

## MVP SUCCESS RULE

If these three workflows function correctly, the project is successful.

Everything else is secondary.

---

## FIVE CORE ENTITIES

Every feature should support at least one of these entities.

## Transport Request

Represents work needing completion.

### Information Required

- Patient Name
- Requesting Department
- Urgency Level
- Equipment Requirements
- Current Status

---

## Dispatcher

Coordinates all transport operations.

### Responsibilities

- Monitor queue
- Assign transporters
- Resolve delays

---

## Transporter

Completes transport requests.

### Information Required: Transport Requests

- Availability
- Current Assignment
- Skill Restrictions
- Physical Restrictions
- Workload

---

## Assignment

Connects requests with transporters.

### Information Required: Assignment Decision Metrics

- Assigned Transporter
- Assignment Time
- Assignment Status

---

## Status

Tracks progress of requests.

### Status Values

- New
- Assigned
- In Progress
- Completed
- Delayed
- Cancelled

---

## SCOPE CONTROL RULE

Whenever a new idea appears, ask:

> Does this directly support one of the five core entities?

If the answer is no, it is likely scope creep.

---

## DISPATCHER WORKFLOW

## Information That Changes Most Frequently

The dispatcher must constantly monitor:

- Staff currently on duty
- Staff currently assigned
- Incoming requests
- Delay information

---

## Information Needed Before Assignment

The dispatcher must know:

### Request Information

- Patient Name
- Requesting Department
- Urgency
- Equipment Needed

### Resource Information

- Available Transporters
- Staff Capabilities
- Injury Restrictions
- Equipment Availability
- Number of Staff Required

---

## PRIORITY MANAGEMENT

## Highest Priority Concern

Determine which transport request requires attention first.

Priority is influenced by:

- Request Type
- Urgency
- Operational Relevance
- Delay Conditions

---

## REQUIRED FEATURES

## Transport Request Queue

Displays:

- New Requests
- Assigned Requests
- In Progress Requests
- Completed Requests

---

## Transporter Panel

Displays:

- Available Transporters
- Assigned Transporters
- Current Workload

---

## Assignment Workflow

Dispatcher can:

- Select Request
- Select Transporter
- Assign Task

---

## Completion Workflow

Transporter can:

- Accept Assignment
- Update Status
- Complete Assignment

---

## OPTIONAL FEATURES

Only build these if MVP is complete.

## Intelligence Features

- AI Recommendations
- Predictive Analytics

## Communication Features

- Messaging
- Notifications

## Operational Features

- Shift Forecasting
- Route Optimization

## Management Features

- KPI Dashboards
- Cost Savings Reporting

---

## SUCCESS METRICS

The project should achieve the following outcomes.

## Dispatcher Efficiency

Dispatcher can assign a request in:

***Less than 10 seconds***

---

## Transporter Efficiency

Transporter can update status in:

***Fewer than 3 interactions***

---

## Queue Visibility

New requests appear immediately.

---

## Staff Visibility

Available transporters are immediately identifiable.

---

## DESIGN PRINCIPLES

## Design Around Peak Operations

The interface should not be optimized for:

- 2 requests
- 1 transporter
- Quiet periods

The interface should be optimized for:

- 20+ requests
- Multiple transporters
- Delays
- Constant interruptions
- High workload periods

---

## CURRENT DESIGN DIRECTION

## Main Product

Dispatch Operations Console

Single-screen operational dashboard focused on:

- Request visibility
- Assignment speed
- Workload awareness
- Operational decision-making

---

## MENTOR ASSESSMENT

## Current Strengths

- Well-defined MVP
- Clear scope boundaries
- Realistic workflow
- Strong domain knowledge
- Strong understanding of operational pain points
- Recognition that a unified console is superior to multiple disconnected screens

---

## Areas Still Requiring Refinement

### User Prioritization

Confirm whether:

- Dispatcher is primary user
- Transporter is primary user

Current assumption:

***Dispatcher is primary user***

---

### Information Architecture

Define:

- Main operations screen layout
- Panel hierarchy
- Visual priority system

---

### Exception Handling

Determine representation for:

- Delays
- Cancellations
- Failed assignments
- Escalations

---

### Measurable Outcomes

Convert success criteria into measurable user outcomes.

---

## OPEN QUESTIONS

These must be answered during the next design review.

## Question 1

If a dispatcher has only 5 seconds to view the screen:

What are the three most important pieces of information they must immediately understand?

### Proposed Answer: Q1

1. New high-priority requests
2. Available transporters
3. Active delays or issues

---

## Question 2

What information must be visible without opening a request?

### Proposed Answer: Q2

- Patient Name
- Department
- Urgency
- Status
- Time Waiting

---

## Question 3

During 20+ active requests, how should the system identify what needs attention first?

### Proposed Answer: Q3

Visual prioritization through:

- Priority indicators
- Aging timers
- Delay warnings
- Queue ordering

---

## REPOSITORY STRUCTURE

```text
patient-transport-platform/
│
├── api/
├── assets/
├── backend/
├── database/
├── deployment/
├── diagrams/
├── docs/
├── scripts/
└── tests/
```

---

## DOCUMENTATION STRUCTURE

```text
docs/
│
├── architecture/
├── decisions/
├── operations/
├── requirements/
├── research/
└── workflows/
```

---

## PROJECT DECISION LOG

## June 10, 2026

Decision:
Dispatcher will be treated as the primary user for design decisions.

Reason:
Dispatcher experiences the highest information load and is the operational coordinator.

---

Decision:
System will focus on a unified dispatch console rather than multiple disconnected screens.

Reason:
Improves situational awareness and assignment speed.

---

## NEXT IMMEDIATE OBJECTIVES

1. Define main operations screen layout
2. Create dispatcher information architecture
3. Create workflow diagram
4. Define transport request entity
5. Define transporter entity
6. Define assignment entity
7. Define status lifecycle
8. Create database draft

---

## REMINDER

Every new feature request must answer:

> Does this help the dispatcher receive, assign, or complete a transport request?

If not, it does not belong in the MVP.
