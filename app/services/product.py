from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
