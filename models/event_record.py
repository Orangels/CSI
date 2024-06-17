from sqlmodel import SQLModel, Field


class eventRecordBase(SQLModel):
    __tablename__ = "event_record"

    Camera_id: int
    area: str  # area 名称
    event: str
    time: int  # 秒级时间戳
    image: str  # base64 图片
    is_upload: bool  # 0: 未上传, 1: 已上传


class eventRecord(eventRecordBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class eventRecordCreat(eventRecordBase):
    pass


class eventRecordUpdate(eventRecordBase):
    Camera_id: int | None = None
    area: str | None = None  # area 名称
    event: str | None = None
    image: str | None = None  # base64 图片
    is_upload: bool | None = None  # 0: 未上传, 1: 已上传
