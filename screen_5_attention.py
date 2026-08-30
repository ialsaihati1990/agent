import streamlit as st
from shared import get_state
from ui import page,refresh,alarm_once,speak_once

page("NHCC INTELLIGENCE AGENT")
refresh(700,"attention")
s=get_state(); sc=s["scenario"]

# Audio should play here as the dedicated attraction screen.
if s["alert_active"]:
    alarm_once(s["event_seq"])
    speak_once(s["voice_seq"],s["voice_text"])

if not s["alert_active"]:
    st.markdown("""<div class="glass" style="text-align:center;padding:95px 30px">
    <div class="k">NHCC INTELLIGENCE AGENT • LISTENING</div>
    <div style="font-size:3.4rem;font-weight:950;margin-top:12px">I’m watching the signals.</div>
    <div class="m" style="font-size:1.25rem;margin-top:12px">If something unusual happens, I’ll tell you.</div>
    <div style="margin-top:28px;color:#54d8cc;font-weight:800">● Monitoring</div></div>""",unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="alert" style="text-align:center;padding:62px 34px">
    <div style="font-size:2.5rem">🔔</div><div class="k" style="color:#ff9aa4">I FOUND SOMETHING</div>
    <div style="font-size:3.1rem;font-weight:950;margin-top:10px">{sc['title']}</div>
    <div class="m" style="font-size:1.3rem;margin-top:14px">{s['voice_text']}</div>
    <div style="margin-top:28px;font-size:1.15rem;font-weight:900">Look at Mission Control → INVESTIGATE</div>
    </div>""",unsafe_allow_html=True)
