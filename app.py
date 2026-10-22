import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="PocketPal - Student Expense System",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Exact PocketPal Dark Theme CSS
st.markdown("""
<style>
    /* Global Styles */
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
        letter-spacing: -0.3px;
    }
    
    p, span, label, div {
        color: #f3e8ff;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #120b1f 0%, #1c1033 60%, #2e1754 100%);
        border: 1px solid #2e1f4d;
        border-left: 6px solid #7c3aed;
        padding: 2.2rem 2.4rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45);
    }
    .hero-banner h1 {
        color: #c084fc !important;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: #f3e8ff !important;
        font-size: 1.1rem;
        margin: 0.6rem 0 1rem 0;
        opacity: 0.9;
    }
    .module-tag {
        display: inline-block;
        background: rgba(124, 58, 237, 0.25);
        border: 1px solid #a855f7;
        color: #e879f9 !important;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Nav Cards */
    .nav-card {
        background: #120b1f;
        border: 1px solid #2e1f4d;
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .nav-card:hover {
        border-color: #7c3aed;
        transform: translateY(-2px);
    }
    .nav-card h3 {
        color: #c084fc;
        margin: 0.4rem 0;
        font-size: 1.25rem;
    }
    .nav-card p {
        color: #f3e8ff;
        opacity: 0.85;
        font-size: 0.92rem;
        margin-bottom: 1.2rem;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: #120b1f;
        border: 1px solid #2e1f4d;
        border-radius: 12px;
        padding: 1.1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        border-top: 3px solid #7c3aed;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #a855f7;
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
    
    /* Buttons */
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

# Data loader helper
def get_data_path():
    candidates = [
        "expenses.csv",
        os.path.join(os.path.dirname(__file__), "expenses.csv"),
        os.path.join(os.path.dirname(__file__), "..", "expenses.csv"),
        os.path.join(os.getcwd(), "expenses.csv"),
        os.path.join(os.getcwd(), "pocketpal", "expenses.csv")
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    return os.path.abspath(candidates[0])

DATA_PATH = get_data_path()

def load_data(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description", "Payment_Method"])
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year_Month"] = df["Date"].dt.strftime("%Y-%m (%b)")
    return df

# Initialize session state dataframe
if "expenses_df" not in st.session_state or st.session_state["expenses_df"] is None or st.session_state["expenses_df"].empty:
    st.session_state["expenses_df"] = load_data(DATA_PATH)

df = st.session_state["expenses_df"]

POCKETPAL_COLORS = ["#7c3aed", "#a855f7", "#c084fc", "#e879f9", "#818cf8", "#38bdf8", "#34d399", "#fb7185"]

DARK_LAYOUT = dict(
    plot_bgcolor="#120b1f",
    paper_bgcolor="#120b1f",
    font=dict(color="#f3e8ff", family="sans-serif"),
    xaxis=dict(
        gridcolor="#2e1f4d",
        zerolinecolor="#2e1f4d",
        title_font=dict(color="#c084fc"),
        tickfont=dict(color="#f3e8ff")
    ),
    yaxis=dict(
        gridcolor="#2e1f4d",
        zerolinecolor="#2e1f4d",
        title_font=dict(color="#c084fc"),
        tickfont=dict(color="#f3e8ff")
    ),
    legend=dict(
        font=dict(color="#f3e8ff"),
        bgcolor="rgba(18, 11, 31, 0.8)",
        bordercolor="#2e1f4d",
        borderwidth=1
    )
)

# Hero Section
st.markdown("""
<div class="hero-banner">
    <div class="module-tag">PocketPal System • Student Financial Management</div>
    <h1>💜 PocketPal — Student Expense System</h1>
    <p>Track daily expenses, control semester budgets, and access intelligent, data-driven saving recommendations.</p>
</div>
""", unsafe_allow_html=True)

# Quick Navigation Section (Interactive Dashboard Buttons)
st.subheader("🚀 Quick Actions & Modules")
col_act1, col_act2, col_act3 = st.columns(3)

with col_act1:
    st.markdown("""
    <div class="nav-card">
        <div>
            <div style="font-size: 2rem;">➕</div>
            <h3>Add Expense</h3>
            <p>Log today's transactions, food purchases, printouts, or rent with instant categorization.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Log Expense Now", key="btn_add_expense", use_container_width=True, type="secondary"):
        st.switch_page("pages/Add_Expense.py")

with col_act2:
    st.markdown("""
    <div class="nav-card">
        <div>
            <div style="font-size: 2rem;">🎯</div>
            <h3>Budget Planner</h3>
            <p>Define monthly category budgets, track spending velocity, and prevent overspending.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Manage Budget", key="btn_budget", use_container_width=True, type="secondary"):
        st.switch_page("pages/Budget.py")

with col_act3:
    st.markdown("""
    <div class="nav-card" style="border: 2px solid #7c3aed; background: #160e26;">
        <div>
            <div style="font-size: 2rem;">💡</div>
            <h3>Saving Advice & ML</h3>
            <p><strong style="color: #e879f9;">Khushi Joshi's Module</strong>: Spending insights, MoM comparisons, 50/30/20 tips, and K-Means clustering.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Saving Advice ⭐", key="btn_advice", use_container_width=True, type="primary"):
        st.switch_page("pages/Saving_Advice.py")

st.markdown("<br>", unsafe_allow_html=True)

# Quick KPI Metrics
st.subheader("📈 Financial Overview")

if not df.empty:
    total_spent = df["Amount"].sum()
    total_count = len(df)
    unique_months = df["Year_Month"].nunique()
    avg_per_month = total_spent / unique_months if unique_months > 0 else total_spent
    top_cat = df.groupby("Category")["Amount"].sum().idxmax()
    top_cat_val = df.groupby("Category")["Amount"].sum().max()
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Spend (All-Time)</div>
            <div class="kpi-val">₹{total_spent:,.2f}</div>
            <div class="kpi-sub">{total_count} transactions logged</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Monthly Spend</div>
            <div class="kpi-val">₹{avg_per_month:,.2f}</div>
            <div class="kpi-sub">Across {unique_months} academic months</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Primary Expense Driver</div>
            <div class="kpi-val" style="font-size: 1.35rem;">{top_cat}</div>
            <div class="kpi-sub">₹{top_cat_val:,.2f} ({(top_cat_val/total_spent*100):.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Active Data Source</div>
            <div class="kpi-val" style="font-size: 1.35rem;">expenses.csv</div>
            <div class="kpi-sub">Verified demo dataset</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations
    col_g1, col_g2 = st.columns([1.3, 1])
    with col_g1:
        st.markdown("##### 📅 Monthly Spending Trajectory")
        m_df = df.groupby("Year_Month")["Amount"].sum().reset_index()
        fig_trend = px.area(
            m_df,
            x="Year_Month",
            y="Amount",
            markers=True,
            color_discrete_sequence=["#7c3aed"],
            title="Expenditure Over Time"
        )
        fig_trend.update_layout(
            **DARK_LAYOUT,
            yaxis_title="Amount (₹)",
            xaxis_title="",
            height=300,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_g2:
        st.markdown("##### 🍩 Spending by Category")
        cat_df = df.groupby("Category")["Amount"].sum().reset_index()
        fig_donut = px.pie(
            cat_df,
            names="Category",
            values="Amount",
            hole=0.48,
            color_discrete_sequence=POCKETPAL_COLORS
        )
        fig_donut.update_layout(
            **DARK_LAYOUT,
            height=300,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color="#ffffff"))
        st.plotly_chart(fig_donut, use_container_width=True)
        
    st.markdown("---")
    
    # Recent Transactions Table
    st.subheader("🕒 Recent Transactions Preview")
    display_df = df.sort_values(by="Date", ascending=False).copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(
        display_df[["Date", "Category", "Amount", "Description", "Payment_Method"]].head(8),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No expense data loaded yet.")

# Sidebar Data Management
with st.sidebar:
    st.header("⚙️ PocketPal Settings")
    st.caption("Student Expense & Saving Module")
    st.markdown("---")
    
    st.markdown("### 👤 Project Module Info")
    st.write("**Student Lead**: Khushi Joshi")
    st.write("**Assigned Page**: `pages/Saving_Advice.py`")
    st.write("**Theme**: PocketPal Dark Theme")
    
    st.markdown("---")
    st.markdown("### 📁 Data Management")
    uploaded_file = st.file_uploader("Upload custom expenses CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            custom_df = pd.read_csv(uploaded_file)
            custom_df["Date"] = pd.to_datetime(custom_df["Date"])
            custom_df["Year_Month"] = custom_df["Date"].dt.strftime("%Y-%m (%b)")
            st.session_state["expenses_df"] = custom_df
            st.success("Uploaded custom expenses successfully!")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            
    if st.button("🔄 Reset to Default Demo Data", use_container_width=True):
        st.session_state["expenses_df"] = load_data(DATA_PATH)
        st.cache_data.clear()
        st.rerun()
