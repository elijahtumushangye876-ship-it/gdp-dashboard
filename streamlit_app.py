import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Page Configuration & Custom Theme
st.set_page_config(page_title="Kigyende United Traders System", layout="wide", initial_sidebar_state="expanded")

# Initialize Session States to act as a live database in memory
if 'members' not in st.session_state:
    st.session_state.members = ["John Doe", "Sarah Namubiru", "David Okello", "Grace Kabasomi"]
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Timestamp", "Member", "Action Type", "Amount_UGX", "Notes"])
if 'security_pin' not in st.session_state:
    st.session_state.security_pin = "1234"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# 2. Security System: Sync & Backup PIN Lock
st.sidebar.markdown("## 🔒 System Security")
if not st.session_state.authenticated:
    input_pin = st.sidebar.text_input("Enter Backup PIN to Access System", type="password", key="pin_entry")
    if st.sidebar.button("Unlock System"):
        if input_pin == st.session_state.security_pin:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.sidebar.error("❌ Incorrect PIN. Please try again.")
else:
    if st.sidebar.button("🔒 Lock System"):
        st.session_state.authenticated = False
        st.rerun()

# Stop execution if not authenticated
if not st.session_state.authenticated:
    st.title("🔰 Kigyende United Traders Financial System")
    st.warning("Please enter your Sync & Backup PIN in the left sidebar to unlock the association records.")
    st.stop()

# 3. Main Dashboard Header
st.title("🏢 Kigyende United Traders")
st.subheader("Association Management & Financial Ledger System")
st.write("---")

# 4. Sidebar Navigation Panels matching the HTML Layout
st.sidebar.markdown("## 🧭 Navigation Panels")
menu = st.sidebar.radio("Go to:", [
    "📈 Overview Analytics", 
    "💸 Loans Ledger (Issue & Repay)", 
    "🏦 Savings Vault (Deposit & Withdraw)", 
    "📊 Cash Flow (Income & Expense)", 
    "👥 Member Directory"
])

# Helper function to inject new log entries into the database
def log_transaction(member, action_type, amount, notes=""):
    new_row = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Member": member,
        "Action Type": action_type,
        "Amount_UGX": float(amount),
        "Notes": notes
    }])
    st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)

# ----------------- PANEL 1: OVERVIEW ANALYTICS -----------------
if menu == "📈 Overview Analytics":
    st.header("Financial Performance Overview")
    
    # Mathematical aggregation formulas from current states
    tx = st.session_state.transactions
    total_income = tx[tx["Action Type"] == "Record Income"]["Amount_UGX"].sum()
    total_expense = tx[tx["Action Type"] == "Record Expense"]["Amount_UGX"].sum()
    total_savings = tx[tx["Action Type"] == "Add Savings"]["Amount_UGX"].sum() - tx[tx["Action Type"] == "Savings Withdrawal"]["Amount_UGX"].sum()
    total_loans_issued = tx[tx["Action Type"] == "Issue Loan"]["Amount_UGX"].sum()
    total_loans_repaid = tx[tx["Action Type"] == "Record Repayment"]["Amount_UGX"].sum()
    active_loans_out = total_loans_issued - total_loans_repaid
    
    # Financial KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net Cash Flow Balance", f"{total_income - total_expense:,.0f} UGX")
    c2.metric("Total Association Savings Vault", f"{total_savings:,.0f} UGX")
    c3.metric("Outstanding Active Loans Out", f"{active_loans_out:,.0f} UGX")
    c4.metric("Total Members Registered", f"{len(st.session_state.members)}")
    
    st.write("---")
    st.subheader("📜 Recent Operational Log Transactions")
    if tx.empty:
        st.info("No transaction data entries have been captured yet.")
    else:
        st.dataframe(tx.sort_values(by="Timestamp", ascending=False), use_container_width=True)
        
        # Performance Analytics Bar Plot Chart
        fig = px.bar(tx, x="Action Type", y="Amount_UGX", color="Action Type", title="Volume Breakdown by Activity Category")
        st.plotly_chart(fig, use_container_width=True)

# ----------------- PANEL 2: LOANS LEDGER -----------------
elif menu == "💸 Loans Ledger (Issue & Repay)":
    st.header("Loan Portfolio Management")
    tab1, tab2 = st.tabs(["🔹 Issue Loan", "🔸 Record Repayment"])
    
    with tab1:
        st.write("### Authorize and Issue a New Member Loan")
        loan_member = st.selectbox("Select Recipient Member", st.session_state.members, key="loan_mem")
        loan_amt = st.number_input("Loan Principal Amount (UGX)", min_value=0, step=1000, key="loan_amt")
        loan_notes = st.text_input("Loan Terms / Return Date Notes", key="loan_notes")
        if st.button("Confirm & Disburse Loan"):
            if loan_amt > 0:
                log_transaction(loan_member, "Issue Loan", loan_amt, loan_notes)
                st.success(f"Successfully processed loan of {loan_amt:,.0f} UGX to {loan_member}")
            else:
                st.error("Amount must be greater than zero.")
                
    with tab2:
        st.write("### Record Incoming Loan Principal/Interest Repayment")
        repay_member = st.selectbox("Select Repaying Member", st.session_state.members, key="repay_mem")
        repay_amt = st.number_input("Repayment Amount Collected (UGX)", min_value=0, step=1000, key="repay_amt")
        repay_notes = st.text_input("Receipt Reference Notes", key="repay_notes")
        if st.button("Log Repayment Receipt"):
            if repay_amt > 0:
                log_transaction(repay_member, "Record Repayment", repay_amt, repay_notes)
                st.success(f"Recorded collection update: {repay_amt:,.0f} UGX from {repay_member}")
            else:
                st.error("Amount must be greater than zero.")

# ----------------- PANEL 3: SAVINGS VAULT -----------------
elif menu == "🏦 Savings Vault (Deposit & Withdraw)":
    st.header("Member Personal Savings Registry")
    tab1, tab2 = st.tabs(["🔹 Add Savings", "🔸 Savings Withdrawal"])
    
    with tab1:
        st.write("### Accept Member Savings Deposit Contribution")
        sav_member = st.selectbox("Select Contributor Member", st.session_state.members, key="sav_mem")
        sav_amt = st.number_input("Savings Deposit Value (UGX)", min_value=0, step=1000, key="sav_amt")
        if st.button("Log Savings Contribution"):
            if sav_amt > 0:
                log_transaction(sav_member, "Add Savings", sav_amt, "Member voluntary savings entry")
                st.success(f"Credited {sav_amt:,.0f} UGX to {sav_member}'s savings pool.")
                
    with tab2:
        st.write("### Process Member Savings Account Cash Out/Withdrawal")
        with_member = st.selectbox("Select Withdrawing Member", st.session_state.members, key="with_mem")
        with_amt = st.number_input("Withdrawal Value Requested (UGX)", min_value=0, step=1000, key="with_amt")
        if st.button("Authorize Savings Cash Out"):
            if with_amt > 0:
                log_transaction(with_member, "Savings Withdrawal", with_amt, "Approved cash out withdrawal")
                st.success(f"Debited {with_amt:,.0f} UGX from {with_member}'s balance vault.")

# ----------------- PANEL 4: CASH FLOW -----------------
elif menu == "📊 Cash Flow (Income & Expense)":
    st.header("General Office Cash Flow Accounting")
    tab1, tab2 = st.tabs(["🔹 Record Income", "🔸 Record Expense"])
    
    with tab1:
        st.write("### Record Direct Non-Member Association Income Entry")
        inc_source = st.text_input("Income Category Revenue Source (e.g., Application Fees, Grants, Produce Sales)")
        inc_amt = st.number_input("Collected Gross Value (UGX)", min_value=0, step=1000, key="inc_amt")
        if st.button("Commit Income Voucher"):
            if inc_amt > 0:
                log_transaction("Association Account", "Record Income", inc_amt, inc_source)
                st.success(f"Logged entry: {inc_amt:,.0f} UGX to association income accounts.")
                
    with tab2:
        st.write("### Record Direct Internal Operating Expense Transaction")
        exp_purpose = st.text_input("Expense Purpose (e.g., Office Rent, Stationary, Refreshments, Transport)")
        exp_amt = st.number_input("Disbursed Cash Outflow Value (UGX)", min_value=0, step=1000, key="exp_amt")
        if st.button("Commit Expense Voucher"):
            if exp_amt > 0:
                log_transaction("Association Account", "Record Expense", exp_amt, exp_purpose)
                st.success(f"Logged expenditure: Outflow of {exp_amt:,.0f} UGX recorded.")

# ----------------- PANEL 5: MEMBER DIRECTORY -----------------
elif menu == "👥 Member Directory":
    st.header("Association Roster Registry")
    
    # Form UI block to add members
    with st.form("Add New Member Profile"):
        new_name = st.text_input("Enter Full Legal Name of New Associate Member")
        submit_btn = st.form_submit_button("➕ Register & Add Member")
        if submit_btn and new_name.strip() != "":
            if new_name.strip() not in st.session_state.members:
                st.session_state.members.append(new_name.strip())
                st.success(f"Member '{new_name}' successfully onboarded into the ledger profile systems.")
                st.rerun()
            else:
                st.warning("This member name profile configuration already exists.")
                
    st.write("---")
    st.subheader("📋 Official Member Rosters")
    for index, name in enumerate(sorted(st.session_state.members)):
        st.write(f"**{index + 1}.** {name}")
