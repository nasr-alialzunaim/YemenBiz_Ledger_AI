# توثيق API لمشروع YemenBiz Ledger AI

بعد تشغيل Backend افتح:

```text
http://127.0.0.1:8000/docs
```

سيظهر Swagger UI التفاعلي.

---

## 1. Customers API

### إضافة عميل

```http
POST /api/customers
```

Body:

```json
{
  "name": "أحمد علي",
  "phone": "777000000",
  "address": "صنعاء",
  "notes": "عميل جملة"
}
```

Response:

```json
{
  "id": 1,
  "name": "أحمد علي",
  "phone": "777000000",
  "address": "صنعاء",
  "notes": "عميل جملة",
  "created_at": "2026-01-01T10:00:00"
}
```

### عرض العملاء

```http
GET /api/customers
```

---

## 2. Products API

### إضافة منتج

```http
POST /api/products
```

Body:

```json
{
  "name": "كرتون ماء",
  "sku": "WATER-001",
  "purchase_price": 1200,
  "sale_price": 1500,
  "stock_quantity": 40,
  "unit": "كرتون"
}
```

### عرض المنتجات

```http
GET /api/products
```

### تعديل منتج

```http
PATCH /api/products/{product_id}
```

Body:

```json
{
  "sale_price": 1600,
  "stock_quantity": 35
}
```

---

## 3. Sales API

### إضافة عملية بيع

```http
POST /api/sales
```

Body:

```json
{
  "customer_name": "أحمد",
  "payment_type": "credit",
  "paid_amount": 0,
  "currency": "YER",
  "notes": "بيع آجل",
  "items": [
    {
      "product_name": "كرتون ماء",
      "quantity": 3,
      "unit_price": 1500
    }
  ]
}
```

أنواع الدفع المقترحة:

| القيمة | المعنى |
|---|---|
| cash | نقد |
| credit | آجل |
| transfer | تحويل |

---

## 4. AI API

### تحليل عملية بيع باللغة العربية

```http
POST /api/ai/parse-sale
```

Body:

```json
{
  "text": "بعت لأحمد 3 كرتون ماء و2 كيس رز آجل بـ 18500 ريال",
  "save_as_sale": false
}
```

Response:

```json
{
  "customer_name": "أحمد",
  "payment_type": "credit",
  "total_amount": 18500,
  "paid_amount": 0,
  "remaining_amount": 18500,
  "currency": "YER",
  "items": [
    {
      "product_name": "كرتون ماء",
      "quantity": 3,
      "unit_price": 3083.33,
      "line_total": 9250
    }
  ],
  "confidence": 0.85,
  "warnings": [],
  "suggested_action": "يمكن حفظ العملية مباشرة بعد المراجعة."
}
```

إذا جعلت:

```json
{
  "save_as_sale": true
}
```

سيحفظ التحليل كعملية بيع بعد التحليل.

---

## 5. Reports API

### ملخص لوحة التحكم

```http
GET /api/reports/dashboard
```

Response:

```json
{
  "total_sales": 85000,
  "total_paid": 52000,
  "total_debts": 33000,
  "customers_count": 12,
  "products_count": 30,
  "low_stock_products_count": 4,
  "sales_count": 20,
  "top_products": [],
  "low_stock_products": []
}
```

### تقرير عربي

```http
GET /api/reports/daily-arabic
```

Response:

```json
{
  "report": "# التقرير التجاري المختصر..."
}
```
