from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.transport_request import TransportRequestCreate
from app.services import transport_request_service

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
