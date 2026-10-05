# Report 14: Zero-Leakage Verification and Static AST Code Audit

## 1. Information Boundary Policy
In accordance with the frozen research protocol, runtime uncertainty estimation must operate exclusively on signals observable at inference time.
Forbidden inputs at runtime include:
- Ground-truth answers or labels
- Gold bounding boxes and page locations
- Benchmark degradation labels (family, severity level)
- Downstream accuracy or evaluation metrics

## 2. Static AST Audit Execution
The automated Abstract Syntax Tree (AST) checker (`src/uncertainty/audit.py`) was executed across all production modules in `src/uncertainty/`:
- `schema.py`
- `signals.py`
- `features.py`
- `temperature.py`
- `isotonic.py`
- `calibration.py`
- `abstention.py`
- `selective.py`
- `metrics.py`
- `provenance.py`
- `baselines.py`
- `pipeline.py`

### Audit Results:
- **Files Checked**: 12
- **Forbidden AST Nodes Detected**: 0
- **Forbidden Attribute Accesses Detected**: 0
- **Partition Integrity Violations**: 0
- **Audit Status**: **PASS**

## 3. Partition Separation Guarantee
1. Calibrator fitting and threshold selection were strictly confined to `split == "val"`.
2. `CalibrationManager.export_artifact` enforces runtime exception if `training_partition == "test"`.
3. The test set (`split == "test"`) was evaluated purely in read-only inference mode using frozen artifacts.
