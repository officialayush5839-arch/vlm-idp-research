# Reproducibility Protocol — Environment, Configuration & Artifact Provenance

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Core Reproducibility Principles

Every empirical claim in the future IEEE paper must be 100% reproducible from:
1. **The Code Repository**: Exact Git commit hash.
2. **The Environment**: Pinned dependencies and virtual environment lockfile.
3. **The Configuration**: Static YAML configuration file.
4. **The Random Seed**: Documented pseudo-random generator state.

---

## 2. Global Seed Policy

To ensure complete computational determinism, all scripts must execute a global seed initialization before loading any model libraries:

```python
def seed_everything(seed: int = 42) -> None:
    import os, random, numpy as np, torch
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
```

---

## 3. Experiment Run Record Schema

Every experiment execution MUST generate an immutable machine-readable record (JSON and Parquet) in `experiments/{module}/runs/run_{experiment_id}.json` conforming to this schema:

```json
{
  "experiment_id": "EXP_ROB_004_QWEN_DEGRADED",
  "timestamp_utc": "2026-10-05T10:14:32Z",
  "git_commit": "e38c12d45a90184b234",
  "git_dirty": false,
  "model": {
    "name": "Qwen2.5-VL-7B-Instruct",
    "version": "transformers-4.49.0",
    "quantization": "4bit-bitsandbytes",
    "device": "cuda:0"
  },
  "dataset": {
    "name": "DocVQA",
    "version": "1.0",
    "split": "test",
    "manifest_sha256": "3a8f10b7..."
  },
  "degradation": {
    "type": "gaussian_blur",
    "severity": 2,
    "parameter": {"sigma": 2.0}
  },
  "configuration": {
    "seed": 42,
    "temperature": 0.0,
    "max_new_tokens": 128,
    "k_retrieval": 5
  },
  "hardware": {
    "gpu_name": "NVIDIA GeForce RTX 3050 Laptop GPU",
    "gpu_vram_total_mb": 6144,
    "cpu_cores": 16,
    "os": "Windows 11"
  },
  "metrics": {
    "em": 0.0,
    "f1": 0.0,
    "anls": 0.0,
    "latency_ms_mean": 0.0,
    "vram_peak_mb": 0.0
  },
  "status": "NOT_RUN"
}
```

---

## 4. Configuration-Driven Architecture

No parameter (retrieval $k$, degradation severity $\sigma$, calibration threshold $\tau$, model temperature $T$) may be hard-coded in Python source code. All parameters are loaded from YAML configuration files located under `configs/`:

```text
configs/
├── models/         # Model architectures, quantization flags, device placement
├── datasets/       # Local paths, split definitions, manifest checksums
├── degradation/    # Parameter grids for 9 corruption families
├── routing/        # Adaptive quality thresholds and routing logic
├── retrieval/      # FAISS index parameters, embedding dimensions, top-k
├── uncertainty/    # Calibrator hyperparameters and decision cutoffs
└── experiments/    # Experiment pipeline configurations
```
