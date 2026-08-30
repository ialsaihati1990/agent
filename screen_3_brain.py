import time, streamlit as st
from shared import get_state,set_state,speak
from ui import page,refresh,metric

page("AGENTIC AI BRAIN")
refresh(850,"brain")
s=get_state(); sc=s["scenario"]; elapsed=time.time()-float(s.get("stage_started_at",time.time()))

# timed choreography
if s["stage"]=="investigating" and elapsed>3.0:
    set_state(stage="correlating",active_agents=16,signals_connected=4,confidence=68,risk_score=66)
    speak("I found related signals. I’m connecting them now."); st.rerun()
elif s["stage"]=="correlating" and elapsed>4.0:
    set_state(stage="synthesizing",active_agents=24,signals_connected=max(5,len(sc["chain"])+2),confidence=84,risk_score=79)
    speak(sc["insight_text"]); st.rerun()
elif s["stage"]=="synthesizing" and elapsed>4.5:
    if sc["id"]=="false_alarm":
        set_state(stage="ready_for_decision",active_agents=18,signals_connected=3,confidence=88,risk_score=24)
    else:
        set_state(stage="ready_for_decision",active_agents=28,signals_connected=max(6,len(sc["chain"])+3),confidence=94,risk_score=88)
    speak(sc["impact_text"]); st.rerun()

st.markdown("""<div class="glass" style="text-align:center;padding:32px">
<div class="k">MULTI-AGENT ORCHESTRATION</div>
<div style="font-size:2.3rem;font-weight:950;margin-top:8px">Observe • Connect • Reason • Prioritize</div>
<div class="m" style="margin-top:8px">A scalable ecosystem of specialized agents working in parallel.</div></div>""",unsafe_allow_html=True)
st.write("")
a,b,c=st.columns(3)
with a: metric("AGENTS ACTIVE",s["active_agents"],"#54d8cc")
with b: metric("SIGNALS CONNECTED",s["signals_connected"],"#7ed8f6")
with c: metric("CONFIDENCE",f'{s["confidence"]}%',"#64a70b" if s["confidence"]>=85 else "#ffb020")
st.write("")

chain=sc.get("chain",[])
cols=st.columns(len(chain) if chain else 1)
for i,x in enumerate(chain):
    with cols[i]:
        st.markdown(f'<div class="glass" style="text-align:center;min-height:115px"><div class="m">STEP {i+1}</div><div style="font-size:1.2rem;font-weight:900;margin-top:8px">{x}</div></div>',unsafe_allow_html=True)

st.write("")
if s["stage"] in ["correlating","synthesizing","ready_for_decision","deep_analysis","simulation","decision_made"]:
    st.markdown(f"""<div class="alert"><div class="k">CONNECTED PATTERN</div>
    <div style="font-size:1.85rem;font-weight:950;margin-top:7px">{sc['insight_text']}</div>
    <div class="m" style="margin-top:8px">{sc['impact_text']}</div></div>""",unsafe_allow_html=True)
else:
    st.markdown('<div class="glass"><div class="m">Waiting for Mission Control to investigate the signal…</div></div>',unsafe_allow_html=True)
