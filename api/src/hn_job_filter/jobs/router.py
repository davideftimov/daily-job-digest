from fastapi import APIRouter, Request, Query
from sqlmodel import select
from hn_job_filter.database import Job
from hn_job_filter.database import SessionDep
from datetime import datetime, date
import time

router = APIRouter()

@router.get("/comments/")
async def get_comments(request: Request, session: SessionDep):
    statement = select(Job)
    results = session.exec(statement).all()
    return results

@router.get("/comments/by-date/{target_date}")
async def get_comments_by_date(
    target_date: str,
    session: SessionDep
):
    # Convert date string to timestamp range
    date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
    start_ts = int(datetime(date_obj.year, date_obj.month, date_obj.day).timestamp())
    end_ts = int(datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59).timestamp())
    
    # Query jobs within the date range
    statement = select(Job).where(
        Job.time_scraped >= start_ts,
        Job.time_scraped <= end_ts
    )
    results = session.exec(statement).all()
    return results