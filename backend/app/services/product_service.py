from sqlalchemy.orm import Session

from backend.app.db.models import Product
from backend.app.schemas.products import ProductCreate, ProductUpdate


def create_product(db: Session, payload: ProductCreate) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session) -> list[Product]:
    return db.query(Product).order_by(Product.created_at.desc()).all()


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def get_or_create_product_by_name(db: Session, name: str, unit_price: float = 0) -> Product:
    product = db.query(Product).filter(Product.name == name).first()
    if product:
        return product

    product = Product(name=name, sale_price=unit_price, stock_quantity=0)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
