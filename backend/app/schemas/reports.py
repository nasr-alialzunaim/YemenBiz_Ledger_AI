from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_sales: float
    total_paid: float
    total_debts: float
    customers_count: int
    products_count: int
    low_stock_products_count: int
    sales_count: int
    top_products: list[dict]
    low_stock_products: list[dict]
