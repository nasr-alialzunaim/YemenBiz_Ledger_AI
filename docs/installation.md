# دليل التثبيت والتشغيل

هذا الدليل مخصص للمطور الذي يريد تشغيل المشروع محليًا.

---

## 1. المتطلبات

- Python 3.10 أو أحدث.
- Git.
- PowerShell على Windows.
- اتصال إنترنت عند تثبيت المكتبات فقط.

---

## 2. تحميل المشروع

```powershell
git clone https://github.com/YOUR_USERNAME/yemenbiz-ledger-ai.git
cd yemenbiz-ledger-ai
```

---

## 3. إنشاء بيئة افتراضية

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---

## 4. تثبيت المكتبات

```powershell
pip install -r backend\requirements.txt
```

---

## 5. تجهيز ملف البيئة

```powershell
Copy-Item .env.example .env
```

الملف الافتراضي يعمل بدون OpenAI.

---

## 6. تشغيل Backend

```powershell
uvicorn backend.app.main:app --reload
```

افتح:

```text
http://127.0.0.1:8000/docs
```

---

## 7. تشغيل Frontend

افتح Terminal جديد:

```powershell
.\.venv\Scripts\activate
streamlit run frontend\streamlit_app.py
```

---

## 8. تشغيل الاختبارات

```powershell
pytest
```

---

## 9. فحص الكود

```powershell
ruff check .
```

---

## 10. مشاكل متوقعة

### مشكلة: ModuleNotFoundError

تأكد أنك داخل جذر المشروع وأنك فعّلت البيئة:

```powershell
.\.venv\Scripts\activate
```

### مشكلة: المنفذ 8000 مستخدم

شغل على منفذ آخر:

```powershell
uvicorn backend.app.main:app --reload --port 8001
```

ثم عدّل `API_BASE_URL` في:

```text
frontend/streamlit_app.py
```
