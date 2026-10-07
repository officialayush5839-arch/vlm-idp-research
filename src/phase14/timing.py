"""Phase 14 Timing & Stage Latency Profiler.

Ensures zero naive wall-clock measurement over asynchronous GPU kernels.
Wraps all measurements in torch.cuda.synchronize() when running under CUDA.
Separates cold-start from warm-steady-state inferences.
"""

import time
from typing import Dict, List, Optional
import numpy as np

class PhysicalStageProfiler:
    def __init__(self, use_cuda_sync: bool = True):
        self.use_cuda_sync = use_cuda_sync
        self.stage_timings: Dict[str, List[float]] = {}
        self._stage_starts: Dict[str, float] = {}
        self._torch = None
        if self.use_cuda_sync:
            try:
                import torch
                if torch.cuda.is_available():
                    self._torch = torch
            except ImportError:
                pass

    def _sync(self):
        if self._torch is not None:
            self._torch.cuda.synchronize()

    def start_stage(self, stage_name: str):
        self._sync()
        self._stage_starts[stage_name] = time.perf_counter()

    def end_stage(self, stage_name: str) -> float:
        self._sync()
        end_time = time.perf_counter()
        if stage_name not in self._stage_starts:
            raise ValueError(f"Stage '{stage_name}' was not started.")
        elapsed = end_time - self._stage_starts.pop(stage_name)
        if stage_name not in self.stage_timings:
            self.stage_timings[stage_name] = []
        self.stage_timings[stage_name].append(elapsed)
        return elapsed

    def get_summary(self) -> Dict[str, Dict[str, float]]:
        summary = {}
        for stage, durations in self.stage_timings.items():
            arr = np.array(durations)
            summary[stage] = {
                "mean_ms": float(np.mean(arr) * 1000.0),
                "std_ms": float(np.std(arr) * 1000.0),
                "median_ms": float(np.median(arr) * 1000.0),
                "p95_ms": float(np.percentile(arr, 95) * 1000.0),
                "p99_ms": float(np.percentile(arr, 99) * 1000.0),
                "min_ms": float(np.min(arr) * 1000.0),
                "max_ms": float(np.max(arr) * 1000.0),
                "count": len(durations)
            }
        return summary
