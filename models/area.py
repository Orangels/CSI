from sqlmodel import SQLModel, Field, Relationship
import time

class AreaBase(SQLModel):
    name: str
    area_coordinate: str  # splice ;
    event_type: str  # splice ;
    area_type: int = 0  # 0: 多边形
    time: int | None = int(time.time())  # 秒级时间戳 (更新时间)
    Camera_id: int = Field(default=None, foreign_key="camera.Camera_id")


class Area(AreaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class AreaCreat(AreaBase):
    pass


class AreaUpdate(AreaBase):
    area_coordinate: str | None = None  # splice ;
    name: str | None = None
    event_type: int | None = None  # splice ;
    area_type: str | None = 0  # 0: 多边形
    time: int | None = int(time.time())  # 秒级时间戳 (更新时间)