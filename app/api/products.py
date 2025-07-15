from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Path
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Product
from uuid import UUID
from datetime import datetime
import shutil
import os
import uuid

router = APIRouter()

@router.get("/products/{product_id}")
def get_product(product_id: int = Path(...), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "id": str(product.id),
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "seller_id": str(product.seller_id),
        "image_url": product.image_url,
        "created_at": product.created_at
    }

@router.post("/products")
async def create_product(
    title: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    seller_id: UUID = Form(...),  # ✅ Accept UUID type
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Save the image to a local directory (or cloud if needed)
        image_extension = os.path.splitext(image.filename)[1]
        image_filename = f"{uuid.uuid4()}{image_extension}"
        image_path = f"static/uploads/{image_filename}"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"/{image_path}"  # Update to Cloudinary URL if using cloud

        product = Product(
            title=title,
            description=description,
            price=price,
            stock=stock,
            seller_id=seller_id,
            image_url=image_url,
            created_at=datetime.utcnow()
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return {
            "message": "Product created successfully",
            "product_id": str(product.id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
