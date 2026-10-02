import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- PAGE SETUP & TRADITIONAL SAVINGS PLUS THEME ---
st.set_page_config(page_title="Savings Plus - Kigyende United Traders", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 5px; border-left: 5px solid #003366; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1 { color: #003366; font-family: 'Arial Black', sans-serif; }
    h2 { color: #004080; }
    </style>
""", unsafe_allow_html=True)

# --- FILE-BASED PERMANENT DATABASE PATHS ---
DATA_DIR = "data"
LEDGER_FILE = os.path.join(DATA_DIR, "transactions.csv")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.csv")

# Ensure the local folders and database tracking files exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(MEMBERS_FILE):
    initial_members = pd.DataFrame([
        {"Account_No": "KT-001", "Full_Name": "Elijah Tumushangye", "Phone": "0700000000", "Status": "Active"},
        {"Account_No": "KT-002", "Full_Name": "Sarah Kyomugisha", "Phone": "0772000000", "Status": "Active"}
    ])
    initial_members.to_csv(MEMBERS_FILE, index=False)

if not os.path.exists(LEDGER_FILE) or os.stat(LEDGER_FILE).st_size == 0:
    initial_ledger = pd.DataFrame(columns=["ID", "Timestamp", "Account_No", "Member_Name", "Module", "Transaction_Type", "Amount_UGX", "Reference"])
    initial_ledger.to_csv(LEDGER_FILE, index=False)

# Load data into live tracking session states
@st.cache_data(ttl=1)  # Refresh cache instantly to prevent stale views
def load_db(file_path):
    return pd.read_csv(file_path)

members_df = load_db(MEMBERS_FILE)
ledger_df = load_db(LEDGER_FILE)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- SYSTEM SECURITY: SYNC & BACKUP PIN LOCK ---
st.sidebar.markdown("# 🔒 SAVINGS PLUS SECURITY")
if not st.session_state.authenticated:
    st.title("🎛️ Savings Plus© Core Banking System")
    st.write("### Kigyende United Traders Data Management Portal")
    pin_input = st.text_input("Enter System Access Passcode (PIN Link)", type="password")
    if st.button("Access Secure Database"):
        if pin_input == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Security Credentials. Please review administrative sync records.")
    st.stop()
else:
    if st.sidebar.button("Log Out / Secure System"):
        st.session_state.authenticated = False
        st.rerun()

# --- MAIN NAVIGATION HEADERS ---
st.title("🏦 Savings Plus© Financial Core Platform")
st.write("**Institution:** Kigyende United Traders Association | **Data Preservation Mode:** Permanent Local File Storage 💾")
st.write("---")

st.sidebar.markdown("# 📂 SYSTEM MODULES")
module_choice = st.sidebar.radio("Select Active Module Panel:", [
    "🖥️ Executive Control Dashboard",
    "💰 Savings & Shares Module",
    "📈 Loans Management Portfolio",
    "📊 General Cash Flow Accounting",
    "👥 Client Registry & Accounts"
])

# Permanent file writer worker function
def append_and_save_transaction(account, name, module, tx_type, amount, ref):
    current_ledger = pd.read_csv(LEDGER_FILE)
    new_id = current_ledger["ID"].max() + 1 if not current_ledger.empty else 1001
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
    updated_ledger = pd.concat([current_ledger, new_tx], ignore_index=True)
    updated_ledger.to_csv(LEDGER_FILE, index=False)
    st.cache_data.clear() # Wipe cache to load new data entries immediately

# ==================== MODULE 1: CONTROL DASHBOARD ====================
if module_choice == "🖥️ Executive Control Dashboard":
    st.header("Financial Performance Indicators")
    
    if not ledger_df.empty:
        # Aggregation computations straight from stored CSV files
        total_savings = ledger_df[ledger_df["Transaction_Type"] == "Add Savings"]["Amount_UGX"].sum() - ledger_df[ledger_df["Transaction_Type"] == "Savings Withdrawal"]["Amount_UGX"].sum()
        total_shares = ledger_df[ledger_df["Transaction_Type"] == "Buy Shares"]["Amount_UGX"].sum()
        loans_issued = ledger_df[ledger_df["Transaction_Type"] == "Issue Loan"]["Amount_UGX"].sum()
        loans_repaid = ledger_df[ledger_df["Transaction_Type"] == "Record Repayment"]["Amount_UGX"].sum()
        outstanding_loans = loans_issued - loans_repaid
        net_income = ledger_df[ledger_df["Transaction_Type"] == "Record Income"]["Amount_UGX"].sum() - ledger_df[ledger_df["Transaction_Type"] == "Record Expense"]["Amount_UGX"].sum()
    else:
        total_savings, total_shares, outstanding_loans, net_income = 0, 0, 0, 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Member Savings Pool", f"{total_savings:,.0f} UGX")
    col2.metric("Total Paid-Up Share Capital", f"{total_shares:,.0f} UGX")
    col3.metric("Outstanding Loan Portfolio", f"{outstanding_loans:,.0f} UGX")
    col4.metric("Net Office Profit Ledger", f"{net_income:,.0f} UGX")

    st.write("---")
    st.subheader("📜 Live Database Transaction Ledger")
    
    if not ledger_df.empty:
        fig = px.bar(ledger_df, x="Module", y="Amount_UGX", color="Transaction_Type", title="Cash Operations Breakdown", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ledger_df.sort_values(by="ID", ascending=False), use_container_width=True)
    else:
        st.info("The system log is completely empty. Please visit modules to insert data entries.")

# ==================== MODULE 2: SAVINGS & SHARES ====================
elif module_choice == "💰 Savings & Shares Module":
    st.header("Member Savings Vault & Share Purchase Registry")
    action = st.radio("Choose Operation Type:", ["Add Savings", "Savings Withdrawal", "Buy Shares"])
    
    selected_member_name = st.selectbox("Select Association Member Account:", members_df["Full_Name"].unique())
    selected_account = members_df[members_df["Full_Name"] == selected_member_name]["Account_No"].values[0]
    
    amount_input = st.number_input("Transaction Amount (UGX)", min_value=0, step=5000)
    ref_input = st.text_input("Voucher Reference details")
    
    if st.button("Post Transaction Entry"):
        if amount_input > 0:
            append_and_save_transaction(selected_account, selected_member_name, "Savings & Shares", action, amount_input, ref_input)
            st.success(f"Successfully saved {action} value of {amount_input:,.0f} UGX to local file storage!")
            st.rerun()

# ==================== MODULE 3: LOANS PORTFOLIO ====================
elif module_choice == "📈 Loans Management Portfolio":
    st.header("Credit Management & Loan Disbursement System")
    action = st.radio("Choose Operation Type:", ["Issue Loan", "Record Repayment"])
    
    selected_member_name = st.selectbox("Select Debtor Target Account:", members_df["Full_Name"].unique())
    selected_account = members_df[members_df["Full_Name"] == selected_member_name]["Account_No"].values[0]
    
    amount_input = st.number_input("Loan Principle Transacted Value (UGX)", min_value=0, step=10000)
    ref_input = st.text_input("Loan Receipt Reference Notes")
    
    if st.button("Post Credit Ledger Voucher"):
        if amount_input > 0:
            append_and_save_transaction(selected_account, selected_member_name, "Loans Module", action, amount_input, ref_input)
            st.success(f"Transaction recorded permanently into CSV repository database!")
            st.rerun()

# ==================== MODULE 4: CASH FLOW ACCOUNTING ====================
elif module_choice == "📊 General Cash Flow Accounting":
    st.header("Institution Operating Revenue & Expense Vouchers")
    action = st.radio("Choose Operation Type:", ["Record Income", "Record Expense"])
    
    amount_input = st.number_input("Cash Outflow/Inflow Voucher Value (UGX)", min_value=0, step=1000)
    ref_input = st.text_input("Transaction Head Description (e.g. Office Rent, Transport fees)")
    
    if st.button("Commit Ledger Post"):
        if amount_input > 0:
            append_and_save_transaction("INSTITUTION-ACC", "Kigyende Office Base", "Cash Flow Module", action, amount_input, ref_input)
            st.success(f"Voucher transaction written successfully to tracking database files.")
            st.rerun()

# ==================== MODULE 5: CLIENT REGISTRY ====================
elif module_choice == "👥 Client Registry & Accounts":
    st.header("Association Member Profile Master Ledger")
    st.dataframe(members_df, use_container_width=True)
    
    st.write("---")
    st.subheader("➕ Onboard New Member Account Profile")
    with st.form("Account Provisioning Form"):
        new_name = st.text_input("Enter Applicant's Full Legal Name")
        new_phone = st.text_input("Active Telephone Contact Number")
        submit_reg = st.form_submit_button("Provision Member Code Account")
        
        if submit_reg and new_name.strip() != "":
            current_members = pd.read_csv(MEMBERS_FILE)
            next_num = len(current_members) + 1
            new_acc_code = f"KT-{next_num:03d}"
            
            new_profile = pd.DataFrame([{"Account_No": new_acc_code, "Full_Name": new_name.strip(), "Phone": new_phone, "Status": "Active"}])
            updated_members = pd.concat([current_members, new_profile], ignore_index=True)
            updated_members.to_csv(MEMBERS_FILE, index=False)
            
            st.cache_data.clear()
            st.success(f"Successfully generated new account card for {new_name} as ID {new_acc_code}!")
            st.rerun()
