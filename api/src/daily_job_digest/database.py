from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select


sqlite_file_name = "../../database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Job(SQLModel, table=True):
    id: str = Field(primary_key=True)
    time: int
    time_scraped: int
    text: str
    filter: bool
    source: str
    url: str
    title: str = Field(default=None)
    location: str = Field(default=None)
    hn_id: int = Field(default=None)
    company: str = Field(default=None)
    viewed: bool = Field(default=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]