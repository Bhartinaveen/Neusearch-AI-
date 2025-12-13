
from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()


# Default to SQLite for local dev if DATABASE_URL not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./neusearch.db")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

