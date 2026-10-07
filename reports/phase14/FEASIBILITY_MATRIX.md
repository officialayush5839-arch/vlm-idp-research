# Model Feasibility Ladder & Hardware Capacity Matrix (`table_03_model_registry.csv`)

## 1. Feasibility Ladder Architecture

To adhere to the zero-fabrication research mandate, Phase 14 established a strict, hierarchical Model Feasibility Ladder separating the idealized target architecture from the physically executed fallback model:

```
[Level 1: Target Model - Qwen2.5-VL-7B-Instruct]
   |--> Test FP16 physical allocation (16.0 GB) -> OOM -> Recorded as Negative Control
   |--> Test INT8 physical allocation (8.5 GB)  -> Exceeds 6GB physical capacity
   |--> Result: NOT_PHYSICALLY_EXECUTABLE_UNDER_6GB_BUDGET
   |
   V
[Level 2: Fallback Model - SmolVLM-500M-Instruct]
   |--> Test FP16 physical inference -> 1,111 MB -> SUCCESS
   |--> Test INT8 physical inference -> 702 MB   -> SUCCESS
   |--> Test INT4 physical inference -> 531 MB   -> SUCCESS
   |--> Result: PHYSICALLY_EXECUTED_ON_CUDA
```

---

## 2. Model Registry Specification (`table_03_model_registry.csv`)

| Model Tier | Model Name | Parameter Count | Precision Modes Tested | Physical Status on RTX 3050 (6GB) |
| :--- | :--- | :---: | :---: | :--- |
| **Tier 1 (Target)** | `Qwen2.5-VL-7B-Instruct` | 7.6B | FP16, INT8, INT4 | **OOM / NOT_PHYSICALLY_EXECUTABLE** |
| **Tier 2 (Fallback)** | `SmolVLM-500M-Instruct` | 500M | FP16, INT8, INT4 | **PHYSICALLY_EXECUTED_ON_CUDA** |

---

## 3. Methodological Significance

In research publications, reporting physical hardware memory walls and negative controls is essential for reproducibility. Rather than simulating or fabricating 7B execution, Phase 14 demonstrates the exact hardware boundary where 7B inference fails, and shows how sub-billion multimodal models can be leveraged on consumer hardware to validate intelligent document processing pipelines.
