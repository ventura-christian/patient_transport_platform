from fastapi import FastAPI
from app.api import transport_requests, transporters, assignments
from app.web import dashboard
from app.web import transport_requests as web_transport_requests
from app.web import assignments as web_assignments

# Create the FastAPI application instance.
app = FastAPI(
    title='Vectris',
    description='Hospital Patient Transport Operations Platform',
)

# Register each router with a URL prefix and a tag for the auto-generated docs.
app.include_router(
    transport_requests.router,
    prefix='/transport-requests',
    tags=['Transport Requests'],
)
app.include_router(
    transporters.router, prefix='/transporters', tags=['Transporters']
)
app.include_router(
    assignments.router, prefix='/assignments', tags=['Assignments']
)
app.include_router(dashboard.router)
app.include_router(web_transport_requests.router)
app.include_router(web_assignments.router)
