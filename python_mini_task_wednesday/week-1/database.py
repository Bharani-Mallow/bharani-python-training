import sqlite3
import logging
from fastapi import Response
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from utils import get_logger

logger = get_logger(__name__, level=logging.DEBUG)

engine = create_engine()
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
Base = declarative_base()


def get_db_connection():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()