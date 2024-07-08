from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.event_record import eventRecord, eventRecordCreat, eventRecordUpdate
from services.event_service import EventService, eventBody,event_page_result
import time
router = APIRouter()


def get_local_service():
    return EventService()


@router.post("/api/device/CreatEvents", response_model=eventRecord, status_code=status.HTTP_201_CREATED)
def creat_events(event: eventRecordCreat, event_service: EventService = Depends(get_local_service)):
    return event_service.create_event(event)


@router.post("/api/device/events", response_model=List[eventRecord], status_code=status.HTTP_200_OK)
def query_events(event: eventBody, event_service: EventService = Depends(get_local_service)):
    return event_service.get_event_by_camera_id_timestamp(event)


@router.post("/api/device/allevents",response_model=List[eventRecord], status_code=status.HTTP_200_OK)
def query_events(limit: int=10, event_service: EventService = Depends(get_local_service)):
    return event_service.get_all(limit)


def get_events_by_camera_id(camera_id: int, event_service: EventService = Depends(get_local_service)):
    return event_service.get_event_by_camera_id(camera_id)


@router.post("/api/device/liveevents", response_model=List[eventRecord], status_code=status.HTTP_200_OK)
def get_each_camera_limit(limit: int, event_service: EventService = Depends(get_local_service)):
    return event_service.get_each_camera_limit(limit)

@router.post("/api/device/pagingevents", response_model=event_page_result, status_code=status.HTTP_200_OK)
def get_paging_events(start_time:int,end_time:int=int(time.time()),current_page:int=1, page_size:int=15, event_service: EventService = Depends(get_local_service)):
    return event_service.get_paging_events(current_page,page_size,start_time,end_time)

@router.post("/api/device/timeevents", response_model=List[eventRecord], status_code=status.HTTP_200_OK)
def get_event_by_time(start_time: int, end_time: int, event_service: EventService = Depends(get_local_service)):
    return event_service.get_event_by_time(start_time, end_time)

@router.get("/api/device/genevents", response_model=bool, status_code=status.HTTP_200_OK)
def generate_random_events(count: int = 10, event_service: EventService = Depends(get_local_service)):
    return event_service.generate_random_events(count)
