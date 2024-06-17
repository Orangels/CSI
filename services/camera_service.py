from typing import List, Optional
from sqlmodel import Session, select
from models.camera import Camera, CameraCreat, CameraUpdate
from database import engine
from services.area_service import AreaService
from fastapi import HTTPException
from pydantic import BaseModel


class CameraService:

    def create_camera(self, camera: CameraCreat) -> Camera:
        new_camera = Camera(**camera.dict())
        with Session(engine) as session:
            session.add(new_camera)
            session.commit()
            session.refresh(new_camera)
        return new_camera

    def get_all_cameras(self) -> List[Camera]:
        with Session(engine) as session:
            return session.query(Camera).all()


    def delete_camera(self, Camera_id: int) -> bool:
        with Session(engine) as session:
            camera = session.get(Camera, Camera_id)
            if camera:
                session.delete(camera)
                session.commit()
                # TODO  return
        area_service = AreaService()
        area_service.delete_area_by_camera_id(Camera_id)
