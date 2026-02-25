from sqlmodel import SQLModel, create_engine, Session
from .settings import settings

engine = create_engine(settings.DATABASE_URL, echo=True)  # echo=True = show SQL queries in console

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

        