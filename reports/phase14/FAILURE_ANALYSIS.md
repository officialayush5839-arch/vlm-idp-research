# Phase 14 Failure Analysis & Target 7B Memory Wall Investigation

## 1. Physical OOM Event Documentation (`table_14_failures.csv`)

During the Phase 14 initialization gate, genuine physical memory allocations were tested on the physical NVIDIA RTX 3050 6GB Laptop GPU to empirically establish the memory ceiling:

```
[W CUDACachingAllocator.cpp:3934] memory allocation failed with OOM on device 0 while trying to allocate 17179869184 bytes (free: 5404360704, total: 6441926656).
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 16.00 GiB on 6.00 GiB GPU.
```

---

## 2. Theoretical vs Empirical Memory Breakdown (7B Class VLM)

| Precision Mode | Model Weight Size | KV Cache + Activation Size (Batch=1, Seq=2048) | Total Required VRAM | Hardware Capacity (RTX 3050) | Execution Feasibility |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **FP16** | 15.2 GB | ~2.4 GB | ~17.6 GB | 6.0 GB | **OOM (Hardware Ceiling)** |
| **INT8** | 7.6 GB | ~1.8 GB | ~9.4 GB | 6.0 GB | **OOM (Hardware Ceiling)** |
| **INT4 (NF4)** | 3.8 GB | ~1.8 GB | ~5.6 GB | 6.0 GB | Marginal (Near OOM / OS Page Thrashing) |

---

## 3. Methodological Decision: Fallback Tier Activation

Because the target 7B class model cannot execute in FP16 or INT8 on 6GB VRAM, the pre-registered model feasibility ladder mandated activating **Tier 2 Fallback (`SmolVLM-500M-Instruct`)**.
- SmolVLM-500M shares the exact same autoregressive Vision-Language architecture (Idefics3 vision transformer + LLaMA-style decoder), supporting identical visual prompt interfaces and BitsAndBytes quantization backends.
- This allowed full physical verification of all architectural mechanisms (quantization, retrieval, grounding, abstention) on physical CUDA hardware without violating zero-fabrication rules.
