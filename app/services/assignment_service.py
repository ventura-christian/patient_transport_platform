from sqlalchemy.orm import Session
from app.models.transport_request import TransportRequest
from app.models.transporter import Transporter
from app.models.request_assignment import RequestAssignment
from typing import Optional


def create_assignment(
    db: Session, request_id: int, transporter_id: int
) -> RequestAssignment:
    # Fetch the transport request.
    request = (
        db.query(TransportRequest)
        .filter(TransportRequest.id == request_id)
        .first()
    )

    # Fetch the transporter.
    transporter = (
        db.query(Transporter).filter(Transporter.id == transporter_id).first()
    )

    # Reject if either doesn't exist.
    if request is None:
        raise ValueError(f'Transport request {request_id} not found.')

    if transporter is None:
        raise ValueError(f'Transporter {transporter_id} not found.')

    # A request can receive assignments while active or already in
    # progress. Complete requests are closed to new assignments.
    if request.status not in ('active', 'in_progress'):
        raise ValueError(
            f'Request {request_id} is {request.status} and cannot be assigned.'
        )

    # Don't allow more transporters than the request actually needs.
    current_assignment_count = (
        db.query(RequestAssignment)
        .filter(RequestAssignment.transport_request_id == request_id)
        .count()
    )
    if current_assignment_count >= request.transporters_required:
        raise ValueError(
            f'Request {request_id} '
            'already has all required transporters assigned.'
        )

    # Reject if the transporter isn't available.
    if transporter.status != 'available':
        raise ValueError(f'Transporter {transporter_id} is not available.')

    # Create the assignment row.
    assignment = RequestAssignment(
        transport_request_id=request_id,
        transporter_id=transporter_id,
    )
    db.add(assignment)

    # Update bot statuses to reflect the new state.
    request.status = 'in_progress'
    transporter.status = 'on_job'

    db.commit()
    db.refresh(assignment)
    return assignment


def get_assignments_for_request(
    db: Session, request_id: int
) -> list[RequestAssignment]:
    # Return all assignment rows for a given request.
    return (
        db.query(RequestAssignment)
        .filter(RequestAssignment.transport_request_id == request_id)
        .all()
    )
