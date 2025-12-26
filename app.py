import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Humanitarian Projects Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-top: 4px solid #2563eb;
    }
    
    .urgent-task {
        background: #fef2f2;
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 4px solid #ef4444;
        margin-bottom: 0.5rem;
    }
    
    .warning-badge {
        background: #fef3c7;
        color: #92400e;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .critical-badge {
        background: #fee2e2;
        color: #991b1b;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .ontrack-badge {
        background: #d1fae5;
        color: #065f46;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def load_data():
    # Countries
    countries = ['Ethiopia', 'Yemen', 'Syria', 'Afghanistan', 'South Sudan', 
                 'Somalia', 'Myanmar', 'Venezuela', 'Haiti', 'All']
    
    # Implementing Partners
    partners = [
        'Global Relief Foundation',
        'International Aid Alliance',
        'Community Development Trust',
        'Emergency Response Network',
        'Sustainable Futures Initiative'
    ]
    
    # Partner payment data
    partner_payments = pd.DataFrame({
        'Partner': partners,
        'Completed': [450000, 320000, 280000, 195000, 175000],
        'Pending': [85000, 65000, 48000, 35000, 28000]
    })
    
    # Project completion by quarter
    quarters_data = []
    for year in [2022, 2023, 2024, 2025]:
        for q in range(1, 5):
            if year == 2025 and q > 1:
                break
            quarterly = np.random.randint(3, 12)
            quarters_data.append({
                'Year': year,
                'Quarter': f'Q{q}',
                'Quarterly_Completed': quarterly,
                'Year_Quarter': f'{year}-Q{q}'
            })
    
    completion_by_quarter = pd.DataFrame(quarters_data)
    completion_by_quarter['Cumulative_Completed'] = completion_by_quarter['Quarterly_Completed'].cumsum()
    
    # Contractual costs by partner and year
    cost_data = []
    years = [2022, 2023, 2024, 2025]
    for partner in partners[:3]:
        for year in years:
            base_cost = np.random.randint(15000, 25000)
            if year == 2024:
                base_cost *= 1.8
            elif year == 2023:
                base_cost *= 1.2
            elif year == 2025:
                base_cost *= 0.7
            
            cost_data.append({
                'Partner': partner,
                'Year': year,
                'Cost': base_cost
            })
    
    contractual_costs = pd.DataFrame(cost_data)
    
    # Urgent tasks
    urgent_tasks = pd.DataFrame({
        'Task': [
            'Project Approval by Regional Lead',
            'Budget Revision Review',
            'Field Assessment Report Submission',
            'Beneficiary Data Validation',
            'Final Project Report'
        ],
        'Overdue_Days': [12, 8, 5, 3, 1],
        'Priority': ['Critical', 'Critical', 'Warning', 'Warning', 'On Track']
    })
    
    return (countries, partner_payments, completion_by_quarter, 
            contractual_costs, urgent_tasks)

# Load data
(countries, partner_payments, completion_by_quarter, 
 contractual_costs, urgent_tasks) = load_data()

# Calculate metrics
total_contract_value = partner_payments['Completed'].sum() + partner_payments['Pending'].sum()
completion_rate = 80.00
completed_payments = partner_payments['Completed'].sum()
pending_payments = partner_payments['Pending'].sum()

# Header
st.markdown(f"""
<div class="main-header">
    <h1>🌍 Humanitarian Projects Dashboard</h1>
    <p>Status as of {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎯 Dashboard Filters")

selected_country = st.sidebar.selectbox(
    "Country / Region",
    options=countries,
    index=len(countries)-1
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 📋 Project Phase")
phase_inception = st.sidebar.checkbox("01 Inception", value=False)
phase_planning = st.sidebar.checkbox("02 Planning", value=False)
phase_implementation = st.sidebar.checkbox("03 Implementation", value=False)
phase_completed = st.sidebar.checkbox("04 Completed", value=False)
phase_closed = st.sidebar.checkbox("05 Closed", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Actions")
if st.sidebar.button("📥 Export Report", use_container_width=True):
    st.sidebar.success("✅ Report exported!")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.sidebar.success("✅ Data refreshed!")

# Main dashboard layout
col1, col2, col3, col4 = st.columns([1.2, 1, 1.2, 1.2])

with col1:
    st.markdown("### Completion Rate")
    fig_completion = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completion_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#1e40af"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#fee2e2'},
                {'range': [50, 75], 'color': '#fef3c7'},
                {'range': [75, 100], 'color': '#d1fae5'}
            ],
        }
    ))
    fig_completion.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white"
    )
    st.plotly_chart(fig_completion, use_container_width=True)

with col2:
    st.markdown("### Total Budget")
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color: #2563eb; margin: 0; font-size: 2.5rem;">${total_contract_value/1000:.0f}K</h2>
        <p style="color: #64748b; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Total Contract Value</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("📌", help="Pin", use_container_width=True)
    with col_b:
        st.button("📋", help="Copy", use_container_width=True)

with col3:
    st.markdown("### Completed vs. Pending")
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Completed', 'Pending'],
        values=[completed_payments, pending_payments],
        marker=dict(colors=['#1e40af', '#dc2626']),
        textinfo='label+percent',
        textposition='inside',
        hole=0.4
    )])
    fig_pie.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text=f'${(completed_payments + pending_payments)/1000:.0f}K', 
                         x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.markdown("### Tasks Requiring Urgent Attention")
    
    # Display urgent tasks
    for idx, row in urgent_tasks.head(3).iterrows():
        priority_class = row['Priority'].lower().replace(' ', '')
        badge_html = f'<span class="{priority_class}-badge">{row["Priority"]}</span>'
        
        st.markdown(f"""
        <div class="urgent-task">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 0.85rem;">{row['Task']}</strong>
                {badge_html}
            </div>
            <div style="color: #ef4444; font-size: 0.75rem; margin-top: 0.3rem;">
                {row['Overdue_Days']} days overdue
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #f1f5f9; padding: 0.5rem; border-radius: 6px; text-align: center; margin-top: 0.5rem;">
        <strong>Total: {len(urgent_tasks)} tasks</strong>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Bottom section with charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 Implementing Partner Payment Status")
    
    fig_partners = go.Figure()
    
    fig_partners.add_trace(go.Bar(
        name='Completed Payment',
        y=partner_payments['Partner'],
        x=partner_payments['Completed'],
        orientation='h',
        marker=dict(color='#1e40af'),
        text=partner_payments['Completed'].apply(lambda x: f'${x/1000:.0f}K'),
        textposition='inside',
        textfont=dict(color='white', size=11)
    ))
    
    fig_partners.add_trace(go.Bar(
        name='Pending Payments',
        y=partner_payments['Partner'],
        x=partner_payments['Pending'],
        orientation='h',
        marker=dict(color='#dc2626'),
        text=partner_payments['Pending'].apply(lambda x: f'${x/1000:.0f}K'),
        textposition='inside',
        textfont=dict(color='white', size=11)
    ))
    
    fig_partners.update_layout(
        barmode='stack',
        height=350,
        xaxis_title='Completed Payment and Pending Payments',
        yaxis_title='Partner',
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=40, b=80)
    )
    
    st.plotly_chart(fig_partners, use_container_width=True)

with col2:
    st.markdown("### 📊 Project Completion by Year & Quarter")
    
    fig_completion_trend = go.Figure()
    
    fig_completion_trend.add_trace(go.Bar(
        name='Quarterly Completed',
        x=completion_by_quarter['Year_Quarter'],
        y=completion_by_quarter['Quarterly_Completed'],
        marker=dict(color='#1e40af'),
        text=completion_by_quarter['Quarterly_Completed'],
        textposition='outside'
    ))
    
    fig_completion_trend.add_trace(go.Scatter(
        name='Cumulative Completed',
        x=completion_by_quarter['Year_Quarter'],
        y=completion_by_quarter['Cumulative_Completed'],
        mode='lines+markers',
        marker=dict(color='#dc2626', size=8),
        line=dict(color='#dc2626', width=3)
    ))
    
    fig_completion_trend.update_layout(
        height=350,
        xaxis_title='Year',
        yaxis_title='Number Completed',
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=40, b=80)
    )
    
    st.plotly_chart(fig_completion_trend, use_container_width=True)

st.markdown("---")

# Bottom chart
st.markdown("### 💵 Budget Allocation by Partner and Year (USD)")

fig_costs = go.Figure()

for partner in contractual_costs['Partner'].unique():
    partner_data = contractual_costs[contractual_costs['Partner'] == partner]
    fig_costs.add_trace(go.Scatter(
        name=partner,
        x=partner_data['Year'],
        y=partner_data['Cost'],
        mode='lines+markers',
        line=dict(width=3),
        marker=dict(size=10)
    ))

# Add reference lines
fig_costs.add_hline(y=20000, line_dash="dot", line_color="gray", opacity=0.5)
fig_costs.add_hline(y=40000, line_dash="dot", line_color="gray", opacity=0.5)

fig_costs.update_layout(
    height=400,
    xaxis_title='Year',
    yaxis_title='Sum of Budget Allocation (USD)',
    legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=0.98),
    margin=dict(l=20, r=20, t=40, b=60),
    hovermode='x unified'
)

st.plotly_chart(fig_costs, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    <p><strong>Humanitarian Projects Monitoring System</strong></p>
    <p style="font-size: 0.85rem;">Data updated in real-time | For internal use only</p>
</div>
""", unsafe_allow_html=True)
