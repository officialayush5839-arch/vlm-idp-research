# VLM-IDP Research

> **Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation**

## Overview

This is a **research-grade** Intelligent Document Processing system based on Vision-Language Models (VLMs) that combines:

1. **Degradation-aware adaptive processing** — detects document quality and routes to appropriate pipelines
2. **Evidence-grounded long-document reasoning** — retrieves and links answers to page/region evidence
3. **Calibrated uncertainty and abstention** — estimates reliability and abstains when evidence is insufficient

## Research Objective

Demonstrate that the intersection of quality-aware routing, multimodal evidence retrieval, evidence grounding, and calibrated uncertainty produces a better accuracy–reliability trade-off than individual components or fixed pipelines.

## Project Type

- **Software-only** AI/ML research project
- **Target**: IEEE research paper
- **Primary VLM**: Qwen2.5-VL 7B (open, reproducible)
- **NOT**: A generic document chatbot or production system

## Repository Structure

```
vlm-idp-research/
├── prd.md                  # Product/Research Requirements Document
├── architecture.md         # Technical architecture source of truth
├── rules.md                # Non-negotiable project constitution
├── phases.md               # Project roadmap (Phase 0–13)
├── memory.md               # Persistent project state
├── goal.md                 # Highest-level project direction
├── task.md                 # Active execution queue
├── agents.md               # Agent operating manual
├── research_protocol.md    # Frozen experimental methodology
│
├── paper/                  # IEEE manuscript, figures, tables
├── configs/                # YAML configuration files
├── data/                   # Datasets (not versioned)
├── src/                    # Source code (Python packages)
├── experiments/            # Experiment outputs
├── tests/                  # Test suite
├── scripts/                # Utility scripts
└── reports/                # Generated reports
```

## Control File Hierarchy

```
rules.md          ← Constitution (supreme authority)
    ↓
goal.md           ← Direction
    ↓
prd.md            ← Requirements
    ↓
architecture.md   ← Technical design
    ↓
phases.md         ← Roadmap
    ↓
task.md           ← Execution
    ↓
memory.md         ← Factual state
```

## Current Status

- **Phase**: 0 — Literature freeze + research protocol
- **Status**: IN_PROGRESS

## Environment

- Python 3.14.6
- NVIDIA RTX 3050 6GB Laptop GPU
- Windows

## Anti-Fabrication Policy

This is a research project intended for publication. **No experimental results, metrics, or data are fabricated.** All results use provenance statuses: `NOT_RUN`, `DECLARED`, `CONFIRMED`, `DERIVED`, etc.

## License

Research use. See project documentation for details.
