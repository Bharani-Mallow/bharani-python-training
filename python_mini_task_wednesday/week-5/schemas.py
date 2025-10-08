from pydantic import BaseModel


class BaseRequest(BaseModel):
    title: str
    description: str


class SubTaskResponse(BaseModel):
    id: int
    title: str
    description: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    subtasks: list[SubTaskResponse]


class SeederRequest(BaseModel):
    number_of_tasks: int
    subtasks_per_task: int
