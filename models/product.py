from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)
