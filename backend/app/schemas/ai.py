from pydantic import BaseModel


class NaturalLanguageSaleRequest(BaseModel):
    text: str
    save_as_sale: bool = False


class ParsedSaleItem(BaseModel):
    product_name: str
    quantity: float = 1
    unit_price: float = 0
    line_total: float = 0


class ParsedSaleResponse(BaseModel):
    customer_name: str | None = None
    payment_type: str = "cash"
    total_amount: float = 0
    paid_amount: float = 0
    remaining_amount: float = 0
    currency: str = "YER"
    items: list[ParsedSaleItem] = []
    confidence: float = 0
    warnings: list[str] = []
    suggested_action: str = ""
