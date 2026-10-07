# Phase 14 Physical GPU Memory & VRAM Profile Report

## 1. Memory Measurement Methodology

GPU memory was sampled directly via PyTorch CUDA memory management APIs:
- `torch.cuda.memory_allocated()`: Actual device tensors allocated by the PyTorch process.
- `torch.cuda.memory_reserved()`: Total memory held by the PyTorch caching allocator.
- `torch.cuda.max_memory_allocated()`: Peak memory watermark reached during execution.

## 2. Memory by Precision Level (`table_05_memory.csv`)

| Precision | Peak VRAM Allocated (MB) | Physical GPU Capacity Fraction | Headroom Available (MB) |
| :--- | :---: | :---: | :---: |
| **Q0 (FP16)** | 1,111.64 MB | 18.09% | 5,032.36 MB |
| **Q1 (INT8)** | 702.01 MB | 11.43% | 5,441.99 MB |
| **Q2 (INT4)** | 530.95 MB | 8.64% | 5,613.05 MB |

## 3. Windows WDDM Virtual Memory Considerations

Under Windows 11, the Windows Display Driver Model (WDDM) allows GPU processes to commit virtual allocations beyond dedicated VRAM by paging to system RAM over the PCIe bus. 
However:
1. Allocating a 16 GB tensor on a 6 GB device causes an immediate hardware-level failure (`torch.OutOfMemoryError`).
2. Paging across PCIe causes extreme throughput degradation (orders of magnitude drop in memory bandwidth).
3. The INT4 footprint of **530.95 MB** ensures 100% on-die GDDR6 residence with zero host RAM paging.
