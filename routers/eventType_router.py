from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.event_type import EventType
from services.eventType_service import EventService
from fastapi.responses import JSONResponse

router = APIRouter()


def get_local_service():
    return EventService()


@router.post("/api/device/eventTypes", response_model=List[EventType],
             status_code=status.HTTP_200_OK)
def get_all_eventTypes(camera_service: EventService = Depends(get_local_service)):
    return camera_service.get_all_event_type()

