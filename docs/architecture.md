# Vectris Software Architecture Decisions & Explanations

> Last Updated: June 29, 2026

## Architecture Type

***What is a monolith?***

This is a single deployable unit:

- All of my code (API, business logic, database connection, frontend templates) lives in one codebase and runs as on frontend application.
- When I start the application, everything starts.
- When I deploy it, everything deploys.

***Alternative: Microservices***

The counterpart to a monolith is a microservice.

In a microservices architecture, I would break the application into many small, independent services.

Benefits of Microservices:

- Each service can scale independently.
- Teams can work on services independently without stepping on each other.
- A failure in one service doesn't bring down the whole system.

Trade-offs of microservices:

- Large operational complexity.
- Network calls between different services can fail, and I would have to think about timeouts, retries, or partial failures.
- Debugging is much harder.

***Why monolithic architecture for Vectris?***

- I only have one codebase and one deployable unit.
- All of my data  relationships(transport_requests, transporters, and request_assignments) heavily rely on each other and keeping all my code in one codebase simplifies my deployment.
- I have myself (one dev), three workflows, a timeline, and a transport team with a handful of users.
- I decided not to separated my codebase using microservices to avoid issues when debugging, simplify deployment, and because I am not taking this product to scale.
- I didn't want to hassle with tons of services, technologies, and attempting to get 5 services running in tandem. I felt this was not only overkill but could create problems that I didn't have otherwise.

## System Layers

I want to enforce the separation of concerns (each part of my application should have one job and know as little as possible about everything else). This will make my codebase easier to debug when something goes ary.

***Database Layer***

- This is where my data lives permanently.
- PostgreSQL is a running process that stores rows in tables on disk.
- Its only job is to store data reliably and retrieve data accurately.

***Business Logic Layer (Service Layer)***

There is one rule for this layer: ***if it's a business rule, it lives in the service layer, not the API***

- This is where decisions happen.
- I don't want to have to write multiple versions of the same code. If I need my API endpoint or my HTTP request to change and update, then I'd essentially be making more of a mess for myself if a bug occurs and I have the same code written twice or in different locations.

***API Layer***

The API layer (app/api/)has a narrow job: to receive input, validate that it's shaped correctly, call the right service, and return the result.

It should not be making business decisions. It should not be writing SQL (structured query language).

It is a thin translation layer between the outside world and the Vectris internals.

***Frontend Layer***

This layer lives in (frontend/) and is the part the dispatcher sees and interacts with.

- These are the Jinja2 templates that contain HTML files with Python variables injected into them.
- The frontend depends on the the API to provide it with data.
- It doesn't apply business rules.
- It asks the API for data and displays it.

***The Direction Rule***

I will apply this rule so that the information and dependencies only flow downward, never upwards.

Each layer will never understand the layer above it and that is what will make Vectris powerful, easy to debug if issues arise, and allow me to adjust tech if I need to without having to rewrite entire sections of the codebase that relies on whatever I may change.

## Technology Stack

***Python***

This is the language I will write Vectris in.

The reasons behind this decision:

- Large ecosystem of libraries
- A robust feature set
- Has nice performance characteristics
- Excellent data manipulation
- Readable syntax that prioritizes clarity
- Strong web framework ecosystem

***FastAPI vs Flask vs Django***

***Why not Flask?***

- It's a microframework that provides routing and request handling but none of the other robust features that Django and FastAPI offer.
- I would have to incorporate all of the other tech I will need (database integration, templating, validation) from third party libraries.
- I would have to make all structural decisions myself and there are better options that provide me those features baked in.

***Why no Django?***

- I felt this framework makes too many decisions and comes packed with an ORM (object relational mapping), an admin panel, a templating engine, authentication, a migration system and much more.
- unfortunately, for my application and needs, this was overkill and was largely unnecessary for my design choice.

***Why FastAPI?***

- It's modern, high performance and designed around Python's type annotation system.
- I get automatic data validation with Pydantic, automatic API documentation with Swagger UI, async support by default, and a clean dependency injection system.
- It's specifically designed for building APIs which is exactly the tech I need for my project.
- I also want to use Jinja2 and vectris can be served both JSON endpoints and HTML pages with FastAPI in a clean and structured fashion.
- It is also the fastest between Flask and Django and the type annotation system will help me catch errors earlier.
- I also liked the automatic documentation feature to help with my presentation.

***PostgreSQL vs Alternatives***

PostgreSQL:

- It is a relational database, and relational means the data is organized into tables with rows and columns.
- Those tables can reference each other through foreign keys.
- SQL is the language used to query it.

MySQL:

- It is another relational database, and it is very similar to PostgreSQL in concept.

SQLite:

- This is a relational database that runs as a file, not a server.
- It's embedded directly into the application and is extremely simple to set up, no installation or configuration.
- The trade off is that it is not suitable for production systems with concurrent writes.

MongoDB:

- This is a non-relational document database.
- Instead of tables and rows, it stores JSON-like documents.
- It is flexible because you don't need to define a schema upfront, but rather you just store the documents.
- The trade-off is that you lose relational integrity, you can't enforce foreign keys, and you can't easily join data across collections the way you join tables in SQL.

***Why PostgreSQL for Vectris?***

My data is relational, with only three tables that have foreign keys between them, a junction table pattern that only made sense with a relational model.

PostgreSQL is also the industry standard for the kind of system that I am building.

PostgreSQL was also preferred for ACID (a set of guarantees that relational databases make about every transaction):

- **Atomicity**: A transaction either completes entirely or doesn't happen at all.
- **Consistency**: The database will only accept data that satisfies every rule I defined - foreign keys, NOT NULL constraints, data types.
- **Isolation**: This ensures if two operations occur at the same, they don't interfere with each other.
- **Durability**: This ensures that once a transaction is committed, it's permanent - a server crash, a power outage, or a restart, the data will survive.

***SQLAlchemy - What is an ORM?***

**ORM** stands for Object Relational Mapper, and understanding why this exists requires understanding the problems they solve.

- To simplify this explanation, Python thinks in objects and PostgreSQL thinks in tables. There is a mismatch that would occur between the two languages, and without the ORM I would have to make raw requests within a string in Python.
- With SQLAlchemy, I can define a Python class that will represent a table. Each attribute of the class represents a column, and when I want to create a new row, I just create a new instance of the class and save it.
- SQLAlchemy will translate it into SQL for me, and when I query it, I will get back Python objects, not raw tuples.

***Alembic - What are migrations?***

This is a migration management tool for SQLAlchemy. It tracks the history of every change I'll make to the database schema. It will store those changes as versions of migration files, and it will let me apply or roll back changes in order.

- For my project Vectris, Alembic will allow me to go from no database to three tables and potentially from three tables to four tables. The evolution of this creation will be tracked, reproducible, and safe.

***Jinja2 - What is Server-Side Rendering?***

Client-side rendering(this is what React and Vue do):

- The server sends a mostly empty HTML file and a large JavaScript file to the browser. The JavaScript runs in the browser, calls the API to fetch data, and builds the HTML dynamically on the client machine.

Server-side rendering(what Jinja2 does):

- The server does all the work, and when the browser requests a page, the server fetches the data from the database, injects it into an HTML template, and sends it back as a complete, fully rendered HTML page.

Jinja2 is a templating engine for Python.

Why does this fit Vectris?

- My dispatcher dashboard is primarily a read display. It shows the current state of operations. A full page refresh when the dispatcher submits a form or assigns a transporter is completely acceptable under these conditions.
- The added complexity of client-side rendering, where I would have to manage the state in JavaScript, handle API errors in the browser, and build a separate deployment, is just not justified for what I need.

## Data Flow - How a Transport Request Moves Through the System

***The HTTP Request-Response Cycle***

Everything on the web operates on requests and responses. A browser makes a request, and a server sends back a response. This is the foundation of how web applications work.

HTTP is the protocol, which is the agreed-upon language that browsers and servers use to communicate.

- When a dispatcher clicks a sign transporter in the dashboard, the browser sends an HTTP request to the FastAPI server. FastAPI will process it, interact with the database, and return an HTTP response, which the browser will then display.
- Understanding this cycle is critical because the entire application is structured around it. Every endpoint I will write in FastAPI is a handler from one specific type of request at one specific URL.

How data will move through Vectris: The Complete Lifecycle

- Step 1: The browser will send a request.
- Step 2: FastAPI will route the request.
- Step 3: The route handler will call the service layer.
- Step 4: The service layer will query the database.
- Step 5: SQLAlchemy will send SQL to PostgreSQL.
- Step 6: SQLAlchemy will return Python objects.
- Step 7: The route handler will pass data to a Jinja2 template.
- Step 8: Jinja2 will render the HTML.
- Step 9: FastAPI will send the HTML response.
- Step 10: The browser will display the page.

## Frontend Architecture

***What the Frontend Is Not***:

- It is not a JavaScript application.
- There is no build step.

***What the Frontend Is***:

- A set of HTML template files that I will store in the frontend/ directory.
- When a route handler in a FastAPI responds to a request, it picks the appropriate template, injects data into it, and sends back complete HTML. The browser just receives and displays.

This means that the front end is tightly coupled to the back end, and they live in the same codebase. They run in the same processes, which is the monolith in practice.

What the Dashboard Must Show

- Active jobs in queue: *SELECT * FROM transport_requests WHERE status = 'active'*
- Transport staff on shift: *SELECT * FROM transporters*
- Transport staff currently on a task: *SELECT * FROM transporters WHERE status = 'on_job'* | I can also join against *request_assignment* to show which request each transporter is assigned to.

## Database Architecture

Why Relational?

- The data I will use has structure and relationships.
- A transport request is meaningless without knowing what a transporter is.
- An assignment is meaningless without knowing which request and which transporter it connects.
- These references are exactly what relational databases are designed to handle, and why I chose to use it for this project.
- Relational databases enforce referential integrity, which means I cannot create an assignment that references a transporter ID that does not exist.
- The database itself will prevent invalid states.
- This is not just a convenience but a guarantee, and the data will always be internally consistent.

The Three Tables

---

> transport_requests

- This is the unit of work.
- A row in this table represents one patient transport job.
- It has a life cycle:
`active -> in progress -> complete`

> transporters

- This is the staff roster.
- A row represents one human being who does transport work.
- They have an availability state.

> request_assignment

- This is the junction table. It exists because a single request might require two transporters. Every assignment is its own row, so you can have as many assignments per request as needed.

---

Foreign Keys and Why They Matter.

- A foreign key is a column in one table that references the primary key of another table.
- If I would try to insert an assignment with a *transport_request_id* that doesn't exist in *transport_requests*, PostgreSQL will reject it. This is the referential integrity guarantee.
- Without foreign keys, I could have orphaned assignments that reference deleted requests, which would be corrupted data.

## What This System Does Not Do (By Design)

Why This Section Exists

***Authentication***

- This is the system that verifies who you are.
- Login screens, passwords, sessions, tokens, this is all authentication.
- It is one of the most complex, security-sensitive areas of software engineering, and getting it wrong has real consequences.

Vectris does not implement authentication, and the reason is because it adds significant complexity that does not affect whether the three core workflows function.

My minimum viable product for this project is a proof of concept for a hospital environment where the dispatcher dashboard would be accessed on a secure internal network.

Real Time Updates

The dispatcher dashboard will be a page, and when it loads, it will show the data at that moment.

If a new transport request comes in two minutes later, the dashboard doesn't automatically update, but rather the dispatcher would have to refresh the page.

Real-time updates would require either web sockets or polling. Both add meaningful complexity and this project doesn't require those features to function and present to faculty.

## What is Pydantic?

Pydantic is a data validation library. It takes a class definition with typed fields, give it some raw data and it will either give you back a clean, validated Python object, or it raises an error telling you exactly what was wrong.

- FastAPI choses Pydantic as the validation engine because they share the same philosophy: use Python type hints to describe data, and enforce those description at runtime.

## Where does Pydantic live in the stack I chose for Vectris?

`Browser -> FastAPI (API layer) -> Pydantic validates input -> Service Layer -> SQLAlchemy -> PostgreSQL`

- Pydantic lives at the entry point of the API layer.
- Before the route handler does anything (call a service or touch the database) Pydantic has already checked that the incoming data is shaped correctly.

If the input is wrong, Pydantic stops the request and FastAPI returns a 422 Unprocessable Entity error automatically.

## Pydantic vs. SQLAlchemy

Purpose:

- SQLAlchemy represents a row in a database table
- Pydantic represents data coming in or going out of the API

Knows About:

- SQLAlchemy: columns, foreign keys, relationships
- Pydantic: fields, types, validation rules

Used when:

- SQLAlchemy: reading/writing to PostgreSQl
- Pydantic: validating HTTP request bodies, shaping HTTP responses

Created by:

- SQLAlchemy: itself when querying
- Pydantic: FastAPI when a request arrives

### Vectris Example form submission example

When a dispatcher submits a form to create a new transport request, this sequence happens (for reference):

1. FastAPI receives the JSON body and passes it to `TransportRequestCreate` (a Pydantic model). Pydantic validates the shape.
2. The service layer takes the validated data and creates a `TransportRequest` instance (a SQLAlchemy model).
3. SQLAlchemy writes that instance to PostgreSQL as a row in `Transport_requests`.
4. When you return data to the browser, you use another Pydantic model, `TransportRequestOut` to control exactly which fields are sent back. I don't want to accidentally serialize internal database state.

## When to use which model?

- Use a SQLAlchemy model when I need data to persist or to be read from the database. This is the data representation of a table row.
- Use a Pydantic model when I am receiving input from an HTTP request body, returning data as an API response or if I am validating any data structure at a boundary(input/output).

## File Section

### File `app/database/session.py`

What this file does:

- Creates the object that knows how to talk to the PostgreSQl database. It holds the connection URL and manages the connection pool.
- Creates a reusable template for opening database sessions. Each request gets its own session.
- Defines the `Base` which is the class that the SQLAlchemy models will inherit from. It's what connects the Python classes to the database.

This file is the foundation that the rest of Vectris will depend on.
The models import `Base` from here.
The dependency injection imports `SessionLocal` from here.

### File `app/models/transport_requests.py`

What this file does:

- This is the first SQLAlchemy file.
- It defines the `transport_requests` table as a Python class.
- Every column I designed in `entities.md` becomes a class attribute in this file.

### File `app/models/request_assignment.py`

What this file does:

- This file introduces a foreign key relationship.
- The `Foreign_key("transport_request.id")` tells SQLAlchemy that the column must match and reference a valid `id` in the `transport_requests` table.
- If that ID doesn't exist then the insert is rejected.

## File `__init__.py`

Python needs these files to treat folders as importable packages. Without them, when Alembic tries to import, the models will fail.

## File `transport_request.py`

This file provides two Pydantic models:

- An input schema (Create) which is what the caller sends in.
- An output schema (Out) which is what the API sends back.

If one schema was used for both requests, I could potentially expose fields I shouldn't or hide fields I would need to return.

Separate schemas let me explicitly control at each boundary.

## File `transport_request_service.py`

This file implements the business logic for transport requests. 

It enforces the status state machine (`active` -> `in_progress` -> `complete`), sets `completed_at` when a request is closed, and is the only place in the codebase that decides how a request changes state.
