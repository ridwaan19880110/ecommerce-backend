from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Product
import cloudinary.uploader

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ CREATE product
@router.post("/products/add")
async def add_product(
    seller_id: int = Form(...),
    title: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    result = cloudinary.uploader.upload(image.file)
    image_url = result["secure_url"]

    product = Product(
        seller_id=seller_id,
        title=title,
        price=price,
        stock=stock,
        image_url=image_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# ✅ READ all products
@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# ✅ READ single product by ID
@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ✅ UPDATE product
@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    title: str = Form(None),
    price: float = Form(None),
    stock: int = Form(None),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if title is not None:
        product.title = title
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock

    db.commit()
    db.refresh(product)
    return product

# ✅ DELETE product
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}
