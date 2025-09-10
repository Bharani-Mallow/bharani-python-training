from events import create_database
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from middleware import DBSessionMiddleware
from routers import task
from settings import settings
from utils import get_openapi_url

app = FastAPI(
    title="Task Application",
    description="A FastAPI application for Task Management",
    version="1.0.0",
    openapi_url=get_openapi_url(),
    lifespan=create_database,
)
app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(task.router)
add_pagination(app)
