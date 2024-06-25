from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.camera import Camera, CameraCreat, CameraUpdate
from services.camera_service import CameraService, CameraBody
from fastapi.responses import JSONResponse

router = APIRouter()


def get_local_service():
    return CameraService()


@router.post("/api/device/cameras", response_model=List[Camera],
             status_code=status.HTTP_200_OK)
def get_all_cameras(camera_service: CameraService = Depends(get_local_service)):
    return camera_service.get_all_cameras()


@router.post("/api/device/creatCamera", response_model=Camera,
             status_code=status.HTTP_201_CREATED)
def creat_cameras(camera: CameraCreat,
                  camera_service: CameraService = Depends(get_local_service)):
    #TODO MQTT client
    return camera_service.create_camera(camera)


@router.post("/api/device/deleteCamera",
             status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(camera_id: int,
                  camera_service: CameraService = Depends(get_local_service)):
    camera_service.delete_camera(camera_id)
    # TODO MQTT client
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/api/device/updateCamera", response_model=Camera,
             status_code=status.HTTP_200_OK)
def update_camera_by_id(camera_id: int, camera_update: CameraUpdate,
                      camera_service: CameraService = Depends(get_local_service)):
    updated_camera = camera_service.update_camera(camera_id, camera_update)
    if updated_camera is None:
        raise HTTPException(status_code=404, detail="User not found")
    # TODO MQTT client
    return updated_camera
