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

# [Functions predict_cash_flow, predict_runway, analyze_vendor_spending, calculate_financial_ratios remain unchanged]

def main():
    # ... your existing Streamlit layout remains unchanged ...
    # Only fixed part is in tab4 for Expense Analytics:
    
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
            subcategory_expenses = (
                filtered_df[filtered_df['Amount'] < 0]
                .groupby('Subcategory')['Amount']
                .sum()
                .abs()
                .sort_values(ascending=False)
                .head(10)
            )
            fig = px.pie(
                values=subcategory_expenses.values,
                names=subcategory_expenses.index,
                title='Top 10 Subcategories',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# Entry point
if __name__ == "__main__":
    main()
