# Phase 7 Reproducibility Audit Report

## 1. Environment & Hardware Specifications
- **Operating System**: Microsoft Windows 11 Home
- **Python**: 3.14.6
- **PyTorch**: 2.14.1+cpu
- **Seed Control**: Explicit seeds [42, 123, 456, 789, 101112] fixed across all runs.
- **Git Commit**: `afdd599` (frozen base) + Phase 7 additions.

## 2. Reproduction Steps
```bash
# 1. Activate environment
.\.venv\Scripts\Activate.ps1

# 2. Run unit and integration tests
pytest -k phase7

# 3. Run smoke test
python scripts/run_phase7_smoke.py

# 4. Run validation sweep
python scripts/run_phase7_validation.py

# 5. Run full benchmark and bootstrap testing
python scripts/run_phase7_benchmark.py

# 6. Run ablations
python scripts/run_phase7_ablations.py
```

## 3. Provenance Verification
Every artifact generated in `experiments/phase7/` contains cryptographic SHA-256 hashes matching source document data and code state.
