# Enterprise Multi-Agent Compliance Intelligence System (Local-First AI)

## Overview

This project demonstrates a **multi-agent AI architecture for compliance auditing**, built using a fully local stack (Ollama, FastAPI, Streamlit).

It simulates how enterprises can automate **regulatory compliance analysis**, **risk scoring**, and **audit reporting** using modular AI agents.

---

## Key Features

* Multi-agent orchestration (Supervisor, Compliance, Risk)
* Query classification and intelligent routing
* AI-driven compliance gap detection
* Risk scoring engine
* Explainable AI outputs (reasoning + controls)
* Full audit logging (traceability)
* Streamlit-based UI for interactive analysis

---

## Architecture

User Query
↓
Supervisor Agent (Classification)
↓
Orchestrator (Routing)
↓
Compliance Agent (Analysis)
↓
Risk Agent (Scoring)
↓
Audit Logger (Traceability)
↓
UI (Streamlit Dashboard)

---
## Architecture Diagram

![Architecture](assets/architecture.png)
---
## Architecture Highlights

- Modular multi-agent design
- Clear separation of concerns
- Local-first execution
- Cloud portability (Azure-ready)
---
## Example Output

```json
{
  "category": "COMPLIANCE_CHECK",
  "risk_level": "HIGH",
  "reasoning": "User data stored outside EU without safeguards",
  "controls_missing": [
    "Encryption",
    "Data residency enforcement"
  ],
  "recommendation": "Implement SCC and encryption",
  "confidence_score": 0.84
}
```

---

## Tech Stack (Local-First)

* LLM: Ollama (phi3)
* Backend: FastAPI
* UI: Streamlit
* Storage: SQLite
* Orchestration: Python (LangGraph-ready)

---

## Enterprise Mapping (Azure)

| Local Component | Enterprise Equivalent |
| --------------- | --------------------- |
| Ollama          | Azure OpenAI Service  |
| FAISS (planned) | Azure AI Search       |
| SQLite          | Azure Cosmos DB       |
| FastAPI         | Azure App Service     |
| Logs            | Azure Monitor         |

---

## Design Principles

* Local-first development
* Modular agent architecture
* Deterministic outputs
* Observability and traceability
* Cloud portability

---

## Future Enhancements

* RAG with compliance documents
* Multi-regulation support (SOX, HIPAA)
* LangGraph orchestration
* Policy simulation engine
* Role-based access control

---

## Why This Project

This project reflects real-world enterprise needs:

* AI governance
* compliance automation
* risk intelligence systems

---

## Author

Senior Azure Solution Architect (15+ years experience)
