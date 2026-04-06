#!/usr/bin/env python3
"""
Generate PDF tender applications and send via email.
Each application = cover letter + company profile + custom tender response + company docs (single PDF).
Email body = short intro referencing the attachment.

The tender response is CUSTOM for each tender — it reads extracted tender documents,
parses requirements, and generates a specific response addressing each requirement.
"""

import json, os, sys, time, smtplib, ssl, re, glob, subprocess, hashlib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from PyPDF2 import PdfMerger

PROJECT = "/Volumes/DATA/PROJECTS/TENDERS"
DB_FILE = f"{PROJECT}/applications/requirements_database.json"
COMPANY_DOCS_PDF = f"{PROJECT}/applications/ZIMA_Company_Documents.pdf"
CONFIG_FILE = f"{PROJECT}/config/email.json"
SENT_LOG = f"{PROJECT}/applications/sent_log.json"
BCC = "andrew.s.mashamba@gmail.com"

BLUE = HexColor("#1565C0")
DARK = HexColor("#222222")
GRAY = HexColor("#666666")
LIGHT_BLUE = HexColor("#E3F2FD")

# ─── Company profile (defaults to ZIMA, overridden by --company-profile) ───
COMPANY = {
    "company_name": "ZIMA Solutions Limited",
    "tagline": "Digital Transformation \u2022 Financial Technology \u2022 System Integration",
    "tin": "181-314-605",
    "registration": "Companies Act, 2002 (No. 181314605)",
    "incorporation_date": "January 2025",
    "business_license": "ICT Services (Local) \u2014 Kinondoni Municipal Council",
    "directors": "Andrew Stanslaus Mashamba, Caroline Ceasar Shija",
    "contact_person": "Andrew Stanslaus Mashamba",
    "contact_title": "Director",
    "address": "Makongo, Near Ardhi University, Kinondoni, Dar es Salaam",
    "phone": "+255 69 241 0353",
    "contact_email": "info@zima.co.tz",
    "website": "zima.co.tz",
    "share_capital": "TZS 1,000,000 (10,000 ordinary shares @ TZS 100)",
    "capabilities": [
        "Bank of Tanzania integrations: RTGS, TIPS, GePG, NIDA (4 active integrations, 99.9% uptime)",
        "Core banking system implementation for banks, SACCOs, microfinance",
        "AI & Machine Learning: conversational AI agents (WhatsApp, web), fraud detection, credit scoring",
        "Digital banking: mobile banking, internet banking, USSD, agency banking",
        "Payment solutions: TanQR, mobile money integration, payment gateways",
        "API Gateway & middleware for enterprise integration",
        "Enterprise software: ERP, HR, Loan, School, Healthcare management systems",
        "Cybersecurity: vulnerability assessments, pen testing, compliance audits",
        "ICT infrastructure: supply, install, maintain servers, networking, UPS, CCTV",
        "Technology consultancy: digital transformation strategy, feasibility studies",
    ],
    "key_facts": [
        "20+ enterprise projects delivered, 50+ client organizations",
        "Strategic partnerships with technology vendors and contractors for non-ICT delivery",
    ],
    "partnership_model": (
        "For non-ICT tenders (construction, supplies, facilities), partners with specialized firms "
        "and adds technology value: project management systems, digital tracking, IoT monitoring, "
        "analytics dashboards."
    ),
    "company_docs_pdf": f"{PROJECT}/applications/ZIMA_Company_Documents.pdf",
    "company_docs_dir": f"{PROJECT}/frontend/public/company_documents/zima_solutions_limited",
}


def _load_company_profile(profile_path):
    """Load a company profile JSON file and override COMPANY defaults."""
    global COMPANY
    try:
        with open(profile_path) as f:
            profile = json.load(f)
        # Override only keys that are provided
        for key in profile:
            COMPANY[key] = profile[key]
        print(f"  Loaded company profile: {COMPANY['company_name']}")
    except Exception as e:
        print(f"  Warning: Could not load company profile: {e}")


def _build_company_profile_text():
    """Build a text description of the company for AI prompts."""
    lines = [f"{COMPANY['company_name']}"]
    if COMPANY.get('tin'):
        lines[0] += f" (TIN: {COMPANY['tin']})"
    if COMPANY.get('incorporation_date'):
        lines[0] += f", incorporated {COMPANY['incorporation_date']}"
    lines[0] += "."
    if COMPANY.get('address'):
        lines.append(f"Located at: {COMPANY['address']}")

    if COMPANY.get('capabilities'):
        lines.append("\nCORE CAPABILITIES:")
        for cap in COMPANY['capabilities']:
            lines.append(f"- {cap}")

    if COMPANY.get('key_facts'):
        lines.append("\nKEY FACTS:")
        for fact in COMPANY['key_facts']:
            lines.append(f"- {fact}")

    if COMPANY.get('directors'):
        lines.append(f"\nDirectors: {COMPANY['directors']}")
    if COMPANY.get('contact_email'):
        lines.append(f"Email: {COMPANY['contact_email']}")
    if COMPANY.get('phone'):
        lines.append(f"Phone: {COMPANY['phone']}")
    if COMPANY.get('website'):
        lines.append(f"Website: {COMPANY['website']}")

    if COMPANY.get('partnership_model'):
        lines.append(f"\nPARTNERSHIP MODEL: {COMPANY['partnership_model']}")

    return "\n".join(lines)

# ─── Styles ───
def get_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle('ZimaTitle', fontSize=18, textColor=BLUE, fontName='Helvetica-Bold',
                         spaceAfter=4*mm))
    s.add(ParagraphStyle('ZimaSubtitle', fontSize=10, textColor=GRAY, fontName='Helvetica',
                         spaceAfter=6*mm))
    s.add(ParagraphStyle('SectionHead', fontSize=13, textColor=BLUE, fontName='Helvetica-Bold',
                         spaceBefore=6*mm, spaceAfter=3*mm))
    s.add(ParagraphStyle('SubSection', fontSize=11, textColor=BLUE, fontName='Helvetica-Bold',
                         spaceBefore=4*mm, spaceAfter=2*mm))
    s.add(ParagraphStyle('Body', fontSize=10.5, textColor=DARK, fontName='Helvetica',
                         leading=15, alignment=TA_JUSTIFY, spaceAfter=3*mm))
    s.add(ParagraphStyle('BodyBold', fontSize=10.5, textColor=DARK, fontName='Helvetica-Bold',
                         leading=15, spaceAfter=2*mm))
    s.add(ParagraphStyle('ZimaBullet', fontSize=10.5, textColor=DARK, fontName='Helvetica',
                         leading=15, leftIndent=15, bulletIndent=5, spaceAfter=2*mm,
                         alignment=TA_JUSTIFY))
    s.add(ParagraphStyle('Small', fontSize=9, textColor=GRAY, fontName='Helvetica',
                         leading=12, spaceAfter=2*mm))
    s.add(ParagraphStyle('Footer', fontSize=8, textColor=GRAY, fontName='Helvetica',
                         alignment=TA_CENTER))
    return s


def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(BLUE)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)
    canvas_obj.setFont('Helvetica-Bold', 9)
    canvas_obj.setFillColor(BLUE)
    canvas_obj.drawString(20*mm, A4[1] - 13*mm, COMPANY['company_name'])
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GRAY)
    header_right = " | ".join(filter(None, [COMPANY.get('contact_email'), COMPANY.get('phone'), COMPANY.get('website')]))
    canvas_obj.drawRightString(A4[0] - 20*mm, A4[1] - 13*mm, header_right)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GRAY)
    footer_left = " | ".join(filter(None, [COMPANY['company_name'],
                                           f"TIN: {COMPANY['tin']}" if COMPANY.get('tin') else None,
                                           COMPANY.get('address', '')]))
    canvas_obj.drawString(20*mm, 12*mm, footer_left)
    canvas_obj.drawRightString(A4[0] - 20*mm, 12*mm, f"Page {doc.page}")
    canvas_obj.restoreState()


# ═══════════════════════════════════════════════════════════════════════════════
# TENDER CONTENT ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def read_tender_content(tender):
    """Read all extracted text files for a tender from the institution downloads.
    Also attempts to extract text from original PDFs if extracted text is insufficient."""
    slug = tender.get('institution_slug', '')
    tid = tender.get('tender_id', '')
    title = (tender.get('title', '') or '').lower()

    # Build alternative ID patterns:
    # AZANIA-BANK-2026-007 → also try AZANIA-2026-007, AZANIABANK-2026-007
    tid_parts = tid.rsplit('-', 2)  # e.g., ['AZANIA-BANK', '2026', '007']
    alt_ids = [tid]
    if len(tid_parts) == 3:
        prefix = tid_parts[0]
        # Try removing middle slug parts: AZANIA-BANK → AZANIA
        prefix_parts = prefix.split('-')
        if len(prefix_parts) > 1:
            alt_ids.append(f"{prefix_parts[0]}-{tid_parts[1]}-{tid_parts[2]}")
            alt_ids.append(f"{''.join(prefix_parts)}-{tid_parts[1]}-{tid_parts[2]}")

    # Try multiple path patterns
    patterns = []
    for alt_id in alt_ids:
        patterns.append(f"{PROJECT}/institutions/{slug}/downloads/{alt_id}/extracted/*.txt")
        patterns.append(f"{PROJECT}/institutions/{slug}/downloads/{alt_id.lower()}/extracted/*.txt")

    all_text = ""
    seen_files = set()
    for pattern in patterns:
        files = sorted(glob.glob(pattern))
        for fpath in files:
            if fpath in seen_files:
                continue
            seen_files.add(fpath)
            try:
                with open(fpath, 'r', errors='replace') as f:
                    content = f.read()
                    all_text += content + "\n\n"
            except Exception:
                continue

    # Also try reading original PDFs that may not have extracted text
    for alt_id in alt_ids:
        for orig_pattern in [
            f"{PROJECT}/institutions/{slug}/downloads/{alt_id}/original/*.pdf",
            f"{PROJECT}/institutions/{slug}/downloads/{alt_id.lower()}/original/*.pdf",
        ]:
            for pdf_path in sorted(glob.glob(orig_pattern)):
                # Skip if we already have extracted text for this PDF
                pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
                extracted_dir = os.path.join(os.path.dirname(os.path.dirname(pdf_path)), 'extracted')
                if os.path.isfile(os.path.join(extracted_dir, pdf_name + '.txt')):
                    continue
                # Try extracting text from the PDF
                try:
                    from tools.pdf.reader import extract_text as pdf_extract
                    pdf_text = pdf_extract(pdf_path)
                    if pdf_text and len(pdf_text.strip()) > 100:
                        all_text += f"\n\n--- Content from {os.path.basename(pdf_path)} ---\n{pdf_text}\n\n"
                except Exception:
                    pass

    # If still no content, try to find files by matching tender title keywords in filenames
    if len(all_text) < 200 and title:
        # Search all extracted files for this institution
        all_extracted = glob.glob(f"{PROJECT}/institutions/{slug}/downloads/*/extracted/*.txt")
        title_words = [w for w in re.split(r'\W+', title) if len(w) > 4]
        for fpath in all_extracted:
            if fpath in seen_files:
                continue
            fname = os.path.basename(fpath).lower()
            # Check if filename matches title keywords
            matches = sum(1 for w in title_words if w in fname)
            if matches >= 2 or (matches >= 1 and len(title_words) <= 2):
                seen_files.add(fpath)
                try:
                    with open(fpath, 'r', errors='replace') as f:
                        content = f.read()
                        all_text += content + "\n\n"
                except Exception:
                    continue

    # Include tender JSON metadata as context
    tender_meta = []
    for key in ['title', 'description', 'reference_number', 'closing_date', 'closing_time',
                'category', 'eligibility', 'contact', 'source_url', 'documents',
                'scope_of_work', 'zima_capability_match']:
        val = tender.get(key)
        if val:
            tender_meta.append(f"{key}: {val}")
    if tender_meta:
        meta_block = "\n--- TENDER METADATA ---\n" + "\n".join(tender_meta) + "\n"
        all_text = meta_block + "\n" + all_text

    return all_text.strip()


def _extract_section(text, start_patterns, end_patterns, max_chars=3000):
    """Extract a section from tender text between start and end patterns."""
    text_lower = text.lower()
    best_start = -1
    for pat in start_patterns:
        idx = text_lower.find(pat.lower())
        if idx >= 0 and (best_start < 0 or idx < best_start):
            best_start = idx

    if best_start < 0:
        return ""

    # Find end
    search_from = best_start + 50
    best_end = min(best_start + max_chars, len(text))
    for pat in end_patterns:
        idx = text_lower.find(pat.lower(), search_from)
        if 0 < idx < best_end:
            best_end = idx

    section = text[best_start:best_end].strip()
    # Clean up extracted text
    section = re.sub(r'\n{3,}', '\n\n', section)
    section = re.sub(r'[ \t]{3,}', ' ', section)
    return section


def analyze_tender_requirements(text, tender):
    """Parse tender document text to extract structured requirements."""
    reqs = {
        'scope_of_work': '',
        'eligibility': [],
        'required_documents': [],
        'evaluation_criteria': [],
        'deliverables': [],
        'timeline': '',
        'special_requirements': [],
        'technical_specs': '',
        'tender_type': '',  # works, services, goods, consultancy, prequalification
        'submission_method': '',
        'lot_details': [],
    }

    if not text or len(text) < 100:
        return reqs

    text_lower = text.lower()

    # Detect tender type
    if any(w in text_lower for w in ['construction', 'building', 'renovation', 'civil works', 'proposed works']):
        reqs['tender_type'] = 'works'
    elif any(w in text_lower for w in ['consultancy', 'consulting', 'advisory', 'consultant']):
        reqs['tender_type'] = 'consultancy'
    elif any(w in text_lower for w in ['supply and delivery', 'supply of', 'provision of goods', 'procurement of']):
        reqs['tender_type'] = 'goods'
    elif any(w in text_lower for w in ['prequalification', 'pre-qualification', 'registration of']):
        reqs['tender_type'] = 'prequalification'
    else:
        reqs['tender_type'] = 'services'

    # Extract scope of work
    scope = _extract_section(text, [
        'scope of work', 'scope of services', 'terms of reference',
        'description of services', 'objective of the assignment',
        'background and objectives', 'project description',
        'the assignment', 'scope of supply',
    ], [
        'section', 'eligibility', 'qualification', 'evaluation',
        'tender data', 'instructions to', 'form of tender',
    ], max_chars=4000)
    reqs['scope_of_work'] = scope

    # Extract eligibility requirements
    elig_text = _extract_section(text, [
        'eligibility', 'qualification criteria', 'minimum requirements',
        'mandatory requirements', 'pre-qualification criteria',
        'tenderer shall', 'bidder shall',
    ], [
        'evaluation', 'price schedule', 'form of tender', 'tender data',
    ], max_chars=3000)

    if elig_text:
        # Parse bullet points or numbered items
        lines = elig_text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 20 and any(line.startswith(p) for p in
                ['a)', 'b)', 'c)', 'd)', 'e)', 'f)', 'i)', 'ii)', 'iii)',
                 '(a)', '(b)', '(c)', '(d)', '(i)', '(ii)',
                 '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.',
                 '-', '•', '*']):
                reqs['eligibility'].append(line.strip('- •*').strip())
            elif re.match(r'^\d+[\.\)]\s', line) and len(line) > 20:
                reqs['eligibility'].append(re.sub(r'^\d+[\.\)]\s*', '', line).strip())

    # Extract required documents from checklist
    doc_patterns = [
        r'certificate\s+of\s+(incorporation|registration)',
        r'tax\s+(clearance|identification|compliance)',
        r'business\s+licen[sc]e',
        r'audited?\s+financial\s+statements?',
        r'power\s+of\s+attorney',
        r'tender\s+secur(ity|ing)',
        r'form\s+of\s+tender',
        r'price\s+schedule',
        r'company\s+profile',
        r'cv\s*(s|\'s)?\s*(of|for)',
        r'list\s+of\s+(similar|major|completed)\s+(projects?|works?|clients?)',
        r'memorandum\s+(and|&)\s+articles',
        r'proof\s+of\s+registration',
        r'insurance\s+(certificate|policy)',
        r'bank\s+(statement|guarantee|reference)',
        r'vat\s+(certificate|registration)',
    ]
    for pat in doc_patterns:
        matches = re.findall(pat, text_lower)
        if matches:
            # Get the full line for context
            for m in re.finditer(pat, text_lower):
                start = max(0, text_lower.rfind('\n', 0, m.start()))
                end = text_lower.find('\n', m.end())
                if end < 0: end = min(m.end() + 100, len(text_lower))
                doc_line = text[start:end].strip()
                if doc_line and doc_line not in reqs['required_documents']:
                    reqs['required_documents'].append(doc_line[:200])

    # Extract evaluation criteria
    eval_text = _extract_section(text, [
        'evaluation criteria', 'evaluation method', 'assessment criteria',
        'marking scheme', 'scoring criteria', 'technical evaluation',
    ], [
        'price schedule', 'form of tender', 'conditions of contract',
        'general conditions',
    ], max_chars=2000)

    if eval_text:
        # Look for percentage/point allocations
        for line in eval_text.split('\n'):
            line = line.strip()
            if re.search(r'\d+\s*(%|points?|marks?)', line) and len(line) > 10:
                reqs['evaluation_criteria'].append(line[:200])

    # Extract deliverables
    deliv_text = _extract_section(text, [
        'deliverables', 'expected output', 'expected deliverable',
        'key deliverable', 'outputs',
    ], [
        'timeline', 'schedule', 'evaluation', 'payment',
    ], max_chars=2000)
    if deliv_text:
        for line in deliv_text.split('\n'):
            line = line.strip()
            if len(line) > 15 and (line.startswith(('-', '•', '*')) or re.match(r'^\d+[\.\)]', line)):
                reqs['deliverables'].append(re.sub(r'^[\d\.\)\-\•\*\s]+', '', line).strip()[:200])

    # Extract timeline
    timeline = _extract_section(text, [
        'duration', 'timeline', 'implementation period', 'contract period',
        'completion date', 'time frame', 'period of assignment',
    ], [
        'evaluation', 'price', 'payment', 'section',
    ], max_chars=1000)
    reqs['timeline'] = timeline

    # Extract technical specifications
    tech = _extract_section(text, [
        'technical specification', 'technical requirement', 'system requirement',
        'functional requirement', 'specifications',
    ], [
        'price schedule', 'form of tender', 'evaluation',
    ], max_chars=3000)
    reqs['technical_specs'] = tech

    # Detect lot structure
    lot_matches = re.findall(r'lot\s*(\d+)[:\s]*([^\n]+)', text_lower)
    for lot_num, lot_desc in lot_matches[:10]:
        reqs['lot_details'].append(f"Lot {lot_num}: {lot_desc.strip()[:150]}")

    # Extract special requirements
    special_patterns = [
        (r'joint\s+venture', 'Joint ventures/consortiums are accepted'),
        (r'site\s+visit', 'Site visit may be required'),
        (r'pre-?tender\s+meeting', 'Pre-tender meeting scheduled'),
        (r'bid\s+security|tender\s+security', 'Tender security/bid bond required'),
        (r'performance\s+(bond|guarantee|security)', 'Performance bond/guarantee required'),
        (r'domestic\s+preference', 'Domestic preference applies'),
        (r'ppra|public\s+procurement', 'Follows PPRA/PPA regulations'),
        (r'nest|e-?procurement', 'Submitted through NeST e-procurement'),
    ]
    for pat, desc in special_patterns:
        if re.search(pat, text_lower):
            reqs['special_requirements'].append(desc)

    # NeST submission
    if 'nest' in text_lower or 'e-procurement' in text_lower:
        reqs['submission_method'] = 'NeST (National e-Procurement System)'

    return reqs


# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN-SPECIFIC RESPONSE MAPPING
# ═══════════════════════════════════════════════════════════════════════════════

# Maps tender keywords → Zima's specific relevant experience and approach
DOMAIN_RESPONSES = {
    'banking': {
        'keywords': ['banking', 'bank', 'financial institution', 'core banking'],
        'experience': (
            "ZIMA Solutions has delivered 20+ enterprise-grade technology projects for banks and "
            "financial institutions in Tanzania, including core banking system integrations, digital "
            "banking platform deployments, and regulatory reporting systems. We maintain 4 active "
            "Bank of Tanzania system integrations (RTGS, TIPS, GePG, NIDA) with 99.9% uptime."
        ),
        'approach': (
            "Our approach is built on deep understanding of BoT regulatory requirements, banking "
            "operations workflows, and the security standards required for financial systems. "
            "We deploy using agile methodology with milestone-based delivery and rigorous security testing."
        ),
    },
    'payment': {
        'keywords': ['payment', 'mobile money', 'gepg', 'rtgs', 'tips', 'tanqr', 'e-payment', 'epayment'],
        'experience': (
            "ZIMA Solutions is an active integrator with Tanzania's national payment infrastructure. "
            "We have implemented RTGS (Real-Time Gross Settlement), TIPS (Tanzania Instant Payment System), "
            "GePG (Government e-Payment Gateway), and TanQR merchant payment solutions. Our payment "
            "gateway platform processes transactions with 99.9% reliability."
        ),
        'approach': (
            "We bring production-proven payment integration expertise, PCI-compliant security practices, "
            "and deep experience with BoT's technical specifications and certification requirements."
        ),
    },
    'ai_data': {
        'keywords': ['artificial intelligence', ' ai ', 'machine learning', 'data analytics',
                     'data warehouse', 'big data', 'chatbot', 'automation'],
        'experience': (
            "ZIMA Solutions designs and deploys AI-powered solutions including conversational AI agents "
            "(WhatsApp, Web, API), fraud detection models, credit scoring systems, and predictive analytics "
            "platforms. We serve 50+ client organizations with intelligent automation solutions."
        ),
        'approach': (
            "We follow a data-driven methodology: data assessment, model development, integration with "
            "existing systems, validation, and continuous learning. Our AI solutions are designed for "
            "the Tanzanian context with support for Swahili language processing."
        ),
    },
    'cybersecurity': {
        'keywords': ['cybersecurity', 'security audit', 'penetration test', 'information security',
                     'vulnerability', 'firewall', 'security assessment'],
        'experience': (
            "ZIMA Solutions provides comprehensive cybersecurity services including vulnerability assessments, "
            "penetration testing, security architecture review, and compliance auditing. We support "
            "financial institutions in meeting BoT cybersecurity guidelines and international standards "
            "(ISO 27001, PCI DSS)."
        ),
        'approach': (
            "Our security practice follows industry-standard methodologies (OWASP, NIST, ISO 27001) "
            "with certified security professionals. We deliver actionable findings with remediation "
            "roadmaps and can support implementation of security improvements."
        ),
    },
    'network_infrastructure': {
        'keywords': ['network', 'infrastructure', 'server', 'data center', 'ict equipment',
                     'hardware', 'switch', 'router', 'cabling', 'cctv', 'laptop', 'desktop',
                     'computer', 'printer', 'scanner', 'photocopier'],
        'experience': (
            "ZIMA Solutions maintains strategic partnerships with leading technology vendors and "
            "equipment manufacturers. We supply, install, configure, and maintain ICT infrastructure "
            "including servers, networking equipment, UPS systems, surveillance systems, and "
            "structured cabling for enterprise environments."
        ),
        'approach': (
            "Through our vendor partnerships, we provide end-to-end infrastructure solutions: "
            "needs assessment, solution design, procurement, installation, configuration, testing, "
            "and ongoing maintenance with SLA-backed support."
        ),
    },
    'software_development': {
        'keywords': ['software', 'system development', 'application development', 'web application',
                     'mobile app', 'portal', 'website', 'platform development', 'erp', 'mis',
                     'management information system', 'management system'],
        'experience': (
            "ZIMA Solutions has built and deployed 20+ enterprise software systems including ERP solutions, "
            "management information systems, loan management platforms, SACCO management systems, "
            "HR management systems, school management systems, and custom web/mobile applications."
        ),
        'approach': (
            "We follow Agile/Scrum methodology with iterative sprints, continuous integration, "
            "and user-centric design. Each project includes requirements documentation, UI/UX design, "
            "development, testing (unit, integration, UAT), deployment, training, and warranty support."
        ),
    },
    'consultancy': {
        'keywords': ['consultancy', 'consulting', 'advisory', 'feasibility study', 'assessment',
                     'review', 'strategy', 'digital transformation', 'capacity building', 'training'],
        'experience': (
            "ZIMA Solutions provides strategic technology consultancy to 50+ organizations across Tanzania. "
            "Our consultancy services include digital transformation strategy, system architecture design, "
            "business requirements documentation, technology feasibility studies, IT security audits, "
            "and regulatory compliance assessment."
        ),
        'approach': (
            "Our consultancy methodology combines stakeholder engagement, current-state analysis, "
            "gap assessment, best-practice benchmarking, and actionable recommendations with "
            "implementation roadmaps. We deliver practical, implementable solutions — not theoretical reports."
        ),
    },
    'sacco_mfi': {
        'keywords': ['sacco', 'microfinance', 'mfi', 'vicoba', 'savings', 'credit society',
                     'cooperative', 'saccos'],
        'experience': (
            "ZIMA Solutions specializes in technology solutions for SACCOs and microfinance institutions. "
            "Our SACCO Management System handles member management, savings products, loan origination and "
            "tracking, dividend calculation, mobile banking integration, and regulatory reporting to TCDC."
        ),
        'approach': (
            "We understand the unique requirements of cooperative financial institutions in Tanzania. "
            "Our solutions comply with TCDC regulations and support both urban and rural SACCO operations "
            "with offline-capable mobile interfaces."
        ),
    },
    'construction': {
        'keywords': ['construction', 'building', 'renovation', 'civil works', 'road',
                     'plumbing', 'electrical installation', 'painting', 'maintenance of building'],
        'experience': (
            "ZIMA Solutions collaborates with established construction firms through strategic partnerships "
            "to deliver building and infrastructure projects. We provide the technology management layer — "
            "project management systems, progress tracking, IoT monitoring, and reporting dashboards — "
            "while our construction partners handle physical execution."
        ),
        'approach': (
            "Our partnership model combines construction expertise with technology oversight: "
            "digital project planning, automated progress reporting, quality assurance tracking, "
            "and financial management systems to ensure on-time, on-budget delivery."
        ),
    },
    'air_conditioning': {
        'keywords': ['air condition', 'hvac', 'cooling system', 'air conditioning',
                     'refrigeration'],
        'experience': (
            "ZIMA Solutions, through strategic partnerships with certified HVAC contractors, provides "
            "air conditioning supply, installation, repair, and maintenance services. We bring technology-driven "
            "maintenance management — predictive maintenance scheduling, IoT-based monitoring of AC systems, "
            "and digital service tracking for enterprise-scale AC fleet management."
        ),
        'approach': (
            "Our approach combines skilled HVAC technicians (through our partners) with technology-driven "
            "maintenance management: digital asset tracking, preventive maintenance scheduling, service history "
            "logging, and performance monitoring dashboards."
        ),
    },
    'generator': {
        'keywords': ['generator', 'power generator', 'genset', 'standby power',
                     'power backup', 'inverter', 'ups system', 'battery backup'],
        'experience': (
            "ZIMA Solutions provides generator maintenance and power solutions through strategic "
            "partnerships with authorized service providers. We add value through IoT-based power "
            "monitoring, automated maintenance scheduling, fuel consumption tracking, and remote "
            "generator management systems."
        ),
        'approach': (
            "Our solution combines physical maintenance expertise (through certified partners) with "
            "digital monitoring and management: remote diagnostics, predictive maintenance alerts, "
            "fuel consumption analytics, and compliance reporting."
        ),
    },
    'insurance': {
        'keywords': ['insurance', 'underwriting', 'claims', 'premium', 'actuarial',
                     'group life', 'health insurance', 'motor insurance'],
        'experience': (
            "ZIMA Solutions provides technology solutions for the insurance industry including "
            "claims management systems, policy administration platforms, agent portals, and "
            "digital distribution channels. We also facilitate insurance procurement through "
            "our network of licensed insurance brokers."
        ),
        'approach': (
            "We bring insurance technology expertise combined with an understanding of TIRA "
            "regulatory requirements. For insurance procurement tenders, we partner with "
            "licensed insurance companies and brokers to deliver comprehensive coverage solutions."
        ),
    },
    'cleaning_security': {
        'keywords': ['cleaning', 'janitorial', 'security guard', 'security services',
                     'guard service', 'office cleaning', 'fumigation', 'pest control'],
        'experience': (
            "ZIMA Solutions partners with established facility management companies to deliver "
            "cleaning, security, and facility services. We enhance service delivery through "
            "technology: digital attendance tracking, quality inspection apps, incident reporting "
            "systems, and performance dashboards."
        ),
        'approach': (
            "Our technology-enhanced facility management approach includes: digital staff scheduling "
            "and tracking, mobile quality inspection tools, real-time incident reporting, and "
            "management dashboards with KPI monitoring and SLA compliance tracking."
        ),
    },
    'printing': {
        'keywords': ['printing', 'stationery', 'stationary', 'office supplies', 'branding material',
                     'publication', 'design and print', 'toner', 'cartridge', 'printed stationeries'],
        'experience': (
            "ZIMA Solutions partners with professional printing and branding firms to deliver "
            "high-quality printed materials, stationery, and branded merchandise. We bring "
            "digital design capability including graphic design, layout, and pre-press preparation."
        ),
        'approach': (
            "We combine in-house digital design and pre-press capability with printing production "
            "through our established print partners, ensuring quality control from design "
            "through final delivery."
        ),
    },
    'prequalification': {
        'keywords': ['prequalification', 'pre-qualification', 'registration of suppliers',
                     'registration of vendors', 'vendor registration', 'supplier registration',
                     'expression of interest'],
        'experience': (
            "ZIMA Solutions seeks registration across multiple categories: ICT Services, Software "
            "Development, System Integration, Technology Consultancy, Digital Services, IT Equipment "
            "Supply, and Technical Training. We have been successfully prequalified with multiple "
            "financial institutions and government agencies in Tanzania."
        ),
        'approach': (
            "We submit comprehensive documentation demonstrating our technical capability, "
            "legal standing, and operational readiness. Our company documents — Certificate of "
            "Incorporation, TIN, Business License, and MEMART — evidence our compliance with "
            "Tanzanian business regulations."
        ),
    },
}


def _escape_xml(text):
    """Escape special characters for reportlab XML/HTML paragraphs."""
    if not text:
        return ""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Remove non-printable characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text


PITCH_CACHE_DIR = f"{PROJECT}/applications/pitches"

def _get_company_profile_text():
    """Get the company profile text for AI prompts (dynamic, uses current COMPANY dict)."""
    return _build_company_profile_text()


def generate_pitch_with_claude(tender, tender_text):
    """Use Claude CLI to read all tender files and generate a professional application response."""
    tid = tender.get('tender_id', '')
    slug = tender.get('institution_slug', '')
    os.makedirs(PITCH_CACHE_DIR, exist_ok=True)

    # Check cache
    cache_file = os.path.join(PITCH_CACHE_DIR, f"{tid}_pitch.json")
    if os.path.isfile(cache_file):
        try:
            with open(cache_file) as f:
                cached = json.load(f)
            if cached.get('sections'):
                return cached['sections']
        except Exception:
            pass

    institution = tender.get('institution_name') or slug
    title = tender.get('title', '')
    ref = tender.get('reference_number', '')
    closing = tender.get('closing_date', '')
    source_url = tender.get('source_url', '')

    # Paths Claude should read
    inst_dir = f"{PROJECT}/institutions/{slug}"
    tender_json_patterns = [
        f"{inst_dir}/tenders/active/{tid}.json",
        f"{inst_dir}/tenders/active/{tid.lower()}.json",
    ]
    tender_json = next((p for p in tender_json_patterns if os.path.isfile(p)), '')

    # Find all downloaded files for this tender
    download_dirs = []
    tid_parts = tid.rsplit('-', 2)
    alt_ids = [tid]
    if len(tid_parts) == 3:
        prefix_parts = tid_parts[0].split('-')
        if len(prefix_parts) > 1:
            alt_ids.append(f"{prefix_parts[0]}-{tid_parts[1]}-{tid_parts[2]}")
    for alt_id in alt_ids:
        for d in [f"{inst_dir}/downloads/{alt_id}", f"{inst_dir}/downloads/{alt_id.lower()}"]:
            if os.path.isdir(d):
                download_dirs.append(d)

    # Build file list for Claude to read
    files_to_read = []
    if tender_json:
        files_to_read.append(tender_json)
    for dd in download_dirs:
        for root, _, fnames in os.walk(dd):
            for fn in sorted(fnames):
                fpath = os.path.join(root, fn)
                if fn.endswith(('.txt', '.json', '.pdf')):
                    files_to_read.append(fpath)

    file_list = "\n".join(f"  - {f}" for f in files_to_read) if files_to_read else "  No files found"

    # Collect company documents
    company_docs_dir = COMPANY.get('company_docs_dir', '')
    company_files = []
    if company_docs_dir and os.path.isdir(company_docs_dir):
        for root, _, fnames in os.walk(company_docs_dir):
            for fn in sorted(fnames):
                fpath = os.path.join(root, fn)
                if fn.endswith(('.pdf', '.txt', '.json', '.md', '.docx', '.doc')):
                    company_files.append(fpath)

    company_file_list = "\n".join(f"  - {f}" for f in company_files) if company_files else "  No company documents found"

    company_profile_text = _get_company_profile_text()
    company_name = COMPANY['company_name']

    prompt = f"""You are writing a professional tender application for {company_name}.

YOUR TASK:
1. Read ALL the tender files listed below to understand this tender completely
2. Read ALL the company documents to understand the applicant's credentials, certifications, and registration details
3. If a source URL is provided, fetch it for additional tender information
4. Write a thorough, professional "RESPONSE TO THIS TENDER" section that incorporates real company details from the documents

ABOUT THE APPLICANT COMPANY:
{company_profile_text}

COMPANY DOCUMENTS (read ALL — these contain certificates, licenses, registration details):
{company_file_list}

TENDER: {title}
INSTITUTION: {institution}
REFERENCE: {ref}
CLOSING DATE: {closing}
SOURCE URL: {source_url or 'Not available'}

TENDER FILES TO READ (read ALL of them):
{file_list}

INSTRUCTIONS:
- Read every file above using the Read tool — both company documents AND tender documents
- From the company documents, extract: registration numbers, certificate details, license validity, directors, share capital, and any other credentials
- Analyze all tender requirements, scope, eligibility criteria, evaluation criteria
- Write a detailed, specific response that shows deep understanding of this tender
- Reference specific company credentials from the actual documents (not just the profile summary)
- Reference specific items from the tender documents
- For tenders outside the company's core expertise, explain how the company would partner with specialists

Return a JSON object with these keys:
{{
  "understanding": "3-5 detailed paragraphs showing deep understanding of what this tender requires. Reference specific requirements from the documents.",
  "why_us": "3-4 paragraphs on why {company_name} is the right choice. Map capabilities to requirements.",
  "approach": ["Phase 1: ... (with deliverables and timeline)", "Phase 2: ...", "Phase 3: ...", "Phase 4: ...", "Phase 5: ..."],
  "value_proposition": "2-3 paragraphs on what makes {company_name}'s offer unique for this tender.",
  "compliance_notes": ["Requirement 1: How {company_name} meets it...", "Requirement 2: ..."],
  "technical_approach": "2-3 paragraphs on specific methodology, tools, technologies.",
  "risk_management": "1-2 paragraphs on key risks and mitigation strategies."
}}

Be professional, confident, specific. No generic phrases. Reference concrete items from the tender.
Return ONLY valid JSON, no markdown formatting."""

    try:
        cmd = ['claude', '-p', '--model', 'sonnet', '--no-session-persistence',
               '--output-format', 'json', '--dangerously-skip-permissions',
               '--max-turns', '10',
               '--allowedTools', 'Read,Glob,Grep,WebFetch,WebSearch',
               '--add-dir', inst_dir]
        if company_docs_dir and os.path.isdir(company_docs_dir):
            cmd.extend(['--add-dir', company_docs_dir])
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True, text=True, timeout=300,
        )

        if result.returncode != 0:
            print(f"           Claude CLI error: {result.stderr[:200]}")
            return None

        # Parse the output — claude with --output-format json wraps in a JSON envelope
        output = result.stdout.strip()
        try:
            envelope = json.loads(output)
            text_content = envelope.get('result', output)
        except json.JSONDecodeError:
            text_content = output

        # Extract JSON from the text content
        json_match = re.search(r'\{[\s\S]*\}', text_content)
        if json_match:
            sections = json.loads(json_match.group())
        else:
            print(f"           No JSON found in Claude response")
            return None

        # Validate required keys (accept both why_us and legacy why_zima)
        if 'why_zima' in sections and 'why_us' not in sections:
            sections['why_us'] = sections.pop('why_zima')
        required_keys = ['understanding', 'why_us', 'approach', 'value_proposition']
        if not all(k in sections for k in required_keys):
            print(f"           Missing keys: {[k for k in required_keys if k not in sections]}")
            return None

        # Cache the result
        with open(cache_file, 'w') as f:
            json.dump({'tender_id': tid, 'sections': sections, 'generated_at': datetime.now().isoformat()}, f, indent=2)

        return sections

    except subprocess.TimeoutExpired:
        print(f"           Claude CLI timeout (300s)")
        return None
    except Exception as e:
        print(f"           Claude CLI error: {e}")
        return None


def get_matching_domains(text, title):
    """Find which domain response categories match this tender.
    Title matches are weighted 5x higher than document text matches."""
    title_lower = title.lower()
    # Use first 5000 chars of text to avoid generic matches from very long docs
    text_sample = text[:5000].lower() if text else ''
    matches = []
    for domain_key, domain in DOMAIN_RESPONSES.items():
        title_score = sum(5 for kw in domain['keywords'] if kw in title_lower)
        text_score = sum(1 for kw in domain['keywords'] if kw in text_sample)
        total = title_score + text_score
        if total > 0:
            matches.append((domain_key, total))
    matches.sort(key=lambda x: -x[1])
    return [m[0] for m in matches[:3]]  # top 3 matching domains


def infer_requirements_from_title(tender):
    """For tenders without extracted documents, infer requirements from title and metadata."""
    title = (tender.get('title', '') or '').lower()
    desc = (tender.get('description', '') or '').lower()
    scope = (tender.get('scope_of_work', '') or '').lower()
    combined = f"{title} {desc} {scope}"

    reqs = {
        'scope_of_work': '',
        'eligibility': [],
        'required_documents': [],
        'evaluation_criteria': [],
        'deliverables': [],
        'timeline': '',
        'special_requirements': [],
        'technical_specs': '',
        'tender_type': 'services',
        'submission_method': '',
        'lot_details': [],
    }

    # Infer tender type
    if any(w in combined for w in ['construction', 'building', 'renovation', 'civil', 'road']):
        reqs['tender_type'] = 'works'
    elif any(w in combined for w in ['supply', 'procurement', 'delivery of', 'provision of goods']):
        reqs['tender_type'] = 'goods'
    elif any(w in combined for w in ['consultancy', 'consultant', 'advisory']):
        reqs['tender_type'] = 'consultancy'
    elif any(w in combined for w in ['prequalification', 'registration', 'expression of interest']):
        reqs['tender_type'] = 'prequalification'

    # Use the scope_of_work from the database if available
    if scope and len(scope) > 20:
        reqs['scope_of_work'] = tender.get('scope_of_work', '')

    # Standard Tanzanian tender requirements
    reqs['required_documents'] = [
        'Certificate of Incorporation/Registration',
        'Tax Identification Number (TIN)',
        'Valid Business License',
        'Company Profile',
    ]

    if tender.get('eligibility') and len(str(tender['eligibility'])) > 10:
        reqs['eligibility'] = [str(tender['eligibility'])]

    return reqs


# ═══════════════════════════════════════════════════════════════════════════════
# PDF GENERATION — CUSTOM PER TENDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_cover_letter(story, styles, tender, reqs):
    """Page 1: Cover letter customized for this specific tender."""
    date_str = datetime.now().strftime('%d %B %Y')
    institution = tender.get('institution_name') or tender.get('institution_slug', '')
    title = tender.get('title', 'Tender Application')
    ref = tender.get('reference_number', '')
    closing = tender.get('closing_date', '')
    tender_type = reqs.get('tender_type', 'services')

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(_escape_xml(COMPANY['company_name']), styles['ZimaTitle']))
    subtitle_parts = [COMPANY.get('tagline', '')]
    if COMPANY.get('address'):
        subtitle_parts.append(_escape_xml(COMPANY['address']))
    contact_bits = []
    if COMPANY.get('phone'):
        contact_bits.append(f"Phone: {COMPANY['phone']}")
    if COMPANY.get('contact_email'):
        contact_bits.append(f"Email: {COMPANY['contact_email']}")
    if COMPANY.get('website'):
        contact_bits.append(f"Web: {COMPANY['website']}")
    if contact_bits:
        subtitle_parts.append(" &bull; ".join(contact_bits))
    story.append(Paragraph("<br/>".join(subtitle_parts), styles['ZimaSubtitle']))

    story.append(HRFlowable(width="100%", thickness=1, color=BLUE))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(date_str, styles['Body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(f"The Procurement Manager / Tender Committee<br/>"
                           f"<b>{_escape_xml(institution)}</b>", styles['Body']))
    story.append(Spacer(1, 3*mm))

    re_line = f"<b>RE: {_escape_xml(title)}</b>"
    if ref:
        re_line += f"<br/><i>Reference: {_escape_xml(ref)}</i>"
    if closing:
        re_line += f"<br/><i>Closing Date: {_escape_xml(closing)}</i>"
    story.append(Paragraph(re_line, styles['BodyBold']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Dear Sir/Madam,", styles['Body']))

    # Customize opening paragraph based on tender type
    cn = _escape_xml(COMPANY['company_name'])
    tin_part = f" (TIN: {COMPANY['tin']})" if COMPANY.get('tin') else ""

    if tender_type == 'prequalification':
        opening = (
            f"We are pleased to submit our application for registration/prequalification "
            f"as referenced above. {cn}{tin_part} wishes to be considered "
            f"as a qualified supplier for <b>{_escape_xml(institution)}</b>."
        )
    elif tender_type == 'consultancy':
        opening = (
            f"We are pleased to submit our expression of interest and technical proposal for "
            f"the above-referenced consultancy assignment. {cn} brings deep "
            f"domain expertise and professional capability to deliver this engagement."
        )
    elif tender_type == 'works':
        opening = (
            f"We are pleased to submit our tender for the above-referenced works. "
            f"{cn} brings comprehensive project delivery capability "
            f"combined with technology-driven project management and quality assurance."
        )
    elif tender_type == 'goods':
        opening = (
            f"We are pleased to submit our tender for the supply of goods as referenced above. "
            f"{cn} maintains strategic partnerships with leading manufacturers "
            f"and authorized distributors."
        )
    else:
        opening = (
            f"We are pleased to submit our application for the above-referenced tender. "
            f"{cn}{tin_part} is well positioned to deliver on the stated requirements."
        )

    story.append(Paragraph(opening, styles['Body']))

    # Specific understanding paragraph
    scope = reqs.get('scope_of_work', '') or tender.get('scope_of_work', '') or tender.get('description', '') or ''
    if scope and len(scope) > 30:
        scope_clean = _escape_xml(scope[:500])
        story.append(Paragraph(
            f"We have carefully reviewed the tender requirements and understand that "
            f"{_escape_xml(institution)} is seeking: <i>{scope_clean}</i>",
            styles['Body']))
    else:
        story.append(Paragraph(
            f"We have carefully reviewed the requirements and are confident in our ability to "
            f"deliver value to <b>{_escape_xml(institution)}</b>. The details of our capabilities, "
            f"relevant experience, and proposed approach are presented in the following pages.",
            styles['Body']))

    story.append(Paragraph(
        "We remain available for any clarifications, presentations, or additional "
        "documentation you may require and look forward to your favorable consideration.",
        styles['Body']))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Yours faithfully,", styles['Body']))
    story.append(Spacer(1, 8*mm))
    signoff_name = _escape_xml(COMPANY.get('contact_person', 'Director'))
    signoff_title = _escape_xml(COMPANY.get('contact_title', ''))
    signoff_company = _escape_xml(COMPANY['company_name'])
    signoff_contact = " | ".join(filter(None, [COMPANY.get('contact_email'), COMPANY.get('phone')]))
    signoff_line = f"<b>{signoff_name}</b>"
    if signoff_title:
        signoff_line += f"<br/>{signoff_title}, {signoff_company}"
    else:
        signoff_line += f"<br/>{signoff_company}"
    if signoff_contact:
        signoff_line += f"<br/>{_escape_xml(signoff_contact)}"
    story.append(Paragraph(signoff_line, styles['Body']))


def build_company_profile(story, styles):
    """Page 2: Company profile (same for all but placed after cover letter)."""
    story.append(Paragraph("1. COMPANY PROFILE", styles['SectionHead']))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE))
    story.append(Spacer(1, 3*mm))

    company_data = []
    field_map = [
        ('Company Name', 'company_name'),
        ('Registration', 'registration'),
        ('Date of Incorporation', 'incorporation_date'),
        ('TIN', 'tin'),
        ('Business License', 'business_license'),
        ('Directors', 'directors'),
        ('Head Office', 'address'),
        ('Phone', 'phone'),
        ('Email', 'contact_email'),
        ('Website', 'website'),
        ('Share Capital', 'share_capital'),
    ]
    for label, key in field_map:
        val = COMPANY.get(key)
        if val:
            company_data.append([label, val])

    t = Table(company_data, colWidths=[45*mm, 115*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor("#E0E0E0")),
        ('LINEBELOW', (0, -1), (-1, -1), 1, BLUE),
    ]))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("1.1 About ZIMA Solutions", styles['SubSection']))
    story.append(Paragraph(
        "ZIMA Solutions Limited is a technology and business innovation company specializing "
        "in digital transformation for financial institutions, government agencies, and "
        "enterprises in Tanzania and East Africa. We design and implement secure, scalable "
        "systems that drive operational efficiency, regulatory compliance, and digital inclusion.",
        styles['Body']))

    story.append(Paragraph("1.2 Key Metrics", styles['SubSection']))
    metrics = [
        ['Enterprise Projects Delivered', '20+'],
        ['Client Organizations Served', '50+'],
        ['Bank of Tanzania Integrations', '4 (RTGS, TIPS, GePG, NIDA)'],
        ['System Uptime Guarantee', '99.9%'],
    ]
    mt = Table(metrics, colWidths=[60*mm, 100*mm])
    mt.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#BBDEFB")),
    ]))
    story.append(mt)


def build_relevant_services(story, styles, tender, matching_domains):
    """Page 3: Services section — only show services RELEVANT to this tender."""
    story.append(Paragraph("2. RELEVANT SERVICES &amp; CAPABILITIES", styles['SectionHead']))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE))
    story.append(Spacer(1, 3*mm))

    title = (tender.get('title', '') or '').lower()

    # Show domain-specific experience first
    if matching_domains:
        story.append(Paragraph("2.1 Directly Relevant Experience", styles['SubSection']))
        for domain_key in matching_domains[:2]:
            domain = DOMAIN_RESPONSES[domain_key]
            story.append(Paragraph(_escape_xml(domain['experience']), styles['Body']))

    # Then show full service list but organized by relevance
    story.append(Paragraph("2.2 Full Service Portfolio", styles['SubSection']))

    services = [
        "<b>Bank of Tanzania Integrations</b> \u2014 RTGS, TIPS, GePG, NIDA",
        "<b>Core Banking Solutions</b> \u2014 Implementation and integration for banks, SACCOs, MFIs",
        "<b>AI &amp; Machine Learning</b> \u2014 Conversational AI, fraud detection, credit scoring, analytics",
        "<b>Digital Banking Platforms</b> \u2014 Mobile banking, internet banking, USSD, agency banking",
        "<b>Payment Solutions</b> \u2014 TanQR, mobile money, payment gateways, reconciliation",
        "<b>API Gateway &amp; Middleware</b> \u2014 Enterprise integration platform",
        "<b>Enterprise Software</b> \u2014 ERP, HR, Loan, School, Healthcare management systems",
        "<b>Cybersecurity</b> \u2014 Vulnerability assessments, pen testing, compliance audits",
        "<b>ICT Infrastructure</b> \u2014 Supply, installation, and maintenance of IT equipment",
        "<b>Technology Consultancy</b> \u2014 Digital strategy, feasibility studies, system architecture",
    ]
    for svc in services:
        story.append(Paragraph(svc, styles['ZimaBullet'], bulletText='\u2022'))


def build_custom_tender_response(story, styles, tender, reqs, matching_domains, pitch_sections):
    """Page 4+: The CUSTOM section — written by Claude CLI for each tender."""
    institution = tender.get('institution_name') or tender.get('institution_slug', '')
    title = tender.get('title', 'Tender Application')
    ref = tender.get('reference_number', '')
    tender_type = reqs.get('tender_type', 'services')

    story.append(Paragraph("3. RESPONSE TO THIS TENDER", styles['SectionHead']))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(f"<b>Tender:</b> {_escape_xml(title)}", styles['Body']))
    if ref:
        story.append(Paragraph(f"<b>Reference:</b> {_escape_xml(ref)}", styles['Body']))
    story.append(Paragraph(f"<b>Institution:</b> {_escape_xml(institution)}", styles['Body']))
    if tender_type:
        type_labels = {
            'works': 'Works/Construction',
            'goods': 'Supply of Goods',
            'services': 'Services',
            'consultancy': 'Consultancy Services',
            'prequalification': 'Prequalification/Vendor Registration',
        }
        story.append(Paragraph(f"<b>Tender Type:</b> {type_labels.get(tender_type, tender_type)}", styles['Body']))
    story.append(Spacer(1, 3*mm))

    if pitch_sections:
        # ── 3.1 Understanding (Claude-generated) ──
        story.append(Paragraph("3.1 Our Understanding of the Requirements", styles['SubSection']))
        understanding = pitch_sections.get('understanding', '')
        if understanding:
            for para in understanding.split('\n\n'):
                para = para.strip()
                if para:
                    story.append(Paragraph(_escape_xml(para), styles['Body']))

        # ── 3.2 Why Us (Claude-generated) ──
        story.append(Paragraph(f"3.2 Why {_escape_xml(COMPANY['company_name'])}", styles['SubSection']))
        why_zima = pitch_sections.get('why_us', '') or pitch_sections.get('why_zima', '')
        if why_zima:
            for para in why_zima.split('\n\n'):
                para = para.strip()
                if para:
                    story.append(Paragraph(_escape_xml(para), styles['Body']))

        # ── 3.3 Proposed Approach (Claude-generated) ──
        story.append(Paragraph("3.3 Proposed Approach", styles['SubSection']))
        approach_steps = pitch_sections.get('approach', [])
        if isinstance(approach_steps, list):
            for step in approach_steps:
                story.append(Paragraph(_escape_xml(str(step)), styles['ZimaBullet'], bulletText='\u2022'))
        elif isinstance(approach_steps, str):
            story.append(Paragraph(_escape_xml(approach_steps), styles['Body']))

        # ── 3.4 Value Proposition (Claude-generated) ──
        value_prop = pitch_sections.get('value_proposition', '')
        if value_prop:
            story.append(Paragraph("3.4 Our Value Proposition", styles['SubSection']))
            story.append(Paragraph(_escape_xml(value_prop), styles['Body']))

        # ── 3.5 Technical Approach (Claude-generated) ──
        tech_approach = pitch_sections.get('technical_approach', '')
        if tech_approach:
            story.append(Paragraph("3.5 Technical Approach &amp; Methodology", styles['SubSection']))
            for para in tech_approach.split('\n\n'):
                para = para.strip()
                if para:
                    story.append(Paragraph(_escape_xml(para), styles['Body']))

        # ── 3.6 Risk Management (Claude-generated) ──
        risk_mgmt = pitch_sections.get('risk_management', '')
        if risk_mgmt:
            story.append(Paragraph("3.6 Risk Management", styles['SubSection']))
            for para in risk_mgmt.split('\n\n'):
                para = para.strip()
                if para:
                    story.append(Paragraph(_escape_xml(para), styles['Body']))

        # ── 3.7 Compliance (Claude-generated) ──
        compliance = pitch_sections.get('compliance_notes', [])
        if compliance:
            story.append(Paragraph("3.7 Eligibility &amp; Compliance", styles['SubSection']))
            if isinstance(compliance, list):
                for note in compliance:
                    story.append(Paragraph(f"\u2713 {_escape_xml(str(note))}", styles['ZimaBullet'], bulletText='\u2022'))
            elif isinstance(compliance, str):
                story.append(Paragraph(_escape_xml(compliance), styles['Body']))

    else:
        # Fallback if Claude CLI failed — use basic approach
        story.append(Paragraph("3.1 Our Understanding", styles['SubSection']))
        scope = reqs.get('scope_of_work', '') or tender.get('scope_of_work', '') or ''
        if scope and len(scope) > 30:
            story.append(Paragraph(
                f"We understand that <b>{_escape_xml(institution)}</b> requires: "
                f"{_escape_xml(scope[:800])}", styles['Body']))
        else:
            story.append(Paragraph(
                f"We understand that <b>{_escape_xml(institution)}</b> is seeking a qualified "
                f"provider for <b>{_escape_xml(title)}</b>.", styles['Body']))

        story.append(Paragraph("3.2 Why ZIMA Solutions", styles['SubSection']))
        if matching_domains:
            domain = DOMAIN_RESPONSES[matching_domains[0]]
            story.append(Paragraph(_escape_xml(domain['experience']), styles['Body']))
        else:
            story.append(Paragraph(
                "ZIMA Solutions brings technology and business innovation capability serving "
                "50+ organizations across Tanzania, with strategic partnerships extending our "
                "delivery capability across specialized domains.", styles['Body']))


def build_financials_and_docs(story, styles):
    """Financial standing and attached documents section."""
    story.append(Paragraph("4. FINANCIAL STANDING &amp; DOCUMENTS", styles['SectionHead']))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "ZIMA Solutions Limited was incorporated in January 2025 under the Companies Act, 2002. "
        "As our company recently completed its inaugural financial year (January 2025 \u2013 January 2026), "
        "our first set of audited financial statements is currently under preparation by our "
        "external auditors and <b>will be available by 1 May 2026</b>.",
        styles['Body']))

    story.append(Paragraph(
        "In the interim, we are pleased to provide the following documents as evidence of "
        "our legal, tax, and operational standing:", styles['Body']))

    docs_list = [
        "<b>Certificate of Incorporation</b> \u2014 Issued under the Companies Act, 2002 (Registration No. 181314605)",
        "<b>Tax Identification Number (TIN)</b> \u2014 TIN: 181-314-605, issued by Tanzania Revenue Authority",
        "<b>Business License</b> \u2014 ICT Services (Local), issued by Kinondoni Municipal Council",
    ]
    for d in docs_list:
        story.append(Paragraph(d, styles['ZimaBullet'], bulletText='\u2022'))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<i>These documents are appended to this application (see attached pages).</i>",
        styles['Small']))


def build_contact_section(story, styles):
    """Contact information section."""
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("5. CONTACT INFORMATION", styles['SectionHead']))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BLUE))
    story.append(Spacer(1, 3*mm))

    contact_data = [
        ['Company', 'ZIMA Solutions Limited'],
        ['Director', 'Andrew Stanslaus Mashamba'],
        ['Phone', '+255 69 241 0353'],
        ['Email', 'info@zima.co.tz'],
        ['Address', 'Makongo, Near Ardhi University, Kinondoni, Dar es Salaam, Tanzania'],
        ['Website', 'zima.co.tz'],
        ['TIN', '181-314-605'],
    ]
    ct = Table(contact_data, colWidths=[35*mm, 125*mm])
    ct.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor("#E0E0E0")),
    ]))
    story.append(ct)


def build_application_pdf(tender, output_path):
    """Build a complete, CUSTOM tender application PDF."""
    styles = get_styles()
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=22*mm, bottomMargin=20*mm,
                            leftMargin=20*mm, rightMargin=20*mm)

    # Step 1: Read the actual tender documents
    tender_text = read_tender_content(tender)

    # Step 2: Analyze requirements from the tender text
    if tender_text and len(tender_text) > 200:
        reqs = analyze_tender_requirements(tender_text, tender)
    else:
        reqs = infer_requirements_from_title(tender)

    # Step 3: Determine matching domains
    title = tender.get('title', '') or ''
    matching_domains = get_matching_domains(tender_text + ' ' + title, title)

    # Step 4: Generate custom pitch using Claude CLI
    print(f"           Generating pitch with Claude...", end='', flush=True)
    pitch_sections = generate_pitch_with_claude(tender, tender_text)
    if pitch_sections:
        print(f" done")
    else:
        print(f" fallback (template)")

    # Step 5: Build the PDF story
    story = []

    # Cover letter (page 1)
    build_cover_letter(story, styles, tender, reqs)
    story.append(PageBreak())

    # Company profile (page 2)
    build_company_profile(story, styles)
    story.append(PageBreak())

    # Relevant services — customized to show relevant capabilities first (page 3)
    build_relevant_services(story, styles, tender, matching_domains)
    story.append(PageBreak())

    # Custom tender response — AI-generated, specific to this tender (pages 4+)
    build_custom_tender_response(story, styles, tender, reqs, matching_domains, pitch_sections)
    story.append(PageBreak())

    # Financial standing & documents (final page before company docs)
    build_financials_and_docs(story, styles)
    build_contact_section(story, styles)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL & SENDING
# ═══════════════════════════════════════════════════════════════════════════════

def merge_with_company_docs(app_pdf, output_pdf):
    """Merge application PDF with company documents PDF."""
    company_docs = COMPANY.get('company_docs_pdf', COMPANY_DOCS_PDF)
    merger = PdfMerger()
    merger.append(app_pdf)
    if os.path.isfile(company_docs):
        merger.append(company_docs)
    merger.write(output_pdf)
    merger.close()


def send_application_email(config, to_emails, tender, pdf_path):
    """Send a short email with the application PDF attached."""
    institution = tender.get('institution_name') or tender.get('institution_slug', '')
    title = tender.get('title', 'Tender Application')
    ref = tender.get('reference_number', '')

    cn = COMPANY['company_name']
    if ref:
        subject = f"Tender Application: {ref} \u2014 {title[:60]} | {cn}"
    else:
        subject = f"Tender Application: {title[:70]} | {cn}"

    body_html = f"""
    <html><body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
    <p>Dear Sir/Madam,</p>

    <p>Please find attached our application for <b>{_escape_xml(title)}</b>.</p>

    <p>The attached document contains our cover letter, company profile, relevant experience
    and capabilities, proposed approach, and supporting company registration documents
    (Certificate of Incorporation, TIN, Business License, and Memorandum &amp; Articles of Association).</p>

    <p>We are available for any clarifications or additional information you may require.</p>

    <p>
    Kind regards,<br/><br/>
    <b>Andrew Stanslaus Mashamba</b><br/>
    Director, ZIMA Solutions Limited<br/>
    Phone: +255 69 241 0353<br/>
    Email: info@zima.co.tz<br/>
    Web: <a href="https://zima.co.tz">zima.co.tz</a>
    </p>
    </body></html>
    """

    msg = MIMEMultipart()
    msg['From'] = "ZIMA Solutions Limited <info@zima.co.tz>"
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg['Bcc'] = BCC
    msg.attach(MIMEText(body_html, 'html'))

    pdf_filename = f"ZIMA_Application_{tender.get('tender_id', 'tender')}.pdf"
    with open(pdf_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=pdf_filename)
    part['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    msg.attach(part)

    all_recip = list(to_emails) + [BCC]
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port'], context=ctx, timeout=30) as server:
        server.login(config['smtp_user'], config['smtp_password'])
        server.sendmail(config['from'], all_recip, msg.as_string())


def log_sent(tid, to, subject, status, error=None):
    log = []
    if os.path.isfile(SENT_LOG):
        with open(SENT_LOG) as f:
            log = json.load(f)
    log.append({
        'tender_id': tid, 'to': to, 'subject': subject,
        'status': status, 'error': error,
        'sent_at': datetime.now().isoformat()
    })
    with open(SENT_LOG, 'w') as f:
        json.dump(log, f, indent=2)


def process_tender(tender, config, db):
    """Generate PDF and send for one tender."""
    tid = tender['tender_id']
    contact = tender.get('contact', {})
    emails = []
    if isinstance(contact, dict):
        emails = contact.get('emails', [])
    emails = list(set(e for e in emails if '@' in str(e)))

    if not emails:
        return 'skip', 'No email'

    if tender.get('application_status') == 'Submitted':
        return 'skip', 'Already submitted'

    app_dir = f"{PROJECT}/applications/pdfs"
    os.makedirs(app_dir, exist_ok=True)

    app_pdf = os.path.join(app_dir, f"{tid}_application.pdf")
    final_pdf = os.path.join(app_dir, f"ZIMA_Application_{tid}.pdf")

    try:
        build_application_pdf(tender, app_pdf)
        merge_with_company_docs(app_pdf, final_pdf)
        send_application_email(config, emails, tender, final_pdf)
        # Update status
        for r in db:
            if r['tender_id'] == tid and r.get('institution_slug') == tender.get('institution_slug'):
                r['application_status'] = 'Submitted'
                r['notes'] = f"Sent {datetime.now().strftime('%Y-%m-%d %H:%M')} to {', '.join(emails)}"
        with open(DB_FILE, 'w') as f:
            json.dump(db, f, indent=2, default=str)
        log_sent(tid, emails, f"Tender: {tender.get('title','')[:60]}", "sent")
        if os.path.exists(app_pdf):
            os.remove(app_pdf)
        return 'sent', f"\u2192 {', '.join(emails)}"
    except Exception as e:
        log_sent(tid, emails, f"Tender: {tender.get('title','')[:60]}", "failed", str(e))
        return 'fail', str(e)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--batch', type=int, default=25)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--tender-id', type=str)
    parser.add_argument('--pdf-only', action='store_true', help='Generate PDF only, do not send')
    parser.add_argument('--company-profile', type=str, help='Path to JSON file with company profile')
    parser.add_argument('--output-dir', type=str, help='Directory for output PDFs and pitch cache')
    args = parser.parse_args()

    # Load company profile if provided
    if args.company_profile and os.path.isfile(args.company_profile):
        _load_company_profile(args.company_profile)

    config = json.load(open(CONFIG_FILE))
    db = json.load(open(DB_FILE))

    if args.tender_id:
        tender = next((r for r in db if r['tender_id'] == args.tender_id), None)
        if not tender:
            print(f"Tender {args.tender_id} not found")
            return

        if args.pdf_only:
            app_dir = args.output_dir or f"{PROJECT}/applications/pdfs"
            os.makedirs(app_dir, exist_ok=True)
            # Redirect pitch cache to output dir so each user gets their own
            if args.output_dir:
                global PITCH_CACHE_DIR
                PITCH_CACHE_DIR = os.path.join(args.output_dir, "pitches")
            # Use company name in filename (sanitized)
            company_slug = re.sub(r'[^a-zA-Z0-9]', '_', COMPANY['company_name']).strip('_')
            app_pdf = os.path.join(app_dir, f"{args.tender_id}_application.pdf")
            final_pdf = os.path.join(app_dir, f"{company_slug}_Application_{args.tender_id}.pdf")
            build_application_pdf(tender, app_pdf)
            merge_with_company_docs(app_pdf, final_pdf)
            if os.path.exists(app_pdf):
                os.remove(app_pdf)
            print(f"  PDF generated: {final_pdf}")
            return

        status, msg = process_tender(tender, config, db)
        print(f"  {status.upper()}: {args.tender_id} {msg}")
        return

    # Get pending tenders with emails
    pending = []
    for r in db:
        if r.get('application_status') in ('Submitted',):
            continue
        if r.get('urgency') == 'EXPIRED':
            continue
        contact = r.get('contact', {})
        emails = contact.get('emails', []) if isinstance(contact, dict) else []
        if emails:
            pending.append(r)

    # Sort by urgency
    uo = {'CRITICAL':0,'URGENT':1,'HIGH':2,'MEDIUM':3,'LOW':4,'UNKNOWN':5}
    pending.sort(key=lambda r: (uo.get(r['urgency'], 5), r['closing_date'] or 'z'))

    batch = pending[args.start:args.start + args.batch]
    print(f"\nBatch: {len(batch)} tenders (of {len(pending)} pending with emails)")
    print("=" * 60)

    sent = skip = fail = 0
    for i, tender in enumerate(batch):
        tid = tender['tender_id']
        title = tender['title'][:50]
        print(f"  [{i+1}/{len(batch)}] {tid}: {title}")

        if args.dry_run:
            # In dry run, still generate the PDF to verify it works
            tender_text = read_tender_content(tender)
            has_docs = "with docs" if len(tender_text) > 200 else "title-only"
            domains = get_matching_domains(tender_text + ' ' + title, title)
            emails = tender.get('contact', {}).get('emails', [])
            print(f"           DRY RUN [{has_docs}] domains={domains[:2]} \u2192 {', '.join(emails)}")
            continue

        if args.pdf_only:
            app_dir = f"{PROJECT}/applications/pdfs"
            os.makedirs(app_dir, exist_ok=True)
            app_pdf = os.path.join(app_dir, f"{tid}_application.pdf")
            final_pdf = os.path.join(app_dir, f"ZIMA_Application_{tid}.pdf")
            try:
                build_application_pdf(tender, app_pdf)
                merge_with_company_docs(app_pdf, final_pdf)
                if os.path.exists(app_pdf):
                    os.remove(app_pdf)
                print(f"           \u2713 PDF: {final_pdf}")
                sent += 1
            except Exception as e:
                print(f"           \u2717 FAIL: {e}")
                fail += 1
            continue

        status, msg = process_tender(tender, config, db)
        if status == 'sent':
            sent += 1
            print(f"           \u2713 SENT {msg}")
            time.sleep(120)  # Rate limit: 30 emails/hour (safe margin under 50/hr cap)
        elif status == 'skip':
            skip += 1
            print(f"           \u2014 {msg}")
        else:
            fail += 1
            print(f"           \u2717 FAIL: {msg}")

    print(f"\n{'=' * 60}")
    print(f"Done: {sent} sent, {skip} skipped, {fail} failed")


if __name__ == '__main__':
    main()
