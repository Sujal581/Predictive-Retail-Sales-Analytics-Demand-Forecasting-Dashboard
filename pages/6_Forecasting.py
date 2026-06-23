import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from style import *
from utils import *

# ==========================
# PAGE CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
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
df=sidebar_filters(df)

# ==========================
# PAGE HEADER
# ==========================

page_header("📈 Demand Forecasting","Demand analysis using actual and forecasted demand values.")

# ==========================
# KPI SECTION
# ==========================

df["forecast_error"]=df["actual_demand"]-df["forecasted_demand"]

mae=mean_absolute_error(df["actual_demand"],df["forecasted_demand"])
rmse=mean_squared_error(df["actual_demand"],df["forecasted_demand"])**0.5
accuracy=r2_score(df["actual_demand"],df["forecasted_demand"])*100

avg_actual=df["actual_demand"].mean()
avg_forecast=df["forecasted_demand"].mean()
max_error=abs(df["forecast_error"]).max()

c1,c2,c3,c4,c5=st.columns(5)
kpi_card(c1,"🎯 Forecast Accuracy",f"{accuracy:.1f}%",color="green")
kpi_card(c2,"📉 MAE",f"{mae:.1f}",color="red")
kpi_card(c3,"📊 RMSE",f"{rmse:.1f}",color="orange")
kpi_card(c4,"📦 Avg Actual Demand",f"{avg_actual:,.0f}",color="cyan")
kpi_card(c5,"⚠️ Max Error",f"{max_error:,.0f}",color="yellow")

# ==========================
# ACTUAL VS FORECASTED CHART
# ==========================

section_header("📈 Actual vs Forecasted Demand")
chart_label("Comparison between actual demand and forecasted demand over time")
daily_forecast=df.groupby("transaction_date")[["actual_demand","forecasted_demand"]].mean().reset_index()
fig=go.Figure()
fig.add_trace(go.Scatter(x=daily_forecast["transaction_date"],y=daily_forecast["actual_demand"],mode="lines",name="Actual Demand"))
fig.add_trace(go.Scatter(x=daily_forecast["transaction_date"],y=daily_forecast["forecasted_demand"],mode="lines",name="Forecasted Demand"))
apply_plot_layout(fig)
st.plotly_chart(fig,use_container_width=True)
chart_note("💡 Daily average demand comparison shows how closely forecasted values follow actual demand.")

# ==========================
# FORECAST ERROR ANALYSIS
# ==========================

section_header("📉 Forecast Error Analysis")
chart_label("Distribution of errors between actual demand and forecasted demand")
fig=px.histogram(df,x="forecast_error",title="Forecast Error Distribution")
apply_plot_layout(fig)
st.plotly_chart(fig,use_container_width=True)
chart_note("💡 Lower forecast error means the demand prediction is more reliable.")

# ==========================
# DEMAND TREND ANALYSIS
# ==========================

section_header("📊 Demand Trend Analysis")
chart_label("Average actual and forecasted demand pattern")
trend_df=df.groupby("transaction_date")[["actual_demand","forecasted_demand"]].mean().reset_index()
fig=px.line(trend_df,x="transaction_date",y=["actual_demand","forecasted_demand"])
apply_plot_layout(fig)
st.plotly_chart(fig,use_container_width=True)
chart_note("💡 Trend comparison helps identify demand changes and forecasting patterns.")

# ==========================
# FORECAST SUMMARY TABLE
# ==========================

section_header("📋 Forecast Summary Table")
chart_label("Detailed comparison of actual demand, forecasted demand, and prediction error")
summary=df[["transaction_date","actual_demand","forecasted_demand","forecast_error"]]
summary=summary.rename(columns={"transaction_date":"📅 Date","actual_demand":"📦 Actual Demand",
    "forecasted_demand":"🔮 Forecasted Demand","forecast_error":"⚠️ Forecast Error"})
st.dataframe(summary,use_container_width=True,hide_index=True)
chart_note("💡 This table helps review forecast accuracy for each transaction date.")

# ==========================
# FORECAST INSIGHTS
# ==========================

section_header("🏢 Forecast Insights")
best_day=df.loc[df["forecasted_demand"].idxmax(),"transaction_date"]
insight_card(f"🤖 Forecast Model: Existing Demand Forecast<br><small>Accuracy: {accuracy:.1f}%</small>",kind="success")
insight_card(f"📈 Highest Forecast Demand Date: {best_day.date()} ",kind="info")
insight_card(f"📦 Average Forecast Demand: {avg_forecast:,.0f} Units",kind="success")
insight_card(f"📉 Forecast Error Level: {mae:,.1f}<br><small>Lower error improves business planning</small>",kind="info")
insight_card("🎯 Use forecast results for inventory planning, demand management, and operational decisions.",kind="warning")