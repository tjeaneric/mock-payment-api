from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from config import settings

DATABASE_URL = settings.db_url

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """Create database session per request, close it after returning response"""
    with Session(engine) as session:
        yield session


# Database Session dependency
sessionDep = Annotated[Session, Depends(get_session)]
