from datetime import datetime
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    sku: str | None = None
    purchase_price: float = 0
    sale_price: float = 0
    stock_quantity: float = 0
    unit: str = "قطعة"


class ProductRead(ProductCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    purchase_price: float | None = None
    sale_price: float | None = None
    stock_quantity: float | None = None
    unit: str | None = None
