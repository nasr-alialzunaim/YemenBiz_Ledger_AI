import json
import re

from backend.app.core.config import settings
from backend.app.schemas.ai import ParsedSaleItem, ParsedSaleResponse


_NUMBER_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _to_float(value: str | None) -> float:
    if not value:
        return 0
    value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return 0


class NaturalLanguageSaleParser:
    """
    Parser for Arabic natural language sales.
    It works in two modes:
    1. Rule-based fallback parser.
    2. Optional OpenAI parser when USE_OPENAI=true and OPENAI_API_KEY is configured.
    """

    def parse(self, text: str) -> ParsedSaleResponse:
        if settings.use_openai and settings.openai_api_key:
            try:
                return self._parse_with_openai(text)
            except Exception:
                return self._parse_with_rules(text)

        return self._parse_with_rules(text)

    def _parse_with_rules(self, text: str) -> ParsedSaleResponse:
        normalized = text.strip()

        payment_type = "cash"
        if any(word in normalized for word in ["آجل", "دين", "دَين", "على الحساب", "بالحساب"]):
            payment_type = "credit"
        elif any(word in normalized for word in ["تحويل", "كريمي", "كاك", "محفظة"]):
            payment_type = "transfer"

        customer_name = self._extract_customer_name(normalized)
        total_amount = self._extract_total_amount(normalized)
        items = self._extract_items(normalized, total_amount)

        paid_amount = total_amount if payment_type == "cash" else 0
        remaining_amount = max(total_amount - paid_amount, 0)

        warnings = []
        if not customer_name and payment_type == "credit":
            warnings.append("العملية آجل لكن لم يتم التعرف على اسم العميل بوضوح.")
        if total_amount <= 0:
            warnings.append("لم يتم استخراج المبلغ الإجمالي بوضوح.")
        if not items:
            warnings.append("لم يتم استخراج المنتجات بوضوح.")

        confidence = 0.55
        if customer_name:
            confidence += 0.15
        if total_amount > 0:
            confidence += 0.15
        if items:
            confidence += 0.15

        return ParsedSaleResponse(
            customer_name=customer_name,
            payment_type=payment_type,
            total_amount=total_amount,
            paid_amount=paid_amount,
            remaining_amount=remaining_amount,
            currency=settings.default_currency,
            items=items,
            confidence=min(confidence, 0.95),
            warnings=warnings,
            suggested_action=(
                "راجع البيانات المستخرجة ثم احفظ العملية."
                if warnings
                else "يمكن حفظ العملية مباشرة بعد المراجعة."
            ),
        )

    def _extract_customer_name(self, text: str) -> str | None:
        patterns = [
            r"(?:بعت|بعنا|بيع|تم البيع)\s+(?:لـ|ل|للعميل)\s*([ء-يA-Za-z\s]{2,30})",
            r"(?:العميل|للعميل)\s+([ء-يA-Za-z\s]{2,30})",
            r"(?:على|عند)\s+([ء-يA-Za-z\s]{2,30})\s+(?:آجل|دين|بالحساب)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                name = re.split(r"\s+(?:عدد|كمية|بـ|ب|آجل|دين|كرتون|كيس|حبة)", name)[0].strip()
                if name:
                    return name
        return None

    def _extract_total_amount(self, text: str) -> float:
        patterns = [
            r"(?:بـ|بمبلغ|المبلغ|إجمالي|اجمالي)\s*(\d+(?:[.,]\d+)?)",
            r"(\d+(?:[.,]\d+)?)\s*(?:ريال|ر\.ي|YER|دولار|USD)",
        ]
        amounts = []
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                amounts.append(_to_float(match.group(1)))
        return max(amounts) if amounts else 0

    def _extract_items(self, text: str, total_amount: float) -> list[ParsedSaleItem]:
        item_patterns = [
            r"(\d+(?:[.,]\d+)?)\s+(كرتون|كيس|حبة|علبة|صندوق|كيلو|لتر|قطعة)\s+([ء-يA-Za-z0-9\s]{2,30})",
            r"([ء-يA-Za-z0-9\s]{2,30})\s+عدد\s+(\d+(?:[.,]\d+)?)",
        ]

        raw_items: list[tuple[str, float]] = []

        for match in re.finditer(item_patterns[0], text):
            qty = _to_float(match.group(1))
            unit = match.group(2)
            name = f"{unit} {match.group(3).strip()}"
            name = re.split(r"\s+(?:و|بـ|بمبلغ|آجل|نقد|تحويل)", name)[0].strip()
            if name and qty:
                raw_items.append((name, qty))

        for match in re.finditer(item_patterns[1], text):
            name = match.group(1).strip()
            qty = _to_float(match.group(2))
            if name and qty:
                raw_items.append((name, qty))

        if not raw_items and total_amount > 0:
            raw_items.append(("منتج غير محدد", 1))

        items: list[ParsedSaleItem] = []
        if raw_items:
            split_total = total_amount / len(raw_items) if total_amount > 0 else 0
            for name, qty in raw_items:
                unit_price = split_total / qty if qty else 0
                items.append(
                    ParsedSaleItem(
                        product_name=name,
                        quantity=qty,
                        unit_price=round(unit_price, 2),
                        line_total=round(unit_price * qty, 2),
                    )
                )

        return items

    def _parse_with_openai(self, text: str) -> ParsedSaleResponse:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        prompt = f"""
أنت محلل مبيعات للمحلات الصغيرة في اليمن.
استخرج عملية البيع من النص التالي وأعد JSON فقط دون أي شرح.

النص:
{text}

المطلوب:
{{
  "customer_name": null,
  "payment_type": "cash|credit|transfer",
  "total_amount": 0,
  "paid_amount": 0,
  "remaining_amount": 0,
  "currency": "YER",
  "items": [
    {{
      "product_name": "",
      "quantity": 1,
      "unit_price": 0,
      "line_total": 0
    }}
  ],
  "confidence": 0.0,
  "warnings": [],
  "suggested_action": ""
}}
"""
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        content = response.choices[0].message.content or "{}"
        data = json.loads(content)
        return ParsedSaleResponse(**data)
