import streamlit as st
import pandas as pd
import plotly.express as px
from style import *
from utils import *

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Inventory Analytics",
    page_icon="📦",
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
df["Revenue"] = (
    df["quantity_sold"] *
    df["unit_price"]
)

# ==========================
# PAGE HEADER
# ==========================

page_header("📋 Inventory Analysis","Monitor inventory health, stockouts, reorder planning and demand patterns.")

# ==========================
# KPI SECTION
# ==========================

avg_inventory = int(df["inventory_level"].mean())
total_stockouts = int(df["stockout_indicator"].mean())
avg_reorder = int(df["reorder_quantity"].mean())
avg_lead_time = round(df["supplier_lead_time"].mean())

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1,"📦 Average Inventory",f"{avg_inventory:,}",color="purple")
kpi_card(c2,"⚠️ Stockouts",f"{total_stockouts:,}",color="orange")
kpi_card(c3,"🔄 Average Reorder Qty",f"{avg_reorder:,}",color="cyan")
kpi_card(c4,"🚚 Lead Time",f"{avg_lead_time} Days",color="yellow")

c1, c2 = st.columns(2)
with c1:
    section_header("📈 Inventory Trend")
    chart_label("📌 Average inventory levels over time.")
    inventory_trend = df.groupby("transaction_date")["inventory_level"].mean().reset_index()
    fig = px.line(inventory_trend,x="transaction_date",y="inventory_level")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Monitoring inventory trends helps identify seasonal fluctuations, inventory shortages, and excess stock situations.")

with c2:
    section_header("📦 Stockouts Distribution")
    chart_label("📌 Distribution of stockout and non-stockout events.")
    stockout_dist = df["stockout_indicator"].value_counts().reset_index()
    stockout_dist.columns = ["Stockout","Count"]
    fig = px.pie(stockout_dist,names="Stockout",values="Count")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Frequent stockouts may result in lost sales and reduced customer satisfaction. Improving replenishment planning can mitigate these risks.")

c3, c4 =st.columns(2)
with c3:
    section_header("⚠️ Top 10 Products with Highest Stockouts")
    chart_label("📌 Top 10 products experiencing the highest number of stockout events.")
    stockout_products = (df.groupby("product_name")["stockout_indicator"].sum().sort_values(ascending=False).head(10).reset_index())
    fig = px.bar(stockout_products,x="stockout_indicator",y="product_name",orientation="h",color="product_name")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 These products frequently run out of stock, indicating potential inventory planning issues. Increasing safety stock levels, improving demand forecasting, or adjusting reorder points can help reduce lost sales and improve product availability.")

# ==========================
# REORDER ANALYSIS
# ==========================
with c4:
    section_header("🔄 Reorder Analysis")
    chart_label("📌 Average reorder quantity across product categories.")
    reorder_data = df.groupby("category").agg(Avg_Reorder=("reorder_quantity","mean"),Avg_Inventory=("inventory_level","mean")).reset_index()
    fig = px.bar(reorder_data,x="category",y="Avg_Reorder",color="category")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Categories with higher reorder quantities may require closer monitoring to maintain optimal inventory levels.")

# ==========================
# DEMAND VS INVENTORY
# ==========================

c5, c6 = st.columns(2)
with c5:
    section_header("🔥 Demand vs Inventory")
    chart_label("📌 Relationship between average inventory levels and customer demand.")
    demand_inventory = df.groupby("product_name").agg(Inventory=("inventory_level","mean"),Demand=("actual_demand","mean")).reset_index()
    fig = px.scatter(demand_inventory,x="Inventory",y="Demand",hover_data="product_name")
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Products with high demand but low inventory levels are at greater risk of stockouts and should be prioritized for replenishment.")

# ==========================
# FORECAST VS ACTUAL DEMAND
# ==========================

with c6:
    section_header("📈 Foreast vs Actual Demand")
    chart_label("📌 Comparison between forecasted demand and actual customer demand.")
    forecast_df = df.groupby("transaction_date").agg(Forecasted_Demand=("forecasted_demand","sum"),Actual_Demand=("actual_demand","sum")).reset_index()
    fig = px.line(forecast_df,x="transaction_date",y=["Forecasted_Demand","Actual_Demand"])
    apply_plot_layout(fig)
    st.plotly_chart(fig,use_container_width=True)
    chart_note("💡 Smaller gaps between forecasted and actual demand indicate better forecasting accuracy and more efficient inventory planning.")

# ==========================
# SUPPLIER ANALYSIS
# ==========================

section_header("🚚 Supplier Analysis")
chart_label("📌 Average supplier lead time across suppliers.")
supplier_df = df.groupby("supplier_id")["supplier_lead_time"].mean().reset_index()
fig = px.bar(supplier_df,x="supplier_id",y="supplier_lead_time",color="supplier_lead_time")
apply_plot_layout(fig)
st.plotly_chart(fig,use_container_width=True)
chart_note("💡 Suppliers with longer lead times may increase inventory risk and require larger safety stock levels.")

# ==========================
# INVENTORY TABLE
# ==========================

section_header("📦 Inventory Summary Table")
chart_label("📌 Detailed inventory metrics including stock levels, reorder points, and stockout occurrences.")
inventory_table = df.groupby(["product_name", "category"]).agg(Inventory_Level=("inventory_level", "mean"),Reorder_Point=("reorder_point", "mean"),
        Reorder_Quantity=("reorder_quantity", "mean"),Stockouts=("stockout_indicator", "sum")).reset_index()
inventory_table = inventory_table.rename(columns={
    "product_name": "📦 Product Name",
    "category": "🏷️ Category",
    "Inventory_Level": "📊 Inventory Level",
    "Reorder_Point": "🔄 Reorder Point",
    "Reorder_Quantity": "📥 Reorder Quantity",
    "Stockouts": "⚠️ Stockouts"
})
st.dataframe(inventory_table,use_container_width=True,hide_index=True)
chart_note("💡 This table helps identify products that require inventory optimization, replenishment adjustments, or stockout prevention measures.")

# ==========================
# INSIGHT
# ==========================

section_header("🏢 Inventory Insights")
stockout_data = (df.groupby("product_name")["stockout_indicator"].sum().sort_values(ascending=False))
high_stockout_product = stockout_data.index[0]
stockout_count = stockout_data.iloc[0]
demand_data = (df.groupby("product_name")["actual_demand"].sum().sort_values(ascending=False))
highest_demand_product = demand_data.index[0]
demand_units = demand_data.iloc[0]
insight_card(f"⚠️ Highest Stockout Product: {high_stockout_product}<br><small>Stockout Events: {stockout_count:,.0f}</small>", kind="warning")
insight_card(f"📈 Highest Demand Product: {highest_demand_product}<br><small>Total Demand: {demand_units:,.0f} Units</small>",kind="success")
insight_card("🔄 Frequent stockouts indicate inventory shortages and potential lost sales opportunities.",kind="info")
insight_card("🎯 Align reorder policies with forecasted demand to minimize stockouts while avoiding excess inventory costs.",kind="success")
