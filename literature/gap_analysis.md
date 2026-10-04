# Gap Analysis — Detailed Evaluation of the Three Research Gaps

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## Overview

The central thesis of this research project is that the primary failure mode of contemporary Vision-Language Models (VLMs) in Intelligent Document Processing (IDP) is not merely raw recognition failure, but **unreliable, ungrounded, and overconfident inference under visual degradation and long-context dependencies**. 

Rather than treating degradation, long documents, and uncertainty as three disconnected challenges, our contribution lies at their **formal intersection**.

---

## Gap 1: Uncertainty-Aware VLM for Reliable Document Processing

| Analysis Dimension | Gap 1 Specification |
|:---|:---|
| **Gap Definition** | Vision-Language Models generate plausible answers even when supporting visual evidence is incomplete, ambiguous, or corrupted, lacking reliable confidence estimation and calibrated abstention mechanisms. |
| **Existing Work** | Variational VQA (Bain et al., 2025), Selective Prediction in NLP (Cole et al., 2023), Conformal Abstention Policies (Park et al., 2025), Neighborhood Consistency (Ren et al., 2024), Softmax calibration (Guo et al., 2017). |
| **What Has Been Solved** | Post-hoc temperature scaling for image classification logits; semantic self-consistency across sampled textual outputs for text LLMs; theoretical risk-coverage bounds via conformal prediction on clean i.i.d. benchmarks. |
| **What Remains Unsolved** | Multimodal calibration in generative document VLMs where errors arise from a mixture of visual degradation, OCR failure, retrieval omission, and hallucinated reasoning. Pure token probabilities fail to capture visual ambiguity. |
| **Why Current Methods Are Insufficient** | Standard VLM self-reported confidence ("How confident are you from 0 to 1?") is notoriously overconfident and uncalibrated. Variational methods require expensive sampling or architectural modifications. Textual self-consistency misses visual hallucination. |
| **Our Proposed Approach** | A multi-signal uncertainty estimation framework combining: (1) visual quality vector degradation scores, (2) multi-engine OCR alignment confidence, (3) dense retrieval similarity scores, (4) bounding-box spatial grounding alignment, and (5) token logit consistency, calibrated via validation-frozen Logistic/Isotonic regression into tri-state decisions: `VERIFIED`, `UNCERTAIN`, `REVIEW_REQUIRED`. |
| **Experimental Evidence Needed** | Expected Calibration Error (ECE) < 0.08 across clean and degraded splits; Selective Accuracy vs. Coverage curves demonstrating significant reduction in unsupported answers at $\ge 70\%$ coverage; risk reduction over fixed-threshold baselines. |
| **Potential Novelty** | Multi-signal multimodal calibration specifically linking visual quality degradation and spatial grounding support to selective prediction abstention in document AI. |
| **Risk of Overlap** | Moderate overlap with general selective prediction literature; mitigated by framing the calibration specifically around document-domain evidence grounding and degradation signals. |
| **Research Strength** | **9.2 / 10** — Addresses a critical trustworthiness barrier for enterprise and safety-critical document automation. |

---

## Gap 2: Evidence-Grounded Long-Document VLM

| Analysis Dimension | Gap 2 Specification |
|:---|:---|
| **Gap Definition** | In multi-page complex documents, relevant evidence is distributed across multiple pages and modalities (tables, forms, prose), but current VLMs either suffer from context-window degradation or produce ungrounded answers without verifiable provenance. |
| **Existing Work** | MMLongBench-Doc (Wang et al., NeurIPS 2024), LongDocURL (Deng et al., ACL 2025), XL-DocBench (2026), ColPali (Faysse et al., 2024), Grounding-DocVQA (Tito et al., ICCV 2023), DocGround (Yang et al., ECCV 2024). |
| **What Has Been Solved** | Page-level text retrieval using dense embeddings (BGE, E5); patch-based visual retrieval (ColPali); single-page bounding box grounding for high-resolution clean scans. |
| **What Remains Unsolved** | Joint multi-page evidence retrieval and fine-grained spatial grounding under varying visual degradation. Existing benchmarks show that $\ge 70\%$ of multi-page questions fail in current VLMs due to "needle-in-a-haystack" visual distraction and context truncation. |
| **Why Current Methods Are Insufficient** | Text-only RAG completely strips visual layout, tabular structure, and graphical annotations. Visual RAG (e.g., passing 50 full-resolution page images) exceeds consumer GPU memory and causes severe visual attention dispersion. Answer-only evaluation hides the fact that up to 40% of correct answers are derived from spurious background correlations rather than true evidence. |
| **Our Proposed Approach** | A hierarchical multimodal retrieval and provenance pipeline: (1) Page-level multimodal indexing (combining text layout chunks and visual page embeddings), (2) Top-$k$ page and region filtering, (3) VLM reasoning conditioned strictly on retrieved multimodal evidence, and (4) Explicit spatial grounding returning normalized bounding boxes, page IDs, and supporting text snippets with verified provenance. |
| **Experimental Evidence Needed** | Page Recall@$k$ ($k \in \{1, 3, 5, 10\}$); Grounding IoU $\ge 0.50$ against human-annotated bounding boxes; reduction in Unsupported Answer Rate on multi-page benchmarks (MMLongBench-Doc, XL-DocBench). |
| **Potential Novelty** | End-to-end provenance architecture that ties generation directly to page/region bounding boxes and triggers `REVIEW_REQUIRED` if grounding support is below the validation-calibrated threshold. |
| **Risk of Overlap** | High interest in multimodal RAG (ColPali); mitigated by focusing on spatial evidence provenance verification and linking grounding scores into the downstream uncertainty module. |
| **Research Strength** | **8.8 / 10** — Long-context multimodal reasoning is one of the highest-priority frontiers in document intelligence. |

---

## Gap 3: Robust VLM-IDP Under Real-World Visual Degradation

| Analysis Dimension | Gap 3 Specification |
|:---|:---|
| **Gap Definition** | Real-world documents suffer from unpredictable combinations of blur, noise, compression, skew, glare, and resolution loss, causing severe performance drops in fixed VLM or fixed OCR pipelines. |
| **Existing Work** | ImageNet-C corruptions (Hendrycks & Dietterich, ICLR 2019), DocTr document restoration (Zhao et al., ACM MM 2022), Consensus Entropy (Chen et al., CVPR 2024), OCR robustness benchmarks (FUNSD, ICDAR). |
| **What Has Been Solved** | Individual image restoration algorithms (e.g., standalone deskewing, neural denoising); static evaluation of OCR engines under specific noise types. |
| **What Remains Unsolved** | Adaptive, degradation-aware routing that dynamically inspects document corruption and selects the optimal processing pathway (Direct VLM, Enhancement + VLM, or OCR-assisted VLM) without imposing heavy compute penalties on clean documents or hallucination artifacts on degraded documents. |
| **Why Current Methods Are Insufficient** | Blindly applying heavy image restoration (e.g., deep deblurring or dewarping) to all documents degrades throughput by $5\times$ to $10\times$ and often introduces synthetic hallucination artifacts into clean text. Conversely, pure VLMs fail abruptly when resolution drops or blur increases, while pure OCR fails on complex graphical layouts. |
| **Our Proposed Approach** | A lightweight Quality & Degradation Assessment module that extracts an interpretable quality vector (blur, noise, illumination, skew, compression, small text, crop, glare, occlusion, resolution, perspective) and an aggregated quality score $\mathcal{Q} \in [0, 1]$. An adaptive router directs pages to: (1) `CLEAN` $\rightarrow$ Direct VLM, (2) `MODERATE` $\rightarrow$ Targeted Enhancement + VLM, (3) `SEVERE` $\rightarrow$ OCR Fallback + OCR-Assisted VLM. Thresholds are learned strictly on validation data. |
| **Experimental Evidence Needed** | Degradation-accuracy slope demonstrating significantly flatter performance degradation curves compared to fixed baselines B2 (VLM-only) and B6 (Fixed Preprocessing + VLM); latency and compute efficiency trade-off analysis. |
| **Potential Novelty** | Systematic, multi-factor degradation benchmarking coupled with dynamic tri-pathway routing specifically engineered for open-source VLMs in document processing. |
| **Risk of Overlap** | Low to moderate. Prior work either studies pure enhancement or pure VLM inference; very few papers systematically evaluate adaptive quality-aware routing across a 9-factor controlled degradation grid. |
| **Research Strength** | **9.5 / 10** — Highly practical, experimentally verifiable, and provides immediate value to real-world scanned document processing. |

---

## Synthesis: The Core Combined Novelty

The three gaps form an interlocking triad:

```text
Visual Degradation (Gap 3)
           ▲
          ╱ ╲
         ╱   ╲
        ╱  ★  ╲
       ▼       ▼
Long-Doc      Uncertainty &
Evidence      Calibrated
Grounding     Abstention
 (Gap 2)       (Gap 1)
```

1. **Degradation directly impairs Evidence Grounding**: Visual blur and noise make bounding-box localization unstable. Adaptive routing preserves grounding fidelity.
2. **Grounding directly powers Uncertainty Estimation**: An answer that cannot be spatially grounded back to the document image is inherently suspect, providing an objective physical grounding signal for calibration.
3. **Uncertainty triggers Abstention under Degradation**: When severe corruption makes reliable reasoning impossible, the system gracefully abstains (`REVIEW_REQUIRED`) with available partial evidence, rather than outputting confident hallucinations.
