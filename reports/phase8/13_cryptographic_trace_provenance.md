# Report 13: Cryptographic Trace Provenance and Collision Avoidance

## 1. Trace Identification Scheme
Every single inference execution in Phase 8 generates a deterministic, unique trace identifier:
$$\text{TraceID} = \texttt{run\_P8\_\{dataset\}\_\{baseline\}\_\{doc\_id\}\_\{query\_id\}\_\{condition\}\_s\{seed\}}$$

Example:
`run_P8_synthetic_multipage_A5_evidence_aware_doc_mp_026_q_doc_mp_026_mild_s42`

## 2. Integrity and Collision Avoidance
1. **Payload Serialization**: Trace outputs are serialized into sorted-key JSON strings and hashed via SHA-256.
2. **Strict Collision Prevention**: If an execution attempts to overwrite an existing trace file with divergent data, `TraceCollisionError` is immediately raised, halting execution and preventing data corruption.
3. **Trace Volume**:
   - 25 test queries $\times$ 6 baselines $\times$ 5 seeds = **750 individual trace files** stored in `experiments/phase8/traces/`.
4. **Model Freeze Verification**:
   All calibration models in `experiments/phase8/models/` are checked against `experiments/phase8/models/manifest.json` before and after test evaluation:
   - `temperature_scaling_calibrator.json`
   - `isotonic_calibrator.json`
   - `evidence_aware_calibrator.json`
   - `abstention_thresholds.json`
   Both pre-benchmark and post-benchmark verification achieved 100% cryptographic match.
