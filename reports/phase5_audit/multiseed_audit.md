# PHASE 5 SCIENTIFIC AUDIT — MULTI-SEED RANDOMIZATION AUDIT

**Audit Item**: Multi-Seed Verification across Seeds $\{42, 123, 456, 789, 101112\}$  
**Audit Status**: VERIFIED PASS  

---

## 1. Audit Target
Section 21 requires verifying whether the five specified seeds:
$$S_5 = \{42, 123, 456, 789, 101112\}$$
represent genuine stochastic experimental variations or merely redundant identical executions.

---

## 2. Empirical Verification of Seed Variance
1. **Degradation Synthesis (`src/benchmark/degradation_runner.py`)**:
   - For stochastic degradation families (e.g., `gaussian_noise`, `occlusion`, `mixed_degradation`), `apply_degradation` feeds `seed` directly to NumPy / OpenCV random generators.
   - **SHA-256 Digest Inspection**:
     - `docvqa_inv_901_deg_gaussian_noise_sev1_seed42.png`: `0731ee4d54c4e5327bc8120b69eb6635f57371a2c820071572218a496bfd2557`
     - `docvqa_inv_901_deg_gaussian_noise_sev1_seed123.png`: `bbb09460751653c86a1ae7d8089d5a2c44ba9c36bb9d831b6bdcb540655ad6c8`
     - The digests are **distinct**, proving non-identical pixel arrays.
2. **Quality Feature Extraction Variance**:
   - The Phase 3 quality feature extractor produced varying numeric measurements across seeds on identical source documents:
     - Seed 42: `noise = 0.3169`
     - Seed 123: `noise = 0.3155`
     - Seed 456: `noise = 0.3163`
     - Seed 789: `noise = 0.3169`
     - Seed 101112: `noise = 0.3180`
3. **Deterministic Degradation Families**:
   - For deterministic transformations (e.g., fixed-angle skew rotation $1^\circ, 3^\circ, 5^\circ, 10^\circ$, or fixed JPEG quality tiers $80, 50, 25, 10$), the image transformation is naturally deterministic, and the seed has no stochastic role. This matches standard vision benchmark methodology.
4. **Model Decoding Control**:
   - Per `protocol/evaluation_protocol.md`, all models operate under greedy decoding ($T = 0.0$) to guarantee reproducibility.

## 3. Verdict
**STATUS: PASS**. Multi-seed execution genuinely perturbs stochastic corruptions, alters physical pixel arrays, and produces measurable variance in visual quality metrics across trials.
