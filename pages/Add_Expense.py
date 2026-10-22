import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(
    page_title="Add Expense - PocketPal",
    page_icon="➕",
    layout="wide"
)

# Exact PocketPal Dark Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #07040d !important;
        color: #f3e8ff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #120b1f !important;
        border-right: 1px solid #2e1f4d !important;
    }
    [data-testid="stSidebar"] * {
        color: #f3e8ff !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #c084fc !important;
        font-weight: 700;
    }
    p, span, label, div {
        color: #f3e8ff;
    }
    .main-header {
        background: linear-gradient(135deg, #120b1f 0%, #1c1033 60%, #2e1754 100%);
        border: 1px solid #2e1f4d;
        border-left: 6px solid #7c3aed;
        padding: 1.8rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .main-header h1 {
        color: #c084fc !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .main-header p {
        color: #f3e8ff !important;
        opacity: 0.9;
        margin: 0.4rem 0 0 0;
        font-size: 1rem;
    }
    .kpi-card {
        background: #120b1f;
        border: 1px solid #2e1f4d;
        border-radius: 12px;
        padding: 1.1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        border-top: 3px solid #7c3aed;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    button[kind="secondary"] {
        background-color: #120b1f !important;
        border: 1px solid #2e1f4d !important;
        color: #f3e8ff !important;
    }
    button[kind="secondary"]:hover {
        border-color: #7c3aed !important;
        color: #c084fc !important;
    }
    [data-testid="stDataFrame"] {
        background-color: #120b1f !important;
        border: 1px solid #2e1f4d !important;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Locate data file
def get_data_path():
    candidates = [
        "expenses.csv",
        os.path.join(os.path.dirname(__file__), "..", "expenses.csv"),
        os.path.join(os.path.dirname(__file__), "expenses.csv"),
        os.path.join(os.getcwd(), "expenses.csv"),
        os.path.join(os.getcwd(), "pocketpal", "expenses.csv")
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    return os.path.abspath(candidates[1])

DATA_PATH = get_data_path()

def load_data():
    if "expenses_df" in st.session_state and st.session_state["expenses_df"] is not None and not st.session_state["expenses_df"].empty:
        return st.session_state["expenses_df"]
    
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df["Date"] = pd.to_datetime(df["Date"])
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description", "Payment_Method"])
    
    st.session_state["expenses_df"] = df
    return df

df = load_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>➕ PocketPal — Add Expense</h1>
    <p>Quickly log your student expenses to maintain up-to-date budgeting and smart advice</p>
</div>
""", unsafe_allow_html=True)

# Navigation bar
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 2])
with col_nav1:
    if st.button("⬅️ Dashboard", use_container_width=True):
        st.switch_page("app.py")
with col_nav2:
    if st.button("💡 Saving Advice", use_container_width=True):
        st.switch_page("pages/Saving_Advice.py")

st.markdown("<br>", unsafe_allow_html=True)

col_form, col_summary = st.columns([1.3, 1])

CATEGORIES = [
    "Food & Dining",
    "Housing & Utilities",
    "Academics & Books",
    "Transportation",
    "Entertainment & Leisure",
    "Personal Care & Shopping",
    "Healthcare & Fitness",
    "Miscellaneous"
]

PAYMENT_METHODS = ["UPI", "Cash", "Debit Card", "Credit Card", "Bank Transfer", "Other"]

with col_form:
    st.subheader("📝 Transaction Details")
    with st.form("add_expense_form", clear_on_submit=True):
        f_date = st.date_input("Date of Expense", value=date.today())
        f_cat = st.selectbox("Category", CATEGORIES, index=0)
        f_amount = st.number_input("Amount (₹)", min_value=1.0, max_value=200000.0, value=150.0, step=10.0)
        f_desc = st.text_input("Description / Notes", placeholder="e.g. Canteen lunch, metro recharge, assignment printout")
        f_method = st.selectbox("Payment Method", PAYMENT_METHODS, index=0)
        
        submitted = st.form_submit_button("💾 Save Expense", use_container_width=True, type="primary")
        
        if submitted:
            if not f_desc.strip():
                st.error("Please provide a short description for this expense.")
            else:
                new_row = pd.DataFrame([{
                    "Date": pd.to_datetime(f_date),
                    "Category": f_cat,
                    "Amount": float(f_amount),
                    "Description": f_desc.strip(),
                    "Payment_Method": f_method
                }])
                
                updated_df = pd.concat([df, new_row], ignore_index=True)
                st.session_state["expenses_df"] = updated_df
                
                # Persist to CSV
                try:
                    updated_df.to_csv(DATA_PATH, index=False)
                    st.success(f"✅ Added: ₹{f_amount:,.2f} for '{f_desc}' under {f_cat}!")
                except Exception as e:
                    st.warning(f"Saved in session memory (CSV write warning: {e})")
                
                df = updated_df

with col_summary:
    st.subheader("📊 Expense Snapshot")
    if not df.empty:
        total_spent = df["Amount"].sum()
        total_count = len(df)
        avg_spend = df["Amount"].mean()
        
        st.markdown(f"""
        <div class="kpi-card" style="margin-bottom: 1rem;">
            <div style="font-size: 0.85rem; color: #c084fc; text-transform: uppercase; font-weight: 600;">Total Expenses Logged</div>
            <div style="font-size: 1.8rem; color: #f3e8ff; font-weight: 700;">₹{total_spent:,.2f}</div>
            <div style="font-size: 0.85rem; color: #a855f7;">{total_count} transactions recorded</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Transactions", f"{total_count}")
        with col_m2:
            st.metric("Avg / Transaction", f"₹{avg_spend:,.2f}")
        
        st.markdown("##### 📌 Top 3 Spending Categories")
        top_cats = df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(3)
        for cat, amt in top_cats.items():
            pct = (amt / total_spent) * 100 if total_spent > 0 else 0
            st.write(f"• **{cat}**: ₹{amt:,.2f} ({pct:.1f}%)")
    else:
        st.info("No expenses logged yet. Add your first expense on the left!")

st.markdown("---")
st.subheader("🕒 Recent Transactions")
if not df.empty:
    display_df = df.sort_values(by="Date", ascending=False).copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(
        display_df[["Date", "Category", "Amount", "Description", "Payment_Method"]].head(15),
        use_container_width=True,
        hide_index=True
    )
else:
    st.write("No transactions found.")
