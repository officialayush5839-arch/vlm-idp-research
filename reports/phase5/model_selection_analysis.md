# Phase 5 — Model Selection & Confusion Matrix Analysis

## 1. Model Selection Distribution Across Policies

Total test conditions evaluated: 900.

| Policy | B0 (Conventional OCR) | B1 (OCR + VLM) | B2 (Native VLM) | B0-U (Unlimited-OCR) |
|:---|:---:|:---:|:---:|:---:|
| **R1_FIXED_BEST** | 0 (0.0%) | 0 (0.0%) | 900 (100.0%) | 0 (0.0%) |
| **R2_RULE_BASED** | 0 (0.0%) | 0 (0.0%) | 760 (84.4%) | 140 (15.6%) |
| **R3_UNCERTAINTY** | 320 (35.6%) | 400 (44.4%) | 180 (20.0%) | 0 (0.0%) |
| **R4_LEARNED** | 0 (0.0%) | 0 (0.0%) | 900 (100.0%) | 0 (0.0%) |
| **R5_COMPOSITE** | 0 (0.0%) | 0 (0.0%) | 800 (88.9%) | 100 (11.1%) |
| **R0_ORACLE** | 180 (20.0%) | 0 (0.0%) | 560 (62.2%) | 160 (17.8%) |

---

## 2. Selection Alignment against Oracle Retrospective Choice

Confusion Matrix: **Actual Best Model (Oracle)** vs **Router Selected Model (R2 Rule-Based)**

| Actual Best (Rows) \ Selected (Cols) | B0 | B1 | B2 | B0-U | Row Total |
|:---|:---:|:---:|:---:|:---:|:---:|
| **B0 (Clean / High Quality)** | 0 | 0 | 140 | 40 | 180 |
| **B1 (Mild Structured)** | 0 | 0 | 0 | 0 | 0 |
| **B2 (Geometric / Noise / Blur)** | 0 | 0 | 560 | 0 | 560 |
| **B0-U (Compression / Lighting)** | 0 | 0 | 60 | 100 | 160 |
| **Column Total** | 0 | 0 | 760 | 140 | 900 |

### Key Observations
1. **Conservative Safety Bias**: R2 never selected B0 under degraded scenarios, preferring the higher safety floor of B2.
2. **Specialized Multimodal Routing**: R2 correctly routed 100 samples to B0-U when severe JPEG compression and lighting attenuation were detected.
3. **Model Selection Accuracy**: R2 matched the exact oracle optimal model in **660 of 900 conditions (73.33% alignment)**.
