import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Budget Planner - PocketPal",
    page_icon="🎯",
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
    .kpi-label {
        font-size: 0.85rem;
        color: #c084fc;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-val {
        font-size: 1.7rem;
        color: #f3e8ff;
        font-weight: 700;
        margin: 0.2rem 0;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #a855f7;
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
</style>
""", unsafe_allow_html=True)

# Data loader
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
    <h1>🎯 PocketPal — Budget Planner & Monitor</h1>
    <p>Set student spending targets, track budget utilization, and avoid end-of-month cash crunches</p>
</div>
""", unsafe_allow_html=True)

# Navigation
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 2])
with col_nav1:
    if st.button("⬅️ Dashboard", use_container_width=True):
        st.switch_page("app.py")
with col_nav2:
    if st.button("💡 Saving Advice", use_container_width=True):
        st.switch_page("pages/Saving_Advice.py")

st.markdown("<br>", unsafe_allow_html=True)

if df.empty:
    st.warning("No expense data found. Please add expenses first.")
    st.stop()

# Prepare Month column
df_budget = df.copy()
df_budget["Year_Month"] = df_budget["Date"].dt.strftime("%Y-%m (%b)")
available_months = sorted(df_budget["Year_Month"].unique(), reverse=True)

col_ctrl1, col_ctrl2 = st.columns([1, 2])
with col_ctrl1:
    selected_month = st.selectbox("📅 Select Month to Review", available_months, index=0)

# Filter by selected month
month_df = df_budget[df_budget["Year_Month"] == selected_month]
actual_spent_total = month_df["Amount"].sum()

# Default category budget limits
DEFAULT_BUDGETS = {
    "Housing & Utilities": 5000.0,
    "Food & Dining": 3000.0,
    "Academics & Books": 1200.0,
    "Transportation": 800.0,
    "Entertainment & Leisure": 600.0,
    "Personal Care & Shopping": 800.0,
    "Healthcare & Fitness": 600.0,
    "Miscellaneous": 400.0
}

# Session state for budgets
if "category_budgets" not in st.session_state:
    st.session_state["category_budgets"] = DEFAULT_BUDGETS.copy()

with st.sidebar:
    st.header("⚙️ Configure Category Budgets")
    st.caption("Adjust limits to match your monthly allowance:")
    for cat in DEFAULT_BUDGETS.keys():
        current_val = float(st.session_state["category_budgets"].get(cat, DEFAULT_BUDGETS[cat]))
        st.session_state["category_budgets"][cat] = st.number_input(
            f"{cat} (₹)",
            min_value=0.0,
            max_value=50000.0,
            value=current_val,
            step=100.0
        )

total_budget = sum(st.session_state["category_budgets"].values())
remaining_budget = total_budget - actual_spent_total
budget_utilization = (actual_spent_total / total_budget * 100) if total_budget > 0 else 0

# Top KPI Metrics
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Monthly Budget</div>
        <div class="kpi-val">₹{total_budget:,.2f}</div>
        <div class="kpi-sub">Total allocated allowance</div>
    </div>
    """, unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Actual Spent</div>
        <div class="kpi-val">₹{actual_spent_total:,.2f}</div>
        <div class="kpi-sub">In {selected_month}</div>
    </div>
    """, unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Remaining Balance</div>
        <div class="kpi-val" style="color: {'#10b981' if remaining_budget >= 0 else '#ef4444'};">₹{remaining_budget:,.2f}</div>
        <div class="kpi-sub">{'Buffer remaining' if remaining_budget >= 0 else 'Deficit incurred'}</div>
    </div>
    """, unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Budget Utilization</div>
        <div class="kpi-val">{budget_utilization:.1f}%</div>
        <div class="kpi-sub">Target: &lt; 100%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Category-wise Comparison
st.subheader(f"📊 Budget vs Actual Spending for {selected_month}")

cat_actual = month_df.groupby("Category")["Amount"].sum().to_dict()
all_categories = list(st.session_state["category_budgets"].keys())

comparison_rows = []
for cat in all_categories:
    budget_amt = st.session_state["category_budgets"].get(cat, 0.0)
    spent_amt = cat_actual.get(cat, 0.0)
    diff = budget_amt - spent_amt
    pct = (spent_amt / budget_amt * 100) if budget_amt > 0 else 0
    comparison_rows.append({
        "Category": cat,
        "Budget": budget_amt,
        "Actual Spent": spent_amt,
        "Remaining": diff,
        "Utilization %": pct
    })

comp_df = pd.DataFrame(comparison_rows)

DARK_LAYOUT = dict(
    plot_bgcolor="#120b1f",
    paper_bgcolor="#120b1f",
    font=dict(color="#f3e8ff", family="sans-serif"),
    xaxis=dict(gridcolor="#2e1f4d", title_font=dict(color="#c084fc"), tickfont=dict(color="#f3e8ff")),
    yaxis=dict(gridcolor="#2e1f4d", title_font=dict(color="#c084fc"), tickfont=dict(color="#f3e8ff")),
    legend=dict(font=dict(color="#f3e8ff"), bgcolor="rgba(18, 11, 31, 0.8)", bordercolor="#2e1f4d", borderwidth=1)
)

# Interactive Chart
fig = go.Figure()
fig.add_trace(go.Bar(
    name="Budgeted Limit",
    x=comp_df["Category"],
    y=comp_df["Budget"],
    marker_color="#2e1f4d"
))
fig.add_trace(go.Bar(
    name="Actual Spent",
    x=comp_df["Category"],
    y=comp_df["Actual Spent"],
    marker_color="#7c3aed"
))

layout_config = DARK_LAYOUT.copy()
layout_config["legend"] = dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
)

fig.update_layout(
    **layout_config,
    barmode="group",
    title=f"Category Budget Comparison ({selected_month})",
    xaxis_tickangle=-30,
    yaxis_title="Amount (₹)",
    margin=dict(l=20, r=20, t=50, b=80)
)

st.plotly_chart(fig, use_container_width=True)

# Progress Bars per category
st.subheader("📋 Category Budget Utilization Progress")
cols = st.columns(2)
for i, row in comp_df.iterrows():
    c_idx = i % 2
    with cols[c_idx]:
        cat = row["Category"]
        spent = row["Actual Spent"]
        budget = row["Budget"]
        pct = row["Utilization %"]
        
        if pct > 100:
            status_text = f"🚨 Exceeded by ₹{(spent - budget):,.2f} ({pct:.0f}%)"
        elif pct >= 80:
            status_text = f"⚠️ Warning: Reached {pct:.0f}% of budget"
        else:
            status_text = f"✅ Healthy: {pct:.0f}% used (₹{row['Remaining']:,.2f} left)"
        
        st.write(f"**{cat}** — Spent ₹{spent:,.2f} of ₹{budget:,.2f}")
        st.caption(status_text)
        progress_val = min(1.0, spent / budget) if budget > 0 else 0.0
        st.progress(progress_val)
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
