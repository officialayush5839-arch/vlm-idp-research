# Literature Matrix — Structured Summary of Related Works

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Classification Overview

All 20 reviewed papers in [`literature_registry.csv`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/literature/literature_registry.csv) are classified into functional research roles:

| Classification | Count | Description / Role in Project |
|:---|:---:|:---|
| **DIRECTLY_RELEVANT** | 8 | Core algorithmic and methodological foundations directly informing our architecture |
| **BASELINE** | 5 | Established benchmarks, datasets, and baseline evaluation systems |
| **COMPETING_APPROACH** | 2 | Primary foundation models and alternative architectures evaluated |
| **PARTIALLY_RELEVANT** | 1 | Specialized enhancement and pre-processing modules |
| **BACKGROUND** | 4 | Mathematical foundations (calibration, corruption benchmarks, layout pretraining) |

---

## 2. Topic-Level Literature Matrix

### Area A: Vision-Language Models & Long-Document Intelligence
*Focus: How modern VLMs parse documents, scale across pages, and handle multimodal structures.*

| Paper ID | Authors & Year | Venue | Primary Contribution | Key Limitation | Relevance to Our Project |
|:---|:---|:---:|:---|:---|:---|
| **P001** | Wang et al. (2024) | NeurIPS | MMLongBench-Doc: 135 long PDFs (avg 47.5 pages) testing multimodal reasoning | Assumes pristine digital PDFs; lacks degradation or adaptive routing | Direct long-document benchmark source and unanswerable question protocol |
| **P002** | Deng et al. (2025) | ACL | LongDocURL: 33,000+ pages evaluating locating, reasoning, and understanding | Evaluation benchmark only; no mitigation architecture | Locating evaluation protocol across pages |
| **P003** | Anonymous (2026) | arXiv | XL-DocBench: Human-verified benchmark up to 2,303 pages requiring page evidence | Pristine scans only; no visual corruptions | Grounding evaluation protocol for multi-page documents |
| **P014** | Bai et al. (2025) | arXiv | Qwen2.5-VL: Dynamic resolution ViT with native bounding-box grounding tokens | 7B model requires quantization on 6GB VRAM; sensitive to severe blur | Primary foundation reasoning engine for our proposed system |
| **P015** | Chen et al. (2024) | arXiv | InternVL 2.0: Progressive alignment with dynamic visual tiling and OCR pretraining | High compute requirements; overconfident on degraded images | Secondary foundation model for cross-architecture generalization (H6) |
| **P017** | Huang et al. (2022) | ACM MM | LayoutLMv3: Unified multimodal pretraining for 2D spatial document AI | Brittle pipeline: fails completely if upstream OCR fails on noisy inputs | Highlights need for adaptive routing over fixed OCR-dependent pipelines |

---

### Area B: Multimodal Retrieval & Evidence Grounding
*Focus: Locating cross-page evidence and anchoring model assertions in verifiable image coordinates.*

| Paper ID | Authors & Year | Venue | Primary Contribution | Key Limitation | Relevance to Our Project |
|:---|:---|:---:|:---|:---|:---|
| **P004** | Faysse et al. (2024) | arXiv | ColPali: Late-interaction patch-level document retrieval with VLMs | High index storage footprint; does not handle image degradation | Architecture blueprint for our multimodal retrieval module |
| **P019** | Tito et al. (2023) | ICCV-W | Grounding-DocVQA: Bounding-box evidence annotations for DocVQA questions | Single-page clean documents only | Informs our bounding-box IoU and Region Recall@$K$ metrics |
| **P020** | Yang et al. (2024) | ECCV | DocGround: Dense spatial grounding tokens reducing hallucination by 28% | Tested only on clean digital documents | Demonstrates that explicit spatial grounding reduces hallucinations |

---

### Area C: Uncertainty Estimation, Calibration & Selective Prediction
*Focus: Measuring model confidence, avoiding hallucinations, and knowing when to abstain.*

| Paper ID | Authors & Year | Venue | Primary Contribution | Key Limitation | Relevance to Our Project |
|:---|:---|:---:|:---|:---|:---|
| **P007** | Gao et al. (2024) | ACL Find. | ReCoVERR: Active evidence retrieval to prevent over-cautious abstention | Evaluated on general scene images, not structured documents | Conceptual framework for selective prediction trade-offs |
| **P008** | Bain et al. (2025) | arXiv | Variational VQA: Variational Bayes for calibrated selective prediction in VLMs | High computational cost during inference | Informs our multi-signal calibration architecture |
| **P009** | Park et al. (2025) | arXiv | Conformal Abstention Policies: Learnable risk-controlled thresholds | Requires clean exchangeable calibration data | Guides our validation-frozen risk-coverage thresholding |
| **P010** | Ren et al. (2024) | arXiv | Neighborhood Consistency: Semantic agreement across visual perturbations | High latency due to multiple forward passes | Inspires our multi-signal consistency score |
| **P016** | Cole et al. (2023) | EMNLP | Selective QA under Ambiguity: Risk-coverage curves for unanswerable questions | Pure text QA; lacks visual document awareness | Formal definition of selective accuracy, coverage, and empirical risk |
| **P018** | Guo et al. (2017) | ICML | Temperature and Platt scaling for neural network probability calibration | Formulated for simple classification, not structured generation | Mathematical definition of Expected Calibration Error (ECE) and Brier score |

---

### Area D: Document Degradation, Quality Assessment & Robustness
*Focus: Quantifying visual corruption, enhancing degraded scans, and routing inputs adaptively.*

| Paper ID | Authors & Year | Venue | Primary Contribution | Key Limitation | Relevance to Our Project |
|:---|:---|:---:|:---|:---|:---|
| **P006** | Jaume et al. (2019) | ICDAR-W | FUNSD: Real-world noisy scanned forms with key-value annotations | Small sample size (199 forms); static scan noise only | Primary benchmark for real-world degraded scanned documents |
| **P011** | Hendrycks & Dietterich (2019) | ICLR | ImageNet-C: 15 corruptions across 5 severity levels for neural robustness | Natural object images; lacks document-specific corruptions (skew, cutoff) | Methodological framework for our 9-factor controlled degradation benchmark |
| **P012** | Zhao et al. (2022) | ACM MM | DocTr: Transformer-based geometric and illumination restoration | Over-enhancement can introduce synthetic text artifacts | Candidate enhancement module in our `MODERATE` routing pathway |
| **P013** | Chen et al. (2024) | CVPR | Consensus Entropy: Multi-VLM agreement for verifying OCR in degraded documents | Multi-model forward passes too expensive for all documents | Validates multi-engine agreement as an indicator of document corruption |
