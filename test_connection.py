from app.db.database import engine, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text  # ✅ import text()

def test_db_connection():
    try:
        # Create a session and test connection
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        # Use SQLAlchemy text() for raw SQL
        session.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")

if __name__ == "__main__":
    test_db_connection()
