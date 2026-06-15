#!/usr/bin/env python3
"""
Download and prepare the Stack Overflow Python Questions & Answers dataset.

Usage:
    1. Install Kaggle CLI:  pip install kaggle
    2. Put your kaggle.json in ~/.kaggle/kaggle.json  (from kaggle.com/settings)
    3. Run:  python scripts/download_data.py
"""

import os
import subprocess
import zipfile
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DATASET = "stackoverflow/pythonquestions"
FILES_NEEDED = ["Questions.csv", "Answers.csv"]


def main():
    # Check if data already present
    if all((DATA_DIR / f).exists() for f in FILES_NEEDED):
        print("✓ Dataset already present in ./data/")
        return

    print(f"Downloading dataset: {DATASET}")
    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATASET, "-p", str(DATA_DIR), "--unzip"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("✗ Kaggle CLI error:", result.stderr)
        print("\nManual download instructions:")
        print(f"  1. Go to https://www.kaggle.com/datasets/{DATASET}")
        print("  2. Download and extract the ZIP")
        print("  3. Place Questions.csv and Answers.csv in ./data/")
        raise SystemExit(1)

    print("✓ Download complete")

    # Verify files
    for f in FILES_NEEDED:
        path = DATA_DIR / f
        if path.exists():
            size_mb = path.stat().st_size / 1_048_576
            print(f"  {f}: {size_mb:.1f} MB")
        else:
            print(f"  ✗ Missing: {f}")

    print("\nRun the server — the index will be built automatically on first start.")


if __name__ == "__main__":
    main()
