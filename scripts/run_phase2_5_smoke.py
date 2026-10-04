"""Controlled Smoke and Degradation Experiment Runner for Unlimited-OCR (B0-U)."""

import json
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw, ImageFilter
import yaml

from src.baselines.base import BaselineSample, BaselineResult
from src.baselines.unlimited_ocr.adapter import B0UnlimitedOCRBaseline
from src.evaluation.artifacts import save_run_artifact, save_experiment_summary


def create_synthetic_document(text_lines, title="INVOICE #INV-2024-001") -> Image.Image:
    """Creates a clean synthetic document page image."""
    img = Image.new("RGB", (600, 400), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.text((40, 40), title, fill=(0, 0, 0))
    y = 100
    for line in text_lines:
        draw.text((40, y), line, fill=(0, 0, 0))
        y += 60
    return img


def apply_synthetic_blur(img: Image.Image, radius: float) -> Image.Image:
    """Applies controlled Gaussian blur per Phase 0 degradation protocol."""
    if radius <= 0:
        return img
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def run_phase2_5_experiments():
    print("=== STARTING PHASE 2.5 UNLIMITED-OCR VALIDATION EXPERIMENTS ===")

    baseline = B0UnlimitedOCRBaseline()
    out_dir = "experiments/phase2_5/artifacts"
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # 1. Single-Page Controlled Smoke Test
    print("\n--- 1. Single-Page Smoke Test (E2_5-SMOKE-B0_U) ---")
    clean_lines = [
        "Vendor: Acme Corporation",
        "Date: 2024-05-12",
        "Total Amount: $1,450.00"
    ]
    clean_img = create_synthetic_document(clean_lines, "INVOICE #INV-2024-001")
    sample_single = BaselineSample(
        sample_id="q_u_single_001",
        document_id="doc_u_single",
        page_idx=0,
        image=clean_img,
        question="What is the total amount?",
        ground_truth_answers=["$1,450.00"]
    )

    t0 = time.perf_counter()
    res_single = baseline.run(sample_single, run_id="run_u_single", seed=42)
    lat_single = (time.perf_counter() - t0) * 1000.0
    save_run_artifact(res_single, output_dir=out_dir)
    save_experiment_summary([res_single], "E2_5-SMOKE-B0_U", output_dir="experiments/phase2_5")
    print(f"Single-page status: {res_single.status} | Latency: {lat_single:.2f} ms | Answer: '{res_single.answer}'")

    # 2. Multi-Page Validation Test
    print("\n--- 2. Multi-Page Validation Test (2 Pages) ---")
    page_imgs = [
        create_synthetic_document(clean_lines, "INVOICE #INV-2024-001 (Page 1)"),
        create_synthetic_document(["Line Item 1: Hardware Support", "Line Item 2: Cloud Storage"], "INVOICE ATTACHMENT (Page 2)")
    ]
    multi_results = []
    for p_idx, p_img in enumerate(page_imgs):
        s = BaselineSample(
            sample_id=f"q_u_multi_p{p_idx}",
            document_id="doc_u_multi",
            page_idx=p_idx,
            image=p_img,
            question="What is the document title?",
            ground_truth_answers=["INVOICE #INV-2024-001 (Page 1)"]
        )
        r = baseline.run(s, run_id=f"run_u_multi_p{p_idx}", seed=42)
        save_run_artifact(r, output_dir=out_dir)
        multi_results.append(r)
    save_experiment_summary(multi_results, "E2_5-MULTIPAGE-B0_U", output_dir="experiments/phase2_5")
    print(f"Multi-page processed: {len(multi_results)} pages | All SUCCESS: {all(r.status == 'SUCCESS' for r in multi_results)}")

    # 3. Controlled Degradation Smoke Test
    print("\n--- 3. Controlled Degradation Smoke Test (Clean, Mild, Medium, Severe) ---")
    degradations = [
        ("clean", 0.0),
        ("mild_blur", 1.0),
        ("medium_blur", 2.0),
        ("severe_blur", 4.0)
    ]
    deg_results = []
    for deg_name, radius in degradations:
        deg_img = apply_synthetic_blur(clean_img, radius)
        s = BaselineSample(
            sample_id=f"q_deg_{deg_name}",
            document_id=f"doc_deg_{deg_name}",
            page_idx=0,
            image=deg_img,
            question="What is the total amount?",
            ground_truth_answers=["$1,450.00"]
        )
        r = baseline.run(s, run_id=f"run_u_deg_{deg_name}", seed=42)
        save_run_artifact(r, output_dir=out_dir)
        deg_results.append(r)
        print(f"Degradation [{deg_name}]: Status={r.status} | Latency={r.latency_ms} ms | Answer='{r.answer}'")
    save_experiment_summary(deg_results, "E2_5-DEG-B0_U", output_dir="experiments/phase2_5")

    # 4. Reproducibility Test (2 repeated runs on identical sample)
    print("\n--- 4. Reproducibility Test (Repeatability Comparison) ---")
    res_repeat = baseline.run(sample_single, run_id="run_u_repeat", seed=42)
    save_run_artifact(res_repeat, output_dir=out_dir)
    save_experiment_summary([res_single, res_repeat], "E2_5-REPRO-B0_U", output_dir="experiments/phase2_5")

    match = (res_single.answer == res_repeat.answer) and (res_single.prompt_hash == res_repeat.prompt_hash)
    print(f"Reproducibility match: {match} (Answer 1: '{res_single.answer}' == Answer 2: '{res_repeat.answer}')")

    print("\n=== PHASE 2.5 EXPERIMENTS COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_phase2_5_experiments()
