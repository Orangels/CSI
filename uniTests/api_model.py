from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] | None = Relationship(back_populates="team")