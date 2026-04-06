"""PDF creation using ReportLab."""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image
)


STYLES = getSampleStyleSheet()

HEADING1 = ParagraphStyle(
    "TenderH1", parent=STYLES["Heading1"],
    fontSize=16, spaceAfter=12, textColor=HexColor("#1a1a2e"),
)
HEADING2 = ParagraphStyle(
    "TenderH2", parent=STYLES["Heading2"],
    fontSize=13, spaceAfter=8, textColor=HexColor("#16213e"),
)
BODY = ParagraphStyle(
    "TenderBody", parent=STYLES["Normal"],
    fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=8,
)
SMALL = ParagraphStyle(
    "TenderSmall", parent=STYLES["Normal"],
    fontSize=9, leading=12, textColor=HexColor("#555555"),
)


def create_from_text(text: str, output_path: str, title: str = "") -> str:
    """Create a simple PDF from plain text."""
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)
    story = []
    if title:
        story.append(Paragraph(title, HEADING1))
        story.append(Spacer(1, 6*mm))

    for line in text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, BODY))
        else:
            story.append(Spacer(1, 3*mm))

    doc.build(story)
    return output_path


def create_proposal(data: dict, output_path: str) -> str:
    """Create a tender proposal PDF from structured data.

    Expected data keys:
        company_name, company_address, tender_title, tender_ref,
        institution, date, sections (list of {heading, content})
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)
    story = []

    # Title page
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph(data.get("tender_title", "Tender Proposal"), HEADING1))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"Submitted to: {data.get('institution', '')}", BODY))
    if data.get("tender_ref"):
        story.append(Paragraph(f"Reference: {data['tender_ref']}", BODY))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"Submitted by: {data.get('company_name', '')}", HEADING2))
    if data.get("company_address"):
        story.append(Paragraph(data["company_address"], BODY))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"Date: {data.get('date', '')}", BODY))
    story.append(PageBreak())

    # Table of Contents placeholder
    story.append(Paragraph("Table of Contents", HEADING1))
    story.append(Spacer(1, 5*mm))
    for i, section in enumerate(data.get("sections", []), 1):
        story.append(Paragraph(f"{i}. {section.get('heading', '')}", BODY))
    story.append(PageBreak())

    # Sections
    for i, section in enumerate(data.get("sections", []), 1):
        story.append(Paragraph(f"{i}. {section.get('heading', '')}", HEADING1))
        story.append(Spacer(1, 3*mm))

        content = section.get("content", "")
        if isinstance(content, list):
            for item in content:
                story.append(Paragraph(f"• {item}", BODY))
        else:
            for para in content.split("\n\n"):
                if para.strip():
                    story.append(Paragraph(para.strip(), BODY))
                    story.append(Spacer(1, 2*mm))

        story.append(Spacer(1, 5*mm))

    doc.build(story)
    return output_path


def create_cover_letter(data: dict, output_path: str) -> str:
    """Create a cover letter PDF.

    Expected data keys:
        company_name, company_address, date, recipient_name,
        recipient_title, institution, institution_address,
        subject, body_paragraphs (list of str), signatory_name, signatory_title
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=2.5*cm, bottomMargin=2.5*cm,
                            leftMargin=3*cm, rightMargin=3*cm)
    story = []

    # Sender
    story.append(Paragraph(data.get("company_name", ""), HEADING2))
    if data.get("company_address"):
        for line in data["company_address"].split("\n"):
            story.append(Paragraph(line, SMALL))
    story.append(Spacer(1, 1*cm))

    # Date
    story.append(Paragraph(data.get("date", ""), BODY))
    story.append(Spacer(1, 8*mm))

    # Recipient
    if data.get("recipient_name"):
        story.append(Paragraph(data["recipient_name"], BODY))
    if data.get("recipient_title"):
        story.append(Paragraph(data["recipient_title"], BODY))
    story.append(Paragraph(data.get("institution", ""), BODY))
    if data.get("institution_address"):
        for line in data["institution_address"].split("\n"):
            story.append(Paragraph(line, BODY))
    story.append(Spacer(1, 8*mm))

    # Subject
    story.append(Paragraph(f"<b>RE: {data.get('subject', '')}</b>", BODY))
    story.append(Spacer(1, 5*mm))

    # Body
    for para in data.get("body_paragraphs", []):
        story.append(Paragraph(para, BODY))
        story.append(Spacer(1, 3*mm))

    # Signature
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Yours faithfully,", BODY))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"<b>{data.get('signatory_name', '')}</b>", BODY))
    story.append(Paragraph(data.get("signatory_title", ""), BODY))

    doc.build(story)
    return output_path


def create_table_pdf(headers: list[str], rows: list[list[str]], output_path: str,
                     title: str = "") -> str:
    """Create a PDF containing a formatted table."""
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []

    if title:
        story.append(Paragraph(title, HEADING1))
        story.append(Spacer(1, 5*mm))

    table_data = [headers] + rows
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f5f5f5")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    doc.build(story)
    return output_path
