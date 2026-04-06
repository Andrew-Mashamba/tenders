#!/usr/bin/env python3
"""Extract text from PDFs in downloads/*/original/ to extracted/."""
import subprocess
import sys
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")

def main():
    for pdf in PROJECT.glob("institutions/*/downloads/*/original/*.pdf"):
        out = pdf.parent.parent / "extracted" / (pdf.stem + ".txt")
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = subprocess.run(
                [sys.executable, "-m", "tools", "pdf", "read", str(pdf)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(PROJECT),
            )
            if r.returncode == 0 and r.stdout.strip():
                out.write_text(r.stdout, encoding="utf-8")
                print(f"Extracted: {pdf.name}")
        except Exception as e:
            print(f"Skip {pdf.name}: {e}")

if __name__ == "__main__":
    main()
