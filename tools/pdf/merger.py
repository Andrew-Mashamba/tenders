"""PDF merge, split, and page extraction."""

from pypdf import PdfReader, PdfWriter


def merge(input_paths: list[str], output_path: str) -> str:
    """Merge multiple PDFs into one."""
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path


def split(input_path: str, page_ranges: list[tuple[int, int]], output_path: str) -> str:
    """Extract page ranges from a PDF.

    page_ranges: list of (start, end) tuples, 1-indexed inclusive.
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for start, end in page_ranges:
        for i in range(start - 1, min(end, len(reader.pages))):
            writer.add_page(reader.pages[i])
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path


def extract_pages(input_path: str, pages: list[int], output_path: str) -> str:
    """Extract specific pages from a PDF. Pages are 1-indexed."""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for p in pages:
        if 1 <= p <= len(reader.pages):
            writer.add_page(reader.pages[p - 1])
    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path
