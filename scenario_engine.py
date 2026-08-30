from __future__ import annotations
import random, time, math
from scenario_catalog import SCENARIOS

FACILITIES = [f"Facility {i:02d}" for i in range(1,13)]
REGIONS = ["Central", "East", "West", "North", "South"]
SEVERITIES = ["EMERGING","OPERATIONAL","PRIORITY"]

def _series(base, end, n=12, noise=0.025, floor=None, ceil=None):
    vals=[]
    for i in range(n):
        f=i/(n-1)
        curved = f*f*(3-2*f)
        v=base+(end-base)*curved
        v += random.gauss(0, max(abs(base),abs(end),1)*noise)
        if floor is not None: v=max(floor,v)
        if ceil is not None: v=min(ceil,v)
        vals.append(round(v,1))
    return vals

METRIC_PROFILES = {
    "arrivals": (92, 148, "patients/h"),
    "ed_wait": (36, 112, "min"),
    "bed_occupancy": (71, 96, "%"),
    "discharge_rate": (31, 17, "patients/h"),
    "los": (4.2, 6.8, "days"),
    "pending_discharge": (8, 27, "patients"),
    "icu_occupancy": (76, 95, "%"),
    "icu_admissions": (7, 13, "patients"),
    "icu_transfers": (9, 4, "patients"),
    "staffing": (96, 78, "%"),
    "ambulance_arrivals": (11, 24, "per hour"),
    "acuity": (2.4, 3.7, "index"),
    "room_temp": (21.5, 28.7, "°C"),
    "hvac_efficiency": (94, 61, "%"),
    "device_load": (62, 94, "%"),
    "maintenance_due": (18, 94, "% threshold"),
    "ups_health": (96, 72, "%"),
    "battery_health": (93, 65, "%"),
    "power_load": (54, 83, "%"),
    "power_events": (0, 4, "events"),
    "latency": (32, 187, "ms"),
    "packet_loss": (0.2, 4.8, "%"),
    "app_response": (0.8, 3.6, "sec"),
    "transaction_load": (55, 91, "%"),
    "water_flow": (61, 102, "index"),
    "water_pressure": (93, 74, "%"),
    "occupancy": (70, 76, "%"),
    "historical_usage": (66, 68, "index"),
    "fuel_level": (67, 23, "%"),
    "fuel_burn": (18, 31, "L/h index"),
    "delivery_eta": (4, 11, "hours"),
    "generator_readiness": (98, 95, "%"),
    "device_utilization": (54, 97, "%"),
    "device_criticality": (70, 96, "score"),
    "downtime_risk": (12, 78, "score"),
    "device_errors": (1, 17, "events"),
    "backup_load": (41, 89, "%"),
    "lab_tat": (48, 126, "min"),
    "analyzer_health": (97, 68, "%"),
    "sample_backlog": (14, 67, "samples"),
    "imaging_requests": (34, 71, "per hour"),
    "imaging_completed": (31, 43, "per hour"),
    "modality_utilization": (67, 96, "%"),
    "backlog": (12, 63, "studies"),
    "workload": (61, 94, "%"),
    "absence_rate": (4, 16, "%"),
    "float_staff": (9, 3, "staff"),
    "stock_level": (78, 24, "%"),
    "consumption_rate": (54, 122, "index"),
    "safety_stock": (45, 45, "%"),
    "dispensing": (63, 119, "index"),
    "days_cover": (12, 3, "days"),
    "failed_transactions": (1, 19, "%"),
    "user_load": (49, 83, "%"),
    "service_dependencies": (3, 8, "services"),
    "integration_latency": (3, 47, "min"),
    "message_backlog": (4, 93, "messages index"),
    "source_health": (99, 96, "%"),
    "data_freshness": (98, 72, "%"),
    "infection_signal": (1.0, 2.8, "index"),
    "baseline": (1.0, 1.0, "index"),
    "affected_area": (1, 4, "areas"),
    "device_days": (58, 74, "index"),
    "hygiene_compliance": (88, 72, "%"),
    "observations": (72, 79, "count"),
    "shift_variance": (4, 17, "%"),
    "trend": (92, 74, "index"),
    "signal": (1.0, 1.7, "index"),
    "related_signals": (1.0, 1.1, "index"),
    "confidence": (35, 54, "%"),
}

def choose_scenario(scenario_id=None):
    if scenario_id:
        for s in SCENARIOS:
            if s["id"] == scenario_id:
                return s
    return random.choice(SCENARIOS)

def generate_scenario(scenario_id=None, facility=None, seed=None):
    if seed is not None:
        random.seed(seed)
    s = dict(choose_scenario(scenario_id))
    facility = facility or random.choice(FACILITIES)
    region = random.choice(REGIONS)
    severity = "EMERGING" if s["id"]=="false_alarm" else random.choice(SEVERITIES)
    delta = random.choice([18,22,27,31,38,44])
    data={}
    for m in s["metrics"]:
        base,end,unit = METRIC_PROFILES.get(m,(50,80,"index"))
        if s["id"]=="false_alarm":
            end = base * random.uniform(.98,1.08)
        data[m]={"values":_series(base,end), "unit":unit, "start":base, "end":round(end,1)}
    return {
        **s,
        "facility": facility,
        "region": region,
        "severity": severity,
        "delta": delta,
        "opening_text": s["opening"].format(facility=facility,delta=delta),
        "investigation_text": s["investigation"].format(facility=facility,delta=delta),
        "insight_text": s["insight"].format(facility=facility,delta=delta),
        "impact_text": s["impact"].format(facility=facility,delta=delta),
        "data": data,
        "created_at": time.time(),
    }
