#!/usr/bin/env python3
"""Generate MABUMBE-2026-006 proposal PDF for ZIMA Solutions Limited."""

import sys
sys.path.insert(0, "/Volumes/DATA/PROJECTS/TENDERS")

import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Frame, PageTemplate, KeepTogether
)
from reportlab.platypus.doctemplate import NextPageTemplate

OUT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS/applications/MABUMBE-2026-006_Coop-Bank-Data-Analytics-AI-Assessment")
OUTPUT = OUT_DIR / "ZIMA_Proposal_CoopBank_AI_Maturity.pdf"
DATA_FILE = OUT_DIR / "proposal_data.json"

# ─── ZIMA Brand Colors (Blue/Tech theme) ───
BLUE_PRIMARY = HexColor("#1565C0")      # Primary blue
BLUE_DARK = HexColor("#0D47A1")         # Dark blue for headings
BLUE_LIGHT = HexColor("#E3F2FD")        # Light blue for table rows
BLUE_ACCENT = HexColor("#42A5F5")       # Accent blue
BLUE_BG = HexColor("#F5F9FF")           # Very light blue background
WHITE = white
DARK_TEXT = HexColor("#1a1a1a")
GREY_TEXT = HexColor("#555555")
GREY_BORDER = HexColor("#BBDEFB")       # Blue-tinted border

# ─── Styles ───
styles = getSampleStyleSheet()

TITLE = ParagraphStyle("Title2", parent=styles["Title"], fontSize=22, spaceAfter=6,
                        textColor=BLUE_DARK, leading=26, fontName="Helvetica-Bold")
SUBTITLE = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=14, spaceAfter=12,
                           textColor=DARK_TEXT, alignment=TA_CENTER)
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, spaceAfter=10,
                      textColor=BLUE_DARK, spaceBefore=16, fontName="Helvetica-Bold")
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceAfter=8,
                      textColor=BLUE_PRIMARY, spaceBefore=12, fontName="Helvetica-Bold")
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontSize=11, spaceAfter=6,
                      textColor=BLUE_PRIMARY, spaceBefore=8, fontName="Helvetica-Bold")
BODY = ParagraphStyle("Body2", parent=styles["Normal"], fontSize=10.5, leading=14.5,
                       alignment=TA_JUSTIFY, spaceAfter=6, textColor=DARK_TEXT)
SMALL = ParagraphStyle("Small2", parent=styles["Normal"], fontSize=9, leading=12,
                        textColor=GREY_TEXT, spaceAfter=4)
BULLET = ParagraphStyle("Bullet2", parent=BODY, leftIndent=18, bulletIndent=6,
                          spaceBefore=2, spaceAfter=2)
CENTER = ParagraphStyle("Center2", parent=BODY, alignment=TA_CENTER)

# Cell styles
CELL = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=9.5, leading=12.5,
                       alignment=TA_LEFT, spaceAfter=0, spaceBefore=0, textColor=DARK_TEXT)
CELL_BOLD = ParagraphStyle("CellBold", parent=CELL, fontName="Helvetica-Bold")
CELL_HDR = ParagraphStyle("CellHdr", parent=CELL, fontName="Helvetica-Bold",
                            fontSize=10, textColor=white)
CELL_FORM_LABEL = ParagraphStyle("CellFormLabel", parent=CELL, fontName="Helvetica-Bold")

# Table styles
HDR_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BLUE_DARK),
    ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_BORDER),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BLUE_BG]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
])

FORM_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), BLUE_LIGHT),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_BORDER),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
])


def _wrap_cell(text, style):
    if isinstance(text, Paragraph):
        return text
    safe = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe = safe.replace("\n", "<br/>")
    return Paragraph(safe, style)


def _wrap_row(row, is_header=False, is_form_label=False):
    result = []
    for i, cell in enumerate(row):
        if is_header:
            result.append(_wrap_cell(cell, CELL_HDR))
        elif i == 0 and is_form_label:
            result.append(_wrap_cell(cell, CELL_FORM_LABEL))
        else:
            result.append(_wrap_cell(cell, CELL))
    return result


def make_form_table(data, col_widths=None):
    if col_widths is None:
        col_widths = [6*cm, 10.5*cm]
    wrapped = [_wrap_row(row, is_form_label=True) for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=0)
    t.setStyle(FORM_STYLE)
    return t


def make_hdr_table(data, col_widths=None):
    wrapped = []
    for i, row in enumerate(data):
        wrapped.append(_wrap_row(row, is_header=(i == 0)))
    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    t.setStyle(HDR_STYLE)
    return t


# ─── Header / Footer ───
def header_footer(canvas, doc):
    canvas.saveState()
    page_width, page_height = A4

    # Header — ZIMA text brand (no logo file)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(BLUE_DARK)
    canvas.drawString(2.5*cm, page_height - 1.3*cm, "ZIMA")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(BLUE_PRIMARY)
    canvas.drawString(4.2*cm, page_height - 1.1*cm, "SOLUTIONS")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(4.2*cm, page_height - 1.45*cm, "Build Your Future")

    # Blue header line
    canvas.setStrokeColor(BLUE_PRIMARY)
    canvas.setLineWidth(1.5)
    canvas.line(2.5*cm, page_height - 1.7*cm, page_width - 2.5*cm, page_height - 1.7*cm)

    # Footer
    canvas.setStrokeColor(BLUE_PRIMARY)
    canvas.setLineWidth(1)
    canvas.line(2.5*cm, 1.6*cm, page_width - 2.5*cm, 1.6*cm)

    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(2.5*cm, 1.2*cm,
                      "ZIMA Solutions Limited | Makongo, Dar es Salaam | +255 69 241 0353 | info@zima.co.tz | zima.co.tz")
    canvas.drawRightString(page_width - 2.5*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()


def header_footer_cover(canvas, doc):
    canvas.saveState()
    page_width, _ = A4
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawCentredString(page_width / 2, 1.2*cm, "CONFIDENTIAL — ZIMA Solutions Limited")
    canvas.restoreState()


def add_content(story, text):
    """Parse text with bullets and sub-headings into story elements."""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("• ") or line.startswith("— "):
            bullet_text = line[2:].strip()
            safe = bullet_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"<bullet>&bull;</bullet> {safe}", BULLET))
        elif line.endswith(":") and len(line) < 80 and not line.startswith("  "):
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"<b>{safe}</b>", BODY))
        else:
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, BODY))


def build():
    with open(DATA_FILE) as f:
        data = json.load(f)

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
                            topMargin=2.2*cm, bottomMargin=2.3*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    doc.addPageTemplates([
        PageTemplate(id='cover', frames=frame, onPage=header_footer_cover),
        PageTemplate(id='content', frames=frame, onPage=header_footer),
    ])

    story = []
    W = doc.width

    # ════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 3*cm))

    # ZIMA text logo on cover
    story.append(Paragraph(
        '<font size="36" color="#0D47A1"><b>ZIMA</b></font> '
        '<font size="18" color="#1565C0">SOLUTIONS</font>',
        ParagraphStyle("LogoStyle", parent=styles["Normal"], alignment=TA_CENTER, spaceAfter=4)
    ))
    story.append(Paragraph(
        '<font size="11" color="#555555"><i>Build Your Future</i></font>',
        ParagraphStyle("TagStyle", parent=styles["Normal"], alignment=TA_CENTER, spaceAfter=8)
    ))
    story.append(Spacer(1, 1*cm))

    story.append(HRFlowable(width="60%", thickness=3, color=BLUE_PRIMARY))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph("TECHNICAL PROPOSAL", TITLE))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "Consultancy Services for<br/>Data Analytics &amp; AI Maturity Assessment",
        ParagraphStyle("CoverSub", parent=SUBTITLE, fontSize=16, leading=20, textColor=BLUE_PRIMARY)
    ))
    story.append(Spacer(1, 8*mm))

    cover_data = [
        ["Submitted To", data["institution"]],
        ["Tender Reference", data["tender_ref"]],
        ["Submitted By", data["company_name"]],
        ["Date", data["date"]],
        ["Contact", "+255 69 241 0353 | info@zima.co.tz"],
    ]
    story.append(make_form_table(cover_data, col_widths=[4.5*cm, 10.5*cm]))

    # ════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════════════
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    story.append(Paragraph("Table of Contents", H1))
    story.append(Spacer(1, 5*mm))

    toc_items = [
        ("1", "Executive Summary"),
        ("2", "Company Profile"),
        ("3", "Understanding of Coop Bank's Requirements"),
        ("4", "Proposed Methodology"),
        ("5", "ZIMA's AI Expertise & Credentials"),
        ("6", "Proposed Team"),
        ("7", "Deliverables Summary"),
        ("8", "Timeline & Investment"),
        ("9", "Why ZIMA Solutions"),
        ("A", "AI Agents Portfolio Summary"),
        ("B", "Administrative Documents"),
    ]
    toc_data = [["Section", "Title"]]
    for num, title in toc_items:
        toc_data.append([num, title])
    story.append(make_hdr_table(toc_data, col_widths=[2*cm, W - 2*cm]))

    # ════════════════════════════════════════════════════════════════
    # MAIN SECTIONS from JSON data
    # ════════════════════════════════════════════════════════════════
    section_num = 1
    for section in data["sections"]:
        story.append(PageBreak())
        heading = section["heading"]
        story.append(Paragraph(f"{section_num}. {heading}", H1))
        story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE_PRIMARY))
        story.append(Spacer(1, 4*mm))

        add_content(story, section["content"])
        section_num += 1

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A — AI AGENTS PORTFOLIO
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix A — ZIMA AI Agents Portfolio", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE_PRIMARY))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "ZIMA's Zona platform operates 40+ production AI agents across multiple industries. "
        "The following highlights our financial services and enterprise agents most relevant to Coop Bank's assessment:",
        BODY
    ))
    story.append(Spacer(1, 3*mm))

    agents_data = [
        ["Agent", "Sector", "Key Capabilities"],
        ["LoanGuide", "Microfinance / Banking",
         "Loan status tracking, repayment reminders, balance inquiries, payment processing via conversational AI"],
        ["InsureBot", "Insurance",
         "Policy queries, claims filing, premium reminders, document collection via WhatsApp/web"],
        ["AccountantAI", "Financial Services",
         "Invoice status tracking, tax reminders, financial document processing, reporting automation"],
        ["CivicBot", "Government",
         "Permit applications, bill payments, complaint management — demonstrates public-sector data integration"],
        ["FarmLink", "Agriculture",
         "Input ordering, market price intelligence, weather alerts — relevant to Coop Bank's agricultural lending"],
        ["ShopAssist", "Retail / E-Commerce",
         "Product search, stock management, returns processing — demonstrates retail analytics and recommendation engine"],
    ]
    story.append(make_hdr_table(agents_data, col_widths=[2.5*cm, 3.5*cm, W - 6*cm]))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("<b>Technology Stack:</b>", BODY))

    tech_data = [
        ["Component", "Technology"],
        ["AI/NLP Engine", "Large Language Models, intent recognition, entity extraction"],
        ["Channels", "WhatsApp Business API, web chat widgets, RESTful APIs"],
        ["Languages", "English and Swahili (bilingual NLP)"],
        ["Integration", "Core banking APIs, mobile money, payment gateways, SMTP"],
        ["Infrastructure", "Cloud-hosted, 99.9% uptime, auto-scaling"],
        ["Data Processing", "Real-time conversational data, transaction analytics, reporting pipelines"],
    ]
    story.append(make_hdr_table(tech_data, col_widths=[3.5*cm, W - 3.5*cm]))

    # ════════════════════════════════════════════════════════════════
    # APPENDIX B — ADMINISTRATIVE DOCUMENTS
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix B — Administrative Documents", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE_PRIMARY))
    story.append(Spacer(1, 4*mm))

    admin_data = [
        ["#", "Document", "Status"],
        ["1", "Company Profile", "Enclosed (Section 2)"],
        ["2", "Certificate of Incorporation (Reg. No. 181314605)", "Annexed"],
        ["3", "Memorandum and Articles of Association", "Annexed"],
        ["4", "Tax Identification Number (TIN: 181-314-605)", "Annexed"],
        ["5", "Business Licence (ICT Services, Kinondoni MC)", "Annexed"],
        ["6", "Company Directors and Shareholders", "Enclosed (Section 6)"],
        ["7", "Key Contact Persons", "Enclosed (below)"],
    ]
    story.append(make_hdr_table(admin_data, col_widths=[1*cm, 9*cm, W - 10*cm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Key Contact Persons", H2))
    contacts_data = [
        ["Name", "Title", "Phone", "Email"],
        ["Andrew Mashamba", "Founder & CEO", "+255 69 241 0353", "info@zima.co.tz"],
        ["Caroline Shija", "Co-Director", "—", "info@zima.co.tz"],
    ]
    story.append(make_hdr_table(contacts_data, col_widths=[4*cm, 3.5*cm, 3.5*cm, W - 11*cm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Company Registration Details", H2))
    reg_data = [
        ["Registration Number", "181314605"],
        ["Date of Incorporation", "17 January 2025"],
        ["TIN", "181-314-605"],
        ["Business Licence", "BL01396912024-2500021919"],
        ["Licence Type", "ICT Services (Local)"],
        ["Registered Office", "Makongo, Near Ardhi University, Kinondoni, Dar es Salaam"],
        ["Share Capital", "TZS 1,000,000 (10,000 shares @ TZS 100)"],
    ]
    story.append(make_form_table(reg_data, col_widths=[5*cm, W - 5*cm]))

    # ════════════════════════════════════════════════════════════════
    # BUILD
    # ════════════════════════════════════════════════════════════════
    doc.multiBuild(story)
    size_kb = OUTPUT.stat().st_size // 1024
    print(f"Proposal PDF generated: {OUTPUT}")
    print(f"Size: {size_kb} KB")


if __name__ == "__main__":
    build()
