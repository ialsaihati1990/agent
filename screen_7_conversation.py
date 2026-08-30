import streamlit as st
from shared import get_state, speak
from supervisor_agent import ask_agent
from ui import page, refresh

page("TALK TO THE COMMAND CENTER")
refresh(1500, "conversation")
s = get_state()
sc = s["scenario"]

st.markdown("""
<div class="glass" style="text-align:center;padding:36px 24px">
  <div class="k">CONVERSATIONAL AGENTIC AI</div>
  <div style="font-size:2.6rem;font-weight:950;margin-top:8px">Ask me what is happening.</div>
  <div class="m" style="font-size:1.05rem;margin-top:10px">
    I can investigate, connect signals, simulate a response, or prepare a case for human review.
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")
suggestions = [
    "What needs attention right now?",
    "Why is this happening?",
    "Investigate this alert.",
    "Go deeper and connect the signals.",
    "Simulate what could happen next.",
    "Show me an equipment maintenance scenario.",
]

st.markdown("#### Try asking")
cols = st.columns(3)
for i, q in enumerate(suggestions):
    if cols[i%3].button(q, use_container_width=True):
        st.session_state["quick_question"] = q

if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

typed = st.chat_input("Ask the NHCC Intelligence Agent…")
user_text = typed or st.session_state.pop("quick_question", None)

if user_text:
    st.session_state.messages.append({"role":"user","content":user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Connecting operational signals…"):
            try:
                ans = ask_agent(user_text, st.session_state.previous_response_id)
                text = ans["text"] or "Analysis complete."
                st.session_state.previous_response_id = ans["response_id"]
                st.markdown(text)
                speak(text)
                st.session_state.messages.append({"role":"assistant","content":text})
            except Exception as e:
                st.error("The conversational agent is not configured yet. Add OPENAI_API_KEY to the deployment secrets.")
                st.caption(str(e))

st.write("")
st.caption("Synthetic demonstration only • AI recommends and explains • Humans decide")
