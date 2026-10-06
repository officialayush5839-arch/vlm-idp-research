# DATASET & SYNTHETIC DEGRADATION AUDIT

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Audit Scope:** Data Scale, Image Sources, Synthetic vs. Real Degradation, and Artifact Fidelity  
**Audit Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE (CRITICAL DEFICIENCY IDENTIFIED: Fixture-Heavy Semi-Synthetic Corpus)

---

## 1. Physical Dataset Inventory & Provenance

A forensic inspection of the physical filesystem (`data/` and `experiments/phase6/indexes/`) reveals the following actual data footprint:

| Directory | Declared Purpose | Actual Files on Disk | Real Document Images | Synthetic / JSON Fixtures | Audit Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `data/raw/` | Ground-truth benchmark images | 4 PNG files (`docvqa_inv_901.png`, `funsd_form_042.png`, `mmlongbench_p0.png`, `sroie_receipt_882.png`) | 4 images | 0 | **EXTREMELY SMALL FOOTPRINT**: Only 4 distinct real source images exist on disk. |
| `data/degraded/` | Synthetic degradation image store | Empty (`.gitkeep`) | 0 | 0 | **EPHEMERAL GENERATION**: Degraded images generated in-memory or in experiment-specific subfolders. |
| `data/splits/` | Split definitions | `dataset_splits.json` | 0 | 1 JSON file referencing 4 documents | **CONFIRMED**: All 4 raw documents assigned to test set. |
| `experiments/phase6/indexes/` | Multi-page corpus index | 50 JSON files (`doc_mp_001.json` to `doc_mp_050.json`) + manifest | 0 physical PDFs | 50 JSON index fixtures with structured metadata | **SYNTHETIC FIXTURE INDEX**: Documents are represented as structured JSON descriptors with `image_path: null`. |

---

## 2. Real vs. Synthetic Proportions

- **Physical Document Images:** Exactly **4 real single-page document images** exist in the repository root.
- **Multi-page Document Corpus:** The 50 multi-page documents (`doc_mp_001` through `doc_mp_050`) utilized throughout Phases 6, 7, 8, 9, 10, 10.5, and 11 are **synthetic JSON fixtures** representing multi-page structures (text snippets, bounding boxes, simulated quality scores, degradation tags) rather than digitized high-resolution multi-page PDF scans.
- **Empirical Ratio:** Real images comprise **<1%** of total evaluation tokens; synthetic/simulated index entries comprise **>99%**.

---

## 3. Physical Plausibility of Synthetic Degradation Models

The repository defines 9 synthetic degradation families (`src/degradation/`):
1. **Gaussian Blur:** Standard kernel convolution ($\sigma \in \{1, 2, 4, 6\}$).
2. **Motion Blur:** Linear kernel convolution at fixed angles.
3. **Gaussian Noise:** Additive zero-mean Gaussian perturbation ($\sigma \in \{5, 15, 30, 50\}$).
4. **JPEG Compression:** Standard DCT quantization (Quality $\in \{80, 50, 25, 10\}$).
5. **Geometric Skew / Rotation:** Planar affine rotations ($\theta \in \{1^\circ, 3^\circ, 5^\circ, 10^\circ\}$).
6. **Illumination Non-Uniformity:** Radial vignette/gradient multiplier.
7. **Occlusion:** Rectangular synthetic black mask overlays ($5\% - 30\%$).
8. **Downsampling / Low-Resolution:** Bilinear downsampling ($75\%, 50\%, 25\%$).
9. **Perspective Distortion:** 4-point projective homography.

### Physical Fidelity Assessment:
- **Plausibility:** **MODERATE (Standard Computer Vision Benchmark Practice)**.
- **Gap to Real-World Physical Scans:**
  - Real document degradation features non-uniform ink bleed, paper bleed-through, scanner glass scratches, stapler punch-holes, physical crumpled paper shadows, curved text along book bindings, and multi-exposure mobile phone flares.
  - The synthetic models apply uniform global transforms that fail to model local camera lens aberrations, non-planar page curvature, or complex lighting reflections.

---

## 4. Assessment Summary & Major Scientific Implication

> **Major Finding:**  
> The current experimental results demonstrate *algorithmic soundness and pipeline logic* under formal mathematical simulations of document noise. However, because downstream phases evaluate over 50 structured JSON fixture documents rather than hundreds of real-world scanned documents, **the empirical performance cannot yet claim robustness on real-world unconstrained physical document archives**.  
> The primary scientific next step must involve **corpus scaling and authentic scanned document integration**.
