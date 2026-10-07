# Phase 15: Interactive Document Upload & Extraction Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-grade, end-user interactive Document Upload & Extraction Studio that processes real PDF/image documents through the existing research pipeline, visualizes spatial evidence bounding boxes, enforces calibrated abstention, and runs safely on the RTX 3050 6GB local hardware without fabricating model capabilities or corrupting Phase 14 frozen artifacts.

**Architecture:** An isolated runtime layer (`src/runtime/`) orchestrates document upload validation, PDF/image conversion, hardware-aware model registry selection, and the existing `src/quality/`, `src/enhancement/`, `src/ocr/`, `src/routing/`, and `src/uncertainty/` modules. A REST API in `src/server.py` serves both endpoints and an interactive document intelligence studio frontend with SVG/Canvas coordinate mapping.

**Tech Stack:** Python 3.14, PyTorch 2.14.1+cu126, Pillow (PIL), pypdf/PyMuPDF/pdf2image fallback, Three.js & Vanilla ES6 Canvas, threading HTTP server.

**Spec:** Defined in Phase 15 Prompt & `architecture.md`.

## Global Constraints
- Phase 14 artifacts must remain frozen: no changes to Phase 14 traces, CSVs, figures, tables, or reports.
- Zero fabrication: no mock outputs, no hardcoded answers, no fake bounding boxes, no fake confidence.
- Hardware-aware: RTX 3050 6GB limits respected; Qwen2.5-VL-7B marked NOT_EXECUTABLE on current local configuration; SmolVLM-500M INT4 marked PHYSICALLY_VALIDATED.
- Safe file handling: temporary storage in `runtime/uploads/`, UUIDs, no path traversal, automatic cleanup.
- Supported file types: PDF, PNG, JPG, JPEG.
- No remote pushes: all commits remain strictly local.

## Review Focus
1. Path traversal attacks via malicious filenames (e.g., `../../etc/passwd` or `..\Windows\System32`).
2. Corrupted or zero-byte file uploads crashing the server.
3. Coordinate desynchronization between normalized document coordinates and browser viewport rendering.
4. Overconfidence on degraded scans: abstention gate must trigger when confidence is below threshold.
5. Multi-page PDF page attribution: evidence must explicitly map to the correct page number.

---

### Task 1: Repository & Pipeline Inspection (Phase 15.1)
**Files:**
- Inspect: `src/quality/`, `src/enhancement/`, `src/ocr/`, `src/routing/`, `src/uncertainty/`, `src/server.py`
- Output: `src/runtime/__init__.py`

**Interfaces:**
- Consumes: Existing module entrypoints.
- Produces: Runtime module package definition.

- [ ] **Step 1: Inspect existing pipeline modules**
- [ ] **Step 2: Create `src/runtime/__init__.py`**
- [ ] **Step 3: Verify module imports cleanly**

---

### Task 2: Upload Manager & Security Layer (Phase 15.2)
**Files:**
- Create: `src/runtime/upload_manager.py`
- Test: `tests/test_phase15_upload.py`

**Interfaces:**
- Produces: `UploadManager.save_upload(raw_bytes: bytes, filename: str, content_type: str) -> UploadRecord`
- Produces: `UploadManager.cleanup_old_uploads(max_age_seconds: int = 3600) -> int`

- [ ] **Step 1: Write tests for file validation, size limits, and path sanitization**
- [ ] **Step 2: Run tests to verify failure**
- [ ] **Step 3: Implement `UploadManager` in `src/runtime/upload_manager.py`**
- [ ] **Step 4: Run tests to verify pass**

---

### Task 3: Document Adapter & Multi-Page PDF Handling (Phase 15.3)
**Files:**
- Create: `src/runtime/document_adapter.py`
- Test: `tests/test_phase15_document_adapter.py`

**Interfaces:**
- Produces: `DocumentAdapter.inspect_document(file_path: Path) -> DocumentMetadata`
- Produces: `DocumentAdapter.render_page_as_image(file_path: Path, page_num: int) -> Image.Image`

- [ ] **Step 1: Write tests for image and PDF rendering, page numbering, dimensions**
- [ ] **Step 2: Run tests to verify failure**
- [ ] **Step 3: Implement `DocumentAdapter` with Pillow & PDF extraction**
- [ ] **Step 4: Run tests to verify pass**

---

### Task 4: Hardware-Aware Model Capability Registry (Phase 15.4)
**Files:**
- Create: `src/runtime/model_registry.py`
- Test: `tests/test_phase15_models.py`

**Interfaces:**
- Produces: `ModelRegistry.get_hardware_status() -> Dict[str, Any]`
- Produces: `ModelRegistry.get_capability_matrix() -> Dict[str, ModelCapability]`

- [ ] **Step 1: Write tests asserting Qwen2.5-VL-7B is NOT_EXECUTABLE on RTX 3050 6GB**
- [ ] **Step 2: Run tests to verify failure**
- [ ] **Step 3: Implement `ModelRegistry` connecting to `src/phase14/hardware_gate.py`**
- [ ] **Step 4: Run tests to verify pass**

---

### Task 5: Pipeline Orchestrator & Evidence Grounding (Phase 15.5)
**Files:**
- Create: `src/runtime/orchestrator.py`
- Test: `tests/test_phase15_orchestrator.py`

**Interfaces:**
- Produces: `PipelineOrchestrator.process_document(upload_record: UploadRecord, question: str, options: dict) -> ExtractionResult`

- [ ] **Step 1: Write tests for end-to-end extraction, quality assessment, routing, abstention**
- [ ] **Step 2: Run tests to verify failure**
- [ ] **Step 3: Implement `PipelineOrchestrator` re-using existing quality, OCR, routing, and abstention**
- [ ] **Step 4: Run tests to verify pass**

---

### Task 6: REST API Extension in `src/server.py` (Phase 15.6)
**Files:**
- Modify: `src/server.py`
- Test: `tests/test_phase15_api.py`

**Interfaces:**
- Produces: `POST /api/upload`, `GET /api/document/{id}/page/{page}`, `POST /api/pipeline/infer`, `GET /api/models/capability`

- [ ] **Step 1: Write tests for multipart upload endpoint and page rendering endpoint**
- [ ] **Step 2: Run tests to verify failure**
- [ ] **Step 3: Extend `VLMIDPRequestHandler` in `src/server.py`**
- [ ] **Step 4: Run tests to verify pass**

---

### Task 7: Frontend Document Extraction Studio UI (Phase 15.7)
**Files:**
- Modify: `docs/index.html`

**Interfaces:**
- Produces: Interactive Studio with file dropzone, live page preview, canvas bounding box overlay, question form, abstention banner, and hardware panel.

- [ ] **Step 1: Design clean document-intelligence UI section in `docs/index.html`**
- [ ] **Step 2: Implement drag-and-drop, client-side preview, zoom controls**
- [ ] **Step 3: Implement REST API hooks for upload, inference, and evidence bounding box rendering**
- [ ] **Step 4: Verify in browser and automated endpoint checks**

---

### Task 8: End-to-End Acceptance Tests & Scientific Safeguard (Phase 15.8 - 15.10)
**Files:**
- Create: `tests/test_phase15_acceptance.py`
- Create: `PHASE_15_IMPLEMENTATION_REPORT.md`
- Modify: `README.md`

- [ ] **Step 1: Run comprehensive test suite across all Phase 15 components**
- [ ] **Step 2: Verify Phase 14 artifacts hash manifest and git status**
- [ ] **Step 3: Generate `PHASE_15_IMPLEMENTATION_REPORT.md`**
- [ ] **Step 4: Update README.md with Document Extraction Studio usage instructions**
- [ ] **Step 5: Create local git commit `feat(phase15): add interactive document extraction studio`**
