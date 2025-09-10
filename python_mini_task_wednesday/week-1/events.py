# Lifespan event manager
from contextlib import asynccontextmanager
import os
import sqlite3
from database import Base, engine, SessionLocal
from fastapi import FastAPI
from models.task import Task


@asynccontextmanager
async def create_database(app: FastAPI):
    if not os.path.exists("./task.db"):
        print("Creating new database file")

    Base.metadata.create_all(bind=engine)
    print("Database tables created")

    # Optional: Add some initial data
    db = SessionLocal()
    try:
        # Check if we need to seed data
        user_count = db.query(Task).count()
        if user_count == 0:

            initial_task = Task(title="", description="")
            db.add(initial_task)
            db.commit()

    except Exception as e:
        print(f"Error adding initial data: {e}")
        db.rollback()
    finally:
        db.close()

    yield  # Application runs here

    # Shutdown
    print("Shutting down...")

    # connection = sqlite3.connect("tasks.db")
    # cursor = connection.cursor()
    # cursor.execute(
    #     """
    # CREATE TABLE IF NOT EXISTS tasks (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     title TEXT NOT NULL,
    #     description TEXT
    # )
    # """
    # )
    # cursor.execute(
    #     "INSERT INTO tasks (title, description) VALUES ('Sample Task', 'This is a sample task description.')"
    # )
    # connection.commit()
    # yield
    # connection.close()
