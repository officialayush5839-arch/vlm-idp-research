# PHASE 0 FINAL REPORT — Research Protocol Freeze & Experimental Foundation

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Project Stage**: Phase 0 Complete  
**Date**: 2026-10-04  
**Target Venue**: IEEE Conference / Journal  

---

## 1. Executive Summary
Phase 0 of the VLM-IDP research project has established the scientific, experimental, and methodological foundation required to build a research-grade Intelligent Document Processing system. Through rigorous literature synthesis across 20 primary academic papers, formal mathematical definitions of 7 evaluation dimensions, and the creation of 9 operational sub-protocols, Phase 0 eliminates all scientific ambiguity and sets an unyielding standard of research integrity (zero data leakage, zero fabricated metrics, multi-seed statistical significance).

---

## 2. Research Problem
Existing Intelligent Document Processing (IDP) systems extract text, tables, and answers from clean digital scans, but their reliability degrades catastrophically when documents contain physical visual corruptions (blur, noise, skew, glare, compression), dense multi-page dependencies, or ambiguous visual evidence. Contemporary Vision-Language Models (VLMs) generate fluent, persuasive answers even when supporting visual evidence is incomplete or ungrounded. In multi-page enterprise documents, evidence is distributed across disjoint layouts, rendering answer-only evaluations insufficient. Therefore, there is a fundamental need for an adaptive VLM-IDP framework that estimates document quality, dynamically routes to specialized pathways, performs multi-page evidence retrieval, grounds answers to verifiable pixels, quantifies predictive uncertainty, and selectively abstains when evidence is insufficient.

---

## 3. Research Gaps
The project addresses three interconnected research gaps:
1. **Gap 1 (Uncertainty-Aware VLM Processing)**: Lack of calibrated confidence estimation and principled selective abstention in generative document VLMs, leading to harmful hallucinations.
2. **Gap 2 (Evidence-Grounded Long-Document Reasoning)**: Severe context degradation and lack of spatial bounding-box provenance when reasoning across multi-page complex documents.
3. **Gap 3 (Robust VLM-IDP Under Visual Degradation)**: Absence of dynamic, quality-aware routing that adapts processing to visual corruptions without imposing heavy compute penalties on clean documents.
*Core Contribution*: The systematic integration of all three gaps into an end-to-end adaptive framework.

---

## 4. Literature Findings
A systematic review of 20 primary papers from CVPR, NeurIPS, ICLR, ICML, ACL, WACV, and ACM MM revealed:
- Recent long-document benchmarks (MMLongBench-Doc, LongDocURL, XL-DocBench) show that VLMs frequently perform *worse* than text LLMs on OCR text due to visual context truncation and lack of locating precision.
- Tito et al. (Grounding-DocVQA) demonstrated that up to 40% of correct answers from top document models exploit spurious linguistic priors without true visual grounding.
- Multimodal retrieval (ColPali) dramatically improves visual layout recall, but operates without uncertainty calibration or degradation handling.
- Selective prediction methods (ReCoVERR, Variational VQA) exist for natural scene VQA, but have not been adapted to multi-page degraded document AI.

---

## 5. Novelty Assessment
As established in [`literature/novelty_matrix.md`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/literature/novelty_matrix.md), our system is the first to simultaneously unify:
1. Multi-factor image quality assessment and tri-pathway adaptive routing (`CLEAN` / `MODERATE` / `SEVERE`),
2. Hierarchical multimodal retrieval with spatial bounding-box provenance tracking, and
3. Multi-signal uncertainty calibration linking visual quality and grounding overlap into a validation-frozen abstention policy.

---

## 6. Research Questions
- **Primary RQ**: How can a Vision-Language Model-based intelligent document processing system adapt its processing strategy to real-world visual degradation while maintaining reliable long-document reasoning, verifiable evidence grounding, and calibrated uncertainty?
- **RQ1**: Which visual degradation factors cause the largest failures in VLM-based document understanding?
- **RQ2**: Can quality-aware routing outperform a fixed VLM pipeline across multiple degradation levels?
- **RQ3**: Does explicit evidence grounding reduce unsupported answers in long documents?
- **RQ4**: Can multimodal retrieval recover cross-page evidence more reliably than text-only retrieval?
- **RQ5**: Can calibrated uncertainty identify incorrect answers early enough to support safe abstention?
- **RQ6**: What accuracy–reliability–latency trade-off is achieved by the integrated framework?

---

## 7. Hypotheses
- **H1**: Increasing visual degradation significantly reduces VLM document extraction/reasoning performance.
- **H2**: Adaptive degradation-aware routing reduces performance degradation compared with a fixed VLM pipeline.
- **H3**: Evidence grounding reduces unsupported/hallucinated answers compared with answer-only VLM inference.
- **H4**: Calibrated uncertainty and abstention reduce harmful false answers while preserving adequate valid-answer coverage.
- **H5**: The integrated framework provides a better accuracy–reliability–latency trade-off than individual components alone.
- **H6**: The proposed method generalizes across document types rather than improving only one benchmark.

---

## 8. Dataset Selection
Seven established public benchmarks have been selected and allocated:
1. `DocVQA`: Primary QA, extraction, and spatial grounding benchmark.
2. `FUNSD`: Real-world historical scan degradation anchor.
3. `SROIE`: Receipt field extraction and thermal print fading.
4. `CORD`: Complex layout retail receipts.
5. `MMLongBench-Doc`: Long-context multi-page reasoning and unanswerable questions.
6. `LongDocURL`: Multi-page cross-element locating and reasoning.
7. `XL-DocBench`: Extra-long document evidence grounding.

---

## 9. Split Protocol
Codified in [`protocol/split_protocol.md`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/protocol/split_protocol.md):
- **Mandatory Zero-Leakage Invariant**: All degraded variants $\mathcal{V}(D_i)$ inherit the partition of source document $D_i$. Clean versions may not exist in train if degraded variants exist in test.
- Deterministic document-level SHA-256 assignment ($70\%$ train / $15\%$ val / $15\%$ test).
- Automated CI assertion asserting empty intersection across partitions.

---

## 10. Degradation Protocol
Codified in [`protocol/degradation_protocol.md`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/protocol/degradation_protocol.md):
- 9 controlled corruption families: Gaussian Blur ($\sigma \in [0, 6]$), JPEG Compression ($Q \in [10, 100]$), Gaussian Noise ($\sigma \in [0, 50]$), Skew / Rotation ($\theta \in [0^\circ, 10^\circ]$), Illumination ($\alpha \in [0.15, 1.00]$), Occlusion ($0\% - 30\%$), Resolution Reduction ($100\% - 15\%$), Perspective Distortion ($\phi \in [0^\circ, 35^\circ]$), and Mixed Degradation.
- Deterministic seeding with coordinate matrix transformation tracking for spatial ground truth.
- Explicit experimental separation of synthetic corruptions vs. natural scan artifacts (`FUNSD`).

---

## 11. Baseline Protocol
Codified in [`protocol/baseline_protocol.md`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/protocol/baseline_protocol.md):
- **B0**: OCR-Only (PaddleOCR / Tesseract)
- **B1**: OCR + VLM (PaddleOCR text fed into Qwen2.5-VL)
- **B2**: VLM-Only (Direct ungrounded Qwen2.5-VL 7B)
- **B3**: VLM + Text RAG (BGE embeddings + FAISS)
- **B4**: VLM + Multimodal Retrieval (ColPali page embeddings + FAISS)
- **B5**: VLM + Spatial Grounding (Qwen2.5-VL coordinate prompting)
- **B6**: Fixed Preprocessing + VLM (Universal OpenCV enhancement + Qwen2.5-VL)
- **PROPOSED**: Quality Assessment + Adaptive Routing + Multimodal Index + Evidence Grounding + Calibrated Uncertainty.

---

## 12. Model Selection
- **Primary VLM**: `Qwen2.5-VL-7B-Instruct` (Native dynamic resolution ViT, spatial bounding-box coordinate tokens, open Apache 2.0 license).
- **Secondary VLM**: `InternVL2-8B` (Used for generalization ablation A9).
- **OCR Engine**: `PaddleOCR` (Primary) and `pytesseract` (Classical).
- **Embeddings & Vector Index**: `BAAI/bge-large-en-v1.5` and `FAISS` (IndexFlatIP).

---

## 13. Retrieval Protocol
- Hierarchical multimodal retrieval: page-level visual embeddings combined with dense layout text chunking.
- Evaluated across $k \in \{1, 3, 5, 10\}$.
- Output schema preserves `document_id`, `page_id`, `region_id`, `bounding_box`, `chunk_id`, and `retrieval_score`.

---

## 14. Evidence Grounding Protocol
- Normalized coordinate interval $[0, 1000]$: $[x_{\text{min}}, y_{\text{min}}, x_{\text{max}}, y_{\text{max}}]$.
- Verified grounding criterion: $\text{Page Match} \wedge \text{IoU}(B_{\text{pred}}, B_{\text{gt}}) \ge 0.50 \wedge \text{Text Alignment} \ge 0.70$.
- Automatic `REVIEW_REQUIRED` trigger if grounding validation fails.

---

## 15. Uncertainty Protocol
- Multi-signal feature vector: $\mathbf{u} = [u_{\text{vlm}}, u_{\text{ocr}}, u_{\text{ret}}, u_{\text{gnd}}, u_{\text{qual}}, u_{\text{agr}}]$.
- Calibrator models: Platt scaling (Logistic Regression), Isotonic Regression, small 2-layer MLP.
- Target metric: Expected Calibration Error (ECE) $< 0.08$.

---

## 16. Abstention Protocol
- Validation-frozen decision cutoffs:
  - $c \ge \tau_{\text{accept}} \wedge \text{Grounding Valid} \implies \textbf{VERIFIED}$
  - $\tau_{\text{review}} \le c < \tau_{\text{accept}} \implies \textbf{UNCERTAIN}$
  - $c < \tau_{\text{review}} \vee \text{Grounding Failed} \implies \textbf{REVIEW\_REQUIRED}$
- Evaluated via Risk-Coverage curves, Selective Accuracy, and Area Under the Risk-Coverage Curve (AURC).

---

## 17. Metrics
- **Extraction & QA**: Exact Match (EM), Token F1, ANLS ($\tau=0.50$).
- **OCR**: Character Error Rate (CER), Word Error Rate (WER).
- **Retrieval**: Page Recall@$k$ ($k \in \{1, 3, 5, 10\}$), MRR.
- **Grounding**: IoU@0.50, Region Recall@$K$, Unsupported Answer Rate (UAR).
- **Calibration**: ECE ($M=10$ bins), Brier Score, Reliability Diagrams.
- **Selective Prediction**: Coverage, Risk, Selective Accuracy, AURC.
- **Robustness**: Performance Drop ($\Delta_{\text{deg}}$), Robustness Slope ($\beta_{\text{rob}}$).
- **Efficiency**: Latency (ms), Peak VRAM (MB), Route Distribution.

---

## 18. Statistical Methodology
- Multi-seed protocol: Minimum 3 seeds ($S_3 = \{42, 123, 456\}$), preferred 5 seeds ($S_5 = \{42, 123, 456, 789, 101112\}$).
- Non-parametric Paired Bootstrap Resampling ($B=10,000$ iterations) for comparing model pairs.
- Reporting format: $\text{Mean} \pm \text{Std}$ with $95\%$ Confidence Intervals.
- Mandatory effect size reporting (Cohen's $d$, Cliff's delta); $p$-values alone are prohibited.

---

## 19. Ablation Plan
Twelve explicit ablations (A1–A12) mapping bijectively to every claimed contribution:
- **A1**: Remove quality assessment
- **A2**: Remove adaptive routing (force single pathway)
- **A3**: Remove OCR fallback pathway
- **A4**: Remove multimodal retrieval (pure text RAG)
- **A5**: Remove evidence grounding verification
- **A6**: Remove uncertainty calibration (raw logits)
- **A7**: Remove abstention mechanism (forced prediction)
- **A8**: Fixed preprocessing vs. adaptive preprocessing
- **A9**: VLM model family comparison (Qwen2.5-VL 7B vs InternVL2 8B)
- **A10**: Retrieval depth comparison ($k \in \{1, 3, 5, 10\}$)
- **A11**: Single degradation vs. mixed composite degradation
- **A12**: Clean vs. synthetic degraded vs. real degraded (FUNSD)

---

## 20. Experiment Matrix
Formalized in [`configs/phase0/experiment_matrix.yaml`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/configs/phase0/experiment_matrix.yaml), spanning all baselines, degradation grid runs, long-document runs, and ablations across multiple seeds.

---

## 21. Reproducibility
- Global deterministic seeding function `seed_everything()` locking Python, NumPy, PyTorch, and cuDNN.
- Machine-readable JSON/Parquet run record schema capturing Git commit, model quantization, hardware specs, and configuration hashes.
- 100% configuration-driven YAML architecture.

---

## 22. Risks
All 15 scientific and engineering risks (R1–R15) cataloged in [`reports/phase0/risk_register.md`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/reports/phase0/risk_register.md) with active mitigation and contingency pathways.

---

## 23. Open Questions
1. *Optimal 4-bit quantization engine for RTX 3050*: Compare `bitsandbytes` NF4 vs. `AWQ` in Phase 1 for VRAM efficiency and inference latency.
2. *Empirical Single-Query Latency*: To be benchmarked on local hardware during Phase 1 technical validation.

---

## 24. Phase 0 Acceptance Criteria
- [x] Primary Research Question frozen
- [x] Secondary Research Questions (RQ1–RQ6) frozen
- [x] Hypotheses (H1–H6) frozen
- [x] Literature survey of 20 academic papers completed and audited
- [x] Gap analysis table completed across all 10 criteria
- [x] Novelty matrix completed across 10 system dimensions
- [x] 7 public benchmark datasets selected with roles defined
- [x] Zero-leakage data partition protocol frozen
- [x] 9-factor controlled degradation grid parameterized
- [x] Baselines B0–B6 and PROPOSED formally specified
- [x] Primary VLM (Qwen2.5-VL 7B) and secondary VLM (InternVL2 8B) selected
- [x] Evaluation metrics mathematically defined across 7 categories
- [x] Multi-signal uncertainty and calibration protocol frozen
- [x] Grounding schema and IoU verification rules frozen
- [x] 5-seed statistical testing and paired bootstrap protocol frozen
- [x] 12 ablations (A1–A12) frozen
- [x] Feasibility and VRAM budget analysis completed
- [x] Claim-to-experiment traceability matrix established
- [x] Risk register (R1–R15) established

---

## 25. Final PASS/FAIL: PASS
Phase 0 satisfies all scientific, architectural, and methodological requirements with zero unresolved contradictions.
