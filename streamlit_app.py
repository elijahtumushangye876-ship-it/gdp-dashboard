import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page & Branding Setup
st.set_page_config(page_title="Kigyende United Traders", layout="wide")
st.title("📊 Kigyende United Traders - Management Portal")
st.write("Internal business tracking, sales summaries, and operational analytics dashboard.")

# 2. Creating Your Business Dataset
@st.cache_data
def load_traders_data():
    # You can later replace this section by uploading an actual Excel/CSV file!
    # For now, we seed realistic operational data for a Ugandan trading enterprise
    data_records = [
        {"Month": "Jan", "Category": "Produce Sales", "Amount_UGX": 4500000, "Type": "Revenue"},
        {"Month": "Jan", "Category": "Transport & Logistics", "Amount_UGX": 1200000, "Type": "Expense"},
        {"Month": "Feb", "Category": "Produce Sales", "Amount_UGX": 5200000, "Type": "Revenue"},
        {"Month": "Feb", "Category": "Store Rent & Utilities", "Amount_UGX": 800000, "Type": "Expense"},
        {"Month": "Mar", "Category": "Wholesale Distribution", "Amount_UGX": 6100000, "Type": "Revenue"},
        {"Month": "Mar", "Category": "Supplier Payouts", "Amount_UGX": 3000000, "Type": "Expense"},
        {"Month": "Apr", "Category": "Produce Sales", "Amount_UGX": 4800000, "Type": "Revenue"},
        {"Month": "Apr", "Category": "Transport & Logistics", "Amount_UGX": 1100000, "Type": "Expense"},
        {"Month": "May", "Category": "Wholesale Distribution", "Amount_UGX": 7300000, "Type": "Revenue"},
        {"Month": "May", "Category": "Stock Replenishment", "Amount_UGX": 3500000, "Type": "Expense"},
    ]
    return pd.DataFrame(data_records)

df = load_traders_data()

# 3. Sidebar Business Navigation
st.sidebar.header("📁 Navigation & Filters")
view_option = st.sidebar.radio("Select View", ["Overview Dashboard", "Detailed Financial Ledger"])
selected_type = st.sidebar.multiselect("Filter Transaction Type", ["Revenue", "Expense"], default=["Revenue", "Expense"])

# Filter dataframe based on user choice
filtered_df = df[df['Type'].isin(selected_type)]

# 4. Content Presentation
if view_option == "Overview Dashboard":
    # Calculate key metrics
    total_rev = df[df['Type'] == "Revenue"]['Amount_UGX'].sum()
    total_exp = df[df['Type'] == "Expense"]['Amount_UGX'].sum()
    net_profit = total_rev - total_exp
    
    # Display performance indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Gross Revenue", value=f"{total_rev:,} UGX")
    with col2:
        st.metric(label="Total Operating Expenses", value=f"{total_exp:,} UGX")
    with col3:
        st.metric(label="Net Estimated Margin", value=f"{net_profit:,} UGX")
        
    st.write("---")
    
    # Performance Visualization
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df, 
            x="Month", 
            y="Amount_UGX", 
            color="Category",
            barmode="group",
            title="Monthly Cash Flow breakdown (UGX)",
            labels={"Amount_UGX": "Value (UGX)", "Month": "Month"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one transaction type in the sidebar.")

elif view_option == "Detailed Financial Ledger":
    st.subheader("Transaction Log Database")
    st.write("Below is the recorded log entries for Kigyende United Traders.")
    st.dataframe(filtered_df, use_container_width=True)
