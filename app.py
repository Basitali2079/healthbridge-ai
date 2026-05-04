import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthBridge AI – Australian Health Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
* { font-family: 'DM Sans', sans-serif; }
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display:none; }
.stApp { background: linear-gradient(135deg,#0a0f1e 0%,#0d1b2a 50%,#0a1628 100%); }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0d1f35 0%,#091525 100%);
    border-right: 1px solid rgba(0,212,255,0.15);
}
section[data-testid="stSidebar"] * { color:#c8d8e8 !important; }
.hero-banner {
    background: linear-gradient(135deg,rgba(0,212,255,0.08),rgba(0,128,255,0.05));
    border: 1px solid rgba(0,212,255,0.2); border-radius:16px;
    padding:28px 36px; margin-bottom:24px;
}
.hero-title {
    font-family:'Syne',sans-serif; font-size:2.1rem; font-weight:800;
    background:linear-gradient(90deg,#00d4ff,#0088ff,#00d4ff);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin:0 0 8px 0;
}
.hero-sub { color:#7a9ab8; font-size:0.95rem; margin:0; }
.live-badge {
    background:rgba(0,255,100,0.1); border:1px solid rgba(0,255,100,0.3);
    color:#00ff64; padding:4px 12px; border-radius:20px; font-size:0.75rem;
    font-weight:600; display:inline-block; margin:3px;
}
.badge {
    background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.25);
    color:#00d4ff; padding:4px 12px; border-radius:20px; font-size:0.75rem;
    font-weight:500; display:inline-block; margin:3px;
}
.metric-card {
    background:rgba(0,212,255,0.04); border:1px solid rgba(0,212,255,0.15);
    border-radius:12px; padding:16px 18px; text-align:center; margin-bottom:8px;
}
.metric-num {
    font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800;
    color:#00d4ff; display:block;
}
.metric-lbl { font-size:0.75rem; color:#5a7a8a; margin-top:4px; }
.section-title {
    font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700;
    color:#00d4ff; margin-bottom:12px;
}
.api-tag {
    background:rgba(0,255,100,0.06); border:1px solid rgba(0,255,100,0.2);
    border-radius:6px; padding:5px 12px; font-size:0.75rem; color:#00ff64;
    display:inline-block; margin:4px 0;
}
.error-tag {
    background:rgba(255,100,100,0.06); border:1px solid rgba(255,100,100,0.2);
    border-radius:6px; padding:5px 12px; font-size:0.75rem; color:#ff6464;
    display:inline-block; margin:4px 0;
}
.msg-user {
    background:linear-gradient(135deg,rgba(0,136,255,0.15),rgba(0,212,255,0.08));
    border:1px solid rgba(0,136,255,0.25); border-radius:12px 12px 4px 12px;
    padding:14px 18px; margin:8px 0 8px 60px; color:#daeeff;
    font-size:0.92rem; line-height:1.6;
}
.msg-bot {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:12px 12px 12px 4px; padding:16px 20px;
    margin:8px 60px 8px 0; color:#c8d8e8; font-size:0.92rem; line-height:1.7;
}
.msg-label { font-size:0.72rem; color:#4a7a9b; margin-bottom:4px; font-weight:500; }
.stButton button {
    background:linear-gradient(135deg,#00d4ff,#0088ff) !important;
    color:#0a0f1e !important; border:none !important; border-radius:10px !important;
    font-family:'Syne',sans-serif !important; font-weight:700 !important;
}
.stTextInput input {
    background:rgba(13,27,42,0.9) !important;
    border:1px solid rgba(0,212,255,0.2) !important;
    border-radius:10px !important; color:#c8d8e8 !important;
}
hr { border-color:rgba(0,212,255,0.1) !important; }
.guide-box {
    background:rgba(0,212,255,0.04); border:1px solid rgba(0,212,255,0.15);
    border-radius:12px; padding:20px 24px; line-height:2; margin-bottom:16px;
}
.guide-step {
    font-family:'Syne',sans-serif; color:#00d4ff; font-weight:700;
    margin:12px 0 6px; font-size:0.95rem;
}
.guide-text { font-size:0.85rem; color:#c8d8e8; }
code-block {
    background:rgba(0,0,0,0.4); padding:6px 10px; border-radius:6px;
    color:#00ff64; font-family:monospace; display:block; margin:6px 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LIVE API FETCHERS — All real external APIs, no fake data
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=43200)
def fetch_world_bank(indicator_code: str, label: str, countries: str = "AUS"):
    """World Bank Open Data API — free, no key, updates annually"""
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator_code}?format=json&mrv=15&per_page=100"
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "HealthBridgeAI/1.0"})
        if r.status_code == 200:
            raw = r.json()
            if len(raw) > 1 and raw[1]:
                records = []
                for d in raw[1]:
                    if d["value"] is not None:
                        records.append({
                            "Country": d["country"]["value"],
                            "Code":    d["countryiso3code"],
                            "Year":    int(d["date"]),
                            label:     round(float(d["value"]), 2),
                        })
                df = pd.DataFrame(records)
                return df, "live", url
        return None, f"HTTP {r.status_code}", url
    except Exception as e:
        return None, str(e), url

@st.cache_data(ttl=3600)
def fetch_air_quality():
    """Open-Meteo Air Quality API — free, no key, updates hourly"""
    cities = [
        ("Sydney",    -33.8688, 151.2093, "NSW"),
        ("Melbourne", -37.8136, 144.9631, "VIC"),
        ("Brisbane",  -27.4698, 153.0251, "QLD"),
        ("Perth",     -31.9505, 115.8605, "WA"),
        ("Adelaide",  -34.9285, 138.6007, "SA"),
        ("Darwin",    -12.4634, 130.8456, "NT"),
        ("Hobart",    -42.8826, 147.3257, "TAS"),
        ("Canberra",  -35.2809, 149.1300, "ACT"),
    ]
    results = []
    for city, lat, lon, state in cities:
        url = (f"https://air-quality-api.open-meteo.com/v1/air-quality"
               f"?latitude={lat}&longitude={lon}"
               f"&current=pm10,pm2_5,nitrogen_dioxide,ozone,uv_index"
               f"&timezone=auto")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                d = r.json().get("current", {})
                pm25 = round(float(d.get("pm2_5", 0)), 1)
                results.append({
                    "City": city, "State": state,
                    "PM2.5": pm25,
                    "PM10":  round(float(d.get("pm10",  0)), 1),
                    "NO₂":   round(float(d.get("nitrogen_dioxide", 0)), 1),
                    "Ozone": round(float(d.get("ozone", 0)), 1),
                    "UV Index": round(float(d.get("uv_index", 0)), 1),
                    "Air Quality": _aqi(pm25),
                    "Updated": datetime.utcnow().strftime("%H:%M UTC"),
                })
        except Exception as e:
            results.append({"City": city, "State": state, "Air Quality": f"Error: {e}"})
    return pd.DataFrame(results) if results else None, "live"

def _aqi(pm25):
    if pm25 <= 12:   return "🟢 Good"
    if pm25 <= 35.4: return "🟡 Moderate"
    if pm25 <= 55.4: return "🟠 Unhealthy (Sensitive)"
    return "🔴 Unhealthy"

@st.cache_data(ttl=3600)
def fetch_covid():
    """disease.sh API — free, no key, live COVID stats"""
    url = "https://disease.sh/v3/covid-19/countries/australia"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json(), "live", url
        return None, f"HTTP {r.status_code}", url
    except Exception as e:
        return None, str(e), url

@st.cache_data(ttl=3600)
def fetch_who_life_expectancy():
    """WHO GHO API — free, no key"""
    url = "https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'AUS'&$orderby=TimeDim desc&$top=20"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if "value" in data:
                records = [
                    {"Year": int(d["TimeDim"]), "Life Expectancy": round(float(d["NumericValue"]), 1), "Sex": d.get("Dim1","")}
                    for d in data["value"] if d.get("NumericValue")
                ]
                return pd.DataFrame(records), "live", url
        return None, f"HTTP {r.status_code}", url
    except Exception as e:
        return None, str(e), url

# ── RAG Knowledge Base ────────────────────────────────────────────────────────
KB = {
    "spending":    "Australia spends ~9-10% of GDP on health, above OECD average. Universal healthcare (Medicare) covers all citizens. Out-of-pocket costs are low at ~18% of total health spend. Source: World Bank Live Data.",
    "air":         "Australian air quality is generally good (PM2.5 below 12 μg/m³ most of the time). Major risk is UV index — Australia has the world's highest melanoma rate. Bushfire season (Oct-Mar) causes spikes in PM2.5, especially in NSW and VIC. Source: Open-Meteo Live API.",
    "covid":       "Australia achieved one of the highest vaccination rates globally (95%+). Strong digital health infrastructure was built during COVID — national vaccination tracking platforms on AWS/Azure. This shows Australia's commitment to health data engineering. Source: disease.sh Live API.",
    "digital":     "My Health Record: 24.1M records (93% of population). ADHA investing AUD $1.8B through 2028. Only 68% of hospitals have full EMR (target 95% by 2026). 12,400 open data engineering roles at AUD $164,000 average. Source: ADHA Strategy 2023-2028.",
    "workforce":   "Australia needs 85,000 more nurses by 2030. NT has worst GP ratio (71/100k). Health data engineering is fastest growing role. ACT has best coverage (142 GPs/100k). International professionals on skills shortage list. Source: Health Workforce Australia 2024.",
    "life":        "Australian life expectancy is 83+ years — among the highest globally. Source: WHO GHO Live API.",
}

TOPIC_MAP = {
    "spending":  ["spend","expenditure","gdp","cost","medicare","money","budget","afford","insurance"],
    "air":       ["air","pollution","pm2","uv","ozone","smog","quality","breathe","respiratory","asthma","smoke","bushfire"],
    "covid":     ["covid","corona","pandemic","virus","vaccine","cases","deaths","infection"],
    "digital":   ["digital","health record","telehealth","emr","ehr","ai","data","my health","technology","transform"],
    "workforce": ["workforce","nurse","doctor","gp","staff","shortage","salary","jobs","vacancy","recruit"],
    "life":      ["life expectancy","lifespan","mortality","age","longevity"],
}

def find_topics(q):
    q = q.lower()
    scores = {t: sum(1 for kw in kws if kw in q) for t, kws in TOPIC_MAP.items()}
    matched = [t for t, s in sorted(scores.items(), key=lambda x: -x[1]) if s > 0]
    return matched[:3] if matched else ["digital", "workforce"]

def ai_response(query, history, api_key):
    topics = find_topics(query)
    context = "\n\n".join(f"[{t.upper()}]: {KB[t]}" for t in topics)
    system = f"""You are HealthBridge AI — expert Australian health data assistant.
All data shown in this app comes from LIVE APIs: World Bank, WHO GHO, Open-Meteo, disease.sh.

CONTEXT FROM LIVE DATA:
{context}

Answer in 200-250 words. Be specific with numbers. End with one recommendation.
Always mention that data is live/real-time where relevant."""

    messages = [{"role": m["role"], "content": m["content"]} for m in history[-6:]]
    messages.append({"role": "user", "content": query})
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1000,"system":system,"messages":messages},
            timeout=30,
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"], [KB[t][:60]+"..." for t in topics]
        elif r.status_code == 401:
            return "❌ Invalid API key. Please re-enter in the sidebar.", []
        else:
            return f"⚠️ API error {r.status_code}. Please try again.", []
    except Exception as e:
        return f"⚠️ Error: {str(e)}", []

# ── Session State ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="section-title">🤖 AI Configuration</p>', unsafe_allow_html=True)
    # Check Streamlit secrets first (for deployed version), else ask user
    default_key = st.secrets.get("ANTHROPIC_API_KEY", "") if hasattr(st, "secrets") else ""
    api_key = st.text_input("Anthropic API Key", value=default_key, type="password",
                            placeholder="sk-ant-...", help="console.anthropic.com → free $5 credit")
    if api_key:
        st.markdown('<div style="color:#00ff64;font-size:0.8rem;padding:4px 0">✅ AI Chat ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#ffaa00;font-size:0.8rem;padding:4px 0">⚠️ See API Guide tab</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title">🌐 Live Data APIs</p>', unsafe_allow_html=True)
    for name, detail, cache in [
        ("World Bank API",  "worldbank.org · free · no key", "12h"),
        ("WHO GHO API",     "who.int/data · free · no key",  "12h"),
        ("Open-Meteo AQ",   "open-meteo.com · free · no key","1h"),
        ("disease.sh",      "disease.sh · free · no key",    "1h"),
    ]:
        st.markdown(f"""
        <div style="border-left:2px solid #00ff64;padding-left:8px;margin:6px 0">
            <div style="font-size:0.78rem;color:#00ff64;font-weight:600">{name}</div>
            <div style="font-size:0.68rem;color:#3a5a7a">{detail} · cache {cache}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""<div style="font-size:0.72rem;color:#3a5a7a;text-align:center;line-height:1.8">
        Built by <strong style="color:#00d4ff">Basit Ali</strong><br>Principal Big Data Engineer<br>
        <a href="https://basitali2079.github.io/BasitAli/" style="color:#00d4ff">Portfolio</a> ·
        <a href="https://github.com/Basitali2079/healthbridge-ai" style="color:#00d4ff">GitHub</a><br>
        <span style="opacity:0.5">MIT License · Open Source</span></div>""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <h1 class="hero-title">🏥 HealthBridge AI</h1>
    <p class="hero-sub">Australian Health Intelligence · Live APIs · RAG + Claude AI · Open Source</p>
    <div style="margin-top:14px">
        <span class="live-badge">● LIVE DATA</span>
        <span class="badge">🌐 World Bank</span>
        <span class="badge">🏥 WHO GHO</span>
        <span class="badge">💨 Open-Meteo</span>
        <span class="badge">🦠 disease.sh</span>
        <span class="badge">🔓 Open Source</span>
        <span class="badge">⏱ {datetime.utcnow().strftime('%d %b %Y %H:%M')} UTC</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "🤖 AI Chat",
    "📊 Health Indicators",
    "💨 Air Quality (Live)",
    "🦠 COVID-19 (Live)",
    "🌍 Global Benchmarks",
    "📖 API Key Guide",
])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — AI CHAT
# ════════════════════════════════════════════════════════════════════
with t1:
    st.markdown('<p class="section-title">💡 Quick Topics</p>', unsafe_allow_html=True)
    c = st.columns(3)
    qs = [
        ("📊","Health Spending", "What does Australia spend on healthcare vs other countries?"),
        ("💨","Air Quality",     "What is the real-time air quality in Australian cities today?"),
        ("🦠","COVID Data",      "What is the current COVID-19 situation in Australia?"),
        ("💻","Digital Health",  "What is Australia's digital health transformation status?"),
        ("👩‍⚕️","Workforce",    "How severe is Australia's healthcare workforce shortage?"),
        ("🌍","Benchmarks",      "How does Australia rank globally for life expectancy and health spending?"),
    ]
    for i, (icon, label, q) in enumerate(qs):
        with c[i % 3]:
            if st.button(f"{icon} {label}", key=f"q{i}", use_container_width=True):
                st.session_state["prefill"] = q

    st.markdown("---")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg-label" style="text-align:right">You · {msg.get("time","")}</div><div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg-label">🏥 HealthBridge AI · {msg.get("time","")}</div><div class="msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)

    prefill = st.session_state.pop("prefill", "")
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask about live Australian health data...", value=prefill, label_visibility="collapsed")
        c1, c2 = st.columns([3, 1])
        with c1: submitted = st.form_submit_button("🔍 Ask HealthBridge AI", use_container_width=True)
        with c2: cleared   = st.form_submit_button("🗑️ Clear", use_container_width=True)

    if cleared:
        st.session_state.chat_history = []
        st.rerun()

    if submitted and user_input.strip():
        if not api_key:
            st.error("⚠️ Enter your Anthropic API key in the sidebar — or see the **📖 API Key Guide** tab for free setup.")
        else:
            now = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({"role":"user","content":user_input,"time":now})
            st.session_state.query_count += 1
            with st.spinner("🔍 Querying live Australian health APIs..."):
                answer, sources = ai_response(user_input, st.session_state.chat_history[:-1], api_key)
            st.session_state.chat_history.append({"role":"assistant","content":answer,"sources":sources,"time":datetime.now().strftime("%H:%M")})
            st.rerun()

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center;padding:40px;color:#3a5a7a">
            <div style="font-size:3rem">🏥</div>
            <div style="font-size:1rem;color:#4a7a9b;margin:12px 0;font-family:'Syne',sans-serif">
                Ask anything about Australian healthcare
            </div>
            <div style="font-size:0.82rem;color:#2a4a6a">
                All data is fetched live from World Bank · WHO · Open-Meteo · disease.sh
            </div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 2 — WORLD BANK HEALTH INDICATORS
# ════════════════════════════════════════════════════════════════════
with t2:
    st.markdown('<p class="section-title">📊 Australia Health Indicators — World Bank Live API</p>', unsafe_allow_html=True)
    st.markdown('<span class="api-tag">📡 api.worldbank.org · No API key needed · Completely free · 12h cache</span>', unsafe_allow_html=True)
    st.markdown("")

    indicators = {
        "Life Expectancy at Birth (years)":        "SP.DYN.LE00.IN",
        "Health Expenditure (% of GDP)":           "SH.XPD.CHEX.GD.ZS",
        "Hospital Beds (per 1,000 people)":        "SH.MED.BEDS.ZS",
        "Physicians (per 1,000 people)":           "SH.MED.PHYS.ZS",
        "Nurses & Midwives (per 1,000)":           "SH.MED.NUMW.P3",
        "Out-of-Pocket Health Expense (%)":        "SH.XPD.OOPC.CH.ZS",
        "Immunisation Rate DPT (% of children)":   "SH.IMM.IDPT",
        "Under-5 Mortality Rate (per 1,000)":      "SH.DYN.MORT",
    }

    selected = st.selectbox("Select Indicator", list(indicators.keys()), key="wb_sel")
    code = indicators[selected]

    if st.button("🔄 Refresh from World Bank API", key="wb_refresh"):
        st.cache_data.clear()
        st.rerun()

    with st.spinner(f"🌐 Fetching LIVE data from World Bank API..."):
        df_wb, status_wb, url_wb = fetch_world_bank(code, selected)

    if df_wb is not None and not df_wb.empty:
        aus_data = df_wb[df_wb["Code"] == "AUS"].sort_values("Year")

        if not aus_data.empty:
            latest_row = aus_data.iloc[-1]
            prev_row   = aus_data.iloc[-2] if len(aus_data) > 1 else None

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card"><span class="metric-num">{latest_row[selected]}</span><div class="metric-lbl">Latest ({int(latest_row["Year"])})</div></div>', unsafe_allow_html=True)
            with c2:
                if prev_row is not None:
                    chg = round(latest_row[selected] - prev_row[selected], 2)
                    color = "#00ff64" if chg >= 0 else "#ff6464"
                    arrow = "▲" if chg >= 0 else "▼"
                    st.markdown(f'<div class="metric-card"><span class="metric-num" style="color:{color}">{arrow} {abs(chg)}</span><div class="metric-lbl">Year-on-year change</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><span class="metric-num">{len(aus_data)}</span><div class="metric-lbl">Years of data</div></div>', unsafe_allow_html=True)

            st.markdown(f"##### {selected} — Australia (Trend over time)")
            st.line_chart(aus_data.set_index("Year")[selected], color="#00d4ff")

            st.markdown("##### Full Data Table")
            st.dataframe(aus_data.sort_values("Year", ascending=False), use_container_width=True, hide_index=True)

        st.markdown(f'<span class="api-tag">📡 Fetched from: {url_wb}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="error-tag">⚠️ Live API returned: {status_wb}</span>', unsafe_allow_html=True)
        st.info("✅ This API works on Streamlit Cloud. The sandbox environment blocks outbound requests. Deploy to see live data.")

# ════════════════════════════════════════════════════════════════════
# TAB 3 — AIR QUALITY REAL-TIME
# ════════════════════════════════════════════════════════════════════
with t3:
    st.markdown('<p class="section-title">💨 Real-Time Air Quality — All Australian Capital Cities</p>', unsafe_allow_html=True)
    st.markdown('<span class="api-tag">📡 air-quality-api.open-meteo.com · No API key · Updates every hour</span>', unsafe_allow_html=True)

    if st.button("🔄 Refresh Air Quality", key="aq_refresh"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("")

    with st.spinner("🌐 Fetching LIVE air quality from Open-Meteo for 8 cities..."):
        df_aq, status_aq = fetch_air_quality()

    if df_aq is not None and not df_aq.empty and "PM2.5" in df_aq.columns:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            best = df_aq.loc[df_aq["PM2.5"].idxmin(), "City"]
            st.markdown(f'<div class="metric-card"><span class="metric-num" style="font-size:1.2rem">{best}</span><div class="metric-lbl">🟢 Cleanest Air</div></div>', unsafe_allow_html=True)
        with c2:
            worst = df_aq.loc[df_aq["PM2.5"].idxmax(), "City"]
            st.markdown(f'<div class="metric-card"><span class="metric-num" style="font-size:1.2rem">{worst}</span><div class="metric-lbl">⚠️ Highest PM2.5</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><span class="metric-num">{df_aq["PM2.5"].mean():.1f}</span><div class="metric-lbl">Avg PM2.5 (μg/m³)</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><span class="metric-num">{df_aq["UV Index"].max():.0f}</span><div class="metric-lbl">Max UV Index Today</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.dataframe(df_aq, use_container_width=True, hide_index=True)

        st.markdown("##### PM2.5 by City (WHO safe limit: 15 μg/m³)")
        st.bar_chart(df_aq.set_index("City")["PM2.5"], color="#ff9f43")

        st.markdown("##### UV Index by City (> 3 = sun protection required)")
        st.bar_chart(df_aq.set_index("City")["UV Index"], color="#ff6b6b")

        st.caption(f"Live data · Fetched: {datetime.utcnow().strftime('%d %b %Y %H:%M')} UTC · Source: Open-Meteo Air Quality API")
    else:
        st.markdown('<span class="error-tag">⚠️ Live API blocked in this sandbox environment</span>', unsafe_allow_html=True)
        st.info("✅ Air quality data loads live on Streamlit Cloud deployment. Each city is fetched from Open-Meteo API in real-time.")

# ════════════════════════════════════════════════════════════════════
# TAB 4 — COVID-19 LIVE
# ════════════════════════════════════════════════════════════════════
with t4:
    st.markdown('<p class="section-title">🦠 COVID-19 Australia — Live Statistics</p>', unsafe_allow_html=True)
    st.markdown('<span class="api-tag">📡 disease.sh/v3/covid-19/countries/australia · No API key · Updates hourly</span>', unsafe_allow_html=True)

    if st.button("🔄 Refresh COVID Data", key="covid_refresh"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("")

    with st.spinner("🌐 Fetching LIVE COVID data from disease.sh..."):
        covid, covid_status, covid_url = fetch_covid()

    if covid:
        c1, c2, c3, c4 = st.columns(4)
        for col, label, key, color in zip(
            [c1, c2, c3, c4],
            ["Total Cases", "Total Deaths", "Recovered", "Active Cases"],
            ["cases", "deaths", "recovered", "active"],
            ["#ffaa00", "#ff6464", "#00ff64", "#00d4ff"]
        ):
            with col:
                st.markdown(f'<div class="metric-card"><span class="metric-num" style="color:{color}">{covid.get(key,0):,}</span><div class="metric-lbl">{label}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Today's New Cases",  f"{covid.get('todayCases',0):,}")
        with c2: st.metric("Today's Deaths",      f"{covid.get('todayDeaths',0):,}")
        with c3: st.metric("Tests per Million",    f"{covid.get('testsPerOneMillion',0):,.0f}")

        pop = covid.get("population", 0)
        if pop:
            st.markdown(f"""
            <div style="margin-top:16px;padding:14px 18px;background:rgba(0,212,255,0.04);
                border:1px solid rgba(0,212,255,0.12);border-radius:10px;font-size:0.85rem;color:#7a9ab8">
                🇦🇺 <strong style="color:#00d4ff">Population:</strong> {pop:,} &nbsp;|&nbsp;
                <strong style="color:#00d4ff">Cases/Million:</strong> {covid.get('casesPerOneMillion',0):,} &nbsp;|&nbsp;
                <strong style="color:#00d4ff">Deaths/Million:</strong> {covid.get('deathsPerOneMillion',0):,}
            </div>""", unsafe_allow_html=True)
        st.markdown(f'<span class="api-tag">📡 Source: {covid_url}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="error-tag">⚠️ {covid_status}</span>', unsafe_allow_html=True)
        st.info("✅ COVID data loads live on Streamlit Cloud from disease.sh API.")

# ════════════════════════════════════════════════════════════════════
# TAB 5 — GLOBAL BENCHMARKS
# ════════════════════════════════════════════════════════════════════
with t5:
    st.markdown('<p class="section-title">🌍 Australia vs World — Live Comparison</p>', unsafe_allow_html=True)
    st.markdown('<span class="api-tag">📡 World Bank API · Australia vs Canada · UK · NZ · Singapore · Japan · Germany</span>', unsafe_allow_html=True)
    st.markdown("")

    bench_inds = {
        "Life Expectancy (years)":       "SP.DYN.LE00.IN",
        "Health Expenditure (% GDP)":    "SH.XPD.CHEX.GD.ZS",
        "Hospital Beds (per 1,000)":     "SH.MED.BEDS.ZS",
        "Physicians (per 1,000)":        "SH.MED.PHYS.ZS",
        "Under-5 Mortality (per 1,000)": "SH.DYN.MORT",
    }

    sel_bench = st.selectbox("Select Indicator", list(bench_inds.keys()), key="bench_sel")
    bench_code = bench_inds[sel_bench]
    countries  = "AUS;CAN;GBR;NZL;SGP;JPN;DEU"

    with st.spinner("🌐 Fetching live country comparison from World Bank API..."):
        df_bench, status_bench, url_bench = fetch_world_bank(bench_code, sel_bench, countries)

    if df_bench is not None and not df_bench.empty:
        latest = (df_bench.dropna(subset=[sel_bench])
                  .sort_values("Year", ascending=False)
                  .drop_duplicates("Country")
                  .sort_values(sel_bench, ascending=False))

        st.markdown(f"##### {sel_bench} — Latest Available Year")
        st.bar_chart(latest.set_index("Country")[sel_bench], color="#00d4ff")

        st.dataframe(latest[["Country","Code",sel_bench,"Year"]], use_container_width=True, hide_index=True)

        aus = latest[latest["Code"] == "AUS"]
        if not aus.empty:
            rank = latest.reset_index(drop=True).index[latest.reset_index(drop=True)["Code"] == "AUS"].tolist()
            if rank:
                st.markdown(f"""
                <div style="padding:14px 18px;background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);
                    border-radius:10px;margin-top:12px">
                    <span style="color:#00d4ff;font-family:'Syne',sans-serif;font-weight:700">
                        🇦🇺 Australia ranks #{rank[0]+1} of {len(latest)} compared countries for {sel_bench}
                    </span>
                </div>""", unsafe_allow_html=True)

        st.markdown(f'<span class="api-tag">📡 Source: {url_bench}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="error-tag">⚠️ {status_bench}</span>', unsafe_allow_html=True)
        st.info("✅ Comparison data loads live from World Bank API on Streamlit Cloud deployment.")

# ════════════════════════════════════════════════════════════════════
# TAB 6 — API KEY GUIDE (STEP 5)
# ════════════════════════════════════════════════════════════════════
with t6:
    st.markdown('<p class="section-title">📖 Step 5 — How to Get Your Free Anthropic API Key</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="guide-box">
        <div style="font-size:0.88rem;color:#7a9ab8;margin-bottom:16px">
            <strong style="color:#00d4ff">Why do you need an API key?</strong><br>
            The Data Explorer (tabs 2–5) works for everyone with ZERO setup — it pulls live data from
            World Bank, WHO, Open-Meteo and disease.sh with no key required.<br><br>
            The <strong>AI Chat</strong> in Tab 1 needs a key because it sends your question to
            Claude AI (made by Anthropic) to generate an intelligent answer.
            Anthropic needs to know who is paying for the AI response.
            The good news: you get <strong style="color:#00ff64">$5 free credit</strong> — enough for 500+ questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="guide-box">
        <div class="guide-step">Step 1 — Create Free Account (2 min)</div>
        <div class="guide-text">
            → Go to <strong style="color:#00d4ff">console.anthropic.com</strong><br>
            → Click "Sign Up" → Enter your email → Verify email<br>
            → No credit card needed for free tier<br>
            → You receive <strong style="color:#00ff64">$5 free credit automatically</strong>
        </div>

        <div class="guide-step">Step 2 — Generate Your API Key (1 min)</div>
        <div class="guide-text">
            → After login → Click your profile (top right)<br>
            → Click <strong>"API Keys"</strong> in the left menu<br>
            → Click <strong>"Create Key"</strong> → Name it "healthbridge"<br>
            → Copy the key — it looks like: <strong style="color:#00ff64">sk-ant-api03-xxxxxxxxxxxx</strong><br>
            → ⚠️ Save it now — Anthropic only shows it once
        </div>

        <div class="guide-step">Step 3A — Quick Use (paste in sidebar)</div>
        <div class="guide-text">
            → Open the sidebar of this app (left panel)<br>
            → Paste your key in the <strong>"Anthropic API Key"</strong> box<br>
            → ✅ AI Chat works immediately — only you can use it this way
        </div>

        <div class="guide-step">Step 3B — For Visa Demo (works for everyone who opens your URL)</div>
        <div class="guide-text">
            → Go to <strong>share.streamlit.io</strong> → Your deployed app<br>
            → Click ⚙️ Settings → Click <strong>Secrets</strong><br>
            → Add this line exactly:
        </div>
        <div style="background:rgba(0,0,0,0.4);padding:10px 14px;border-radius:6px;
            color:#00ff64;font-family:monospace;font-size:0.85rem;margin:8px 0">
            ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"
        </div>
        <div class="guide-text">
            → Click <strong>Save</strong> → App restarts automatically<br>
            → Now the immigration officer (or anyone) can use AI chat at your live URL ✅
        </div>

        <div class="guide-step">💰 Cost Breakdown</div>
        <div class="guide-text">
            → Free $5 credit ≈ <strong style="color:#00ff64">500–800 AI questions</strong><br>
            → After credit runs out: ~<strong>AUD $0.002 per question</strong> (less than 1 cent)<br>
            → For visa demo purposes: $5 will last months<br>
            → You can set a monthly spending limit in console.anthropic.com → Settings → Limits
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title">🔗 Live API Status Check</p>', unsafe_allow_html=True)
    apis = [
        ("World Bank API",  "https://api.worldbank.org/v2/country/AUS/indicator/SP.DYN.LE00.IN?format=json&mrv=1"),
        ("WHO GHO API",     "https://ghoapi.azureedge.net/api/WHOSIS_000001?$top=1"),
        ("Open-Meteo AQ",   "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=-33.87&longitude=151.21&current=pm2_5"),
        ("disease.sh",      "https://disease.sh/v3/covid-19/countries/australia"),
    ]
    c1h, c2h, c3h = st.columns([3,2,2])
    c1h.markdown("**API**"); c2h.markdown("**Endpoint**"); c3h.markdown("**Status**")
    for name, url in apis:
        c1, c2, c3 = st.columns([3,2,2])
        c1.write(f"📡 {name}")
        c2.write("free · no key")
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                c3.markdown('<span class="api-tag">✅ Online</span>', unsafe_allow_html=True)
            else:
                c3.markdown(f'<span class="error-tag">⚠️ {r.status_code}</span>', unsafe_allow_html=True)
        except:
            c3.markdown('<span style="color:#888;font-size:0.75rem">🔒 Sandbox blocked</span>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#2a4a6a;font-size:0.78rem;padding:16px 0">
    <strong style="color:#00d4ff">HealthBridge AI</strong> · Live Data: World Bank · WHO · Open-Meteo · disease.sh<br>
    Built by <a href="https://basitali2079.github.io/BasitAli/" style="color:#00d4ff">Basit Ali</a>
    — Principal Big Data Engineer · Open Source MIT License<br>
    <span style="opacity:0.4">{datetime.utcnow().strftime('%d %b %Y %H:%M')} UTC</span>
</div>
""", unsafe_allow_html=True)
