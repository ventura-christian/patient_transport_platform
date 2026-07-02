from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.transport_request import TransportRequestCreate
from app.services import transport_request_service
from app.services import (
    transport_request_service,
    transporter_service,
    assignment_service,
)

router = APIRouter()

templates = Jinja2Templates(directory='frontend/templates')

# Hardcoded department list. The database column is free text (see
# decisions.md); this list only exists to keep data entry consistent.
DEPARTMENTS = [
    'Emergency',
    'ICU',
    'Medical-Surgical',
    'Radiology',
    'Surgery',
    'Oncology',
    'Cardiology',
    'Discharge',
]

EQUIPMENT_OPTIONS = [
    'Wheelchair',
    'Stretcher',
    'Portable Oxygen',
]


@router.get('/create-request')
def show_create_request_form(request: Request):
    context = {
        'departments': DEPARTMENTS,
        'equipment_options': EQUIPMENT_OPTIONS,
    }
    return templates.TemplateResponse(request, 'create_request.html', context)


@router.post('/create-request')
def submit_create_request(
    patient_name: str = Form(...),
    origin_department: str = Form(...),
    origin_room: str = Form(...),
    destination_department: str = Form(...),
    equipment_needed: str = Form(''),
    biohazard: bool = Form(False),
    transporters_required: int = Form(1),
    db: Session = Depends(get_db),
):
    # HTML forms send "" for an unselected dropdown, not None.
    # The schema/database expect None, so convert it here.
    cleaned_equipment = equipment_needed or None

    data = TransportRequestCreate(
        patient_name=patient_name,
        origin_department=origin_department,
        origin_room=origin_room,
        destination_department=destination_department,
        equipment_needed=cleaned_equipment,
        biohazard=biohazard,
        transporters_required=transporters_required,
    )
    transport_request_service.create_request(db, data)

    # 303 tells the browser to re-fetch with GET, so a page refresh
    # afterward doesn't resubmit the form and duplicate the request.
    return RedirectResponse(url='/dashboard', status_code=303)


@router.get('/requests/{request_id}')
def show_job_detail(
    request_id: int, request: Request, db: Session = Depends(get_db)
):
    transport_request = transport_request_service.get_request_by_id(
        db, request_id
    )

    assigned_transporters = []
    if transport_request is not None:
        assignments = assignment_service.get_assignments_for_request(
            db, request_id
        )
        all_transporters = transporter_service.get_all_transporters(db)
        for a in assignments:
            for t in all_transporters:
                if t.id == a.transporter_id:
                    assigned_transporters.append(t)

    context = {
        'transport_request': transport_request,
        'assigned_transporters': assigned_transporters,
    }
    return templates.TemplateResponse(request, 'job_detail.html', context)


@router.post('/requests/{request_id}/complete')
def complete_request(
    request_id: int, request: Request, db: Session = Depends(get_db)
):
    try:
        transport_request_service.update_status(db, request_id, 'complete')
    except ValueError as e:
        transport_request = transport_request_service.get_request_by_id(
            db, request_id
        )
        assigned_transporters = []
        if transport_request is not None:
            assignments = assignment_service.get_assignments_for_request(
                db, request_id
            )
            all_transporters = transporter_service.get_all_transporters(db)
            for a in assignments:
                for t in all_transporters:
                    if t.id == a.transporter_id:
                        assigned_transporters.append(t)
        context = {
            'transport_request': transport_request,
            'assigned_transporters': assigned_transporters,
            'error': str(e),
        }
        return templates.TemplateResponse(request, 'job_detail.html', context)

    return RedirectResponse(url='/dashboard', status_code=303)
