from pathlib import Path
import base64, html, json
import streamlit as st

def page(title, kicker="NATIONAL HEALTH COMMAND CENTER"):
    st.set_page_config(page_title=title,page_icon="⚡",layout="wide",initial_sidebar_state="collapsed")
    st.markdown(f"""
<style>
#MainMenu,footer,header{{visibility:hidden}}
.stApp{{background:radial-gradient(circle at 82% 8%,rgba(0,163,224,.14),transparent 25%),radial-gradient(circle at 10% 85%,rgba(0,209,193,.09),transparent 28%),linear-gradient(155deg,#04101d,#071526 56%,#0a1e31);color:#fff}}
.block-container{{padding-top:.75rem;padding-bottom:1rem;max-width:1700px}}
*{{font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}}
.top{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,.11);padding:8px 2px 14px}}
.k{{font-size:.75rem;letter-spacing:.18em;color:#78d6f6;font-weight:800}}
.t{{font-size:1.65rem;font-weight:950}}
.m{{color:#9bb2c7}}
.glass{{background:rgba(9,31,51,.76);border:1px solid rgba(126,216,246,.16);border-radius:24px;padding:22px;box-shadow:0 18px 50px rgba(0,0,0,.22)}}
.metric{{font-size:2.25rem;font-weight:950}}
.alert{{background:rgba(255,77,94,.08);border:1px solid rgba(255,77,94,.46);border-radius:24px;padding:24px}}
.pulse{{display:inline-block;width:14px;height:14px;border-radius:50%;background:#ff4d5e;animation:p 1.2s infinite}}
@keyframes p{{0%{{box-shadow:0 0 0 0 rgba(255,77,94,.55)}}70%{{box-shadow:0 0 0 20px rgba(255,77,94,0)}}100%{{box-shadow:0 0 0 0 rgba(255,77,94,0)}}}}
.scan{{height:2px;background:linear-gradient(90deg,transparent,#00a3e0,transparent);animation:s 2.8s linear infinite}}
@keyframes s{{from{{transform:translateX(-55%)}}to{{transform:translateX(55%)}}}}
div.stButton>button{{min-height:56px;border-radius:16px;font-weight:850;border:1px solid rgba(126,216,246,.25)}}
[data-testid=stDialog] div[role=dialog]{{border-radius:26px!important;background:#071526!important;color:white!important}}
</style>
<div class="top"><div><div class="k">{kicker}</div><div class="t">{title}</div></div><div style="text-align:right"><div class="k">LIVE COMMAND EXPERIENCE</div><div class="m">Agentic AI • Synthetic Demo</div></div></div>
""",unsafe_allow_html=True)

def refresh(ms,key):
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=ms,key=key)
    except Exception: pass

def metric(label,value,tone="#7ed8f6"):
    st.markdown(f'<div class="glass"><div class="m">{label}</div><div class="metric" style="color:{tone}">{value}</div></div>',unsafe_allow_html=True)

def alarm_once(seq):
    k=f"alarm_{seq}"
    if st.session_state.get(k): return
    st.session_state[k]=True
    p=Path(__file__).parent/"assets"/"alert.wav"
    if p.exists():
        b64=base64.b64encode(p.read_bytes()).decode()
        st.components.v1.html(f'<audio autoplay><source src="data:audio/wav;base64,{b64}" type="audio/wav"></audio>',height=0)

def speak_once(seq,text):
    k=f"voice_{seq}"
    if st.session_state.get(k) or not text: return
    st.session_state[k]=True
    safe=json.dumps(text)
    st.components.v1.html(f"""
<script>
(function(){{
  const text={safe};
  function say(){{
    if(!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(text);
    u.rate=0.92; u.pitch=0.92; u.volume=1.0;
    const voices=window.speechSynthesis.getVoices();
    const preferred=voices.find(v=>/en[-_](US|GB)/i.test(v.lang)) || voices[0];
    if(preferred) u.voice=preferred;
    window.speechSynthesis.speak(u);
  }}
  setTimeout(say,280);
}})();
</script>""",height=0)

def chart_html(metric_name, values, unit):
    # lightweight SVG sparkline
    if not values: return ""
    lo=min(values); hi=max(values); span=max(hi-lo,1e-9)
    pts=[]
    for i,v in enumerate(values):
        x=20+i*(560/(len(values)-1))
        y=150-((v-lo)/span)*110
        pts.append(f"{x:.1f},{y:.1f}")
    return f"""
<div class="glass">
<div class="m">{metric_name.replace('_',' ').upper()} • {unit}</div>
<svg viewBox="0 0 600 180" style="width:100%;height:auto;margin-top:10px">
<polyline points="{' '.join(pts)}" fill="none" stroke="#7ed8f6" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="20" y1="150" x2="580" y2="150" stroke="rgba(255,255,255,.12)"/>
<text x="20" y="174" fill="#9bb2c7" font-size="14">{values[0]}</text>
<text x="540" y="174" fill="#fff" font-size="14">{values[-1]}</text>
</svg></div>"""
