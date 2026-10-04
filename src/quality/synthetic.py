"""
Synthetic Degradation Generator strictly compliant with Phase 0 Degradation Protocol.
Produces deterministic, parameterized visual corruptions spanning all 9 protocol-defined families:
1. Gaussian Blur (sigma: 0, 1, 2, 4, 6)
2. JPEG Compression (quality: 100, 80, 50, 25, 10)
3. Gaussian Noise (sigma: 0, 5, 15, 30, 50)
4. Skew / Rotation (angle: 0, 1, 3, 5, 10 deg)
5. Illumination / Brightness (alpha: 1.0, 0.75, 0.50, 0.30, 0.15)
6. Occlusion / Cutoff (area: 0%, 5%, 10%, 20%, 30%)
7. Resolution Reduction (scale: 1.0, 0.75, 0.50, 0.25, 0.15)
8. Perspective Distortion (tilt: 0, 5, 15, 25, 35 deg)
9. Mixed Degradation (composite)
"""

from __future__ import annotations

import io
import math
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def create_clean_document_fixture(
    text_lines: Optional[List[str]] = None,
    title: str = "OFFICIAL RESEARCH DOCUMENT",
    width: int = 600,
    height: int = 400,
) -> Image.Image:
    """
    Creates a clean, crisp synthetic document page fixture.
    """
    img = Image.new("RGB", (width, height), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((40, 40), title, fill=(0, 0, 0))

    if text_lines is None:
        text_lines = [
            "Organization: VLM Intelligent Document Processing Lab",
            "Project: Adaptive, Uncertainty-Aware Document Intelligence",
            "Document ID: DOC-2026-VAL-001",
            "Invoice Amount Due: $12,450.00",
            "Validation Status: CONFIRMED - ZERO LEAKAGE INVARIANT",
        ]

    y = 90
    for line in text_lines:
        draw.text((40, y), line, fill=(0, 0, 0))
        y += 45

    return img


def apply_degradation(
    image: Image.Image,
    family: str,
    severity: int,
    seed: int = 42,
) -> Image.Image:
    """
    Applies exact protocol-defined degradation to an image.
    Severity must be in {0, 1, 2, 3, 4}.

    Args:
        image: PIL Image
        family: Degradation family name
        severity: Discrete severity level 0-4
        seed: Random seed for deterministic generation

    Returns:
        Degraded PIL Image
    """
    if severity == 0 or family == "clean":
        return image.copy()

    rng = np.random.RandomState(seed + severity * 1000)

    # Convert to RGB numpy array
    img_np = np.array(image.convert("RGB"))
    H, W, C = img_np.shape

    if family == "gaussian_blur":
        sigmas = [0.0, 1.0, 2.0, 4.0, 6.0]
        sigma = sigmas[severity]
        ksize = int(2 * math.ceil(3 * sigma) + 1)
        ksize = max(3, ksize | 1)  # must be odd
        blurred = cv2.GaussianBlur(img_np, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)
        return Image.fromarray(blurred)

    elif family == "jpeg_compression":
        qualities = [100, 80, 50, 25, 10]
        q = qualities[severity]
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=q)
        buf.seek(0)
        return Image.open(buf).convert("RGB")

    elif family == "gaussian_noise":
        sigmas = [0.0, 5.0, 15.0, 30.0, 50.0]
        sigma = sigmas[severity]
        noise = rng.normal(0.0, sigma, img_np.shape)
        noisy = np.clip(img_np.astype(np.float64) + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy)

    elif family == "skew_rotation":
        angles = [0.0, 1.0, 3.0, 5.0, 10.0]
        angle = angles[severity]
        # Rotate around center with white background padding
        center = (W / 2.0, H / 2.0)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            img_np,
            M,
            (W, H),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(250, 250, 250),
        )
        return Image.fromarray(rotated)

    elif family == "illumination":
        alphas = [1.00, 0.75, 0.50, 0.30, 0.15]
        alpha = alphas[severity]
        attenuated = np.clip(img_np.astype(np.float64) * alpha, 0, 255).astype(np.uint8)
        return Image.fromarray(attenuated)

    elif family == "occlusion":
        ratios = [0.00, 0.05, 0.10, 0.20, 0.30]
        ratio = ratios[severity]
        occ_img = img_np.copy()
        target_area = int(W * H * ratio)
        # Rectangular patch: aspect ratio between 0.8 and 1.2
        patch_w = int(math.sqrt(target_area * 1.0))
        patch_h = int(target_area / max(1, patch_w))
        patch_w = min(W, patch_w)
        patch_h = min(H, patch_h)

        x0 = (W - patch_w) // 2
        y0 = (H - patch_h) // 2
        # Uniform dark mask
        occ_img[y0 : y0 + patch_h, x0 : x0 + patch_w] = (20, 20, 20)
        return Image.fromarray(occ_img)

    elif family == "resolution_reduction":
        factors = [1.00, 0.75, 0.50, 0.25, 0.15]
        factor = factors[severity]
        down_w = max(16, int(W * factor))
        down_h = max(16, int(H * factor))
        downsampled = cv2.resize(img_np, (down_w, down_h), interpolation=cv2.INTER_AREA)
        upsampled = cv2.resize(downsampled, (W, H), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(upsampled)

    elif family == "perspective_distortion":
        tilts = [0.0, 5.0, 15.0, 25.0, 35.0]
        tilt_deg = tilts[severity]
        # 4-point homography tilting vertical edges inward
        tilt_rad = math.radians(tilt_deg)
        delta_x = int((W * 0.4) * math.sin(tilt_rad))
        delta_y = int((H * 0.2) * math.sin(tilt_rad))

        src_pts = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
        dst_pts = np.float32([
            [delta_x, delta_y],
            [W - delta_x, delta_y],
            [W, H - delta_y],
            [0, H - delta_y],
        ])
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(
            img_np,
            M,
            (W, H),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(30, 30, 30),
        )
        return Image.fromarray(warped)

    elif family == "mixed_degradation":
        # Composite: Blur + Noise + JPEG + Skew
        # Apply blur
        res = apply_degradation(image, "gaussian_blur", severity, seed=seed)
        # Apply noise
        res = apply_degradation(res, "gaussian_noise", severity, seed=seed)
        # Apply jpeg
        res = apply_degradation(res, "jpeg_compression", severity, seed=seed)
        # Apply skew
        res = apply_degradation(res, "skew_rotation", severity, seed=seed)
        return res

    else:
        raise ValueError(f"Unknown degradation family: {family}")
