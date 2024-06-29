from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status,Request
from models.camera import Camera, CameraCreat, CameraUpdate
from services.camera_service import CameraService, CameraBody
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import requests

router = APIRouter()


def get_local_service():
    return CameraService()


@router.post(
    "/api/device/cameras", response_model=List[Camera], status_code=status.HTTP_200_OK
)
def get_all_cameras(camera_service: CameraService = Depends(get_local_service)):
    return camera_service.get_all_cameras()


@router.post(
    "/api/device/creatCamera",
    response_model=Camera,
    status_code=status.HTTP_201_CREATED,
)
def creat_cameras(
    camera: CameraCreat, camera_service: CameraService = Depends(get_local_service)
):
    # TODO MQTT client
    new_camera = camera_service.create_camera(camera)
    add_zlm_stream_sroxy(new_camera)
    # TODO 判断数据库是否更新成功，返回camera状态，再添加推流 
    return new_camera


@router.post("/api/device/deleteCamera", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(
    camera_id: int, camera_service: CameraService = Depends(get_local_service)
):
    camera_service.delete_camera(camera_id)
    # TODO MQTT client

    del_zlm_stream_sroxy(camera_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/api/device/updateCamera", response_model=Camera, status_code=status.HTTP_200_OK
)
def update_camera_by_id(
    camera_id: int,
    camera_update: CameraUpdate,
    camera_service: CameraService = Depends(get_local_service),
):
    origin_camera = camera_service.get_camera_by_id(camera_id)


    updated_camera = camera_service.update_camera(camera_id, camera_update)
    if updated_camera is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if origin_camera.Camera_addr != updated_camera.Camera_addr:
        del_zlm_stream_sroxy(camera_id)
        add_zlm_stream_sroxy(updated_camera)

    # TODO MQTT client
    return updated_camera

STREAM_SERVER_PORT = 8005
STREAM_SERVER_SECRET="9AfMK3utUmoWGFybU58ncrgCTt42cMtX"
def add_zlm_stream_sroxy(camera:Camera):
    #实际播放地址为ws/http ://127.0.0.1:8005/camera/{Camera_id}.live.flv
    url = f"http://127.0.0.1:{STREAM_SERVER_PORT}/index/api/addStreamProxy?secret={STREAM_SERVER_SECRET}&vhost=__defaultVhost__&app=camera&stream={camera.Camera_id}&enable_rtmp=1&url={camera.Camera_addr}"
    response = requests.request("GET", url)
    print(response.text)

def del_zlm_stream_sroxy(camera_id):
    url = f"http://127.0.0.1:{STREAM_SERVER_PORT}/index/api/delStreamProxy?secret={STREAM_SERVER_SECRET}&key=__defaultVhost__/camera/{camera_id}"
    response = requests.request("GET", url)
    print(response.text)

def sync_zlm_stream_proxy(camera_service: CameraService = Depends(get_local_service)):
    url = f"http://127.0.0.1:{STREAM_SERVER_PORT}/index/api/getMediaList?secret={STREAM_SERVER_SECRET}"
    response = requests.request("GET", url)
    if response.status_code == 200:
        try:
            response_data = response.json()
            server_proxy_data = response_data.get('data', [])
            server_streams = {camera.get('stream') for camera in server_proxy_data}
            cameras = camera_service.get_all_cameras()
            local_camera_ids = {camera['id'] for camera in cameras}

            cameras_to_delete = server_streams - local_camera_ids
            for camera_id in cameras_to_delete:
                del_zlm_stream_sroxy(camera_id)

            cameras_to_add = local_camera_ids - server_streams
            for camera_id in cameras_to_add:
                camera = next((camera for camera in cameras if camera.Camera_id == camera_id), None)
                if camera:
                    add_zlm_stream_sroxy(camera)
        except Exception as e:
            print(f"Error syncing stream proxy: {e}")
