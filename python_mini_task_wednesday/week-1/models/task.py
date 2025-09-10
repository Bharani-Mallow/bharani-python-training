from database import Base
from sqlalchemy import Column, String, Text


class Task(Base):

    __tablename__ = "tasks"

    title = Column("task_title", String(100), nullable=False)
    description = Column("task_description", Text)
