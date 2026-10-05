# Phase 8 Uncertainty Information Boundary Report

## 1. Information Boundary Principles
To guarantee zero data leakage and preserve IEEE research validity, all features processed during Phase 8 are classified into four mutually exclusive categories:
1. `OBSERVABLE_AT_INFERENCE`: Legitimately available at runtime without oracle knowledge.
2. `CALIBRATION_ONLY`: Available during offline model fitting on the validation split.
3. `GROUND_TRUTH_ONLY`: Evaluation labels used solely for computing post-hoc metrics.
4. `FORBIDDEN`: Never permitted to enter the runtime pipeline or influence decisions.

## 2. Feature Classification Matrix

| Feature | Source | Available at inference? | Allowed at Runtime? | Reason |
| :--- | :--- | :---: | :---: | :--- |
| `model_confidence` | VLM / OCR | Yes | **YES** | Observable generation confidence score |
| `retrieval_margin` | Phase 6 | Yes | **YES** | Observable score difference between top-1 and top-2 candidates |
| `retrieval_entropy` | Phase 6 | Yes | **YES** | Observable dispersion of candidate retrieval scores |
| `semantic_support_score` | Phase 7 | Yes | **YES** | Observable lexical/entity overlap between answer and evidence snippet |
| `entity_coverage` | Phase 7 | Yes | **YES** | Observable fraction of query tokens found in retrieved evidence |
| `spatial_valid` | Phase 7 | Yes | **YES** | Geometric non-degeneracy of candidate bounding boxes in $[0, 1000]$ |
| `sufficiency_status` | Phase 7 | Yes | **YES** | Observable classification of query requirement satisfaction |
| `grounding_status` | Phase 7 | Yes | **YES** | Synthesized output from evidence grounding pipeline |
| `citation_count` | Phase 7 | Yes | **YES** | Number of verifiable citations emitted |
| `visual_quality_score` | Phase 3 | Yes | **YES** | Image quality score computed directly from input pixels |
| `blur`, `noise`, `skew` | Phase 3 | Yes | **YES** | Observable image degradation feature measurements |
| `page_count` | Ingestion | Yes | **YES** | Total number of pages in the input document |
| `gold_answer` | Dataset | No | **FORBIDDEN** | Oracle ground-truth answer text |
| `gold_evidence_pages` | Dataset | No | **FORBIDDEN** | Oracle page labels |
| `gold_evidence_bboxes` | Dataset | No | **FORBIDDEN** | Oracle spatial annotation coordinates |
| `degradation_family` | Benchmark | No | **FORBIDDEN** | Synthetic metadata label (blur, noise, etc.) |
| `degradation_severity` | Benchmark | No | **FORBIDDEN** | Synthetic severity index (0..4) |
| `oracle_correctness` | Evaluator | No | **GROUND_TRUTH_ONLY** | Binary indicator $y \in \{0, 1\}$ used solely for computing ECE/AURC |
