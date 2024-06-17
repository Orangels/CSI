from sqlmodel import SQLModel, Field


class AreaBase(SQLModel):
    Camera_id: int  #
    name: str
    area_coordinate: str  # splice ;
    event_type: str  # splice ;
    area_type: int = 0  # 0: 多边形
    time: int  # 秒级时间戳 (更新时间)


class Area(AreaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class AreaCreat(AreaBase):
    pass


class AreaUpdate(AreaBase):
    area_coordinate: str | None = None  # splice ;
    name: str | None = None
    event_type: str | None = None  # splice ;
    area_type: str | None = 0  # 0: 多边形
