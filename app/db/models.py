from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base


class Buyer(Base):
    __tablename__ = "buyers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)  # ✅ Required field
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # ✅ Add this line
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image_url = Column(String)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("buyers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")
    delivery_slot = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("Buyer")
    product = relationship("Product")
