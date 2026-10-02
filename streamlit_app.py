import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- TRADITIONAL SACCO BRANDING & SETUP ---
st.set_page_config(page_title="Kigyende United Traders Association", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stMetric { background-color: #ffffff; padding: 18px; border-radius: 6px; border-top: 4px solid #006633; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #004d26; font-family: 'Segoe UI', sans-serif; font-weight: bold; }
    h2, h3 { color: #006633; }
    .stButton>button { background-color: #006633; color: white; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Datasets if empty with exact Document Backlogs
if 'initialized_data' not in st.session_state:
    st.session_state.initialized_data = True
    
    # Static master KPIs from document audit row
    st.session_state.kpis = {
        "total_members": 99,
        "total_savings": 2776000,
        "total_principal_disbursed": 240350000,
        "total_loans_outstanding": 94869204,
        "overdue_loans_count": 118,
        "total_income_all_time": 239144300,
        "total_expenditure_all_time": 1500000,
        "total_insurance_collected": 3511500,
        "total_fines_accrued": 5639564,
        "cash_in_hand_latest": 6889590,
        "interest_due": 21716750,
        "interest_received": 16736600
    }

    # Populate verified members from page rules roster
    st.session_state.members_list = [
        {"Member_ID": "M001", "Name": "TUMURAMYE AUGUSTINA", "Status": "Active"},
        {"Member_ID": "M002", "Name": "TWESIGYE LAURIANO", "Status": "Active"},
        {"Member_ID": "M003", "Name": "BAREKYE PROSPER", "Status": "Active"},
        {"Member_ID": "M004", "Name": "ORISHABA THOMAS", "Status": "Active"},
        {"Member_ID": "M005", "Name": "MONDAY EVARISTO", "Status": "Active"},
        {"Member_ID": "M006", "Name": "TAYEBWA ALEXANDER", "Status": "Active"},
        {"Member_ID": "M007", "Name": "KARURU CHRISTOPHER", "Status": "Active"},
        {"Member_ID": "M008", "Name": "MUCUNGUZI ABERT", "Status": "Active"},
        {"Member_ID": "M009", "Name": "MWEBAZE NABORTH", "Status": "Active"},
        {"Member_ID": "M010", "Name": "BYARUGABA DAVID", "Status": "Active"},
        {"Member_ID": "M035", "Name": "TUMUSHABE ROBINAH", "Status": "Dormant"},
        {"Member_ID": "M060", "Name": "NIWAGABA SATRINA", "Status": "Active"},
        {"Member_ID": "M098", "Name": "MATSIKO RICHARD", "Status": "Active"},
        {"Member_ID": "M100", "Name": "FRANCIS MUKOKO", "Status": "Active"}
    ]

    # Populate active loan portfolio data matching audit sheets
    st.session_state.loans_portfolio = [
        {"Loan_ID": "L001", "Member_ID": "M001", "Name": "TUMURAMYE AUGUSTINA", "Principal": 2000000, "Date_Issued": "2023-12-22", "Method": "Reducing Balance", "Status": "Overdue", "Balance": 21210},
        {"Loan_ID": "L002", "Member_ID": "M002", "Name": "TWESIGYE LAURIANO", "Principal": 2000000, "Date_Issued": "2023-12-20", "Method": "Reducing Balance", "Status": "Overdue", "Balance": 351635},
        {"Loan_ID": "L003", "Member_ID": "M003", "Name": "BAREKYE PROSPER", "Principal": 1500000, "Date_Issued": "2024-01-01", "Method": "Reducing Balance", "Status": "Settled", "Balance": 0},
        {"Loan_ID": "L060", "Member_ID": "M060", "Name": "NIWAGABA SATRINA", "Principal": 1000000, "Date_Issued": "2024-02-21", "Method": "Reducing Balance", "Status": "Settled", "Balance": 0},
        {"Loan_ID": "L128", "Member_ID": "M060", "Name": "NIWAGABA SATRINA", "Principal": 2000000, "Date_Issued": "2026-03-12", "Method": "Flat", "Status": "Settled", "Balance": 0},
        {"Loan_ID": "L160", "Member_ID": "M060", "Name": "NIWAGABA SATRINA", "Principal": 2000000, "Date_Issued": "2026-04-13", "Method": "Flat", "Status": "Overdue", "Balance": 1688166}
    ]

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- SYNC & BACKUP PASSCODE CONTROL ---
st.sidebar.markdown("# 🔒 GATEWAY SECURITY")
if not st.session_state.authenticated:
    st.title("🔰 Kigyende United Traders Association")
    st.subheader("Mitooma, Uganda — Secure Management Terminal")
    access_pin = st.text_input("Enter Association Backup Passcode PIN", type="password")
    if st.button("Unlock Association Ledger"):
        if access_pin == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials. Verify with management sync record parameters.")
    st.stop()

# --- MAIN WORKBOOK APP LAYOUT ---
st.title("📋 Kigyende United Traders Central Ledger")
st.write("Financial Records Portal — Mitooma Districts Management Base")
st.write("---")

# Navigation sheet panels matching workbook layout mapping rules
st.sidebar.markdown("# 📂 WORKBOOK SHEETS")
panel = st.sidebar.radio("Go to Workbook Section:", [
    "📊 Central Yearly Dashboard",
    "👥 Members & Onboarding",
    "💰 Savings Vault Ledger",
    "📥 Income Entry Log",
    "📤 Expenditure Flow Book",
    "💸 Loans Portfolio Registry",
    "🖨️ Loan Repayment Amortization Schedule"
])

# Extract configurations for computing fields dynamically
kpis = st.session_state.kpis
m_df = pd.DataFrame(st.session_state.members_list)
l_df = pd.DataFrame(st.session_state.loans_portfolio)

# ==================== PANEL 1: DASHBOARD SURPLUS ====================
if panel == "📊 Central Yearly Dashboard":
    st.header("Financial Position & Key Performance Aggregations")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Members Enrolled", f"{kpis['total_members']} Members")
    col2.metric("Total Member Savings Pool", f"{kpis['total_savings']:,} UGX")
    col3.metric("Total Loans Outstanding", f"{kpis['total_loans_outstanding']:,} UGX")
    col4.metric("Cash in Hand (Latest)", f"{kpis['cash_in_hand_latest']:,} UGX")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Active Overdue Loans (Count)", f"{kpis['overdue_loans_count']} Loans")
    col6.metric("Total Operating Revenue", f"{kpis['total_income_all_time']:,} UGX")
    col7.metric("Insurance Fund Accumulated", f"{kpis['total_insurance_collected']:,} UGX")
    col8.metric("Fines Balance Accrued", f"{kpis['total_fines_accrued']:,} UGX")
    
    st.write("---")
    st.subheader("📈 Macro Cash Flow Distributions (All Time Tracking Data)")
    chart_data = pd.DataFrame([
        {"Metric": "Revenue Balance", "Value_UGX": kpis['total_income_all_time']},
        {"Metric": "Savings Pools", "Value_UGX": kpis['total_savings']},
        {"Metric": "Loan Credit Out", "Value_UGX": kpis['total_principal_disbursed']},
        {"Metric": "Operating Cost Outflow", "Value_UGX": kpis['total_expenditure_all_time']}
    ])
    fig = px.bar(chart_data, x="Metric", y="Value_UGX", color="Metric", title="Association Capital Portfolio Analysis")
    st.plotly_chart(fig, use_container_width=True)

# ==================== PANEL 2: MEMBERS REGISTRY ====================
elif panel == "👥 Members & Onboarding":
    st.header("Members Profile Master Registry")
    st.dataframe(m_df, use_container_width=True)
    
    st.write("---")
    st.subheader("➕ Onboard New Associate Member Profile")
    with st.form("Member Form"):
        m_id = st.text_input("Assigned Short Member ID (e.g., M101, M102)")
        m_name = st.text_input("Enter Full Legal Applicant Name")
        m_status = st.selectbox("Current Account Classification Status", ["Active", "Dormant"])
        submitted = st.form_submit_button("Register Profile Sheet Entry")
        if submitted and m_id and m_name:
            st.session_state.members_list.append({"Member_ID": m_id.strip().upper(), "Name": m_name.strip().upper(), "Status": m_status})
            st.success(f"Profile saved! Member '{m_name}' pinned under target key sequence index.")
            st.rerun()

# ==================== PANEL 3: SAVINGS LEDGER ====================
elif panel == "💰 Savings Vault Ledger":
    st.header("Savings Pool Contributions Registry")
    st.info("💡 Entry Note: Savings are captured on a yearly timeline sequence. Do not insert specific fractional calendars.")
    
    select_mem = st.selectbox("Target Contributor Profile Account:", m_df["Name"].unique())
    select_id = m_df[m_df["Name"] == select_mem]["Member_ID"].values[0]
    
    save_year = st.selectbox("Target Operating Financial Year Block", ["2024", "2025", "2026", "2027"])
    save_amt = st.number_input("Deposited Contribution Capital Value (UGX)", min_value=0, step=10000)
    
    if st.button("Commit Savings Token"):
        if save_amt > 0:
            st.session_state.kpis["total_savings"] += save_amt
            st.success(f"Successfully posted savings increment! Credited account index: {select_id} for Fiscal Year {save_year}.")
            st.rerun()

# ==================== PANEL 4: INCOME VOUCHER ====================
elif panel == "📥 Income Entry Log":
    st.header("Income Management & Cash Vouchers")
    
    inc_cat = st.selectbox("Revenue Allocation Classification Category", [
        "Membership Fee", "Loan Repayment - Principal", "Loan Repayment - Interest", "Fine Payment", "Donation Vouchers", "Forms & Miscellaneous Income"
    ])
    inc_mem = st.selectbox("Associated Member Actor Context", m_df["Member_ID"].unique())
    inc_amt = st.number_input("Gross Inward Value Collected (UGX)", min_value=0, step=5000)
    
    if st.button("Commit Income Voucher Log"):
        if inc_amt > 0:
            st.session_state.kpis["total_income_all_time"] += inc_amt
            st.session_state.kpis["cash_in_hand_latest"] += inc_amt
            st.success(f"Income item committed! Cash-box index updated successfully.")
            st.rerun()

# ==================== PANEL 5: EXPENDITURE BOOK ====================
elif panel == "📤 Expenditure Flow Book":
    st.header("Expenditure Disbursal Vouchers")
    
