import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# Page configuration
st.set_page_config(page_title="JBUJB Merchant Dashboard", layout="wide")

# Custom CSS for white background, orange headers, black text, and dark gray metric values
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    
    .main .block-container {
        background-color: white;
        color: #000000;
    }
    
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #FF6B35 !important;
    }
    
    .metric-container {
        background-color: white;
        border: 2px solid #FF6B35;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    
    .stMetric {
        color: #333333 !important;
    }
    
    .stMetric label {
        color: #FF6B35 !important;
    }
    
    .stSelectbox label, .stDateInput label {
        color: #FF6B35 !important;
    }
    
    .sidebar .sidebar-content {
        background-color: white;
    }
    
    .stDataFrame, .stTable {
        color: #000000;
    }
    
    .stPlotlyChart {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 JBUJB Merchant Insights Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

# Date filter options
filter_option = st.sidebar.selectbox(
    "Select Time Period",
    ["Today", "Yesterday", "This Week", "Last Week", "Custom Date Range"]
)

# Calculate date ranges based on selection
today = datetime.date.today()
yesterday = today - timedelta(days=1)
week_start = today - timedelta(days=today.weekday())
last_week_start = week_start - timedelta(days=7)
last_week_end = week_start - timedelta(days=1)

if filter_option == "Today":
    start_date, end_date = today, today
elif filter_option == "Yesterday":
    start_date, end_date = yesterday, yesterday
elif filter_option == "This Week":
    start_date, end_date = week_start, today
elif filter_option == "Last Week":
    start_date, end_date = last_week_start, last_week_end
else:  # Custom Date Range
    date_range = st.sidebar.date_input(
        "Select custom date range", 
        [today - timedelta(days=7), today]
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = today - timedelta(days=7), today

st.sidebar.markdown(f"**Selected Period:** {start_date} to {end_date}")
st.sidebar.markdown("---")

# Generate sample data based on date range
days_in_range = (end_date - start_date).days + 1

# Sample KPI data (in real implementation, this would come from your database)
def generate_sample_data(days):
    np.random.seed(42)  # For consistent demo data
    base_multiplier = max(1, days / 7)  # Scale based on date range
    
    total_qr_scans = int(np.random.randint(100, 300) * base_multiplier)
    total_orders = int(total_qr_scans * 0.123)  # 12.3% conversion
    total_revenue = total_orders * np.random.uniform(20, 35)
    
    return {
        'total_qr_scans': total_qr_scans,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_time_scan_to_order': np.random.uniform(5, 12),
        'avg_order_value': total_revenue / max(total_orders, 1),
        'canceled_orders': int(total_orders * np.random.uniform(0.05, 0.15)),
        'repeat_visitors_pct': np.random.uniform(15, 30),
        'avg_session_duration': np.random.uniform(3, 8),
        'bounce_rate': np.random.uniform(25, 45),
        'coupon_redemption_rate': np.random.uniform(8, 20),
        'item_conversion_rate': np.random.uniform(15, 35),
        'customer_retention_rate': np.random.uniform(20, 40),
        'avg_fulfillment_time': np.random.uniform(10, 20)
    }

data = generate_sample_data(days_in_range)

# KPI Overview Section
st.subheader("📊 Key Performance Indicators")

# First row of KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Total QR Scans", f"{data['total_qr_scans']:,}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    conversion_rate = (data['total_orders'] / data['total_qr_scans'] * 100) if data['total_qr_scans'] > 0 else 0
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Average Order Value", f"{data['avg_order_value']:.0f} MAD")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Total Revenue", f"{data['total_revenue']:.0f} MAD")
    st.markdown('</div>', unsafe_allow_html=True)

# Second row of KPIs
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Avg Time Scan to Order", f"{data['avg_time_scan_to_order']:.1f} min")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Canceled Orders", f"{data['canceled_orders']}")
    st.markdown('</div>', unsafe_allow_html=True)

with col7:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Repeat Visitors", f"{data['repeat_visitors_pct']:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col8:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Customer Retention Rate", f"{data['customer_retention_rate']:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Third row of KPIs
col9, col10, col11, col12 = st.columns(4)

with col9:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Avg Session Duration", f"{data['avg_session_duration']:.1f} min")
    st.markdown('</div>', unsafe_allow_html=True)

with col10:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Bounce Rate", f"{data['bounce_rate']:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col11:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Coupon Redemption Rate", f"{data['coupon_redemption_rate']:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col12:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Avg Fulfillment Time", f"{data['avg_fulfillment_time']:.1f} min")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Charts Section
col_left, col_right = st.columns(2)

with col_left:
    # Traffic Overview
    st.subheader("QR Scans Traffic Overview")
    traffic_dates = pd.date_range(start=start_date, end=end_date)
    traffic_data = pd.DataFrame({
        "Date": traffic_dates,
        "QR Scans": np.random.randint(50, 200, size=len(traffic_dates))
    })
    
    fig_traffic = px.line(traffic_data, x="Date", y="QR Scans", 
                         color_discrete_sequence=['#FF6B35'])
    fig_traffic.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#000000'
    )
    st.plotly_chart(fig_traffic, use_container_width=True)

with col_right:
    # Time of Day Analysis
    st.subheader("Peak Usage Hours")
    hours = list(range(8, 23))  # 8 AM to 10 PM
    usage_data = pd.DataFrame({
        "Hour": [f"{h}:00" for h in hours],
        "Orders": np.random.randint(5, 50, size=len(hours))
    })
    
    fig_hours = px.bar(usage_data, x="Hour", y="Orders",
                      color_discrete_sequence=['#FF6B35'])
    fig_hours.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#000000'
    )
    st.plotly_chart(fig_hours, use_container_width=True)

# Menu Items Analysis
st.subheader("Menu Items Performance")

col_items1, col_items2 = st.columns(2)

with col_items1:
    st.write("**Top Viewed Menu Items**")
    top_viewed = pd.DataFrame({
        "Item": ["Tagine Chicken", "Couscous Royal", "Pastilla", "Harira Soup", "Mint Tea"],
        "Views": [450, 380, 320, 280, 250],
        "Orders": [95, 85, 70, 65, 60]
    })
    top_viewed["Conversion Rate"] = (top_viewed["Orders"] / top_viewed["Views"] * 100).round(1)
    st.dataframe(top_viewed, use_container_width=True)

with col_items2:
    st.write("**Most Ordered Items**")
    most_ordered = pd.DataFrame({
        "Item": ["Couscous Royal", "Tagine Chicken", "Pastilla", "Harira Soup", "Lamb Kebab"],
        "Orders": [95, 90, 78, 65, 58],
        "Revenue (MAD)": [2375, 2250, 1950, 975, 1450]
    })
    st.dataframe(most_ordered, use_container_width=True)

# Menu Category Performance
st.subheader("Menu Category Performance")
category_data = pd.DataFrame({
    "Category": ["Mains", "Appetizers", "Desserts", "Beverages"],
    "Orders": [250, 150, 80, 120],
    "Revenue (MAD)": [6250, 2250, 1200, 960]
})
fig_category = px.bar(category_data, x="Category", y="Orders", 
                     color_discrete_sequence=['#FF6B35'],
                     title="Orders by Menu Category")
fig_category.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='#000000'
)
st.plotly_chart(fig_category, use_container_width=True)
st.dataframe(category_data, use_container_width=True)

# Low Performing Items
st.subheader("⚠Items Needing Attention")
low_performing = pd.DataFrame({
    "Item": ["Vegetarian Tagine", "Fish Pastilla", "Almond Cookies"],
    "Views": [120, 85, 95],
    "Orders": [8, 5, 12],
    "Conversion Rate": [6.7, 5.9, 12.6],
    "Issue": ["Low conversion", "Low views", "Average performance"]
})
st.dataframe(low_performing, use_container_width=True)

# Coupons Performance
st.subheader("Coupon Performance")
col_coupon1, col_coupon2 = st.columns(2)

with col_coupon1:
    coupon_data = pd.DataFrame({
        "Coupon": ["WELCOME10", "LUNCH15", "DINNER20", "WEEKEND25"],
        "Distributed": [500, 300, 200, 150],
        "Used": [85, 45, 32, 28],
        "Redemption Rate": [17.0, 15.0, 16.0, 18.7]
    })
    st.dataframe(coupon_data, use_container_width=True)

with col_coupon2:
    fig_coupon = px.bar(coupon_data, x="Coupon", y="Redemption Rate",
                       color_discrete_sequence=['#FF6B35'],
                       title="Coupon Redemption Rates")
    fig_coupon.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='#000000'
    )
    st.plotly_chart(fig_coupon, use_container_width=True)

# Customer-Level Insights
st.subheader("👤 Top Customer Insights")

col_cust1, col_cust2 = st.columns(2)

with col_cust1:
    st.write("**Top Customers by Spend**")
    top_customers = pd.DataFrame({
        "Customer ID": ["CUST001", "CUST002", "CUST003", "CUST004"],
        "Total Spend (MAD)": [1250, 980, 750, 620],
        "Order Count": [10, 8, 6, 5]
    })
    st.dataframe(top_customers, use_container_width=True)

with col_cust2:
    st.write("**Customer Order Frequency**")
    order_freq = pd.DataFrame({
        "Customer ID": ["CUST001", "CUST002", "CUST003", "CUST004"],
        "Orders": [10, 8, 6, 5],
        "Last Order Date": [
            (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            (today - timedelta(days=5)).strftime("%Y-%m-%d"),
            (today - timedelta(days=10)).strftime("%Y-%m-%d"),
            (today - timedelta(days=15)).strftime("%Y-%m-%d")
        ]
    })
    st.dataframe(order_freq, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #FF6B35;">JBUJB QR Insights Dashboard — Enhanced v3.1</p>', 
    unsafe_allow_html=True
)
