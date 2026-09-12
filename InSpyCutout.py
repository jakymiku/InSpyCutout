from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = sorted((ROOT / "src").glob("InSpyCutout.part*.py.txt"))
if not PARTS:
    raise RuntimeError("InSpyCutout source parts are missing.")

source = "".join(part.read_text(encoding="utf-8") for part in PARTS)
exec(compile(source, str(ROOT / "InSpyCutout.full.py"), "exec"), globals(), globals())
