import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "task_manager.db")

def get_database_url() -> str:
    return f"sqlite:///./{DB_NAME}"

engine = create_engine(
    get_database_url(),
    echo=os.getenv("DEBUG", "False").lower() == "true",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
