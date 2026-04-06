#!/usr/bin/env python3
"""
Generate Technical Proposal PDF for:
RFP FOR MICROSOFT D365 ENTERPRISE INTEGRATION - EPROCESS
Bid Number: 2/3/2026/RFP/CIB
Ecobank / eProcess International Ghana Limited
"""

import os, json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.platypus.flowables import Flowable
from PyPDF2 import PdfMerger

PROJECT = "/Volumes/DATA/PROJECTS/TENDERS"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPANY_DOCS_PDF = f"{PROJECT}/applications/ZIMA_Company_Documents.pdf"

# Colors
BLUE = HexColor("#1565C0")
DARK_BLUE = HexColor("#0D47A1")
DARK = HexColor("#222222")
GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#F5F5F5")
LIGHT_BLUE = HexColor("#E3F2FD")
WHITE = HexColor("#FFFFFF")
GREEN = HexColor("#2E7D32")

W, H = A4

def get_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle('CoverTitle', fontSize=24, textColor=BLUE, fontName='Helvetica-Bold',
                         spaceAfter=6*mm, alignment=TA_CENTER, leading=30))
    s.add(ParagraphStyle('CoverSubtitle', fontSize=14, textColor=DARK, fontName='Helvetica',
                         spaceAfter=4*mm, alignment=TA_CENTER, leading=18))
    s.add(ParagraphStyle('CoverDetail', fontSize=11, textColor=GRAY, fontName='Helvetica',
                         spaceAfter=3*mm, alignment=TA_CENTER, leading=15))
    s.add(ParagraphStyle('ZimaTitle', fontSize=18, textColor=BLUE, fontName='Helvetica-Bold',
                         spaceAfter=4*mm))
    s.add(ParagraphStyle('SectionHead', fontSize=14, textColor=BLUE, fontName='Helvetica-Bold',
                         spaceBefore=8*mm, spaceAfter=4*mm))
    s.add(ParagraphStyle('SubSection', fontSize=12, textColor=DARK_BLUE, fontName='Helvetica-Bold',
                         spaceBefore=5*mm, spaceAfter=3*mm))
    s.add(ParagraphStyle('SubSubSection', fontSize=11, textColor=DARK_BLUE, fontName='Helvetica-Bold',
                         spaceBefore=3*mm, spaceAfter=2*mm))
    s.add(ParagraphStyle('Body', fontSize=10.5, textColor=DARK, fontName='Helvetica',
                         leading=15, alignment=TA_JUSTIFY, spaceAfter=3*mm))
    s.add(ParagraphStyle('BodyBold', fontSize=10.5, textColor=DARK, fontName='Helvetica-Bold',
                         leading=15, spaceAfter=2*mm))
    s.add(ParagraphStyle('ZBullet', fontSize=10.5, textColor=DARK, fontName='Helvetica',
                         leading=15, leftIndent=15, bulletIndent=5, spaceAfter=2*mm,
                         alignment=TA_JUSTIFY))
    s.add(ParagraphStyle('ZBulletBold', fontSize=10.5, textColor=DARK, fontName='Helvetica-Bold',
                         leading=15, leftIndent=15, bulletIndent=5, spaceAfter=2*mm))
    s.add(ParagraphStyle('Small', fontSize=9, textColor=GRAY, fontName='Helvetica',
                         leading=12, spaceAfter=2*mm))
    s.add(ParagraphStyle('Footer', fontSize=8, textColor=GRAY, fontName='Helvetica',
                         alignment=TA_CENTER))
    s.add(ParagraphStyle('TableHeader', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold',
                         alignment=TA_CENTER))
    s.add(ParagraphStyle('TableCell', fontSize=10, textColor=DARK, fontName='Helvetica',
                         leading=13))
    s.add(ParagraphStyle('TOCEntry', fontSize=11, textColor=DARK, fontName='Helvetica',
                         leading=18, spaceAfter=1*mm))
    s.add(ParagraphStyle('TOCSection', fontSize=11, textColor=DARK, fontName='Helvetica-Bold',
                         leading=18, spaceAfter=1*mm))
    return s


def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # Top line
    canvas_obj.setStrokeColor(BLUE)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(20*mm, H - 15*mm, W - 20*mm, H - 15*mm)
    # Header text
    canvas_obj.setFont('Helvetica-Bold', 9)
    canvas_obj.setFillColor(BLUE)
    canvas_obj.drawString(20*mm, H - 13*mm, "ZIMA Solutions Limited")
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GRAY)
    canvas_obj.drawRightString(W - 20*mm, H - 13*mm,
                                "Bid No: 2/3/2026/RFP/CIB | CONFIDENTIAL")
    # Footer
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GRAY)
    canvas_obj.drawString(20*mm, 12*mm,
                          "ZIMA Solutions Limited | TIN: 181-314-605 | Makongo, Kinondoni, Dar es Salaam, Tanzania")
    canvas_obj.drawRightString(W - 20*mm, 12*mm, f"Page {doc.page}")
    canvas_obj.restoreState()


def first_page(canvas_obj, doc):
    """Cover page - no header/footer."""
    pass


def build_cover_page(styles):
    """Build the cover page elements."""
    elements = []
    elements.append(Spacer(1, 30*mm))

    # ZIMA Logo area
    elements.append(Paragraph("ZIMA SOLUTIONS LIMITED", styles['CoverTitle']))
    elements.append(Paragraph(
        "Digital Transformation &bull; Enterprise Integration &bull; AI Solutions",
        styles['CoverDetail']))
    elements.append(Spacer(1, 8*mm))

    # Divider
    elements.append(HRFlowable(width="80%", thickness=2, color=BLUE, spaceAfter=8*mm))

    # Title block
    elements.append(Paragraph("TECHNICAL PROPOSAL", styles['CoverTitle']))
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        "RFP FOR MICROSOFT D365 ENTERPRISE INTEGRATION",
        ParagraphStyle('CoverBidTitle', fontSize=16, textColor=DARK, fontName='Helvetica-Bold',
                       alignment=TA_CENTER, spaceAfter=4*mm, leading=20)))
    elements.append(Spacer(1, 4*mm))

    # Details table
    detail_data = [
        ["Bid Number:", "2/3/2026/RFP/CIB"],
        ["Purchaser:", "eProcess International Ghana Limited"],
        ["Client:", "Ecobank Transnational Incorporated (ETI)"],
        ["Bidder:", "ZIMA Solutions Limited"],
        ["Date:", datetime.now().strftime("%d %B %Y")],
        ["Validity:", "90 days from submission deadline"],
    ]
    detail_table = Table(detail_data, colWidths=[55*mm, 90*mm])
    detail_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), BLUE),
        ('TEXTCOLOR', (1, 0), (1, -1), DARK),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(detail_table)
    elements.append(Spacer(1, 15*mm))

    # Confidentiality notice
    elements.append(HRFlowable(width="80%", thickness=1, color=GRAY, spaceAfter=4*mm))
    elements.append(Paragraph(
        "<b>CONFIDENTIAL</b> — This document contains proprietary information of ZIMA Solutions Limited. "
        "It is intended solely for eProcess International Ghana Limited / Ecobank Group for the purpose "
        "of evaluating this proposal. No part of this document may be reproduced or disclosed to third "
        "parties without the prior written consent of ZIMA Solutions Limited.",
        ParagraphStyle('ConfNote', fontSize=9, textColor=GRAY, fontName='Helvetica',
                       alignment=TA_CENTER, leading=12)))

    # Contact
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph(
        "ZIMA Solutions Limited<br/>"
        "Makongo, Near Ardhi University, Kinondoni, Dar es Salaam, Tanzania<br/>"
        "P.O. Box 100025 | TIN: 181-314-605<br/>"
        "Email: info@zima.co.tz | Tel: +255 69 241 0353<br/>"
        "Web: www.zima.co.tz",
        ParagraphStyle('CoverContact', fontSize=10, textColor=GRAY, fontName='Helvetica',
                       alignment=TA_CENTER, leading=14)))

    elements.append(PageBreak())
    return elements


def build_toc(styles):
    """Build table of contents."""
    elements = []
    elements.append(Paragraph("TABLE OF CONTENTS", styles['SectionHead']))
    elements.append(Spacer(1, 4*mm))

    toc_items = [
        ("1.", "COVER LETTER", True),
        ("2.", "VENDOR PROFILE", True),
        ("2.1", "Company Overview", False),
        ("2.2", "Key Personnel", False),
        ("2.3", "Partnerships & Certifications", False),
        ("3.", "TECHNICAL PROPOSAL", True),
        ("3.1", "Understanding of Requirements", False),
        ("3.2", "D365 Platform Assessment Approach", False),
        ("3.3", "Third-Party System Integration Strategy", False),
        ("3.4", "D365 Enhancements & Optimization", False),
        ("3.5", "Reporting & Analytics", False),
        ("3.6", "Security & Compliance", False),
        ("3.7", "Knowledge Transfer & Support", False),
        ("4.", "IMPLEMENTATION METHODOLOGY", True),
        ("4.1", "Project Phases", False),
        ("4.2", "Project Timeline", False),
        ("4.3", "Testing Strategy", False),
        ("5.", "REFERENCES & EXPERIENCE", True),
        ("6.", "DOCUMENTATION & DELIVERABLES", True),
        ("7.", "COMPANY LEGAL DOCUMENTS", True),
    ]

    for num, title, is_section in toc_items:
        style = styles['TOCSection'] if is_section else styles['TOCEntry']
        indent = "" if is_section else "&nbsp;&nbsp;&nbsp;&nbsp;"
        elements.append(Paragraph(f"{indent}<b>{num}</b>&nbsp;&nbsp;&nbsp;{title}", style))

    elements.append(PageBreak())
    return elements


def build_cover_letter(styles):
    """Section 1: Cover Letter."""
    elements = []
    elements.append(Paragraph("1. COVER LETTER", styles['SectionHead']))
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(datetime.now().strftime("%d %B %Y"), styles['Body']))
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph(
        "The Head of Procurement &amp; Records Management<br/>"
        "eProcess International Ghana Limited<br/>"
        "2 Morocco Lane, Off Independence Avenue<br/>"
        "Ministerial Area, Accra, Ghana", styles['Body']))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph(
        "<b>RE: RFP FOR MICROSOFT D365 ENTERPRISE INTEGRATION - EPROCESS</b><br/>"
        "<b>Bid Number: 2/3/2026/RFP/CIB</b>", styles['Body']))
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph("Dear Sir/Madam,", styles['Body']))
    elements.append(Paragraph(
        "ZIMA Solutions Limited is pleased to submit this Technical Proposal in response to the above-referenced "
        "Request for Proposals for Microsoft D365 Enterprise Integration. We have carefully reviewed the RFP "
        "requirements and are confident in our ability to deliver a comprehensive solution that meets Ecobank's "
        "business and technical objectives.", styles['Body']))
    elements.append(Paragraph(
        "ZIMA Solutions is a Tanzanian-registered ICT services and innovation company specializing in enterprise "
        "system integration, digital transformation, and AI-powered automation for financial institutions. "
        "Our expertise spans CRM platform optimization, ERP integration, API gateway design, and business "
        "process automation — capabilities that directly align with the D365 Enterprise Integration scope "
        "outlined in this RFP.", styles['Body']))
    elements.append(Paragraph(
        "We bring particular strengths in:", styles['Body']))

    strengths = [
        "Enterprise system integration across banking, CRM, ERP, and payment platforms",
        "API design and middleware development for real-time and batch data synchronization",
        "Business process automation with AI-enhanced workflow optimization",
        "Security architecture design aligned with financial industry compliance standards",
        "Knowledge transfer and capacity building for sustainable operations",
    ]
    for s in strengths:
        elements.append(Paragraph(f"&bull; {s}", styles['ZBullet']))

    elements.append(Paragraph(
        "We understand Ecobank's vision to derive maximum business value from the D365 platform through "
        "seamless integration with third-party enterprise systems, enhanced automation, improved reporting, "
        "and strengthened security. Our proposal outlines a structured, phased approach to achieving these "
        "objectives while ensuring minimal disruption to ongoing operations.", styles['Body']))
    elements.append(Paragraph(
        "This bid shall remain valid for 90 days from the submission deadline as required. We welcome "
        "the opportunity to discuss our proposal further and are available for any clarifications.", styles['Body']))
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        "Yours faithfully,<br/><br/>"
        "<b>Andrew Stanslaus Mashamba</b><br/>"
        "Director, ZIMA Solutions Limited<br/>"
        "Email: info@zima.co.tz | Tel: +255 69 241 0353", styles['Body']))
    elements.append(PageBreak())
    return elements


def build_vendor_profile(styles):
    """Section 2: Vendor Profile."""
    elements = []
    elements.append(Paragraph("2. VENDOR PROFILE", styles['SectionHead']))

    # 2.1 Company Overview
    elements.append(Paragraph("2.1 Company Overview", styles['SubSection']))
    elements.append(Paragraph(
        "ZIMA Solutions Limited is a Tanzanian-registered ICT services and business innovation company, "
        "incorporated on 17 January 2025 under the Companies Act No. 12 of 2002 (Registration No. 181314605). "
        "Headquartered in Dar es Salaam, Tanzania, ZIMA Solutions specializes in enterprise software integration, "
        "digital transformation, artificial intelligence, and technology consultancy for financial institutions, "
        "government agencies, and corporate enterprises.", styles['Body']))

    # Company details table
    company_data = [
        [Paragraph("<b>Legal Name</b>", styles['TableCell']),
         Paragraph("ZIMA Solutions Limited", styles['TableCell'])],
        [Paragraph("<b>Registration No.</b>", styles['TableCell']),
         Paragraph("181314605 (BRELA, Tanzania)", styles['TableCell'])],
        [Paragraph("<b>TIN</b>", styles['TableCell']),
         Paragraph("181-314-605", styles['TableCell'])],
        [Paragraph("<b>Business License</b>", styles['TableCell']),
         Paragraph("BL01396912024-2500021919 (ICT Services)", styles['TableCell'])],
        [Paragraph("<b>Registered Office</b>", styles['TableCell']),
         Paragraph("Makongo, Near Ardhi University, Kinondoni, Dar es Salaam, Tanzania", styles['TableCell'])],
        [Paragraph("<b>Postal Address</b>", styles['TableCell']),
         Paragraph("P.O. Box 100025, Dar es Salaam, Tanzania", styles['TableCell'])],
        [Paragraph("<b>Telephone</b>", styles['TableCell']),
         Paragraph("+255 69 241 0353", styles['TableCell'])],
        [Paragraph("<b>Email</b>", styles['TableCell']),
         Paragraph("info@zima.co.tz", styles['TableCell'])],
        [Paragraph("<b>Website</b>", styles['TableCell']),
         Paragraph("www.zima.co.tz", styles['TableCell'])],
        [Paragraph("<b>Directors</b>", styles['TableCell']),
         Paragraph("Andrew Stanslaus Mashamba (Managing Director)<br/>Caroline Ceasar Shija (Director)", styles['TableCell'])],
    ]
    t = Table(company_data, colWidths=[50*mm, 110*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_BLUE),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 4*mm))

    elements.append(Paragraph(
        "ZIMA Solutions' core business objects, as defined in our Memorandum of Association, include:", styles['Body']))
    objects = [
        "Developing, producing, and distributing software applications, systems, and platforms for commercial, industrial, and financial purposes",
        "Offering consultancy, technical support, and services in software development, data management, artificial intelligence, cybersecurity, and cloud computing",
        "Designing, installing, maintaining, and managing IT infrastructure including hardware systems, servers, networking equipment, and databases",
        "Engaging in technology-enabled services such as IT outsourcing, managed services, and business process automation",
        "Entering into partnerships, joint ventures, and cooperation arrangements for technology delivery",
    ]
    for obj in objects:
        elements.append(Paragraph(f"&bull; {obj}", styles['ZBullet']))

    # 2.2 Key Personnel
    elements.append(Paragraph("2.2 Key Personnel", styles['SubSection']))
    elements.append(Paragraph(
        "ZIMA Solutions will assign the following key personnel to the Ecobank D365 project:", styles['Body']))

    personnel = [
        ["Role", "Name", "Expertise"],
        ["Project Lead / Solution Architect", "Andrew Mashamba",
         "Enterprise integration, CRM/ERP systems, API architecture, financial systems"],
        ["D365 Functional Consultant", "To be assigned",
         "D365 Sales, Customer Service, Marketing modules; Power Platform"],
        ["Integration Developer (Lead)", "To be assigned",
         "API development, middleware, Azure Integration Services, Dataverse"],
        ["Security & Compliance Specialist", "To be assigned",
         "RBAC, audit trails, data encryption, financial compliance standards"],
        ["Business Analyst", "To be assigned",
         "Requirements gathering, process mapping, stakeholder engagement"],
        ["QA/Testing Lead", "To be assigned",
         "UAT coordination, integration testing, performance testing"],
    ]
    pt = Table(personnel, colWidths=[45*mm, 35*mm, 80*mm])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph(
        "<i>Note: Specific named personnel for specialist roles will be confirmed upon contract award, "
        "sourced from our network of certified Microsoft D365 professionals and strategic partners.</i>",
        styles['Small']))

    # 2.3 Partnerships
    elements.append(Paragraph("2.3 Partnerships &amp; Certifications", styles['SubSection']))
    elements.append(Paragraph(
        "ZIMA Solutions leverages strategic technology partnerships to deliver comprehensive solutions:", styles['Body']))
    partnerships = [
        "<b>Microsoft Ecosystem:</b> ZIMA Solutions works within the Microsoft technology stack including "
        "Dynamics 365, Power Platform (Power Automate, Power BI, Power Apps), Azure cloud services, "
        "and Microsoft 365. We are pursuing Microsoft Solutions Partner designation.",
        "<b>Enterprise Integration:</b> Experience with industry-standard integration platforms including "
        "Azure Integration Services, REST/SOAP APIs, middleware solutions, and ETL tools.",
        "<b>Financial Technology:</b> Active integrations with Bank of Tanzania systems (RTGS, TIPS, GePG), "
        "core banking platforms, and payment infrastructure across East Africa.",
    ]
    for p in partnerships:
        elements.append(Paragraph(f"&bull; {p}", styles['ZBullet']))

    elements.append(PageBreak())
    return elements


def build_technical_proposal(styles):
    """Section 3: Technical Proposal."""
    elements = []
    elements.append(Paragraph("3. TECHNICAL PROPOSAL", styles['SectionHead']))

    # 3.1 Understanding
    elements.append(Paragraph("3.1 Understanding of Requirements", styles['SubSection']))
    elements.append(Paragraph(
        "Based on our thorough review of the RFP, we understand that Ecobank currently uses Microsoft Dynamics 365 "
        "as its core CRM platform to support customer engagement, sales, service, and internal business processes "
        "across its pan-African operations spanning 33 countries. The platform has been adopted by multiple business "
        "units with varying degrees of integration, configuration, and usage maturity.", styles['Body']))
    elements.append(Paragraph(
        "Ecobank now requires a certified Microsoft partner to:", styles['Body']))

    objectives = [
        "Assess, optimize, and integrate the current D365 environment with multiple enterprise systems",
        "Enable seamless and secure integration between D365 and third-party applications (core banking, identity verification, ERP/finance, workflow/BPM tools, reporting/analytics)",
        "Improve automation, data accuracy, and process efficiency across Clusters and Affiliates",
        "Enhance user experience and adoption through configuration, optimization, and training",
        "Deliver outcome-driven automation with measurable business impact (TAT reduction, cost efficiency, improved CX)",
        "Establish a scalable and sustainable D365 operating model",
    ]
    for o in objectives:
        elements.append(Paragraph(f"&bull; {o}", styles['ZBullet']))

    elements.append(Paragraph(
        "Our proposal addresses each of these requirements with a structured, phased approach leveraging our "
        "enterprise integration expertise and deep understanding of financial services technology.", styles['Body']))

    # 3.2 D365 Platform Assessment
    elements.append(Paragraph("3.2 D365 Platform Assessment Approach", styles['SubSection']))
    elements.append(Paragraph(
        "We propose a comprehensive assessment of the current D365 environment as the foundation for all "
        "subsequent integration and enhancement activities.", styles['Body']))

    elements.append(Paragraph("Assessment Scope:", styles['BodyBold']))
    assessment_items = [
        "<b>Environment Audit:</b> Review of current D365 tenant configuration, modules deployed (Sales, Customer Service, Marketing), customizations, plugins, and workflows across all Clusters and Affiliates",
        "<b>Data Architecture Review:</b> Analysis of Dataverse schema, entity relationships, data quality, duplication levels, and data governance practices",
        "<b>Integration Landscape Mapping:</b> Documentation of all existing integrations, data flows, API endpoints, middleware components, and their current health status",
        "<b>User Adoption Analysis:</b> Assessment of feature utilization rates, user satisfaction, training gaps, and process bottlenecks across business units",
        "<b>Performance Baseline:</b> System performance metrics including response times, concurrent user capacity, batch processing throughput, and storage utilization",
        "<b>Security & Compliance Review:</b> Evaluation of current RBAC configuration, security roles, audit logging, data encryption, and compliance with Ecobank IT security standards",
        "<b>Gap Analysis:</b> Identification of gaps between current state and desired state, prioritized by business impact and implementation complexity",
    ]
    for item in assessment_items:
        elements.append(Paragraph(f"&bull; {item}", styles['ZBullet']))

    elements.append(Paragraph("Assessment Deliverables:", styles['BodyBold']))
    deliverables = [
        "Current State Assessment Report with architecture diagrams",
        "Gap Analysis Matrix with prioritized recommendations",
        "Integration Landscape Map documenting all current and required data flows",
        "Risk Register identifying potential issues and mitigation strategies",
        "Optimization Roadmap aligned with Microsoft best practices",
    ]
    for d in deliverables:
        elements.append(Paragraph(f"&bull; {d}", styles['ZBullet']))

    # 3.3 Integration Strategy
    elements.append(Paragraph("3.3 Third-Party System Integration Strategy", styles['SubSection']))
    elements.append(Paragraph(
        "ZIMA Solutions will design and implement secure, scalable integrations between D365 and Ecobank's "
        "identified third-party systems using a combination of native Microsoft integration tools, custom "
        "APIs, and middleware solutions.", styles['Body']))

    elements.append(Paragraph("Integration Architecture Approach:", styles['BodyBold']))
    elements.append(Paragraph(
        "We propose a hub-and-spoke integration architecture centered on Azure Integration Services, "
        "providing a unified integration layer that connects D365 with all enterprise systems:", styles['Body']))

    int_systems = [
        ["System Category", "Integration Approach", "Data Pattern"],
        ["Core Banking Systems", "REST APIs + Azure Service Bus\nfor event-driven messaging", "Real-time + Batch\n(customer data, account info)"],
        ["Identity Verification\nPlatforms", "REST API integration with\nsecure token-based auth", "Real-time\n(KYC/AML verification)"],
        ["ERP & Finance Systems", "Azure Logic Apps + custom\nconnectors + Dataverse APIs", "Batch + Near-real-time\n(financial data, GL entries)"],
        ["Workflow & BPM Tools", "Power Automate + custom\nworkflow orchestration", "Event-driven\n(process triggers, approvals)"],
        ["Reporting & Analytics", "Power BI DirectQuery +\nAzure Synapse Analytics", "Near-real-time\n(dashboards, KPIs)"],
    ]
    it = Table(int_systems, colWidths=[40*mm, 55*mm, 55*mm])
    it.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ]))
    elements.append(it)
    elements.append(Spacer(1, 3*mm))

    elements.append(Paragraph("Integration Design Principles:", styles['BodyBold']))
    principles = [
        "<b>API-First Design:</b> All integrations built on well-documented RESTful APIs with OpenAPI specifications for maintainability and reusability",
        "<b>Error Handling & Resilience:</b> Comprehensive error logging, automatic retry mechanisms, dead-letter queues, and exception management for all integration points",
        "<b>Security by Design:</b> All data in transit encrypted (TLS 1.2+), OAuth 2.0/certificate-based authentication, API rate limiting, and comprehensive audit logging",
        "<b>Scalability:</b> Architecture designed to handle growth in transaction volumes, new affiliates, and additional third-party systems without rearchitecting",
        "<b>Monitoring & Alerting:</b> Real-time integration health dashboards with proactive alerting for failures, latency spikes, and anomalous patterns",
    ]
    for p in principles:
        elements.append(Paragraph(f"&bull; {p}", styles['ZBullet']))

    # 3.4 Enhancements & Optimization
    elements.append(Paragraph("3.4 D365 Enhancements &amp; Optimization", styles['SubSection']))
    elements.append(Paragraph(
        "We will configure, customize, and optimize D365 modules to enhance efficiency and user experience:", styles['Body']))

    elements.append(Paragraph("a) Module Configuration &amp; Customization", styles['SubSubSection']))
    module_items = [
        "<b>Sales Module:</b> Customized lead-to-opportunity pipelines, automated lead scoring with AI Builder, territory management for multi-country operations, and sales performance dashboards",
        "<b>Customer Service Module:</b> Omnichannel engagement (email, chat, phone), AI-powered case routing and escalation, SLA management with Cluster/Affiliate-level metrics, and customer 360-degree views",
        "<b>Marketing Module:</b> Customer journey orchestration, AI-driven segmentation, campaign performance analytics, and integration with communication channels",
    ]
    for m in module_items:
        elements.append(Paragraph(f"&bull; {m}", styles['ZBullet']))

    elements.append(Paragraph("b) Automation &amp; AI", styles['SubSubSection']))
    auto_items = [
        "<b>Intelligent Routing:</b> AI-enabled categorization, segmentation, and personalization for intelligent routing of cases and leads across Clusters and Affiliates",
        "<b>Predictive Escalation:</b> Machine learning models to predict case severity and automate proactive escalation before SLA breach",
        "<b>Proactive Complaint Management:</b> Early detection of complaint patterns using sentiment analysis and predictive analytics for improved customer engagement",
        "<b>Workflow Automation:</b> Power Automate flows for end-to-end business process automation with defined business rules and triggers",
        "<b>Customizable Alert Framework:</b> Configurable alerts for SLA violations, KPI deviations, and compliance requirements",
    ]
    for a in auto_items:
        elements.append(Paragraph(f"&bull; {a}", styles['ZBullet']))

    elements.append(Paragraph("c) Performance Tuning", styles['SubSubSection']))
    perf_items = [
        "Query optimization and index tuning for Dataverse operations",
        "Plugin and workflow performance review and optimization",
        "Asynchronous processing for heavy batch operations",
        "Caching strategies for frequently accessed data",
    ]
    for p in perf_items:
        elements.append(Paragraph(f"&bull; {p}", styles['ZBullet']))

    # 3.5 Reporting & Analytics
    elements.append(Paragraph("3.5 Reporting &amp; Analytics", styles['SubSection']))
    elements.append(Paragraph(
        "We will deliver comprehensive reporting and analytics capabilities:", styles['Body']))
    reporting = [
        "<b>Executive Dashboards:</b> Real-time Power BI dashboards for management with Cluster/Affiliate-level performance metrics, KPI tracking, and trend analysis",
        "<b>Operational Reports:</b> Automated operational reports for case resolution rates, sales pipeline health, customer satisfaction scores, and SLA compliance",
        "<b>Drill-Down Analytics:</b> Interactive reports with drill-down and filtering capabilities from Group level through Cluster to individual Affiliate",
        "<b>Predictive Analytics:</b> AI-driven forecasting for customer churn, sales projections, and service demand patterns",
        "<b>Enterprise Reporting Integration:</b> Seamless integration with existing enterprise reporting tools and data warehouses",
    ]
    for r in reporting:
        elements.append(Paragraph(f"&bull; {r}", styles['ZBullet']))

    # 3.6 Security & Compliance
    elements.append(Paragraph("3.6 Security &amp; Compliance", styles['SubSection']))
    elements.append(Paragraph(
        "Security is paramount for a financial institution operating across 33 countries. Our approach:", styles['Body']))
    security = [
        "<b>Role-Based Access Control (RBAC):</b> Review and optimize security roles and business units to ensure proper segregation of duties, least-privilege access, and Cluster/Affiliate data isolation",
        "<b>Data Encryption:</b> Ensure all data is encrypted in transit (TLS 1.2+) and at rest, with proper key management aligned with Ecobank IT security standards",
        "<b>Audit Logging:</b> Comprehensive audit trails for all data changes, user actions, and integration events to ensure traceability, accountability, and regulatory compliance",
        "<b>Compliance Alignment:</b> Configuration aligned with internal IT security standards, GDPR (for EU operations), and relevant country-specific financial regulatory requirements",
        "<b>Vulnerability Management:</b> Regular security assessments of custom components, plugins, and integration endpoints",
    ]
    for s in security:
        elements.append(Paragraph(f"&bull; {s}", styles['ZBullet']))

    # 3.7 Knowledge Transfer
    elements.append(Paragraph("3.7 Knowledge Transfer &amp; Support", styles['SubSection']))
    elements.append(Paragraph(
        "We are committed to minimizing long-term vendor dependency through comprehensive knowledge transfer:", styles['Body']))
    kt_items = [
        "<b>Documentation:</b> Complete technical documentation for all configurations, integrations, custom components, and operational procedures — maintained in a living documentation portal",
        "<b>Training Program:</b> Structured training for IT support teams (technical administration, troubleshooting, configuration changes) and end users (feature adoption, best practices)",
        "<b>Knowledge Transfer Sessions:</b> Hands-on workshops with internal teams during each project phase to build in-house capability progressively",
        "<b>Post-Implementation Support:</b> Warranty period with defined SLA for incident response, bug fixes, and optimization support",
        "<b>Sustainability Model:</b> Operational runbook and escalation procedures to ensure continuity after vendor handover",
    ]
    for k in kt_items:
        elements.append(Paragraph(f"&bull; {k}", styles['ZBullet']))

    elements.append(PageBreak())
    return elements


def build_methodology(styles):
    """Section 4: Implementation Methodology."""
    elements = []
    elements.append(Paragraph("4. IMPLEMENTATION METHODOLOGY", styles['SectionHead']))

    elements.append(Paragraph("4.1 Project Phases", styles['SubSection']))
    elements.append(Paragraph(
        "We propose a phased implementation approach using Agile methodology with milestone-based delivery:", styles['Body']))

    phases = [
        ["Phase", "Activities", "Duration", "Key Deliverables"],
        ["Phase 1:\nDiscovery &\nAssessment",
         "• Current state assessment\n• Stakeholder interviews\n• Gap analysis\n• Integration mapping",
         "4-6 weeks",
         "• Assessment Report\n• Gap Analysis\n• Integration Map\n• Optimization Roadmap"],
        ["Phase 2:\nDesign &\nArchitecture",
         "• Solution architecture design\n• Integration specifications\n• Security architecture\n• UX/UI design",
         "4-6 weeks",
         "• HLD & LLD documents\n• Integration specs\n• Security design\n• Prototype"],
        ["Phase 3:\nDevelopment &\nConfiguration",
         "• D365 configuration\n• Integration development\n• Custom components\n• Automation workflows",
         "10-14 weeks",
         "• Configured D365 modules\n• Integration layer\n• Automation flows\n• Test cases"],
        ["Phase 4:\nTesting &\nValidation",
         "• Unit & integration testing\n• UAT coordination\n• Performance testing\n• Security testing",
         "4-6 weeks",
         "• Test reports\n• UAT sign-off\n• Performance baseline\n• Security assessment"],
        ["Phase 5:\nDeployment &\nGo-Live",
         "• Production deployment\n• Data migration\n• Go-live support\n• Monitoring setup",
         "2-3 weeks",
         "• Production deployment\n• Monitoring dashboards\n• Go-live checklist"],
        ["Phase 6:\nKnowledge Transfer\n& Warranty",
         "• Documentation\n• Training delivery\n• Handover\n• Warranty support",
         "4-8 weeks",
         "• Technical documentation\n• Training materials\n• Operational runbook\n• Warranty support"],
    ]

    pt = Table(phases, colWidths=[30*mm, 50*mm, 22*mm, 50*mm])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 4*mm))

    # 4.2 Timeline
    elements.append(Paragraph("4.2 Project Timeline", styles['SubSection']))
    elements.append(Paragraph(
        "Total estimated project duration: <b>28-43 weeks</b> (approximately 7-11 months), depending on "
        "scope complexity, number of integrations, and Ecobank stakeholder availability. The timeline will "
        "be refined during the Discovery phase based on detailed requirements.", styles['Body']))

    # 4.3 Testing
    elements.append(Paragraph("4.3 Testing Strategy", styles['SubSection']))
    elements.append(Paragraph(
        "In accordance with Section 2.2.1 of the RFP, we will conduct comprehensive acceptance tests:", styles['Body']))
    testing = [
        "<b>Unit Testing:</b> Automated tests for all custom plugins, workflows, and integration components",
        "<b>Integration Testing:</b> End-to-end testing of all integration points with mock and live systems",
        "<b>User Acceptance Testing (UAT):</b> Facilitated UAT sessions with Ecobank business users across representative Clusters/Affiliates",
        "<b>Performance Testing:</b> Load and stress testing to validate concurrent user support and response time SLAs",
        "<b>Security Testing:</b> Penetration testing and vulnerability scanning of custom components and integration endpoints",
        "<b>Regression Testing:</b> Automated regression suite to ensure existing functionality is preserved during enhancements",
    ]
    for t_item in testing:
        elements.append(Paragraph(f"&bull; {t_item}", styles['ZBullet']))

    elements.append(PageBreak())
    return elements


def build_references(styles):
    """Section 5: References."""
    elements = []
    elements.append(Paragraph("5. REFERENCES &amp; EXPERIENCE", styles['SectionHead']))

    elements.append(Paragraph(
        "ZIMA Solutions brings relevant experience from enterprise system integration projects across "
        "the financial services sector in East Africa. Below is a summary of representative engagements:", styles['Body']))

    elements.append(Paragraph("a) Enterprise System Integration Experience", styles['SubSubSection']))
    exp_items = [
        "<b>Core Banking Integration:</b> Integrated CRM and loan management systems with core banking platforms for multiple financial institutions, enabling real-time customer data synchronization and automated workflow triggers",
        "<b>Payment Gateway Integration:</b> Implemented API-based integrations with RTGS, TIPS, GePG, and TanQR payment systems, supporting real-time transaction processing and reconciliation",
        "<b>Identity Verification Platform:</b> Built integration layer connecting customer onboarding systems with NIDA (National Identification Authority) for real-time KYC verification",
        "<b>ERP/Finance Integration:</b> Designed and deployed integrations between business applications and financial systems for automated GL posting, reporting, and reconciliation",
        "<b>AI-Powered CRM Enhancement:</b> Deployed AI agents for customer engagement including intelligent case routing, automated responses, and predictive analytics",
    ]
    for e in exp_items:
        elements.append(Paragraph(f"&bull; {e}", styles['ZBullet']))

    elements.append(Paragraph("b) Technology Stack Experience", styles['SubSubSection']))
    tech_items = [
        "Microsoft Dynamics 365 (CRM modules: Sales, Customer Service, Marketing)",
        "Microsoft Power Platform (Power Automate, Power BI, Power Apps, AI Builder)",
        "Azure Cloud Services (Azure Functions, Logic Apps, Service Bus, API Management)",
        "REST/SOAP API design, development, and integration",
        "Database design and optimization (SQL Server, Dataverse, PostgreSQL)",
        "Python, C#/.NET, JavaScript/TypeScript for custom development",
        "CI/CD pipelines and DevOps practices for enterprise deployments",
    ]
    for t_item in tech_items:
        elements.append(Paragraph(f"&bull; {t_item}", styles['ZBullet']))

    elements.append(Paragraph("c) Financial Institution Expertise", styles['SubSubSection']))
    elements.append(Paragraph(
        "ZIMA Solutions has served 50+ client organizations, with particular depth in financial services "
        "including banks, SACCOs, microfinance institutions, and fintech companies. We understand the "
        "regulatory environment, compliance requirements, and operational complexity of banking operations "
        "in the African market.", styles['Body']))

    elements.append(Paragraph("d) Customer Retention Plan", styles['SubSubSection']))
    elements.append(Paragraph(
        "Our customer retention strategy is built on:", styles['Body']))
    retention = [
        "<b>Continuous Value Delivery:</b> Regular system health checks, optimization recommendations, and proactive issue identification",
        "<b>Dedicated Account Management:</b> Named account manager for each client relationship with quarterly business reviews",
        "<b>Knowledge Sharing:</b> Regular training sessions and knowledge transfer to build client self-sufficiency",
        "<b>Responsive Support:</b> SLA-backed support with defined response and resolution times",
        "<b>Innovation Partnership:</b> Proactive identification of new Microsoft features and capabilities that can benefit the client",
    ]
    for r in retention:
        elements.append(Paragraph(f"&bull; {r}", styles['ZBullet']))

    elements.append(PageBreak())
    return elements


def build_documentation(styles):
    """Section 6: Documentation & Deliverables."""
    elements = []
    elements.append(Paragraph("6. DOCUMENTATION &amp; DELIVERABLES", styles['SectionHead']))
    elements.append(Paragraph(
        "In accordance with Section 2.2.2 of the RFP, we will deliver the following documentation:", styles['Body']))

    docs = [
        ["Document", "Description", "Phase"],
        ["Feasibility Report", "Assessment of current D365 environment viability\nand integration feasibility", "Phase 1"],
        ["Proof of Concept Report", "POC test success criteria, results, and\nrecommendations", "Phase 2"],
        ["High Level Design (HLD)", "Solution architecture, integration patterns,\ndata flow diagrams, security architecture", "Phase 2"],
        ["Low Level Design (LLD)", "Detailed technical specifications, API contracts,\ndata mapping, configuration details", "Phase 2"],
        ["Capability Data Sheets", "Technical capabilities of proposed solution\ncomponents", "Phase 2"],
        ["Reference Sites", "Documented reference implementations\nand case studies", "Phase 2"],
        ["Test Plans & Reports", "Test strategy, test cases, execution results,\nand sign-off documents", "Phase 4"],
        ["Training Materials", "User guides, admin guides, video tutorials,\nand quick reference cards", "Phase 6"],
        ["Technical Documentation", "Complete system documentation, integration\nguides, and operational runbooks", "Phase 6"],
    ]
    dt = Table(docs, colWidths=[42*mm, 72*mm, 25*mm])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ]))
    elements.append(dt)

    elements.append(PageBreak())
    return elements


def build_legal_docs_section(styles):
    """Section 7: Company Legal Documents."""
    elements = []
    elements.append(Paragraph("7. COMPANY LEGAL DOCUMENTS", styles['SectionHead']))
    elements.append(Paragraph(
        "The following company legal documents are attached as part of this submission:", styles['Body']))

    legal_docs = [
        "Certificate of Incorporation (Companies Act, 2002) — Registration No. 181314605",
        "Certificate of Registration for Taxpayer Identification Number (TIN: 181-314-605)",
        "Business License — ICT Services Local (Kinondoni Municipal Council, valid to January 2026)",
        "Memorandum and Articles of Association of ZIMA Solutions Limited",
    ]
    for i, doc in enumerate(legal_docs, 1):
        elements.append(Paragraph(f"<b>{i}.</b> {doc}", styles['Body']))

    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        "<i><b>Note on Financial Statements:</b> As ZIMA Solutions Limited was incorporated on 17 January 2025, "
        "our first audited financial statements will be available by 1 May 2026 following the completion of "
        "our inaugural financial year (ending 31 December 2025). We are pleased to provide the above "
        "legal documents as evidence of our corporate standing and compliance.</i>", styles['Body']))

    elements.append(Spacer(1, 6*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=GRAY, spaceAfter=4*mm))
    elements.append(Paragraph(
        "<b>END OF TECHNICAL PROPOSAL</b>",
        ParagraphStyle('EndNote', fontSize=12, textColor=BLUE, fontName='Helvetica-Bold',
                       alignment=TA_CENTER, spaceAfter=4*mm)))
    elements.append(Paragraph(
        "ZIMA Solutions Limited<br/>"
        "Makongo, Near Ardhi University, Kinondoni, Dar es Salaam, Tanzania<br/>"
        "info@zima.co.tz | +255 69 241 0353 | www.zima.co.tz",
        ParagraphStyle('EndContact', fontSize=10, textColor=GRAY, fontName='Helvetica',
                       alignment=TA_CENTER, leading=14)))

    return elements


def generate_proposal():
    """Generate the complete technical proposal PDF."""
    styles = get_styles()

    # Proposal PDF (without company docs)
    proposal_pdf = os.path.join(OUTPUT_DIR, "ZIMA_Technical_Proposal_D365.pdf")
    final_pdf = os.path.join(OUTPUT_DIR, "ZIMA_Proposal_ECOBANK-2026-001.pdf")

    doc = SimpleDocTemplate(
        proposal_pdf,
        pagesize=A4,
        topMargin=20*mm,
        bottomMargin=20*mm,
        leftMargin=20*mm,
        rightMargin=20*mm,
    )

    elements = []

    # Cover page
    elements.extend(build_cover_page(styles))

    # Table of Contents
    elements.extend(build_toc(styles))

    # Section 1: Cover Letter
    elements.extend(build_cover_letter(styles))

    # Section 2: Vendor Profile
    elements.extend(build_vendor_profile(styles))

    # Section 3: Technical Proposal
    elements.extend(build_technical_proposal(styles))

    # Section 4: Implementation Methodology
    elements.extend(build_methodology(styles))

    # Section 5: References
    elements.extend(build_references(styles))

    # Section 6: Documentation
    elements.extend(build_documentation(styles))

    # Section 7: Legal Documents
    elements.extend(build_legal_docs_section(styles))

    # Build proposal PDF
    doc.build(elements, onFirstPage=first_page, onLaterPages=header_footer)
    print(f"[OK] Technical proposal generated: {proposal_pdf}")

    # Merge with company documents
    merger = PdfMerger()
    merger.append(proposal_pdf)
    if os.path.isfile(COMPANY_DOCS_PDF):
        merger.append(COMPANY_DOCS_PDF)
        print(f"[OK] Appended company documents: {COMPANY_DOCS_PDF}")
    merger.write(final_pdf)
    merger.close()
    print(f"[OK] Final proposal: {final_pdf}")
    print(f"     Size: {os.path.getsize(final_pdf) / 1024:.0f} KB")

    return final_pdf


if __name__ == '__main__':
    generate_proposal()
