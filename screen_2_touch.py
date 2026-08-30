import streamlit as st
from scenario_catalog import SCENARIOS
from shared import get_state,new_mission,set_state,speak,reset
from ui import page,refresh

page("MISSION CONTROL")
refresh(1100,"touch")
s=get_state(); sc=s["scenario"]

@st.dialog("🔔 ATTENTION",width="large")
def popup():
    st.markdown(f"## {sc['title']}")
    st.write(sc["opening_text"])
    st.caption("The Command Center has received a new operational signal.")
    a,b=st.columns(2)
    if a.button("⚡ INVESTIGATE NOW",type="primary",use_container_width=True):
        set_state(stage="investigating",active_agents=8,signals_connected=2,confidence=47,risk_score=49)
        speak(sc["investigation_text"]); st.rerun()
    if b.button("Continue Monitoring",use_container_width=True):
        set_state(stage="monitoring"); st.rerun()

st.markdown("""<div class="glass" style="text-align:center;padding:42px 28px">
<div class="k">TOUCH EXPERIENCE</div>
<div style="font-size:2.7rem;font-weight:950;margin-top:8px">Choose a mission — or let the system surprise you.</div>
<div class="m" style="margin-top:10px">Your choice changes every connected booth screen.</div></div>""",unsafe_allow_html=True)
st.write("")

if s["stage"]=="idle":
    options={f"{x['domain']} — {x['title']}":x["id"] for x in SCENARIOS}
    chosen=st.selectbox("Scenario Library",list(options))
    a,b,c=st.columns(3)
    if a.button("🔔 START SELECTED MISSION",type="primary",use_container_width=True):
        new_mission(options[chosen]); st.rerun()
    if b.button("🎲 SURPRISE ME",use_container_width=True):
        new_mission(None); st.rerun()
    if c.button("↻ RESET",use_container_width=True):
        reset(); st.rerun()
else:
    st.markdown(f"""<div class="alert"><span class="pulse"></span>
    <div style="font-size:1.75rem;font-weight:950;margin-top:8px">{sc['title']}</div>
    <div class="m">{sc['opening_text']}</div></div>""",unsafe_allow_html=True)
    st.write("")
    if s["stage"]=="alert":
        popup()
        if st.button("⚡ INVESTIGATE ALERT",type="primary",use_container_width=True):
            set_state(stage="investigating",active_agents=8,signals_connected=2,confidence=47,risk_score=49)
            speak(sc["investigation_text"]); st.rerun()
    elif s["stage"] in ["investigating","correlating","synthesizing"]:
        st.info("Watch the AI Brain. Specialized agents are working in parallel.")
        if st.button("🧠 GO DEEPER",use_container_width=True):
            set_state(stage="deep_analysis",active_agents=32,signals_connected=8,confidence=97,risk_score=91)
            speak("I’m expanding the analysis across additional operational domains."); st.rerun()
    elif s["stage"] in ["ready_for_decision","deep_analysis","simulation","decision_made","monitoring"]:
        st.success("Decision intelligence is ready.")
        a,b=st.columns(2)
        if a.button("🎯 SEND TO HUMAN DECISION",type="primary",use_container_width=True):
            set_state(stage="ready_for_decision"); st.rerun()
        if b.button("🎲 NEXT SURPRISE",use_container_width=True):
            new_mission(None); st.rerun()
