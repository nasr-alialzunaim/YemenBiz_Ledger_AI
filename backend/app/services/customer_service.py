from sqlalchemy.orm import Session

from backend.app.db.models import Customer
from backend.app.schemas.customers import CustomerCreate


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def list_customers(db: Session) -> list[Customer]:
    return db.query(Customer).order_by(Customer.created_at.desc()).all()


def get_or_create_customer_by_name(db: Session, name: str | None) -> Customer | None:
    if not name:
        return None

    existing = db.query(Customer).filter(Customer.name == name).first()
    if existing:
        return existing

    customer = Customer(name=name)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
