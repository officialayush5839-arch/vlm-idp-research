"""Evaluation Metrics Implementation for Extraction, QA, and OCR."""

import re
import string
from typing import List, Union


def normalize_answer(text: str) -> str:
    """
    Standardize text according to Phase 0 evaluation protocol:
    1. Lowercase text
    2. Strip punctuation
    3. Remove English articles ('a', 'an', 'the')
    4. Collapse consecutive whitespace
    """
    if not text:
        return ""

    text = text.lower()
    # Strip punctuation
    text = "".join(ch for ch in text if ch not in set(string.punctuation))
    # Remove articles
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    # Collapse whitespace
    text = " ".join(text.split())
    return text.strip()


def compute_exact_match(prediction: str, ground_truths: List[str]) -> float:
    """Binary Exact Match score against any valid ground-truth target."""
    if not ground_truths:
        return 0.0

    norm_pred = normalize_answer(prediction)
    for gt in ground_truths:
        if norm_pred == normalize_answer(gt):
            return 1.0
    return 0.0


def compute_token_f1(prediction: str, ground_truths: List[str]) -> float:
    """Token-level F1 score computed against the best-matching ground truth."""
    if not ground_truths:
        return 0.0

    norm_pred = normalize_answer(prediction)
    pred_tokens = norm_pred.split()
    if not pred_tokens:
        return 1.0 if any(not normalize_answer(gt) for gt in ground_truths) else 0.0

    best_f1 = 0.0
    for gt in ground_truths:
        gt_tokens = normalize_answer(gt).split()
        if not gt_tokens:
            continue

        common_tokens = set(pred_tokens).intersection(set(gt_tokens))
        if not common_tokens:
            continue

        precision = len(common_tokens) / len(pred_tokens)
        recall = len(common_tokens) / len(gt_tokens)
        f1 = (2 * precision * recall) / (precision + recall)
        if f1 > best_f1:
            best_f1 = f1

    return round(best_f1, 4)


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Standard dynamic programming Levenshtein distance."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def compute_anls(prediction: str, ground_truths: List[str], tau: float = 0.50) -> float:
    """Average Normalized Levenshtein Similarity with threshold tau."""
    if not ground_truths:
        return 0.0

    norm_pred = normalize_answer(prediction)
    best_similarity = 0.0

    for gt in ground_truths:
        norm_gt = normalize_answer(gt)
        if not norm_pred and not norm_gt:
            sim = 1.0
        elif not norm_pred or not norm_gt:
            sim = 0.0
        else:
            dist = _levenshtein_distance(norm_pred, norm_gt)
            max_len = max(len(norm_pred), len(norm_gt))
            norm_dist = dist / float(max_len)
            sim = (1.0 - norm_dist) if norm_dist < tau else 0.0

        if sim > best_similarity:
            best_similarity = sim

    return round(best_similarity, 4)


def compute_cer(prediction: str, ground_truth: str) -> float:
    """Character Error Rate (CER) = Levenshtein(pred, gt) / len(gt)."""
    if not ground_truth:
        return 0.0 if not prediction else 1.0

    dist = _levenshtein_distance(prediction, ground_truth)
    return round(dist / float(len(ground_truth)), 4)


def compute_wer(prediction: str, ground_truth: str) -> float:
    """Word Error Rate (WER) computed on tokenized word sequences."""
    pred_words = prediction.strip().split()
    gt_words = ground_truth.strip().split()

    if not gt_words:
        return 0.0 if not pred_words else 1.0

    # Token-level Levenshtein
    n, m = len(pred_words), len(gt_words)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if pred_words[i - 1] == gt_words[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost # substitution
            )

    return round(dp[n][m] / float(m), 4)
