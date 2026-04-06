"""DOCX reading and text extraction."""

from docx import Document


def extract_text(path: str) -> str:
    """Extract all text from a DOCX file."""
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def extract_structure(path: str) -> dict:
    """Extract structured content: headings, paragraphs, tables."""
    doc = Document(path)
    elements = []

    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        style = para.style.name if para.style else "Normal"
        elements.append({
            "type": "heading" if "Heading" in style else "paragraph",
            "style": style,
            "text": para.text,
            "bold": any(run.bold for run in para.runs),
        })

    tables = extract_tables(path)

    return {"elements": elements, "tables": tables}


def extract_tables(path: str) -> list[list[list[str]]]:
    """Extract all tables from a DOCX as list of tables, each a list of rows."""
    doc = Document(path)
    tables = []
    for table in doc.tables:
        rows = []
        for row in table.rows:
            rows.append([cell.text.strip() for cell in row.cells])
        tables.append(rows)
    return tables
