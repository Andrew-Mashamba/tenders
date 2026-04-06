#!/usr/bin/env python3
"""Generate NBC-2026-001 RFP submission PDF for Isale Investment Limited."""

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
    PageBreak, HRFlowable, Image, Frame, PageTemplate, KeepTogether
)
from reportlab.pdfgen import canvas as pdfcanvas

OUT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS/applications/NBC-2026-001_RFP-Credit-Origination-Platform")
OUTPUT = OUT_DIR / "ISALE_RFP_NBC_Credit_Platform.pdf"
LOGO = Path("/Volumes/DATA/PROJECTS/TENDERS/isale_investiment_ltd/isale_logo.png")
DATA_FILE = OUT_DIR / "rfp_data.json"

# ─── Brand Colors ───
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

# Cell styles for word-wrapping inside tables
CELL = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=9.5, leading=12.5,
                       alignment=TA_LEFT, spaceAfter=0, spaceBefore=0, textColor=DARK_TEXT)
CELL_BOLD = ParagraphStyle("CellBold", parent=CELL, fontName="Helvetica-Bold")
CELL_HDR = ParagraphStyle("CellHdr", parent=CELL, fontName="Helvetica-Bold",
                            fontSize=10, textColor=white)
CELL_FORM_LABEL = ParagraphStyle("CellFormLabel", parent=CELL, fontName="Helvetica-Bold")

# Table styles — green branded
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

    # Footer
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


def add_bullets(story, text):
    """Parse text with bullet points into story elements."""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("• ") or line.startswith("— "):
            bullet_text = line[2:].strip()
            safe = bullet_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"<bullet>&bull;</bullet> {safe}", BULLET))
        elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or \
             line.startswith("4. ") or line.startswith("5. ") or line.startswith("6. ") or \
             line.startswith("7. ") or line.startswith("8. ") or line.startswith("9. "):
            # Numbered item — treat as sub-heading
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, H3))
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

    story.append(Paragraph("TECHNICAL PROPOSAL", TITLE))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="60%", thickness=3, color=GREEN_PRIMARY))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph(
        "Commercial Credit Origination, Assessment<br/>&amp; Workflow Platform",
        ParagraphStyle("CoverSub", parent=SUBTITLE, fontSize=16, leading=20, textColor=GREEN_PRIMARY)
    ))
    story.append(Spacer(1, 5*mm))

    cover_data = [
        ["Submitted To", data["institution"]],
        ["RFP Reference", data["tender_ref"]],
        ["Submitted By", data["company_name"]],
        ["Date", data["date"]],
    ]
    story.append(make_form_table(cover_data, col_widths=[5*cm, 10*cm]))
    story.append(Spacer(1, 1.5*cm))

    story.append(Paragraph("Submitted to:", SMALL))
    for line in data["submission_to"].split("\n"):
        safe = line.replace("&", "&amp;")
        story.append(Paragraph(safe, BODY))

    # ════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════════════
    from reportlab.platypus.doctemplate import NextPageTemplate
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    story.append(Paragraph("Table of Contents", H1))
    story.append(Spacer(1, 5*mm))

    toc_items = [
        ("1", "Executive Summary"),
        ("2", "Company Profile"),
        ("3", "Understanding of NBC's Requirements"),
        ("4", "Proposed Solution Overview"),
        ("5", "Implementation Approach"),
        ("6", "Team Qualifications"),
        ("7", "Support Model (24/7 Local Support)"),
        ("8", "Regulatory Compliance & Security"),
        ("9", "Value Proposition"),
        ("A", "Evaluation Criteria Response Matrix"),
        ("B", "Administrative Documents Checklist"),
        ("C", "Conflict of Interest Declaration"),
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
        story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
        story.append(Spacer(1, 4*mm))

        add_bullets(story, section["content"])
        section_num += 1

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A — EVALUATION CRITERIA RESPONSE
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix A — Evaluation Criteria Response", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "The following matrix addresses each of NBC's evaluation criteria with our response and supporting evidence.",
        BODY
    ))
    story.append(Spacer(1, 3*mm))

    eval_data = [
        ["#", "Criterion", "Max Score", "Isale Response"],
        ["1", "5+ years Core Banking implementation experience",
         "5", "Isale Investment Limited incorporated Oct 2018 (7+ years). CEO Victor Tesha has 10+ years banking experience at NBC, Azania, UBA, ICB Tanzania. Certificate of Incorporation and business registration provided."],
        ["2", "Not blacklisted/debarred by any government authority",
         "5", "Isale confirms it has not been blacklisted or debarred by any government authority. Legal undertaking provided. No arbitration/legal suits or unsettled disputes with financial sector clients."],
        ["3", "Annual Audited Reports for last 3 financial years",
         "5", "Audited financial statements for 2021, 2022, and 2023 to be provided separately."],
        ["4", "Legal presence in Tanzania with offices",
         "2", "Headquartered at Plot 83, Ada Estate, Dar es Salaam, Tanzania. Additional presence in Dubai, UAE. Valid ICT Services business licence from Kinondoni Municipal Council."],
        ["5", "5+ completed similar projects (with evidence)",
         "15", "Isale has delivered banking technology solutions including digital banking platforms, payment system implementations (PSP licensed by BOT), and enterprise software for financial institutions across East Africa."],
        ["6", "Sufficient technical staff for 2-year project",
         "10", "Core team of experienced banking technology professionals led by Victor Tesha (CEO) and Prem Ruparelia (Director). Team augmented with specialist consultants. CVs provided."],
        ["7", "Solution alignment with RFP requirements",
         "12", "Comprehensive solution addressing all 9 functional modules: Entity Management, Financial Analysis, PD Risk Grading, Credit Proposal Workflow, Deal Structuring, RBAC, Integration, Alerts, Training. Detailed in Section 4."],
        ["8", "Project plan alignment with 2-year timeline",
         "6", "Phased implementation plan (40 weeks core + 64 weeks stabilization) within the 2-year period. Detailed Gantt with stage-gates. See Section 5."],
        ["9", "Cost effectiveness / value for money",
         "20", "Competitive pricing in Tanzania Shillings. Local delivery reduces travel/logistics costs. Lean operations with experienced team. Detailed pricing in Commercial Proposal."],
        ["10", "24/7 local support capability",
         "13", "24/7 support from Dar es Salaam office with Tier 1/2/3 model. 99.5% uptime SLA, 4-hour RTO, 1-hour RPO. Evidence of similar support for financial institutions. See Section 7."],
        ["11", "Regulatory compliance and security standards",
         "7", "BOT PSP licence holder. ISO 27001 alignment. OWASP Top 10 security controls. AES-256 encryption, TLS 1.2+, RBAC, full audit trail. Compliance matrix in Section 8."],
    ]
    story.append(make_hdr_table(eval_data, col_widths=[1*cm, 5*cm, 1.8*cm, W - 7.8*cm]))

    # ════════════════════════════════════════════════════════════════
    # APPENDIX B — ADMINISTRATIVE DOCUMENTS CHECKLIST
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix B — Administrative Documents Checklist", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
    story.append(Spacer(1, 4*mm))

    admin_data = [
        ["#", "Required Document", "Status", "Reference"],
        ["1", "Company profile showing services offered", "Enclosed", "Section 2"],
        ["2", "Key contact persons", "Enclosed", "See below"],
        ["3", "Article and Memorandum of Association", "Enclosed", "Annexed"],
        ["4", "Certified Tax Clearance Certificate", "Enclosed", "Annexed"],
        ["5", "Company structure and number of employees", "Enclosed", "Section 6"],
        ["6", "Current Audited Financial Statements", "To follow", "Sent separately"],
        ["7", "List of directors, nationalities, IDs", "Enclosed", "See below"],
        ["8", "List of shareholders and shareholding", "Enclosed", "See below"],
        ["9", "List of current and previous clients", "Enclosed", "See below"],
        ["10", "Certified Certificate of Incorporation", "Enclosed", "Annexed"],
        ["11", "Insurance Cover", "To follow", "Sent separately"],
        ["12", "Certified Tax Identification Number (TIN)", "Enclosed", "Annexed"],
        ["13", "Certified Value Added Tax Certificate (VAT)", "Enclosed", "Annexed"],
        ["14", "Certified Trading License", "Enclosed", "Annexed"],
        ["15", "Anti-Bribery and Corruption Policy", "Enclosed", "Annexed"],
        ["16", "Business Continuity Plan", "Enclosed", "Annexed"],
        ["17", "Annual Returns to regulatory body", "Enclosed", "Annexed"],
        ["18", "Signed Declaration of Conflict-of-Interest", "Enclosed", "Appendix C"],
        ["19", "Other relevant information", "Enclosed", "PSP Licence"],
    ]
    story.append(make_hdr_table(admin_data, col_widths=[1*cm, 7*cm, 2.5*cm, W - 10.5*cm]))

    # Key contacts
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Key Contact Persons", H2))
    contacts_data = [
        ["Name", "Title", "Phone", "Email"],
        ["Victor Tesha", "CEO / Project Director", "+255 620 300 000", "victor@isalegroup.co.tz"],
        ["Prem Ruparelia", "Director / Strategic Advisor", "+971 50 XXX XXXX", "prem@isalegroup.co.tz"],
    ]
    story.append(make_hdr_table(contacts_data, col_widths=[4*cm, 4.5*cm, 3.5*cm, W - 12*cm]))

    # Directors
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("List of Directors", H2))
    directors_data = [
        ["Name", "Nationality", "Position", "Identification"],
        ["Victor Tesha", "Tanzanian", "CEO / Director", "National ID provided"],
        ["Prem Ruparelia", "British", "Director", "Passport copy provided"],
    ]
    story.append(make_hdr_table(directors_data, col_widths=[4*cm, 3*cm, 3.5*cm, W - 10.5*cm]))

    # Shareholders
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("List of Shareholders", H2))
    shareholders_data = [
        ["Name", "Nationality", "Shareholding %"],
        ["Victor Tesha", "Tanzanian", "—"],
        ["Prem Ruparelia", "British", "—"],
    ]
    story.append(make_hdr_table(shareholders_data, col_widths=[5*cm, 4*cm, W - 9*cm]))
    story.append(Paragraph("<i>Detailed shareholding structure available in the Memorandum and Articles of Association.</i>", SMALL))

    # Clients
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("List of Current and Previous Clients", H2))
    clients_data = [
        ["#", "Client", "Sector", "Services Provided"],
        ["1", "Banking / Financial Institution clients", "Financial Services", "Digital banking, payment systems, enterprise software"],
        ["2", "Government institutions", "Public Sector", "Digital transformation, ICT solutions"],
        ["3", "Corporate clients", "Various", "ERP, CRM, business consulting"],
    ]
    story.append(make_hdr_table(clients_data, col_widths=[1*cm, 5*cm, 3.5*cm, W - 9.5*cm]))
    story.append(Paragraph("<i>Detailed client references with contact details available upon request.</i>", SMALL))

    # ════════════════════════════════════════════════════════════════
    # APPENDIX C — CONFLICT OF INTEREST DECLARATION
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix C — Declaration of Conflict of Interest", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
    story.append(Spacer(1, 8*mm))

    coi_text = """I, <b>Victor Tesha</b>, on behalf of <b>Isale Investment Limited</b> ("Supplier") hereby declare that:

1. The Supplier, including our employees, directors and subcontractors, and their respective spouses, do not have a kinship or other personal relationship with the employees and directors of the Bank, other than in their capacity as Bank customers.

2. The Supplier, its employees, directors and subcontractors will not benefit directly or indirectly, financially or in kind, as a result of a kinship or other personal relationship with the employees or directors of the Bank, as a result of the appointment of the Supplier.

3. In the event that a kinship or other personal relationship exists or arises at any time during this and any related engagement, the Supplier will provide the required information.

4. Failure to disclose a kinship or personal relationship will result in disqualification and sanction from any future RFP process."""

    story.append(Paragraph(coi_text, BODY))
    story.append(Spacer(1, 1*cm))

    sig_data = [
        ["NBC Employee Name", "N/A — No conflict exists"],
        ["NBC Business Unit", "N/A"],
        ["Position in NBC Business Unit", "N/A"],
        ["", ""],
        ["Supplier Signature", "________________________"],
        ["Name", "Victor Tesha, CEO"],
        ["Company", "Isale Investment Limited"],
        ["Date", data["date"]],
    ]
    story.append(make_form_table(sig_data, col_widths=[6*cm, 10*cm]))

    # ════════════════════════════════════════════════════════════════
    # APPENDIX D — ANTI-BRIBERY AND CORRUPTION POLICY ACKNOWLEDGEMENT
    # ════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Appendix D — Anti-Bribery and Corruption Policy", H1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREEN_PRIMARY))
    story.append(Spacer(1, 8*mm))

    abc_text = """Isale Investment Limited acknowledges and agrees to comply with NBC's Anti-Bribery and Corruption provisions as set out in the RFP document.

<b>Undertakings, Representations and Warranties:</b>

Isale Investment Limited represents and warrants that neither it nor any of its Associated Persons have taken or will take any action that might cause NBC to violate the Bribery Act or any Applicable Anti-Bribery Law, including the Tanzania Prevention and Combatting of Corruption Act, No. 11 of 2007, and the Economic and Organized Crimes Control Act.

Specifically, neither Isale nor any of its Associated Persons will authorise, offer, give or agree to offer or give, directly or indirectly, any payment, gift or other advantage with respect to any activities undertaken relating to this engagement.

Isale Investment Limited has implemented and maintains adequate procedures designed to comply with all applicable anti-bribery and anti-corruption laws and regulations.

Isale Investment Limited will maintain appropriate, complete and up-to-date books, accounts, and records that accurately reflect its transactions relating to any agreement with NBC."""

    story.append(Paragraph(abc_text, BODY))
    story.append(Spacer(1, 1*cm))

    abc_sig = [
        ["Acknowledged By", "Victor Tesha"],
        ["Title", "CEO, Isale Investment Limited"],
        ["Date", data["date"]],
        ["Signature", "________________________"],
    ]
    story.append(make_form_table(abc_sig, col_widths=[5*cm, 10*cm]))

    # ════════════════════════════════════════════════════════════════
    # BUILD
    # ════════════════════════════════════════════════════════════════
    doc.multiBuild(story)
    size_kb = OUTPUT.stat().st_size // 1024
    print(f"RFP PDF generated: {OUTPUT}")
    print(f"Size: {size_kb} KB")


if __name__ == "__main__":
    build()
