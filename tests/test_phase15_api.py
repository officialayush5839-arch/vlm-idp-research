"""Tests for Phase 15 REST API Endpoints."""

import json
import time
import socket
import threading
import urllib.request
import urllib.error
from io import BytesIO
import pytest
from PIL import Image

from src.server import ThreadedHTTPServer, VLMIDPRequestHandler

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@pytest.fixture(scope="module")
def api_server():
    port = get_free_port()
    server = ThreadedHTTPServer(("127.0.0.1", port), VLMIDPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.3)
    base_url = f"http://127.0.0.1:{port}"
    yield base_url
    server.shutdown()
    server.server_close()

def build_multipart_body(filename: str, file_bytes: bytes, content_type: str = "image/png"):
    boundary = "----WebKitFormBoundaryPhase15TestBoundary"
    body = BytesIO()
    body.write(f"--{boundary}\r\n".encode("utf-8"))
    body.write(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8")
    )
    body.write(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.write(file_bytes)
    body.write(b"\r\n")
    body.write(f"--{boundary}--\r\n".encode("utf-8"))
    return boundary, body.getvalue()

def test_api_models_capability(api_server):
    req = urllib.request.Request(f"{api_server}/api/models/capability")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert "models" in data
        assert "hardware" in data
        assert "qwen2.5-vl-7b" in data["models"]
        assert data["models"]["qwen2.5-vl-7b"]["status"] == "NOT_EXECUTABLE"
        assert "smolvlm-500m" in data["models"]

def test_multipart_upload_and_preview(api_server):
    # Create valid 1x1 PNG image
    buf = BytesIO()
    img = Image.new("RGB", (200, 300), color=(255, 255, 255))
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    boundary, body = build_multipart_body("test_sample.png", png_bytes, "image/png")
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

    req = urllib.request.Request(f"{api_server}/api/upload", data=body, headers=headers)
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        upload_data = json.loads(resp.read().decode("utf-8"))
        assert upload_data["status"] == "accepted"
        assert "upload_id" in upload_data
        assert upload_data["page_count"] == 1
        upload_id = upload_data["upload_id"]

    # Verify preview page image endpoint
    page_req = urllib.request.Request(f"{api_server}/api/document/{upload_id}/page/1")
    with urllib.request.urlopen(page_req) as page_resp:
        assert page_resp.status == 200
        assert page_resp.headers.get("Content-Type") == "image/png"
        page_bytes = page_resp.read()
        assert len(page_bytes) > 0

def test_upload_missing_file_rejected(api_server):
    req = urllib.request.Request(
        f"{api_server}/api/upload",
        data=b"not multipart data",
        headers={"Content-Type": "application/json"},
    )
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(req)
    assert exc_info.value.code == 400

def test_pipeline_infer_with_real_upload(api_server):
    buf = BytesIO()
    img = Image.new("RGB", (500, 600), color=(255, 255, 255))
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    boundary, body = build_multipart_body("invoice_doc.png", png_bytes, "image/png")
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    req = urllib.request.Request(f"{api_server}/api/upload", data=body, headers=headers)
    with urllib.request.urlopen(req) as resp:
        upload_data = json.loads(resp.read().decode("utf-8"))
        upload_id = upload_data["upload_id"]

    # Call infer on this upload_id
    infer_payload = json.dumps({
        "upload_id": upload_id,
        "question": "What is the total balance due?",
        "page_num": 1
    }).encode("utf-8")

    infer_req = urllib.request.Request(
        f"{api_server}/api/pipeline/infer",
        data=infer_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(infer_req) as resp:
        assert resp.status == 200
        result = json.loads(resp.read().decode("utf-8"))
        assert "answer" in result
        assert "confidence" in result
        assert "routing_decision" in result
        assert "quality" in result
        assert "timing" in result
