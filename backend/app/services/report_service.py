from collections import defaultdict

from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.models import Customer, Product, Sale, SaleItem


def dashboard_summary(db: Session) -> dict:
    sales = db.query(Sale).all()
    products = db.query(Product).all()
    customers_count = db.query(Customer).count()

    total_sales = sum(s.total_amount for s in sales)
    total_paid = sum(s.paid_amount for s in sales)
    total_debts = sum(s.remaining_amount for s in sales)

    product_totals: dict[str, float] = defaultdict(float)
    for item in db.query(SaleItem).all():
        product_totals[item.product_name_snapshot] += item.quantity

    top_products = [
        {"name": name, "quantity_sold": qty}
        for name, qty in sorted(product_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    low_stock_products = [
        {"id": p.id, "name": p.name, "stock_quantity": p.stock_quantity, "unit": p.unit}
        for p in products
        if p.stock_quantity <= settings.low_stock_threshold
    ]

    return {
        "total_sales": total_sales,
        "total_paid": total_paid,
        "total_debts": total_debts,
        "customers_count": customers_count,
        "products_count": len(products),
        "low_stock_products_count": len(low_stock_products),
        "sales_count": len(sales),
        "top_products": top_products,
        "low_stock_products": low_stock_products,
    }


def generate_arabic_daily_report(db: Session) -> str:
    summary = dashboard_summary(db)
    lines = [
        "# التقرير التجاري المختصر",
        "",
        f"- إجمالي المبيعات: {summary['total_sales']:.2f} {settings.default_currency}",
        f"- المبالغ المحصلة: {summary['total_paid']:.2f} {settings.default_currency}",
        f"- الديون المتبقية: {summary['total_debts']:.2f} {settings.default_currency}",
        f"- عدد العملاء: {summary['customers_count']}",
        f"- عدد المنتجات: {summary['products_count']}",
        f"- منتجات منخفضة المخزون: {summary['low_stock_products_count']}",
        "",
        "## أكثر المنتجات مبيعًا",
    ]

    if summary["top_products"]:
        for product in summary["top_products"]:
            lines.append(f"- {product['name']}: {product['quantity_sold']}")
    else:
        lines.append("- لا توجد مبيعات مسجلة بعد.")

    if summary["low_stock_products"]:
        lines += ["", "## تنبيهات المخزون"]
        for product in summary["low_stock_products"]:
            lines.append(
                f"- {product['name']}: الكمية الحالية {product['stock_quantity']} {product['unit']}"
            )

    return "\n".join(lines)
