from sqlmodel import SQLModel, create_engine
from decouple import config

DATABASE_URL = config("DB_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

