from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import transport_request_service, transporter_service

router = APIRouter()

templates = Jinja2Templates(directory='frontend/templates')


@router.get('/dashboard')
def show_dashboard(request: Request, db: Session = Depends(get_db)):
    all_requests = transport_request_service.get_all_requests(db)
    all_transporters = transporter_service.get_all_transporters(db)

    # Split the single request list into the two queue sections
    # the dashboard needs to show separately.
    active_requests = [r for r in all_requests if r.status == 'active']
    in_progress_requests = [
        r for r in all_requests if r.status == 'in_progress'
    ]

    context = {
        'active_requests': active_requests,
        'in_progress_requests': in_progress_requests,
        'transporters': all_transporters,
        'waiting_count': len(active_requests),
        'in_progress_count': len(in_progress_requests),
        'available_count': len(
            [t for t in all_transporters if t.status == 'available']
        ),
    }
    return templates.TemplateResponse(request, 'dashboard.html', context)
