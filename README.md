# 🏥 HealthBridge AI — Australian Health Intelligence Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://healthbridge-ai.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Data: AIHW 2024](https://img.shields.io/badge/Data-AIHW%202024-green.svg)](https://www.aihw.gov.au/)

> An open-source AI-powered health intelligence chatbot that enables policy makers, researchers, clinicians, and citizens to explore Australia's healthcare landscape through natural language queries.

Demo Link: https://demo-healthbridge-ai.streamlit.app/
---

## 🎯 What It Does

HealthBridge AI uses **Retrieval-Augmented Generation (RAG)** to answer natural language questions about Australian health data — grounded in real datasets from the Australian Institute of Health and Welfare (AIHW) and the Australian Digital Health Agency (ADHA).

**Ask questions like:**
- *"What are hospital emergency wait times across Australian states?"*
- *"How does rural healthcare access compare to metro areas?"*
- *"What is the digital health transformation plan for Australia?"*
- *"What are the biggest gaps in Indigenous Australian health outcomes?"*
- *"What chronic diseases cost Australia the most?"*

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│         RAG Pipeline                │
│  ┌──────────────────────────────┐   │
│  │  1. Query Analysis           │   │
│  │     (keyword extraction)     │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│  ┌──────────▼───────────────────┐   │
│  │  2. Context Retrieval        │   │
│  │     (Knowledge Base lookup)  │   │
│  │     - AIHW Hospital Data     │   │
│  │     - Chronic Disease Stats  │   │
│  │     - Rural Health Metrics   │   │
│  │     - Digital Health KPIs    │   │
│  │     - Mental Health Data     │   │
│  │     - Workforce Statistics   │   │
│  │     - Indigenous Health      │   │
│  │     - Aged Care Data         │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│  ┌──────────▼───────────────────┐   │
│  │  3. Augmented Generation     │   │
│  │     (Claude claude-sonnet-4-20250514 API)    │   │
│  │     Context-grounded answer  │   │
│  └──────────┬───────────────────┘   │
└────────────-┼───────────────────────┘
             │
    ┌────────▼────────┐
    │  Streamlit UI   │
    │  + Data Tables  │
    └─────────────────┘
```

---

## 📊 Data Domains Covered

| Domain | Source | Coverage |
|--------|--------|----------|
| Hospital Wait Times | AIHW MyHospitals 2023–24 | All 6 states |
| Chronic Disease Burden | AIHW Australia's Health 2024 | 5 major conditions |
| Rural & Remote Health | AIHW Rural Health 2024 | Metro/Rural/Remote |
| Digital Health KPIs | Australian Digital Health Agency 2024 | 6 key metrics |
| Mental Health Services | AIHW Mental Health Services 2024 | National + state |
| Healthcare Workforce | Health Workforce Australia 2024 | Shortage data |
| Indigenous Health | AIHW ATSI Health 2024 | Closing the Gap |
| Aged Care | Aged Care Quality Commission 2024 | National stats |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Basitali2079/healthbridge-ai.git
cd healthbridge-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Add your API key
Enter your [Anthropic API key](https://console.anthropic.com/) in the sidebar.  
*(Free tier available — no credit card required for testing)*

---

## ☁️ Deploy for Free (Streamlit Cloud)

1. Fork this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select this repo → set main file: `app.py`
4. Add `ANTHROPIC_API_KEY` in Secrets (optional — users can add their own key)
5. Click **Deploy** — live in 2 minutes ✅

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI/LLM | Anthropic Claude (claude-sonnet-4-20250514) |
| RAG Pipeline | Custom Python (keyword-based retrieval) |
| Data Processing | Pandas |
| Data Sources | AIHW, ADHA, Health Workforce Australia |
| Deployment | Streamlit Community Cloud (free) |
| Language | Python 3.9+ |

---

## 🗺️ Roadmap

- [ ] **v1.1** — Vector embeddings with FAISS for semantic search
- [ ] **v1.2** — Live data ingestion from data.gov.au APIs
- [ ] **v1.3** — Interactive Plotly charts for all data domains
- [ ] **v1.4** — PDF report generation for policy makers
- [ ] **v2.0** — Multi-modal: upload Medicare/PBS data for custom analysis
- [ ] **v2.1** — Predictive analytics (disease burden forecasting)

---

## 🤝 Contributing

Contributions are welcome! This project was built to support Australia's digital health community.

```bash
# Fork → Clone → Create branch
git checkout -b feature/your-feature
# Make changes → Commit → Push → PR
```

**Ideas for contribution:**
- Add more AIHW datasets (PBS, MBS, cancer screening)
- Improve the RAG with vector search
- Add state-level filtering
- Build a comparison mode (state vs state)

---

## 📖 About the Author

Built by **[Basit Ali](https://basitali2079.github.io/BasitAli/)** — Principal Big Data & Cloud Data Engineer with 9+ years building national-scale data platforms across healthcare, telecom, and government.

This project was inspired by work on Saudi Arabia's **National Patient Profile Platform** (Health Grid AI) — consolidating healthcare data from 100+ hospital systems. HealthBridge AI applies the same data engineering principles to Australia's open health data ecosystem.

**Connect:**
- 🌐 [Portfolio](https://basitali2079.github.io/BasitAli/)
- 💼 [LinkedIn](https://www.linkedin.com/in/basit-ali-93211811b/)
- 📧 Basitali4545@yahoo.com

---

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

## ⭐ Star This Repo

If HealthBridge AI is useful to you, please **star** this repository — it helps the project reach more people in the Australian health data community!

---

*Data sourced from AIHW, ADHA, and Australian Government open data portals. This tool is for informational purposes only and does not constitute medical or health policy advice.*
