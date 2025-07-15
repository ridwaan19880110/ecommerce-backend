from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

load_dotenv()  # ✅ This loads variables from .env file

# ✅ Correct environment variable fetch
DATABASE_URL = os.getenv("SUPABASE_DB_URL")

if not DATABASE_URL:
    raise ValueError("Missing SUPABASE_DB_URL in environment variables")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
