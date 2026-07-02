from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.transport_request import (
    TransportRequestCreate,
    TransportRequestOut,
)
from app.services import transport_request_service

router = APIRouter()


@router.post('/', response_model=TransportRequestOut)
def create_request(
    data: TransportRequestCreate, db: Session = Depends(get_db)
):
    return transport_request_service.create_request(db, data)


@router.get('/', response_model=list[TransportRequestOut])
def list_requests(db: Session = Depends(get_db)):
    return transport_request_service.get_all_requests(db)


@router.patch('/{request_id}/status', response_model=TransportRequestOut)
def update_request_status(
    request_id: int, new_status: str, db: Session = Depends(get_db)
):
    try:
        request = transport_request_service.update_status(
            db, request_id, new_status
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if request is None:
        raise HTTPException(
            status_code=404, detail='Transport request not found'
        )

    return request
