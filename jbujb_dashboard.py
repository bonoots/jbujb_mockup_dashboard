import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta
import base64
import json

# ---------- Configuration ----------
st.set_page_config(
    page_title="JBUJB Merchant Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Enhanced CSS Styling ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #ff6a00 0%, #ff8533 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 106, 0, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .kpi-box {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e9ecef;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6a00, #ff8533);
    }
    
    .kpi-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(255, 106, 0, 0.15);
        border-color: #ff6a00;
    }
    
    .kpi-label {
        color: #6c757d;
        font-weight: 500;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        color: #212529;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .kpi-change {
        font-size: 12px;
        font-weight: 500;
        padding: 4px 8px;
        border-radius: 12px;
        display: inline-block;
    }
    
    .positive-change {
        background-color: #d4edda;
        color: #155724;
    }
    
    .negative-change {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .section-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 2rem 0 1rem 0;
        border-left: 5px solid #ff6a00;
    }
    
    .section-header h3 {
        color: #495057;
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    .alert-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffeaa7;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border-left: 6px solid #ffc107;
    }
    
    .alert-box h4 {
        color: #856404;
        margin: 0 0 10px 0;
        font-weight: 600;
    }
    
    .metric-positive {
        color: #28a745 !important;
    }
    
    .metric-negative {
        color: #dc3545 !important;
    }
    
    .sidebar-metric {
        background: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .data-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
    }
    
    .stDataFrame {
        border: none !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f3f4;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ff6a00;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #e55a00;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Enhanced Data Generation ----------
@st.cache_data
def generate_enhanced_data(days, seed=42):
    """Generate more realistic sample data with trends and patterns"""
    np.random.seed(seed)
    base_multiplier = max(1, days / 7)
    
    # Generate time series data
    dates = pd.date_range(start=datetime.date.today() - timedelta(days=days-1), 
                         end=datetime.date.today(), freq='D')
    
    # Create realistic patterns
    qr_scans_daily = []
    orders_daily = []
    revenue_daily = []
    
    for i, date in enumerate(dates):
        # Weekend boost
        weekend_multiplier = 1.3 if date.weekday() >= 5 else 1.0
        # Time trend (slight growth)
        trend_multiplier = 1 + (i * 0.02)
        
        daily_scans = int(np.random.normal(150, 30) * weekend_multiplier * trend_multiplier)
        daily_scans = max(daily_scans, 50)  # Minimum scans
        
        # Conversion rate varies
        conversion_rate = np.random.normal(0.12, 0.03)
        conversion_rate = max(0.05, min(0.25, conversion_rate))
        
        daily_orders = int(daily_scans * conversion_rate)
        daily_revenue = daily_orders * np.random.normal(28, 8)
        
        qr_scans_daily.append(daily_scans)
        orders_daily.append(daily_orders)
        revenue_daily.append(max(daily_revenue, 0))
    
    # Aggregate data
    total_qr_scans = sum(qr_scans_daily)
    total_orders = sum(orders_daily)
    total_revenue = sum(revenue_daily)
    
    # Calculate metrics
    data = {
        'total_qr_scans': total_qr_scans,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'conversion_rate': (total_orders / total_qr_scans * 100) if total_qr_scans > 0 else 0,
        'avg_order_value': total_revenue / max(total_orders, 1),
        'avg_time_scan_to_order': np.random.uniform(4, 8),
        'canceled_orders': int(total_orders * np.random.uniform(0.05, 0.12)),
        'repeat_visitors_pct': np.random.uniform(20, 35),
        'avg_session_duration': np.random.uniform(4, 10),
        'bounce_rate': np.random.uniform(20, 40),
        'coupon_redemption_rate': np.random.uniform(12, 25),
        'customer_retention_rate': np.random.uniform(25, 45),
        'avg_fulfillment_time': np.random.uniform(8, 15),
        'peak_hour': np.random.choice(['12:00', '13:00', '19:00', '20:00']),
        'top_category': 'Burgers',
        'qr_scans_daily': qr_scans_daily,
        'orders_daily': orders_daily,
        'revenue_daily': revenue_daily,
        'dates': dates
    }
    
    return data

# ---------- Logo at Top Left ----------
# Create a container for the logo at the top
logo_container = st.container()
with logo_container:
    # Create columns to position logo on the left
    logo_col, spacer_col = st.columns([1, 5])
    
    with logo_col:
        import os
        if os.path.exists("jbujb_logo_1.svg"):
            try:
                # Try direct SVG display first
                st.image("jbujb_logo_1.svg", width=150)
            except:
                try:
                    # Fallback: Embed SVG as HTML
                    with open("jbujb_logo_1.svg", "r") as f:
                        svg_content = f.read()
                    
                    st.markdown(f"""
                        <div style="width: 150px; height: auto;">
                            {svg_content}
                        </div>
                    """, unsafe_allow_html=True)
                except:
                    # Final fallback: Text logo
                    st.markdown("""
                        <div style="width: 150px; height: 60px; background: #ff6a00; color: white; 
                                    display: flex; align-items: center; justify-content: center; 
                                    font-weight: bold; font-size: 24px; border-radius: 8px;">
                            JBUJB
                        </div>
                    """, unsafe_allow_html=True)
        else:
            # Show fallback if file not found
            st.markdown("""
                <div style="width: 150px; height: 60px; background: #ff6a00; color: white; 
                            display: flex; align-items: center; justify-content: center; 
                            font-weight: bold; font-size: 24px; border-radius: 8px;">
                    JBUJB
                </div>
            """, unsafe_allow_html=True)
    
    with spacer_col:
        st.write("")  # Empty spacer

# ---------- Header ----------
st.markdown("""
    <div class="main-header">
        <h1> JBUJB Merchant Analytics</h1>
        <p>Real-time insights and performance metrics for your restaurant</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Enhanced Sidebar ----------
st.sidebar.markdown("### 📊 Dashboard Filters")

# Time period selection
filter_option = st.sidebar.selectbox(
    "Select Time Period",
    ["Today", "Yesterday", "This Week", "Last Week", "Last 30 Days", "Custom Date Range"],
    index=2
)

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
elif filter_option == "Last 30 Days":
    start_date, end_date = today - timedelta(days=30), today
else:
    date_range = st.sidebar.date_input(
        "Select custom date range", 
        [today - timedelta(days=7), today],
        max_value=today
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = today - timedelta(days=7), today

# Additional filters
st.sidebar.markdown("### 🎯 Additional Filters")
show_comparison = st.sidebar.checkbox("Show Period Comparison", value=True)
show_predictions = st.sidebar.checkbox("Show Trend Predictions", value=False)

# Quick stats in sidebar
days_in_range = (end_date - start_date).days + 1
data = generate_enhanced_data(days_in_range)

st.sidebar.markdown("### 📈 Quick Stats")
st.sidebar.metric("Period", f"{days_in_range} days")
st.sidebar.metric("Avg Daily Scans", f"{data['total_qr_scans']/days_in_range:.0f}")
st.sidebar.metric("Avg Daily Revenue", f"{data['total_revenue']/days_in_range:.0f} MAD")
st.sidebar.metric("Total QR Scans", f"{data['total_qr_scans']:,}")
st.sidebar.metric("Total Revenue", f"{data['total_revenue']:.0f} MAD")

# ---------- Enhanced KPI Section ----------
st.markdown('<div class="section-header"><h3>📊 Key Performance Indicators</h3></div>', unsafe_allow_html=True)

# Generate comparison data if enabled
comparison_data = None
if show_comparison and days_in_range > 1:
    comparison_data = generate_enhanced_data(days_in_range, seed=24)

# KPI calculations with comparisons
kpi_metrics = [
    {
        'label': 'Total QR Scans',
        'value': f"{data['total_qr_scans']:,}",
        'change': f"+{((data['total_qr_scans'] - comparison_data['total_qr_scans']) / comparison_data['total_qr_scans'] * 100):.1f}%" if comparison_data else None,
        'positive': data['total_qr_scans'] > (comparison_data['total_qr_scans'] if comparison_data else 0)
    },
    {
        'label': 'Conversion Rate',
        'value': f"{data['conversion_rate']:.1f}%",
        'change': f"{data['conversion_rate'] - (comparison_data['conversion_rate'] if comparison_data else 0):+.1f}%" if comparison_data else None,
        'positive': data['conversion_rate'] > (comparison_data['conversion_rate'] if comparison_data else 0)
    },
    {
        'label': 'Average Order Value',
        'value': f"{data['avg_order_value']:.0f} MAD",
        'change': f"{data['avg_order_value'] - (comparison_data['avg_order_value'] if comparison_data else 0):+.0f} MAD" if comparison_data else None,
        'positive': data['avg_order_value'] > (comparison_data['avg_order_value'] if comparison_data else 0)
    },
    {
        'label': 'Total Revenue',
        'value': f"{data['total_revenue']:,.0f} MAD",
        'change': f"+{((data['total_revenue'] - comparison_data['total_revenue']) / comparison_data['total_revenue'] * 100):.1f}%" if comparison_data else None,
        'positive': data['total_revenue'] > (comparison_data['total_revenue'] if comparison_data else 0)
    },
    {
        'label': 'Total Orders',
        'value': f"{data['total_orders']:,}",
        'change': f"{data['total_orders'] - (comparison_data['total_orders'] if comparison_data else 0):+}" if comparison_data else None,
        'positive': data['total_orders'] > (comparison_data['total_orders'] if comparison_data else 0)
    },
    {
        'label': 'Avg Session Duration',
        'value': f"{data['avg_session_duration']:.1f} min",
        'change': f"{data['avg_session_duration'] - (comparison_data['avg_session_duration'] if comparison_data else 0):+.1f} min" if comparison_data else None,
        'positive': data['avg_session_duration'] > (comparison_data['avg_session_duration'] if comparison_data else 0)
    },
    {
        'label': 'Bounce Rate',
        'value': f"{data['bounce_rate']:.1f}%",
        'change': f"{data['bounce_rate'] - (comparison_data['bounce_rate'] if comparison_data else 0):+.1f}%" if comparison_data else None,
        'positive': data['bounce_rate'] < (comparison_data['bounce_rate'] if comparison_data else 100)
    },
    {
        'label': 'Fulfillment Time',
        'value': f"{data['avg_fulfillment_time']:.1f} min",
        'change': f"{data['avg_fulfillment_time'] - (comparison_data['avg_fulfillment_time'] if comparison_data else 0):+.1f} min" if comparison_data else None,
        'positive': data['avg_fulfillment_time'] < (comparison_data['avg_fulfillment_time'] if comparison_data else 100)
    }
]

# Display KPIs using Streamlit columns (more reliable than custom HTML)
num_cols = 4
for i in range(0, len(kpi_metrics), num_cols):
    cols = st.columns(num_cols)
    for j, col in enumerate(cols):
        if i + j < len(kpi_metrics):
            kpi = kpi_metrics[i + j]
            with col:
                # Create custom metric display
                delta = kpi['change'] if kpi['change'] else None
                delta_color = "normal" if kpi['positive'] else "inverse"
                
                st.metric(
                    label=kpi['label'],
                    value=kpi['value'],
                    delta=delta,
                    delta_color=delta_color
                )

# ---------- Enhanced Charts Section ----------
st.markdown('<div class="section-header"><h3>📊 Performance Analytics</h3></div>', unsafe_allow_html=True)

# Create subplot dashboard
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Daily Performance Trends")
    
    # Multi-line chart
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Scatter(
        x=data['dates'], y=data['qr_scans_daily'],
        mode='lines+markers', name='QR Scans',
        line=dict(color='#ff6a00', width=3),
        marker=dict(size=6)
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=data['dates'], y=[x*10 for x in data['orders_daily']],  # Scale for visibility
        mode='lines+markers', name='Orders (×10)',
        line=dict(color='#28a745', width=3),
        marker=dict(size=6),
        yaxis='y2'
    ))
    
    fig_trends.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        hovermode='x unified',
        xaxis_title="Date",
        yaxis_title="QR Scans",
        yaxis2=dict(title="Orders (×10)", side="right", overlaying="y"),
        legend=dict(x=0, y=1.1, orientation="h"),
        font=dict(size=14, color="#000000")
    )
    
    # Ensure axis text is visible
    fig_trends.update_xaxes(tickfont=dict(color="#000000", size=12))
    fig_trends.update_yaxes(tickfont=dict(color="#000000", size=12))
    
    st.plotly_chart(fig_trends, use_container_width=True)

with col_right:
    st.subheader("⏰ Peak Usage Hours")
    
    # Enhanced hourly data
    hours = list(range(8, 23))
    hourly_base = [10, 15, 25, 45, 80, 120, 95, 85, 70, 90, 110, 85, 60, 40, 25]
    hourly_orders = [max(5, int(base * np.random.uniform(0.8, 1.2))) 
                    for base in hourly_base]
    
    fig_hours = go.Figure(data=[
        go.Bar(
            x=[f"{h:02d}:00" for h in hours],
            y=hourly_orders,
            marker_color=['#ff6a00' if val == max(hourly_orders) else '#ff8533' 
                         for val in hourly_orders],
            text=hourly_orders,
            textposition='outside'
        )
    ])
    
    fig_hours.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        xaxis_title="Hour of Day",
        yaxis_title="Orders",
        showlegend=False,
        font=dict(size=14, color="#000000")
    )
    
    # Ensure axis text is visible
    fig_hours.update_xaxes(tickfont=dict(color="#000000", size=12))
    fig_hours.update_yaxes(tickfont=dict(color="#000000", size=12))
    
    st.plotly_chart(fig_hours, use_container_width=True)

# ---------- Menu Performance Dashboard ----------
st.markdown('<div class="section-header"><h3>🍽️ Menu Performance Analytics</h3></div>', unsafe_allow_html=True)

col_menu1, col_menu2 = st.columns(2)

with col_menu1:
    st.write("**🏆 Top Performing Items**")
    top_items = pd.DataFrame({
        "Item": ["Big Bite", "Super Filet", "Maxi Grill", "Zinker", "Chicken Wings"],
        "Views": [485, 420, 385, 350, 320],
        "Orders": [118, 105, 92, 84, 78],
        "Revenue (MAD)": [2950, 2625, 2300, 1260, 1950],
        "Conversion %": [24.3, 25.0, 23.9, 24.0, 24.4]
    })
    
    st.dataframe(top_items, use_container_width=True)

with col_menu2:
    st.write("**📊 Category Performance**")
    category_data = pd.DataFrame({
        "Category": ["Burgers", "Sandwiches", "Fried Items", "Beverages", "Desserts"],
        "Orders": [285, 180, 95, 140, 85],
        "Revenue (MAD)": [7125, 2700, 1425, 1120, 2125],
        "Avg Order Value": [25.0, 15.0, 15.0, 8.0, 25.0]
    })
    
    st.dataframe(category_data, use_container_width=True)

# Category performance chart
fig_category = px.treemap(
    category_data, 
    path=['Category'], 
    values='Revenue (MAD)',
    color='Orders',
    color_continuous_scale='Oranges',
    title="Revenue Distribution by Category"
)
fig_category.update_layout(
    height=400,
    font=dict(size=14, color="#000000"),
    title_font=dict(size=16, color="#000000")
)
st.plotly_chart(fig_category, use_container_width=True)

# ---------- Alerts and Recommendations ----------
st.markdown('<div class="section-header"><h3>⚠️ Smart Alerts & Recommendations</h3></div>', unsafe_allow_html=True)

# Generate smart alerts based on data
alerts = []

# Bundle Suggestions Alert
alerts.append({
    'type': 'success',
    'title': 'Bundle Opportunity',
    'message': "Create 'Family Pack' combining top 3 items - potential 15% revenue increase."
})

# High-Value Customers Alert
alerts.append({
    'type': 'warning',
    'title': 'VIP Customer Engagement',
    'message': "5 VIP customers haven't ordered this week. Send personalized offers."
})

# Order Fulfillment Delays Alert
if data['avg_fulfillment_time'] > 12:
    alerts.append({
        'type': 'error',
        'title': 'Order Fulfillment Delays',
        'message': f"Average fulfillment time is {data['avg_fulfillment_time']:.1f} minutes (target: <12 min). Kitchen may be overwhelmed."
    })

# Declining Daily Orders Alert (simulated comparison)
import random
weekly_decline = random.uniform(8, 15)  # Simulate 8-15% decline
alerts.append({
    'type': 'warning',
    'title': 'Declining Daily Orders',
    'message': f"Orders down {weekly_decline:.0f}% compared to last week. Consider promotional campaigns."
})

# Menu Item Performance Alert
alerts.append({
    'type': 'info',
    'title': 'Menu Item Performance',
    'message': "3 items haven't been ordered in 7 days. Consider removing or promoting them."
})

# Display alerts using Streamlit's native components with enhanced styling
for alert in alerts:
    if alert['type'] == 'error':
        st.error(f"🔴 **{alert['title']}** - {alert['message']}")
    elif alert['type'] == 'warning':
        st.warning(f"🟠 **{alert['title']}** - {alert['message']}")
    elif alert['type'] == 'success':
        st.success(f"🟢 **{alert['title']}** - {alert['message']}")
    else:
        st.info(f"🟡 **{alert['title']}** - {alert['message']}")

# ---------- Customer Analytics ----------
st.markdown('<div class="section-header"><h3>👥 Customer Analytics</h3></div>', unsafe_allow_html=True)

col_cust1, col_cust2, col_cust3 = st.columns(3)

with col_cust1:
    st.write("**💰 Top Customers**")
    top_customers = pd.DataFrame({
        "Customer": ["VIP-001", "VIP-002", "VIP-003", "REG-004", "REG-005"],
        "Spend (MAD)": [1450, 1200, 980, 750, 650],
        "Orders": [12, 10, 8, 6, 5],
        "Frequency": ["Weekly", "Weekly", "Bi-weekly", "Monthly", "Monthly"]
    })
    st.dataframe(top_customers, use_container_width=True)

with col_cust2:
    st.write("**📊 Customer Segments**")
    segments = pd.DataFrame({
        "Segment": ["VIP", "Regular", "New", "At Risk"],
        "Count": [15, 45, 25, 8],
        "Avg Spend": [1200, 400, 150, 200]
    })
    
    fig_segments = px.pie(segments, values='Count', names='Segment', 
                         color_discrete_sequence=['#ff6a00', '#ff8533', '#ffb366', '#ffcc99'])
    fig_segments.update_layout(
        height=300,
        font=dict(size=14, color="#000000")
    )
    st.plotly_chart(fig_segments, use_container_width=True)

with col_cust3:
    st.write("**🎯 Retention Metrics**")
    st.metric("Customer Retention", f"{data['customer_retention_rate']:.1f}%")
    st.metric("Repeat Visitors", f"{data['repeat_visitors_pct']:.1f}%")
    st.metric("Avg Customer Lifetime", "4.2 months")
    st.metric("Churn Rate", f"{100-data['customer_retention_rate']:.1f}%")

# ---------- Export and Footer ----------
st.markdown("---")

col_export, col_info = st.columns([3, 1])

with col_export:
    if st.button("📊 Export Dashboard Data", type="primary"):
        # Create export data
        export_data = {
            'period': f"{start_date} to {end_date}",
            'kpis': kpi_metrics,
            'menu_performance': top_items.to_dict(),
            'generated_at': datetime.datetime.now().isoformat()
        }
        st.download_button(
            label="Download JSON Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"jbujb_report_{start_date}_{end_date}.json",
            mime="application/json"
        )

with col_info:
    st.info("💡 Dashboard auto-refreshes every 5 minutes")

st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 12px; margin-top: 2rem;">
    <h4 style="color: #ff6a00; margin: 0;"> JBUJB Enhanced Analytics Dashboard</h4>
    <p style="color: #6c757d; margin: 0.5rem 0 0 0;">Version 4.0 - Powered by Advanced Analytics & Real-time Insights</p>
</div>
""", unsafe_allow_html=True)
