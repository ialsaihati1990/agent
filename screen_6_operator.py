import streamlit as st
from scenario_catalog import SCENARIOS
from shared import get_state,new_mission,reset,speak,set_state
from ui import page,refresh

page("OPERATOR CONSOLE")
refresh(1500,"operator")
s=get_state()
st.caption("Hidden/Staff screen — trigger specific booth moments without touching visitor screens.")

domains=sorted(set(x["domain"] for x in SCENARIOS))
domain=st.selectbox("Domain",["All"]+domains)
filtered=[x for x in SCENARIOS if domain=="All" or x["domain"]==domain]
labels={f"{x['domain']} — {x['title']}":x["id"] for x in filtered}
pick=st.selectbox("Scenario",list(labels))
a,b,c=st.columns(3)
if a.button("🔔 TRIGGER",type="primary",use_container_width=True):
    new_mission(labels[pick]); st.rerun()
if b.button("🎲 RANDOM SURPRISE",use_container_width=True):
    new_mission(None); st.rerun()
if c.button("↻ RESET ALL",use_container_width=True):
    reset(); st.rerun()

st.write("")
st.markdown("### Live state")
st.json({
    "mission_id":s["mission_id"],"stage":s["stage"],"scenario":s["scenario"]["title"],
    "facility":s["scenario"]["facility"],"risk_score":s["risk_score"],
    "active_agents":s["active_agents"],"signals_connected":s["signals_connected"],"confidence":s["confidence"]
})

st.write("")
custom=st.text_input("Make the agent say something")
if st.button("🎙️ SPEAK",use_container_width=True) and custom.strip():
    speak(custom.strip()); st.rerun()
