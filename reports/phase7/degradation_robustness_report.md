# Evidence Grounding Degradation Robustness Report

## 1. Degradation Analysis
In long documents, degradation (blur, noise, compression, low resolution) distorts OCR characters and layout coordinates.
Across degradation tiers in the test corpus:
- **Clean**: Text and bounding boxes are sharp.
- **Mild**: Minor character distortion; layout structure fully preserved.
- **Moderate**: Noticeable OCR noise; cell separators degraded.
- **Severe**: Significant character omissions; text-only retrieval fails to find keywords.

## 2. Robustness Behavior
1. **Multimodal Resilience**: In severe degradation where lexical keywords are corrupted, B7-5 leverages visual layout and structural region coordinates to maintain evidence localization.
2. **Abstention Integrity**: Under severe corruption where evidence cannot be confirmed, B7-5 safely outputs `INSUFFICIENT_EVIDENCE` or `PARTIALLY_SUPPORTED` rather than hallucinating false grounded confidence.
