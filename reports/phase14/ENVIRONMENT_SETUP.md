# Phase 14 Isolated Environment Setup & Reproduction Guide

## 1. Motivation for Environment Isolation

In Phases 0 through 13, the primary workspace environment was `.venv` running CPU-only PyTorch `2.14.1+cpu` on Python 3.14.6. To strictly maintain historical immutability and prevent non-reproducible dependency pollution, Phase 14 established a completely isolated virtual environment:
```
c:\Users\ARYAN - AYUSH\OneDrive\Desktop\Nlp\vlm-idp-research\.venv_phase14
```
The legacy `.venv` remains completely untouched, matching the frozen Phase 13 state.

## 2. Environment Construction Procedure

### Step 1: Virtual Environment Creation
```powershell
python -m venv .venv_phase14
```

### Step 2: Native PyTorch CUDA 12.6 Wheel Installation
Because standard PyPI does not distribute CUDA wheels for Python 3.14 Windows by default, the official PyTorch wheel was downloaded and installed directly from the PyTorch nightly/cu126 channel:
- **Wheel**: `torch-2.14.1+cu126-cp314-cp314-win_amd64.whl`
- **Size**: 2,623,168,985 bytes (~2.44 GB)
- **SHA-256**: `14470fc38ad82cb348f9211c47101859bf55d9ea4c45b73e2ca39b89e3ec015c`
```powershell
.\.venv_phase14\Scripts\pip.exe install torch-2.14.1+cu126-cp314-cp314-win_amd64.whl
```

### Step 3: Companion Multimodal & Quantization Stack
```powershell
.\.venv_phase14\Scripts\pip.exe install transformers==4.48.3 tokenizers==0.21.4 huggingface-hub==0.36.2 bitsandbytes==0.50.2 accelerate==1.15.0 torchvision==0.29.1 sentence-transformers==6.1.0 numpy==2.5.3 scipy==1.18.1 pandas==3.0.6 scikit-learn==1.9.1 pillow==12.3.0 pyyaml==6.0.3 matplotlib==3.11.2
```

## 3. Dependency Pin Verification

Key installed versions in `.venv_phase14`:
- `torch`: `2.14.1+cu126` (CUDA 12.6 runtime linked)
- `transformers`: `4.48.3` (configured with `image_seq_len=64` to prevent Idefics3 processor unpacking quirks)
- `bitsandbytes`: `0.50.2` (native Windows 64-bit CUDA kernels compiled)
- `accelerate`: `1.15.0`
- `matplotlib`: `3.11.2`
- `pandas`: `3.0.6`
- `numpy`: `2.5.3`

All dependency pins are recorded in `experiments/phase14/environment/environment_lock.txt` and `requirements_phase14.txt`.
