from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hn_job_filter.database import create_db_and_tables
from hn_job_filter.jobs import router as job_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router.router)

