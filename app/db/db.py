from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # or use PostgreSQL if needed

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # remove connect_args for Postgres
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
