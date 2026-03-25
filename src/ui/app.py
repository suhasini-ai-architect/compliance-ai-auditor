import streamlit as st
import sys
import os
import sqlite3
import pandas as pd
import json

# -------------------------------
# Add project root to path so main.py is importable
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import process_query        # main.py at root folder
from src.utils.db import init_db      # utils/db.py inside src

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🛡️ AI Compliance Auditor", layout="wide")
init_db()

st.title("🛡️ AI Compliance Auditor Dashboard")

# -------------------------------
# Input Section
# -------------------------------
st.subheader("🔍 Enter a query for analysis")
query = st.text_area("Your query here:")

# -------------------------------
# Risk color function (bulletproof)
# -------------------------------
def risk_color(risk_score):
    try:
        # If a dict is passed accidentally
        if isinstance(risk_score, dict):
            risk_score = risk_score.get("score", 0.0)
        risk_score = float(risk_score)
    except:
        return "gray"

    if risk_score >= 0.7:
        return "red"
    elif risk_score >= 0.4:
        return "orange"
    return "green"

# -------------------------------
# Analyze Button
# -------------------------------
if st.button("Analyze"):
    if query.strip():
        # Call full pipeline
        result = process_query(query)

        # ---- Compliance Result ----
        st.subheader("📊 Compliance Result")
        st.json(result.get("compliance_result", "No result"))

        # ---- Risk Assessment ----
        st.subheader("🚨 Risk Assessment")

        # Get risk_score safely from compliance_result
        risk_score = result.get("compliance_result", {}).get("risk_score", 0.0)
        if isinstance(risk_score, dict):
            risk_score = risk_score.get("score", 0.0)

        try:
            risk_score = float(risk_score)
        except:
            risk_score = 0.0

        st.markdown(
            f"<div style='color:{risk_color(risk_score)}; font-weight:bold; font-size:18px'>Risk Score: {risk_score}</div>",
            unsafe_allow_html=True
        )

        # ---- Agent Trace ----
        st.subheader("🧠 Agent Trace")
        st.markdown(f"""
**Category:** {result.get('category')}  
**Processed by:** {result.get('compliance_result', {}).get('_agent', result.get('category'))}
""")

        # ---- Download JSON Report ----
        st.download_button(
            label="📥 Download JSON Report",
            data=json.dumps(result, indent=2),
            file_name="audit_report.json",
            mime="application/json"
        )
    else:
        st.warning("Please enter a query")

# -------------------------------
# Audit Logs Section
# -------------------------------
st.subheader("📂 Audit Logs")
conn = sqlite3.connect("audit_logs.db")
df = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY id DESC", conn)
conn.close()
st.dataframe(df)