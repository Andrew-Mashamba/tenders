#!/usr/bin/env python3
"""
Tender Application Email Sender
Sends customized cover letters with Zima company documents to tender contacts.
Updates the requirements database tracker after each send.
"""

import smtplib
import ssl
import json
import os
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from datetime import datetime

PROJECT = "/Volumes/DATA/PROJECTS/TENDERS"
CONFIG_FILE = f"{PROJECT}/config/email.json"
DB_FILE = f"{PROJECT}/applications/requirements_database.json"
COMPANY_DOCS = f"{PROJECT}/applications/ZIMA_Company_Documents.pdf"
SENT_LOG = f"{PROJECT}/applications/sent_log.json"
BCC_EMAIL = "andrew.s.mashamba@gmail.com"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_db():
    with open(DB_FILE) as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=2, default=str)

def log_sent(tender_id, to_email, subject, status, error=None):
    log = []
    if os.path.isfile(SENT_LOG):
        with open(SENT_LOG) as f:
            log = json.load(f)
    log.append({
        'tender_id': tender_id,
        'to': to_email,
        'subject': subject,
        'status': status,
        'error': error,
        'sent_at': datetime.now().isoformat(),
    })
    with open(SENT_LOG, 'w') as f:
        json.dump(log, f, indent=2)

def send_email(config, to_emails, subject, body_html, attachments=None, bcc=None):
    """Send email with attachments via SMTP SSL."""
    msg = MIMEMultipart()
    msg['From'] = f"ZIMA Solutions Limited <{config['from']}>"
    msg['To'] = ", ".join(to_emails) if isinstance(to_emails, list) else to_emails
    msg['Subject'] = subject
    if bcc:
        msg['Bcc'] = bcc

    msg.attach(MIMEText(body_html, 'html'))

    if attachments:
        for filepath in attachments:
            if not os.path.isfile(filepath):
                continue
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                part = MIMEApplication(f.read(), Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

    all_recipients = list(to_emails) if isinstance(to_emails, list) else [to_emails]
    if bcc:
        all_recipients.append(bcc)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port'], context=ctx, timeout=30) as server:
        server.login(config['smtp_user'], config['smtp_password'])
        server.sendmail(config['from'], all_recipients, msg.as_string())

    return True

def generate_cover_letter_html(tender, company_info):
    """Generate a professional HTML cover letter customized for the tender."""

    institution = tender.get('institution_name') or tender.get('institution_slug', 'Sir/Madam')
    title = tender.get('title', 'Tender Application')
    ref = tender.get('reference_number', '')
    closing = tender.get('closing_date', '')
    scope = tender.get('scope_of_work', '') or tender.get('description', '')

    # Determine what Zima capabilities are relevant
    capabilities = tender.get('zima_capability_match', ['General'])

    # Build capability-specific paragraphs
    capability_paragraphs = ""

    if 'ICT/Tech' in capabilities:
        capability_paragraphs += """
        <p>ZIMA Solutions has delivered <strong>20+ enterprise-grade technology projects</strong> across Tanzania,
        including core banking integrations, payment gateway implementations (RTGS, TIPS, GePG, TanQR),
        and AI-powered customer engagement platforms. We hold <strong>4 active Bank of Tanzania system integrations</strong>
        with a proven track record of 99.9% system uptime.</p>
        """

    if 'Consultancy' in capabilities:
        capability_paragraphs += """
        <p>Our consultancy practice brings deep domain expertise in financial services technology,
        digital transformation strategy, and regulatory compliance. We have supported <strong>50+ client organizations</strong>
        in designing and implementing systems that meet Bank of Tanzania and government standards.</p>
        """

    if 'Prequalification' in capabilities:
        capability_paragraphs += """
        <p>ZIMA Solutions seeks to register as a qualified supplier for your organization.
        We specialize in ICT solutions, digital services, software development, system integration,
        and technology consultancy. Our attached company documents demonstrate our legal standing,
        tax compliance, and technical capability.</p>
        """

    if 'Supply/Procurement' in capabilities:
        capability_paragraphs += """
        <p>ZIMA Solutions maintains strategic partnerships with leading technology vendors and
        equipment manufacturers, enabling us to supply, deliver, install, and maintain a wide range
        of ICT equipment and solutions. We combine supply capability with in-house technical expertise
        for end-to-end service delivery.</p>
        """

    if not capability_paragraphs or 'General' in capabilities:
        capability_paragraphs += """
        <p>ZIMA Solutions Limited is a registered ICT and business innovation company serving
        <strong>50+ organizations</strong> across Tanzania. Our portfolio spans digital transformation,
        system integration, AI solutions, payment platforms, and enterprise management systems.
        We bring both technical depth and strategic partnerships to deliver comprehensive solutions.</p>
        """

    # Financial statement note
    financials_note = """
    <p><em>As ZIMA Solutions Limited was incorporated in January 2025, our first audited financial statements
    will be available by 1 May 2026 following the completion of our inaugural financial year.
    We are pleased to provide our Certificate of Incorporation, Tax Identification Number (TIN),
    Business License, and Memorandum &amp; Articles of Association as evidence of our legal and
    operational standing.</em></p>
    """

    ref_line = f"<strong>Reference:</strong> {ref}<br>" if ref else ""
    closing_line = f"<strong>Closing Date:</strong> {closing}<br>" if closing else ""

    html = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #222; line-height: 1.6; max-width: 700px; margin: 0 auto;">

    <div style="border-bottom: 3px solid #1565C0; padding-bottom: 10px; margin-bottom: 20px;">
        <h2 style="color: #1565C0; margin-bottom: 5px;">ZIMA Solutions Limited</h2>
        <p style="color: #666; margin: 0; font-size: 13px;">
            Digital Transformation &bull; Financial Technology &bull; System Integration<br>
            Makongo, Kinondoni, Dar es Salaam &bull; +255 69 241 0353 &bull; info@zima.co.tz
        </p>
    </div>

    <p>{datetime.now().strftime('%d %B %Y')}</p>

    <p>
        The Procurement Manager / Tender Committee<br>
        <strong>{institution}</strong>
    </p>

    <p><strong>RE: {title}</strong></p>
    <p style="font-size: 13px; color: #555;">
        {ref_line}
        {closing_line}
    </p>

    <p>Dear Sir/Madam,</p>

    <p>We write to express our interest in the above-referenced tender and to submit our application
    for consideration. ZIMA Solutions Limited is a Tanzanian-registered ICT services and business
    innovation company (TIN: 181-314-605), specializing in digital transformation for financial
    institutions, government agencies, and enterprises.</p>

    {capability_paragraphs}

    <h3 style="color: #1565C0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Our Core Offerings</h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <tr>
            <td style="padding: 6px; border-bottom: 1px solid #eee; width: 50%; vertical-align: top;">
                &#8226; Core Banking System Integration<br>
                &#8226; RTGS, TIPS, GePG, TanQR Gateways<br>
                &#8226; NIDA Identity Verification<br>
                &#8226; API Gateway &amp; Middleware
            </td>
            <td style="padding: 6px; border-bottom: 1px solid #eee; width: 50%; vertical-align: top;">
                &#8226; AI Agents &amp; Machine Learning<br>
                &#8226; SACCO &amp; Microfinance Systems<br>
                &#8226; Loan Management Systems<br>
                &#8226; SMS, USSD &amp; WhatsApp Services
            </td>
        </tr>
        <tr>
            <td style="padding: 6px; vertical-align: top;">
                &#8226; HR Management Systems<br>
                &#8226; School Management Systems<br>
                &#8226; Healthcare/Zahanati Systems
            </td>
            <td style="padding: 6px; vertical-align: top;">
                &#8226; ERP &amp; Enterprise Solutions<br>
                &#8226; Cybersecurity Services<br>
                &#8226; Web &amp; Mobile Applications
            </td>
        </tr>
    </table>

    <h3 style="color: #1565C0; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Attached Documents</h3>
    <ol style="font-size: 13px;">
        <li>Certificate of Incorporation (Companies Act, 2002)</li>
        <li>Tax Identification Number (TIN: 181-314-605)</li>
        <li>Business License — ICT Services (Kinondoni Municipal Council)</li>
        <li>Memorandum &amp; Articles of Association</li>
    </ol>

    {financials_note}

    <p>We are confident in our ability to deliver value to <strong>{institution}</strong> and
    welcome the opportunity to discuss our proposal further. We remain available for any
    clarifications or additional documentation you may require.</p>

    <p>
        Yours faithfully,<br><br>
        <strong>Andrew Stanslaus Mashamba</strong><br>
        Director, ZIMA Solutions Limited<br>
        <a href="mailto:info@zima.co.tz">info@zima.co.tz</a> |
        <a href="tel:+255692410353">+255 69 241 0353</a><br>
        <a href="https://zima.co.tz">www.zima.co.tz</a>
    </p>

    <div style="border-top: 2px solid #1565C0; margin-top: 30px; padding-top: 10px; font-size: 11px; color: #999;">
        <p>ZIMA Solutions Limited | Makongo, Near Ardhi University, Kinondoni, Dar es Salaam, Tanzania<br>
        TIN: 181-314-605 | Incorporated under Companies Act, 2002</p>
    </div>

    </body>
    </html>
    """
    return html


def send_tender_application(tender, config, extra_attachments=None):
    """Send a single tender application email."""

    # Determine recipient emails
    contact = tender.get('contact', {})
    to_emails = []
    if isinstance(contact, dict):
        if contact.get('emails'):
            to_emails.extend(contact['emails'])
        if contact.get('email'):
            to_emails.append(contact['email'])

    # Remove duplicates and invalid
    to_emails = list(set(e for e in to_emails if '@' in str(e)))

    if not to_emails:
        return False, "No submission email found"

    # Generate subject
    title = tender.get('title', 'Tender Application')
    ref = tender.get('reference_number', '')
    if ref:
        subject = f"Tender Application: {ref} — {title[:80]} | ZIMA Solutions Limited"
    else:
        subject = f"Tender Application: {title[:80]} | ZIMA Solutions Limited"

    # Generate cover letter
    body = generate_cover_letter_html(tender, None)

    # Attachments
    attachments = [COMPANY_DOCS]
    if extra_attachments:
        attachments.extend(extra_attachments)

    try:
        send_email(config, to_emails, subject, body, attachments, bcc=BCC_EMAIL)
        return True, f"Sent to {', '.join(to_emails)}"
    except Exception as e:
        return False, str(e)


def process_batch(start=0, batch_size=25, dry_run=False):
    """Process a batch of tenders."""
    config = load_config()
    db = load_db()

    # Filter to unsent, non-expired
    pending = [r for r in db if r['application_status'] not in ('Submitted', 'Sent')
               and r['urgency'] != 'EXPIRED']

    # Sort by urgency
    urgency_order = {'CRITICAL':0,'URGENT':1,'HIGH':2,'MEDIUM':3,'LOW':4,'UNKNOWN':5}
    pending.sort(key=lambda r: (urgency_order.get(r['urgency'], 5), r['closing_date'] or 'z'))

    batch = pending[start:start + batch_size]

    print(f"\n{'='*60}")
    print(f"Processing batch: {len(batch)} tenders (offset {start})")
    print(f"{'='*60}")

    sent_count = 0
    skip_count = 0
    fail_count = 0

    for i, tender in enumerate(batch):
        tid = tender['tender_id']
        title = tender['title'][:50]

        # Get emails
        contact = tender.get('contact', {})
        emails = []
        if isinstance(contact, dict):
            emails = contact.get('emails', [])
            if contact.get('email'): emails.append(contact['email'])
        emails = list(set(e for e in emails if '@' in str(e)))

        if not emails:
            print(f"  [{i+1}/{len(batch)}] SKIP {tid} — no email")
            skip_count += 1
            continue

        print(f"  [{i+1}/{len(batch)}] {tid} → {', '.join(emails)}")

        if dry_run:
            print(f"           DRY RUN — would send: {title}")
            continue

        success, msg = send_tender_application(tender, config)

        if success:
            # Update DB
            for r in db:
                if r['tender_id'] == tid and r['institution_slug'] == tender['institution_slug']:
                    r['application_status'] = 'Submitted'
                    r['notes'] = f"Sent {datetime.now().strftime('%Y-%m-%d %H:%M')} to {', '.join(emails)}"
            save_db(db)
            log_sent(tid, emails, f"Tender: {title}", "sent")
            sent_count += 1
            print(f"           ✓ {msg}")

            # Rate limit: wait between sends
            time.sleep(3)
        else:
            log_sent(tid, emails, f"Tender: {title}", "failed", msg)
            fail_count += 1
            print(f"           ✗ FAILED: {msg}")

    print(f"\n{'='*60}")
    print(f"Batch complete: {sent_count} sent, {skip_count} skipped (no email), {fail_count} failed")
    print(f"{'='*60}")
    return sent_count, skip_count, fail_count


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Send tender applications')
    parser.add_argument('--start', type=int, default=0, help='Start offset')
    parser.add_argument('--batch', type=int, default=25, help='Batch size')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (no actual sends)')
    parser.add_argument('--tender-id', type=str, help='Send for a specific tender ID only')
    args = parser.parse_args()

    if args.tender_id:
        config = load_config()
        db = load_db()
        tender = next((r for r in db if r['tender_id'] == args.tender_id), None)
        if tender:
            success, msg = send_tender_application(tender, config)
            print(f"{'✓' if success else '✗'} {args.tender_id}: {msg}")
            if success:
                for r in db:
                    if r['tender_id'] == args.tender_id:
                        r['application_status'] = 'Submitted'
                save_db(db)
        else:
            print(f"Tender {args.tender_id} not found")
    else:
        process_batch(args.start, args.batch, args.dry_run)
