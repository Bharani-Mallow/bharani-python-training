# Task Management API

A FastAPI-based REST API for managing tasks and subtasks with SQLAlchemy integration.

## Overview

This application provides a complete task management system with the following features:

- Create, read, update, and delete tasks
- Create, read, update, and delete subtasks associated with tasks
- Data seeding capability to populate the database with sample tasks and subtasks
- SQLite database integration using SQLAlchemy ORM
- Automatic table creation on application startup

## Project Structure

```
week-5/
├── main.py           # FastAPI application entrypoint
├── db.py             # Database connection and session management
├── models.py         # SQLAlchemy ORM models (Task and SubTask)
├── schemas.py        # Pydantic schemas for request/response validation
├── routers.py        # API route handlers and business logic
├── test.db           # SQLite database file
└── pyproject.toml    # Project dependencies and metadata
```

## Installation

1. Make sure you have Python 3.13 or higher installed
2. Install dependencies:

```bash
uv sync
```
3. Activate the virtual environment
```bash
source .venv/bin/activate
```

## Starting the Application

Start the FastAPI server using uvicorn:

```bash
uv run fastapi dev main.py
```

The server will start on http://localhost:8000 by default.

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
