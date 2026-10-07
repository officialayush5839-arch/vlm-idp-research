# Phase 14 Physical Quantization Benchmark Report

## 1. Overview of Precision Modes Evaluated

To assess the practical trade-off between memory footprint and execution speed, we evaluated three distinct precision tiers on the NVIDIA RTX 3050 6GB Laptop GPU using `BitsAndBytesConfig` and native PyTorch CUDA execution:
1. **Q0 (FP16)**: Full half-precision floating point (`torch.float16`).
2. **Q1 (INT8)**: 8-bit vector-wise quantization via BitsAndBytes (`load_in_8bit=True`).
3. **Q2 (INT4)**: NormalFloat-4 (NF4) quantization with FP16 compute dtype (`load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`, `bnb_4bit_compute_dtype=torch.float16`).

---

## 2. Empirical Benchmark Matrix (`table_04_quantization_matrix.csv`)

| Precision Mode | Model Weight Load Time (s) | Peak CUDA VRAM (MB) | Forward Latency (s) | Generation Throughput (tok/s) | Physical Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Q0 (FP16)** | 2.154 s | 1,111.64 MB | 0.863 s | 27.81 tok/s | EXECUTED |
| **Q1 (INT8)** | 3.382 s | 702.01 MB | 2.802 s | 8.57 tok/s | EXECUTED |
| **Q2 (INT4)** | 1.382 s | 530.95 MB | 1.455 s | 16.49 tok/s | EXECUTED |

---

## 3. Analysis & Key Insights

### 3.1 Memory Compression
- Transitioning from FP16 (1,111.64 MB) to INT8 (702.01 MB) reduced physical VRAM footprint by **36.85%** (-409.63 MB).
- Transitioning from FP16 to INT4 NF4 (530.95 MB) reduced physical VRAM footprint by **52.24%** (-580.69 MB).
- The sub-600 MB footprint of INT4 ensures that even on memory-constrained 6GB laptop hardware, multiple pages and large vision embeddings can reside in VRAM simultaneously without risk of paging to system RAM.

### 3.2 Latency and Compute Overhead
- **FP16** achieved the fastest generation speed (0.863s latency, 27.81 tokens/sec), because Ampere Tensor Cores operate natively on dense FP16 matrices without on-the-fly dequantization overhead.
- **INT8** exhibited a latency penalty (2.802s, 8.57 tokens/sec), attributable to outlier-channel vector quantization overhead and kernel dispatch latencies in `bitsandbytes` on Windows.
- **INT4 (NF4)** demonstrated a substantial speedup over INT8 (1.455s vs 2.802s, nearly 2x faster at 16.49 tokens/sec) due to optimized 4-bit packed GEMM kernels.

### 3.3 Loading Time
- INT4 demonstrated the fastest load time (1.382s) because reading 4-bit compressed weights from disk to GPU memory minimizes PCIe and storage bandwidth bottlenecks.
