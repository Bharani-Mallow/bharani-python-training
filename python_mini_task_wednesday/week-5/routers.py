from db import get_db_session
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models import SubTask, Task
from schemas import BaseRequest, SeederRequest, SubTaskResponse, TaskResponse
from sqlalchemy.orm import Session

task_router = APIRouter()


@task_router.post("/seeder")
def seed_data(
    seeder_request: SeederRequest, session: Session = Depends(get_db_session)
):
    new_tasks = []
    for task_index in range(seeder_request.number_of_tasks):
        task = Task(
            title=f"Task {task_index + 1}",
            description=f"Description for Task {task_index + 1}",
        )
        task.subtasks = [
            SubTask(
                title=f"Subtask {subtask_index + 1} for Task {task_index + 1}",
                description=f"Description for Subtask {subtask_index + 1} of Task {task_index + 1}",
            )
            for subtask_index in range(seeder_request.subtasks_per_task)
        ]
        new_tasks.append(task)
    session.add_all(new_tasks)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"Seeded {seeder_request.number_of_tasks} tasks with {seeder_request.subtasks_per_task} subtasks each."
        },
    )


@task_router.get(
    "/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK
)
def get_tasks(session: Session = Depends(get_db_session)):
    tasks = session.query(Task).all()
    return tasks


@task_router.get("/tasks/{task_id}/subtasks", response_model=list[SubTaskResponse])
def get_subtasks(task_id: int, session: Session = Depends(get_db_session)):
    subtasks = session.query(SubTask).filter(SubTask.task_id == task_id).all()
    return subtasks


@task_router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_db_session)):
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    return task


@task_router.get("/subtasks/{subtask_id}", response_model=SubTaskResponse)
def get_subtask(subtask_id: int, session: Session = Depends(get_db_session)):
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        return JSONResponse(status_code=404, content={"message": "Subtask not found"})
    return subtask


@task_router.post(
    "/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
def create_task(task: BaseRequest, session: Session = Depends(get_db_session)):
    new_task = Task(title=task.title, description=task.description)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@task_router.post(
    "/tasks/{task_id}/subtasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subtask(
    task_id: int, subtask: BaseRequest, session: Session = Depends(get_db_session)
):
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    new_subtask = SubTask(
        title=subtask.title, description=subtask.description, task_id=task_id
    )
    session.add(new_subtask)
    session.commit()
    session.refresh(task)
    return task


@task_router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task_data: BaseRequest, session: Session = Depends(get_db_session)
):
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    task.title = task_data.title
    task.description = task_data.description
    session.commit()
    session.refresh(task)
    return task


@task_router.put("/subtasks/{subtask_id}", response_model=SubTaskResponse)
def update_subtask(
    subtask_id: int,
    subtask_data: BaseRequest,
    session: Session = Depends(get_db_session),
):
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        return JSONResponse(status_code=404, content={"message": "Subtask not found"})
    subtask.title = subtask_data.title
    subtask.description = subtask_data.description
    session.commit()
    session.refresh(subtask)
    return subtask


@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, session: Session = Depends(get_db_session)):
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    session.delete(task)
    session.commit()
    return JSONResponse(content={"message": "Task deleted successfully"})


@task_router.delete("/subtasks/{subtask_id}", status_code=status.HTTP_200_OK)
def delete_subtask(subtask_id: int, session: Session = Depends(get_db_session)):
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        return JSONResponse(status_code=404, content={"message": "Subtask not found"})
    session.delete(subtask)
    session.commit()
    return JSONResponse(content={"message": "Subtask deleted successfully"})
