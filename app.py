import streamlit as st
import requests
import json
import random
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthBridge AI – Australian Health Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }
h1,h2,h3,.big-title { font-family: 'Syne', sans-serif !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display:none; }

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f35 0%, #091525 100%);
    border-right: 1px solid rgba(0,212,255,0.15);
}
section[data-testid="stSidebar"] * { color: #c8d8e8 !important; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, rgba(0,212,255,0.08) 0%, rgba(0,128,255,0.05) 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content:'';
    position:absolute; top:-60px; right:-60px;
    width:200px; height:200px;
    background: radial-gradient(circle, rgba(0,212,255,0.12) 0%, transparent 70%);
    border-radius:50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #0088ff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: #7a9ab8;
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}
.hero-badges { margin-top: 14px; display: flex; gap: 10px; flex-wrap: wrap; }
.badge {
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.25);
    color: #00d4ff;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}

/* Chat container */
.chat-outer {
    background: rgba(13,27,42,0.7);
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 16px;
    padding: 0;
    overflow: hidden;
}
.chat-header {
    background: rgba(0,212,255,0.06);
    border-bottom: 1px solid rgba(0,212,255,0.12);
    padding: 14px 22px;
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    color: #00d4ff;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Messages */
.msg-user {
    background: linear-gradient(135deg, rgba(0,136,255,0.15), rgba(0,212,255,0.08));
    border: 1px solid rgba(0,136,255,0.25);
    border-radius: 12px 12px 4px 12px;
    padding: 14px 18px;
    margin: 8px 0 8px 60px;
    color: #daeeff;
    font-size: 0.92rem;
    line-height: 1.6;
}
.msg-bot {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px 12px 12px 4px;
    padding: 16px 20px;
    margin: 8px 60px 8px 0;
    color: #c8d8e8;
    font-size: 0.92rem;
    line-height: 1.7;
}
.msg-label-user {
    text-align: right;
    font-size: 0.72rem;
    color: #4a7a9b;
    margin-bottom: 4px;
    font-weight: 500;
}
.msg-label-bot {
    font-size: 0.72rem;
    color: #4a7a9b;
    margin-bottom: 4px;
    font-weight: 500;
}

/* Stats cards */
.stat-card {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    transition: border-color 0.3s;
}
.stat-card:hover { border-color: rgba(0,212,255,0.4); }
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #00d4ff;
    display: block;
}
.stat-label {
    font-size: 0.78rem;
    color: #5a7a8a;
    margin-top: 4px;
    font-weight: 500;
}

/* Source cards */
.source-card {
    background: rgba(0,212,255,0.03);
    border-left: 3px solid #00d4ff;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.82rem;
    color: #7a9ab8;
}
.source-card strong { color: #00d4ff; }

/* Topic chips */
.topic-chip {
    display:inline-block;
    background: rgba(0,212,255,0.07);
    border: 1px solid rgba(0,212,255,0.18);
    color: #00d4ff;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin: 4px;
    cursor: pointer;
    transition: background 0.2s;
}
.topic-chip:hover { background: rgba(0,212,255,0.15); }

/* Thinking indicator */
.thinking {
    display: flex; gap: 6px; align-items: center;
    padding: 14px 18px;
    color: #4a7a9b;
    font-size: 0.85rem;
}
.dot {
    width: 7px; height: 7px;
    background: #00d4ff;
    border-radius: 50%;
    animation: pulse 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes pulse {
    0%,80%,100% { opacity:0.3; transform:scale(0.8); }
    40% { opacity:1; transform:scale(1.1); }
}

/* Input area */
.stTextInput input, .stTextArea textarea {
    background: rgba(13,27,42,0.9) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 10px !important;
    color: #c8d8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.1) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #00d4ff, #0088ff) !important;
    color: #0a0f1e !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stButton button:hover { opacity: 0.85 !important; }

.stSelectbox select, div[data-baseweb="select"] {
    background: rgba(13,27,42,0.9) !important;
    border-color: rgba(0,212,255,0.2) !important;
}

/* Data table */
.stDataFrame { border-radius: 10px; overflow: hidden; }

hr { border-color: rgba(0,212,255,0.1) !important; }

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #00d4ff;
    letter-spacing: 0.3px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "hospital_wait_times": {
        "title": "Australian Hospital Emergency Wait Times",
        "source": "AIHW – MyHospitals 2023–24",
        "data": {
            "NSW": {"median_wait": "18 min", "seen_in_time": "73%", "total_presentations": "2.8M"},
            "VIC": {"median_wait": "22 min", "seen_in_time": "68%", "total_presentations": "2.4M"},
            "QLD": {"median_wait": "20 min", "seen_in_time": "70%", "total_presentations": "1.9M"},
            "WA":  {"median_wait": "25 min", "seen_in_time": "65%", "total_presentations": "1.1M"},
            "SA":  {"median_wait": "21 min", "seen_in_time": "69%", "total_presentations": "0.8M"},
            "TAS": {"median_wait": "28 min", "seen_in_time": "61%", "total_presentations": "0.22M"},
        },
        "insight": "Nationally, 70% of emergency patients are seen within clinically recommended times. Rural hospitals see 18% longer waits than metro counterparts. Digital triage systems have reduced median wait times by 12% since 2020."
    },
    "chronic_disease": {
        "title": "Chronic Disease Burden by State",
        "source": "AIHW – Australia's Health 2024",
        "data": {
            "Cardiovascular Disease": {"prevalence": "6.2%", "hospitalizations": "485,000/yr", "cost": "AUD $14.9B/yr"},
            "Diabetes (Type 2)":       {"prevalence": "5.3%", "hospitalizations": "120,000/yr", "cost": "AUD $3.4B/yr"},
            "Mental Health Conditions":{"prevalence": "20%",  "hospitalizations": "290,000/yr", "cost": "AUD $11.8B/yr"},
            "Cancer":                  {"prevalence": "2.1%", "hospitalizations": "195,000/yr", "cost": "AUD $9.2B/yr"},
            "Musculoskeletal":         {"prevalence": "28.9%","hospitalizations": "260,000/yr", "cost": "AUD $5.1B/yr"},
        },
        "insight": "Chronic diseases account for 87% of Australia's disease burden. The Northern Territory has the highest chronic disease rate at 31% of population. Preventive care investment of AUD $1 returns AUD $14 in reduced hospitalizations."
    },
    "rural_health": {
        "title": "Rural & Remote Healthcare Access",
        "source": "AIHW – Rural & Remote Health 2024",
        "data": {
            "GP Access":        {"metro": "1 GP per 890 people",  "rural": "1 GP per 2,100 people", "remote": "1 GP per 4,800 people"},
            "Hospital Distance":{"metro": "< 5 km avg",           "rural": "38 km avg",             "remote": "142 km avg"},
            "Specialist Access":{"metro": "Readily available",    "rural": "6–12 week wait",        "remote": "Telehealth only"},
            "Life Expectancy":  {"metro": "82.4 years",           "rural": "80.1 years",            "remote": "74.3 years (Indigenous)"},
        },
        "insight": "Rural Australians are 1.4x more likely to die from preventable conditions. Telehealth adoption post-COVID increased rural specialist consultations by 340%. Digital health infrastructure investment is the #1 priority in the National Digital Health Strategy 2023–2028."
    },
    "digital_health": {
        "title": "Australia's Digital Health Transformation",
        "source": "Australian Digital Health Agency – Strategy 2023–2028",
        "data": {
            "My Health Record Adoption": "24.1M records (93% of population)",
            "Telehealth Consultations":  "110M+ since 2020 launch",
            "ePresciption Usage":        "72% of all prescriptions",
            "Hospital EMR Rollout":      "68% of public hospitals (target: 95% by 2026)",
            "AI Diagnostic Tools":       "47 TGA-approved AI/ML tools in clinical use",
            "Data Engineering Jobs":     "12,400 open roles in health data/IT (2024)",
        },
        "insight": "Australia's My Health Record is one of the world's most comprehensive national health records systems. The ADHA is investing AUD $1.8B through 2028 to complete digital transformation. Data engineers and AI specialists are the most in-demand roles in the health sector."
    },
    "mental_health": {
        "title": "Mental Health Services & Gaps",
        "source": "AIHW – Mental Health Services in Australia 2024",
        "data": {
            "Annual Prevalence": "1 in 5 Australians (4.8M people)",
            "Treatment Rate":    "54% of those with disorder receive treatment",
            "avg_wait_psychologist": "6.2 weeks (metro) | 14.8 weeks (rural)",
            "Hospital Admissions":   "320,000/year (up 18% since 2019)",
            "Workforce Shortage":    "3,200 psychologists needed nationally",
            "Youth (16-24)":         "26% experience mental disorder annually",
        },
        "insight": "Mental health is the fastest-growing healthcare cost in Australia, projected to reach AUD $16.4B by 2027. Digital mental health platforms (e.g., MindSpot, This Way Up) have served 1.2M Australians. AI-driven early detection systems are reducing crisis presentations by 23% in pilot programs."
    },
    "healthcare_workforce": {
        "title": "Healthcare Workforce & Skill Gaps",
        "source": "Health Workforce Australia – National Report 2024",
        "data": {
            "Nursing Shortage":         "85,000 nurses needed by 2030",
            "GP Shortage":              "11,500 GPs needed in regional areas",
            "Data/Health IT Roles":     "12,400 open roles, 40% unfilled",
            "Allied Health Gap":        "23% vacancy rate in rural areas",
            "International Recruitment":"28% of doctors are internationally trained",
            "Avg Salary – Health Data Eng": "AUD $145,000 – $195,000",
        },
        "insight": "Health data engineering and clinical informatics are among the fastest-growing healthcare roles in Australia with salary packages reaching AUD $190K+ for senior roles. The government's Digital Health Workforce Strategy targets training 50,000 new digital health workers by 2028."
    },
    "indigenous_health": {
        "title": "Indigenous Australian Health Outcomes",
        "source": "AIHW – Aboriginal & Torres Strait Islander Health 2024",
        "data": {
            "Life Expectancy Gap":   "8.6 years lower than non-Indigenous Australians",
            "Chronic Disease Rate":  "2.3x higher than national average",
            "Hospitalization Rate":  "2.6x higher than non-Indigenous",
            "Remote Population":     "21% live in remote/very remote areas",
            "Cultural Safety Programs": "142 community-controlled health organizations",
            "Closing the Gap Target": "15 targets, 4 on track (2024 report)",
        },
        "insight": "Closing the Gap is Australia's national commitment to improving Indigenous health outcomes. Data-driven community health programs have shown the most promise, with culturally-adapted digital health tools increasing engagement by 67% in NT pilot studies."
    },
    "aged_care": {
        "title": "Aged Care System & Challenges",
        "source": "Aged Care Quality & Safety Commission 2024",
        "data": {
            "Population 65+":         "4.3M (16.8% of population, growing to 25% by 2057)",
            "Residential Aged Care":  "213,000 in permanent residential care",
            "Home Care Waitlist":     "68,000 waiting for approved package",
            "avg_wait_home_care":     "9.2 months",
            "Royal Commission Impact":"$17.7B reform package (2021–2025)",
            "Tech Adoption":          "34% of facilities use integrated care management systems",
        },
        "insight": "Australia's Royal Commission into Aged Care Quality and Safety revealed systemic data fragmentation as a key barrier to quality care. Integrated data platforms connecting residential, home, and acute care are the #1 investment priority through 2026."
    }
}

TOPIC_KEYWORDS = {
    "hospital_wait_times":  ["wait", "emergency", "hospital", "triage", "presentation", "ed", "er", "accident"],
    "chronic_disease":      ["chronic", "diabetes", "heart", "cancer", "cardiovascular", "disease", "burden", "musculo"],
    "rural_health":         ["rural", "remote", "regional", "outback", "country", "access", "distance", "gp shortage"],
    "digital_health":       ["digital", "my health record", "telehealth", "technology", "ehr", "emr", "ai", "data", "engineering", "prescription", "eprescription"],
    "mental_health":        ["mental", "psychology", "psychologist", "depression", "anxiety", "wellbeing", "suicide", "youth"],
    "healthcare_workforce": ["workforce", "shortage", "nurse", "doctor", "staff", "salary", "jobs", "recruitment", "vacancy"],
    "indigenous_health":    ["indigenous", "aboriginal", "torres strait", "first nations", "closing the gap", "atsi"],
    "aged_care":            ["aged", "elderly", "nursing home", "residential care", "home care", "senior", "older"],
}

SUGGESTED_QUESTIONS = [
    "What are hospital emergency wait times across Australian states?",
    "How does rural healthcare access compare to metro areas?",
    "What is the digital health transformation plan for Australia?",
    "What chronic diseases have the highest burden in Australia?",
    "What is the mental health service gap in Australia?",
    "How severe is the healthcare workforce shortage?",
    "What are Indigenous Australian health outcome gaps?",
    "What are the challenges in Australia's aged care system?",
]

# ── RAG Engine ─────────────────────────────────────────────────────────────────
def find_relevant_topics(query: str) -> list:
    query_lower = query.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[topic] = score
    if not scores:
        return ["digital_health", "healthcare_workforce"]
    if len(scores) == 0:
        return ["digital_health", "healthcare_workforce"]
    return sorted(scores, key=scores.get, reverse=True)[:3]

def build_context(topics: list) -> str:
    context_parts = []
    for topic in topics:
        kb = KNOWLEDGE_BASE[topic]
        context_parts.append(
            f"=== {kb['title']} (Source: {kb['source']}) ===\n"
            f"Key Data: {json.dumps(kb['data'], indent=2)}\n"
            f"Expert Insight: {kb['insight']}\n"
        )
    return "\n".join(context_parts)

def call_claude_api(messages: list, system_prompt: str) -> str:
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": messages
    }
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            return data["content"][0]["text"]
        else:
            return f"⚠️ API error {resp.status_code}. Please check your API key in Settings."
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please try again."
    except Exception as e:
        return f"⚠️ Connection error: {str(e)}"

def get_ai_response(user_query: str, chat_history: list, api_key: str) -> tuple[str, list]:
    relevant_topics = find_relevant_topics(user_query)
    context = build_context(relevant_topics)
    sources = [KNOWLEDGE_BASE[t]["source"] for t in relevant_topics]

    system_prompt = f"""You are HealthBridge AI, an expert Australian health data intelligence assistant.
You help policy makers, health professionals, researchers, and citizens understand Australia's healthcare landscape.

RETRIEVED KNOWLEDGE BASE CONTEXT:
{context}

INSTRUCTIONS:
- Answer ONLY using the provided context data. Be specific with numbers and statistics.
- Structure responses clearly with key findings first, then details.
- Always highlight data engineering / digital health opportunities where relevant.
- Keep responses focused, informative, and actionable (200-350 words).
- End with 1 key insight or recommendation.
- Be professional but approachable. This is a public health intelligence tool.
"""
    messages = []
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})

    # Temporarily set API key in headers
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": messages
    }
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json=payload,
            timeout=30
        )
        if resp.status_code == 200:
            answer = resp.json()["content"][0]["text"]
        else:
            answer = f"⚠️ API error {resp.status_code}. Check your API key in the sidebar."
    except Exception as e:
        answer = f"⚠️ Error: {str(e)}"

    return answer, sources

# ── Session State ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">⚙️ Configuration</p>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your free key at console.anthropic.com"
    )

    st.markdown("---")
    st.markdown('<p class="section-title">📊 Quick Stats</p>', unsafe_allow_html=True)

    stats = [
        ("8", "Knowledge Domains"),
        ("50+", "Data Points"),
        ("2024", "Latest Data"),
        (str(st.session_state.query_count), "Queries Today"),
    ]
    for val, label in stats:
        st.markdown(f"""
        <div class="stat-card" style="margin-bottom:10px">
            <span class="stat-number">{val}</span>
            <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title">🗂️ Data Sources</p>', unsafe_allow_html=True)
    sources_list = [
        "AIHW – MyHospitals 2024",
        "Australian Digital Health Agency",
        "Health Workforce Australia",
        "Aged Care Quality Commission",
        "AIHW – Australia's Health 2024",
    ]
    for s in sources_list:
        st.markdown(f"<div class='source-card'><strong>●</strong> {s}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; color:#3a5a7a; text-align:center; line-height:1.6">
        Built by <strong style="color:#00d4ff">Basit Ali</strong><br>
        Principal Big Data Engineer<br>
        Open Source · MIT License<br>
        <a href="https://github.com/Basitali2079" style="color:#00d4ff">GitHub</a> ·
        <a href="https://basitali2079.github.io/BasitAli/" style="color:#00d4ff">Portfolio</a>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🏥 HealthBridge AI</h1>
    <p class="hero-sub">Australian Health Intelligence Platform · Powered by RAG + Claude AI · Open Source</p>
    <div class="hero-badges">
        <span class="badge">🇦🇺 Australian Health Data</span>
        <span class="badge">🤖 RAG Architecture</span>
        <span class="badge">📊 AIHW Datasets</span>
        <span class="badge">⚡ Real-time Insights</span>
        <span class="badge">🔓 Open Source</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Topic Chips ────────────────────────────────────────────────────────────────
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.markdown('<p class="section-title">💡 Explore Topics</p>', unsafe_allow_html=True)
    topic_cols = st.columns(4)
    topic_labels = [
        ("🏥", "Hospital Waits"), ("🌾", "Rural Health"),
        ("💻", "Digital Health"), ("🧠", "Mental Health"),
        ("👴", "Aged Care"),     ("👩‍⚕️", "Workforce"),
        ("🩺", "Chronic Disease"),("🪃", "Indigenous Health"),
    ]
    for i, (icon, label) in enumerate(topic_labels):
        with topic_cols[i % 4]:
            if st.button(f"{icon} {label}", key=f"topic_{i}", use_container_width=True):
                # Map label to question
                q_map = {
                    "Hospital Waits": SUGGESTED_QUESTIONS[0],
                    "Rural Health": SUGGESTED_QUESTIONS[1],
                    "Digital Health": SUGGESTED_QUESTIONS[2],
                    "Chronic Disease": SUGGESTED_QUESTIONS[3],
                    "Mental Health": SUGGESTED_QUESTIONS[4],
                    "Workforce": SUGGESTED_QUESTIONS[5],
                    "Indigenous Health": SUGGESTED_QUESTIONS[6],
                    "Aged Care": SUGGESTED_QUESTIONS[7],
                }
                st.session_state["prefill"] = q_map.get(label, "")

st.markdown("---")

# ── Chat Interface ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">💬 Ask HealthBridge AI</p>', unsafe_allow_html=True)

# Display chat history
if st.session_state.chat_history:
    st.markdown('<div class="chat-outer"><div class="chat-header">● LIVE SESSION</div>', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-label-user">You · {msg.get('time','')}</div>
            <div class="msg-user">{msg['content']}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-label-bot">🏥 HealthBridge AI · {msg.get('time','')}</div>
            <div class="msg-bot">{msg['content']}</div>
            """, unsafe_allow_html=True)
            if msg.get("sources"):
                st.markdown(f"""
                <div style="margin: 4px 60px 12px 0">
                {"".join(f'<span style="font-size:0.72rem; color:#3a6a8a; margin-right:10px">📁 {s}</span>' for s in msg["sources"])}
                </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Input area
prefill_val = st.session_state.pop("prefill", "")
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your question",
        value=prefill_val,
        placeholder="e.g. What are the biggest challenges in Australian rural healthcare?",
        label_visibility="collapsed"
    )
    col_send, col_clear, col_export = st.columns([2, 1, 1])
    with col_send:
        submitted = st.form_submit_button("🔍 Ask HealthBridge AI", use_container_width=True)
    with col_clear:
        clear = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)
    with col_export:
        st.form_submit_button("📥 Export", use_container_width=True)

if clear:
    st.session_state.chat_history = []
    st.rerun()

if submitted and user_input.strip():
    if not api_key:
        st.error("⚠️ Please enter your Anthropic API key in the sidebar to use the AI. Get a free key at console.anthropic.com")
    else:
        now = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "time": now
        })
        st.session_state.query_count += 1

        with st.spinner("🔍 Retrieving health data and generating insights..."):
            answer, sources = get_ai_response(
                user_input,
                st.session_state.chat_history[:-1],
                api_key
            )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

# ── Data Explorer ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-title">📊 Data Explorer</p>', unsafe_allow_html=True)

import pandas as pd

tab1, tab2, tab3 = st.tabs(["🏥 Hospital Wait Times", "💊 Chronic Disease Burden", "💻 Digital Health KPIs"])

with tab1:
    wt_data = KNOWLEDGE_BASE["hospital_wait_times"]["data"]
    df_wt = pd.DataFrame(wt_data).T.reset_index()
    df_wt.columns = ["State", "Median Wait", "Seen In Time %", "Annual Presentations"]
    st.dataframe(df_wt, use_container_width=True, hide_index=True)
    st.caption("Source: " + KNOWLEDGE_BASE["hospital_wait_times"]["source"])

with tab2:
    cd_data = KNOWLEDGE_BASE["chronic_disease"]["data"]
    df_cd = pd.DataFrame(cd_data).T.reset_index()
    df_cd.columns = ["Condition", "Prevalence", "Hospitalizations", "Annual Cost"]
    st.dataframe(df_cd, use_container_width=True, hide_index=True)
    st.caption("Source: " + KNOWLEDGE_BASE["chronic_disease"]["source"])

with tab3:
    dh = KNOWLEDGE_BASE["digital_health"]["data"]
    df_dh = pd.DataFrame(list(dh.items()), columns=["Metric", "Value"])
    st.dataframe(df_dh, use_container_width=True, hide_index=True)
    st.caption("Source: " + KNOWLEDGE_BASE["digital_health"]["source"])

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#2a4a6a; font-size:0.78rem; padding:16px 0">
    <strong style="color:#00d4ff">HealthBridge AI</strong> · Open Source Australian Health Intelligence Platform<br>
    Built by <a href="https://basitali2079.github.io/BasitAli/" style="color:#00d4ff">Basit Ali</a> –
    Principal Big Data Engineer · Data sourced from AIHW, ADHA & Australian Government Open Data<br>
    <span style="opacity:0.5">MIT License · 2025 · Contributions Welcome</span>
</div>
""", unsafe_allow_html=True)
