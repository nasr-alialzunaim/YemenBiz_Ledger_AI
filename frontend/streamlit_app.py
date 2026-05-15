import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="YemenBiz Ledger AI",
    page_icon="💼",
    layout="wide",
)

st.title("YemenBiz Ledger AI")
st.caption("دفتر تجاري ذكي للمحلات الصغيرة في اليمن")

page = st.sidebar.radio(
    "القائمة",
    [
        "لوحة التحكم",
        "إدخال بيع بالذكاء الاصطناعي",
        "إضافة منتج",
        "إضافة عميل",
        "المبيعات",
        "التقرير العربي",
    ],
)

if page == "لوحة التحكم":
    st.header("لوحة التحكم")
    try:
        data = requests.get(f"{API_BASE_URL}/api/reports/dashboard", timeout=10).json()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("إجمالي المبيعات", f"{data['total_sales']:.2f}")
        c2.metric("المحصّل", f"{data['total_paid']:.2f}")
        c3.metric("الديون", f"{data['total_debts']:.2f}")
        c4.metric("منتجات منخفضة", data["low_stock_products_count"])

        st.subheader("أكثر المنتجات مبيعًا")
        st.write(data["top_products"])

        st.subheader("تنبيهات المخزون")
        st.write(data["low_stock_products"])
    except Exception as exc:
        st.error(f"تعذر الاتصال بالـ API: {exc}")

elif page == "إدخال بيع بالذكاء الاصطناعي":
    st.header("إدخال بيع باللغة العربية")
    text = st.text_area(
        "اكتب العملية كما يقولها صاحب المحل",
        value="بعت لأحمد 3 كرتون ماء و2 كيس رز آجل بـ 18500 ريال",
        height=140,
    )
    save = st.checkbox("حفظ العملية كمبيعة بعد التحليل", value=False)

    if st.button("تحليل العملية"):
        response = requests.post(
            f"{API_BASE_URL}/api/ai/parse-sale",
            json={"text": text, "save_as_sale": save},
            timeout=30,
        )
        if response.ok:
            st.success("تم التحليل")
            st.json(response.json())
        else:
            st.error(response.text)

elif page == "إضافة منتج":
    st.header("إضافة منتج")
    with st.form("product_form"):
        name = st.text_input("اسم المنتج")
        sku = st.text_input("الكود / SKU")
        purchase_price = st.number_input("سعر الشراء", min_value=0.0)
        sale_price = st.number_input("سعر البيع", min_value=0.0)
        stock_quantity = st.number_input("كمية المخزون", min_value=0.0)
        unit = st.text_input("الوحدة", value="قطعة")
        submitted = st.form_submit_button("حفظ")

    if submitted:
        response = requests.post(
            f"{API_BASE_URL}/api/products",
            json={
                "name": name,
                "sku": sku or None,
                "purchase_price": purchase_price,
                "sale_price": sale_price,
                "stock_quantity": stock_quantity,
                "unit": unit,
            },
            timeout=10,
        )
        st.write(response.json())

elif page == "إضافة عميل":
    st.header("إضافة عميل")
    with st.form("customer_form"):
        name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الهاتف")
        address = st.text_input("العنوان")
        notes = st.text_area("ملاحظات")
        submitted = st.form_submit_button("حفظ")

    if submitted:
        response = requests.post(
            f"{API_BASE_URL}/api/customers",
            json={
                "name": name,
                "phone": phone or None,
                "address": address or None,
                "notes": notes or None,
            },
            timeout=10,
        )
        st.write(response.json())

elif page == "المبيعات":
    st.header("المبيعات")
    try:
        data = requests.get(f"{API_BASE_URL}/api/sales", timeout=10).json()
        st.write(data)
    except Exception as exc:
        st.error(str(exc))

elif page == "التقرير العربي":
    st.header("التقرير العربي")
    try:
        data = requests.get(f"{API_BASE_URL}/api/reports/daily-arabic", timeout=10).json()
        st.markdown(data["report"])
    except Exception as exc:
        st.error(str(exc))
