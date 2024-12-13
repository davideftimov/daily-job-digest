from fastapi import APIRouter, Request
from sqlmodel import select
from hn_job_filter.database import Comment
from hn_job_filter.database import SessionDep

router = APIRouter()

@router.get("/comments/")
async def get_comments(request: Request, session: SessionDep):
    statement = select(Comment)
    results = session.exec(statement).all()
    return results