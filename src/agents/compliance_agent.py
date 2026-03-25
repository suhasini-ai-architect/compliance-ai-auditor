import requests
import json
import re

AGENT_NAME = "Compliance Agent"

# -------------------------------
# Ollama call
# -------------------------------
def ask_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": "phi3", "prompt": prompt, "stream": False}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        print(f"OLLAMA ERROR ({AGENT_NAME}):", str(e))
        return ""

# -------------------------------
# Extract structured JSON from LLM output
# -------------------------------
def extract_json(text: str, query: str) -> dict:
    try:
        match = re.search(r'\{[\s\S]*?\}', text)  # non-greedy match
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    # fallback logic
    query_lower = query.lower()
    if "data" in query_lower or "gdpr" in query_lower:
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

# -------------------------------
# Main compliance check
# -------------------------------
def compliance_check(query: str) -> dict:
    """
    Processes a query through Compliance Agent
    Returns structured JSON for UI or logging
    """
    prompt = f"""
You are a GDPR / Compliance expert.

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
    result = extract_json(response, query)

    # Normalize risk level
    risk_level = result.get("risk_level", "MEDIUM").upper()
    result["risk_level"] = risk_level

    # Map to numeric score
    mapping = {
        "LOW": 0.3,
        "MEDIUM": 0.6,
        "HIGH": 0.9
    }
    result["risk_score"] = mapping.get(risk_level, 0.5)

    # Add agent trace
    result["_agent"] = AGENT_NAME

    return result