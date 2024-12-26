from fastapi import APIRouter, Request, Query
from sqlmodel import select
from daily_job_digest.database import Job
from daily_job_digest.database import SessionDep
from datetime import datetime, date, time

router = APIRouter()

@router.get("/comments/")
async def get_comments(request: Request, session: SessionDep):
    statement = select(Job)
    results = session.exec(statement).all()
    return results

@router.get("/comments/by-date/{target_date}")
async def get_comments_by_date(
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