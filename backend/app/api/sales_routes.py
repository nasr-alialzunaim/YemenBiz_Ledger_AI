from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.sales import SaleCreate, SaleRead
from backend.app.services.sales_service import create_sale, list_sales

router = APIRouter(prefix="/api/sales", tags=["Sales"])


@router.post("", response_model=SaleRead)
def create(payload: SaleCreate, db: Session = Depends(get_db)):
    return create_sale(db, payload)


@router.get("", response_model=list[SaleRead])
def index(db: Session = Depends(get_db)):
    return list_sales(db)
