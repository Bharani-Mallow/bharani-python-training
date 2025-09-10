from typing import Optional

from endpoints import task
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from pydantic import ValidationError
from schemas.task import QueryParams, Task

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("/", description="API to create a Task")
def create_task(request: Request, payload: Task):
    return task.create(request, payload)


@router.get("/get_task", description="API to get a Task")
def get_task(
    request: Request,
    task_id: int = Query(..., alias="taskId"),
):

    return {"task": task}


@router.get("/list_tasks", description="API to list all Tasks")
def list_tasks(
    request: Request,
    query_params: Optional[str] = None,
):

    return {"tasks": tasks}


@router.patch("/update_task/{task_id}", description="API to update a Task")
def update_task(
    request: Request,
    task_id: int,
    payload: Task,
):
    return task.update(request, task_id, payload)
    return {"message": "Task updated successfully"}


@router.delete("/delete_task", description="API to delete a Task")
def delete_task(
    request: Request,
    task_id: int = Query(..., alias="taskId"),
):

    return {"message": "Task deleted successfully"}
