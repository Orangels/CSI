from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.event_record import eventRecord, eventRecordCreat, eventRecordUpdate
from services.event_service import EventService, eventBody

router = APIRouter()


def get_local_service():
    return EventService()


@router.post("/api/device/CreatEvents", response_model=eventRecord, status_code=status.HTTP_201_CREATED)
def creat_events(event: eventRecordCreat, event_service: EventService = Depends(get_local_service)):
    return event_service.create_event(event)


@router.post("/api/device/events", response_model=List[eventRecord], status_code=status.HTTP_200_OK)
def query_events(event: eventBody, event_service: EventService = Depends(get_local_service)):
    return event_service.get_event_by_camera_id_timestamp(event)


@router.post("/api/device/allevents", response_model=List[eventRecord], status_code=status.HTTP_200_OK)
def query_events(event_service: EventService = Depends(get_local_service)):
    return event_service.get_all()