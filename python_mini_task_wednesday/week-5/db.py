from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite+pysqlite:///./test.db", echo=True, future=True)


class Base(DeclarativeBase):
    pass


def get_db_session():
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with session_local() as session:
        yield session
