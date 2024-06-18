from typing import List, Optional
from sqlmodel import Session, select
from models.event_type import EventType
from database import engine
from fastapi import HTTPException
from pydantic import BaseModel


class EventService:

    def get_all_event_type(self) -> List[EventType]:
        with Session(engine) as session:
            return session.query(EventType).all()
