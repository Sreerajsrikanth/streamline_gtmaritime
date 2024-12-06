import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(
    page_title="GTReplicate ROI Calculator",
    page_icon="🚢",
    layout="wide"
)

# Title
st.title("🚢 GTReplicate ROI Calculator")

# Create two columns for input and visualization
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Fleet Information")
    
    # Input fields with default values and proper typing
    vessels = st.number_input("Number of Vessels", min_value=1, value=10, step=1)
    data_per_vessel = st.number_input("Data Transfer per Vessel (GB/month)", min_value=1, value=50, step=1)
    bandwidth_cost = st.number_input("Bandwidth Cost (USD/GB)", min_value=1, value=30, step=1)
    
    st.subheader("Current Process")
    monthly_hours = st.number_input("Monthly Hours per Vessel", min_value=1, value=20, step=1)
    it_cost = st.number_input("IT Cost per Hour (USD)", min_value=1, value=50, step=1)
    failure_rate = st.number_input("Monthly Transfer Failures", min_value=0, value=5, step=1)
    failure_time = st.number_input("Hours per Failure Resolution", min_value=0, value=2, step=1)

# Calculate metrics
current_bandwidth_cost = vessels * data_per_vessel * bandwidth_cost
current_manual_cost = vessels * monthly_hours * it_cost
current_failure_cost = vessels * failure_rate * failure_time * it_cost
current_total = current_bandwidth_cost + current_manual_cost + current_failure_cost

# GTReplicate scenario (with efficiency improvements)
gt_bandwidth_cost = current_bandwidth_cost * 0.4  # 60% reduction
gt_manual_cost = current_manual_cost * 0.25  # 75% reduction
gt_failure_cost = current_failure_cost * 0.1  # 90% reduction
gt_total = gt_bandwidth_cost + gt_manual_cost + gt_failure_cost

with col2:
    # Create comparison data
    categories = ['Bandwidth Cost', 'Manual Operations', 'Failure Resolution']
    current_values = [current_bandwidth_cost, current_manual_cost, current_failure_cost]
    gt_values = [gt_bandwidth_cost, gt_manual_cost, gt_failure_cost]

    # Bar chart
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Current',
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
        title='Cost Comparison (USD/Month)',
        barmode='group',
        height=400,
        width=None  # Let Streamlit handle the width
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie chart data
    savings_data = pd.DataFrame({
        'Category': ['Bandwidth Savings', 'Operation Savings', 'Failure Resolution Savings'],
        'Value': [
            current_bandwidth_cost - gt_bandwidth_cost,
            current_manual_cost - gt_manual_cost,
            current_failure_cost - gt_failure_cost
        ]
    })

    # Only create pie chart if there are savings
    if savings_data['Value'].sum() > 0:
        fig_pie = px.pie(
            savings_data,
            values='Value',
            names='Category',
            title='Savings Breakdown'
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

# Summary metrics
st.subheader("Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Monthly Cost",
        f"${current_total:,.2f}"
    )

with col2:
    st.metric(
        "GTReplicate Monthly Cost",
        f"${gt_total:,.2f}"
    )

with col3:
    savings = current_total - gt_total
    st.metric(
        "Monthly Savings",
        f"${savings:,.2f}",
        delta=f"{(savings/current_total)*100:.1f}%"
    )

# Add debug information
st.subheader("Debug Information")
st.write("Input Values:", {
    'vessels': vessels,
    'data_per_vessel': data_per_vessel,
    'bandwidth_cost': bandwidth_cost,
    'monthly_hours': monthly_hours,
    'it_cost': it_cost,
    'failure_rate': failure_rate,
    'failure_time': failure_time
})

st.write("Calculated Costs:", {
    'current_bandwidth_cost': current_bandwidth_cost,
    'current_manual_cost': current_manual_cost,
    'current_failure_cost': current_failure_cost,
    'gt_bandwidth_cost': gt_bandwidth_cost,
    'gt_manual_cost': gt_manual_cost,
    'gt_failure_cost': gt_failure_cost
})