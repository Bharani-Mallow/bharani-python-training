from contextlib import asynccontextmanager

from db import Base, engine
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from routers import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)


@app.get("/health-check")
def health_check():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})


app.include_router(task_router)
