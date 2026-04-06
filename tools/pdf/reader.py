"""PDF reading and text extraction."""

import json
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


def extract_text(path: str, pages: list[int] | None = None) -> str:
    """Extract text from a PDF file using pdfplumber."""
    with pdfplumber.open(path) as pdf:
        result = []
        for i, page in enumerate(pdf.pages):
            if pages and (i + 1) not in pages:
                continue
            text = page.extract_text()
            if text:
                result.append(f"--- Page {i + 1} ---\n{text}")
    return "\n\n".join(result)


def extract_tables(path: str, pages: list[int] | None = None) -> list[dict]:
    """Extract tables from a PDF as list of dicts."""
    tables = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            if pages and (i + 1) not in pages:
                continue
            for table in page.extract_tables():
                if not table or len(table) < 2:
                    continue
                headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(table[0])]
                rows = []
                for row in table[1:]:
                    rows.append({
                        headers[j]: (str(cell).strip() if cell else "")
                        for j, cell in enumerate(row)
                        if j < len(headers)
                    })
                tables.append({"page": i + 1, "headers": headers, "rows": rows})
    return tables


def get_metadata(path: str) -> dict:
    """Get PDF metadata."""
    reader = PdfReader(path)
    meta = reader.metadata
    return {
        "pages": len(reader.pages),
        "title": meta.title if meta else None,
        "author": meta.author if meta else None,
        "subject": meta.subject if meta else None,
        "creator": meta.creator if meta else None,
        "producer": meta.producer if meta else None,
        "encrypted": reader.is_encrypted,
    }


def get_page_count(path: str) -> int:
    """Get the number of pages in a PDF."""
    return len(PdfReader(path).pages)
