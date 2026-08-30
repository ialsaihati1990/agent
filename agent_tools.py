from __future__ import annotations
from typing import Dict, Any, List
from shared import get_state, set_state, speak, new_mission
from scenario_catalog import SCENARIOS

def get_live_state() -> Dict[str, Any]:
    s = get_state()
    sc = s["scenario"]
    return {
        "mission_id": s["mission_id"],
        "stage": s["stage"],
        "facility": sc["facility"],
        "region": sc["region"],
        "domain": sc["domain"],
        "scenario_id": sc["id"],
        "scenario_title": sc["title"],
        "risk_score": s["risk_score"],
        "confidence": s["confidence"],
        "signals_connected": s["signals_connected"],
        "active_agents": s["active_agents"],
        "metrics": {
            k: {"latest": v["values"][-1], "unit": v["unit"]}
            for k, v in sc["data"].items()
        },
        "insight": sc["insight_text"],
        "impact": sc["impact_text"],
        "decision": s["decision"],
    }

def investigate_current_alert() -> Dict[str, Any]:
    s = get_state()
    sc = s["scenario"]
    set_state(stage="investigating", active_agents=8, signals_connected=2, confidence=47, risk_score=max(49, s["risk_score"]))
    speak(sc["investigation_text"])
    return {"status":"started", "message":sc["investigation_text"]}

def request_deeper_analysis() -> Dict[str, Any]:
    s = get_state()
    sc = s["scenario"]
    set_state(stage="deep_analysis", active_agents=36, signals_connected=10, confidence=98, risk_score=min(96, max(70, s["risk_score"]+6)))
    text = "Deeper analysis is complete. I found additional supporting signals across connected operational domains."
    speak(text)
    return {"status":"complete","message":text,"insight":sc["insight_text"],"impact":sc["impact_text"]}

def run_response_simulation() -> Dict[str, Any]:
    s = get_state()
    sc = s["scenario"]
    set_state(stage="simulation", simulation="recommended_response", decision="simulate")
    text = "Simulation ready. I am comparing the current trajectory with a synthetic response scenario."
    speak(text)
    return {"status":"ready","message":text,"scenario":sc["title"]}

def escalate_for_human_review() -> Dict[str, Any]:
    set_state(stage="decision_made", decision="human_review")
    text = "Escalation prepared for human review. No operational action has been executed."
    speak(text)
    return {"status":"prepared","message":text}

def trigger_scenario(scenario_id: str) -> Dict[str, Any]:
    valid = {x["id"] for x in SCENARIOS}
    if scenario_id not in valid:
        return {"status":"error","message":"Unknown scenario_id"}
    s = new_mission(scenario_id)
    return {"status":"started","scenario":s["scenario"]["title"],"facility":s["scenario"]["facility"]}

def list_scenarios() -> List[Dict[str,str]]:
    return [{"id":x["id"],"domain":x["domain"],"title":x["title"]} for x in SCENARIOS]
