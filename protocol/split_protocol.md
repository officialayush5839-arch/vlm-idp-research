# Split Protocol — Data Partitioning and Zero-Leakage Invariants

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. The Zero-Leakage Invariant (Mandatory Research Rule)

In experiments involving document image degradation, data leakage is an insidious failure mode: if clean document $D_i$ appears in the training or validation partition, and a degraded variant $\tilde{D}_i$ appears in the test partition, the model can exploit memorized textual content rather than demonstrating true visual robustness under degradation.

> [!CAUTION] Mandatory Zero-Leakage Invariant
> Let $\mathcal{D} = \{D_1, D_2, \dots, D_N\}$ be the set of clean source documents, and let $\mathcal{V}(D_i) = \{D_i^{(v_1)}, D_i^{(v_2)}, \dots\}$ be the family of all corrupted or transformed variants derived from document $D_i$.
> 
> For any partition assignment $\Pi: \mathcal{D} \to \{\text{Train}, \text{Validation}, \text{Test}\}$:
> $$\forall D_i \in \mathcal{D}, \quad \text{if } \Pi(D_i) = \mathcal{P}, \text{ then } \forall \tilde{D} \in \mathcal{V}(D_i), \quad \Pi(\tilde{D}) \equiv \mathcal{P}$$
> 
> Under no circumstances may a clean source document and any of its synthetic or augmented variants belong to different data partitions.

---

## 2. Partition Strategy

For datasets with official public test splits (e.g., DocVQA, FUNSD):
1. **Official Test Partition**: Preserved strictly for final evaluation. If test annotations are held privately by benchmark organizers, the official validation set is split into a **Frozen Validation Set (50%)** for threshold tuning/calibration and a **Held-Out Test Set (50%)** for local evaluation.
2. **Official Training Partition**: Used for model fine-tuning (if applicable) and synthetic corruption training.

For custom long-document or un-split benchmarks (e.g., LongDocURL subsets):
*   **Training Partition**: $70\%$ of unique source documents.
*   **Validation Partition**: $15\%$ of unique source documents (used strictly for calibrating uncertainty parameters and learning routing thresholds).
*   **Test Partition**: $15\%$ of unique source documents (frozen; evaluated only once during Phase 9).

---

## 3. Implementation Specification

1. **Document-Level Grouping**: Splitting is executed at the `document_id` level, never at the `page_id` or `question_id` level. All pages and questions belonging to document $D_i$ inherit the document's partition.
2. **Deterministic Hashing**: Document partition assignment is computed using a deterministic SHA-256 hash of the `document_id` combined with a fixed partition seed:
   ```python
   def assign_partition(document_id: str, seed: int = 42) -> str:
       hash_val = int(hashlib.sha256(f"{document_id}_{seed}".encode()).hexdigest(), 16)
       normalized = (hash_val % 10000) / 10000.0
       if normalized < 0.70:
           return "train"
       elif normalized < 0.85:
           return "val"
       else:
           return "test"
   ```
3. **Partition Manifests**: All partition mappings will be recorded as immutable CSV/JSON files in `data/manifests/` with SHA-256 checksums before any model inference begins.
4. **Audit Script**: An automated unit test in `tests/test_splits.py` will assert that the intersection of document IDs between train, val, and test is strictly empty ($\mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{val}} = \emptyset$, $\mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{test}} = \emptyset$, $\mathcal{D}_{\text{val}} \cap \mathcal{D}_{\text{test}} = \emptyset$).
