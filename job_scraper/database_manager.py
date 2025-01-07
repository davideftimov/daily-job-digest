from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class Job(SQLModel, table=True):
    id: str = Field(primary_key=True)
    time: int
    time_scraped: int
    text: str
    filter: bool
    source: str  # To track which platform the job came from
    url: str
    title: str | None = None
    location: str | None = None
    hn_id: int | None = None
    company: str | None = None
    viewed: bool = Field(default=False)

class DatabaseManager:
    def __init__(self, sqlite_file_name="database.db"):
        self.sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(self.sqlite_url)
        self.create_tables()

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def job_exists(self, job_id: str) -> bool:
        with Session(self.engine) as session:
            existing_job = session.exec(
                select(Job)
                .where(Job.id == job_id)
            ).first()
            return existing_job is not None

    def save_job(self, job: Job):
        if not self.job_exists(job.id):
            with Session(self.engine) as session:
                session.add(job)
                session.commit()

    def get_max_hn_id(self) -> int:
        with Session(self.engine) as session:
            max_id = session.exec(
                select(Job)
                .where(Job.source == "hackernews")
                .order_by(Job.hn_id.desc())
            ).first()
            return max_id.hn_id if max_id is not None else 0