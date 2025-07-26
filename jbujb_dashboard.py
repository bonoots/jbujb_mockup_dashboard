import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="JBUJB Merchant Dashboard", layout="wide")

# Title
st.title("📊 JBUJB Merchant Insights Dashboard")

# Date Range Filter
st.sidebar.header("📅 Filters")
date_range = st.sidebar.date_input("Select date range", [datetime.date.today() - datetime.timedelta(days=7), datetime.date.today()])

st.sidebar.markdown("---")

# Dummy KPIs
total_qr_scans = 1525
conversion_rate = 12.3
repeat_visitors = 22
avg_order_value = 25.4
avg_scan_to_order_time = 7
orders_per_hour = 14

# KPI Overview
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total QR Scans", f"{total_qr_scans}")
col2.metric("Conversion Rate", f"{conversion_rate}%")
col3.metric("Repeat Visitors", f"{repeat_visitors}%")
col4.metric("Avg. Order Value", f"${avg_order_value}")

# Charts Section
st.subheader("📈 Traffic Overview")
traffic_data = pd.DataFrame({
    "Day": pd.date_range(end=datetime.date.today(), periods=7),
    "QR Scans": np.random.randint(100, 300, size=7)
})
st.line_chart(traffic_data.set_index("Day"))

# Top Items
st.subheader("🍔 Top Viewed Menu Items")
top_items = pd.DataFrame({
    "Item": ["Burger", "Fries", "Salad"],
    "Views": [300, 200, 150]
})
st.bar_chart(top_items.set_index("Item"))

# Location Performance
st.subheader("📍 Location Performance")
location_perf = pd.DataFrame({
    "Location": ["Location A", "Location B", "Location C", "Location D"],
    "Revenue": [2400, 1800, 950, 3000]
})
st.bar_chart(location_perf.set_index("Location"))

# Device Type
st.subheader("📱 Customer Device Insights")
st.progress(0.79)  # 79% use mobile

# Footer
st.markdown("---")
st.caption("JBUJB QR Insights Dashboard — v1.0")
