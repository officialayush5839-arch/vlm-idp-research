# Phase 6 Report 01: Hierarchical Multimodal Retrieval Architecture

## 1. Executive Summary
Phase 6 establishes a hierarchical coarse-to-fine multimodal retrieval architecture designed to alleviate the computational bottleneck of Vision-Language Models (VLMs) when reasoning over long, multi-page, and visually degraded documents.

## 2. The Long-Document VLM Bottleneck
VLMs such as Qwen2.5-VL exhibit quadratic or high linear token scaling with respect to image resolution and page count. Feeding an entire 50-page document into a 7B VLM requires tens of thousands of visual tokens, exceeding consumer GPU VRAM limits (RTX 3050 6GB) and causing catastrophic attention dilution.

## 3. Coarse-to-Fine Pipeline Design
To resolve this, Phase 6 implements a two-stage hierarchical paradigm:
```
           +---------------------------------------------+
           | Input Document: Multi-Page Corpus (N pages) |
           +----------------------+----------------------+
                                  |
                                  v
           +---------------------------------------------+
           | Stage 1: Multimodal Page Indexing           |
           |   - Text stream: BM25 Lexical + Dense SVD   |
           |   - Visual stream: Spatial Layout Pyramids  |
           +----------------------+----------------------+
                                  |
                                  v
           +---------------------------------------------+
           | Stage 2: Coarse Page Retrieval & Fusion     |
           |   - Score Normalization (Min-Max)           |
           |   - Hybrid Combination (alpha = 0.60)       |
           |   - Output: Top-K Candidate Pages (K=3)     |
           +----------------------+----------------------+
                                  |
                                  v
           +---------------------------------------------+
           | Stage 3: Cross-Modal Reranker               |
           |   - Query-Layout Structural Alignment       |
           |   - Region Density Bonus & Diversity Filter |
           +----------------------+----------------------+
                                  |
                                  v
           +---------------------------------------------+
           | Stage 4: Fine-Grained Region Localization   |
           |   - Sub-page bounding box filtering         |
           |   - Coordinate system: [0, 1000] integer    |
           |   - Output: Top-M Target Regions (M=3)      |
           +----------------------+----------------------+
                                  |
                                  v
           +---------------------------------------------+
           | Standardized EvidencePackage + Provenance   |
           |   - Pruned Page Payload (Reduction: 70-94%) |
           |   - Passed to Downstream VLM Reasoning      |
           +---------------------------------------------+
```

## 4. Key Architectural Guarantees
1. **Zero Test-Set Leakage**: Ground-truth target pages/regions are strictly forbidden from retrieval scoring.
2. **Determinism**: Fully deterministic execution across random seeds with fixed initializations.
3. **Software-Only & CPU-Friendly**: Implemented in pure Python, numpy, and scikit-learn without heavy external vector database binaries.
