import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Telecom Customer Service Dashboard", layout="wide")

# Title
st.title("📱 Telecom Customer Service Analytics Dashboard")
st.markdown("*Comprehensive analysis of customer behavior, revenue trends, and support impact*")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('telecom_data.csv')

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Dashboard")

# Region filter
regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['region'].unique(),
    default=df['region'].unique()
)

# Segment filter
segments = st.sidebar.multiselect(
    "Select Customer Segment(s)",
    options=df['segment'].unique(),
    default=df['segment'].unique()
)

# Churn risk filter
churn_filter = st.sidebar.selectbox(
    "Churn Risk Level",
    options=['All', 'Low', 'Medium', 'High']
)

# Apply filters
filtered_df = df[df['region'].isin(regions) & df['segment'].isin(segments)]

if churn_filter != 'All':
    filtered_df = filtered_df[filtered_df['churn_risk_category'] == churn_filter]

# --- KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Customers",
        f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):+}" if len(filtered_df) != len(df) else None
    )

with col2:
    total_revenue = filtered_df['monthly_revenue'].sum()
    st.metric(
        "💰 Monthly Revenue",
        f"R{total_revenue:,.2f}",
        delta=f"{total_revenue/1000:.1f}K"
    )

with col3:
    avg_churn = filtered_df['churn_risk_score'].mean()
    st.metric(
        "⚠️ Avg Churn Risk",
        f"{avg_churn:.1f}%",
        delta="High Risk" if avg_churn > 50 else "Low Risk",
        delta_color="inverse" if avg_churn > 50 else "normal"
    )

with col4:
    avg_satisfaction = filtered_df['satisfaction_score'].mean()
    st.metric(
        "⭐ Customer Satisfaction",
        f"{avg_satisfaction:.2f}/5.0",
        delta="Good" if avg_satisfaction > 3.5 else "Needs Improvement"
    )

st.divider()

# --- CHARTS ---
col1, col2 = st.columns(2)

with col1:
    # Revenue by Segment
    revenue_by_segment = filtered_df.groupby('segment')['monthly_revenue'].sum().reset_index()
    fig_segment_revenue = px.pie(
        revenue_by_segment,
        values='monthly_revenue',
        names='segment',
        title='💰 Revenue by Customer Segment (Rands)',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_segment_revenue.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_segment_revenue, use_container_width=True)

with col2:
    # Customer Distribution by Segment
    segment_counts = filtered_df['segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    fig_segment_dist = px.bar(
        segment_counts,
        x='Segment',
        y='Count',
        title='📊 Customer Distribution by Segment',
        color='Segment',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig_segment_dist, use_container_width=True)

# --- ROW 2 ---
col1, col2 = st.columns(2)

with col1:
    # Payment Method Preferences
    payment_counts = filtered_df['payment_method'].value_counts().reset_index()
    payment_counts.columns = ['Payment Method', 'Count']
    fig_payment = px.bar(
        payment_counts,
        x='Payment Method',
        y='Count',
        title='💳 Payment Method Preferences',
        color='Payment Method',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    st.plotly_chart(fig_payment, use_container_width=True)

with col2:
    # Churn Risk Distribution
    churn_dist = filtered_df['churn_risk_category'].value_counts().reset_index()
    churn_dist.columns = ['Risk Level', 'Count']
    colors = {'Low': '#2ecc71', 'Medium': '#f39c12', 'High': '#e74c3c'}
    fig_churn = px.bar(
        churn_dist,
        x='Risk Level',
        y='Count',
        title='⚠️ Churn Risk Distribution',
        color='Risk Level',
        color_discrete_map=colors
    )
    st.plotly_chart(fig_churn, use_container_width=True)

# --- ROW 3 ---
col1, col2 = st.columns(2)

with col1:
    # Support Tickets by Segment
    tickets_by_segment = filtered_df.groupby('segment')['support_tickets'].mean().reset_index()
    fig_tickets = px.bar(
        tickets_by_segment,
        x='segment',
        y='support_tickets',
        title='🎫 Average Support Tickets by Segment',
        color='segment',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_tickets.update_layout(yaxis_title="Avg Tickets")
    st.plotly_chart(fig_tickets, use_container_width=True)

with col2:
    # Satisfaction Score by Segment
    satisfaction_by_segment = filtered_df.groupby('segment')['satisfaction_score'].mean().reset_index()
    fig_satisfaction = px.bar(
        satisfaction_by_segment,
        x='segment',
        y='satisfaction_score',
        title='⭐ Average Satisfaction Score by Segment',
        color='segment',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_satisfaction.update_layout(yaxis_title="Avg Satisfaction (1-5)")
    st.plotly_chart(fig_satisfaction, use_container_width=True)

# --- ROW 4: Correlation Analysis ---
st.subheader("📈 Key Metrics Correlation")

correlation_cols = ['tenure_months', 'monthly_charges', 'support_tickets', 'satisfaction_score', 'churn_risk_score']
correlation_df = filtered_df[correlation_cols].corr()

fig_corr = px.imshow(
    correlation_df,
    text_auto=True,
    aspect="auto",
    color_continuous_scale='RdBu_r',
    title="Metric Correlations"
)
st.plotly_chart(fig_corr, use_container_width=True)

# --- RAW DATA ---
with st.expander("📊 View Raw Customer Data"):
    st.dataframe(filtered_df.head(100))

# --- SUMMARY STATISTICS ---
with st.expander("📈 Summary Statistics"):
    st.write("### Customer Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Top 5 Regions by Revenue (Rands)**")
        top_regions = filtered_df.groupby('region')['monthly_revenue'].sum().sort_values(ascending=False).head(5)
        st.dataframe(top_regions)
    
    with col2:
        st.write("**Contract Type Distribution**")
        contract_dist = filtered_df['contract_type'].value_counts()
        st.dataframe(contract_dist)
    
    with col3:
        st.write("**Support Tier Distribution**")
        support_dist = filtered_df['support_tier'].value_counts()
        st.dataframe(support_dist)