# STATISTICAL POWER ANALYSIS & SAMPLE CLUSTERING

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 12 — Authentic Real-World Document Benchmark & Degradation Generalization  
**Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE (Cluster-Aware Resampling Specified)

---

## 1. Problem Formulation & Unit of Independence

In historical phases (Phases 10–11), sample counts were artificially inflated by bootstrapping over 625–875 runs that repeatedly re-evaluated the same 25 documents across 5 random seeds. 

In Phase 12, statistical modeling enforces **explicit multi-level clustering**:

$$\text{Seed} \ll \text{Page} \ll \text{Document Instance} \ll \mathbf{\text{Document Family}}$$

The true independent experimental unit is the **Document Family** ($N_{\text{family}} = 52$).

---

## 2. Statistical Power Analysis

For paired cluster-robust bootstrap comparisons with $\alpha = 0.05$ and target power $1 - \beta = 0.80$:
- **Test Set Cluster Count:** $K = 11$ independent document families (comprising 55 documents, 275 pages, and 55 evaluation queries evaluated across 5 seeds = 275 test runs per baseline).
- **Detectable Effect Size:**
  - With $K = 11$ clusters, the minimum detectable effect size is Cohen's $d \approx 0.62$ (medium-to-large effect size).
  - While this is a dramatic improvement over Phase 10's $N=5$ per domain, statistical tests must acknowledge that subtle effects ($d < 0.3$) will lack power at the family level.
- **Resampling Protocol:** Resampling iterations ($B = 10,000$) resample **entire document families with replacement** (Cluster Bootstrap) rather than individual queries or pages, preserving intra-family correlation structures.

---

## 3. Multiple Comparison Control

When testing multiple hypotheses ($H_{12}\text{-1}$ through $H_{12}\text{-5}$) across 7 modalities:
- Significance thresholds are adjusted using the **Holm-Bonferroni step-down procedure** to strictly control the Family-Wise Error Rate (FWER) at $\alpha = 0.05$.
- Unadjusted $p$-values will never be reported in isolation.
