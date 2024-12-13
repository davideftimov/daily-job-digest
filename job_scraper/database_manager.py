
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class Comment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    time: int
    text: str
    filter: bool
    source: str  # To track which platform the job came from
    url: str

class DatabaseManager:
    def __init__(self, sqlite_file_name="database.db"):
        self.sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(self.sqlite_url)
        self.create_tables()

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def save_comment(self, comment_id: int, time: int, text: str, filter: bool, source: str, url: str):
        with Session(self.engine) as session:
            comment = Comment(id=comment_id, time=time, text=text, filter=filter, source=source, url=url)
            session.add(comment)
            session.commit()

    def get_max_comment_id(self, source: str) -> int:
        with Session(self.engine) as session:
            max_id = session.exec(
                select(Comment)
                .where(Comment.source == source)
                .order_by(Comment.id.desc())
            ).first()
            return max_id.id if max_id is not None else 0