import streamlit as st
import pandas as pd
from style import *

# ==========================
# PAGE CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Business Recommendations",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded")

# ==========================
# CUSTOM STYLE
# ==========================

inject_css()
sidebar_brand()

# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():
    df=pd.read_csv("data/Walmart.csv")
    df["transaction_date"]=pd.to_datetime(df["transaction_date"])
    return df

df=load_data()

# ==========================
# DATA CALCULATION
# ==========================

df["Revenue"]=df["quantity_sold"]*df["unit_price"]

# ==========================
# PAGE HEADER
# ==========================

page_header("🎯 Business Recommendations","AI-driven insights and strategic recommendations based on sales, inventory, customer, and demand analytics.")

# ==========================
# KPI SUMMARY
# ==========================

total_revenue=df["Revenue"].sum()
total_demand=df["actual_demand"].sum()
stockout_rate=df["stockout_indicator"].mean()*100

forecast_accuracy=100-(abs(df["forecasted_demand"]-df["actual_demand"])/df["actual_demand"].replace(0,1)).mean()*100

c1,c2,c3,c4=st.columns(4)

kpi_card(c1,"💰 Revenue",f"${total_revenue:,.0f}",color="green")
kpi_card(c2,"📦 Demand",f"{total_demand:,.0f}",color="orange")
kpi_card(c3,"⚠️ Stockout Rate",f"{stockout_rate:.1f}%",color="purple")
kpi_card(c4,"🎯 Forecast Accuracy",f"{forecast_accuracy:.1f}%",color="cyan")

# ==========================
# SALES STRATEGY
# ==========================

section_header("📈 Sales Strategy")
chart_label("Revenue-based product and category performance insights")
top_product=df.groupby("product_name")["Revenue"].sum().idxmax()
top_category=df.groupby("category")["Revenue"].sum().idxmax()
insight_card(f"🏆 Highest Revenue Product: {top_product}<br><small>Increase marketing focus and inventory availability</small>",kind="success")
insight_card(f"📦 Best Performing Category: {top_category}<br><small>Consider expanding category visibility</small>",kind="info")
chart_note("💡 Focus resources on products and categories generating maximum revenue.")

# ==========================
# INVENTORY OPTIMIZATION
# ==========================

section_header("📦 Inventory Optimization")
chart_label("Stockout analysis for improving inventory planning")
high_stockout=df.groupby("product_name")["stockout_indicator"].sum().idxmax()
insight_card(f"⚠️ Highest Stockout Product: {high_stockout}<br><small>Increase safety stock and reorder frequency</small>",kind="warning")
chart_note("💡 Reducing stockouts improves customer satisfaction and prevents lost sales.")

# ==========================
# CUSTOMER RETENTION
# ==========================

section_header("👥 Customer Retention")
chart_label("Customer segment analysis based on revenue contribution")
best_loyalty=df.groupby("customer_loyalty_level")["Revenue"].sum().idxmax()
insight_card(f"⭐ Valuable Customer Segment: {best_loyalty}<br><small>Create loyalty rewards and personalized offers</small>",kind="success")
chart_note("💡 Retaining high-value customers improves long-term revenue.")

# ==========================
# MARKETING PROMOTION
# ==========================

section_header("📢 Marketing & Promotions")
chart_label("Promotion performance based on generated revenue")
best_promo=df.groupby("promotion_type")["Revenue"].sum().idxmax()
insight_card(f"🎯 Best Promotion Type: {best_promo}<br><small>Prioritize during seasonal campaigns</small>",kind="info")
chart_note("💡 Use successful promotions to maximize campaign performance.")

# ==========================
# STORE PERFORMANCE
# ==========================

section_header("🌍 Store Performance")
chart_label("Comparison of store revenue performance")
best_store=df.groupby("store_location")["Revenue"].sum().idxmax()
weak_store=df.groupby("store_location")["Revenue"].sum().idxmin()
insight_card(f"🏆 Best Store: {best_store}",kind="success")
insight_card(f"📉 Lowest Performing Store: {weak_store}<br><small>Analyze operational issues</small>",kind="warning")
chart_note("💡 Apply successful strategies from top-performing locations.")

# ==========================
# FORECAST RECOMMENDATIONS
# ==========================

section_header("📈 Demand Forecasting")
chart_label("Future demand recommendation based on forecasted values")
future_avg=df["forecasted_demand"].tail(100).mean()
actual_avg=df["actual_demand"].tail(100).mean()
if future_avg>actual_avg:
    insight_card(f"📈 Demand Increase Expected<br><small>Forecasted Demand: {future_avg:.0f}</small><br>Recommendation: Prepare additional inventory.",kind="success")
else:
    insight_card(f"📉 Demand Decrease Expected<br><small>Forecasted Demand: {future_avg:.0f}</small><br>Recommendation: Reduce excess inventory.",kind="warning")
chart_note("💡 Forecast insights help optimize inventory and future planning.")

# ==========================
# EXECUTIVE SUMMARY
# ==========================

section_header("📋 Executive Summary")
chart_label("Key strategic actions generated from analytics")
st.markdown("""
### Key Strategic Actions

✅ Invest more in top-performing products and categories

✅ Improve inventory planning for stockout-prone products

✅ Strengthen loyalty programs for valuable customers

✅ Expand successful promotional campaigns

✅ Optimize low-performing stores

✅ Use forecasting for better inventory decisions

✅ Monitor demand accuracy regularly
""")
chart_note("💡 Data-driven recommendations help improve sales, profitability, and operational efficiency.")

# ==========================
# FINAL MESSAGE
# ==========================

insight_card("🚀 This dashboard converts retail data into actionable business intelligence for smarter decisions.",kind="success")