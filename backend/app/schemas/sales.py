from datetime import datetime
from pydantic import BaseModel


class SaleItemCreate(BaseModel):
    product_id: int | None = None
    product_name: str
    quantity: float = 1
    unit_price: float = 0


class SaleCreate(BaseModel):
    customer_id: int | None = None
    customer_name: str | None = None
    payment_type: str = "cash"
    paid_amount: float = 0
    currency: str = "YER"
    notes: str | None = None
    items: list[SaleItemCreate]


class SaleItemRead(BaseModel):
    id: int
    product_id: int | None
    product_name_snapshot: str
    quantity: float
    unit_price: float
    line_total: float

    class Config:
        from_attributes = True


class SaleRead(BaseModel):
    id: int
    customer_id: int | None
    customer_name_snapshot: str | None
    total_amount: float
    paid_amount: float
    remaining_amount: float
    payment_type: str
    currency: str
    notes: str | None
    created_at: datetime
    items: list[SaleItemRead] = []

    class Config:
        from_attributes = True
