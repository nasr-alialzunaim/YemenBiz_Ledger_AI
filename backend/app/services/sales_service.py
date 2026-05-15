from sqlalchemy.orm import Session

from backend.app.db.models import Product, Sale, SaleItem
from backend.app.schemas.ai import ParsedSaleResponse
from backend.app.schemas.sales import SaleCreate
from backend.app.services.customer_service import get_or_create_customer_by_name
from backend.app.services.product_service import get_or_create_product_by_name


def create_sale(db: Session, payload: SaleCreate) -> Sale:
    customer = None
    if payload.customer_id:
        customer = db.query(Product).filter(Product.id == payload.customer_id).first()
    elif payload.customer_name:
        customer = get_or_create_customer_by_name(db, payload.customer_name)

    total_amount = sum(item.quantity * item.unit_price for item in payload.items)
    paid_amount = payload.paid_amount if payload.payment_type != "cash" else total_amount
    remaining_amount = max(total_amount - paid_amount, 0)

    sale = Sale(
        customer_id=getattr(customer, "id", None),
        customer_name_snapshot=payload.customer_name,
        total_amount=total_amount,
        paid_amount=paid_amount,
        remaining_amount=remaining_amount,
        payment_type=payload.payment_type,
        currency=payload.currency,
        notes=payload.notes,
    )
    db.add(sale)
    db.flush()

    for item in payload.items:
        product = None
        if item.product_id:
            product = db.query(Product).filter(Product.id == item.product_id).first()
        else:
            product = get_or_create_product_by_name(db, item.product_name, item.unit_price)

        line_total = item.quantity * item.unit_price

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=getattr(product, "id", None),
            product_name_snapshot=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=line_total,
        )
        db.add(sale_item)

        if product:
            product.stock_quantity = max((product.stock_quantity or 0) - item.quantity, 0)

    db.commit()
    db.refresh(sale)
    return sale


def create_sale_from_parsed(db: Session, parsed: ParsedSaleResponse) -> Sale:
    payload = SaleCreate(
        customer_name=parsed.customer_name,
        payment_type=parsed.payment_type,
        paid_amount=parsed.paid_amount,
        currency=parsed.currency,
        notes="Created from natural language parser.",
        items=[
            {
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in parsed.items
        ],
    )
    return create_sale(db, payload)


def list_sales(db: Session) -> list[Sale]:
    return db.query(Sale).order_by(Sale.created_at.desc()).all()
