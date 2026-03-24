def calculate_risk(compliance_result):
    risk_map = {
        "LOW": 20,
        "MEDIUM": 50,
        "HIGH": 85
    }

    level = compliance_result.get("risk_level", "LOW")

    score = risk_map.get(level.upper(), 20)

    if score >= 80:
        severity = "CRITICAL"
    elif score >= 50:
        severity = "HIGH"
    else:
        severity = "LOW"

    return {
        "risk_score": score,
        "severity": severity
    }


if __name__ == "__main__":
    sample = {"risk_level": "HIGH"}
    print(calculate_risk(sample))