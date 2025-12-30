import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Company Financial Analytics", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>.main{padding:0rem 1rem;}.stMetric{background-color:#f0f2f6;padding:15px;border-radius:10px;}</style>""", unsafe_allow_html=True)

@st.cache_data
def generate_company_data():
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=365)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    transactions = []
    
    categories = {
        'Revenue': {'Customer Payments': ['Acme Corp', 'TechStart Inc', 'Global Solutions', 'Enterprise Co', 'Innovation Labs'],
                    'Service Revenue': ['Consulting Fee', 'SaaS Subscription', 'License Revenue', 'Maintenance Fee'],
                    'Product Sales': ['Product Sale - Client A', 'Product Sale - Client B', 'Bulk Order Payment']},
        'Payroll': {'Salaries': ['Payroll - Engineering', 'Payroll - Sales', 'Payroll - Operations', 'Payroll - Management'],
                    'Benefits': ['Health Insurance', '401k Contribution', 'Employee Benefits']},
        'Operating Expenses': {'Office': ['Office Rent', 'Utilities - Electric', 'Utilities - Internet', 'Office Supplies', 'Cleaning Services'],
                               'Software': ['AWS Cloud Services', 'Microsoft 365', 'Salesforce', 'Slack Enterprise', 'GitHub Enterprise', 'Adobe Creative Cloud'],
                               'Marketing': ['Google Ads', 'LinkedIn Ads', 'Conference Sponsorship', 'Marketing Agency', 'Content Marketing'],
                               'Professional Services': ['Legal Fees', 'Accounting Services', 'Consulting Services', 'Audit Fees']},
        'Equipment': {'Equipment': ['MacBook Pro', 'Dell Workstation', 'Office Furniture', 'Server Hardware', 'Network Equipment']},
        'Travel': {'Travel': ['Flight Booking', 'Hotel Accommodation', 'Uber Business', 'Restaurant - Client Dinner', 'Conference Registration']},
        'Insurance': {'Insurance': ['Business Insurance', 'Liability Insurance', 'Property Insurance']},
        'Taxes': {'Taxes': ['Federal Tax Payment', 'State Tax Payment', 'Payroll Tax']},
        'Loan Payments': {'Loan Payments': ['Business Loan Payment', 'Equipment Financing']},
        'Investments': {'Investments': ['Investment in Marketing', 'R&D Investment', 'Equipment Purchase']},
        'Miscellaneous': {'Miscellaneous': ['Bank Fees', 'Transaction Fees', 'Late Payment Fee']}
    }
    
    for week in range(52):
        week_date = start_date + timedelta(weeks=week)
        num_revenue = np.random.randint(2, 6)
        for _ in range(num_revenue):
            revenue_date = week_date + timedelta(days=np.random.randint(0, 7))
            if np.random.random() > 0.3:
                subcategory = 'Customer Payments'
                amount = np.random.uniform(5000, 50000)
            else:
                subcategory = np.random.choice(['Service Revenue', 'Product Sales'])
                amount = np.random.uniform(2000, 20000)
            vendor = np.random.choice(categories['Revenue'][subcategory])
            transactions.append({'Date': revenue_date.strftime('%Y-%m-%d'), 'Description': vendor, 'Amount': round(amount, 2),
                               'Category': 'Revenue', 'Subcategory': subcategory, 'Type': 'Credit'})
    
    for month in range(12):
        month_date = start_date + timedelta(days=month*30)
        for day in [1, 15]:
            payroll_date = month_date.replace(day=day)
            for dept in ['Engineering', 'Sales', 'Operations', 'Management']:
                amount = {'Engineering': -np.random.uniform(45000, 55000), 'Sales': -np.random.uniform(30000, 40000),
                         'Operations': -np.random.uniform(25000, 35000), 'Management': -np.random.uniform(35000, 45000)}[dept]
                transactions.append({'Date': payroll_date.strftime('%Y-%m-%d'), 'Description': f'Payroll - {dept}', 'Amount': round(amount, 2),
                                   'Category': 'Payroll', 'Subcategory': 'Salaries', 'Type': 'Debit'})
        
        benefits_date = month_date.replace(day=5)
        for benefit in ['Health Insurance', '401k Contribution']:
            amount = -np.random.uniform(8000, 12000)
            transactions.append({'Date': benefits_date.strftime('%Y-%m-%d'), 'Description': benefit, 'Amount': round(amount, 2),
                               'Category': 'Payroll', 'Subcategory': 'Benefits', 'Type': 'Debit'})
        
        office_date = month_date.replace(day=1)
        transactions.append({'Date': office_date.strftime('%Y-%m-%d'), 'Description': 'Office Rent', 'Amount': -8500.00,
                           'Category': 'Operating Expenses', 'Subcategory': 'Office', 'Type': 'Debit'})
        
        for utility in ['Utilities - Electric', 'Utilities - Internet']:
            amount = -np.random.uniform(500, 1500)
            transactions.append({'Date': office_date.strftime('%Y-%m-%d'), 'Description': utility, 'Amount': round(amount, 2),
                               'Category': 'Operating Expenses', 'Subcategory': 'Office', 'Type': 'Debit'})
        
        software_date = month_date.replace(day=10)
        for software in ['AWS Cloud Services', 'Microsoft 365', 'Salesforce', 'Slack Enterprise']:
            amount = {'AWS Cloud Services': -np.random.uniform(3000, 5000), 'Microsoft 365': -np.random.uniform(800, 1200),
                     'Salesforce': -np.random.uniform(2000, 3000), 'Slack Enterprise': -np.random.uniform(400, 600)}[software]
            transactions.append({'Date': software_date.strftime('%Y-%m-%d'), 'Description': software, 'Amount': round(amount, 2),
                               'Category': 'Operating Expenses', 'Subcategory': 'Software', 'Type': 'Debit'})
        
        insurance_date = month_date.replace(day=20)
        transactions.append({'Date': insurance_date.strftime('%Y-%m-%d'), 'Description': 'Business Insurance',
                           'Amount': round(-np.random.uniform(2000, 3000), 2), 'Category': 'Insurance', 'Subcategory': 'Insurance', 'Type': 'Debit'})
        
        loan_date = month_date.replace(day=25)
        transactions.append({'Date': loan_date.strftime('%Y-%m-%d'), 'Description': 'Business Loan Payment', 'Amount': -5000.00,
                           'Category': 'Loan Payments', 'Subcategory': 'Loan Payments', 'Type': 'Debit'})
    
    for date in dates:
        if np.random.random() > 0.6:
            marketing_vendor = np.random.choice(['Google Ads', 'LinkedIn Ads', 'Marketing Agency', 'Content Marketing'])
            amount = -np.random.uniform(1000, 5000)
            transactions.append({'Date': date.strftime('%Y-%m-%d'), 'Description': marketing_vendor, 'Amount': round(amount, 2),
                               'Category': 'Operating Expenses', 'Subcategory': 'Marketing', 'Type': 'Debit'})
        
        if np.random.random() > 0.85:
            travel_type = np.random.choice(['Flight Booking', 'Hotel Accommodation', 'Uber Business', 'Restaurant - Client Dinner'])
            amount = -np.random.uniform(200, 2000)
            transactions.append({'Date': date.strftime('%Y-%m-%d'), 'Description': travel_type, 'Amount': round(amount, 2),
                               'Category': 'Travel', 'Subcategory': 'Travel', 'Type': 'Debit'})
        
        if np.random.random() > 0.95:
            service = np.random.choice(['Legal Fees', 'Accounting Services', 'Consulting Services'])
            amount = -np.random.uniform(1000, 10000)
            transactions.append({'Date': date.strftime('%Y-%m-%d'), 'Description': service, 'Amount': round(amount, 2),
                               'Category': 'Operating Expenses', 'Subcategory': 'Professional Services', 'Type': 'Debit'})
        
        if np.random.random() > 0.98:
            equipment = np.random.choice(['MacBook Pro', 'Dell Workstation', 'Office Furniture', 'Network Equipment'])
            amount = -np.random.uniform(1500, 8000)
            transactions.append({'Date': date.strftime('%Y-%m-%d'), 'Description': equipment, 'Amount': round(amount, 2),
                               'Category': 'Equipment', 'Subcategory': 'Equipment', 'Type': 'Debit'})
    
    for quarter in range(4):
        tax_date = start_date + timedelta(days=quarter*90 + 45)
        for tax_type in ['Federal Tax Payment', 'State Tax Payment']:
            amount = -np.random.uniform(15000, 25000)
            transactions.append({'Date': tax_date.strftime('%Y-%m-%d'), 'Description': tax_type, 'Amount': round(amount, 2),
                               'Category': 'Taxes', 'Subcategory': 'Taxes', 'Type': 'Debit'})
    
    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    df['Balance'] = 250000 + df['Amount'].cumsum()
    return df

def predict_cash_flow(df, days=90):
    daily_flow = df.groupby(df['Date'].dt.date)['Amount'].sum()
    X = np.arange(len(daily_flow)).reshape(-1, 1)
    y = daily_flow.values
    model = LinearRegression()
    model.fit(X, y)
    future_X = np.arange(len(daily_flow), len(daily_flow) + days).reshape(-1, 1)
    predictions = model.predict(future_X)
    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
    return pd.DataFrame({'Date': future_dates, 'Predicted_Cash_Flow': predictions})

def predict_runway(df):
    current_balance = df['Balance'].iloc[-1]
    monthly_expenses = df[df['Amount'] < 0].groupby(df[df['Amount'] < 0]['Date'].dt.to_period('M'))['Amount'].sum().abs()
    avg_monthly_burn = monthly_expenses.mean()
    monthly_revenue = df[df['Amount'] > 0].groupby(df[df['Amount'] > 0]['Date'].dt.to_period('M'))['Amount'].sum()
    avg_monthly_revenue = monthly_revenue.mean()
    net_monthly = avg_monthly_revenue - avg_monthly_burn
    runway_months = current_balance / abs(net_monthly) if net_monthly < 0 else float('inf')
    return {'current_balance': current_balance, 'monthly_burn': avg_monthly_burn, 'monthly_revenue': avg_monthly_revenue,
            'net_monthly': net_monthly, 'runway_months': runway_months}

def analyze_vendor_spending(df):
    vendor_spending = df[df['Amount'] < 0].groupby('Description').agg({'Amount': ['sum', 'count', 'mean'], 'Category': 'first'}).reset_index()
    vendor_spending.columns = ['Vendor', 'Total', 'Count', 'Average', 'Category']
    vendor_spending['Total'] = vendor_spending['Total'].abs()
    vendor_spending['Average'] = vendor_spending['Average'].abs()
    return vendor_spending.sort_values('Total', ascending=False)

def calculate_financial_ratios(df):
    last_quarter = df[df['Date'] >= df['Date'].max() - timedelta(days=90)]
    revenue = last_quarter[last_quarter['Amount'] > 0]['Amount'].sum()
    expenses = last_quarter[last_quarter['Amount'] < 0]['Amount'].sum()
    operating_expenses = last_quarter[(last_quarter['Amount'] < 0) & (~last_quarter['Category'].isin(['Payroll', 'Taxes']))]['Amount'].sum()
    gross_profit = revenue + expenses
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
    operating_margin = ((revenue + operating_expenses) / revenue * 100) if revenue > 0 else 0
    burn_rate = abs(expenses) / 3
    return {'revenue': revenue, 'expenses': abs(expenses), 'gross_profit': gross_profit, 'gross_margin': gross_margin,
            'operating_margin': operating_margin, 'monthly_burn': burn_rate}

def main():
    st.title("🏢 Company Financial Analytics Dashboard")
    st.markdown("### AI-Powered Business Banking Intelligence")
    
    with st.sidebar:
        st.header("📊 Data Source")
        data_source = st.radio("Choose data source:", ["Use Sample Data", "Upload Company CSV"])
        
        if data_source == "Upload Company CSV":
            uploaded_file = st.file_uploader("Upload company bank statement", type=['csv'])
            st.info("Expected columns: Date, Description, Amount, Category, Subcategory")
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                df['Date'] = pd.to_datetime(df['Date'])
                if 'Balance' not in df.columns:
                    df['Balance'] = 250000 + df['Amount'].cumsum()
            else:
                df = generate_company_data()
        else:
            df = generate_company_data()
        
        st.markdown("---")
        st.header("⚙️ Settings")
        prediction_days = st.slider("Forecast horizon (days)", 30, 180, 90)
        
        st.markdown("---")
        st.header("📅 Date Range")
        date_range = st.date_input("Select period", value=(df['Date'].min(), df['Date'].max()),
                                   min_value=df['Date'].min(), max_value=df['Date'].max())
    
    if len(date_range) == 2:
        mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Executive Dashboard", "💰 Cash Flow Analysis", "📈 Predictions & Forecasts",
                                              "🔍 Expense Analytics", "📋 Detailed Reports"])
    
    with tab1:
        st.header("Executive Dashboard")
        total_revenue = filtered_df[filtered_df['Amount'] > 0]['Amount'].sum()
        total_expenses = filtered_df[filtered_df['Amount'] < 0]['Amount'].sum()
        net_income = total_revenue + total_expenses
        current_balance = filtered_df['Balance'].iloc[-1]
        ratios = calculate_financial_ratios(filtered_df)
        runway = predict_runway(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💵 Total Revenue", f"${total_revenue:,.0f}",
                     delta=f"{(net_income/total_revenue*100):.1f}% profit margin" if total_revenue > 0 else "0%")
        with col2:
            st.metric("💸 Total Expenses", f"${abs(total_expenses):,.0f}")
        with col3:
            st.metric("📊 Net Income", f"${net_income:,.0f}", delta="Profitable" if net_income > 0 else "Loss")
        with col4:
            st.metric("🏦 Current Balance", f"${current_balance:,.0f}")
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📉 Monthly Burn Rate", f"${runway['monthly_burn']:,.0f}")
        with col2:
            st.metric("💹 Gross Margin", f"{ratios['gross_margin']:.1f}%")
        with col3:
            if runway['runway_months'] == float('inf'):
                st.metric("🚀 Cash Runway", "Positive Cash Flow")
            else:
                st.metric("⏱️ Cash Runway", f"{runway['runway_months']:.1f} months")
        with col4:
            st.metric("📈 Operating Margin", f"{ratios['operating_margin']:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Revenue vs Expenses Trend")
            monthly_data = filtered_df.copy()
            monthly_data['Month'] = monthly_data['Date'].dt.to_period('M')
            monthly_revenue = monthly_data[monthly_data['Amount'] > 0].groupby('Month')['Amount'].sum()
            monthly_expenses = monthly_data[monthly_data['Amount'] < 0].groupby('Month')['Amount'].sum().abs()
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Revenue', x=monthly_revenue.index.astype(str), y=monthly_revenue.values, marker_color='green'))
            fig.add_trace(go.Bar(name='Expenses', x=monthly_expenses.index.astype(str), y=monthly_expenses.values, marker_color='red'))
            fig.update_layout(barmode='group', title='Monthly Revenue vs Expenses')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Expense Breakdown")
            expense_by_category = filtered_df[filtered_df['Amount'] < 0].groupby('Category')['Amount'].sum().abs()
            fig = px.pie(values=subcategory_expenses.values, names=subcategory_expenses.index, title='Top 10 Subcategories')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("📋 Detailed Transaction Reports")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            categories = ['All'] + sorted(filtered_df['Category'].unique().tolist())
            selected_category = st.selectbox("Filter by Category", categories)
        with col2:
            subcategories = ['All'] + sorted(filtered_df['Subcategory'].unique().tolist())
            selected_subcategory = st.selectbox("Filter by Subcategory", subcategories)
        with col3:
            transaction_type = st.selectbox("Transaction Type", ['All', 'Debit', 'Credit'])
        with col4:
            min_amount = st.number_input("Minimum Amount ($)", value=0.0)
        
        report_df = filtered_df.copy()
        if selected_category != 'All':
            report_df = report_df[report_df['Category'] == selected_category]
        if selected_subcategory != 'All':
            report_df = report_df[report_df['Subcategory'] == selected_subcategory]
        if transaction_type != 'All':
            if transaction_type == 'Debit':
                report_df = report_df[report_df['Amount'] < 0]
            else:
                report_df = report_df[report_df['Amount'] > 0]
        report_df = report_df[report_df['Amount'].abs() >= min_amount]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Transactions", len(report_df))
        with col2:
            st.metric("Total Amount", f"${report_df['Amount'].sum():,.0f}")
        with col3:
            st.metric("Average", f"${report_df['Amount'].mean():,.0f}")
        with col4:
            st.metric("Largest", f"${report_df['Amount'].abs().max():,.0f}")
        with col5:
            st.metric("Smallest", f"${report_df['Amount'].abs().min():,.0f}")
        
        st.markdown("---")
        st.subheader("Transaction Details")
        display_df = report_df[['Date', 'Description', 'Category', 'Subcategory', 'Amount', 'Balance']].copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
        display_df['Balance'] = display_df['Balance'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display_df, use_container_width=True, height=500)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download as CSV", data=csv,
                             file_name=f"company_transactions_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
        with col2:
            summary = f"""Company Financial Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: {date_range[0]} to {date_range[1]}

SUMMARY
Total Transactions: {len(report_df)}
Total Amount: ${report_df['Amount'].sum():,.2f}
Average Transaction: ${report_df['Amount'].mean():,.2f}

FILTERS APPLIED
Category: {selected_category}
Subcategory: {selected_subcategory}
Type: {transaction_type}
Minimum Amount: ${min_amount:,.2f}"""
            st.download_button(label="📄 Download Summary", data=summary,
                             file_name=f"summary_report_{datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain")

if __name__ == "__main__":
    main()pie(values=expense_by_category.values, names=expense_by_category.index, hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Account Balance Over Time")
        fig = px.line(filtered_df, x='Date', y='Balance', title='Cash Balance Trend')
        fig.update_traces(line_color='#1f77b4', line_width=3)
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("💼 Vendor Spending Analysis")
        vendor_data = analyze_vendor_spending(filtered_df)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Top 15 Vendors by Total Spending**")
            top_vendors = vendor_data.head(15)
            fig = px.bar(top_vendors, x='Vendor', y='Total', color='Category',
                        labels={'Total': 'Total Spent ($)', 'Vendor': 'Vendor'}, title='Top Vendors')
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Vendor Summary**")
            st.metric("Total Vendors", len(vendor_data))
            st.metric("Avg per Vendor", f"${vendor_data['Total'].mean():,.0f}")
            st.metric("Top Vendor Spend", f"${vendor_data['Total'].iloc[0]:,.0f}")
        
        st.subheader("🔄 Recurring Expenses")
        recurring = vendor_data[vendor_data['Count'] >= 3].sort_values('Total', ascending=False).head(20)
        recurring_display = recurring[['Vendor', 'Category', 'Count', 'Average', 'Total']].copy()
        recurring_display['Average'] = recurring_display['Average'].apply(lambda x: f"${x:,.2f}")
        recurring_display['Total'] = recurring_display['Total'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(recurring_display, use_container_width=True, height=400)
        total_recurring = recurring['Total'].sum()
        st.info(f"💡 **Total Recurring Expenses:** ${total_recurring:,.2f} ({len(recurring)} vendors)")
        
        st.subheader("👥 Payroll Analysis")
        payroll_data = filtered_df[filtered_df['Category'] == 'Payroll']
        col1, col2 = st.columns(2)
        with col1:
            dept_payroll = payroll_data[payroll_data['Subcategory'] == 'Salaries'].groupby(
                payroll_data['Description'].str.replace('Payroll - ', ''))['Amount'].sum().abs()
            fig = px.bar(x=dept_payroll.index, y=dept_payroll.values,
                        labels={'x': 'Department', 'y': 'Total Payroll ($)'}, title='Payroll by Department',
                        color=dept_payroll.values, color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            total_payroll = payroll_data['Amount'].sum()
            total_benefits = payroll_data[payroll_data['Subcategory'] == 'Benefits']['Amount'].sum()
            st.metric("Total Payroll Cost", f"${abs(total_payroll):,.0f}")
            st.metric("Employee Benefits", f"${abs(total_benefits):,.0f}")
            st.metric("Benefits as % of Payroll", f"{(abs(total_benefits)/abs(total_payroll)*100):.1f}%")
    
    with tab2:
        st.header("💰 Cash Flow Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            operating_cash = filtered_df[~filtered_df['Category'].isin(['Investments', 'Loan Payments'])]['Amount'].sum()
            st.metric("Operating Cash Flow", f"${operating_cash:,.0f}")
        with col2:
            investing_cash = filtered_df[filtered_df['Category'] == 'Investments']['Amount'].sum()
            st.metric("Investing Cash Flow", f"${investing_cash:,.0f}")
        with col3:
            financing_cash = filtered_df[filtered_df['Category'] == 'Loan Payments']['Amount'].sum()
            st.metric("Financing Cash Flow", f"${financing_cash:,.0f}")
        
        st.markdown("---")
        st.subheader("Daily Cash Flow")
        daily_flow = filtered_df.groupby(filtered_df['Date'].dt.date)['Amount'].sum().reset_index()
        daily_flow.columns = ['Date', 'Cash_Flow']
        fig = go.Figure()
        colors = ['green' if x >= 0 else 'red' for x in daily_flow['Cash_Flow']]
        fig.add_trace(go.Bar(x=daily_flow['Date'], y=daily_flow['Cash_Flow'], marker_color=colors, name='Daily Cash Flow'))
        fig.update_layout(title='Daily Cash Flow', xaxis_title='Date', yaxis_title='Amount ($)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Revenue Sources")
        revenue_sources = filtered_df[filtered_df['Amount'] > 0].groupby('Subcategory')['Amount'].sum().sort_values(ascending=False)
        fig = px.bar(x=revenue_sources.index, y=revenue_sources.values,
                    labels={'x': 'Revenue Source', 'y': 'Amount ($)'}, title='Revenue by Source')
        fig.update_traces(marker_color='green')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Top Revenue Clients")
        top_clients = filtered_df[filtered_df['Category'] == 'Revenue'].groupby('Description')['Amount'].agg(['sum', 'count']).sort_values('sum', ascending=False).head(10)
        top_clients.columns = ['Total Revenue', 'Number of Transactions']
        top_clients['Total Revenue'] = top_clients['Total Revenue'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(top_clients, use_container_width=True)
    
    with tab3:
        st.header("📈 Predictions & Forecasts")
        st.subheader(f"Cash Flow Forecast (Next {prediction_days} Days)")
        cash_flow_pred = predict_cash_flow(filtered_df, prediction_days)
        fig = px.line(cash_flow_pred, x='Date', y='Predicted_Cash_Flow',
                     title=f'Predicted Daily Cash Flow (Next {prediction_days} Days)')
        fig.update_traces(line_color='purple', line_width=2)
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        total_predicted_flow = cash_flow_pred['Predicted_Cash_Flow'].sum()
        avg_daily_flow = cash_flow_pred['Predicted_Cash_Flow'].mean()
        with col1:
            st.metric("Projected Total Cash Flow", f"${total_predicted_flow:,.0f}")
        with col2:
            st.metric("Average Daily Flow", f"${avg_daily_flow:,.0f}")
        with col3:
            projected_balance = current_balance + total_predicted_flow
            st.metric("Projected Balance", f"${projected_balance:,.0f}")
        
        st.markdown("---")
        st.subheader("🚀 Financial Runway Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Current Metrics")
            st.write(f"**Current Balance:** ${runway['current_balance']:,.0f}")
            st.write(f"**Monthly Revenue:** ${runway['monthly_revenue']:,.0f}")
            st.write(f"**Monthly Burn Rate:** ${runway['monthly_burn']:,.0f}")
            st.write(f"**Net Monthly Cash Flow:** ${runway['net_monthly']:,.0f}")
            if runway['runway_months'] == float('inf'):
                st.success("✅ **Status:** Company is cash flow positive!")
            elif runway['runway_months'] > 12:
                st.success(f"✅ **Cash Runway:** {runway['runway_months']:.1f} months (Healthy)")
            elif runway['runway_months'] > 6:
                st.warning(f"⚠️ **Cash Runway:** {runway['runway_months']:.1f} months (Monitor closely)")
            else:
                st.error(f"🚨 **Cash Runway:** {runway['runway_months']:.1f} months (Critical - Action needed)")
        
        with col2:
            st.markdown("### Scenario Analysis")
            scenarios = {'Current Trajectory': runway['net_monthly'],
                        '10% Cost Reduction': runway['net_monthly'] + (runway['monthly_burn'] * 0.10),
                        '20% Revenue Increase': runway['net_monthly'] + (runway['monthly_revenue'] * 0.20),
                        'Combined (10% cost cut + 20% revenue)': runway['net_monthly'] + (runway['monthly_burn'] * 0.10) + (runway['monthly_revenue'] * 0.20)}
            scenario_df = pd.DataFrame(list(scenarios.items()), columns=['Scenario', 'Monthly Net Cash Flow'])
            scenario_df['Runway (Months)'] = scenario_df['Monthly Net Cash Flow'].apply(
                lambda x: current_balance / abs(x) if x < 0 else float('inf'))
            st.dataframe(scenario_df, use_container_width=True)
        
        st.subheader("📊 Category Expense Forecast")
        last_month = filtered_df[filtered_df['Date'] >= filtered_df['Date'].max() - timedelta(days=30)]
        category_spending = last_month[last_month['Amount'] < 0].groupby('Category')['Amount'].sum().abs()
        next_month_pred = category_spending * 1.02
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Last Month', x=category_spending.index, y=category_spending.values, marker_color='lightblue'))
        fig.add_trace(go.Bar(name='Predicted Next Month', x=next_month_pred.index, y=next_month_pred.values, marker_color='darkblue'))
        fig.update_layout(barmode='group', title='Category Spending: Last vs Next Month')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("🔍 Expense Analytics")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Expenses by Category")
            category_expenses = filtered_df[filtered_df['Amount'] < 0].groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
            fig = px.bar(x=category_expenses.index, y=category_expenses.values,
                        labels={'x': 'Category', 'y': 'Amount ($)'}, color=category_expenses.values,
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Expenses by Subcategory")
            subcategory_expenses = filtered_df[filtered_df['Amount'] < 0].groupby('Subcategory')['Amount'].sum().abs().sort_values(ascending=False).head(10)
            fig = px.
