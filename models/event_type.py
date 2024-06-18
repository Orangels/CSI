from sqlmodel import SQLModel, Field


class EventTypeBase(SQLModel):
    name: str
    type_id: int
    authority_level: int  # 0-9 使用 10-19 定制 20-29 附加
    description: str | None


class EventType(EventTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


