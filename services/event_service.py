from typing import List, Optional
from sqlmodel import Session, select
from models.event_record import eventRecord, eventRecordCreat, eventRecordUpdate
from database import engine
from fastapi import HTTPException
from pydantic import BaseModel


class eventBody(BaseModel):
    camera_id: str
    start_time: int
    finish_time: int
    offset: int | None = 10
    limit: int | None = 10


class EventService:

    def create_event(self, event_data: eventRecordCreat) -> eventRecord:
        new_event = eventRecord(**event_data.dict())
        with Session(engine) as session:
            session.add(new_event)
            session.commit()
            session.refresh(new_event)
        return new_event

    def get_event_by_camera_id_timestamp(self, v_event: eventBody) -> List[eventRecord]:
        camera_id, start_time, finish_time, offset, limit = v_event.dict().values()
        with Session(engine) as session:
            statement = select(eventRecord).where(
                eventRecord.time >= start_time,
                eventRecord.time < finish_time,
                eventRecord.Camera_id == camera_id).offset(offset).limit(limit)
            results = session.exec(statement)
            if len(results.all()) == 0:
                raise HTTPException(status_code=404, detail="Event not found")
            return results.all()

    def get_all(self) -> List[eventRecord]:
        with Session(engine) as session:
            statement = select(eventRecord).limit(10)
            results = session.exec(statement)
            data = results.all()
            if len(data) == 0:
                return []
            return data