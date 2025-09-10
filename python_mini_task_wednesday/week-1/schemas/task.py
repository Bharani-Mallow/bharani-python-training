from typing import Annotated

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, StringConstraints


class Task(BaseModel):
    title: str = Annotated[str, StringConstraints(max_length=100)]
    description: str = Annotated[str, StringConstraints(max_length=300)]


class QueryParams(BaseModel):
    search_term: str = Query("", alias="searchTerm")
