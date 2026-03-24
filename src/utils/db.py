import sqlite3
from datetime import datetime
import json

DB_NAME = "audit_logs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        category TEXT,
        compliance_result TEXT,
        risk_score INTEGER,
        severity TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_result(query, category, compliance_result, risk):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO audit_logs (query, category, compliance_result, risk_score, severity, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        query,
        category,
        json.dumps(compliance_result),
        risk.get("risk_score"),
        risk.get("severity"),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()