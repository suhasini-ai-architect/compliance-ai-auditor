# main.py

from src.agents.compliance_agent import compliance_check
from src.agents.risk_agent import calculate_risk
from src.utils.db import log_result

def process_query(query):
    """
    Full pipeline: classify, run compliance, calculate risk, return structured result
    """
    # Simple classification (for now only compliance check)
    category = "COMPLIANCE_CHECK"

    if category == "COMPLIANCE_CHECK":
        compliance_result = compliance_check(query)
        risk_score = calculate_risk(compliance_result)

        # Log into SQLite
        log_result(query, category, compliance_result, risk_score)

        return {
            "category": category,
            "compliance_result": compliance_result,
            "risk_score": risk_score
        }

    else:
        return {
            "category": category,
            "compliance_result": {},
            "risk_score": None
        }

# Optional: test locally
if __name__ == "__main__":
    test_query = "Check GDPR compliance risks for storing user data in Pune data center"
    result = process_query(test_query)
    print(result)