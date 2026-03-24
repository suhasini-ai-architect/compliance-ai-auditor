import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.compliance_agent import compliance_check
from agents.risk_agent import calculate_risk
from utils.db import init_db, log_result

import sqlite3
import pandas as pd



st.set_page_config(page_title="AI Compliance Auditor", layout="wide")

init_db()

st.title("🛡️ AI Compliance Auditor Dashboard")

# Input
query = st.text_area("Enter your query:")

if st.button("Analyze"):
    if query:
        result = compliance_check(query)
        risk = calculate_risk(result)

        # Save
        log_result(query, "COMPLIANCE_CHECK", result, risk)

        st.subheader("📊 Compliance Result")
        st.json(result)

        st.subheader("🚨 Risk Assessment")
        st.json(risk)
    else:
        st.warning("Please enter a query")


# ---- Show Logs ----

st.subheader("📂 Audit Logs")

conn = sqlite3.connect("audit_logs.db")
df = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY id DESC", conn)
conn.close()

st.dataframe(df)