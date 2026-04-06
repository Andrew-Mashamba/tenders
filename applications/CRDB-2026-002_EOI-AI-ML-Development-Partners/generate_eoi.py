#!/usr/bin/env python3
"""Generate CRDB-2026-002 AI/ML EOI submission PDF for Isale Investment Limited."""

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
    PageBreak, HRFlowable, Image, Frame, PageTemplate
)
from reportlab.platypus.doctemplate import NextPageTemplate

OUT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS/applications/CRDB-2026-002_EOI-AI-ML-Development-Partners")
OUTPUT = OUT_DIR / "ISALE_EOI_CRDB_AI_ML_Partners.pdf"
LOGO = Path("/Volumes/DATA/PROJECTS/TENDERS/isale_investiment_ltd/isale_logo.png")
DATA_FILE = OUT_DIR / "eoi_data.json"

# ─── Brand Colors (Isale green) ───
GREEN_PRIMARY = HexColor("#2E7D32")
GREEN_DARK = HexColor("#1B5E20")
GREEN_LIGHT = HexColor("#E8F5E9")
GREEN_ACCENT = HexColor("#4CAF50")
GREEN_BG = HexColor("#F1F8E9")
WHITE = white
DARK_TEXT = HexColor("#1a1a1a")
GREY_TEXT = HexColor("#555555")
GREY_BORDER = HexColor("#C8E6C9")

# ─── Styles ───
styles = getSampleStyleSheet()

TITLE = ParagraphStyle("Title2", parent=styles["Title"], fontSize=22, spaceAfter=6,
                        textColor=GREEN_DARK, leading=26, fontName="Helvetica-Bold")
SUBTITLE = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=14, spaceAfter=12,
                           textColor=DARK_TEXT, alignment=TA_CENTER)
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, spaceAfter=10,
                      textColor=GREEN_DARK, spaceBefore=16, fontName="Helvetica-Bold")
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceAfter=8,
                      textColor=GREEN_PRIMARY, spaceBefore=12, fontName="Helvetica-Bold")
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontSize=11, spaceAfter=6,
                      textColor=GREEN_PRIMARY, spaceBefore=8, fontName="Helvetica-Bold")
BODY = ParagraphStyle("Body2", parent=styles["Normal"], fontSize=10.5, leading=14.5,
                       alignment=TA_JUSTIFY, spaceAfter=6, textColor=DARK_TEXT)
SMALL = ParagraphStyle("Small2", parent=styles["Normal"], fontSize=9, leading=12,
                        textColor=GREY_TEXT, spaceAfter=4)
BULLET = ParagraphStyle("Bullet2", parent=BODY, leftIndent=18, bulletIndent=6,
                          spaceBefore=2, spaceAfter=2)
CENTER = ParagraphStyle("Center2", parent=BODY, alignment=TA_CENTER)

CELL = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=9.5, leading=12.5,
                       alignment=TA_LEFT, spaceAfter=0, spaceBefore=0, textColor=DARK_TEXT)
CELL_BOLD = ParagraphStyle("CellBold", parent=CELL, fontName="Helvetica-Bold")
CELL_HDR = ParagraphStyle("CellHdr", parent=CELL, fontName="Helvetica-Bold",
                            fontSize=10, textColor=white)
CELL_FORM_LABEL = ParagraphStyle("CellFormLabel", parent=CELL, fontName="Helvetica-Bold")

HDR_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GREEN_DARK),
    ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_BORDER),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GREEN_BG]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
])

FORM_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), GREEN_LIGHT),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_BORDER),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
])

# CRDB template table style (grey headers as per original)
CRDB_TEMPLATE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#4a4a4a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("BACKGROUND", (0, 1), (0, -1), GREEN_LIGHT),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_BORDER),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
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
        col_widths = [7*cm, 10*cm]
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


def make_crdb_table(data, col_widths=None):
    """CRDB template-style table with dark header and green label column."""
    wrapped = []
    for i, row in enumerate(data):
        if i == 0:
            wrapped.append(_wrap_row(row, is_header=True))
        else:
            wrapped.append(_wrap_row(row, is_form_label=True))
    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    t.setStyle(CRDB_TEMPLATE)
    return t


# ─── Header / Footer ───
def header_footer(canvas, doc):
    canvas.saveState()
    page_width, page_height = A4

    if LOGO.exists():
        canvas.drawImage(str(LOGO), 2.5*cm, page_height - 1.8*cm, width=1.4*cm, height=1.4*cm,
                         preserveAspectRatio=True, mask='auto')
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(GREEN_DARK)
    canvas.drawString(4.2*cm, page_height - 1.25*cm, "Isale Investment Limited")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(4.2*cm, page_height - 1.55*cm, "Business, Investments and Technology")

    canvas.setStrokeColor(GREEN_PRIMARY)
    canvas.setLineWidth(1.5)
    canvas.line(2.5*cm, page_height - 2*cm, page_width - 2.5*cm, page_height - 2*cm)

    canvas.setStrokeColor(GREEN_PRIMARY)
    canvas.setLineWidth(1)
    canvas.line(2.5*cm, 1.6*cm, page_width - 2.5*cm, 1.6*cm)

    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(2.5*cm, 1.2*cm,
                      "Isale Investment Limited | Plot 83, Ada Estate, Dar es Salaam | +255 620 300 000 | victor@isalegroup.co.tz")
    canvas.drawRightString(page_width - 2.5*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()


def header_footer_cover(canvas, doc):
    canvas.saveState()
    page_width, _ = A4
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawCentredString(page_width / 2, 1.2*cm, "CONFIDENTIAL — Isale Investment Limited")
    canvas.restoreState()


def add_content(story, text):
    """Parse text with bullets and sub-headings into story elements."""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("• "):
            bullet_text = line[2:].strip()
            safe = bullet_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"<bullet>&bull;</bullet> {safe}", BULLET))
        elif line.endswith(":") and len(line) < 80 and not line.startswith(" "):
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"<b>{safe}</b>", BODY))
        else:
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, BODY))


def build():
    with open(DATA_FILE) as f:
        data = json.load(f)

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
                            topMargin=2.5*cm, bottomMargin=2.3*cm,
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
    story.append(Spacer(1, 2*cm))

    if LOGO.exists():
        story.append(Image(str(LOGO), width=4*cm, height=4*cm))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("EXPRESSION OF INTEREST", TITLE))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="60%", thickness=3, color=GREEN_PRIMARY))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph(
        "AI/ML Development and<br/>Implementation Partners",
        ParagraphStyle("CoverSub", parent=SUBTITLE, fontSize=16, leading=20, textColor=GREEN_PRIMARY)
    ))
    story.append(Spacer(1, 8*mm))

    cover_data = [
        ["Submitted To", data["institution"]],
        ["Reference", data["tender_ref"]],
        ["Submitted By", data["company_name"]],
        ["Date", data["date"]],
        ["Contact", "Victor Tesha, CEO | +255 620 300 000 | victor@isalegroup.co.tz"],
    ]
    story.append(make_form_table(cover_data, col_widths=[4.5*cm, 10.5*cm]))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph(
        "<i>Open for International Competitive Bidding</i>",
        CENTER
    ))

    # ════════════════════════════════════════════════════════════════
    # SECTION 1 — COMPANY PROFILE (CRDB Template)
    # ════════════════════════════════════════════════════════════════
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    story.append(Paragraph("Section 1 — Company Profile", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "As prescribed by the CRDB Bank EOI template (Section 2.4.1):",
        SMALL
    ))
    story.append(Spacer(1, 3*mm))

    cp = data["company_profile"]

    # Company Profile table — matching CRDB template
    profile_data = [
        ["Company Profile", "Details"],
        ["Company Name", cp["company_name"]],
        ["Company Location", cp["company_location"]],
        ["Registered Office Address", cp["registered_office"]],
        ["Key Contact (Email)", cp["key_contact_email"]],
        ["Key Contact (Phone)", cp["key_contact_phone"]],
        ["Key Contact Person", cp["key_contact_person"]],
        ["Association (Joint Venture\nor Subcontracting)", "No. Isale Investment Limited is submitting\nas a sole bidder without JV or subcontracting arrangements."],
    ]
    story.append(make_crdb_table(profile_data, col_widths=[6*cm, W - 6*cm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Experience", H2))

    exp_data = [
        ["Experience", "Details"],
        ["Number of years in business", cp["years_in_business"]],
        ["Years providing AI/ML implementations", cp["years_providing_ai_ml"]],
        ["Number of clients", cp["number_of_clients"]],
        ["Clients using AI/ML solutions", cp["number_of_clients_ai_ml"]],
    ]
    story.append(make_crdb_table(exp_data, col_widths=[6*cm, W - 6*cm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Terminated Projects", H2))
    term_data = [
        ["Terminated Projects", "Details"],
        ["Disclosure", cp["terminated_projects"]],
    ]
    story.append(make_crdb_table(term_data, col_widths=[6*cm, W - 6*cm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Audited Financial Statements", H2))
    fin_data = [
        ["Year", "Status"],
        ["2025", cp["financial_2025"]],
        ["2024", cp["financial_2024"]],
        ["2023", cp["financial_2023"]],
    ]
    story.append(make_crdb_table(fin_data, col_widths=[6*cm, W - 6*cm]))

    # ════════════════════════════════════════════════════════════════
    # COMPANY BACKGROUND
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Company Background", H2))

    add_content(story, """Isale Investment Limited (formerly Leeds Company Limited) is a Tanzanian-registered ICT services and business consulting firm incorporated on 1st October 2018 (Registration No. 137771411). The company specializes in banking technology solutions, enterprise software implementation, AI/ML solutions development, and digital transformation.

Isale holds a Payment Service Provider (PSP) licence (NBPSL No. 0000-70) issued by the Bank of Tanzania, valid through 25th August 2030, authorizing the provision of payment system services across Mainland Tanzania and Tanzania Zanzibar. The company is VAT-registered (VRN: 40-313410-P) and holds a current ICT Services business licence from Kinondoni Municipal Council.

The company maintains offices in Dar es Salaam, Tanzania and Dubai, UAE (Le Solerium Towers, Dubai Silicon Oasis), enabling delivery across East Africa and the wider region.

Isale's technology division, Isale Digital, delivers AI/ML solutions, banking technology, business solutions (ERP, CRM, supply chain management), and government digital transformation solutions. The company's AI practice focuses on:

• Conversational AI — Production platform with 40+ industry-specific AI agents deployed across WhatsApp, web chat, and API channels, including financial services agents for microfinance, insurance, and accounting
• Machine Learning for Financial Services — Credit scoring models, fraud detection, customer analytics, and predictive forecasting for banking institutions
• Banking Technology Integration — RTGS, TIPS, GePG, and NIDA integrations with Bank of Tanzania systems, loan management, SACCOS/microfinance platforms
• Natural Language Processing — Bilingual NLP (English and Swahili) for chatbots, document processing, and intelligent automation
• Agentic AI — Autonomous AI agents that execute multi-step workflows with tool-use capabilities, audit trails, and human-in-the-loop controls""")

    # Team
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Key Team Members", H2))

    team_data = [
        ["Name", "Role", "Qualifications & Experience"],
        ["Victor Tesha", "CEO / Project Director",
         "MBA (Marketing), BA Social Science. 10+ years banking (NBC Bank, Azania Bank, UBA Tanzania, ICB Tanzania). Spearheaded NBC's 2013-2018 strategic turnaround. Expertise in credit risk management, commercial banking, digital transformation."],
        ["Prem Ruparelia", "Director / Strategic Advisor",
         "MA Corporate Strategy & Governance, MCIPS (UK). 20+ years (NatWest Bank, DHL, BAE Systems, Roche Pharmaceuticals). Expertise in investment management, operating model redesign, large-scale transformation."],
    ]
    story.append(make_hdr_table(team_data, col_widths=[3*cm, 3.5*cm, W - 6.5*cm]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<i>The team is augmented with specialist AI/ML engineers, data scientists, NLP researchers, "
        "and banking integration specialists as required.</i>",
        SMALL
    ))

    # ════════════════════════════════════════════════════════════════
    # SECTION 2 — APPROACH AND METHODOLOGY
    # ════════════════════════════════════════════════════════════════
    for section in data["sections"]:
        story.append(PageBreak())
        heading = section["heading"]

        # Map to CRDB's required methodology sections
        section_map = {
            "Understanding of Business Needs": "2.1",
            "Solution Design & Development": "2.2",
            "Governance, Compliance & Ethics": "2.3",
            "Technology & Tools": "2.4",
            "Project Management Approach": "2.5",
            "Knowledge Transfer & Sustainability": "2.6",
        }
        prefix = section_map.get(heading, "")
        if prefix:
            story.append(Paragraph(f"Section {prefix} — {heading}", H1))
        else:
            story.append(Paragraph(heading, H1))

        story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
        story.append(Spacer(1, 4*mm))

        add_content(story, section["content"])

    # ════════════════════════════════════════════════════════════════
    # AI/ML USE CASES SUMMARY TABLE
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix — AI/ML Use Cases for CRDB Bank", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "Summary of proposed AI/ML use cases aligned with CRDB Bank's strategic priorities:",
        BODY
    ))
    story.append(Spacer(1, 3*mm))

    uc_data = [
        ["Use Case", "Business Value", "Technology", "Timeline"],
        ["Fraud Detection\n& Prevention",
         "Reduce fraud losses by 40-60%.\nReal-time transaction scoring.\nAutomated alert generation.",
         "Anomaly detection,\nbehavioural analytics,\nApache Kafka streaming",
         "Phase 1\n(Weeks 5-14)"],
        ["Credit Scoring\n& Risk Assessment",
         "Improve credit accuracy by 20-30%.\nAlternative data integration.\nExplainable AI for compliance.",
         "XGBoost, LightGBM,\nSHAP explainability,\nalternative data features",
         "Phase 1\n(Weeks 5-14)"],
        ["Conversational AI\n(Chatbots)",
         "Automate 60-70% of routine inquiries.\nBilingual (English/Swahili).\n24/7 customer service.",
         "LLMs, NLP,\nWhatsApp Business API,\nweb chat, Simbanking",
         "Phase 1\n(Weeks 5-14)"],
        ["Customer Analytics\n& Segmentation",
         "Increase cross-sell by 15-25%.\nChurn prediction.\nNext-best-product engine.",
         "Clustering, classification,\nrecommendation systems,\nreal-time scoring",
         "Phase 2\n(Weeks 15-30)"],
        ["Financial Forecasting",
         "Improve forecast accuracy by 20%.\nCash flow & liquidity prediction.\nMarket risk analysis.",
         "LSTM, Prophet,\ntime-series models,\nBI dashboard integration",
         "Phase 2\n(Weeks 15-30)"],
        ["Agentic AI\nWorkflows",
         "Automate multi-step processes.\nLoan origination automation.\nCompliance workflow agents.",
         "LangChain/LangGraph,\ntool-use LLMs,\naudit trail systems",
         "Phase 3\n(Weeks 31-44)"],
    ]
    story.append(make_hdr_table(uc_data, col_widths=[3*cm, 4.5*cm, 4*cm, W - 11.5*cm]))

    # Track record summary
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Production AI/ML Track Record", H2))

    track_data = [
        ["Capability", "Evidence"],
        ["Conversational AI Agents", "40+ production agents across financial services, healthcare, agriculture, government. Bilingual NLP (English/Swahili). WhatsApp, web, API deployment."],
    ]
    story.append(make_hdr_table(track_data, col_widths=[4*cm, W - 4*cm]))

    # ════════════════════════════════════════════════════════════════
    # BUILD
    # ════════════════════════════════════════════════════════════════
    doc.multiBuild(story)
    size_kb = OUTPUT.stat().st_size // 1024
    print(f"EOI PDF generated: {OUTPUT}")
    print(f"Size: {size_kb} KB")


if __name__ == "__main__":
    build()
