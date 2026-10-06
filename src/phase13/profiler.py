"""Phase 13 Systems Profiler & Latency/VRAM Breakdown Engine.

Provides:
1. Stage-by-stage latency decomposition:
   - document_loading
   - preprocessing
   - retrieval
   - evidence_extraction
   - vlm_inference
   - evidence_verification
   - reliability_decision
2. CUDA synchronization and VRAM telemetry when available:
   - torch.cuda.synchronize()
   - torch.cuda.max_memory_allocated()
3. Clear status marking for gated environments.
"""

import time
from typing import Dict, List, Any, Optional

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


class SystemsProfiler:
    """Accurately records multi-stage pipeline latency and VRAM telemetry."""

    def __init__(self, use_cuda_sync: bool = False):
        self.use_cuda_sync = use_cuda_sync and HAS_TORCH and torch.cuda.is_available()
        self.stage_times: Dict[str, float] = {}
        self.current_stage: Optional[str] = None
        self._stage_start: float = 0.0

    def start_stage(self, stage_name: str) -> None:
        """Starts timing a specific pipeline stage."""
        if self.use_cuda_sync:
            torch.cuda.synchronize()
        self.current_stage = stage_name
        self._stage_start = time.perf_counter()

    def end_stage(self, stage_name: str) -> float:
        """Ends timing the stage and records elapsed milliseconds."""
        if self.use_cuda_sync:
            torch.cuda.synchronize()
        elapsed_ms = (time.perf_counter() - self._stage_start) * 1000.0
        self.stage_times[stage_name] = elapsed_ms
        self.current_stage = None
        return elapsed_ms

    def get_peak_vram_mib(self) -> Optional[float]:
        """Queries peak allocated VRAM if running on CUDA."""
        if self.use_cuda_sync and torch.cuda.is_available():
            return torch.cuda.max_memory_allocated() / (1024.0 * 1024.0)
        return None

    def get_summary(self) -> Dict[str, Any]:
        """Returns the full decomposition dictionary."""
        total_latency = sum(self.stage_times.values())
        return {
            "stage_latencies_ms": self.stage_times.copy(),
            "total_latency_ms": total_latency,
            "peak_vram_mib": self.get_peak_vram_mib(),
            "cuda_synchronized": self.use_cuda_sync
        }
