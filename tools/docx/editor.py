"""DOCX editing — find/replace, insert sections, modify styles."""

from docx import Document
from docx.shared import Pt


def find_replace(path: str, replacements: dict, output_path: str) -> str:
    """Replace text in a DOCX. replacements is {old_text: new_text}."""
    doc = Document(path)

    for paragraph in doc.paragraphs:
        for old, new in replacements.items():
            if old in paragraph.text:
                for run in paragraph.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for old, new in replacements.items():
                        if old in paragraph.text:
                            for run in paragraph.runs:
                                if old in run.text:
                                    run.text = run.text.replace(old, new)

    doc.save(output_path)
    return output_path


def append_paragraph(path: str, text: str, output_path: str,
                     style: str = "Normal", bold: bool = False) -> str:
    """Append a paragraph to an existing DOCX."""
    doc = Document(path)
    p = doc.add_paragraph(style=style)
    run = p.add_run(text)
    run.bold = bold
    doc.save(output_path)
    return output_path


def append_heading(path: str, text: str, level: int, output_path: str) -> str:
    """Append a heading to an existing DOCX."""
    doc = Document(path)
    doc.add_heading(text, level=level)
    doc.save(output_path)
    return output_path


def insert_page_break(path: str, output_path: str) -> str:
    """Append a page break to an existing DOCX."""
    doc = Document(path)
    doc.add_page_break()
    doc.save(output_path)
    return output_path
