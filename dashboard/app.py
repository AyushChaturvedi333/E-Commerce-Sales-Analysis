import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/ecommerce_sales.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df


df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("🛒 E-Commerce Sales Analysis Dashboard")
st.markdown("### Sales, Profit and Customer Insights")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

# Region
regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

# Category
categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

# Customer Segment
segments = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Customer_Segment"].unique()),
    default=sorted(df["Customer_Segment"].unique())
)

# Payment Mode
payments = st.sidebar.multiselect(
    "Payment Mode",
    options=sorted(df["Payment_Mode"].unique()),
    default=sorted(df["Payment_Mode"].unique())
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Customer_Segment"].isin(segments)) &
    (df["Payment_Mode"].isin(payments))
].copy()

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

if "Profit" in filtered_df.columns:
    total_profit = filtered_df["Profit"].sum()
else:
    total_profit = 0

avg_order_value = total_sales / total_orders if total_orders else 0

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "🛍️ Quantity Sold",
    f"{total_quantity:,}"
)

col4.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.2f}"
)

col5.metric(
    "🧾 Avg Order Value",
    f"₹{avg_order_value:,.2f}"
)

st.divider()

# -----------------------------
# SALES BY CATEGORY
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

# -----------------------------
# SALES BY REGION
# -----------------------------
with col2:
    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_region = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales by Region",
        hole=0.4
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
monthly_sales = (
    filtered_df
    .set_index("Order_Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order_Date",
    y="Sales",
    markers=True,
    title="📅 Monthly Sales Trend"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# -----------------------------
# PROFIT BY CATEGORY
# -----------------------------
if "Profit" in filtered_df.columns:

    profit_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
    )

    fig_profit = px.bar(
        profit_category,
        x="Category",
        y="Profit",
        title="📈 Profit by Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

# -----------------------------
# TOP PRODUCTS
# -----------------------------
st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products.sort_values("Sales"),
    x="Sales",
    y="Product",
    orientation="h",
    title="Top 10 Products by Sales",
    text_auto=".2s"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "E-Commerce Sales Analysis | Built with Python, Pandas, Plotly and Streamlit"
)