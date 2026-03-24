import requests
import json
import re


def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi3",   # ✅ use phi3
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


def extract_json(text, query):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    # ✅ fallback logic (VERY IMPORTANT)
    if "data" in query.lower() or "gdpr" in query.lower():
        return {
            "risk_level": "HIGH",
            "applicable_regulation": "GDPR",
            "issue": "Potential data compliance issue",
            "recommendation": "Review data handling and apply safeguards"
        }

    return {
        "risk_level": "MEDIUM",
        "applicable_regulation": "Unknown",
        "issue": "Parsing failed",
        "recommendation": "Manual review required"
    }


def compliance_check(query):
    prompt = f"""
You are a GDPR compliance expert.

Return ONLY JSON. No explanation.

Format:
{{
  "risk_level": "LOW or MEDIUM or HIGH",
  "applicable_regulation": "GDPR",
  "issue": "short issue",
  "recommendation": "clear action"
}}

Example:
{{
  "risk_level": "HIGH",
  "applicable_regulation": "GDPR",
  "issue": "Data stored outside EU without safeguards",
  "recommendation": "Use encryption and SCC"
}}

Query: {query}
"""

    response = ask_ollama(prompt)
    return extract_json(response, query)