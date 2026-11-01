# genpark-personal-agent-cardiac-pulse-wave-velocity-ba-pwav-arterial-stiffness-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Brachial-Ankle Pulse Wave Velocity (baPWV, cm/s) central arterial compliance & vascular calcification index.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `assess_bapwv_arterial_stiffness`
- **Category**: `personal_agent`

### Method Documentation
Evaluate systemic arterial stiffness and central aortic compliance using Brachial-Ankle Pulse Wave Velocity (baPWV, cm/s).
Calculates age-adjusted vascular aging delta, predicts coronary atherosclerosis progression, and flags arterial wall stiffening thresholds (> 1400 cm/s).

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "assess_bapwv_arterial_stiffness",
    "arguments": {
    "bapwv_cm_s": 1520.0,
    "age_years": 48,
    "systolic_bp_mmhg": 132,
    "diastolic_bp_mmhg": 84
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
