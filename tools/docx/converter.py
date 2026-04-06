"""DOCX to PDF conversion."""

import subprocess
import sys
from pathlib import Path


def to_pdf(input_path: str, output_path: str) -> str:
    """Convert a DOCX to PDF.

    Tries in order:
    1. docx2pdf (uses Microsoft Word on macOS)
    2. LibreOffice headless
    """
    input_p = Path(input_path)
    output_p = Path(output_path)
    output_p.parent.mkdir(parents=True, exist_ok=True)

    # Try docx2pdf first (requires MS Word on macOS)
    try:
        from docx2pdf import convert
        convert(str(input_p), str(output_p))
        if output_p.exists():
            return str(output_p)
    except Exception:
        pass

    # Try LibreOffice headless
    for lo_path in [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "soffice",
        "libreoffice",
    ]:
        try:
            result = subprocess.run(
                [lo_path, "--headless", "--convert-to", "pdf",
                 "--outdir", str(output_p.parent), str(input_p)],
                capture_output=True, text=True, timeout=60,
            )
            # LibreOffice outputs to same dir with .pdf extension
            lo_output = output_p.parent / f"{input_p.stem}.pdf"
            if lo_output.exists():
                if lo_output != output_p:
                    lo_output.rename(output_p)
                return str(output_p)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    print("Error: DOCX-to-PDF conversion requires Microsoft Word or LibreOffice.", file=sys.stderr)
    print("Install LibreOffice: brew install --cask libreoffice", file=sys.stderr)
    sys.exit(1)
