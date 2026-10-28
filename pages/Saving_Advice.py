import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

st.set_page_config(
    page_title="Saving Advice & ML Insights - PocketPal",
    page_icon="💡",
    layout="wide"
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

    /* Main Header Banner */
    .main-header {
        background: linear-gradient(135deg, #120b1f 0%, #1c1033 60%, #2e1754 100%);
        border: 1px solid #2e1f4d;
        border-left: 6px solid #7c3aed;
        padding: 2rem 2.2rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .main-header h1 {
        color: #c084fc !important;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
    }
    .main-header p {
        color: #f3e8ff !important;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        font-size: 1.05rem;
    }
    
    /* Author Badge */
    .author-badge {
        display: inline-block;
        background: rgba(124, 58, 237, 0.25);
        border: 1px solid #a855f7;
        color: #e879f9 !important;
        padding: 0.25rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
    
    /* KPI / Stat Cards */
    .stat-card {
        background-color: #120b1f !important;
        border: 1px solid #2e1f4d !important;
        border-top: 3px solid #7c3aed !important;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: #a855f7 !important;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
    }
    .stat-title {
        color: #c084fc !important;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        color: #f3e8ff !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.2rem 0;
    }
    .stat-sub {
        color: #a855f7 !important;
        font-size: 0.85rem;
    }
    
    /* Tip Cards */
    .tip-card {
        background-color: #120b1f !important;
        border: 1px solid #2e1f4d !important;
        border-left: 5px solid #a855f7 !important;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .tip-card h4 {
        margin: 0 0 0.3rem 0;
        color: #e879f9 !important;
        font-size: 1.05rem;
    }
    .tip-card p {
        margin: 0;
        color: #f3e8ff !important;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    
    /* Cluster Result Box */
    .cluster-box {
        background: #120b1f !important;
        border: 2px solid #7c3aed !important;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.2);
    }
    .cluster-tag {
        background: #7c3aed;
        color: #ffffff !important;
        padding: 0.3rem 0.85rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .cluster-title {
        color: #e879f9 !important;
        margin: 0.6rem 0 0.3rem 0;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    /* Button Styling */
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
    
    /* Tabs & Dataframe */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #120b1f !important;
        border-radius: 10px;
        padding: 4px;
        border: 1px solid #2e1f4d;
    }
    .stTabs [data-baseweb="tab"] {
        color: #f3e8ff !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7c3aed !important;
        border-radius: 8px;
        color: #ffffff !important;
        font-weight: 600;
    }
    [data-testid="stDataFrame"] {
        background-color: #120b1f !important;
        border: 1px solid #2e1f4d !important;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Locate data file robustly
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

def load_and_preprocess_data():
    # Priority: read from st.session_state if present, else read CSV
    if "expenses_df" in st.session_state and st.session_state["expenses_df"] is not None and not st.session_state["expenses_df"].empty:
        df = st.session_state["expenses_df"].copy()
    elif os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        st.session_state["expenses_df"] = df.copy()
    else:
        return pd.DataFrame()
        
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year_Month"] = df["Date"].dt.strftime("%Y-%m (%b)")
    df["Month_Name"] = df["Date"].dt.strftime("%B %Y")
    df["Day_Name"] = df["Date"].dt.strftime("%A")
    df["Is_Weekend"] = df["Date"].dt.weekday >= 5
    return df

df = load_and_preprocess_data()

# Categorization mapping for 50/30/20 & Discretionary split
NEEDS_CATEGORIES = ["Housing & Utilities", "Academics & Books", "Healthcare & Fitness", "Transportation"]
WANTS_CATEGORIES = ["Food & Dining", "Entertainment & Leisure", "Personal Care & Shopping", "Miscellaneous"]

# Dark Theme Plotly Base Configuration
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

# Header
st.markdown("""
<div class="main-header">
    <div class="author-badge">PocketPal AI Financial Advisor • Module Lead: Khushi Joshi</div>
    <h1>💡 Saving Advice & Financial Intelligence</h1>
    <p>Comprehensive spending insights, month-over-month comparisons, personalized student budgeting advice, and K-Means clustering analytics.</p>
</div>
""", unsafe_allow_html=True)

# Navigation Bar
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 2])
with nav_col1:
    if st.button("⬅️ Dashboard", use_container_width=True):
        st.switch_page("app.py")
with nav_col2:
    if st.button("➕ Add Expense", use_container_width=True):
        st.switch_page("pages/Add_Expense.py")
with nav_col3:
    if st.button("🎯 Budget Planner", use_container_width=True):
        st.switch_page("pages/Budget.py")

st.markdown("<br>", unsafe_allow_html=True)

if df.empty:
    st.error("No transaction data available. Please verify that expenses.csv is loaded.")
    st.stop()

# Main Tabs
tab_insights, tab_mom, tab_advice, tab_ml = st.tabs([
    "🔍 Spending Insights",
    "📅 Monthly Comparison",
    "💰 Saving Recommendations",
    "🤖 K-Means Clustering"
])

# -------------------------------------------------------------
# TAB 1: SPENDING INSIGHTS
# -------------------------------------------------------------
with tab_insights:
    st.subheader("📊 Comprehensive Spending Insights")
    st.caption("Detailed breakdown of student expenditure patterns across academic terms")
    
    total_spend = df["Amount"].sum()
    num_txns = len(df)
    unique_months = df["Year_Month"].nunique()
    avg_monthly_spend = total_spend / unique_months if unique_months > 0 else total_spend
    
    df["Spend_Type"] = df["Category"].apply(lambda c: "Essential (Needs)" if c in NEEDS_CATEGORIES else "Discretionary (Wants)")
    needs_total = df[df["Spend_Type"] == "Essential (Needs)"]["Amount"].sum()
    wants_total = df[df["Spend_Type"] == "Discretionary (Wants)"]["Amount"].sum()
    discretionary_ratio = (wants_total / total_spend * 100) if total_spend > 0 else 0
    
    # KPI Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Total Spending</div>
            <div class="stat-value">₹{total_spend:,.2f}</div>
            <div class="stat-sub">{num_txns} logged transactions</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Avg Monthly Spend</div>
            <div class="stat-value">₹{avg_monthly_spend:,.2f}</div>
            <div class="stat-sub">Across {unique_months} academic months</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Discretionary Ratio</div>
            <div class="stat-value">{discretionary_ratio:.1f}%</div>
            <div class="stat-sub">₹{wants_total:,.2f} spent on wants</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        top_cat = df.groupby("Category")["Amount"].sum().idxmax()
        top_cat_amt = df.groupby("Category")["Amount"].sum().max()
        top_pct = (top_cat_amt / total_spend) * 100
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Top Expense Driver</div>
            <div class="stat-value" style="font-size: 1.3rem;">{top_cat}</div>
            <div class="stat-sub">₹{top_cat_amt:,.2f} ({top_pct:.1f}% of total)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_pie, col_bar = st.columns([1, 1.2])
    cat_summary = df.groupby("Category")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
    
    with col_pie:
        st.markdown("##### 🍩 Spending Share by Category")
        fig_donut = px.pie(
            cat_summary,
            names="Category",
            values="Amount",
            hole=0.52,
            color_discrete_sequence=POCKETPAL_COLORS
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color="#ffffff"))
        fig_donut.update_layout(
            **DARK_LAYOUT,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            height=340
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_bar:
        st.markdown("##### 📊 Category Expenditure Ranking")
        fig_bar = px.bar(
            cat_summary,
            x="Amount",
            y="Category",
            orientation="h",
            text="Amount",
            color="Amount",
            color_continuous_scale=["#2e1f4d", "#7c3aed", "#e879f9"]
        )
        fig_bar.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside", textfont=dict(color="#f3e8ff"))
        bar_layout = DARK_LAYOUT.copy()
        bar_layout.update({
            "yaxis": dict(
                autorange="reversed",
                gridcolor="#2e1f4d",
                tickfont=dict(color="#f3e8ff")
            ),
            "xaxis": dict(
                gridcolor="#2e1f4d",
                tickfont=dict(color="#f3e8ff")
            ),
            "margin": dict(l=10, r=40, t=10, b=10),
            "height": 340,
            "coloraxis_showscale": False
        })
        fig_bar.update_layout(**bar_layout)
        st.plotly_chart(fig_bar, use_container_width=True)

    
    # Behavioral Insights: Weekend vs Weekday & Payment Methods
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("##### 🗓️ Weekday vs. Weekend Spending Pattern")
        day_split = df.groupby("Is_Weekend")["Amount"].agg(["sum", "mean", "count"]).reset_index()
        day_split["Type"] = day_split["Is_Weekend"].map({False: "Weekday (Mon-Fri)", True: "Weekend (Sat-Sun)"})
        
        fig_day = px.bar(
            day_split,
            x="Type",
            y="sum",
            text="sum",
            color="Type",
            color_discrete_map={"Weekday (Mon-Fri)": "#7c3aed", "Weekend (Sat-Sun)": "#e879f9"}
        )
        fig_day.update_traces(texttemplate="₹%{text:,.2f}", textposition="outside", textfont=dict(color="#f3e8ff"))
        fig_day.update_layout(
            **DARK_LAYOUT,
            yaxis_title="Total Spent (₹)",
            xaxis_title="",
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig_day, use_container_width=True)
        st.caption(f"Average transaction on weekends: **₹{day_split[day_split['Is_Weekend']==True]['mean'].values[0]:,.2f}** vs weekdays: **₹{day_split[day_split['Is_Weekend']==False]['mean'].values[0]:,.2f}**")
        
    with col_w2:
        st.markdown("##### 💳 Payment Method Distribution")
        pay_df = df.groupby("Payment_Method")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
        fig_pay = px.pie(
            pay_df,
            names="Payment_Method",
            values="Amount",
            color_discrete_sequence=["#7c3aed", "#a855f7", "#c084fc", "#e879f9"]
        )
        fig_pay.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color="#ffffff"))
        fig_pay.update_layout(
            **DARK_LAYOUT,
            height=280,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_pay, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: MONTHLY COMPARISON
# -------------------------------------------------------------
with tab_mom:
    st.subheader("📅 Month-over-Month (MoM) Trend & Variance Analysis")
    st.caption("Compare how student spending evolved over successive academic months")
    
    months_order = sorted(df["Year_Month"].unique())
    monthly_totals = df.groupby("Year_Month")["Amount"].sum().reindex(months_order).reset_index()
    
    # MoM Growth Metrics
    if len(monthly_totals) >= 2:
        prev_month_amt = monthly_totals.iloc[-2]["Amount"]
        curr_month_amt = monthly_totals.iloc[-1]["Amount"]
        mom_diff = curr_month_amt - prev_month_amt
        mom_growth_pct = (mom_diff / prev_month_amt) * 100 if prev_month_amt > 0 else 0
        
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Previous Month Spend", f"₹{prev_month_amt:,.2f}")
        mcol2.metric("Latest Month Spend", f"₹{curr_month_amt:,.2f}", delta=f"{mom_growth_pct:.1f}%")
        mcol3.metric("Net Change", f"₹{abs(mom_diff):,.2f}", delta="Spend Increased" if mom_diff > 0 else "Spend Decreased", delta_color="inverse")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # MoM Grouped Bar Chart
    mom_cat = df.groupby(["Year_Month", "Category"])["Amount"].sum().reset_index()
    fig_mom = px.bar(
        mom_cat,
        x="Year_Month",
        y="Amount",
        color="Category",
        barmode="group",
        color_discrete_sequence=POCKETPAL_COLORS,
        title="Category-wise Spending Across Months"
    )
    mom_layout = DARK_LAYOUT.copy()
    mom_layout.update({
    "yaxis_title": "Amount (₹)",
    "xaxis_title": "Academic Month",
    "legend": dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
})
fig_mom.update_layout(**mom_layout)
st.plotly_chart(fig_mom, use_container_width=True)


    
st.markdown("---")
st.subheader("🔬 Deep-Dive: Compare Any Two Months")
    
c_m1, c_m2 = st.columns(2)
with c_m1:
    month_a = st.selectbox("Select Baseline Month (A)", months_order, index=max(0, len(months_order)-2))
with c_m2:
    month_b = st.selectbox("Select Comparison Month (B)", months_order, index=len(months_order)-1)
    
df_a = df[df["Year_Month"] == month_a].groupby("Category")["Amount"].sum()
df_b = df[df["Year_Month"] == month_b].groupby("Category")["Amount"].sum()

comparison_table = pd.DataFrame({
    f"{month_a} (₹)": df_a,
    f"{month_b} (₹)": df_b
}).fillna(0)

comparison_table["Difference (₹)"] = comparison_table[f"{month_b} (₹)"] - comparison_table[f"{month_a} (₹)"]
comparison_table["% Change"] = np.where(
    comparison_table[f"{month_a} (₹)"] > 0,
    (comparison_table["Difference (₹)"] / comparison_table[f"{month_a} (₹)"]) * 100,
    0.0
)

# Styled Table
st.markdown(f"##### Variance Table ({month_a} vs {month_b})")
formatted_comp = comparison_table.copy()
formatted_comp[f"{month_a} (₹)"] = formatted_comp[f"{month_a} (₹)"].apply(lambda x: f"₹{x:,.2f}")
formatted_comp[f"{month_b} (₹)"] = formatted_comp[f"{month_b} (₹)"].apply(lambda x: f"₹{x:,.2f}")
formatted_comp["Difference (₹)"] = formatted_comp["Difference (₹)"].apply(lambda x: f"{'+' if x>0 else ''}₹{x:,.2f}")
formatted_comp["% Change"] = formatted_comp["% Change"].apply(lambda x: f"{'+' if x>0 else ''}{x:.1f}%")
st.dataframe(formatted_comp, use_container_width=True)

# Top Surge & Top Saver
biggest_surge = comparison_table["Difference (₹)"].idxmax()
biggest_surge_val = comparison_table["Difference (₹)"].max()
biggest_drop = comparison_table["Difference (₹)"].idxmin()
biggest_drop_val = comparison_table["Difference (₹)"].min()

col_s1, col_s2 = st.columns(2)
with col_s1:
    if biggest_surge_val > 0:
        st.warning(f"🚨 **Surge Alert**: Spending on **{biggest_surge}** rose by **₹{biggest_surge_val:,.2f}** in {month_b}.")
    else:
        st.info("No category saw an increase in spending.")
with col_s2:
    if biggest_drop_val < 0:
        st.success(f"🎉 **Savings Win**: Spending on **{biggest_drop}** reduced by **₹{abs(biggest_drop_val):,.2f}** in {month_b}.")
    else:
        st.info("No spending reductions detected between these months.")

# -------------------------------------------------------------
# TAB 3: SAVING RECOMMENDATIONS & GOAL SIMULATOR
# -------------------------------------------------------------
with tab_advice:
    st.subheader("💡 Tailored Student Saving Advice & Recommendations")
    st.caption("Actionable, rule-based strategies and dynamic monthly savings calculator")

    # 50/30/20 Rule Benchmark
    st.markdown("#### 🎯 50/30/20 Student Budget Rule Benchmark")
    total_spent_val = df["Amount"].sum()
    needs_spent_val = df[df["Category"].isin(NEEDS_CATEGORIES)]["Amount"].sum()
    wants_spent_val = df[df["Category"].isin(WANTS_CATEGORIES)]["Amount"].sum()

    needs_pct = (needs_spent_val / total_spent_val) * 100 if total_spent_val > 0 else 0
    wants_pct = (wants_spent_val / total_spent_val) * 100 if total_spent_val > 0 else 0

    col_rule1, col_rule2 = st.columns([1.2, 1])
    with col_rule1:
        st.write(f"• **Needs (Essentials)**: **{needs_pct:.1f}%** (Benchmark: 50%)")
        st.progress(min(1.0, needs_pct / 100))
        st.write(f"• **Wants (Discretionary)**: **{wants_pct:.1f}%** (Benchmark: 30%)")
        st.progress(min(1.0, wants_pct / 100))
        st.caption("Standard 50/30/20 rule recommends: 50% Needs, 30% Wants, 20% Savings/Emergency Fund.")
        
    with col_rule2:
        if wants_pct > 35:
            st.warning(f"⚠️ **High Discretionary Spending ({wants_pct:.1f}%)**: Your non-essential spending is higher than the recommended 30% limit. Target trimming dining out and entertainment.")
        elif wants_pct <= 30:
            st.success(f"🌟 **Excellent Discipline**: Your discretionary spend ({wants_pct:.1f}%) is within healthy student limits!")
        else:
            st.info(f"ℹ️ **Moderate Discretionary**: At {wants_pct:.1f}%, your wants spending is close to the recommended threshold.")
            
    st.markdown("---")

    # Actionable Student Tips
    st.markdown("#### 🎓 Personalized Student Cost-Optimization Tips")

    food_total = df[df["Category"] == "Food & Dining"]["Amount"].sum()
    ent_total = df[df["Category"] == "Entertainment & Leisure"]["Amount"].sum()
    acad_total = df[df["Category"] == "Academics & Books"]["Amount"].sum()
    transit_total = df[df["Category"] == "Transportation"]["Amount"].sum()

    tip_cols = st.columns(2)
    with tip_cols[0]:
        st.markdown(f"""
        <div class="tip-card">
            <h4>🍔 Smart Dining & Cafeteria Management</h4>
            <p>You have spent <b>₹{food_total:,.2f}</b> on Food & Dining. Packing snacks for library sessions and opting for monthly canteen tokens can save an estimated <b>₹400 – ₹700/month</b> compared to ad-hoc food delivery.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="tip-card">
            <h4>🎬 Subscriptions & Weekend Splurges</h4>
            <p>Entertainment expenditure stands at <b>₹{ent_total:,.2f}</b>. Consider student bundle plans (e.g. Spotify/YouTube Student) or split OTT platforms among dorm mates to cut subscriptions by <b>50%</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tip_cols[1]:
        st.markdown(f"""
        <div class="tip-card">
            <h4>📚 Academic Textbooks & Printing Optimization</h4>
            <p>Academics & books accounted for <b>₹{acad_total:,.2f}</b>. Leverage college library reserve copies, open-source PDFs, and senior student textbook buybacks to lower term book costs by up to <b>40%</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="tip-card">
            <h4>🚇 Public Transit & Student Pass Discounts</h4>
            <p>Transportation totaled <b>₹{transit_total:,.2f}</b>. Apply for official student concession metro/bus smart cards rather than daily ticket purchases, saving up to <b>₹250/month</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")

    # Dynamic Goal Simulator
    st.markdown("#### 🎯 Interactive Monthly Savings Simulator")
    st.caption("Simulate how minor cuts in discretionary spending help reach your target semester savings goal")

    sim_col1, sim_col2 = st.columns([1.2, 1])
    with sim_col1:
        target_pct = st.slider("Select Target Savings Percentage on Discretionary Spend:", min_value=5, max_value=40, value=15, step=5)
        monthly_wants = wants_spent_val / unique_months if unique_months > 0 else wants_spent_val
        potential_monthly_savings = monthly_wants * (target_pct / 100)
        annualized_savings = potential_monthly_savings * 12
        
        st.write(f"Trimming **{target_pct}%** of your discretionary purchases yields:")
        res_m1, res_m2 = st.columns(2)
        res_m1.metric("Monthly Savings", f"₹{potential_monthly_savings:,.2f}")
        res_m2.metric("Annual Savings Potential", f"₹{annualized_savings:,.2f}")
        
    with sim_col2:
        st.markdown("##### ✂️ Recommended Trimming Action Plan")
        dining_trim = (food_total / unique_months) * (target_pct / 100) if unique_months > 0 else 0
        ent_trim = (ent_total / unique_months) * (target_pct / 100) if unique_months > 0 else 0
        st.write(f"• **Food & Dining**: Cut ₹{dining_trim:,.2f}/mo (skip 2 food deliveries)")
        st.write(f"• **Entertainment**: Cut ₹{ent_trim:,.2f}/mo (share 1 subscription)")
        st.write(f"• **Personal Shopping**: Cut ₹{(potential_monthly_savings - dining_trim - ent_trim):,.2f}/mo (avoid impulse buys)")

    # -------------------------------------------------------------
    # TAB 4: K-MEANS CLUSTERING (MACHINE LEARNING)
    # -------------------------------------------------------------
    with tab_ml:
        st.subheader("🤖 Machine Learning: Student Spending Archetypes (K-Means)")
        st.caption("Unsupervised clustering models group student financial profiles into behavioral spending personas")

        # Generate representative peer student dataset for clustering model
        np.random.seed(42)
        c1_spend = np.random.normal(5200, 700, 30)
        c1_ratio = np.random.normal(0.22, 0.04, 30)
        c1_freq = np.random.normal(20, 4, 30)

        c2_spend = np.random.normal(11500, 1200, 30)
        c2_ratio = np.random.normal(0.58, 0.06, 30)
        c2_freq = np.random.normal(52, 6, 30)

        c3_spend = np.random.normal(8200, 900, 30)
        c3_ratio = np.random.normal(0.38, 0.05, 30)
        c3_freq = np.random.normal(32, 5, 30)

        c4_spend = np.random.normal(9400, 1000, 30)
        c4_ratio = np.random.normal(0.28, 0.05, 30)
        c4_freq = np.random.normal(22, 4, 30)

        sim_spend = np.clip(np.concatenate([c1_spend, c2_spend, c3_spend, c4_spend]), 3000, 18000)
        sim_ratio = np.clip(np.concatenate([c1_ratio, c2_ratio, c3_ratio, c4_ratio]), 0.10, 0.85)
        sim_freq = np.clip(np.concatenate([c1_freq, c2_freq, c3_freq, c4_freq]), 8, 70)
        sim_avg_tx = sim_spend / sim_freq

        cohort_df = pd.DataFrame({
            "Total_Spend": sim_spend,
            "Discretionary_Ratio": sim_ratio * 100,
            "Txn_Frequency": sim_freq,
            "Avg_Txn_Amount": sim_avg_tx
        })

        # Compute User's actual feature values from real data
        user_total_spend = avg_monthly_spend
        user_discretionary_ratio = discretionary_ratio
        user_frequency = num_txns / unique_months if unique_months > 0 else num_txns
        user_avg_tx = total_spend / num_txns if num_txns > 0 else 100.0

        # Train K-Means
        features = ["Total_Spend", "Discretionary_Ratio", "Txn_Frequency", "Avg_Txn_Amount"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(cohort_df[features])

        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        cohort_df["Cluster"] = kmeans.fit_predict(X_scaled)

        archetype_names = {
            0: "🌱 The Frugal Saver (Disciplined, minimal wants)",
            1: "🦋 The Social Butterfly (High wants & leisure)",
            2: "⚖️ The Balanced Budgeter (Moderate & steady)",
            3: "🔬 The Academic Investor (Targeted essential spends)"
        }

        # Predict user cluster from actual user feature vector
        user_features = np.array([[user_total_spend, user_discretionary_ratio, user_frequency, user_avg_tx]])
        user_scaled = scaler.transform(user_features)
        user_cluster = int(kmeans.predict(user_scaled)[0])

        cohort_df["Archetype"] = cohort_df["Cluster"].map(archetype_names)
        user_archetype_label = archetype_names[user_cluster]

        # User Profile Box in Exact Dark Theme
        st.markdown(f"""
        <div class="cluster-box">
            <span class="cluster-tag">YOUR CLUSTER RESULT</span>
            <div class="cluster-title">{user_archetype_label}</div>
            <p style="color: #f3e8ff; margin: 0; font-size: 0.95rem;">
                Based on your actual monthly burn rate of <b style="color: #c084fc;">₹{user_total_spend:,.2f}</b> and discretionary ratio of <b style="color: #c084fc;">{user_discretionary_ratio:.1f}%</b> from <b>expenses.csv</b>, the K-Means algorithm classifies your spending profile into this archetype.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Scatter Plot
        st.markdown("##### 🗺️ 2D Cluster Space: Discretionary Spending Ratio vs Total Spend")

        fig_cluster = px.scatter(
            cohort_df,
            x="Discretionary_Ratio",
            y="Total_Spend",
            color="Archetype",
            size="Txn_Frequency",
            hover_data=["Avg_Txn_Amount"],
            color_discrete_sequence=["#10b981", "#e879f9", "#7c3aed", "#38bdf8"],
            labels={"Discretionary_Ratio": "Discretionary Spending Ratio (%)", "Total_Spend": "Monthly Total Spend (₹)"}
        )

        # Add User marker
        fig_cluster.add_trace(go.Scatter(
            x=[user_discretionary_ratio],
            y=[user_total_spend],
            mode="markers+text",
            marker=dict(symbol="star", size=24, color="#e879f9", line=dict(width=2, color="#ffffff")),
            name="⭐ YOU ARE HERE",
            text=["⭐ YOU ARE HERE"],
            textposition="top center",
            textfont=dict(color="#f3e8ff", size=13, family="sans-serif")
        ))

        
        cluster_layout = DARK_LAYOUT.copy()
cluster_layout.update({
    "legend": dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    "height": 450
})

fig_cluster.update_layout(**cluster_layout)
st.plotly_chart(fig_cluster, use_container_width=True)

st.markdown("---")

# Archetype Characteristics Table
st.markdown("##### 📋 Student Spending Archetype Benchmark Table")
summary_archetypes = cohort_df.groupby("Archetype")[["Total_Spend", "Discretionary_Ratio", "Txn_Frequency", "Avg_Txn_Amount"]].mean().reset_index()
summary_archetypes.columns = ["Student Archetype", "Avg Monthly Spend (₹)", "Discretionary Ratio (%)", "Monthly Txns", "Avg Txn Size (₹)"]
summary_archetypes["Avg Monthly Spend (₹)"] = summary_archetypes["Avg Monthly Spend (₹)"].apply(lambda x: f"₹{x:,.2f}")
summary_archetypes["Discretionary Ratio (%)"] = summary_archetypes["Discretionary Ratio (%)"].apply(lambda x: f"{x:.1f}%")
summary_archetypes["Monthly Txns"] = summary_archetypes["Monthly Txns"].apply(lambda x: f"{x:.0f} txns")
summary_archetypes["Avg Txn Size (₹)"] = summary_archetypes["Avg Txn Size (₹)"].apply(lambda x: f"₹{x:,.2f}")

st.dataframe(summary_archetypes, use_container_width=True, hide_index=True)

st.info("💡 **Model Methodology**: Feature standardization via `StandardScaler()`, followed by partition-based clustering with `KMeans(k=4, random_state=42)`. Your current financial profile is dynamically scaled and projected onto the trained feature space.")
