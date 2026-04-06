#!/usr/bin/env python3
"""Generate CRDB-2026-003 EOI submission PDF for Isale Investment Limited."""

import sys
sys.path.insert(0, "/Volumes/DATA/PROJECTS/TENDERS")

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image, Frame, PageTemplate
)
from reportlab.pdfgen import canvas as pdfcanvas

OUT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS/applications/CRDB-2026-003_EOI-End-to-End-Lending-System")
OUTPUT = OUT_DIR / "ISALE_EOI_CRDB_E2E_Lending_System.pdf"
LOGO = Path("/Volumes/DATA/PROJECTS/TENDERS/isale_investiment_ltd/isale_logo.png")

# ─── Brand Colors ───
GREEN_PRIMARY = HexColor("#2E7D32")    # Primary green
GREEN_DARK = HexColor("#1B5E20")       # Dark green for headings
GREEN_LIGHT = HexColor("#E8F5E9")      # Light green for table alternating rows
GREEN_ACCENT = HexColor("#4CAF50")     # Accent green
GREEN_BG = HexColor("#F1F8E9")         # Very light green background
WHITE = white
DARK_TEXT = HexColor("#1a1a1a")
GREY_TEXT = HexColor("#555555")
GREY_BORDER = HexColor("#C8E6C9")      # Green-tinted border

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
    """Draw branded header with logo and green line, plus footer."""
    canvas.saveState()
    page_width, page_height = A4

    # Header — logo + green line
    if LOGO.exists():
        canvas.drawImage(str(LOGO), 2.5*cm, page_height - 1.8*cm, width=1.4*cm, height=1.4*cm,
                         preserveAspectRatio=True, mask='auto')
    # Company name next to logo
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(GREEN_DARK)
    canvas.drawString(4.2*cm, page_height - 1.25*cm, "Isale Investment Limited")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawString(4.2*cm, page_height - 1.55*cm, "Business, Investments and Technology")

    # Green header line
    canvas.setStrokeColor(GREEN_PRIMARY)
    canvas.setLineWidth(1.5)
    canvas.line(2.5*cm, page_height - 2*cm, page_width - 2.5*cm, page_height - 2*cm)

    # Footer — green line + text
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
    """Cover page — no header, just subtle footer."""
    canvas.saveState()
    page_width, _ = A4
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawCentredString(page_width / 2, 1.2*cm, "CONFIDENTIAL — Isale Investment Limited")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
                            topMargin=2.5*cm, bottomMargin=2.3*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)

    # Page templates
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

    # Logo centered on cover
    if LOGO.exists():
        story.append(Image(str(LOGO), width=4*cm, height=4*cm))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("EXPRESSION OF INTEREST", TITLE))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="60%", thickness=3, color=GREEN_PRIMARY))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Implementation of an End-to-End (E2E) Lending System<br/>for CRDB Bank Plc and its Subsidiaries", SUBTITLE))
    story.append(Spacer(1, 2*cm))

    cover_data = [
        ["Submitted To:", "CRDB Bank Plc\nSecretary, Management Tender Committee\ntenders@crdbbank.co.tz"],
        ["Submitted By:", "Isale Investment Limited\nPlot 83, Ada Estate, Dar es Salaam\nP.O Box 71959\n+255 620 300 000\nvictor@isalegroup.co.tz"],
        ["Date:", "13 March 2026"],
        ["Reference:", "EOI — E2E Lending System"],
    ]
    story.append(make_form_table(cover_data, [4*cm, 12*cm]))

    # Switch to content template for subsequent pages
    from reportlab.platypus import NextPageTemplate
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Table of Contents", H1))
    story.append(Spacer(1, 3*mm))
    toc_items = [
        "1. Company Profile (Appendix A.1)",
        "2. Association / Joint Venture (Appendix A.2)",
        "3. Proposed Solution (Appendix A.3)",
        "4. Summary of Experience (Appendix A.4)",
        "5. Proposed Team Qualifications (Appendix A.5)",
        "6. Firm's Experience and References (Appendix B)",
        "7. Approach and Methodology",
        "8. Annexures — Certificates and Financial Statements",
    ]
    for item in toc_items:
        story.append(Paragraph(item, BODY))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A.1 — PROPOSING COMPANY
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Appendix A.1 — Proposing Company", H1))
    a1_data = [
        ["Required Information", "Details"],
        ["Name", "Isale Investment Limited"],
        ["Year of Incorporation", "2018 (as Leeds Company Limited; renamed to Isale Investment Limited in 2023)"],
        ["Registered Office Address", "Plot 83, Ada Estate, Next to King Solomon Hall,\nP.O Box 71959, Dar es Salaam, Tanzania"],
        ["Key Contact Details", "Victor Tesha — CEO & Founder\nEmail: victor@isalegroup.co.tz\nPhone: +255 620 300 000"],
        ["Number of Years Implementing\nE2E Lending Software", "Isale's leadership team brings 10+ years of banking technology and credit systems experience. The firm has been delivering banking and ICT solutions since 2018."],
        ["Number of Implementations of\nE2E Lending Software", "Isale proposes to deliver this engagement through a strategic technology partnership with established Temenos implementation specialists, combining Isale's deep local banking domain knowledge with proven Temenos Transact implementation capability."],
    ]
    story.append(make_hdr_table(a1_data, [5.5*cm, W - 5.5*cm]))
    story.append(Spacer(1, 5*mm))

    # Company Summary Table
    story.append(Paragraph("Summary of Company Information", H2))
    summary_data = [
        ["Field", "Detail"],
        ["Company Name", "Isale Investment Limited"],
        ["Company Location", ""],
        ["  Location of Corporate Headquarters", "Plot 83, Ada Estate, Dar es Salaam, Tanzania"],
        ["  Nearest Office to Tanzania", "Dar es Salaam (Headquarters)"],
        ["Experience", ""],
        ["  Number of Years in Business", "8 years (incorporated October 2018)"],
        ["  Years Providing Banking Technology Solutions", "8 years"],
        ["Customer Base", ""],
        ["  Number of Clients", "Multiple clients across banking, government, and private sectors in Tanzania and East Africa"],
        ["  Clients Using Proposed Solution Version", "To be detailed in subsequent RFP response"],
        ["Terminated Projects", "None"],
        ["Organization Size / Total Revenue", ""],
        ["  2025", "Available in audited financial statements (annexed)"],
        ["  2024", "Available in audited financial statements (annexed)"],
        ["  2023", "Available in audited financial statements (annexed)"],
        ["  2022", "Available in audited financial statements (annexed)"],
        ["  2021", "Available in audited financial statements (annexed)"],
        ["  2020", "N/A — Company trading as Leeds Company Limited"],
    ]
    story.append(make_hdr_table(summary_data, [6*cm, W - 6*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A.2 — ASSOCIATION / JOINT VENTURE
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Appendix A.2 — Association (Joint Venture / Sub-contracting)", H1))
    story.append(Paragraph(
        "Isale Investment Limited intends to form a strategic technology partnership with specialist "
        "Temenos implementation consultants to augment its delivery capability for this engagement. "
        "The details of the technology partner will be finalized and formally communicated should Isale "
        "be shortlisted for the RFP stage.", BODY))
    story.append(Spacer(1, 3*mm))
    a2_data = [
        ["Required Information", "Details"],
        ["Nature of Association", "Sub-contracting (Technology Implementation Partner)"],
        ["Names of Party", "To be confirmed upon shortlisting for RFP"],
        ["Year of Incorporation", "To be confirmed"],
        ["Registered Office Address", "To be confirmed"],
        ["Key Contact Details", "Isale Investment Limited (Prime Partner)\nVictor Tesha — victor@isalegroup.co.tz\n+255 620 300 000"],
        ["Years Implementing E2E\nLending Software", "Partner selection criteria includes minimum 5 years Temenos lending implementation experience"],
        ["Number of E2E Lending\nImplementations", "Partner selection criteria includes minimum 3 successful E2E lending implementations"],
    ]
    story.append(make_hdr_table(a2_data, [5.5*cm, W - 5.5*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A.3 — PROPOSED SOLUTION
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Appendix A.3 — Proposed Solution", H1))
    a3_data = [
        ["Required Information", "Details"],
        ["Name of Proposed Solution", "Integrated E2E Lending Solution built on Temenos Transact Lending modules, Temenos Infinity (digital channels), and best-of-breed credit decisioning components, orchestrated via WSO2 Integration Platform"],
        ["Version of Proposed E2E\nLending Solution", "Temenos Transact R21 (aligned with CRDB Bank's current CBS version) with latest compatible lending module releases"],
        ["Name of OEM", "Temenos AG (Core Banking & Lending Platform)\nWSO2 Inc. (Enterprise Integration Platform)\nAdditional specialist vendors as required for credit decisioning and collections"],
        ["OEM Authorization", "OEM authorization letters and/or partnership agreements will be provided upon shortlisting for the RFP stage. Isale's Bank of Tanzania PSP licence (NBPSL No. 0000-70) demonstrates regulatory standing for financial technology service delivery."],
    ]
    story.append(make_hdr_table(a3_data, [5.5*cm, W - 5.5*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A.4 — EXPERIENCE SUMMARY
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Appendix A.4 — High Level Summary of Experience", H1))
    story.append(Paragraph(
        "Isale Investment Limited's experience is anchored in the direct banking sector experience "
        "of its leadership team, combined with the firm's ICT solutions delivery track record:", BODY))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("A. Leadership Banking Experience (Direct Institutional Experience)", H2))
    a4a_data = [
        ["Institution", "Size / Type", "Country", "Role / Modules"],
        ["NBC Bank Limited", "Large commercial bank\n(Top 5 Tanzania)", "Commercial Bank\nTanzania", "Retail Assets & Mortgage product management;\nCorporate Credit Risk;\nStrategy formulation & execution (2013-2018 turnaround)"],
        ["Azania Bank Limited", "Mid-tier commercial bank", "Commercial Bank\nTanzania", "Business Support & Recoveries;\nCorporate and Retail Banking;\nLegal & Credit Recovery"],
        ["UBA Tanzania Limited", "International bank\n(Pan-African)", "Commercial Bank\nTanzania", "Acting Head, Corporate Banking;\nCredit origination and assessment"],
        ["ICB Tanzania Limited", "Mid-tier commercial bank", "Commercial Bank\nTanzania", "Credit Executive — Retail Credit;\nLending operations and credit decisioning"],
        ["NatWest Bank (UK)", "Major UK bank\n(Top 4)", "Commercial Bank\nUnited Kingdom", "Investment management;\nStraight-through processing;\nOperating model redesign"],
    ]
    story.append(make_hdr_table(a4a_data, [3.2*cm, 3.5*cm, 3*cm, W - 9.7*cm]))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("B. Isale Investment ICT Solutions Delivery", H2))
    story.append(Paragraph(
        "Isale Digital has delivered banking solutions, ERP systems, CRM implementations, "
        "and digital transformation projects for clients across the financial services, government, "
        "and private sectors in Tanzania and the wider East African region. Specific project details "
        "and client references for relevant technology implementations will be provided in full "
        "during the RFP stage.", BODY))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPENDIX A.5 — TEAM QUALIFICATIONS
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Appendix A.5 — Proposed Team Qualifications", H1))
    a5_data = [
        ["Name", "Area of Expertise", "Lending\nImplementations", "Years of\nExperience", "Academic Qualifications"],
        ["Victor Tesha", "Credit & Risk Management;\nCommercial Banking;\nCorporate Strategy;\nProduct Development;\nBusiness Transformation", "Multiple\n(NBC, Azania,\nUBA, ICB)", "10+", "MBA (Marketing);\nBA Social Science"],
        ["Prem Ruparelia", "Corporate Strategy &\nGovernance; Procurement;\nInvestment Management;\nOperating Model Redesign;\nLarge-scale Transformation", "Multiple\n(NatWest, DHL,\nBAE Systems)", "20+", "MA Corporate Strategy\n& Governance;\nMCIPS (UK)"],
        ["Project Manager\n(To be assigned)", "Project Management;\nBanking Technology;\nTemenos Implementation", "Min. 3", "Min. 8", "PMP/PRINCE2;\nDegree in IT/Engineering"],
        ["Technical Lead\n(To be assigned)", "Temenos Transact;\nWSO2 Integration;\nLending Systems", "Min. 3", "Min. 8", "Degree in Computer Science\nor equivalent"],
        ["Business Analyst\n(To be assigned)", "Credit Processes;\nLending Operations;\nRequirements Engineering", "Min. 2", "Min. 5", "Degree in Banking/Finance\nor equivalent"],
    ]
    story.append(make_hdr_table(a5_data, [2.8*cm, 4*cm, 2.2*cm, 2*cm, W - 11*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPENDIX B — FIRM EXPERIENCE / REFERENCE
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Appendix B — Specific Firm Experience / Reference", H1))
    story.append(Paragraph(
        "The following reference details the most relevant institutional experience of "
        "Isale Investment Limited's leadership in banking technology transformation:", BODY))
    story.append(Spacer(1, 3*mm))

    b_data = [
        ["Field", "Details"],
        ["Assignment Name", "Strategic Turnaround and Digital Transformation — NBC Bank Limited"],
        ["Country", "Tanzania"],
        ["Location within Country", "Dar es Salaam (Head Office) with nationwide branch network"],
        ["Duration of Assignment", "60 months (2013-2018)"],
        ["Total Staff-Months", "60 (Victor Tesha — full-time engagement)"],
        ["Approx. Value of Services", "Integral part of NBC's strategic transformation programme — value as part of institutional employment"],
        ["Start Date", "2013"],
        ["Completion Date", "2018"],
        ["Associated Consultants", "N/A — Direct institutional engagement"],
        ["Senior Professional Staff\nand Functions", "Victor Tesha — Retail Assets & Mortgage Product Manager;\nCorporate Credit Risk Consultant;\nStrategy formulation and execution lead"],
        ["Name and Version of System", "NBC Core Banking and Lending Systems"],
        ["Modules Implemented/Managed", "Retail lending products (Personal loans, Mortgage);\nCorporate credit origination and assessment;\nCredit risk management frameworks;\nProduct development and segmentation;\nDistribution network optimization"],
        ["E2E Lending System?", "Yes — End-to-end involvement across origination, credit assessment, product management, and portfolio management"],
        ["Narrative Description", "Victor Tesha spearheaded NBC Bank's 2013-2018 strategy formulation and execution that transformed the organization from an underperforming entity into a profit-making institution. His role encompassed the full credit lifecycle including retail asset product management, corporate credit risk assessment, lending process optimization, and distribution strategy. This transformation involved modernizing NBC's lending operations, implementing improved credit decisioning frameworks, and driving digital channel adoption for loan origination."],
        ["Services Provided", "Strategy formulation and execution; Retail and corporate credit product management; Credit risk framework design; Lending process reengineering; Distribution network optimization; Board reporting on strategic review findings"],
    ]
    story.append(make_hdr_table(b_data, [4.5*cm, W - 4.5*cm]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # APPROACH AND METHODOLOGY (max 6 pages)
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Approach and Methodology", H1))
    story.append(Paragraph("<i>Limited to 6 pages as prescribed by CRDB Bank</i>", SMALL))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("1. Understanding of Requirements", H2))
    story.append(Paragraph(
        "CRDB Bank seeks to digitally unify its entire credit lifecycle across Consumer, MSME, and "
        "Corporate segments through an integrated End-to-End (E2E) Lending Solution. The solution must "
        "be built upon Temenos Transact R21 (core banking system of record) and WSO2 (enterprise integration "
        "platform), covering loan origination, credit assessment, approval, disbursement, servicing, collections, "
        "and recovery. The architecture must support multi-entity deployment (Tanzania, Burundi, DRC), "
        "segment-specific lending models including Agribusiness and Islamic financing, and minimize CBS customization.", BODY))

    story.append(Paragraph("2. Proposed Solution Architecture", H2))
    story.append(Paragraph(
        "Our proposed E2E Lending Solution follows CRDB Bank's target modular, integration-led architecture:", BODY))

    layers = [
        "<b>Digital &amp; Assisted Channels:</b> Temenos Infinity for branch, mobile, internet banking, and RM-assisted origination — providing a unified customer experience across all touchpoints.",
        "<b>Loan Origination &amp; Workflow Layer:</b> Configurable workflow engine supporting multi-segment origination with automated document management, KYC/AML verification (NIDA integration), and maker-checker controls. Segment-specific workflows for Consumer (straight-through eligible), MSME (semi-automated), Corporate (committee-based), Agribusiness, and Islamic financing.",
        "<b>Credit Decisioning Layer:</b> Rules-based and scorecard-driven credit assessment engine integrating with Tanzania credit bureaus (CRB Africa, Dun &amp; Bradstreet), NIDA for identity verification, internal behavioral scoring, and collateral valuation systems.",
        "<b>Core Banking Layer (Temenos Transact R21):</b> System of record for loan account setup, disbursement, schedule management, accruals, repayment processing, restructuring, write-off, and financial postings. Minimal customization — leveraging Transact's native lending product factory.",
        "<b>Collateral Management:</b> End-to-end collateral lifecycle — registration, valuation, perfection tracking, insurance monitoring, lien management, and release.",
        "<b>Collections &amp; Recovery:</b> Automated arrears detection, segmented collection strategies, workout management, restructuring workflows, legal recovery tracking, and external agency management.",
        "<b>Enterprise Integration Layer (WSO2):</b> API management, service orchestration, and event-driven integration patterns. Secure, loosely coupled integrations between all lending ecosystem components.",
        "<b>Data, Reporting &amp; Analytics:</b> Centralized data warehouse for Bank of Tanzania regulatory returns, portfolio monitoring, credit risk analytics, and performance dashboards.",
    ]
    for layer in layers:
        story.append(Paragraph(layer, BULLET, bulletText="\u2022"))

    story.append(Paragraph("3. Response to EOI Section 2.1 — Required Outcomes", H2))
    outcomes = [
        ["Required Outcome", "How Our Solution Addresses It"],
        ["Digitally unified credit lifecycle", "Single platform spanning origination through collections with Temenos Transact as system of record, eliminating siloed processes across Consumer, MSME, and Corporate segments"],
        ["Minimize CBS customization", "Leverage Temenos Transact R21 native lending product factory and APIs; implement business logic in the origination and decisioning layers external to CBS"],
        ["Straight-through & workflow-driven lending", "Configurable workflow engine with auto-decisioning for pre-approved segments; rules-based routing to manual review only when policy thresholds are triggered"],
        ["Segment-specific lending models", "Parameterized product and workflow configuration supporting Consumer, MSME, Corporate, Agribusiness, and Islamic financing within a common architecture"],
        ["Credit governance & regulatory compliance", "Centralized policy rules, audit trails, maker-checker controls, segregation of duties, and automated Bank of Tanzania regulatory reporting"],
        ["Improved time-to-market", "Product factory approach enabling new lending products and policy changes through configuration rather than development"],
        ["Scalable, future-ready platform", "Modular architecture supporting multi-entity rollout; containerized deployment; API-first design for future integrations"],
    ]
    story.append(make_hdr_table(outcomes, [5*cm, W - 5*cm]))
    story.append(PageBreak())

    story.append(Paragraph("4. Implementation Approach — Phased Delivery", H2))
    story.append(Paragraph(
        "We propose an agile, phased methodology designed for incremental value realization and "
        "risk-controlled rollout:", BODY))

    phases = [
        ["Phase", "Duration", "Key Activities", "Stage-Gate / Deliverables"],
        ["Phase 1\nDiscovery &\nFoundation", "Weeks\n1-6", "Requirements gathering across all segments;\nCurrent-state process mapping & gap analysis;\nSolution design & integration architecture;\nEnvironment setup (sandbox, UAT, staging);\nProject governance & RACI", "BRD, Solution Design Document,\nIntegration Architecture,\nProject Plan\n\nGate: Design Sign-off"],
        ["Phase 2\nCore Lending\nBuild", "Weeks\n7-18", "Configure LOS workflows (Consumer, MSME);\nCredit decisioning rules & scorecards;\nTemenos Transact R21 integration via WSO2;\nCollateral management module;\nUnit testing & SIT", "Configured LOS, Credit Engine,\nCollateral Module, SIT Report\n\nGate: SIT Sign-off"],
        ["Phase 3\nCorporate &\nSpecialized", "Weeks\n19-28", "Corporate segment (complex deal structures);\nAgribusiness & Islamic financing models;\nCollections & recovery workflows;\nRegulatory reporting & analytics;\nExternal integrations (bureaus, NIDA)", "Corporate Module, Collections,\nAnalytics Layer\n\nGate: Extended SIT Sign-off"],
        ["Phase 4\nTest, Train\n& Go-Live", "Weeks\n29-36", "UAT with CRDB business teams;\nData migration from legacy systems;\nTechnical & end-user training;\nParallel run & production cutover;\nHyper-care support (4 weeks)", "UAT Report, Training Materials,\nMigration Report, Go-Live\nChecklist\n\nGate: Go-Live Approval"],
        ["Phase 5\nMulti-Entity\nRollout", "Weeks\n37-48", "Configure & deploy to Burundi subsidiary;\nGreenfield deployment for DRC;\nRegulatory localization per jurisdiction;\nPost-deployment optimization", "Entity Go-Live Reports,\nStabilization Report\n\nGate: Entity Acceptance"],
    ]
    story.append(make_hdr_table(phases, [2.3*cm, 1.8*cm, 5.5*cm, W - 9.6*cm]))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("5. Key Assumptions", H2))
    assumptions = [
        "CRDB Bank will provide a dedicated project team including business SMEs, IT resources, and an executive Project Sponsor with authority to make binding decisions.",
        "Access to Temenos Transact R21 sandbox environment will be provided within 2 weeks of project initiation.",
        "WSO2 platform administration support will be available from CRDB Bank's IT team throughout the project.",
        "Third-party integrations (credit bureaus, NIDA, external data sources) require separate commercial agreements managed by CRDB Bank.",
        "Change management and organizational readiness activities will be jointly planned and executed.",
        "The project timeline of 48 weeks assumes concurrent workstreams and timely stage-gate approvals.",
        "CRDB Bank's existing data quality and completeness is sufficient for migration; data cleansing, if required, will be a joint responsibility.",
    ]
    for a in assumptions:
        story.append(Paragraph(a, BULLET, bulletText="\u2022"))
    story.append(PageBreak())

    story.append(Paragraph("6. Training and Knowledge Transfer", H2))
    story.append(Paragraph(
        "Our training approach follows a train-the-trainer model designed to build sustainable internal capability:", BODY))
    training = [
        "<b>Technical Training:</b> System administration, configuration management, integration monitoring (WSO2), database management, and troubleshooting — targeting CRDB Bank IT team.",
        "<b>Functional Training:</b> Product configuration, workflow management, credit policy setup, reporting customization — targeting CRDB Bank business operations and product teams.",
        "<b>End-User Training:</b> Loan origination, credit assessment, approval processes, collections management — delivered via train-the-trainer to branch and central processing teams.",
        "<b>Documentation:</b> Comprehensive system documentation, user manuals, integration specifications, and operations runbooks.",
    ]
    for t in training:
        story.append(Paragraph(t, BULLET, bulletText="\u2022"))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # ANNEXURES
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("Annexures", H1))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("The following documents are annexed to this EOI submission:", BODY))
    story.append(Spacer(1, 3*mm))

    annexures = [
        ["#", "Document", "Status"],
        ["1", "Certificate of Incorporation (BRELA — Reg. No. 137771411)", "Attached"],
        ["2", "Certificate of Change of Name (Leeds Company Limited to Isale Investment Limited)", "Attached"],
        ["3", "Tax Identification Number (TIN) Certificate — TIN: 137-771-411", "Attached"],
        ["4", "VAT Registration Certificate — VRN: 40-313410-P", "Attached"],
        ["5", "ICT Business Licence — BL01396912025-2600015282 (Valid to Oct 2026)", "Attached"],
        ["6", "Payment Service Provider Licence — NBPSL No. 0000-70 (Bank of Tanzania, Valid to Aug 2030)", "Attached"],
        ["7", "Audited Financial Statements — 2021", "To be provided separately*"],
        ["8", "Audited Financial Statements — 2022", "To be provided separately*"],
        ["9", "Audited Financial Statements — 2023", "To be provided separately*"],
    ]
    story.append(make_hdr_table(annexures, [1.5*cm, 10.5*cm, W - 12*cm]))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<i>* Audited financial statements for 2021, 2022, and 2023 will be submitted as a separate "
        "attachment to the same email. Should CRDB Bank require these prior to shortlisting, Isale "
        "Investment Limited will provide them upon request.</i>", SMALL))

    # Build
    doc.build(story)
    print(f"EOI PDF generated: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build()
