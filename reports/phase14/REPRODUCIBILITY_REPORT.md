# Phase 14 Reproducibility & Provenance Report

## 1. Reproducibility Manifest (`table_15_reproducibility.csv`)

| Verification Check | Target / Artifact | Result | Status |
| :--- | :--- | :---: | :---: |
| **Historical Immutability Audit** | `frozen_phase13_sha256_manifest.json` | 22,162 files verified, 0 mutations | **PASS** |
| **Execution Traces Generated** | `physical_inference_traces.jsonl` | 1,100 records generated | **PASS** |
| **Random Seeds Evaluated** | Seeds: 42, 123, 456, 789, 101112 | 5 independent seeds executed | **PASS** |
| **Physical Hardware Telemetry** | NVIDIA RTX 3050 6GB Laptop GPU | Monitored via native CUDA APIs | **PASS** |
| **Quantization Backends** | BitsAndBytes NF4 / LLM.int8() | Native Windows CUDA kernels verified | **PASS** |

---

## 2. Environment Locks

- Environment Lockfile: `experiments/phase14/environment/environment_lock.txt`
- Requirements: `requirements_phase14.txt`
- Package Versions: `experiments/phase14/environment/package_versions.json`
- Python Executable: `.venv_phase14/Scripts/python.exe` (Python 3.14.6)
- PyTorch CUDA: `torch==2.14.1+cu126`

---

## 3. Seed Determinism Protocol

All evaluation passes set explicit pseudorandom seeds:
- Model decoding: Greedy deterministic (`do_sample=False`, `temperature=0.0`).
- Bootstrap sampling: Seeded NumPy random generators (`RandomState(seed)`).
- Document and query ordering: Preserved identically via `experiments/phase14/test_manifest.json`.
