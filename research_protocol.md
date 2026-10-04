# VLM-IDP Research Protocol: Frozen Experimental Methodology

## 0. Research Questions and Hypotheses

### Primary Research Question
> How can a Vision-Language Model-based intelligent document processing system adapt its processing strategy to real-world visual degradation while maintaining reliable long-document reasoning, verifiable evidence grounding, and calibrated uncertainty?

### Secondary Research Questions
- **RQ1**: Which visual degradation factors cause the largest failures in VLM-based document understanding?
- **RQ2**: Can quality-aware routing outperform a fixed VLM pipeline across multiple degradation levels?
- **RQ3**: Does explicit evidence grounding reduce unsupported answers in long documents?
- **RQ4**: Can multimodal retrieval recover cross-page evidence more reliably than text-only retrieval?
- **RQ5**: Can calibrated uncertainty identify incorrect answers early enough to support safe abstention?
- **RQ6**: What accuracy–reliability–latency trade-off is achieved by the integrated framework?

### Research Hypotheses
- **H1**: Increasing visual degradation significantly reduces VLM document extraction/reasoning performance.
- **H2**: Adaptive degradation-aware routing reduces performance degradation compared with a fixed VLM pipeline.
- **H3**: Evidence grounding reduces unsupported/hallucinated answers compared with answer-only VLM inference.
- **H4**: Calibrated uncertainty and abstention reduce harmful false answers while preserving adequate valid-answer coverage.
- **H5**: The integrated framework provides a better accuracy–reliability–latency trade-off than individual components alone.
- **H6**: The proposed method generalizes across document types rather than improving only one benchmark.

## 1. Baselines
- **B0** = OCR-only
- **B1** = OCR + VLM
- **B2** = VLM-only
- **B3** = VLM + text RAG
- **B4** = VLM + multimodal/page retrieval
- **B5** = VLM + spatial/evidence grounding
- **B6** = Fixed preprocessing + VLM
- **PROPOSED** = Quality-aware adaptive routing + Multimodal retrieval + Evidence grounding + Calibrated uncertainty + Abstention

## 2. Ablations (A1-A12)
- **A1** = remove quality/degradation assessment
- **A2** = remove adaptive routing
- **A3** = remove OCR fallback
- **A4** = remove multimodal retrieval
- **A5** = remove evidence grounding
- **A6** = remove uncertainty calibration
- **A7** = remove abstention
- **A8** = fixed preprocessing vs adaptive preprocessing
- **A9** = VLM size comparison
- **A10** = retrieval k comparison (k=1,3,5,10)
- **A11** = single degradation vs mixed degradation
- **A12** = clean vs synthetic degraded vs real degraded

## 3. Statistical Requirements
- Minimum 3 seeds, preferably 5
- Report: mean, std, 95% CI, effect size
- Paired bootstrap or justified test
- No p-value-only reporting
- No test-set tuning

## 4. Evaluation Metrics
- **Extraction**: EM, F1, ANLS
- **OCR**: CER, WER
- **QA**: EM, F1
- **Retrieval**: Recall@1, 3, 5, 10
- **Grounding**: IoU, mAP, Region Recall@K
- **Hallucination**: Unsupported Answer Rate, Hallucination-Free Accuracy
- **Calibration**: ECE, Brier, Reliability Diagram
- **Abstention**: Risk-Coverage, Selective Accuracy, Coverage, Risk
- **Robustness**: Accuracy vs severity, Performance drop, Robustness slope
- **Efficiency**: Latency, Throughput, VRAM, Tokens, Route

## 5. Dataset Protocol
- **Target Datasets**:
  - `DocVQA`: Document Visual Question Answering
  - `FUNSD`: Form Understanding in Noisy Scanned Documents
  - `SROIE`: Scanned Receipts OCR and Information Extraction
  - `CORD`: Consolidated Receipt Dataset for Post-OCR Parsing
  - `MMLongBench-Doc`: Long-Context Multimodal Document Benchmark
  - `LongDocURL`: Long-document understanding and retrieval
  - `XL-DocBench`: Cross-page document benchmark
- **Partitions**: Strict `train` / `validation` / `test` splits.
- **Zero-Leakage Invariant**:
  - If clean source document $D_i$ is in partition $P$, all derived degraded variants $D_i^{(v)}$ MUST belong strictly to partition $P$.
  - Clean versions cannot be in `train` if degraded variants are in `test`.
- **Integrity**: Record immutable dataset versions and SHA-256 hashes for all manifests.

## 6. Experiment Record Schema
`experiment_id, timestamp, git_commit, model, model_version, dataset, dataset_version, dataset_split, seed, prompt_version, temperature, top_p, max_tokens, batch_size, hardware, software_environment, configuration, metrics, outputs, status`

## 7. Reporting Standards
Distinguish clearly between:
- OBSERVATION
- INTERPRETATION
- HYPOTHESIS
- CONCLUSION
Do not turn observation into causal claim without supporting experiments.

## 8. Degradation Benchmark Protocol
Controlled variants to generate and test against:
- **Blur**: $\sigma = 0, 1, 2, 4, 6$
- **JPEG Quality**: $100, 80, 50, 25, 10$
- **Noise (Gaussian)**: $\sigma = 0, 5, 15, 30, 50$
- **Rotation / Skew**: $0^\circ, 1^\circ, 3^\circ, 5^\circ, 10^\circ$
- **Brightness / Illumination**: $100\%, 75\%, 50\%, 30\%$
- **Occlusion**: $0\%, 5\%, 10\%, 20\%, 30\%$
- **Resolution Reduction**: $100\%, 75\%, 50\%, 25\%$
- **Perspective Distortion**: Off-axis angles ($0^\circ, 5^\circ, 15^\circ, 25^\circ$)
- **Mixed Degradation**: Composite realistic degradations (e.g., blur + compression + low resolution)

## 9. Literature Registry Requirements
For each relevant paper, record:
`title, authors, year, venue, URL/DOI, research problem, method, dataset, metrics, limitations, relevance, overlap with our contribution`

**Required Topics to Track**:
VLMs, Document Understanding, DocVQA, Long-document reasoning, Evidence grounding, Document hallucination, Uncertainty estimation, Selective prediction, Abstention, Robust document AI, OCR robustness, Multimodal RAG, Spatial grounding, Document degradation.

---

## 10. Operational Sub-Protocols & Artifacts
The frozen methodology is operationalized across detailed sub-protocol documents:
- **Dataset Curation**: [`protocol/dataset_protocol.md`](protocol/dataset_protocol.md)
- **Zero-Leakage Partitioning**: [`protocol/split_protocol.md`](protocol/split_protocol.md)
- **Controlled Degradation Grid**: [`protocol/degradation_protocol.md`](protocol/degradation_protocol.md)
- **Comparative Baselines**: [`protocol/baseline_protocol.md`](protocol/baseline_protocol.md)
- **Mathematical Metrics**: [`protocol/evaluation_protocol.md`](protocol/evaluation_protocol.md)
- **Multi-Signal Uncertainty**: [`protocol/uncertainty_protocol.md`](protocol/uncertainty_protocol.md)
- **Spatial Grounding**: [`protocol/grounding_protocol.md`](protocol/grounding_protocol.md)
- **Statistical Significance**: [`protocol/statistical_protocol.md`](protocol/statistical_protocol.md)
- **Reproducibility Standards**: [`protocol/reproducibility_protocol.md`](protocol/reproducibility_protocol.md)
- **Literature Registry**: [`literature/literature_registry.csv`](literature/literature_registry.csv)
- **Gap Analysis**: [`literature/gap_analysis.md`](literature/gap_analysis.md)
- **Novelty Matrix**: [`literature/novelty_matrix.md`](literature/novelty_matrix.md)
- **Claim Traceability**: [`reports/phase0/claim_traceability.md`](reports/phase0/claim_traceability.md)
- **Risk Register**: [`reports/phase0/risk_register.md`](reports/phase0/risk_register.md)
- **Feasibility Budget**: [`reports/phase0/feasibility_analysis.md`](reports/phase0/feasibility_analysis.md)
- **Phase 0 Final Report**: [`reports/phase0/PHASE0_REPORT.md`](reports/phase0/PHASE0_REPORT.md)
