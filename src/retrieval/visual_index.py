"""
Visual Representation and Retrieval Module.
Extracts spatial layout and multi-scale image visual feature descriptors to rank
pages by visual similarity or cross-modal layout relevance.
"""

from typing import List, Dict, Any, Optional
import os
import numpy as np
from PIL import Image
from src.retrieval.schema import DocumentPageRecord, PageRetrievalResult


def extract_image_features(image_path: str, target_size=(256, 256)) -> np.ndarray:
    """
    Extract multi-scale spatial grid color and gradient histogram descriptors.
    """
    if not os.path.exists(image_path):
        return np.zeros(128, dtype=float)

    try:
        with Image.open(image_path) as img:
            img = img.convert("L").resize(target_size)
            arr = np.asarray(img, dtype=float) / 255.0

        # Spatial pyramid: 1x1, 2x2, 4x4 grid cells
        descriptors = []
        # Mean intensity and std for whole image
        descriptors.extend([np.mean(arr), np.std(arr)])

        # 2x2 grid
        h, w = arr.shape
        for r in range(2):
            for c in range(2):
                cell = arr[r * (h // 2):(r + 1) * (h // 2), c * (w // 2):(c + 1) * (w // 2)]
                descriptors.extend([np.mean(cell), np.std(cell)])

        # 4x4 grid
        for r in range(4):
            for c in range(4):
                cell = arr[r * (h // 4):(r + 1) * (h // 4), c * (w // 4):(c + 1) * (w // 4)]
                descriptors.extend([np.mean(cell), np.std(cell)])

        # 16-bin intensity histogram
        hist, _ = np.histogram(arr, bins=16, range=(0.0, 1.0))
        hist = hist.astype(float) / (hist.sum() + 1e-6)
        descriptors.extend(hist.tolist())

        # Pad or truncate to 128 dimensions
        vec = np.zeros(128, dtype=float)
        length = min(len(descriptors), 128)
        vec[:length] = descriptors[:length]

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec
    except Exception:
        return np.zeros(128, dtype=float)


def extract_layout_features(page: DocumentPageRecord) -> np.ndarray:
    """
    Synthesize visual layout descriptor from page regions (spatial bounding boxes and region types).
    Provides robust fallback when raw image tensors are not on disk.
    """
    vec = np.zeros(128, dtype=float)
    if not page.regions:
        # Default placeholder based on page text length and quality
        vec[0] = min(1.0, len(page.clean_text) / 2000.0)
        vec[1] = page.quality_score
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    # Type counts
    type_map = {"text": 0, "table": 1, "figure": 2, "form": 3, "header": 4, "footer": 5, "mixed": 6}
    type_counts = np.zeros(7, dtype=float)
    areas = []
    y_centers = []

    for reg in page.regions:
        t_idx = type_map.get(reg.region_type, 6)
        type_counts[t_idx] += 1
        xmin, ymin, xmax, ymax = reg.bbox
        area = ((xmax - xmin) * (ymax - ymin)) / 1_000_000.0
        areas.append(area)
        y_centers.append((ymin + ymax) / 2000.0)

    # Normalize type counts
    type_counts /= (len(page.regions) + 1e-6)
    vec[:7] = type_counts
    vec[7] = np.mean(areas) if areas else 0.0
    vec[8] = np.std(areas) if areas else 0.0
    vec[9] = np.mean(y_centers) if y_centers else 0.0
    vec[10] = page.quality_score

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


class VisualRetriever:
    """
    Visual index ranking document pages by visual feature or layout similarity.
    """
    def __init__(self):
        self.pages: List[DocumentPageRecord] = []
        self.page_embeddings: Optional[np.ndarray] = None

    def build(self, pages: List[DocumentPageRecord]) -> None:
        """
        Extract visual or layout features for all pages and store normalized embedding matrix.
        """
        self.pages = list(pages)
        if not self.pages:
            self.page_embeddings = None
            return

        embeddings = []
        for p in self.pages:
            if p.image_path and os.path.exists(p.image_path):
                v = extract_image_features(p.image_path)
            else:
                v = extract_layout_features(p)
            embeddings.append(v)

        mat = np.array(embeddings, dtype=float)
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.page_embeddings = mat / norms

    def search_by_vector(self, query_vec: np.ndarray, top_k: int = 5) -> List[PageRetrievalResult]:
        """
        Search pages using a normalized visual query vector.
        """
        if not self.pages or self.page_embeddings is None:
            return []

        q_norm = np.linalg.norm(query_vec)
        if q_norm > 0:
            query_vec = query_vec / q_norm

        sims = (self.page_embeddings @ query_vec.T).flatten()
        ranked_indices = np.argsort(-sims)[:min(top_k, len(self.pages))]

        results = []
        for rank, idx in enumerate(ranked_indices, start=1):
            p = self.pages[idx]
            sim = float(sims[idx])
            norm_score = max(0.0, sim)
            results.append(
                PageRetrievalResult(
                    page_number=p.page_number,
                    score=float(round(norm_score, 6)),
                    text_score=0.0,
                    visual_score=float(round(norm_score, 6)),
                    rank=rank,
                    metadata={"document_id": p.document_id, "method": "visual_layout"}
                )
            )
        return results

    def search_by_text_concept(self, query_text: str, top_k: int = 5) -> List[PageRetrievalResult]:
        """
        Cross-modal query mapping: map keywords like 'chart', 'table', 'logo', 'receipt'
        into layout expectation vector.
        """
        concept_vec = np.zeros(128, dtype=float)
        q_lower = query_text.lower()
        if "table" in q_lower or "grid" in q_lower or "row" in q_lower:
            concept_vec[1] = 1.0  # table feature position
        if "figure" in q_lower or "chart" in q_lower or "graph" in q_lower or "plot" in q_lower:
            concept_vec[2] = 1.0  # figure feature position
        if "form" in q_lower or "signature" in q_lower:
            concept_vec[3] = 1.0
        if "header" in q_lower or "title" in q_lower:
            concept_vec[4] = 1.0

        if np.linalg.norm(concept_vec) == 0:
            concept_vec[0] = 1.0  # default general layout

        return self.search_by_vector(concept_vec, top_k=top_k)
