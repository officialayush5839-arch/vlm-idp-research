"""Test suite for VLM-IDP Full-Stack Server & REST API."""

import json
import time
import socket
import threading
import urllib.request
import pytest
from src.server import ThreadedHTTPServer, VLMIDPRequestHandler

def get_free_port():
    """Finds an available TCP port for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@pytest.fixture(scope="module")
def server_instance():
    """Starts the test server in a background daemon thread."""
    port = get_free_port()
    server = ThreadedHTTPServer(("127.0.0.1", port), VLMIDPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.3) # Allow socket to bind
    base_url = f"http://127.0.0.1:{port}"
    yield base_url
    server.shutdown()
    server.server_close()

def test_frontend_serving(server_instance):
    """Verify that root / serves index.html with 200 OK and expected text."""
    req = urllib.request.Request(f"{server_instance}/")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        content = resp.read().decode("utf-8")
        assert "VLM-IDP RESEARCH" in content
        assert "text/html" in resp.headers.get("Content-Type", "")

def test_svg_asset_serving(server_instance):
    """Verify that SVG assets are served with proper image/svg+xml MIME type."""
    req = urllib.request.Request(f"{server_instance}/assets/architecture-3d-pipeline.svg")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        assert "image/svg+xml" in resp.headers.get("Content-Type", "")
        content = resp.read()
        assert b"<svg" in content

def test_api_health(server_instance):
    """Verify that GET /api/health returns online status and system environment."""
    req = urllib.request.Request(f"{server_instance}/api/health")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "online"
        assert "Phase 14" in data["research_phase"]
        assert "hardware" in data

def test_api_metrics(server_instance):
    """Verify that GET /api/metrics returns the frozen research metrics."""
    req = urllib.request.Request(f"{server_instance}/api/metrics")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert "empirical_benchmarks" in data
        assert data["empirical_benchmarks"]["exact_match"]["delta"] == "+0.0836"
        assert data["empirical_benchmarks"]["hallucination_rate"]["relative_reduction"] == "-92.1%"

def test_api_pipeline_infer(server_instance):
    """Verify that POST /api/pipeline/infer executes and returns complete schema."""
    payload = json.dumps({
        "document_name": "test_invoice.pdf",
        "query": "What is the total amount due?",
        "degradation_level": 0.1
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{server_instance}/api/pipeline/infer",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "VERIFIED"
        assert data["routing_decision"] == "CLEAN"
        assert "evidence" in data
        assert len(data["evidence"]) > 0
        assert "runtime_telemetry" in data

def test_api_quality_assess(server_instance):
    """Verify that POST /api/quality/assess returns 10-feature quality vector."""
    payload = json.dumps({"degradation_level": 0.45}).encode("utf-8")
    req = urllib.request.Request(
        f"{server_instance}/api/quality/assess",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert "quality_assessment" in data
        assert "blur_score" in data["quality_assessment"]
        assert "overall_quality" in data["quality_assessment"]
