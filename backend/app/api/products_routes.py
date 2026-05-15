from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.products import ProductCreate, ProductRead, ProductUpdate
from backend.app.services.product_service import create_product, list_products, update_product

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("", response_model=ProductRead)
def create(payload: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, payload)


@router.get("", response_model=list[ProductRead])
def index(db: Session = Depends(get_db)):
    return list_products(db)


@router.patch("/{product_id}", response_model=ProductRead)
def update(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
