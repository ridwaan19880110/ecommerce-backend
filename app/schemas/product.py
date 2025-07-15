from pydantic import BaseModel

class ProductBase(BaseModel):
    seller_id: int
    title: str
    price: float
    stock: int
    image_url: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
