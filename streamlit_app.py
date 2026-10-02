import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Savings Plus - Kigyende United Traders", layout="wide")

# --- CUSTOM INTERFACE STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stMetric { background-color: #ffffff; padding: 18px; border-radius: 6px; border-top: 5px solid #006633; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #004d26; font-family: 'Segoe UI', sans-serif; font-weight: bold; }
    h2, h3 { color: #006633; }
    .stButton>button { background-color: #006633; color: white; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- THE ABSOLUTE SOURCE DATABASES FROM YOUR WORKBOOK ---
if 'members_db' not in st.session_state:
    st.session_state.members_db = pd.DataFrame([
        {"Member_ID": "M001", "Full_Name": "TUMURAMYE AUGUSTINA", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M002", "Full_Name": "TWESIGYE LAURIANO", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M003", "Full_Name": "BAREKYE PROSPER", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M004", "Full_Name": "ORISHABA THOMAS", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M005", "Full_Name": "MONDAY EVARISTO", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M006", "Full_Name": "TAYEBWA ALEXANDER", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M007", "Full_Name": "KARURU CHRISTOPHER", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M008", "Full_Name": "MUCUNGUZI ABERT", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M009", "Full_Name": "MWEBAZE NABORTH", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M010", "Full_Name": "BYARUGABA DAVID", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M011", "Full_Name": "KOMUGISHA AGNESS", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M015", "Full_Name": "NATURINDA BENSON", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M016", "Full_Name": "MUSINGUZI AMON", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M017", "Full_Name": "ORIKIRIZA BRAIN", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M018", "Full_Name": "ARINAITWE HAPPY", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M020", "Full_Name": "MAGEZI YORAM", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M021", "Full_Name": "GUMISHABE HAPPINESS", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M023", "Full_Name": "BIRUNGI FRANK", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M024", "Full_Name": "BASIGA PETER 2", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M025", "Full_Name": "TWESIGYE EVARIST", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M026", "Full_Name": "TIBENDERANA BESERI", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M033", "Full_Name": "NINSIIMA UDITAH", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M035", "Full_Name": "TUMUSHABE ROBINAH", "Date_Joined": "2023-11-10", "Status": "Dormant"},
        {"Member_ID": "M038", "Full_Name": "NASASIRA BOAZ", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M039", "Full_Name": "BYARUHANGA MOSES", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M040", "Full_Name": "NKURUNUNGI FRED", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M044", "Full_Name": "NATUKUNDA EMILIANO", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M045", "Full_Name": "BAGUMA ALEX", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M046", "Full_Name": "TWASIIMA OLIVA", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M047", "Full_Name": "BESIGYE WILSON", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M048", "Full_Name": "BYAMUGISHA ANDREW", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M057", "Full_Name": "KABAREBE ALFAT", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M058", "Full_Name": "TAYEBWA MOSES", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M060", "Full_Name": "NIWAGABA SATRINA", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M066", "Full_Name": "BYARUHANGA SILIANO", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M068", "Full_Name": "AGABA ABIAS", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M069", "Full_Name": "TUMUKUNDE COSTANCE", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M076", "Full_Name": "BYENSI FELEX", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M084", "Full_Name": "AKANKWASA JUNIOR", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M086", "Full_Name": "KYOMUHANGI LYDIA", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M088", "Full_Name": "BUSINGYE ERICK", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M098", "Full_Name": "MATSIKO RICHARD", "Date_Joined": "2023-11-10", "Status": "Active"},
        {"Member_ID": "M099", "Full_Name": "TUMURANZE GERALD", "Date_Joined": "2026-02-08", "Status": "Active"},
        {"Member_ID": "M100", "Full_Name": "FRANCIS MUKOKO", "Date_Joined": "2023-11-10", "Status": "Active"}
    ])

if 'ledger_db' not in st.session_state:
    st.session_state.ledger_db = pd.DataFrame([
        {"Date": "2023-11-10", "Member_ID": "M001", "Category": "Membership Fee", "Loan_ID": "-", "Amount_UGX": 110000},
        {"Date": "2023-11-10", "Member_ID": "M002", "Category": "Membership Fee", "Loan_ID": "-", "Amount_UGX": 110000},
        {"Date": "2023-11-10", "Member_ID": "M003", "Category": "Membership Fee", "Loan_ID": "-", "Amount_UGX": 110000},
        {"Date": "2023-11-10", "Member_ID": "Rt.Hon", "Category": "Donation (Tayebwa Thomas)", "Loan_ID": "-", "Amount_UGX": 50000000},
        {"Date": "2024-06-20", "Member_ID": "M035", "Category": "Loan Repayment - Interest", "Loan_ID": "L035", "Amount_UGX": 6000},
        {"Date": "2024-06-20", "Member_ID": "M035", "Category": "Loan Repayment - Principal", "Loan_ID": "L035", "Amount_UGX": 100000},
        {"Date": "2023-12-19", "Member_ID": "M040", "Category": "Loan Repayment - Interest", "Loan_ID": "L040", "Amount_UGX": 15000},
        {"Date": "2023-12-19", "Member_ID": "M040", "Category": "Loan Repayment - Principal", "Loan_ID": "L040", "Amount_UGX": 135000},
        {"Date": "2026-02-02", "Member_ID": "M100", "Category": "Loan Repayment - Principal", "Loan_ID": "L117", "Amount_UGX": 1254200},
        {"Date": "2026-03-12", "Member_ID": "M058", "Category": "Loan Repayment - Principal", "Loan_ID": "L058", "Amount_UGX": 180000}
    ])

if 'loans_db' not in st.session_state:
    st.session_state.loans_db = pd.DataFrame([
        {"Loan_ID": "L001", "Member_ID": "M001", "Member_Name": "TUMURAMYE AUGUSTINA", "Date_Issued": "2023-12-22", "Principal_UGX": 2000000, "Interest_Method": "Reducing Balance", "Status": "Overdue", "Balance_UGX": 21210},
        {"Loan_ID": "L002", "Member_ID": "M002", "Member_Name": "TWESIGYE LAURIANO", "Date_Issued": "2023-12-20", "Principal_UGX": 2000000, "Interest_Method": "Reducing Balance", "Status": "Overdue", "Balance_UGX": 351635},
        {"Loan_ID": "L003", "Member_ID": "M003", "Member_Name": "BAREKYE PROSPER", "Date_Issued": "2024-01-01", "Principal_UGX": 1500000, "Interest_Method": "Reducing Balance", "Status": "Settled", "Balance_UGX": 0},
        {"Loan_ID": "L060", "Member_ID": "M060", "Member_Name": "NIWAGABA SATRINA", "Date_Issued": "2024-02-21", "Principal_UGX": 1000000, "Interest_Method": "Reducing Balance", "Status": "Settled", "Balance_UGX": 0},
        {"Loan_ID": "L128", "Member_ID": "M060", "Member_Name": "NIWAGABA SATRINA", "Date_Issued": "2026-03-12", "Principal_UGX": 2000000, "Interest_Method": "Flat", "Status": "Settled", "Balance_UGX": 0},
        {"Loan_ID": "L160", "Member_ID": "M060", "Member_Name": "NIWAGABA SATRINA", "Date_Issued": "2026-04-13", "Principal_UGX": 2000000, "Interest_Method": "Flat", "Status": "Overdue", "Balance_UGX": 1688166}
    ])

# --- NAVIGATION SHEETS PANEL ---
st.sidebar.markdown("# 📁 SYSTEM MODULES")
panel_choice = st.sidebar.radio("Select Active Workbook Tab:", [
    "📈 Central Performance Dashboard",
    "👥 Members Directory (99 Profiles)",
    "💸 Loans Portfolio Registry",
    "📊 Financial Central Ledger",
    "🖨️ Automated Member Statement"
])

# Global database pulls
m_df = st.session_state.members_db
l_df = st.session_state.ledger_db
loans_df = st.session_state.loans_db

# ==================== TAB 1: PERFORMANCE DASHBOARD ====================
if panel_choice == "📈 Central Performance Dashboard":
    st.header("Kigyende United Traders Association - Mitooma")
    st.write("### Executive Summary Dashboard Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Members Registered", "99 Profiles")
    col2.metric("Total Savings Pool Balance", "2,776,000 UGX")
    col3.metric("Total Principal Disbursed", "240,350,000 UGX")
    col4.metric("Total Loans Outstanding", "94,869,204 UGX")
    
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Overdue Loans Count", "118 Records")
    col6.metric("Total Revenue Logged", "239,144,300 UGX")
    col7.metric("Total Operating Expenditure", "1,500,000 UGX")
    col8.metric("Cash Box Balance (Latest)", "6,889,590 UGX")
    
    st.write("---")
    st.subheader("⚠️ Interest Recouperation Data Variance")
