import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Generate Sample Data ---
np.random.seed(42)
account_managers = ['Alex Morgan', 'Jordan Taylor', 'Casey Lee', 'Jamie Parker']
customers = [f"Customer {i}" for i in range(1, 31)]
products = ['Product A', 'Product B', 'Product C', 'Product D']
payment_methods = ['Credit Card', 'Bank Transfer', 'PayPal', 'Invoice']
pipeline_stages = ['Initial Contact', 'Demo Scheduled', 'Negotiation', 'Closed Won', 'Closed Lost']

data = []
start_date = datetime(2024, 1, 1)
for customer in customers:
    am = random.choice(account_managers)
    contract_date = start_date + timedelta(days=random.randint(0, 250))
    turnaround_days = random.randint(1, 15)
    busiest_time = contract_date + timedelta(days=random.randint(0, 5))
    product = random.choice(products)
    payment = random.choice(payment_methods)
    value = random.randint(1000, 20000)
    pipeline = random.choice(pipeline_stages)

    data.append({
        'Account Manager': am,
        'Customer': customer,
        'Contract Date': contract_date,
        'Turnaround Time (days)': turnaround_days,
        'Busiest Interaction Date': busiest_time,
        'Product': product,
        'Payment Method': payment,
        'Contract Value': value,
        'Pipeline Stage': pipeline
    })

df = pd.DataFrame(data)

# --- Streamlit App Setup ---
st.set_page_config(page_title="Customer Engagement Dashboard", layout="wide")
st.title("📊 Customer Engagement Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filter by")
selected_am = st.sidebar.selectbox("Account Manager", options=["All"] + sorted(df["Account Manager"].unique().tolist()))
selected_product = st.sidebar.multiselect("Product", options=df["Product"].unique(), default=df["Product"].unique())
selected_payment = st.sidebar.multiselect("Payment Method", options=df["Payment Method"].unique(), default=df["Payment Method"].unique())
min_value, max_value = st.sidebar.slider("Contract Value Range", int(df["Contract Value"].min()), int(df["Contract Value"].max()), (int(df["Contract Value"].min()), int(df["Contract Value"].max())))

# --- Filter Logic ---
filtered_df = df[
    (df["Product"].isin(selected_product)) &
    (df["Payment Method"].isin(selected_payment)) &
    (df["Contract Value"].between(min_value, max_value))
]
if selected_am != "All":
    filtered_df = filtered_df[filtered_df["Account Manager"] == selected_am]

# --- KPI Metrics ---
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Contracts", len(filtered_df))
col2.metric("Avg. Turnaround (days)", f"{filtered_df['Turnaround Time (days)'].mean():.2f}")
col3.metric("Total Value", f"${filtered_df['Contract Value'].sum():,}")

# --- Visualizations ---
st.subheader("📊 Engagement Insights")
tab1, tab2 = st.tabs(["Turnaround & Volume", "Product & Pipeline"])

with tab1:
    st.markdown("**📅 Average Turnaround Over Time**")
    turnaround_chart = filtered_df.groupby('Contract Date')['Turnaround Time (days)'].mean()
    st.line_chart(turnaround_chart)

    st.markdown("**📈 Customer Engagement Volume**")
    volume_chart = filtered_df['Contract Date'].value_counts().sort_index()
    st.bar_chart(volume_chart)

with tab2:
    st.markdown("**📦 Sales by Product**")
    product_sales = filtered_df.groupby('Product')['Contract Value'].sum()
    st.bar_chart(product_sales)

    st.markdown("**🧭 Pipeline Overview**")
    st.dataframe(filtered_df[['Customer', 'Account Manager', 'Product', 'Pipeline Stage', 'Contract Value']].sort_values(by="Pipeline Stage"))

# --- Raw Data View ---
with st.expander("🔎 View Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True))
