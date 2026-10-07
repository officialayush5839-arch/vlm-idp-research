"""Phase 14 Publication Figure Generation Engine.

Generates 12 publication-quality figures at 300 DPI from real physical execution tables and traces:
1. fig_01_cuda_vram_by_precision.png
2. fig_02_e2e_latency_by_precision.png
3. fig_03_throughput_by_precision.png
4. fig_04_model_loading_time.png
5. fig_05_pareto_vram_vs_latency.png
6. fig_06_context_scaling_latency.png
7. fig_07_accuracy_by_condition.png
8. fig_08_grounding_iou_by_condition.png
9. fig_09_unsupported_answer_rate.png
10. fig_10_safe_useful_coverage.png
11. fig_11_latency_by_modality.png
12. fig_12_precision_quality_tradeoff.png
"""

import os
import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(r"c:\Users\ARYAN - AYUSH\OneDrive\Desktop\Nlp\vlm-idp-research")
TABLES_DIR = REPO_ROOT / "experiments" / "phase14" / "tables"
TRACES_FILE = REPO_ROOT / "experiments" / "phase14" / "traces" / "physical_inference_traces.jsonl"
FIGURES_DIR = REPO_ROOT / "experiments" / "phase14" / "figures"

def set_ieee_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9,
        "figure.titlesize": 13,
        "grid.color": "#e0e0e0",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
    })

def generate_all_figures():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    set_ieee_style()

    # Load required data
    df_q = pd.read_csv(TABLES_DIR / "table_04_quantization_matrix.csv")
    df_traces = pd.read_json(TRACES_FILE, lines=True)

    colors = ["#2b5c8f", "#d95f02", "#7570b3", "#1b9e77"]

    # 1. Physical CUDA VRAM Allocation by Precision
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    bars = ax.bar(df_q["Precision"], df_q["Peak_VRAM_MB"], color=["#1f77b4", "#ff7f0e", "#2ca02c"], width=0.5, edgecolor="black")
    ax.axhline(6144, color="crimson", linestyle="--", linewidth=1.2, label="RTX 3050 Physical Limit (6,144 MB)")
    ax.set_ylabel("Peak CUDA VRAM (MB)")
    ax.set_title("Physical CUDA VRAM Footprint by Precision Level")
    ax.grid(True, axis="y")
    ax.legend(loc="upper right")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 60, f"{h:.1f} MB", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylim(0, 7000)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_01_cuda_vram_by_precision.png")
    plt.close(fig)

    # 2. End-to-End Inference Latency by Precision
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    bars = ax.bar(df_q["Precision"], df_q["Latency_s"], color=["#1f77b4", "#ff7f0e", "#2ca02c"], width=0.5, edgecolor="black")
    ax.set_ylabel("Mean Physical Latency (seconds)")
    ax.set_title("VLM Forward Latency across Quantization Modes")
    ax.grid(True, axis="y")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.05, f"{h:.3f} s", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(df_q["Latency_s"]) * 1.25)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_02_e2e_latency_by_precision.png")
    plt.close(fig)

    # 3. Token Generation Throughput
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    bars = ax.bar(df_q["Precision"], df_q["Throughput_tok_s"], color=["#1f77b4", "#ff7f0e", "#2ca02c"], width=0.5, edgecolor="black")
    ax.set_ylabel("Throughput (tokens / second)")
    ax.set_title("Physical Neural Generation Throughput")
    ax.grid(True, axis="y")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f"{h:.1f} tok/s", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(df_q["Throughput_tok_s"]) * 1.2)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_03_throughput_by_precision.png")
    plt.close(fig)

    # 4. Model Loading Time
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    bars = ax.bar(df_q["Precision"], df_q["Load_Time_s"], color=["#386cb0", "#f0027f", "#bf5b17"], width=0.5, edgecolor="black")
    ax.set_ylabel("Weight Dequantization & Load Time (s)")
    ax.set_title("CUDA Device Loading & Quantization Overhead")
    ax.grid(True, axis="y")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.1, f"{h:.2f} s", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(df_q["Load_Time_s"]) * 1.25)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_04_model_loading_time.png")
    plt.close(fig)

    # 5. Pareto Frontier (VRAM vs Latency)
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    for _, row in df_q.iterrows():
        ax.scatter(row["Peak_VRAM_MB"], row["Latency_s"], s=150, edgecolor="black", label=row["Precision"], zorder=5)
        ax.annotate(row["Precision"], (row["Peak_VRAM_MB"] + 15, row["Latency_s"] + 0.02), fontsize=9, fontweight="bold")
    ax.set_xlabel("Peak CUDA VRAM (MB)")
    ax.set_ylabel("Mean Latency (s)")
    ax.set_title("Memory-Efficiency vs Latency Trade-Off")
    ax.grid(True)
    ax.legend(loc="upper left")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_05_pareto_vram_vs_latency.png")
    plt.close(fig)

    # 6. Page Context Scaling vs Latency
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    cond_lat = df_traces.groupby(["condition", "pages_fed"])["physical_latency_s"].mean().reset_index()
    for _, row in cond_lat.iterrows():
        ax.bar(row["condition"], row["physical_latency_s"], width=0.45, edgecolor="black", color="#4daf4a")
        ax.text(row["condition"], row["physical_latency_s"] + 0.03, f"{row['physical_latency_s']:.2f} s\n({row['pages_fed']} pgs)", ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("Mean Latency (seconds)")
    ax.set_title("Context Pruning Speedup (Pages Fed vs Latency)")
    ax.grid(True, axis="y")
    ax.set_ylim(0, max(cond_lat["physical_latency_s"]) * 1.3)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_06_context_scaling_latency.png")
    plt.close(fig)

    # 7. Exact Match Accuracy by Condition
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    accs = df_traces.groupby("condition")["exact_match_accuracy"].agg(["mean", "std"]).reset_index()
    ax.bar(accs["condition"], accs["mean"], yerr=accs["std"], capsize=4, width=0.45, color="#377eb8", edgecolor="black")
    ax.set_ylabel("Exact Match Accuracy")
    ax.set_title("Document QA Extraction Quality Across Conditions")
    ax.grid(True, axis="y")
    for idx, row in accs.iterrows():
        ax.text(row["condition"], row["mean"] / 2, f"{row['mean']:.3f}", ha="center", va="center", color="white", fontweight="bold")
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_07_accuracy_by_condition.png")
    plt.close(fig)

    # 8. Evidence Grounding IoU
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    ious = df_traces.groupby("condition")["grounding_iou"].agg(["mean", "std"]).reset_index()
    ax.bar(ious["condition"], ious["mean"], yerr=ious["std"], capsize=4, width=0.45, color="#984ea3", edgecolor="black")
    ax.set_ylabel("Mean Bounding-Box IoU")
    ax.set_title("Spatial Evidence Grounding Precision")
    ax.grid(True, axis="y")
    for idx, row in ious.iterrows():
        ax.text(row["condition"], row["mean"] / 2, f"{row['mean']:.3f}", ha="center", va="center", color="white", fontweight="bold")
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_08_grounding_iou_by_condition.png")
    plt.close(fig)

    # 9. Unsupported Answer Rate
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    uars = df_traces.groupby("condition")["unsupported_answer_rate"].mean().reset_index()
    bars = ax.bar(uars["condition"], uars["unsupported_answer_rate"], width=0.45, color="#e41a1c", edgecolor="black")
    ax.set_ylabel("Unsupported Answer Rate (UAR)")
    ax.set_title("Hallucination Suppression across Pipeline Stages")
    ax.grid(True, axis="y")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.005, f"{h:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(uars["unsupported_answer_rate"]) * 1.35)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_09_unsupported_answer_rate.png")
    plt.close(fig)

    # 10. Safe Useful Coverage
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    sucs = df_traces.groupby("condition")["safe_useful_coverage"].mean().reset_index()
    bars = ax.bar(sucs["condition"], sucs["safe_useful_coverage"], width=0.45, color="#4daf4a", edgecolor="black")
    ax.set_ylabel("Safe Useful Coverage (SUC)")
    ax.set_title("Effective Reliable Task Coverage (SUC)")
    ax.grid(True, axis="y")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h / 2, f"{h:.3f}", ha="center", va="center", color="white", fontweight="bold")
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_10_safe_useful_coverage.png")
    plt.close(fig)

    # 11. Latency by Document Modality
    fig, ax = plt.subplots(figsize=(6.5, 4), dpi=300)
    mod_lat = df_traces.groupby(["modality", "condition"])["physical_latency_s"].mean().unstack()
    mod_lat.plot(kind="bar", ax=ax, edgecolor="black", colormap="viridis")
    ax.set_ylabel("Mean Latency (s)")
    ax.set_title("Physical Latency by Document Modality & Pipeline")
    ax.grid(True, axis="y")
    ax.legend(title="Condition", loc="upper right")
    plt.xticks(rotation=0)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_11_latency_by_modality.png")
    plt.close(fig)

    # 12. Precision-Quality Tradeoff
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    prec_labels = ["FP16", "INT8", "INT4"]
    mem_saved = [0, (1 - 702.01/1111.64)*100, (1 - 530.95/1111.64)*100]
    throughputs = df_q["Throughput_tok_s"].values
    ax.plot(prec_labels, mem_saved, marker="o", color="#e41a1c", linewidth=2, label="VRAM Reduction (%)")
    ax.set_ylabel("VRAM Reduction (%)", color="#e41a1c")
    ax.tick_params(axis="y", labelcolor="#e41a1c")
    ax2 = ax.twinx()
    ax2.plot(prec_labels, throughputs, marker="s", color="#377eb8", linewidth=2, linestyle="--", label="Throughput (tok/s)")
    ax2.set_ylabel("Throughput (tok/s)", color="#377eb8")
    ax2.tick_params(axis="y", labelcolor="#377eb8")
    ax.set_title("Quantization Efficiency & Throughput Trade-Off")
    ax.grid(True)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_12_precision_quality_tradeoff.png")
    plt.close(fig)

    print("Successfully generated all 12 publication figures at 300 DPI.")

if __name__ == "__main__":
    generate_all_figures()
