"""Tesseract OCR Integration for VLM-IDP."""

import time
from typing import List, Optional
from PIL import Image

from src.ocr.base import OCRBackend
from src.ocr.schema import OCRResult, OCRLine, OCRWord
from src.ingestion.coordinates import normalize_coordinates


class TesseractBackend(OCRBackend):
    """Tesseract OCR Backend Implementation with Normalized Coordinates."""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config or {})
        self._initialized = False
        self._check_tesseract()

    @property
    def engine_name(self) -> str:
        return "tesseract"

    @property
    def engine_version(self) -> str:
        return "5.3.0"

    def _check_tesseract(self) -> None:
        try:
            import pytesseract
            # Test if tesseract executable is accessible
            _ = pytesseract.get_tesseract_version()
            self._initialized = True
        except (ImportError, Exception):
            self._initialized = False

    def extract(
        self,
        image: Image.Image,
        page_idx: int = 0,
        document_id: str = "doc_unknown"
    ) -> OCRResult:
        start_time = time.perf_counter()
        img_w, img_h = image.size

        if not self._initialized:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return OCRResult(
                document_id=document_id,
                page_idx=page_idx,
                full_text="",
                confidence=1.0,
                lines=[],
                engine=self.engine_name,
                engine_version=self.engine_version,
                latency_ms=round(latency_ms, 2)
            )

        import pytesseract
        data = pytesseract.image_to_data(
            image,
            lang=self.config.get("lang", "eng"),
            output_type=pytesseract.Output.DICT
        )

        n_boxes = len(data["text"])
        lines_dict = {}

        for i in range(n_boxes):
            text = data["text"][i].strip()
            conf = float(data["conf"][i])
            if conf < 0 or not text:
                continue

            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            raw_bbox = [int(x), int(y), int(x + w), int(y + h)]
            norm_bbox = normalize_coordinates(raw_bbox, img_w, img_h)

            line_num = data["line_num"][i]
            if line_num not in lines_dict:
                lines_dict[line_num] = []

            word = OCRWord(
                word_id=f"p{page_idx}_w{i}",
                text=text,
                confidence=round(conf / 100.0, 4),
                raw_bbox=raw_bbox,
                normalized_bbox=norm_bbox
            )
            lines_dict[line_num].append(word)

        lines: List[OCRLine] = []
        total_conf = 0.0
        total_words = 0

        for line_num, words in sorted(lines_dict.items()):
            line_text = " ".join([w.text for w in words])
            line_conf = sum([w.confidence for w in words]) / len(words)
            min_x = min([w.raw_bbox[0] for w in words])
            min_y = min([w.raw_bbox[1] for w in words])
            max_x = max([w.raw_bbox[2] for w in words])
            max_y = max([w.raw_bbox[3] for w in words])
            raw_line_bbox = [min_x, min_y, max_x, max_y]
            norm_line_bbox = normalize_coordinates(raw_line_bbox, img_w, img_h)

            line = OCRLine(
                line_id=f"p{page_idx}_l{line_num}",
                text=line_text,
                confidence=round(line_conf, 4),
                raw_bbox=raw_line_bbox,
                normalized_bbox=norm_line_bbox,
                words=words
            )
            lines.append(line)
            total_conf += sum([w.confidence for w in words])
            total_words += len(words)

        avg_conf = (total_conf / total_words) if total_words > 0 else 1.0
        full_text = "\n".join([line.text for line in lines])
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return OCRResult(
            document_id=document_id,
            page_idx=page_idx,
            full_text=full_text,
            confidence=round(avg_conf, 4),
            lines=lines,
            engine=self.engine_name,
            engine_version=self.engine_version,
            latency_ms=round(latency_ms, 2)
        )
