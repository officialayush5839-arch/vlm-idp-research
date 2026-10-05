# Phase 5 — Adaptive Routing Architecture Document

## 1. System Overview
The Adaptive Routing Module (`src/routing/`) provides an inference-time decision layer that evaluates document visual degradation and pipeline uncertainty signals to select among heterogeneous processing pipelines:
- **B0**: Conventional OCR (PaddleOCR primary / Tesseract secondary)
- **B1**: Hybrid OCR + VLM (`Qwen2.5-VL-7B-Instruct` conditioned on OCR text)
- **B2**: Native VLM (`Qwen2.5-VL-7B-Instruct` vision-only)
- **B0-U**: Contemporary Multimodal OCR (`Unlimited-OCR`)

## 2. Decoupled Pipeline Design
The routing engine operates strictly as an orchestration layer external to the baseline models and feature extractors:
```text
                         INPUT DEGRADED DOCUMENT
                                    |
                                    v
                   +----------------------------------+
                   |  Phase 3 Quality Pipeline        |
                   |  (Extracts 10-feature vector)    |
                   +----------------+-----------------+
                                    |
                                    v
                   +----------------------------------+
                   |  Quality Feature Adapter         |
                   |  (Normalizes features [0, 1])    |
                   +----------------+-----------------+
                                    |
                                    v
                   +----------------------------------+
                   |  Uncertainty Adapter             |
                   |  (Assembles 6-signal vector u)   |
                   +----------------+-----------------+
                                    |
                                    v
                   +----------------------------------+
                   |  Routing Policy Manager          |
                   |  (R1, R2, R3, R4, R5, R0)        |
                   +----------------+-----------------+
                                    |
                                    v
                          SELECTED CANDIDATE
                         (B0 / B1 / B2 / B0-U)
                                    |
                                    v
                   +----------------------------------+
                   |  Candidate Model Execution       |
                   +----------------+-----------------+
                                    |
                                    v
                   +----------------------------------+
                   |  Structural Fallback Handler     |
                   |  (Checks non-empty / valid bbox) |
                   +----------------+-----------------+
                                    |
                        +-----------+-----------+
                        |                       |
                     Valid                  Malformed
                        |                       |
                        v                       v
                   Task Evaluator          Execute B2 Fallback
                        |                       |
                        +-----------+-----------+
                                    |
                                    v
                         Immutable JSON Artifact
                         + Full Decision Trace
```

## 3. Module Responsibilities
- `schema.py`: Formal Pydantic v2 schemas (`RoutingDecision`, `RoutingTrace`, `UncertaintyVector`, `RoutingCost`, `RoutingRunArtifact`).
- `feature_adapter.py`: Adapts Phase 3 `PageQualityAssessment` into a 10-dimensional float vector.
- `rule_engine.py`: Evaluates deterministic boundaries configured in `configs/phase5/router_rules.yaml`.
- `uncertainty.py`: Extracts and normalizes the 6 signals conforming to `protocol/uncertainty_protocol.md`.
- `calibration.py`: Fits post-hoc logistic and isotonic calibrators strictly on validation split data.
- `learned_router.py`: Lightweight classifier trained on validation model selection outcomes.
- `policy.py`: Central dispatching interface for all policies (R0 through R5).
- `fallback.py`: Structural output validator guarding against silent crashes and schema violations.
- `cost.py`: Computes engineering objective cost $J = \lambda_{\text{compute}} \cdot \text{compute} + \lambda_{\text{latency}} \cdot \text{latency}$.
- `decision_trace.py`: Logs immutable JSON audit traces.
- `audit.py`: Static AST analyzer preventing test data or ground-truth leakage.
- `router.py`: High-level orchestrator.
- `pipeline.py`: End-to-end sample processing lifecycle.
