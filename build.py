"""Create demo data and stage the static frontend for Vercel."""
import os
from pathlib import Path
import shutil
from database import create_database

ROOT = Path(__file__).resolve().parent
if __name__ == "__main__":
    os.chdir(ROOT)
    create_database()
    (ROOT / "public").mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "frontend/index.html", ROOT / "public/index.html")
