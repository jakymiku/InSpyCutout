from __future__ import annotations

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
