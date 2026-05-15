from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.customers import CustomerCreate, CustomerRead
from backend.app.services.customer_service import create_customer, list_customers

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.post("", response_model=CustomerRead)
def create(payload: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, payload)


@router.get("", response_model=list[CustomerRead])
def index(db: Session = Depends(get_db)):
    return list_customers(db)
