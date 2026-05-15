from datetime import datetime
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone: str | None = None
    address: str | None = None
    notes: str | None = None


class CustomerRead(CustomerCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
