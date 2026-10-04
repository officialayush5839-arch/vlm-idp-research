"""Output Parser for Unlimited-OCR Raw Generation."""

import re
from typing import List, Tuple, Optional, Dict
from src.baselines.unlimited_ocr.schemas import UnlimitedOCRElement, UnlimitedOCRParsedOutput
from src.ingestion.coordinates import denormalize_coordinates


class UnlimitedOCRParser:
    """Parses raw Unlimited-OCR outputs into structured layout elements and text."""

    GROUNDING_REGEX = re.compile(
        r"(?P<type>[a-zA-Z_\-]+)\s*\[(?P<x1>\d+),\s*(?P<y1>\d+),\s*(?P<x2>\d+),\s*(?P<y2>\d+)\](?P<text>.*)"
    )

    def __init__(self, target_space: Tuple[int, int] = (0, 1000)):
        self.min_val, self.max_val = target_space

    def parse(
        self,
        raw_text: str,
        page_width: Optional[int] = None,
        page_height: Optional[int] = None
    ) -> UnlimitedOCRParsedOutput:
        """
        Parses raw text. If spatial grounding tags exist, extracts elements and bboxes.
        Validates normalized coordinates against [0, 1000].
        Computes pixel-space raw_bbox if page dimensions are supplied.
        """
        if not raw_text or not raw_text.strip():
            return UnlimitedOCRParsedOutput(
                elements=[],
                full_transcription="",
                detected_element_counts={},
                has_spatial_grounding=False
            )

        lines = raw_text.strip().splitlines()
        elements: List[UnlimitedOCRElement] = []
        counts: Dict[str, int] = {}
        text_lines: List[str] = []

        for idx, line in enumerate(lines):
            line_str = line.strip()
            if not line_str:
                continue

            match = self.GROUNDING_REGEX.match(line_str)
            if match:
                el_type = match.group("type").lower()
                x1 = int(match.group("x1"))
                y1 = int(match.group("y1"))
                x2 = int(match.group("x2"))
                y2 = int(match.group("y2"))
                content = match.group("text").strip()

                # Validate [0, 1000] boundaries
                is_valid = (
                    self.min_val <= x1 <= self.max_val and
                    self.min_val <= y1 <= self.max_val and
                    self.min_val <= x2 <= self.max_val and
                    self.min_val <= y2 <= self.max_val and
                    x1 <= x2 and y1 <= y2
                )

                if is_valid:
                    norm_bbox = [x1, y1, x2, y2]
                    raw_bbox = None
                    if page_width and page_height and page_width > 0 and page_height > 0:
                        raw_bbox = [
                            int(round(coord))
                            for coord in denormalize_coordinates(norm_bbox, page_width, page_height)
                        ]

                    elem = UnlimitedOCRElement(
                        element_id=f"el_{idx:04d}",
                        element_type=el_type,
                        text=content,
                        normalized_bbox=norm_bbox,
                        raw_bbox=raw_bbox,
                        confidence=1.0  # Deterministic generation token match
                    )
                    elements.append(elem)
                    counts[el_type] = counts.get(el_type, 0) + 1
                    text_lines.append(content)
                else:
                    # Inverted or out of bounds coordinates
                    text_lines.append(content or line_str)
            else:
                # Line without grounding tags
                text_lines.append(line_str)

        has_grounding = len(elements) > 0
        full_text = "\n".join(text_lines)

        return UnlimitedOCRParsedOutput(
            elements=elements,
            full_transcription=full_text,
            detected_element_counts=counts,
            has_spatial_grounding=has_grounding
        )
