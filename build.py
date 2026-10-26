"""Stage the static frontend for Vercel."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
if __name__ == "__main__":
    (ROOT / "public").mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "frontend/index.html", ROOT / "public/index.html")

