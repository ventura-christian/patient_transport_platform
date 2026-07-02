from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import (
    transport_request_service,
    transporter_service,
    assignment_service,
)

router = APIRouter()

templates = Jinja2Templates(directory='frontend/templates')


@router.get('/assign/{request_id}')
def show_assign_form(
    request_id: int, request: Request, db: Session = Depends(get_db)
):
    transport_request = transport_request_service.get_request_by_id(
        db, request_id
    )
    all_transporters = transporter_service.get_all_transporters(db)
    available_transporters = [
        t for t in all_transporters if t.status == 'available'
    ]

    context = {
        'transport_request': transport_request,
        'available_transporters': available_transporters,
    }
    return templates.TemplateResponse(request, 'assign.html', context)


@router.post('/assign/{request_id}')
def submit_assignment(
    request_id: int,
    request: Request,
    transporter_id: int = Form(...),
    db: Session = Depends(get_db),
):
    try:
        assignment_service.create_assignment(db, request_id, transporter_id)
    except ValueError as e:
        # Something changed between loading the page and submitting
        # (request no longer active, transporter no longer available).
        # Re-show the same screen with an error instead of crashing.
        transport_request = transport_request_service.get_request_by_id(
            db, request_id
        )
        all_transporters = transporter_service.get_all_transporters(db)
        available_transporters = [
            t for t in all_transporters if t.status == 'available'
        ]
        context = {
            'transport_request': transport_request,
            'available_transporters': available_transporters,
            'error': str(e),
        }
        return templates.TemplateResponse(request, 'assign.html', context)

    return RedirectResponse(url='/dashboard', status_code=303)
