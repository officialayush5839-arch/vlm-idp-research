"""scripts/generate_phase10_5_figures.py
Generates publication-quality figures for Phase 10.5 report:
1. Fig 10.5.1: Safe Useful Coverage (SUC) by Domain & Baseline
2. Fig 10.5.2: Safe vs. Unsafe Recovery Trade-off across Strategies
3. Fig 10.5.3: Recovery State Taxonomy Distribution in D2 and D4
"""

import os
import json
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("experiments/phase10_5/figures", exist_ok=True)

with open("experiments/phase10_5/results/recovery_benchmark_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

domains = ["D0_in_domain", "D1_layout_shift", "D2_visual_style_shift", "D3_structure_shift", "D4_combined_shift"]
domain_labels = ["D0 In-Domain", "D1 Layout", "D2 Visual Blur", "D3 Structure", "D4 Combined"]

# Fig 1: SUC comparison
b0_suc = [summary["B10.5-0"][d]["safe_useful_coverage"] for d in domains]
b5_suc = [summary["B10.5-5"][d]["safe_useful_coverage"] for d in domains]

x = np.arange(len(domains))
width = 0.35

plt.figure(figsize=(9, 5))
plt.bar(x - width/2, b0_suc, width, label="B10.5-0 (Phase 10 Abstention)", color="#5C6BC0")
plt.bar(x + width/2, b5_suc, width, label="B10.5-5 (Proposed Recovery)", color="#26A69A")
plt.xlabel("Domain / Distribution Shift")
plt.ylabel("Safe Useful Coverage (SUC)")
plt.title("Phase 10.5: Safe Useful Coverage Across Distribution Shifts")
plt.xticks(x, domain_labels)
plt.ylim(0, 1.05)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("experiments/phase10_5/figures/fig10_5_suc_by_domain.png", dpi=300)
plt.close()

# Fig 2: Safe vs Unsafe Recovery Trade-off across Baselines
baselines = ["B10.5-0", "B10.5-1", "B10.5-2", "B10.5-3", "B10.5-4", "B10.5-5"]
overall_suc = []
overall_urr = []
for b in baselines:
    tot_s = sum(summary[b][d]["num_safe_useful"] for d in domains)
    tot_u = sum(summary[b][d]["num_unsafe"] for d in domains)
    tot = sum(summary[b][d]["total_samples"] for d in domains)
    overall_suc.append(tot_s / tot)
    overall_urr.append(tot_u / tot)

plt.figure(figsize=(7, 5))
plt.scatter(overall_urr, overall_suc, color="#D81B60", s=120, edgecolors="black", zorder=4)
for i, txt in enumerate(baselines):
    plt.annotate(txt, (overall_urr[i] + 0.005, overall_suc[i] - 0.01), fontsize=9)

plt.axvline(x=0.05, color="red", linestyle="--", label="URR Safety Bound (5%)")
plt.xlabel("Overall Unsafe Recovery Rate (URR)")
plt.ylabel("Overall Safe Useful Coverage (SUC)")
plt.title("Phase 10.5: Safety vs. Utility Recovery Trade-off")
plt.xlim(-0.02, 0.40)
plt.ylim(0.40, 0.75)
plt.legend()
plt.grid(linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("experiments/phase10_5/figures/fig10_5_safety_tradeoff.png", dpi=300)
plt.close()

print("Figures successfully generated in experiments/phase10_5/figures/")
