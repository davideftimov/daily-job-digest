
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class Job(SQLModel, table=True):
    id: int = Field(primary_key=True)
    time: int
    text: str
    filter: bool
    source: str  # To track which platform the job came from
    url: str
    title: str | None = None
    location: str | None = None

class DatabaseManager:
    def __init__(self, sqlite_file_name="database.db"):
        self.sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(self.sqlite_url)
        self.create_tables()

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def save_job(self, job: Job):
        with Session(self.engine) as session:
            session.add(job)
            session.commit()

    def get_max_job_id(self, source: str) -> int:
        with Session(self.engine) as session:
            max_id = session.exec(
                select(Job)
                .where(Job.source == source)
                .order_by(Job.id.desc())
            ).first()
            return max_id.id if max_id is not None else 0