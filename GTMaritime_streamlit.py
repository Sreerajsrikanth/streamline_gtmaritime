import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(
    page_title="GTReplicate ROI Calculator",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme styling
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        color: white;
    }
    .stNumberInput > div > div > input {
        background-color: #2D2D2D;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚢 GTReplicate ROI Calculator")

# Create columns for input and visualization
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Fleet Information")
    vessels = st.number_input("Number of Vessels", min_value=1, value=10, step=1)
    
    st.subheader("Current Process Costs")
    data_per_vessel = st.number_input("Data Transfer per Vessel (GB/month)", min_value=1, value=50, step=1)
    bandwidth_cost = st.number_input("Bandwidth Cost (USD/GB)", min_value=1, value=30, step=1)
    monthly_hours = st.number_input("Monthly Manual Hours per Vessel", min_value=1, value=20, step=1)
    it_cost = st.number_input("IT Personnel Cost (USD/hour)", min_value=1, value=50, step=1)
    failure_rate = st.number_input("Monthly Transfer Failures per Vessel", min_value=0, value=5, step=1)
    failure_time = st.number_input("Hours per Failure Resolution", min_value=0, value=2, step=1)
    
    st.subheader("GTReplicate Costs")
    gtreplicate_cost = st.number_input("GTReplicate License Cost (USD/vessel/month)", min_value=0, value=30, step=1)
    implementation_cost = st.number_input("One-time Implementation Cost (USD)", min_value=0, value=0, step=1000)
    maintenance_hours = st.number_input("Monthly Maintenance Hours per Vessel", min_value=0, value=5, step=1)

# Calculate core license costs
monthly_license_cost = vessels * gtreplicate_cost
annual_license_cost = monthly_license_cost * 12

# Calculate current process costs (monthly)
current_bandwidth_cost = vessels * data_per_vessel * bandwidth_cost
current_manual_cost = vessels * monthly_hours * it_cost
current_failure_cost = vessels * failure_rate * failure_time * it_cost
current_total = current_bandwidth_cost + current_manual_cost + current_failure_cost

# Calculate GTReplicate costs (monthly)
gt_bandwidth_cost = current_bandwidth_cost * 0.4  # 60% reduction
gt_manual_cost = vessels * maintenance_hours * it_cost
gt_failure_cost = current_failure_cost * 0.1  # 90% reduction
gt_monthly_total = gt_bandwidth_cost + gt_manual_cost + gt_failure_cost + monthly_license_cost

with col2:
    # Core License Costs
    st.subheader("License Costs")
    license_col1, license_col2 = st.columns(2)
    
    with license_col1:
        st.metric(
            "Monthly License Cost",
            f"${monthly_license_cost:,.2f}",
            f"${gtreplicate_cost:.2f} per vessel"
        )
    
    with license_col2:
        st.metric(
            "Annual License Cost",
            f"${annual_license_cost:,.2f}",
            f"${annual_license_cost/vessels:.2f} per vessel"
        )

    st.markdown("---")

    # Cost Comparison Bar Chart
    categories = ['Bandwidth Cost', 'Manual Operations', 'Failure Resolution']
    current_values = [current_bandwidth_cost, current_manual_cost, current_failure_cost]
    gt_values = [gt_bandwidth_cost, gt_manual_cost + monthly_license_cost, gt_failure_cost]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Current Process',
        x=categories,
        y=current_values,
        marker_color='#FF6B6B'
    ))
    fig_bar.add_trace(go.Bar(
        name='GTReplicate',
        x=categories,
        y=gt_values,
        marker_color='#4ECDC4'
    ))

    fig_bar.update_layout(
        title='Monthly Cost Comparison (USD)',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # Savings Breakdown
    savings_data = pd.DataFrame({
        'Category': ['Bandwidth Savings', 'Operation Savings', 'Failure Resolution Savings'],
        'Value': [
            current_bandwidth_cost - gt_bandwidth_cost,
            current_manual_cost - (gt_manual_cost + monthly_license_cost),
            current_failure_cost - gt_failure_cost
        ]
    })

    fig_pie = px.pie(
        savings_data,
        values='Value',
        names='Category',
        title='Monthly Savings Breakdown'
    )
    fig_pie.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Financial Summary
st.subheader("Financial Summary")
col1, col2, col3 = st.columns(3)

monthly_savings = current_total - gt_monthly_total
annual_savings = monthly_savings * 12
roi_months = implementation_cost / monthly_savings if monthly_savings > 0 else float('inf')

with col1:
    st.metric(
        "Current Monthly Cost",
        f"${current_total:,.2f}",
        f"${current_total/vessels:,.2f} per vessel"
    )

with col2:
    st.metric(
        "GTReplicate Monthly Cost",
        f"${gt_monthly_total:,.2f}",
        f"${gt_monthly_total/vessels:,.2f} per vessel"
    )

with col3:
    st.metric(
        "Monthly Savings",
        f"${monthly_savings:,.2f}",
        f"${monthly_savings/vessels:,.2f} per vessel"
    )

# Efficiency Metrics
st.subheader("Operational Improvements")
eff_col1, eff_col2, eff_col3 = st.columns(3)

with eff_col1:
    failure_reduction = ((current_failure_cost - gt_failure_cost) / current_failure_cost * 100)
    st.metric(
        "Transfer Failure Reduction",
        f"{failure_reduction:.1f}%",
        f"From {failure_rate} to {failure_rate * 0.1:.1f} failures/month"
    )

with eff_col2:
    bandwidth_reduction = ((current_bandwidth_cost - gt_bandwidth_cost) / current_bandwidth_cost * 100)
    st.metric(
        "Bandwidth Cost Reduction",
        f"{bandwidth_reduction:.1f}%",
        f"${current_bandwidth_cost/vessels:.2f} to ${gt_bandwidth_cost/vessels:.2f} per vessel"
    )

with eff_col3:
    time_reduction = ((current_manual_cost - gt_manual_cost) / current_manual_cost * 100)
    st.metric(
        "Manual Time Reduction",
        f"{time_reduction:.1f}%",
        f"{monthly_hours} to {maintenance_hours} hours/month"
    )