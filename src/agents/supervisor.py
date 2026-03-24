import requests
from src.agents.compliance_agent import compliance_check
from src.agents.risk_agent import calculate_risk
from src.utils.db import init_db, log_result


def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi3",   # ✅ use phi3 (fits your RAM)
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        print("OLLAMA RAW:", data)

        return data.get("response", "")

    except Exception as e:
        print("OLLAMA ERROR:", str(e))
        return ""


def classify_query(query):
    prompt = f"""
Classify this query into ONE word:

COMPLIANCE_CHECK → if legal, GDPR, privacy, data laws
RISK_ANALYSIS → if risk scoring
RETRIEVAL → if asking for info
GENERAL → anything else

Return ONLY the word.

Query: {query}
"""

    response = ask_ollama(prompt)
    response = response.strip().upper()

    if "COMPLIANCE" in response:
        return "COMPLIANCE_CHECK"
    elif "RISK" in response:
        return "RISK_ANALYSIS"
    elif "RETRIEVAL" in response:
        return "RETRIEVAL"
    else:
        return "GENERAL"


if __name__ == "__main__":
    init_db()

    query = "Check GDPR compliance risks for storing user data in Pune data center"

    category = classify_query(query)
    print("\n🧠 Query Classification:", category)

    if category == "COMPLIANCE_CHECK":
        print("➡️ Running Compliance Agent...\n")

        result = compliance_check(query)
        print("📊 Compliance Result:", result)

        risk = calculate_risk(result)
        print("\n🚨 Risk Assessment:", risk)

        log_result(query, category, result, risk)

    elif category == "RETRIEVAL":
        print("➡️ Route to Retriever Agent")

    elif category == "RISK_ANALYSIS":
        print("➡️ Route to Risk Agent")

    else:
        print("➡️ Route to General LLM")