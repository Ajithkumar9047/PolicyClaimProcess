from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)  # Drop all tables
    SQLModel.metadata.create_all(engine)  # Create new tables with updated schema

def get_session():
    with Session(engine) as session:
        yield session
