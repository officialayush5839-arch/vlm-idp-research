# Decision Threshold & Operating Points Provenance Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Threshold Provenance & Derivation Table

| Threshold Parameter | Value | Source Partition | Derivation Objective | Test Influenced? |
|---|---|---|---|:---:|
| `tau_accept` | 0.9038 | Validation (`val`) | 75th percentile of validation calibrated confidence | NO |
| `tau_warning` | 0.8143 | Validation (`val`) | 45th percentile of validation calibrated confidence | NO |
| `tau_escalate` | 0.5487 | Validation (`val`) | 20th percentile of validation calibrated confidence | NO |
| `u_max_accept` | 0.2500 | Validation (`val`) | Maximum allowed uncertainty for full acceptance | NO |
| `u_max_warning` | 0.5000 | Validation (`val`) | Maximum allowed uncertainty for warning state | NO |
| `u_max_escalate` | 0.7000 | Validation (`val`) | Maximum allowed uncertainty for escalation state | NO |

---

## 2. Findings
- Thresholds were generated deterministically during the execution of `scripts/run_phase9_calibrate.py` and serialized to `experiments/phase9/models/reliability_thresholds.json`.
- The test split was completely untouched during threshold selection.
