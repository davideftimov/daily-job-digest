from fastapi import APIRouter, Request, Query
from sqlmodel import select
from daily_job_digest.database import Job
from daily_job_digest.database import SessionDep
from datetime import datetime, date, time
from typing import Optional

router = APIRouter()

@router.get("/jobs/")
async def get_jobs(
    request: Request, 
    session: SessionDep,
    target_date: Optional[date] = None,
    source: Optional[str] = None
):
    statement = select(Job)
    
    if target_date:
        start_ts = int(datetime.combine(target_date, time.min).timestamp())
        end_ts = int(datetime.combine(target_date, time.max).timestamp())
        statement = statement.where(
            Job.time_scraped >= start_ts,
            Job.time_scraped <= end_ts
        )
    
    if source:
        statement = statement.where(Job.source == source)
    
    results = session.exec(statement).all()
    return results

@router.put("/jobs/{job_id}/viewed")
def mark_job_viewed(job_id: str, session: SessionDep):
    job = session.get(Job, job_id)
    if job:
        job.viewed = True
        session.add(job)
        session.commit()
    return {"success": bool(job)}