from fastapi import APIRouter, Request, Query
from sqlmodel import select
from daily_job_digest.database import Job
from daily_job_digest.database import SessionDep
from datetime import datetime, date, time

router = APIRouter()

@router.get("/jobs/")
async def get_jobs(request: Request, session: SessionDep):
    statement = select(Job)
    results = session.exec(statement).all()
    return results

@router.get("/jobs/by-date/{target_date}")
async def get_jobs_by_date(
    target_date: date,
    session: SessionDep
):
    # Convert date to timestamp range using combine
    start_ts = int(datetime.combine(target_date, time.min).timestamp())
    end_ts = int(datetime.combine(target_date, time.max).timestamp())
    
    statement = select(Job).where(
        Job.time_scraped >= start_ts,
        Job.time_scraped <= end_ts
    )
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