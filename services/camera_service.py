from typing import List, Optional
from sqlmodel import Session, select
from models.camera import Camera, CameraCreat, CameraUpdate
from models.area import Area
from database import engine
from services.area_service import AreaService
from fastapi import HTTPException
from pydantic import BaseModel
import time


class CameraBody(BaseModel):
    Camera_addr: str  # rtsp 地址
    frame_height: int
    frame_width: int
    MAC: str
    name: str | None
    description: str | None
    state: int = 1  # 1在线, 0 不在线
    Camera_id: int
    areas: List[Area] = []


class CameraService:

    def create_camera(self, camera: CameraCreat) -> Camera:
        new_camera = Camera(**camera.dict())
        new_camera.time = int(time.time())
        with Session(engine) as session:
            session.add(new_camera)
            session.commit()
            session.refresh(new_camera)
        return new_camera


    def get_all_cameras(self) -> List[Camera]:
        with Session(engine) as session:
            cameras = session.query(Camera).all()
            return cameras


    # def get_all_cameras(self) -> List[CameraBody]:
    #     resp = []
    #     merged_data = dict()
    #     with Session(engine) as session:
    #         statement = select(Camera, Area).join(Area, isouter=True)
    #         results = session.exec(statement).all()
    #         for camera, area in results:
    #             camera_resp = CameraBody(**camera.dict())
    #             if area is not None:
    #                 camera_resp.areas.append(area)
    #             merged_data[camera_resp.Camera_id] = camera_resp
    #             resp.append(camera_resp)
    #
    #     for item in resp:
    #         if len(item.areas) > 0:
    #             if item.areas[0].id != merged_data[item.Camera_id].areas[0].id:
    #                 merged_data[item.Camera_id].areas.append(item.areas[0])
    #     return list(merged_data.values())

    def delete_camera(self, Camera_id: int) -> bool:
        with Session(engine) as session:
            camera = session.get(Camera, Camera_id)
            if camera:
                session.delete(camera)
                session.commit()
                # TODO  return
        # TODO 同一事务
        area_service = AreaService()
        area_service.delete_area_by_camera_id(Camera_id)

    def update_camera(self, camera_id: int,
                      camera_update: CameraUpdate) -> Camera:
        with Session(engine) as session:
            camera = session.get(Camera, camera_id)
            if not camera:
                raise HTTPException(status_code=404, detail="Area not found")
            for var, value in camera_update.dict(exclude_unset=True).items():
                setattr(camera, var,
                        value if value is not None else getattr(camera, var))
            camera.time = int(time.time())
            session.commit()
            session.refresh(camera)
            return camera

    def get_camera_by_id(self, Camera_id: int) -> Optional[Camera]:
        with Session(engine) as session:
            camera = session.get(Camera, Camera_id)
            return camera
    
    