import streamlit as st
from scenario_catalog import SCENARIOS
from shared import get_state, new_mission, reset, speak, set_state
from ui import page, refresh

page("MISSION CONTROL")
refresh(1400, "operator")

# ---------- MISSION CONTROL VISUAL SYSTEM ----------
st.markdown("""
<style>
.block-container{
    max-width:1560px !important;
    padding-top:.7rem !important;
}

/* Make Streamlit controls fit the dark NHCC interface */
[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label{
    color:#8fa9bb !important;
    font-weight:750 !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] input{
    background:#0c2539 !important;
    color:#fff !important;
    border:1px solid rgba(102,215,255,.22) !important;
    border-radius:14px !important;
}
[data-baseweb="select"] > div{
    background:#0c2539 !important;
    color:#fff !important;
    border-color:rgba(102,215,255,.22) !important;
}
[data-baseweb="select"] *{
    color:#fff !important;
}

/* Hard button overrides */
[data-testid="stButton"] button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"],
button[kind="secondary"],
button[kind="primary"]{
    background:linear-gradient(145deg,#0c2a40,#0b3850) !important;
    color:#fff !important;
    border:1px solid rgba(102,215,255,.3) !important;
    border-radius:15px !important;
    min-height:55px !important;
    font-weight:900 !important;
}
[data-testid="stButton"] button:hover{
    background:linear-gradient(145deg,#123f61,#0a5670) !important;
    border-color:#66d7ff !important;
}
[data-testid="stButton"] button *{
    color:#fff !important;
}
.launch div.stButton > button{
    background:linear-gradient(90deg,#ff3f50,#d9253e) !important;
    border-color:rgba(255,120,130,.65) !important;
    box-shadow:0 0 30px rgba(255,63,80,.16) !important;
}
.launch div.stButton > button:hover{
    background:linear-gradient(90deg,#ff5260,#e72e45) !important;
}

/* Cards */
.hero{
    margin:20px 0 18px;
    padding:24px 26px;
    border-radius:24px;
    border:1px solid rgba(102,215,255,.16);
    background:
      radial-gradient(circle at 84% 10%,rgba(0,163,224,.16),transparent 28%),
      linear-gradient(135deg,rgba(10,35,55,.94),rgba(6,23,38,.94));
    box-shadow:0 22px 70px rgba(0,0,0,.24);
}
.eyebrow{
    color:#67d7ff;
    letter-spacing:.18em;
    font-weight:900;
    font-size:.75rem;
}
.hero-title{
    font-size:2rem;
    font-weight:950;
    line-height:1.1;
    margin-top:7px;
    color:white;
}
.hero-copy{
    color:#9fb5c7;
    margin-top:8px;
    max-width:880px;
    line-height:1.55;
}
.live-dot{
    display:inline-block;
    width:9px;height:9px;border-radius:50%;
    background:#62edbd;
    box-shadow:0 0 16px rgba(98,237,189,.8);
    margin-right:7px;
}

.scenario-card{
    background:linear-gradient(145deg,rgba(12,42,64,.93),rgba(8,31,49,.96));
    border:1px solid rgba(102,215,255,.16);
    border-radius:20px;
    padding:21px 22px;
    min-height:150px;
}
.card-k{
    color:#65d8ff;
    font-size:.72rem;
    font-weight:900;
    letter-spacing:.15em;
}
.card-title{
    color:#fff;
    font-size:1.45rem;
    font-weight:950;
    margin-top:8px;
}
.card-meta{
    color:#91aabc;
    font-size:.9rem;
    margin-top:7px;
}
.pills{margin-top:15px}
.pill{
    display:inline-block;
    border:1px solid rgba(102,215,255,.16);
    color:#a9c5d6;
    background:rgba(0,163,224,.06);
    border-radius:999px;
    padding:5px 9px;
    margin-right:5px;
    margin-bottom:5px;
    font-size:.72rem;
}

.section-title{
    color:#fff;
    font-weight:950;
    font-size:1.1rem;
    margin:8px 0 10px;
}
.section-sub{
    color:#7893a7;
    font-size:.82rem;
    margin-top:-7px;
    margin-bottom:9px;
}

.stat-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:10px;
}
.stat{
    background:rgba(8,34,54,.82);
    border:1px solid rgba(102,215,255,.12);
    border-radius:16px;
    padding:14px 15px;
}
.stat-v{
    color:#fff;
    font-weight:950;
    font-size:1.5rem;
}
.stat-l{
    color:#829caf;
    font-size:.75rem;
    margin-top:2px;
}
.risk-low{color:#6de6bc}
.risk-mid{color:#ffc768}
.risk-high{color:#ff7884}

.timeline{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:8px;
    margin:10px 0 5px;
}
.step{
    position:relative;
    border-radius:14px;
    padding:12px 8px;
    text-align:center;
    border:1px solid rgba(102,215,255,.12);
    background:rgba(9,31,49,.78);
    color:#6f8b9f;
    font-size:.76rem;
    font-weight:800;
}
.step.active{
    color:#fff;
    border-color:rgba(102,215,255,.55);
    background:linear-gradient(145deg,rgba(0,163,224,.25),rgba(0,118,129,.18));
    box-shadow:0 0 22px rgba(0,163,224,.08);
}
.step.done{
    color:#92ead0;
    border-color:rgba(98,237,189,.25);
}

.event-strip{
    margin-top:10px;
    border-radius:18px;
    border:1px solid rgba(255,88,105,.24);
    background:linear-gradient(90deg,rgba(153,29,42,.18),rgba(9,31,49,.85));
    padding:15px 18px;
}
.event-k{
    color:#ff7584;
    font-size:.72rem;
    letter-spacing:.14em;
    font-weight:900;
}
.event-t{
    color:#fff;
    font-size:1rem;
    font-weight:900;
    margin-top:4px;
}

.voicebox{
    background:rgba(9,31,49,.72);
    border:1px solid rgba(102,215,255,.13);
    border-radius:18px;
    padding:16px 18px;
}
.small-note{
    color:#718b9d;
    font-size:.76rem;
}
</style>
""", unsafe_allow_html=True)

s = get_state()
scenario = s["scenario"]

# ---------- HELPERS ----------
stage_order = ["idle", "alert", "investigating", "correlating", "ready_for_decision"]
stage_names = {
    "idle": "READY",
    "alert": "SIGNAL",
    "investigating": "INVESTIGATE",
    "correlating": "CORRELATE",
    "ready_for_decision": "INSIGHT",
    "simulation": "SIMULATION",
    "escalated": "HUMAN REVIEW",
    "complete": "COMPLETE",
}
stage = s.get("stage", "idle")

def risk_class(v):
    if v >= 70:
        return "risk-high"
    if v >= 40:
        return "risk-mid"
    return "risk-low"

def advance_to(target):
    mapping = {
        "alert": dict(stage="alert", alert_active=True,
                      active_agents=0, signals_connected=1, confidence=31,
                      risk_score=max(32, int(s.get("risk_score", 18)))),
        "investigating": dict(stage="investigating", alert_active=True,
                              active_agents=5, signals_connected=2, confidence=58,
                              risk_score=max(46, int(s.get("risk_score", 18)))),
        "correlating": dict(stage="correlating", alert_active=True,
                            active_agents=9, signals_connected=4, confidence=78,
                            risk_score=max(63, int(s.get("risk_score", 18)))),
        "ready_for_decision": dict(stage="ready_for_decision", alert_active=True,
                                   active_agents=12, signals_connected=5, confidence=94,
                                   risk_score=max(78, int(s.get("risk_score", 18)))),
    }
    set_state(**mapping[target])

# ---------- HERO ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow"><span class="live-dot"></span>STAFF-ONLY CONTROL LAYER</div>
  <div class="hero-title">Mission Control</div>
  <div class="hero-copy">
    Launch a synthetic operational event and orchestrate the live booth experience across visitor screens.
    This console controls the story; the visitor screens deliver the cinematic AI experience.
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- SCENARIO SELECTOR ----------
st.markdown('<div class="section-title">1 · Select the live event</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Choose a domain and scenario, or let the system surprise the audience.</div>', unsafe_allow_html=True)

domains = sorted(set(x["domain"] for x in SCENARIOS))
c1, c2 = st.columns([0.34, 0.66])
with c1:
    domain = st.selectbox("Operational domain", ["All"] + domains)
filtered = [x for x in SCENARIOS if domain == "All" or x["domain"] == domain]
labels = {f"{x['domain']} — {x['title']}": x["id"] for x in filtered}
with c2:
    pick = st.selectbox("Scenario", list(labels))

selected_id = labels[pick]
selected = next(x for x in SCENARIOS if x["id"] == selected_id)
chain_html = "".join(f'<span class="pill">{x}</span>' for x in selected.get("chain", []))
metric_html = "".join(f'<span class="pill">{x.replace("_"," ").title()}</span>' for x in selected.get("metrics", []))

left, right = st.columns([0.56, 0.44])
with left:
    st.markdown(f"""
    <div class="scenario-card">
      <div class="card-k">SELECTED MISSION</div>
      <div class="card-title">{selected['title']}</div>
      <div class="card-meta">{selected['domain']} · Synthetic operational event</div>
      <div class="pills">{chain_html}</div>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown(f"""
    <div class="scenario-card">
      <div class="card-k">SIGNALS THE AGENTS WILL CONNECT</div>
      <div class="card-title" style="font-size:1.1rem">Multi-domain investigation</div>
      <div class="pills">{metric_html}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
launch_col, surprise_col, reset_col = st.columns([1.4, 1, 0.8])
with launch_col:
    st.markdown('<div class="launch">', unsafe_allow_html=True)
    if st.button("🔴  LAUNCH LIVE EVENT", type="primary", use_container_width=True):
        new_mission(selected_id)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with surprise_col:
    if st.button("🎲  SURPRISE ME", use_container_width=True):
        new_mission(None)
        st.rerun()
with reset_col:
    if st.button("↻  RESET", use_container_width=True):
        reset()
        st.rerun()

# ---------- LIVE MISSION ----------
s = get_state()
scenario = s["scenario"]
stage = s.get("stage", "idle")

st.write("")
st.markdown('<div class="section-title">2 · Live mission status</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">A human-readable control view — no raw JSON.</div>', unsafe_allow_html=True)

risk = int(s.get("risk_score", 0) or 0)
confidence = int(s.get("confidence", 0) or 0)
agents = s.get("active_agents", 0)
if isinstance(agents, list):
    agents = len(agents)
signals = int(s.get("signals_connected", 0) or 0)

st.markdown(f"""
<div class="stat-grid">
  <div class="stat"><div class="stat-v">#{s.get('mission_id',1):02d}</div><div class="stat-l">Mission</div></div>
  <div class="stat"><div class="stat-v">{stage_names.get(stage, stage.upper())}</div><div class="stat-l">Current Stage</div></div>
  <div class="stat"><div class="stat-v {risk_class(risk)}">{risk}</div><div class="stat-l">Risk Score</div></div>
  <div class="stat"><div class="stat-v">{confidence}%</div><div class="stat-l">AI Confidence</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="event-strip">
  <div class="event-k">{scenario.get('severity','EMERGING')} · {scenario.get('facility','Synthetic Facility')}</div>
  <div class="event-t">{scenario.get('title','Monitoring')}</div>
</div>
""", unsafe_allow_html=True)

# Timeline logic
normalized = stage
if stage in ("simulation", "escalated", "complete"):
    normalized = "ready_for_decision"
idx = stage_order.index(normalized) if normalized in stage_order else 0

steps = [
    ("SIGNAL", 1),
    ("AGENTS", 2),
    ("CORRELATION", 3),
    ("AI INSIGHT", 4),
    ("HUMAN DECISION", 5),
]
html_steps = []
for label, pos in steps:
    cls = "step"
    if idx + 1 > pos:
        cls += " done"
    elif idx + 1 == pos:
        cls += " active"
    html_steps.append(f'<div class="{cls}">{label}</div>')
st.markdown('<div class="timeline">' + "".join(html_steps) + '</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
  <div class="stat"><div class="stat-v">{agents}</div><div class="stat-l">Specialized Agents Active</div></div>
  <div class="stat"><div class="stat-v">{signals}</div><div class="stat-l">Operational Signals Connected</div></div>
</div>
""", unsafe_allow_html=True)

# ---------- STORY CHOREOGRAPHY ----------
st.write("")
st.markdown('<div class="section-title">3 · Control the story</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Use these controls during the booth demo to move every connected screen through the same mission.</div>', unsafe_allow_html=True)

a, b, c, d = st.columns(4)
if a.button("⚠️  Signal Detected", use_container_width=True):
    advance_to("alert")
    speak(scenario.get("opening_text", "Attention. A new operational signal has been detected."))
    st.rerun()
if b.button("⚡  Activate Agents", use_container_width=True):
    advance_to("investigating")
    speak(scenario.get("investigation_text", "I am investigating the connected operational signals."))
    st.rerun()
if c.button("🧠  Connect Signals", use_container_width=True):
    advance_to("correlating")
    speak("I am connecting signals across operational domains.")
    st.rerun()
if d.button("✨  Reveal AI Insight", use_container_width=True):
    advance_to("ready_for_decision")
    speak(scenario.get("insight_text", "The connected pattern is now clear. Human review is recommended."))
    st.rerun()

# ---------- VOICE ----------
st.write("")
st.markdown('<div class="section-title">4 · Agent voice</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Send a short spoken line to the public Attention screen.</div>', unsafe_allow_html=True)

custom = st.text_input(
    "Voice message",
    placeholder="Example: Excuse me. I found something you may want to see."
)
vc1, vc2 = st.columns([1.4, 1])
with vc1:
    if st.button("🎙️  SPEAK TO THE BOOTH", use_container_width=True) and custom.strip():
        speak(custom.strip())
        st.rerun()
with vc2:
    if st.button("🔔  SPEAK CURRENT ALERT", use_container_width=True):
        speak(scenario.get("opening_text", "Attention. A new signal requires review."))
        st.rerun()

st.markdown("""
<div class="small-note">
Synthetic demonstration only · Operator controls are staff-only · AI recommends and explains · Humans decide
</div>
""", unsafe_allow_html=True)
