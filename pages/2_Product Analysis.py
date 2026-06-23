import streamlit as st
import pandas as pd
import plotly.express as px
from style import *
from utils import *

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Business Recommendations",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded")

# ==========================
# STYLE
# ==========================

inject_css()
sidebar_brand()

# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():
    df = pd.read_csv("data/Walmart.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df

df = load_data()
df=sidebar_filters(df)
# Revenue Column
df["Revenue"] = (df["quantity_sold"] *df["unit_price"])

# ==========================
# PAGE HEADER
# ==========================

page_header("📦 Product Analysis","Analyze product performance, category contribution and revenue generation.")

# ==========================
# KPI SECTIONS
# ==========================

top_product = df.groupby("product_name")["quantity_sold"].sum().idxmax()
top_category = df.groupby("category")["Revenue"].sum().idxmax()
total_product = df["product_name"].nunique()
avg_product = round(df.groupby("product_name")["quantity_sold"].sum().mean(),0)

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1,"📦 Total Product",total_product,color="red")
kpi_card(c2,"🏆 TOp Product",top_category,color="blue")
kpi_card(c3,"💰 Top Category",top_category,color="orange")
kpi_card(c4,"📈 Avg Product Sales",avg_product,color="purple")

c1, c2 = st.columns(2)
# ==========================
# TOP 10 PRODUCT BY SALES
# ==========================

with c1:
    section_header("🏆 Top 10 Product by Sales")
    chart_label("📌 Top 10 products with the highest sales volume.")
    top_product = df.groupby("product_name")["quantity_sold"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_product,x="product_name",y="quantity_sold",color="product_name")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Chart Note: These products contribute the largest share of unit sales and should be prioritized for inventory planning and promotional campaigns.")

# ==========================
# TOP 10 PRODUCT BY REVENUE
# ==========================

with c2:
    section_header("🏆 Top 10 Product by Revenue")
    chart_label("📌 Top 10 products generating the highest revenue.")
    top_product = df.groupby("product_name")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_product,x="product_name",y="Revenue",color="product_name")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Chart Note: These products are the key revenue drivers and can be targeted for premium pricing and upselling strategies.")

# ==========================
# CATEGORY PERFORMANCE
# ==========================

c3, c4 = st.columns(2)
with c3:
    section_header("💰 Cateogry - Wise Sales")
    chart_label("📌 Total quantity sold across product categories.")
    category_sales = df.groupby("category")["quantity_sold"].sum().reset_index().sort_values("quantity_sold",ascending=False)
    fig = px.bar(category_sales,x="category",y="quantity_sold",color="category")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Chart Note: Categories with higher sales volumes indicate stronger customer demand and market preference.")

with c4:
    section_header("💸 Revenue Contribution by Category")
    chart_label("📌 Percentage contribution of each category to total revenue.")
    category_revenue = df.groupby("category")["Revenue"].sum().reset_index()
    fig = px.pie(category_revenue,names="category",values="Revenue")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Chart Note: Categories with larger revenue shares have the greatest impact on business profitability.")
     
# ==========================
# PRODUCT PERFORMING TABLE
# ==========================

section_header("🗒️ Product Performance Table")
chart_label("📌 Detailed product-level performance metrics.")
product_table = df.groupby(["product_name","category"]).agg(
    Quantity_Sold=("quantity_sold","sum"),
    Revenue=("Revenue","sum"),
    Avg_Price=("unit_price","mean")).reset_index().sort_values("Revenue",ascending=False)
product_table = product_table.rename(columns={"product_name": "📦 Product Name","category": "🏷️ Category","Quantity_Sold": "📊 Units Sold",
    "Revenue": "💰 Total Revenue ($)","Avg_Price": "💵 Average Price ($)"})
product_table["💵 Average Price ($)"] = product_table["💰 Total Revenue ($)"].round(0).astype(int)
product_table["💵 Average Price ($)"] = product_table["💵 Average Price ($)"].round(0).astype(int)
st.dataframe(product_table,use_container_width=True,hide_index=True)
chart_note("💡 Table Note: Compare product sales, revenue, and pricing performance to identify top-performing and underperforming products.")

# ==========================
# LOW PERFORMING PRODUCT
# ==========================

section_header("📉 Low Performing Product")
chart_label("📌 Bottom 10 products based on revenue generation.")
product_table = df.groupby("product_name")["Revenue"].sum().sort_values().head(10).reset_index()
fig = px.bar(product_table,x="Revenue",y="product_name",orientation="h",color="product_name")
apply_plot_layout(fig)
st.plotly_chart(fig,use_container_width=True)
chart_note("💡 Chart Note: These products generate the least revenue and may require promotional efforts, pricing review, or inventory optimization.")

# ==========================
# INSIGHT
# ==========================

section_header("🏢 Business Insights")
best_product_data = (df.groupby("product_name")["quantity_sold"].sum().sort_values(ascending=False))
best_product = best_product_data.index[0]
best_product_sales = best_product_data.iloc[0]
best_category_data = (df.groupby("category")["Revenue"].sum().sort_values(ascending=False))
best_category = best_category_data.index[0]
best_category_revenue = best_category_data.iloc[0]
worst_product_data = (df.groupby("product_name")["Revenue"].sum().sort_values())
worst_product = worst_product_data.index[0]
worst_product_revenue = worst_product_data.iloc[0]

insight_card(f"📦 Best Selling Product: {best_product}<br><small>Total Units Sold: {best_product_sales:,.0f}</small>",kind="success")
insight_card(f"📈 Highest Revenue Category: {best_category}<br><small>Total Revenue: ₹{best_category_revenue:,.2f}</small>",kind="success")
insight_card(f"📉 Lowest Performing Product: {worst_product}<br><small>Total Revenue: ₹{worst_product_revenue:,.2f}</small>",kind="warning")