from __future__ import annotations
import config  # loads Streamlit secrets into environment
import json, os
from typing import Any, Dict, List
from openai import OpenAI
from agent_tools import (
    get_live_state, investigate_current_alert, request_deeper_analysis,
    run_response_simulation, escalate_for_human_review, trigger_scenario, list_scenarios
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.1")

SYSTEM = """
You are the NHCC Intelligence Agent for an exhibition demonstration of an Agentic AI command-center experience.
You are speaking to visitors in a live booth. Be concise, confident, engaging, and operationally clear.

Important rules:
- All displayed data are synthetic demonstration data.
- Never claim the data are real Ministry of Health data.
- Never diagnose patients or present a clinical diagnosis.
- Never execute real operational actions.
- You may investigate, correlate, simulate, and prepare escalation for human review.
- Human decision remains final.
- Prefer short spoken answers: normally 2-5 sentences.
- If the visitor asks what is happening now, call get_live_state.
- If the visitor asks to investigate, call investigate_current_alert.
- If the visitor asks for more detail/root cause, call request_deeper_analysis.
- If the visitor asks "what if", "simulate", or "what happens if we act", call run_response_simulation.
- If they ask to escalate, call escalate_for_human_review.
- If they ask to demonstrate a scenario, call list_scenarios first if needed, then trigger_scenario.
- Explain relationships between signals, not just single KPIs.
- If the current scenario is a false alarm / validation case, explicitly say no escalation is currently required.
"""

TOOLS = [
    {
        "type":"function",
        "name":"get_live_state",
        "description":"Read the current synthetic booth state and latest operational signals.",
        "parameters":{"type":"object","properties":{},"additionalProperties":False},
        "strict":True,
    },
    {
        "type":"function",
        "name":"investigate_current_alert",
        "description":"Start a multi-agent investigation of the current alert.",
        "parameters":{"type":"object","properties":{},"additionalProperties":False},
        "strict":True,
    },
    {
        "type":"function",
        "name":"request_deeper_analysis",
        "description":"Expand analysis across additional connected operational domains.",
        "parameters":{"type":"object","properties":{},"additionalProperties":False},
        "strict":True,
    },
    {
        "type":"function",
        "name":"run_response_simulation",
        "description":"Run a synthetic response simulation for the current scenario.",
        "parameters":{"type":"object","properties":{},"additionalProperties":False},
        "strict":True,
    },
    {
        "type":"function",
        "name":"escalate_for_human_review",
        "description":"Prepare the current case for human review without executing any real action.",
        "parameters":{"type":"object","properties":{},"additionalProperties":False},
        "strict":True,
    },
    {
        "type":"function",
        "name":"list_scenarios",
        "description":"List available synthetic demonstration scenarios.",
        "parameters":{"type":"object","properties":{},"additionalProperties":False},
        "strict":True,
    },
    {
        "type":"function",
        "name":"trigger_scenario",
        "description":"Trigger one synthetic demonstration scenario by its scenario_id.",
        "parameters":{
            "type":"object",
            "properties":{"scenario_id":{"type":"string"}},
            "required":["scenario_id"],
            "additionalProperties":False
        },
        "strict":True,
    },
]

FUNCTIONS = {
    "get_live_state": lambda **_: get_live_state(),
    "investigate_current_alert": lambda **_: investigate_current_alert(),
    "request_deeper_analysis": lambda **_: request_deeper_analysis(),
    "run_response_simulation": lambda **_: run_response_simulation(),
    "escalate_for_human_review": lambda **_: escalate_for_human_review(),
    "list_scenarios": lambda **_: list_scenarios(),
    "trigger_scenario": lambda scenario_id, **_: trigger_scenario(scenario_id),
}

def _client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    return OpenAI(api_key=key)

def ask_agent(user_text: str, previous_response_id: str | None = None) -> Dict[str,Any]:
    client = _client()
    kwargs = {
        "model": MODEL,
        "instructions": SYSTEM,
        "input": user_text,
        "tools": TOOLS,
        "parallel_tool_calls": True,
    }
    if previous_response_id:
        kwargs["previous_response_id"] = previous_response_id

    response = client.responses.create(**kwargs)

    # Resolve function calls until the model returns a natural-language answer.
    for _ in range(6):
        calls = [item for item in response.output if getattr(item, "type", None) == "function_call"]
        if not calls:
            return {"text": response.output_text, "response_id": response.id}

        tool_outputs = []
        for call in calls:
            args = json.loads(call.arguments or "{}")
            result = FUNCTIONS[call.name](**args)
            tool_outputs.append({
                "type":"function_call_output",
                "call_id":call.call_id,
                "output":json.dumps(result),
            })

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS,
            parallel_tool_calls=True,
        )

    return {"text":"I completed the analysis, but the demonstration reached its tool-call limit.","response_id":response.id}
