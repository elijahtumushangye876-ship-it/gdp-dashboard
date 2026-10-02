import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE SETUP & TRADITIONAL SAVINGS PLUS BLUE THEME ---
st.set_page_config(page_title="Savings Plus - Kigyende United Traders", layout="wide")

# Custom CSS styling to mimic a core banking desktop layout
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 5px; border-left: 5px solid #003366; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1 { color: #003366; font-family: 'Arial Black', sans-serif; }
    h2 { color: #004080; }
    </style>
""", unsafe_allow_html=True)

# --- LIVE DATABASES (SESSION STATE STORAGE) ---
if 'members_db' not in st.session_state:
    st.session_state.members_db = pd.DataFrame([
        {"Account_No": "KT-001", "Full_Name": "Elijah Tumushangye", "Phone": "0700000000", "Status": "Active"},
        {"Account_No": "KT-002", "Full_Name": "Sarah Kyomugisha", "Phone": "0772000000", "Status": "Active"},
        {"Account_No": "KT-003", "Full_Name": "John Mukasa", "Phone": "0751000000", "Status": "Active"}
    ])

if 'ledger_db' not in st.session_state:
    # Seed historical entries to generate immediate dashboard reporting analytics
    st.session_state.ledger_db = pd.DataFrame([
        {"ID": 1001, "Timestamp": "2026-10-01 09:30", "Account_No": "KT-001", "Member_Name": "Elijah Tumushangye", "Module": "Savings Module", "Transaction_Type": "Add Savings", "Amount_UGX": 500000.0, "Reference": "Cash Deposit"},
        {"ID": 1002, "Timestamp": "2026-10-01 11:15", "Account_No": "KT-002", "Member_Name": "Sarah Kyomugisha", "Module": "Shares Module", "Transaction_Type": "Buy Shares", "Amount_UGX": 200000.0, "Reference": "Share Capital"},
        {"ID": 1003, "Timestamp": "2026-10-01 14:00", "Account_No": "KT-003", "Member_Name": "John Mukasa", "Module": "Loans Module", "Transaction_Type": "Issue Loan", "Amount_UGX": 1500000.0, "Reference": "Boda Boda Loan Investment"},
        {"ID": 1004, "Timestamp": "2026-10-02 10:00", "Account_No": "KT-001", "Member_Name": "Elijah Tumushangye", "Module": "Loans Module", "Transaction_Type": "Record Repayment", "Amount_UGX": 150000.0, "Reference": "Loan Inst. 1"},
        {"ID": 1005, "Timestamp": "2026-10-02 11:30", "Account_No": "KT-002", "Member_Name": "Sarah Kyomugisha", "Module": "Cash Flow Module", "Transaction_Type": "Record Income", "Amount_UGX": 45000.0, "Reference": "Passbook Fees"}
    ])

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- SYSTEM SECURITY: SYNC & BACKUP PIN LOCK ---
st.sidebar.markdown("# 🔒 SAVINGS PLUS SECURITY")
if not st.session_state.authenticated:
    st.title("🎛️ Savings Plus© Core Banking System")
    st.write("### Kigyende United Traders Account Deployment Portal")
    pin_input = st.text_input("Enter System Access Passcode (PIN Link)", type="password")
    if st.button("Access Database"):
        if pin_input == "1234":  # Default temporary management PIN
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Security Credentials. Please review administrative sync records.")
    st.stop()
else:
    if st.sidebar.button("Log Out / Secure System"):
        st.session_state.authenticated = False
        st.rerun()

# --- MAIN SYSTEM LAYOUT HEADERS ---
st.title("🏦 Savings Plus© Financial Core Platform")
st.write("**Institution:** Kigyende United Traders Association | **System Status:** Online 🟢")
st.write("---")

# --- SAVINGS PLUS 5 CORE ADMINISTRATIVE MODULES ---
st.sidebar.markdown("# 📂 SYSTEM MODULES")
module_choice = st.sidebar.radio("Select Active Module Panel:", [
    "🖥️ Executive Control Dashboard",
    "💰 Savings & Shares Module",
    "📈 Loans Management Portfolio",
    "📊 General Cash Flow Accounting",
    "👥 Client Registry & Accounts"
])

# Global Database Pulls
ledger = st.session_state.ledger_db
members = st.session_state.members_db

def append_transaction(account, name, module, tx_type, amount, ref):
    new_id = ledger["ID"].max() + 1 if not ledger.empty else 1001
    new_tx = pd.DataFrame([{
        "ID": new_id,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Account_No": account,
        "Member_Name": name,
        "Module": module,
        "Transaction_Type": tx_type,
        "Amount_UGX": float(amount),
        "Reference": ref
    }])
    st.session_state.ledger_db = pd.concat([st.session_state.ledger_db, new_tx], ignore_index=True)

# ==================== MODULE 1: CONTROL DASHBOARD ====================
if module_choice == "🖥️ Executive Control Dashboard":
    st.header("Financial Performance Indicators")
    
    # Financial Balance Math Aggregations
    total_savings = ledger[ledger["Transaction_Type"] == "Add Savings"]["Amount_UGX"].sum() - ledger[ledger["Transaction_Type"] == "Savings Withdrawal"]["Amount_UGX"].sum()
    total_shares = ledger[ledger["Transaction_Type"] == "Buy Shares"]["Amount_UGX"].sum()
    loans_issued = ledger[ledger["Transaction_Type"] == "Issue Loan"]["Amount_UGX"].sum()
    loans_repaid = ledger[ledger["Transaction_Type"] == "Record Repayment"]["Amount_UGX"].sum()
    outstanding_loans = loans_issued - loans_repaid
    
    net_income = ledger[ledger["Transaction_Type"] == "Record Income"]["Amount_UGX"].sum() - ledger[ledger["Transaction_Type"] == "Record Expense"]["Amount_UGX"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Member Savings Pool", f"{total_savings:,.0f} UGX")
    col2.metric("Total Paid-Up Share Capital", f"{total_shares:,.0f} UGX")
    col3.metric("Outstanding Loan Portfolio", f"{outstanding_loans:,.0f} UGX")
    col4.metric("Net Office Profit Ledger", f"{net_income:,.0f} UGX")

    st.write("---")
    st.subheader("📊 Association Operational Charts")
    
    if not ledger.empty:
        fig = px.bar(ledger, x="Module", y="Amount_UGX", color="Transaction_Type", 
                     title="Cash Distribution Metrics Across Systems", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📜 Complete Central Audit Log (All Modules)")
        st.dataframe(ledger.sort_values(by="ID", ascending=False), use_container_width=True)
    else:
        st.info("No transaction voucher movements saved in ledger files.")

# ==================== MODULE 2: SAVINGS & SHARES ====================
elif module_choice == "💰 Savings & Shares Module":
    st.header("Member Savings Vault & Share Purchase Registry")
    action = st.radio("Choose Operation Type:", ["Add Savings Deposit", "Process Savings Withdrawal", "Purchase Equity Shares"])
    
    selected_member_name = st.selectbox("Select Association Member Account:", members["Full_Name"].unique())
    selected_account = members[members["Full_Name"] == selected_member_name]["Account_No"].values[0]
    
    amount_input = st.number_input("Transaction Amount (UGX)", min_value=0, step=5000)
    ref_input = st.text_input("Voucher / Payment Memo Reference Details")
    
    if st.button("Post Transaction Entry"):
        if amount_input > 0:
            append_transaction(selected_account, selected_member_name, "Savings & Shares", action, amount_input, ref_input)
            st.success(f"Successfully committed entry: {action} of {amount_input:,.0f} UGX to account {selected_account}")
        else:
            st.error("Input financial balance value must be greater than zero.")

# ==================== MODULE 3: LOANS PORTFOLIO ====================
elif module_choice == "📈 Loans Management Portfolio":
    st.header("Credit Management & Loan Disbursement System")
    action = st.radio("Choose Operation Type:", ["Issue Loan", "Record Repayment"])
    
    selected_member_name = st.selectbox("Select Debtor/Borrower Target Account:", members["Full_Name"].unique())
    selected_account = members[members["Full_Name"] == selected_member_name]["Account_No"].values[0]
    
    amount_input = st.number_input("Loan Principle Transacted Value (UGX)", min_value=0, step=10000)
    ref_input = st.text_input("Loan Disbursal / Repayment Receipt Reference Notes")
    
    if st.button("Post Credit Ledger Voucher"):
        if amount_input > 0:
            append_transaction(selected_account, selected_member_name, "Loans Module", action, amount_input, ref_input)
            st.success(f"Loan Record updated: Logged '{action}' of {amount_input:,.0f} UGX for {selected_member_name}.")
        else:
            st.error("Please insert a valid financial amount configuration.")

# ==================== MODULE 4: CASH FLOW ACCOUNTING ====================
elif module_choice == "📊 General Cash Flow Accounting":
    st.header("Institution Operating Revenue & Expense Vouchers")
    action = st.radio("Choose Operation Type:", ["Record Income", "Record Expense"])
    
    amount_input = st.number_input("Cash Outflow/Inflow Voucher Value (UGX)", min_value=0, step=1000)
    ref_input = st.text_input("Transaction Head Description (e.g., Office Stationery, Interest income, Rent)")
    
    if st.button("Commit Ledger Post"):
        if amount_input > 0:
            append_transaction("INSTITUTION-ACC", "Kigyende Office Base", "Cash Flow Module", action, amount_input, ref_input)
            st.success(f"Office Cash Registry Updated: Recorded {action} of {amount_input:,.0f} UGX under item: '{ref_input}'")
        else:
            st.error("Voucher item value entry cannot be empty.")

# ==================== MODULE 5: CLIENT REGISTRY ====================
elif module_choice == "👥 Client Registry & Accounts":
    st.header("Association Member Profile Master Ledger")
    
    st.subheader("👥 Current Active Accounts List")
    st.dataframe(members, use_container_width=True)
    
    st.write("---")
    st.subheader("➕ Open/Register New Member Account Profile")
    with st.form("Account Provisioning Form"):
