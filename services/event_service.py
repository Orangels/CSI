from typing import List, Optional
from sqlmodel import Session, select,func
from models.event_record import eventRecord, eventRecordCreat, eventRecordUpdate
from models.camera import Camera
from database import engine
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import desc
import time
import random


class eventBody(BaseModel):
    camera_id: str
    start_time: int
    finish_time: int
    offset: int | None = 10
    limit: int | None = 10


class event_page_result(BaseModel):
    total: int
    current: int
    page_size: int
    events: List[eventRecord]


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
            statement = (
                select(eventRecord)
                .where(
                    eventRecord.time >= start_time,
                    eventRecord.time < finish_time,
                    eventRecord.Camera_id == camera_id,
                )
                .offset(offset)
                .limit(limit)
            )
            results = session.exec(statement)
            if len(results.all()) == 0:
                raise HTTPException(status_code=404, detail="Event not found")
            return results.all()

    def get_all(self, count=10) -> List[eventRecord]:
        with Session(engine) as session:
            statement = (
                select(eventRecord).order_by(desc(eventRecord.time)).limit(count)
            )
            results = session.exec(statement)
            data = results.all()
            if len(data) == 0:
                return []
            return data

    # 每个摄像头获取最多{count}条event live界面使用
    def get_each_camera_limit(self, count=10) -> List[eventRecord]:
        with Session(engine) as session:
            statement = select(Camera)
            cameras = session.exec(statement).all()
            all_events: List[eventRecord] = []
            for camera in cameras:
                statement = (
                    select(eventRecord)
                    .where(eventRecord.Camera_id == camera.Camera_id)
                    .order_by(desc(eventRecord.time))
                    .limit(count)
                )
                events = session.exec(statement).all()
                all_events.extend(events)
            return all_events

    def get_paging_events(
        self, current: int, page_size: int, start_time: int, end_time: int
    ) -> event_page_result:
        with Session(engine) as session:
            total_statement = select(func.count()).select_from(eventRecord).where(eventRecord.time >= start_time, eventRecord.time <= end_time)
            total = session.exec(total_statement).scalar()

            statement = (
                select(eventRecord)
                .where(eventRecord.time >= start_time, eventRecord.time <= end_time)
                .offset((current - 1) * page_size)
                .limit(page_size)
                .order_by(desc(eventRecord.id))
            )
            results = session.exec(statement)
            events = results.all()

            return event_page_result(
                total=total,
                current=current,
                page_size=page_size,
                events=events,
            )

    def get_event_by_time(self, start_time, end_time)-> List[eventRecord]:
        with Session(engine) as session:
            statement = (
                select(eventRecord)
                .where(eventRecord.time >= start_time, eventRecord.time <= end_time)
                .order_by(desc(eventRecord.id))
            )
            results = session.exec(statement)
            events = results.all()
            return events

    def generate_random_events(self, count: int = 5) -> bool:
        with Session(engine) as session:
            cameras: List[Camera] = session.query(Camera).all()
            for camera in cameras:
                for i in range(count):
                    t = int(time.time()) - random.randint(0, 86400) * i
                    a = "区域" + str(random.randint(1, count))
                    event = random.choice(
                        [
                            "人员核查",
                            "电子围栏",
                            "安全帽检测",
                            "跌倒检测",
                            "烟火检测",
                            "积水检测",
                            "设备状态检测",
                            "反光衣检测",
                            "打架检测",
                            "抽烟检测",
                        ]
                    )
                    event_data = eventRecordCreat(
                        Camera_id=camera.Camera_id,
                        area=a,
                        event=event,
                        time=t,
                        image="images/event" + str(random.randint(1, 4)) + ".jpg",
                        is_upload=True,
                    )
                    new_event = eventRecord(**event_data.dict())
                    session.add(new_event)
            session.commit()
        return True
