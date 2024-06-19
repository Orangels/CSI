from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.area import Area, AreaCreat, AreaUpdate
from services.area_service import AreaService
from fastapi.responses import JSONResponse

router = APIRouter()


def get_local_service():
    return AreaService()


@router.post("/api/device/areas", response_model=List[Area],
             status_code=status.HTTP_200_OK)
def get_all_areas(area_service: AreaService = Depends(get_local_service)):
    return area_service.get_all_areas()


@router.post("/api/device/creatArea", response_model=Area,
             status_code=status.HTTP_201_CREATED)
def creat_areas(area: AreaCreat,
                area_service: AreaService = Depends(get_local_service)):
    # TODO MQTT client
    return area_service.create_area(area)


@router.post("/api/device/deleteCameraAreas",
             status_code=status.HTTP_204_NO_CONTENT)
def delete_area_by_camera_id(camera_id: int,
                             area_service: AreaService = Depends(
                                 get_local_service)):
    area_service.delete_area_by_camera_id(camera_id)
    # TODO MQTT client
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/api/device/deleteArea",
             status_code=status.HTTP_204_NO_CONTENT)
def delete_area_by_id(area_id: int,
                      area_service: AreaService = Depends(get_local_service)):
    area_service.delete_area(area_id)
    # TODO MQTT client
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/api/device/updateArea", response_model=Area,
             status_code=status.HTTP_200_OK)
def update_area_by_id(area_id: int, area_update: AreaUpdate,
                      area_service: AreaService = Depends(get_local_service)):
    updated_area = area_service.update_area(area_id, area_update)
    if updated_area is None:
        raise HTTPException(status_code=404, detail="User not found")
    # TODO MQTT client
    return updated_area
