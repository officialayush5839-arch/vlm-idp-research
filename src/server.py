"""Full-Stack Web & API Server for VLM-IDP Research.

Serves:
1. Interactive Document Extraction Studio & 3D Frontend Showcase (docs/index.html & assets/)
2. REST API for:
   - Multipart File Upload & Document Management (POST /api/upload)
   - Dynamic Page Image Rendering (GET /api/document/{id}/page/{page})
   - Real Pipeline Inference & Grounding (POST /api/pipeline/infer)
   - Model Capability & Hardware Gating (GET /api/models/capability)
   - Hardware Health & Research Metrics (GET /api/health, GET /api/metrics)
Default Port: 8896
"""

import os
import sys
import json
import re
import mimetypes
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = PROJECT_ROOT / "assets"

from src.runtime.upload_manager import UploadManager, UploadValidationError
from src.runtime.document_adapter import DocumentAdapter, DocumentAdapterError
from src.runtime.model_registry import ModelRegistry, ModelSelectionError
from src.runtime.orchestrator import PipelineOrchestrator

# Global singletons for runtime management
_upload_manager = UploadManager()
_document_adapter = DocumentAdapter()
_model_registry = ModelRegistry()
_orchestrator = PipelineOrchestrator(
    upload_manager=_upload_manager,
    document_adapter=_document_adapter,
    model_registry=_model_registry,
)


def get_hardware_status():
    """Inspects hardware status using ModelRegistry / Phase 14 hardware gate."""
    return _model_registry.get_hardware_status()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread for concurrent serving."""
    daemon_threads = True


class VLMIDPRequestHandler(BaseHTTPRequestHandler):
    """Custom request handler serving static 3D UI, Document Studio, and REST API."""

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_path = self.path.split("?")[0]

        # 1. API Health & Metrics
        if parsed_path == "/api/health":
            self._handle_api_health()
            return
        elif parsed_path == "/api/metrics":
            self._handle_api_metrics()
            return
        elif parsed_path == "/api/models/capability":
            self._handle_api_models_capability()
            return

        # 2. Document Page Image Endpoint: /api/document/{upload_id}/page/{page_num}
        doc_page_match = re.match(r"^/api/document/([a-zA-Z0-9_-]+)/page/(\d+)$", parsed_path)
        if doc_page_match:
            upload_id = doc_page_match.group(1)
            page_num = int(doc_page_match.group(2))
            self._handle_api_document_page(upload_id, page_num)
            return

        # 404 for unknown /api/ routes
        if parsed_path.startswith("/api/"):
            self._send_json({"error": "Endpoint not found"}, status=404)
            return

        # Static File Routes
        self._handle_static_file(parsed_path)

    def do_POST(self):
        parsed_path = self.path.split("?")[0]
        content_type_header = self.headers.get("Content-Type", "")

        # 1. Multipart Upload Endpoint: POST /api/upload
        if parsed_path == "/api/upload":
            self._handle_api_upload(content_type_header)
            return

        # 2. JSON Body Endpoints
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON in request body"}, status=400)
            return

        if parsed_path == "/api/pipeline/infer":
            self._handle_pipeline_infer(payload)
        elif parsed_path == "/api/quality/assess":
            self._handle_quality_assess(payload)
        else:
            self._send_json({"error": "API route not found"}, status=404)

    # =========================================================================
    # MULTIPART UPLOAD PARSER & HANDLER
    # =========================================================================

    def _handle_api_upload(self, content_type_header: str):
        if "multipart/form-data" not in content_type_header:
            self._send_json({"error": "Expected multipart/form-data content type"}, status=400)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            self._send_json({"error": "Empty upload request body"}, status=400)
            return

        raw_body = self.rfile.read(content_length)

        # Extract boundary
        boundary_match = re.search(r'boundary=([^;]+)', content_type_header)
        if not boundary_match:
            self._send_json({"error": "Missing boundary in multipart request"}, status=400)
            return

        boundary = boundary_match.group(1).strip().strip('"').encode("utf-8")
        parts = raw_body.split(b"--" + boundary)

        file_bytes: Optional[bytes] = None
        orig_filename: Optional[str] = None
        part_mime: Optional[str] = None

        for part in parts:
            if b"Content-Disposition:" not in part:
                continue

            # Split header and body
            header_end = part.find(b"\r\n\r\n")
            if header_end == -1:
                continue

            header_bytes = part[:header_end]
            body_bytes = part[header_end + 4:].rstrip(b"\r\n")

            header_str = header_bytes.decode("utf-8", errors="replace")

            # Look for file part
            file_match = re.search(r'Content-Disposition:[^;]+;[^\r\n]*name=["\']file["\'];[^\r\n]*filename=["\']([^"\']+)["\']', header_str, re.IGNORECASE)
            if not file_match:
                # Alternate pattern where filename comes before name or without quotes
                file_match = re.search(r'filename=["\']([^"\']+)["\']', header_str, re.IGNORECASE)

            if file_match:
                orig_filename = file_match.group(1)
                file_bytes = body_bytes
                mime_match = re.search(r'Content-Type:\s*([^\r\n]+)', header_str, re.IGNORECASE)
                if mime_match:
                    part_mime = mime_match.group(1).strip()
                break

        if file_bytes is None or orig_filename is None:
            self._send_json({"error": "No file field found in multipart form data"}, status=400)
            return

        try:
            record = _upload_manager.save_upload(
                raw_bytes=file_bytes,
                filename=orig_filename,
                content_type=part_mime
            )
            doc_meta = _document_adapter.inspect_document(Path(record.file_path))

            response = {
                "status": "accepted",
                "upload_id": record.upload_id,
                "filename": record.original_filename,
                "sanitized_filename": record.sanitized_filename,
                "extension": record.extension,
                "content_type": record.content_type,
                "size_bytes": record.size_bytes,
                "page_count": doc_meta.page_count,
                "is_pdf": doc_meta.is_pdf,
                "dimensions_per_page": doc_meta.dimensions_per_page,
                "preview_url": f"/api/document/{record.upload_id}/page/1"
            }
            self._send_json(response, status=200)

        except UploadValidationError as e:
            self._send_json({"error": str(e), "error_type": "VALIDATION_ERROR"}, status=400)
        except DocumentAdapterError as e:
            self._send_json({"error": str(e), "error_type": "DOCUMENT_ADAPTER_ERROR"}, status=422)
        except Exception as e:
            self._send_json({"error": f"Internal upload error: {str(e)}"}, status=500)

    # =========================================================================
    # DOCUMENT PAGE RENDERING HANDLER
    # =========================================================================

    def _handle_api_document_page(self, upload_id: str, page_num: int):
        record = _upload_manager.get_upload(upload_id)
        if not record:
            self._send_json({"error": f"Document '{upload_id}' not found."}, status=404)
            return

        try:
            page_png_bytes = _document_adapter.render_page_to_bytes(
                file_path=Path(record.file_path),
                page_num=page_num,
                format="PNG"
            )
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(page_png_bytes)))
            self.send_header("Cache-Control", "public, max-age=600")
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(page_png_bytes)
        except DocumentAdapterError as e:
            self._send_json({"error": str(e)}, status=400)
        except Exception as e:
            self._send_json({"error": f"Rendering error: {str(e)}"}, status=500)

    # =========================================================================
    # MODEL CAPABILITY HANDLER
    # =========================================================================

    def _handle_api_models_capability(self):
        matrix = _model_registry.get_capability_matrix()
        hw = _model_registry.get_hardware_status()
        self._send_json({
            "hardware": hw,
            "models": {k: v.to_dict() for k, v in matrix.items()}
        })

    # =========================================================================
    # INFERENCE HANDLER
    # =========================================================================

    def _handle_pipeline_infer(self, payload: Dict[str, Any]):
        upload_id = payload.get("upload_id")
        question = payload.get("question") or payload.get("query", "What is the total amount?")
        page_num = int(payload.get("page_num", 1))
        model_id = payload.get("model_id", "smolvlm-500m")

        # 1. Real Upload Inference Flow
        if upload_id:
            try:
                res = _orchestrator.process_document(
                    upload_id=upload_id,
                    question=question,
                    page_num=page_num,
                    model_id=model_id,
                    options=payload.get("options")
                )
                self._send_json(res.to_dict(), status=200)
            except ModelSelectionError as e:
                self._send_json({"error": str(e), "error_type": "MODEL_UNAVAILABLE"}, status=400)
            except FileNotFoundError as e:
                self._send_json({"error": str(e), "error_type": "DOCUMENT_NOT_FOUND"}, status=404)
            except Exception as e:
                self._send_json({"error": f"Inference error: {str(e)}"}, status=500)
            return

        # 2. Backwards-compatible Legacy Synthetic Simulation Flow
        doc_name = payload.get("document_name", "invoice_specimen_clean.pdf")
        query = question
        deg_level = float(payload.get("degradation_level", 0.15))

        overall_quality = max(0.05, 1.0 - deg_level * 0.90)
        if overall_quality >= 0.75:
            route = "CLEAN"
            pathway_desc = "Direct VLM Stream (Sub-second pass)"
        elif overall_quality >= 0.40:
            route = "MODERATE"
            pathway_desc = "Enhancement (Wiener Deconvolution) + VLM"
        else:
            route = "SEVERE"
            pathway_desc = "Dual OCR Fallback (PaddleOCR + Tesseract) + VLM"

        pruned_pages = [1, 2]
        confidence = round(max(0.35, 0.98 - deg_level * 0.45), 3)
        if confidence >= 0.75:
            status = "VERIFIED"
            answer = "$1,420.50"
            evidence = [
                {
                    "page": 1,
                    "bbox": [140, 280, 420, 310],
                    "normalized_bbox": [0.14, 0.28, 0.42, 0.31],
                    "text": "TOTAL BALANCE DUE: $1,420.50",
                    "iou": 0.88,
                    "confidence": 0.96
                }
            ]
            abstained = False
        else:
            status = "ABSTAIN / REVIEW_REQUIRED"
            answer = "ABSTAIN: Visual degradation exceeds safe evidence threshold"
            evidence = []
            abstained = True

        response = {
            "document_id": doc_name,
            "query": query,
            "answer": answer,
            "confidence": confidence,
            "status": status,
            "abstained": abstained,
            "routing_decision": route,
            "pathway_description": pathway_desc,
            "context_pruning": {
                "total_pages": 5,
                "retrieved_pages": pruned_pages,
                "page_reduction_pct": 60.0
            },
            "evidence": evidence,
            "quality": {
                "overall_quality": round(overall_quality, 3),
                "degradation_level": deg_level
            },
            "timing": {
                "total_ms": 3750.0
            },
            "runtime_telemetry": {
                "quantization": "INT4 NF4 BitsAndBytes",
                "hardware": "NVIDIA GeForce RTX 3050 6GB GDDR6",
                "vram_mb": 530.9,
                "latency_s": 3.75,
                "speedup": "2.0x vs Full-Doc Baseline"
            }
        }
        self._send_json(response)

    def _handle_api_health(self):
        hw = get_hardware_status()
        health_data = {
            "status": "online",
            "service": "VLM-IDP Full-Stack Server & Document Extraction Studio",
            "port": 8896,
            "research_phase": "Phase 14 (Physical CUDA 12.6 Enabled) · Phase 15 (Interactive Document Studio Active)",
            "environment": {
                "python_version": sys.version.split()[0],
                "python_executable": sys.executable,
                "project_root": str(PROJECT_ROOT)
            },
            "hardware": hw
        }
        self._send_json(health_data)

    def _handle_api_metrics(self):
        metrics_data = {
            "research_title": "Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation",
            "target_standard": "IEEE Quality Experimental Methodology",
            "empirical_benchmarks": {
                "exact_match": {
                    "unpruned_baseline": 0.7091,
                    "proposed_pruned_grounded": 0.7927,
                    "delta": "+0.0836",
                    "p_value": 0.0002,
                    "hypothesis": "H14-3 CONFIRMED"
                },
                "hallucination_rate": {
                    "unpruned_baseline": 0.2218,
                    "proposed_calibrated": 0.0109,
                    "relative_reduction": "-92.1%",
                    "p_value": "<0.0001",
                    "hypothesis": "H14-4 CONFIRMED"
                },
                "physical_cuda_quantization": {
                    "fp16": {"vram_mb": 1111.6, "throughput_tok_s": 27.8},
                    "int8": {"vram_mb": 702.0, "reduction_pct": 36.8, "throughput_tok_s": 8.6},
                    "int4_nf4": {"vram_mb": 530.9, "reduction_pct": 52.2, "throughput_tok_s": 16.5}
                },
                "latency_speedup": "2.0x (7.48s -> 3.75s)",
                "safe_useful_coverage": "89.1%"
            }
        }
        self._send_json(metrics_data)

    def _handle_quality_assess(self, payload):
        deg_level = float(payload.get("degradation_level", 0.0))
        quality_vector = {
            "blur_score": round(min(1.0, deg_level * 0.85 + 0.05), 3),
            "noise_score": round(min(1.0, deg_level * 0.70 + 0.02), 3),
            "contrast_score": round(max(0.0, 1.0 - deg_level * 0.60), 3),
            "skew_deg": round(deg_level * 8.5, 1),
            "glare_score": round(min(1.0, deg_level * 0.40), 3),
            "occlusion_score": round(min(1.0, deg_level * 0.50), 3),
            "overall_quality": round(max(0.05, 1.0 - deg_level * 0.90), 3)
        }
        self._send_json({"quality_assessment": quality_vector})

    def _handle_static_file(self, req_path):
        if req_path in ("/", ""):
            filepath = DOCS_DIR / "index.html"
        elif req_path.startswith("/assets/"):
            subpath = req_path[len("/assets/"):]
            filepath = ASSETS_DIR / subpath
        elif req_path.startswith("/docs/"):
            subpath = req_path[len("/docs/"):]
            filepath = DOCS_DIR / subpath
        else:
            clean_subpath = req_path.lstrip("/")
            p_docs = DOCS_DIR / clean_subpath
            p_assets = ASSETS_DIR / clean_subpath
            if p_docs.is_file():
                filepath = p_docs
            elif p_assets.is_file():
                filepath = p_assets
            else:
                filepath = DOCS_DIR / "index.html"

        if not filepath.is_file():
            self.send_error(404, f"File not found: {req_path}")
            return

        content_type, _ = mimetypes.guess_type(str(filepath))
        if filepath.suffix.lower() == ".svg":
            content_type = "image/svg+xml"
        elif not content_type:
            content_type = "application/octet-stream"

        try:
            with open(filepath, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self._set_cors_headers()
            if filepath.suffix.lower() in [".svg", ".png", ".jpg", ".js", ".css"]:
                self.send_header("Cache-Control", "public, max-age=3600")
            else:
                self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")


def run_server(port=8896, host="0.0.0.0"):
    """Starts the full-stack server on the specified port."""
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, VLMIDPRequestHandler)
    print("=" * 72)
    print("   VLM-IDP RESEARCH — DOCUMENT EXTRACTION STUDIO & API (PORT 8896)")
    print("=" * 72)
    print(f" * Interactive Studio:       http://localhost:{port}/")
    print(f" * Multipart Upload API:     POST http://localhost:{port}/api/upload")
    print(f" * Document Page Image:      GET  http://localhost:{port}/api/document/{{id}}/page/{{p}}")
    print(f" * Pipeline Inference API:   POST http://localhost:{port}/api/pipeline/infer")
    print(f" * Model Capability API:     GET  http://localhost:{port}/api/models/capability")
    print(f" * Hardware Health Status:   GET  http://localhost:{port}/api/health")
    print("-" * 72)
    print(" Ready on all network interfaces. Press Ctrl+C to terminate.")
    print("=" * 72)
    sys.stdout.flush()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down gracefully...")
        httpd.shutdown()
        httpd.server_close()
        print("[Server] Terminated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start VLM-IDP Full-Stack Server")
    parser.add_argument("--port", type=int, default=8896, help="Port to bind (default: 8896)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    args = parser.parse_args()
    run_server(port=args.port, host=args.host)
