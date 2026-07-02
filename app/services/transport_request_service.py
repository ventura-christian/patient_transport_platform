from sqlalchemy.orm import Session
from app.models.transport_request import TransportRequest
from app.schemas.transport_request import TransportRequestCreate
from app.models.request_assignment import RequestAssignment
from app.models.transporter import Transporter
from typing import Optional


VALID_TRANSITIONS = {
    'active': 'in_progress',
    'in_progress': 'complete',
}


def create_request(
    db: Session, data: TransportRequestCreate
) -> TransportRequest:
    # Creates a new SQLAlchemy model instance
    # from the validated Pydantic input.
    request = TransportRequest(
        patient_name=data.patient_name,
        origin_department=data.origin_department,
        origin_room=data.origin_room,
        destination_department=data.destination_department,
        equipment_needed=data.equipment_needed,
        biohazard=data.biohazard,
        transporters_required=data.transporters_required,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def get_request_by_id(
    db: Session, request_id: int
) -> Optional[TransportRequest]:
    # Look up a single request by id. Returns None if it doesn't
    # exist so the caller can decide how to handle that.
    return (
        db.query(TransportRequest)
        .filter(TransportRequest.id == request_id)
        .first()
    )


def update_status(
    db: Session, request_id: int, new_status: str
) -> Optional[TransportRequest]:
    # Find the request or return None if it doesn't exist.
    request = (
        db.query(TransportRequest)
        .filter(TransportRequest.id == request_id)
        .first()
    )

    if request is None:
        return None

    # Enforce that the status can only move to its valid next state.
    if VALID_TRANSITIONS.get(request.status) != new_status:
        raise ValueError(
            f"Cannot transition from '{request.status}' to '{new_status}'"
        )

    # A request can't be marked complete until it has the number of
    # transporters it originally asked for.
    if new_status == 'complete':
        assignment_count = (
            db.query(RequestAssignment)
            .filter(RequestAssignment.transport_request_id == request_id)
            .count()
        )
        if assignment_count < request.transporters_required:
            raise ValueError(
                f'Request {request_id} needs {request.transporters_required} '
                f'transporter(s) but only has {assignment_count} assigned.'
            )

    request.status = new_status

    # If completing the request, record when it finished
    if new_status == 'complete':
        from datetime import datetime, timezone

        request.completed_at = datetime.now(timezone.utc)

        # Free up every transporter who was assigned to this request.
        assignments = (
            db.query(RequestAssignment)
            .filter(RequestAssignment.transport_request_id == request_id)
            .all()
        )
        for assignment in assignments:
            transporter = (
                db.query(Transporter)
                .filter(Transporter.id == assignment.transporter_id)
                .first()
            )
            if transporter is not None:
                transporter.status = 'available'

    db.commit()
    db.refresh(request)
    return request


def get_all_requests(db: Session) -> list[TransportRequest]:
    # Return every row in the transport_requests table.
    return db.query(TransportRequest).all()
