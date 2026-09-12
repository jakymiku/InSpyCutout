import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
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

PARTS = sorted((ROOT / "src").glob("InSpyCutout.part*.py.txt"))
if not PARTS:
    raise RuntimeError("InSpyCutout source parts are missing.")

source = "".join(part.read_text(encoding="utf-8") for part in PARTS)
exec(compile(source, str(ROOT / "InSpyCutout.full.py"), "exec"), globals(), globals())
