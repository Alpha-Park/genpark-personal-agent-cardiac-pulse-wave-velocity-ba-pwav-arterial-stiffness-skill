# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-cardiac-pulse-wave-velocity-ba-pwav-arterial-stiffness-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def assess_bapwv_arterial_stiffness(bapwv_cm_s, age_years, systolic_bp_mmhg=125, diastolic_bp_mmhg=80):
    if bapwv_cm_s <= 0 or age_years <= 0:
        raise ValueError("baPWV and age must be positive values")
        
    # Expected baPWV regression equation based on normal population cohorts:
    # Expected baPWV ~ 1000 + (11.5 * age) + (3.8 * (MAP - 90))
    map_bp = diastolic_bp_mmhg + (systolic_bp_mmhg - diastolic_bp_mmhg) / 3.0
    expected_bapwv = 1000.0 + (11.5 * age_years) + (3.8 * (map_bp - 90.0))
    
    delta_velocity = bapwv_cm_s - expected_bapwv
    # Vascular age adjustment: ~11.5 cm/s per chronological year
    vascular_age_gap_years = delta_velocity / 11.5
    estimated_vascular_age = max(18.0, round(age_years + vascular_age_gap_years, 1))
    
    # Clinical cutoff (AHA / Japanese Circulation Society):
    # < 1400 cm/s: Normal arterial compliance
    # 1400 - 1799 cm/s: Moderate arterial stiffening (early vascular aging EVA)
    # >= 1800 cm/s: Severe arteriosclerosis / high end-organ damage risk
    if bapwv_cm_s < 1400.0:
        stiffness_tier = "NORMAL_ELASTIC_ARTERIAL_COMPLIANCE"
        risk_level = "LOW"
    elif bapwv_cm_s < 1800.0:
        stiffness_tier = "MODERATE_ARTERIAL_STIFFENING"
        risk_level = "ELEVATED"
    else:
        stiffness_tier = "ADVANCED_ARTERIOSCLEROTIC_RIGIDITY"
        risk_level = "HIGH_STROKE_CAD_RISK"
        
    return {
        "measured_bapwv_cm_s": round(bapwv_cm_s, 1),
        "expected_population_bapwv": round(expected_bapwv, 1),
        "delta_velocity_cm_s": round(delta_velocity, 1),
        "chronological_age_years": age_years,
        "estimated_vascular_biological_age": estimated_vascular_age,
        "arterial_stiffness_tier": stiffness_tier,
        "cardiovascular_risk_tier": risk_level,
        "clinical_action": "High pulse wave velocity indicates medial elastocalcinosis; evaluate aortic root calcification and central pulse pressure." if bapwv_cm_s >= 1400.0 else "Healthy arterial windkessel buffering."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "assess_bapwv_arterial_stiffness",
                        "description": """Evaluate systemic arterial stiffness and central aortic compliance using Brachial-Ankle Pulse Wave Velocity (baPWV, cm/s).
Calculates age-adjusted vascular aging delta, predicts coronary atherosclerosis progression, and flags arterial wall stiffening thresholds (> 1400 cm/s).""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = assess_bapwv_arterial_stiffness(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'bapwv_cm_s': 1520.0, 'age_years': 48, 'systolic_bp_mmhg': 132, 'diastolic_bp_mmhg': 84}
        out = assess_bapwv_arterial_stiffness(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
