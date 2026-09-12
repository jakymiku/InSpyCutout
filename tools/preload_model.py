from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = ROOT / "cache"
CACHE_PATHS = {
    "PIP_CACHE_DIR": CACHE_ROOT / "pip",
    "TRANSPARENT_BACKGROUND_FILE_PATH": CACHE_ROOT / "models",
    "TORCH_HOME": CACHE_ROOT / "torch",
    "TORCH_EXTENSIONS_DIR": CACHE_ROOT / "torch_extensions",
    "HF_HOME": CACHE_ROOT / "huggingface",
    "XDG_CACHE_HOME": CACHE_ROOT / "xdg",
}
for key, path in CACHE_PATHS.items():
    path.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault(key, str(path))

try:
    import torch
    from transparent_background import Remover

    if torch.cuda.is_available():
        device = "cuda:0"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    print(f"Preloading InSPyReNet base model on {device}...")
    try:
        Remover(mode="base", device=device, resize="static")
    except TypeError:
        Remover(mode="base", device=device)
    print("Model ready.")
except Exception as exc:
    print(f"Model preload failed: {exc}")
    raise
