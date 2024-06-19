from sqlmodel import SQLModel, Field, Relationship
from models.area import Area


class CameraBase(SQLModel):
    Camera_addr: str  # rtsp 地址
    frame_height: int
    frame_width: int
    MAC: str
    name: str | None
    description: str | None
    state: int = 1  # 1在线, 0 不在线
    areas: list["Area"] = Relationship(back_populates="area")


class Camera(CameraBase, table=True):
    Camera_id: int | None = Field(default=None, primary_key=True)


class CameraCreat(CameraBase):
    pass


class CameraUpdate(CameraBase):
    Camera_addr: str | None = None  # rtsp 地址
    frame_height: int | None = None
    frame_width: int | None = None
    MAC: str | None = None
    name: str | None
    description: str | None
    state: int = 1  # 1在线, 0 不在线

