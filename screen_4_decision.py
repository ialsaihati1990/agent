import streamlit as st
from shared import get_state,set_state,speak,new_mission
from ui import page,refresh,metric,chart_html

page("HUMAN DECISION")
refresh(900,"decision")
s=get_state(); sc=s["scenario"]

if s["stage"] not in ["ready_for_decision","deep_analysis","simulation","decision_made"]:
    st.markdown("""<div class="glass" style="text-align:center;padding:65px">
    <div class="k">HUMAN-IN-THE-LOOP</div><div style="font-size:2.3rem;font-weight:950;margin-top:8px">Waiting for decision intelligence</div>
    <div class="m" style="margin-top:8px">No operational action is executed automatically.</div></div>""",unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="glass"><div class="k">AI ANALYSIS COMPLETE</div>
    <div style="font-size:2.45rem;font-weight:950;margin-top:8px">The decision is yours.</div>
    <div class="m" style="margin-top:8px">{sc['impact_text']}</div></div>""",unsafe_allow_html=True)
    st.write("")
    a,b,c=st.columns(3)
    with a: metric("RISK SCORE",s["risk_score"],"#ff6675" if s["risk_score"]>70 else "#ffb020")
    with b: metric("CONFIDENCE",f'{s["confidence"]}%',"#64a70b")
    with c: metric("DOMAIN",sc["domain"],"#7ed8f6")
    st.write("")
    st.markdown(f"""<div class="glass">
    <div class="m">WHAT CHANGED?</div><div style="font-size:1.3rem;font-weight:900;margin-top:5px">{sc['opening_text']}</div>
    <hr style="border-color:rgba(255,255,255,.09)"><div class="m">CONNECTED INSIGHT</div><div style="margin-top:5px">{sc['insight_text']}</div>
    <hr style="border-color:rgba(255,255,255,.09)"><div class="m">WHY IT MATTERS</div><div style="margin-top:5px">{sc['impact_text']}</div>
    </div>""",unsafe_allow_html=True)
    st.write("")
    a,b,c=st.columns(3)
    if a.button("🔎 DEEPER ANALYSIS",use_container_width=True):
        set_state(stage="deep_analysis",active_agents=36,signals_connected=10,confidence=98,risk_score=min(96,s["risk_score"]+5))
        speak("Deeper analysis complete. I found additional supporting signals."); st.rerun()
    if b.button("🧪 SIMULATE RESPONSE",type="primary",use_container_width=True):
        set_state(stage="simulation",simulation="recommended_response",decision="simulate")
        speak("Simulation ready. Compare the current trajectory with the proposed response."); st.rerun()
    if c.button("⬆️ ESCALATE FOR REVIEW",use_container_width=True):
        set_state(stage="decision_made",decision="human_review")
        speak("Escalation prepared for human review. No operational action has been executed."); st.rerun()

    if s["stage"]=="simulation":
        st.write("")
        m=sc["metrics"][0]; d=sc["data"][m]
        vals=d["values"]; start=vals[-1]
        improved=[round(start-(start-vals[0])*(i/7)*.55,1) for i in range(8)]
        st.markdown(f"""<div class="glass"><div class="k">SYNTHETIC RESPONSE SIMULATION</div>
        <div style="font-size:1.35rem;font-weight:900;margin-top:8px">{m.replace('_',' ').title()}</div>
        <div class="m">Current end-state: {vals[-1]} {d['unit']} • Simulated direction: {improved[-1]} {d['unit']}</div></div>""",unsafe_allow_html=True)
        st.markdown(chart_html("simulated_response",improved,d["unit"]),unsafe_allow_html=True)
