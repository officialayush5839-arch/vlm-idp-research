# Grounding Decision Matrix Report

## 1. Decision State Machine Architecture
The grounding decision state machine (`src/evidence/grounding_classifier.py`) deterministically synthesizes spatial, semantic, numeric, and sufficiency outcomes:

```text
               Candidate Evidence Units
                         │
        ┌────────────────┴────────────────┐
     [Empty?]                          [Present]
        │                                 │
     (YES) ────────┐                      ▼
        │          │             [Sufficiency Check]
        │          │                      │
        │          │        ┌─────────────┴─────────────┐
        │          │   [INSUFFICIENT]        [SUFFICIENT/PARTIAL]
        │          │        │                           │
        │          │        ▼                           ▼
        │          ├──> INSUFFICIENT_EVIDENCE    [Numeric Verification]
        │          │                                    │
        │          │                      ┌─────────────┴─────────────┐
        │          │                   [FAILED]                    [PASSED]
        │          │                      │                           │
        │          │                      ▼                           ▼
        │          └────────────────> NOT_SUPPORTED         [Semantic Support]
        │                                                     │
        │                                       ┌─────────────┴─────────────┐
        │                                    [FAILED]                    [PASSED]
        │                                       │                           │
        │                                       ▼                           ▼
        │                                  NOT_SUPPORTED           [Spatial Alignment]
        │                                                                   │
        │                                                     ┌─────────────┴─────────────┐
        │                                                   [FAIL]                      [PASS]
        │                                                     │                           │
        │                                                     ▼                           ▼
        │                                                NOT_SUPPORTED          [Sufficiency / Partial?]
        │                                                                                 │
        │                                                                    ┌────────────┴────────────┐
        │                                                                  (YES)                      (NO)
        │                                                                    │                          │
        │                                                                    ▼                          ▼
        └────────────────────────────────────────────────────────────> PARTIALLY_SUPPORTED          SUPPORTED
```

## 2. Invariants
- Zero Hallucination: An answer is NEVER marked `SUPPORTED` without passing all spatial, semantic, numeric, and sufficiency constraints.
- When evidence is missing, the system outputs `INSUFFICIENT_EVIDENCE` rather than fabricating rationale.
