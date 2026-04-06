"""DOCX document creation."""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def create_proposal(data: dict, output_path: str) -> str:
    """Create a tender proposal DOCX from structured data.

    Expected data keys:
        company_name, company_address, tender_title, tender_ref,
        institution, date, sections (list of {heading, content})
    """
    doc = Document()

    # Set default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)

    # Title page
    for _ in range(6):
        doc.add_paragraph()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(data.get("tender_title", "Tender Proposal"))
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = RGBColor(26, 26, 46)

    doc.add_paragraph()

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run(f"Submitted to: {data.get('institution', '')}").font.size = Pt(13)

    if data.get("tender_ref"):
        ref = doc.add_paragraph()
        ref.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ref.add_run(f"Reference: {data['tender_ref']}").font.size = Pt(12)

    for _ in range(3):
        doc.add_paragraph()

    by = doc.add_paragraph()
    by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = by.add_run(f"Submitted by: {data.get('company_name', '')}")
    run.bold = True
    run.font.size = Pt(14)

    if data.get("company_address"):
        addr = doc.add_paragraph()
        addr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        addr.add_run(data["company_address"]).font.size = Pt(11)

    date_p = doc.add_paragraph()
    date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_p.add_run(f"Date: {data.get('date', '')}").font.size = Pt(11)

    doc.add_page_break()

    # Table of contents
    doc.add_heading("Table of Contents", level=1)
    for i, section in enumerate(data.get("sections", []), 1):
        doc.add_paragraph(f"{i}. {section.get('heading', '')}")
    doc.add_page_break()

    # Sections
    for i, section in enumerate(data.get("sections", []), 1):
        doc.add_heading(f"{i}. {section.get('heading', '')}", level=1)

        content = section.get("content", "")
        if isinstance(content, list):
            for item in content:
                p = doc.add_paragraph(style="List Bullet")
                p.add_run(item)
        else:
            for para in content.split("\n\n"):
                if para.strip():
                    p = doc.add_paragraph()
                    p.add_run(para.strip())

    doc.save(output_path)
    return output_path


def create_cover_letter(data: dict, output_path: str) -> str:
    """Create a cover letter DOCX.

    Expected data keys:
        company_name, company_address, date, recipient_name,
        recipient_title, institution, institution_address,
        subject, body_paragraphs (list of str), signatory_name, signatory_title
    """
    doc = Document()

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    # Sender
    sender = doc.add_paragraph()
    run = sender.add_run(data.get("company_name", ""))
    run.bold = True
    run.font.size = Pt(13)

    if data.get("company_address"):
        for line in data["company_address"].split("\n"):
            p = doc.add_paragraph()
            run = p.add_run(line)
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(85, 85, 85)

    doc.add_paragraph()

    # Date
    doc.add_paragraph(data.get("date", ""))
    doc.add_paragraph()

    # Recipient
    if data.get("recipient_name"):
        doc.add_paragraph(data["recipient_name"])
    if data.get("recipient_title"):
        doc.add_paragraph(data["recipient_title"])
    doc.add_paragraph(data.get("institution", ""))
    if data.get("institution_address"):
        for line in data["institution_address"].split("\n"):
            doc.add_paragraph(line)

    doc.add_paragraph()

    # Subject
    subj = doc.add_paragraph()
    run = subj.add_run(f"RE: {data.get('subject', '')}")
    run.bold = True
    run.underline = True

    doc.add_paragraph()

    # Body
    for para in data.get("body_paragraphs", []):
        p = doc.add_paragraph()
        p.add_run(para)

    # Signature
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph("Yours faithfully,")
    doc.add_paragraph()
    doc.add_paragraph()

    sig = doc.add_paragraph()
    run = sig.add_run(data.get("signatory_name", ""))
    run.bold = True

    doc.add_paragraph(data.get("signatory_title", ""))

    doc.save(output_path)
    return output_path


def create_from_template(template_path: str, data: dict, output_path: str) -> str:
    """Create a DOCX by replacing {{placeholders}} in an existing template.

    Replaces {{key}} patterns in paragraphs and table cells with values from data.
    """
    doc = Document(template_path)

    def replace_in_paragraph(paragraph):
        full_text = paragraph.text
        for key, value in data.items():
            placeholder = "{{" + key + "}}"
            if placeholder in full_text:
                full_text = full_text.replace(placeholder, str(value))
        if full_text != paragraph.text:
            for run in paragraph.runs:
                run.text = ""
            if paragraph.runs:
                paragraph.runs[0].text = full_text

    for paragraph in doc.paragraphs:
        replace_in_paragraph(paragraph)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_in_paragraph(paragraph)

    doc.save(output_path)
    return output_path


def add_table(output_path: str, headers: list[str], rows: list[list[str]],
              existing_path: str | None = None) -> str:
    """Create or append a formatted table to a DOCX."""
    doc = Document(existing_path) if existing_path else Document()

    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Headers
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        for run in cell.paragraphs[0].runs:
            run.bold = True

    # Rows
    for row_data in rows:
        row = table.add_row()
        for i, value in enumerate(row_data):
            if i < len(row.cells):
                row.cells[i].text = str(value)

    doc.save(output_path)
    return output_path
