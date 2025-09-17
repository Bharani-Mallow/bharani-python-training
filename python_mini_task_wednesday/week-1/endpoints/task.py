import logging

from exception import BadRequestError
from fastapi import Request, Response, status
from models.task import Task
from schemas import task
from sqlalchemy.orm import Session
from utils import get_logger

logger = get_logger(__name__, level=logging.DEBUG)


def create(request: Request, payload: task.Task):
    try:
        db: Session = request.state.db
        task = Task(title=payload.title, description=payload.description)
        db.add(task)
        db.commit()
        return Response(
            content={"message": "Task created successfully"},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as error:
        db.rollback()
        logger.debug(error)
        raise BadRequestError("Task cannot be created")


def update(request: Request, task_id: int, payload: task.Task):
    try:
        db: Session = request.state.db
        data = payload.model_dump()
        db.query(Task).filter(Task.id == task_id).update(**data)
        db.commit()
        return Response(
            content={"message": "Task updated successfully"},
            status_code=status.HTTP_200_OK,
        )
    except Exception as error:
        db.rollback()
        logger.debug(error)
        raise BadRequestError("Task cannot be updated")


def get(request: Request, task_id: int):
    try:
        db: Session = request.state.db
        task = db.query(Task).get(task_id)
    except Exception as error:
        logger.debug(error)



def list():
    pass


def delete():
    pass
