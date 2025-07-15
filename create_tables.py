from app.db.database import Base, engine
from app.db.models import Product  # 👈 Correct import path

# Create all tables defined by Base subclasses (like Product)
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
