import streamlit as st
from shared import get_state, speak
from supervisor_agent import ask_agent
from ui import page, refresh

page("TALK TO THE COMMAND CENTER")
refresh(1500, "conversation")

# Fix quick-action button contrast on dark theme
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(135deg, #0b2a44, #123f61) !important;
    color: #ffffff !important;
    border: 1px solid rgba(126,216,246,.38) !important;
    min-height: 68px !important;
    border-radius: 18px !important;
    font-size: 1rem !important;
    font-weight: 850 !important;
    text-align: left !important;
    padding: 0 18px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.18) !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #123f61, #0b5670) !important;
    border-color: #7ed8f6 !important;
}
div.stButton > button p {
    color: #ffffff !important;
}
[data-testid="stChatInput"] {
    border: 1px solid rgba(126,216,246,.35) !important;
    border-radius: 18px !important;
}
</style>
""", unsafe_allow_html=True)

s = get_state()

st.markdown("""
<div class="glass" style="text-align:center;padding:36px 24px">
  <div class="k">CONVERSATIONAL AGENTIC AI</div>
  <div style="font-size:2.6rem;font-weight:950;margin-top:8px">Ask me what is happening.</div>
  <div class="m" style="font-size:1.05rem;margin-top:10px">
    I can investigate, connect signals, simulate a response, or prepare a case for human review.
  </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

@st.dialog("NHCC Intelligence Agent", width="large")
def action_popup(question: str):
    st.markdown(f"### {question}")
    st.write("I’ll connect the current synthetic signals and update the command-center experience.")
    c1, c2 = st.columns(2)
    if c1.button("⚡ Run Analysis", type="primary", use_container_width=True, key="popup_run"):
        st.session_state.pending_question = question
        st.rerun()
    if c2.button("Cancel", use_container_width=True, key="popup_cancel"):
        st.rerun()

st.write("")
st.markdown("#### Try asking")

suggestions = [
    ("⚠️", "What needs attention right now?"),
    ("🔍", "Why is this happening?"),
    ("⚡", "Investigate this alert."),
    ("🧠", "Go deeper and connect the signals."),
    ("🧪", "Simulate what could happen next."),
    ("🛠️", "Show me an equipment maintenance scenario."),
]

cols = st.columns(3)
for i, (icon, q) in enumerate(suggestions):
    if cols[i % 3].button(f"{icon}  {q}", use_container_width=True, key=f"quick_{i}"):
        action_popup(q)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

typed = st.chat_input("Ask the NHCC Intelligence Agent…")
user_text = typed or st.session_state.pop("pending_question", None)

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
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
                st.session_state.messages.append({"role": "assistant", "content": text})
            except Exception as e:
                st.error("The conversational agent is not configured yet. Add OPENAI_API_KEY to the deployment secrets.")
                st.caption(str(e))

st.write("")
st.caption("Synthetic demonstration only • AI recommends and explains • Humans decide")
