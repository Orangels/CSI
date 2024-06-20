import time
from typing import List, Optional
from sqlmodel import Session, select, delete
from models.area import Area, AreaCreat, AreaUpdate
from database import engine
from fastapi import HTTPException
from pydantic import BaseModel


class AreaService:

    def create_area(self, area: AreaCreat) -> Area:
        new_area = Area(**area.dict())
        with Session(engine) as session:
            session.add(new_area)
            session.commit()
            session.refresh(new_area)
        return new_area

    def get_all_areas(self) -> List[Area]:
        with Session(engine) as session:
            return session.query(Area).all()


    def get_area_by_id(self, area_id: int) -> Area:
        with Session(engine) as session:
            area = session.get(Area, area_id)
            if not area:
                raise HTTPException(status_code=404, detail="Area not found")
            return area


    def get_area_by_camera_id(self, camera_id: int) -> List[Area]:
        with Session(engine) as session:
            statement = select(Area).where(Area.Camera_id == camera_id)
            results = session.exec(statement)
            if len(results.all()) == 0:
                raise HTTPException(status_code=404, detail="Area not found")
            return results.all()


    def delete_area_by_camera_id(self, camera_id: int) -> List[Area] | None:
        with Session(engine) as session:
            statement = delete(Area).where(Area.Camera_id == camera_id)
            results = session.exec(statement)
            session.commit()



    def delete_area(self, area_id: int) -> bool:
        with Session(engine) as session:
            area = session.get(Area, area_id)
            if area:
                session.delete(area)
                session.commit()
                # TODO  return


    def update_area(self, area_id: int, area_update: AreaUpdate) -> Area:
        with Session(engine) as session:
            area = session.get(Area, area_id)
            if not area:
                raise HTTPException(status_code=404, detail="Area not found")
            for var, value in area_update.dict(exclude_unset=True).items():
                setattr(area, var, value if value is not None else getattr(area, var))
            area.time = int(time.time())
            session.commit()
            session.refresh(area)
            return area
