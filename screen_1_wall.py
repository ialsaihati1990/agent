import streamlit as st
from shared import get_state
from ui import page, refresh, alarm_once, speak_once, metric, chart_html

page("LIVE HEALTH SYSTEM")
refresh(850,"wall")
s=get_state(); sc=s["scenario"]

if s["alert_active"]:
    alarm_once(s["event_seq"])
    speak_once(s["voice_seq"],s["voice_text"])

st.markdown('<div class="scan"></div>',unsafe_allow_html=True)
l,r=st.columns([1.45,1])
with l:
    st.markdown(f"""
<div class="glass" style="min-height:500px;position:relative;overflow:hidden">
 <div class="k">OPERATIONAL NETWORK • {sc['region'].upper()}</div>
 <div style="position:absolute;inset:80px 55px 38px;border-radius:34px;border:1px solid rgba(126,216,246,.11);
 background:radial-gradient(circle at 54% 48%,rgba(255,77,94,.22),transparent 11%),radial-gradient(circle at 30% 62%,rgba(0,163,224,.14),transparent 10%),radial-gradient(circle at 75% 70%,rgba(0,209,193,.12),transparent 11%)"></div>
 <div style="position:absolute;left:51%;top:47%;transform:translate(-50%,-50%);text-align:center"><span class="pulse"></span><div style="font-size:1.25rem;font-weight:950">{sc['facility']}</div><div class="m">{sc['title']}</div></div>
 <div style="position:absolute;left:21%;top:64%;color:#7ed8f6">● Facility 03</div>
 <div style="position:absolute;right:17%;bottom:19%;color:#54d8cc">● Facility 10</div>
 <div style="position:absolute;left:17%;top:28%;color:#7ed8f6">● Facility 01</div>
</div>""",unsafe_allow_html=True)

with r:
    if s["alert_active"]:
        st.markdown(f"""<div class="alert"><div class="k" style="color:#ff9aa4">🔔 {sc['severity']} SIGNAL</div>
        <div style="font-size:2rem;font-weight:950;margin-top:7px">{sc['title']}</div>
        <div class="m" style="margin-top:10px">{sc['opening_text']}</div></div>""",unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass"><div class="k">SYSTEM STATUS</div><div style="font-size:1.8rem;font-weight:950;color:#54d8cc;margin-top:8px">Monitoring Live Signals</div><div class="m" style="margin-top:8px">Waiting for an emerging pattern…</div></div>',unsafe_allow_html=True)
    st.write("")
    a,b=st.columns(2)
    with a: metric("RISK SCORE",s["risk_score"],"#ffb020" if s["risk_score"]<75 else "#ff6675")
    with b: metric("CONNECTED SIGNALS",s["signals_connected"])

# show first metric trend
m=sc["metrics"][0]; d=sc["data"][m]
st.markdown(chart_html(m,d["values"],d["unit"]),unsafe_allow_html=True)
st.caption("All facilities, values, alerts and recommendations are synthetically generated for demonstration.")
