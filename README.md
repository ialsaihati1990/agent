# NHCC Agentic AI — Living Command Center V2

A multi-screen Streamlit exhibition prototype with:
- 24 synthetic operational scenarios
- scenario-specific synthetic time-series data
- surprise mode
- audible alert
- proactive voice agent
- popup interaction
- scenario chaining
- timed multi-agent investigation choreography
- human-in-the-loop decision screen
- response simulation
- optional Supabase synchronization across separate Streamlit deployments
- hidden operator console

## Screens
- `screen_1_wall.py` — live operational wall
- `screen_2_touch.py` — visitor mission control / touch screen
- `screen_3_brain.py` — multi-agent brain
- `screen_4_decision.py` — human decision / simulation
- `screen_5_attention.py` — voice + alert attraction screen
- `screen_6_operator.py` — staff-only scenario trigger console

## Run locally
Open six terminals, or use six displays on one workstation:

```bash
streamlit run screen_1_wall.py --server.port 8501
streamlit run screen_2_touch.py --server.port 8502
streamlit run screen_3_brain.py --server.port 8503
streamlit run screen_4_decision.py --server.port 8504
streamlit run screen_5_attention.py --server.port 8505
streamlit run screen_6_operator.py --server.port 8506
```

All local apps share `booth_state.db`.

## Deploy as separate Streamlit apps
Use Supabase because separate cloud apps do not share a local SQLite file.

1. Create a Supabase project.
2. Run `supabase_schema.sql`.
3. Set `SUPABASE_URL` and `SUPABASE_KEY` as environment variables for every app.
4. Deploy each screen as a separate Streamlit app from the same repository.
5. Open each URL on the corresponding booth display.

## Browser audio note
Modern browsers may block autoplay audio until that browser tab has received a user interaction. For a real booth, click once on the dedicated attention/voice display after launch, or configure the kiosk browser to permit autoplay. After that, alerts and speech can play automatically.

## Safety / demo integrity
All facilities, values, alerts, predicted impacts and recommendations are synthetic demonstration content. The experience does not execute operational actions.


## V3 — Conversational Supervisor Agent
New screen:
- `screen_7_conversation.py` — visitor chat interface connected to an OpenAI-powered Supervisor Agent.

The agent can call booth tools:
- read current live synthetic signals
- investigate the current alert
- request deeper cross-domain analysis
- run a synthetic response simulation
- prepare escalation for human review
- list and trigger demo scenarios

### Configure OpenAI
Add to Streamlit secrets:

```toml
OPENAI_API_KEY="..."
OPENAI_MODEL="gpt-5.1"
```

Do not commit the real API key to GitHub.

### Run conversational screen locally
```bash
streamlit run screen_7_conversation.py --server.port 8507
```

### Voice
V3 sends each conversational answer to the shared booth voice state so the dedicated Attention screen can speak it. The visitor can type or tap suggested questions. For production-grade real-time microphone conversation, the next step is a Realtime voice frontend rather than relying only on Streamlit chat.
