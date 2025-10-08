from cache import (
    cache_service,
    get_subtask_cache_key,
    get_task_cache_key,
    get_task_subtasks_cache_key,
    get_tasks_list_cache_key,
)
from config import redis_config
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

    # Clear all caches since we've added new data
    cache_service.delete_pattern("task:*")
    cache_service.delete_pattern("subtask:*")
    cache_service.delete_from_cache(get_tasks_list_cache_key())

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
    # Try to get from cache first
    cache_key = get_tasks_list_cache_key()
    cached_tasks = cache_service.get_from_cache(cache_key)

    if cached_tasks is not None:
        return cached_tasks

    # If not in cache, fetch from database
    tasks = session.query(Task).all()

    # Convert to response format and cache
    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            subtasks=[
                SubTaskResponse(
                    id=subtask.id, title=subtask.title, description=subtask.description
                )
                for subtask in task.subtasks
            ],
        )
        task_responses.append(task_response)

    # Cache the result
    cache_service.set_in_cache(
        cache_key, [task.dict() for task in task_responses], redis_config.tasks_list_ttl
    )

    return task_responses


@task_router.get("/tasks/{task_id}/subtasks", response_model=list[SubTaskResponse])
def get_subtasks(task_id: int, session: Session = Depends(get_db_session)):
    # Try to get from cache first
    cache_key = get_task_subtasks_cache_key(task_id)
    cached_subtasks = cache_service.get_from_cache(cache_key)

    if cached_subtasks is not None:
        return cached_subtasks

    # If not in cache, fetch from database
    subtasks = session.query(SubTask).filter(SubTask.task_id == task_id).all()

    # Convert to response format and cache
    subtask_responses = [
        SubTaskResponse(
            id=subtask.id, title=subtask.title, description=subtask.description
        )
        for subtask in subtasks
    ]

    # Cache the result
    cache_service.set_in_cache(
        cache_key,
        [subtask.dict() for subtask in subtask_responses],
        redis_config.subtask_ttl,
    )

    return subtask_responses


@task_router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_db_session)):
    # Try to get from cache first
    cache_key = get_task_cache_key(task_id)
    cached_task = cache_service.get_from_cache(cache_key)

    if cached_task is not None:
        return cached_task

    # If not in cache, fetch from database
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})

    # Convert to response format and cache
    task_response = TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        subtasks=[
            SubTaskResponse(
                id=subtask.id, title=subtask.title, description=subtask.description
            )
            for subtask in task.subtasks
        ],
    )

    # Cache the result
    cache_service.set_in_cache(cache_key, task_response.dict(), redis_config.task_ttl)

    return task_response


@task_router.get("/subtasks/{subtask_id}", response_model=SubTaskResponse)
def get_subtask(subtask_id: int, session: Session = Depends(get_db_session)):
    # Try to get from cache first
    cache_key = get_subtask_cache_key(subtask_id)
    cached_subtask = cache_service.get_from_cache(cache_key)

    if cached_subtask is not None:
        return cached_subtask

    # If not in cache, fetch from database
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        return JSONResponse(status_code=404, content={"message": "Subtask not found"})

    # Convert to response format and cache
    subtask_response = SubTaskResponse(
        id=subtask.id, title=subtask.title, description=subtask.description
    )

    # Cache the result
    cache_service.set_in_cache(
        cache_key, subtask_response.dict(), redis_config.subtask_ttl
    )

    return subtask_response


@task_router.post(
    "/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
def create_task(task: BaseRequest, session: Session = Depends(get_db_session)):
    new_task = Task(title=task.title, description=task.description)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # Invalidate tasks list cache since we added a new task
    cache_service.delete_from_cache(get_tasks_list_cache_key())

    # Convert to response format
    task_response = TaskResponse(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        subtasks=[],
    )

    return task_response


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

    # Invalidate caches related to this task
    cache_service.invalidate_task_cache(task_id)
    cache_service.delete_from_cache(get_tasks_list_cache_key())

    # Convert to response format
    task_response = TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        subtasks=[
            SubTaskResponse(
                id=subtask.id, title=subtask.title, description=subtask.description
            )
            for subtask in task.subtasks
        ],
    )

    return task_response


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

    # Invalidate caches related to this task
    cache_service.invalidate_task_cache(task_id)
    cache_service.delete_from_cache(get_tasks_list_cache_key())

    # Convert to response format
    task_response = TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        subtasks=[
            SubTaskResponse(
                id=subtask.id, title=subtask.title, description=subtask.description
            )
            for subtask in task.subtasks
        ],
    )

    return task_response


@task_router.put("/subtasks/{subtask_id}", response_model=SubTaskResponse)
def update_subtask(
    subtask_id: int,
    subtask_data: BaseRequest,
    session: Session = Depends(get_db_session),
):
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        return JSONResponse(status_code=404, content={"message": "Subtask not found"})

    # Store task_id before updating for cache invalidation
    task_id = subtask.task_id

    subtask.title = subtask_data.title
    subtask.description = subtask_data.description
    session.commit()
    session.refresh(subtask)

    # Invalidate caches related to this subtask and its parent task
    cache_service.invalidate_subtask_cache(subtask_id, task_id)
    cache_service.delete_from_cache(get_tasks_list_cache_key())

    # Convert to response format
    subtask_response = SubTaskResponse(
        id=subtask.id, title=subtask.title, description=subtask.description
    )

    return subtask_response


@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, session: Session = Depends(get_db_session)):
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})

    # Store subtask IDs for cache invalidation before deletion
    subtask_ids = [subtask.id for subtask in task.subtasks]

    session.delete(task)
    session.commit()

    # Invalidate all related caches
    cache_service.invalidate_task_cache(task_id)
    cache_service.delete_from_cache(get_tasks_list_cache_key())

    # Invalidate individual subtask caches
    for subtask_id in subtask_ids:
        cache_service.delete_from_cache(get_subtask_cache_key(subtask_id))

    return JSONResponse(content={"message": "Task deleted successfully"})


@task_router.delete("/subtasks/{subtask_id}", status_code=status.HTTP_200_OK)
def delete_subtask(subtask_id: int, session: Session = Depends(get_db_session)):
    subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        return JSONResponse(status_code=404, content={"message": "Subtask not found"})

    # Store task_id for cache invalidation before deletion
    task_id = subtask.task_id

    session.delete(subtask)
    session.commit()

    # Invalidate caches related to this subtask and its parent task
    cache_service.invalidate_subtask_cache(subtask_id, task_id)
    cache_service.delete_from_cache(get_tasks_list_cache_key())

    return JSONResponse(content={"message": "Subtask deleted successfully"})


@task_router.get("/cache/stats", status_code=status.HTTP_200_OK)
def get_cache_stats():
    """Get cache statistics and health information."""
    stats = cache_service.get_cache_stats()
    return JSONResponse(content=stats)


@task_router.post("/cache/clear", status_code=status.HTTP_200_OK)
def clear_cache():
    """Clear all cache entries."""
    try:
        # Clear all task and subtask related caches
        deleted_count = cache_service.delete_pattern("task:*")
        deleted_count += cache_service.delete_pattern("subtask:*")
        cache_service.delete_from_cache(get_tasks_list_cache_key())

        return JSONResponse(
            content={
                "message": f"Cache cleared successfully. Deleted {deleted_count} keys."
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"Error clearing cache: {str(e)}"}
        )
