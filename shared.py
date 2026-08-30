from __future__ import annotations
import config  # loads Streamlit secrets into environment
import json, os, sqlite3, time
from pathlib import Path
from typing import Any, Dict
from scenario_engine import generate_scenario

ROOT=Path(__file__).parent
DB_PATH=ROOT/"booth_state.db"

def default_state():
    sc=generate_scenario("patient_surge", seed=7)
    return {
        "mission_id":1,
        "stage":"idle",
        "alert_active":False,
        "scenario":sc,
        "active_agents":0,
        "signals_connected":0,
        "confidence":0,
        "risk_score":18,
        "decision":"",
        "simulation":"",
        "voice_seq":0,
        "voice_text":"",
        "event_seq":0,
        "stage_started_at":time.time(),
        "updated_at":time.time(),
    }

def _sb():
    url=os.getenv("SUPABASE_URL")
    key=os.getenv("SUPABASE_KEY")
    if not url or not key: return None
    try:
        from supabase import create_client
        return create_client(url,key)
    except Exception: return None

def _ensure():
    conn=sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS booth_state(id INTEGER PRIMARY KEY CHECK(id=1),payload TEXT NOT NULL)")
    if not conn.execute("SELECT 1 FROM booth_state WHERE id=1").fetchone():
        conn.execute("INSERT INTO booth_state VALUES(1,?)",(json.dumps(default_state()),)); conn.commit()
    return conn

def get_state()->Dict[str,Any]:
    sb=_sb()
    if sb:
        try:
            d=sb.table("booth_state").select("payload").eq("id",1).single().execute().data
            if d and d.get("payload"): return d["payload"]
        except Exception: pass
    conn=_ensure(); row=conn.execute("SELECT payload FROM booth_state WHERE id=1").fetchone(); conn.close()
    return json.loads(row[0])

def set_state(**updates):
    s=get_state(); old_stage=s.get("stage")
    s.update(updates)
    if "stage" in updates and updates["stage"]!=old_stage: s["stage_started_at"]=time.time()
    s["event_seq"]=int(s.get("event_seq",0))+1; s["updated_at"]=time.time()
    sb=_sb()
    if sb:
        try:
            sb.table("booth_state").upsert({"id":1,"payload":s}).execute()
            return s
        except Exception: pass
    conn=_ensure(); conn.execute("UPDATE booth_state SET payload=? WHERE id=1",(json.dumps(s),)); conn.commit(); conn.close()
    return s

def speak(text):
    s=get_state()
    return set_state(voice_text=text, voice_seq=int(s.get("voice_seq",0))+1)

def new_mission(scenario_id=None):
    current=get_state()
    sc=generate_scenario(scenario_id)
    s=default_state()
    s.update({
        "mission_id":int(current.get("mission_id",0))+1,
        "scenario":sc,
        "stage":"alert",
        "alert_active":True,
        "risk_score":32,
        "signals_connected":1,
        "confidence":31,
        "voice_seq":int(current.get("voice_seq",0))+1,
        "voice_text":sc["opening_text"],
        "event_seq":int(current.get("event_seq",0))+1,
        "stage_started_at":time.time(),
        "updated_at":time.time(),
    })
    sb=_sb()
    if sb:
        try:
            sb.table("booth_state").upsert({"id":1,"payload":s}).execute(); return s
        except Exception: pass
    conn=_ensure(); conn.execute("UPDATE booth_state SET payload=? WHERE id=1",(json.dumps(s),)); conn.commit(); conn.close()
    return s

def reset():
    cur=get_state(); s=default_state()
    s["mission_id"]=int(cur.get("mission_id",0))+1
    s["voice_seq"]=int(cur.get("voice_seq",0))+1
    s["voice_text"]="Monitoring operational signals."
    s["event_seq"]=int(cur.get("event_seq",0))+1
    sb=_sb()
    if sb:
        try:
            sb.table("booth_state").upsert({"id":1,"payload":s}).execute(); return s
        except Exception: pass
    conn=_ensure(); conn.execute("UPDATE booth_state SET payload=? WHERE id=1",(json.dumps(s),)); conn.commit(); conn.close()
    return s
