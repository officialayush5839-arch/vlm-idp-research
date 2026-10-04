import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw, ImageFont
import yaml

from src.baselines.base import BaselineSample
from src.baselines.b0_ocr import B0OCRBaseline
from src.baselines.b1_ocr_vlm import B1OCRVLMBaseline
from src.baselines.b2_vlm import B2VLMBaseline
from src.vlm.loader import VLMLoader
from src.vlm.inference import VLMInferenceEngine
from src.evaluation.metrics import (
    compute_exact_match,
    compute_token_f1,
    compute_anls,
    normalize_answer
)
from src.evaluation.artifacts import save_run_artifact, save_experiment_summary


def create_synthetic_doc_sample(idx: int) -> BaselineSample:
    """Generate a clean synthetic document image with known text and question."""
    w, h = 600, 400
    img = Image.new("RGB", (w, h), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)

    titles = [
        ("INVOICE #INV-2024-001", "Acme Corporation", "$1,450.00", "2024-05-12"),
        ("RECEIPT #REC-8891", "Metro Logistics", "$320.50", "2024-06-01"),
        ("STATEMENT #ST-4402", "Pacific Telecom", "$89.99", "2024-06-15"),
        ("PURCHASE ORDER #PO-109", "Global Supplies", "$5,200.00", "2024-07-04"),
        ("TAX INVOICE #TX-771", "Apex Consulting", "$750.00", "2024-07-20")
    ]
    title, vendor, total, date = titles[idx % len(titles)]

    draw.text((40, 40), title, fill=(0, 0, 0))
    draw.text((40, 100), f"Vendor: {vendor}", fill=(0, 0, 0))
    draw.text((40, 160), f"Date: {date}", fill=(0, 0, 0))
    draw.text((40, 220), f"Total Amount: {total}", fill=(0, 0, 0))

    questions = [
        ("What is the total amount?", total),
        ("Who is the vendor?", vendor),
        ("What is the date?", date),
        ("What is the total amount?", total),
        ("Who is the vendor?", vendor)
    ]
    q_text, gt_ans = questions[idx % len(questions)]

    return BaselineSample(
        sample_id=f"smoke_q_{idx:03d}",
        document_id=f"doc_smoke_{idx:03d}",
        page_idx=0,
        image=img,
        question=q_text,
        ground_truth_answers=[gt_ans]
    )


def run_smoke_experiments():
    print("=== STARTING PHASE 2 CONTROLLED SMOKE EXPERIMENTS ===")
    samples = [create_synthetic_doc_sample(i) for i in range(5)]

    # Initialize baselines
    loader = VLMLoader()
    model, processor, metadata = loader.load_model_and_processor(mock_mode=True)
    engine = VLMInferenceEngine(model, processor, metadata, device="cpu", mock_mode=True)

    b0 = B0OCRBaseline()
    b1 = B1OCRVLMBaseline(vlm_engine=engine)
    b2 = B2VLMBaseline(vlm_engine=engine)

    # 1. E2-SMOKE-B0
    print("Running E2-SMOKE-B0...")
    b0_results = []
    for s in samples:
        res = b0.run(s, run_id="run_smoke_b0", seed=42)
        save_run_artifact(res)
        b0_results.append(res)
    save_experiment_summary(b0_results, "E2-SMOKE-B0")

    # 2. E2-SMOKE-B1
    print("Running E2-SMOKE-B1...")
    b1_results = []
    for s in samples:
        res = b1.run(s, run_id="run_smoke_b1", seed=42)
        save_run_artifact(res)
        b1_results.append(res)
    save_experiment_summary(b1_results, "E2-SMOKE-B1")

    # 3. E2-SMOKE-B2
    print("Running E2-SMOKE-B2...")
    b2_results = []
    for s in samples:
        res = b2.run(s, run_id="run_smoke_b2", seed=42)
        save_run_artifact(res)
        b2_results.append(res)
    save_experiment_summary(b2_results, "E2-SMOKE-B2")

    # 4. E2-REPRO-B0 (Repeatability check)
    print("Running E2-REPRO-B0 (Repeatability run)...")
    repro_results = []
    for s in samples:
        res = b0.run(s, run_id="run_repro_b0", seed=42)
        repro_results.append(res)
    save_experiment_summary(repro_results, "E2-REPRO-B0")

    # Verify reproducibility
    exact_matches = 0
    for r1, r2 in zip(b0_results, repro_results):
        if r1.answer == r2.answer:
            exact_matches += 1
    repro_rate = (exact_matches / len(samples)) * 100.0
    print(f"B0 Reproducibility Match Rate: {repro_rate:.1f}% ({exact_matches}/{len(samples)})")

    print("=== SMOKE EXPERIMENTS COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_smoke_experiments()
