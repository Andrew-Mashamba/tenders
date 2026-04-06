#!/usr/bin/env python3
"""
Re-enrich shallow README.md files in institutions/ folders.
Finds all READMEs with <=30 lines (from the initial crawl), re-crawls
those domains, and regenerates them using the detailed format from crawl_all_tz.py.
"""

import asyncio
import aiohttp
import ssl
import re
import json
import os
import logging
import warnings
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone

# Suppress noise
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")

BASE_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
INST_DIR = BASE_DIR / "institutions"

TIMEOUT = aiohttp.ClientTimeout(total=15, connect=8)
CONCURRENCY = 30

TENDER_KEYWORDS = [
    'tender', 'tenders', 'procurement', 'rfp', 'rfq', 'rfi',
    'expression of interest', 'eoi', 'bidding', 'bid',
    'zabuni', 'manunuzi',
    'quotation', 'invitation to bid', 'request for proposal',
    'supply', 'prequalification',
]

STRONG_KEYWORDS = {
    'tender', 'tenders', 'procurement', 'rfp', 'rfq', 'eoi',
    'expression of interest', 'bidding', 'zabuni', 'manunuzi', 'prequalification',
}

TENDER_PATHS = [
    '/tenders', '/tender', '/procurement', '/tenders/', '/tender/',
    '/procurement/', '/bids', '/opportunities',
    '/zabuni', '/manunuzi',
    '/en/tenders', '/en/procurement',
]

DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar'}


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def classify_domain(domain):
    d = domain.lower()
    if '.go.tz' in d:
        if any(x in d for x in ['dc.go', 'mc.go', 'tc.go', 'cc.go']):
            return "Local Government Authority"
        elif any(x in d for x in ['wasa', 'uwsa', 'wssa']):
            return "Water Utility"
        elif any(x in d for x in ['hospital', 'health']):
            return "Government Hospital"
        else:
            return "Government Agency"
    elif '.ac.tz' in d or '.sc.tz' in d:
        return "Educational Institution"
    elif '.or.tz' in d:
        return "NGO / Non-Profit Organization"
    elif any(x in d for x in ['bank', 'benki']):
        return "Bank"
    elif any(x in d for x in ['insurance', 'bima']):
        return "Insurance Company"
    elif any(x in d for x in ['saccos', 'sacco']):
        return "SACCOS"
    elif any(x in d for x in ['finance', 'microfinance']):
        return "Microfinance / Financial Services"
    elif any(x in d for x in ['hospital', 'clinic', 'health', 'medical']):
        return "Healthcare"
    elif any(x in d for x in ['mining', 'oil', 'gas', 'energy', 'electric']):
        return "Energy / Mining"
    elif any(x in d for x in ['transport', 'logistics', 'shipping', 'freight']):
        return "Transport / Logistics"
    elif any(x in d for x in ['hotel', 'safari', 'travel', 'tour']):
        return "Tourism / Hospitality"
    elif any(x in d for x in ['invest', 'capital', 'securities', 'broker']):
        return "Investment / Securities"
    elif any(x in d for x in ['construction', 'building', 'engineer']):
        return "Construction / Engineering"
    elif any(x in d for x in ['tech', 'software', 'ict', 'digital', 'computer']):
        return "ICT / Technology"
    else:
        return "Commercial / Private Sector"


def extract_page_info(text, url, domain):
    text_lower = text.lower()
    info = {
        'url': url,
        'title': '',
        'description': '',
        'keywords_found': [],
        'tender_links': [],
        'document_links': [],
        'contact_email': [],
        'contact_phone': [],
        'social_media': {},
        'has_tender_page': False,
        'tender_page_urls': [],
        'document_download_paths': [],
        'raw_text_snippet': '',
    }

    m = re.search(r'<title[^>]*>([^<]+)</title>', text, re.I)
    info['title'] = m.group(1).strip()[:200] if m else domain

    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', text, re.I)
    if not m:
        m = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']description["\']', text, re.I)
    if m:
        info['description'] = m.group(1).strip()[:500]

    for kw in TENDER_KEYWORDS:
        if kw in text_lower:
            info['keywords_found'].append(kw)

    tender_link_re = re.compile(
        r'href=["\']([^"\']*(?:tender|procurement|rfp|rfq|bid|zabuni|manunuzi|quotation)[^"\']*)["\']', re.I)
    for m in tender_link_re.finditer(text):
        link = m.group(1)
        if not link.startswith(('javascript:', 'mailto:', '#', 'tel:')):
            full = urljoin(url, link)
            info['tender_links'].append(full)
    info['tender_links'] = list(set(info['tender_links']))[:20]

    if info['tender_links']:
        info['has_tender_page'] = True
        info['tender_page_urls'] = info['tender_links'][:5]

    doc_link_re = re.compile(r'href=["\']([^"\']+\.(?:pdf|doc|docx|xls|xlsx|zip|rar))["\']', re.I)
    for m in doc_link_re.finditer(text):
        full = urljoin(url, m.group(1))
        info['document_links'].append(full)
    info['document_links'] = list(set(info['document_links']))[:20]

    path_patterns = [r'/(?:storage|uploads|media|wp-content/uploads|assets|files|documents|content/dam)/[^"\'>\s]+']
    for pat in path_patterns:
        for m in re.finditer(pat, text, re.I):
            path = m.group(0)
            if any(path.lower().endswith(ext) for ext in DOCUMENT_EXTENSIONS):
                info['document_download_paths'].append(path)
    info['document_download_paths'] = list(set(info['document_download_paths']))[:10]

    email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    emails = set(email_re.findall(text))
    info['contact_email'] = [e for e in emails if not any(x in e.lower() for x in
        ['example.com', 'sentry.io', 'wordpress', 'wixpress', 'schema.org',
         'w3.org', 'google.com', 'facebook.com', 'twitter.com', 'jquery',
         'cloudflare', 'gravatar', 'github'])][:5]

    phone_re = re.compile(r'(?:\+255|0)\s*\d[\d\s\-]{7,12}')
    info['contact_phone'] = list(set(phone_re.findall(text)))[:5]

    social_patterns = {
        'facebook': r'(?:facebook\.com|fb\.com)/([a-zA-Z0-9._-]+)',
        'twitter': r'twitter\.com/([a-zA-Z0-9_]+)',
        'linkedin': r'linkedin\.com/(?:company|in)/([a-zA-Z0-9._-]+)',
        'instagram': r'instagram\.com/([a-zA-Z0-9._-]+)',
    }
    for platform, pat in social_patterns.items():
        m = re.search(pat, text, re.I)
        if m:
            info['social_media'][platform] = m.group(1)

    for kw in ['tender', 'procurement', 'zabuni']:
        idx = text_lower.find(kw)
        if idx > 0:
            start = max(0, idx - 100)
            end = min(len(text), idx + 200)
            snippet = re.sub(r'<[^>]+>', ' ', text[start:end])
            snippet = re.sub(r'\s+', ' ', snippet).strip()
            if len(snippet) > 20:
                info['raw_text_snippet'] = snippet[:300]
                break

    return info


def generate_readme(domain, hits):
    title = hits[0]['title']
    url = hits[0]['url']
    org_type = classify_domain(domain)
    parsed = urlparse(url)
    homepage = f"{parsed.scheme}://{parsed.netloc}/"

    all_kws = set()
    all_tender_links = []
    all_doc_links = []
    all_emails = []
    all_phones = []
    social = {}
    doc_paths = []
    description = ''
    snippet = ''

    for h in hits:
        all_kws.update(h.get('keywords_found', []))
        all_tender_links.extend(h.get('tender_links', []))
        all_doc_links.extend(h.get('document_links', []))
        all_emails.extend(h.get('contact_email', []))
        all_phones.extend(h.get('contact_phone', []))
        social.update(h.get('social_media', {}))
        doc_paths.extend(h.get('document_download_paths', []))
        if h.get('description') and not description:
            description = h['description']
        if h.get('raw_text_snippet') and not snippet:
            snippet = h['raw_text_snippet']

    all_tender_links = list(set(all_tender_links))[:15]
    all_doc_links = list(set(all_doc_links))[:15]
    all_emails = list(set(all_emails))[:5]
    all_phones = list(set(all_phones))[:5]
    doc_paths = list(set(doc_paths))[:10]

    tender_url = all_tender_links[0] if all_tender_links else homepage
    strong = all_kws & STRONG_KEYWORDS
    is_strong = bool(strong)

    if any(x in domain for x in ['.go.tz']):
        strategy = f"Scrape {tender_url} for government tender notices. Government sites often post zabuni/manunuzi."
    elif 'bank' in domain:
        strategy = f"Scrape {tender_url} for banking tender notices and EOIs. Banks post frequently."
    else:
        strategy = f"Scrape {tender_url} for tender/procurement notices."

    slug = domain.replace('.co.tz', '').replace('.go.tz', '').replace('.or.tz', '').replace('.ac.tz', '').replace('.sc.tz', '').replace('.tz', '')

    selectors_block = """  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" """

    url_patterns = ""
    if doc_paths:
        url_patterns = "\n".join(f'      - "{domain}{p}"' for p in doc_paths[:5])
    else:
        url_patterns = f'      - "{domain}/*.pdf"'

    link_selectors = """        - 'a[href$=".pdf"]'
        - 'a[href$=".doc"]'
        - 'a[href$=".docx"]'
        - 'a[href$=".xls"]'
        - 'a[href$=".xlsx"]'
        - 'a[href$=".zip"]'
        - 'a[href*="/storage/"]'
        - 'a[href*="/uploads/"]'
        - 'a[href*="/media/"]'
        - 'a[href*="/wp-content/uploads/"]'
        - 'a[href*="/download"]'
        - 'a[download]'"""

    doc_notes = ""
    if doc_paths:
        doc_notes = f"Known document paths: {', '.join(doc_paths[:3])}"
    else:
        doc_notes = "Document storage paths not yet identified. Check tender detail pages for download links."

    contact_block = ""
    if all_emails or all_phones:
        contact_block = "\ncontact:\n"
        if all_emails:
            contact_block += f"  email: \"{all_emails[0]}\"\n"
            if len(all_emails) > 1:
                contact_block += f"  alternate_emails:\n"
                for e in all_emails[1:]:
                    contact_block += f"    - \"{e}\"\n"
        if all_phones:
            contact_block += f"  phone: \"{all_phones[0]}\"\n"

    social_block = ""
    if social:
        social_block = "\nsocial_media:\n"
        for platform, handle in social.items():
            social_block += f"  {platform}: \"{handle}\"\n"

    readme = f"""---
institution:
  name: "{title}"
  slug: "{slug}"
  category: "{org_type}"
  status: "active"
  country: "Tanzania"
  domain: "{domain}"

website:
  homepage: "{homepage}"
  tender_url: "{tender_url}"
{contact_block}
scraping:
  enabled: true
  method: "http_get"
  strategy: "{strategy}"
{selectors_block}
  schedule: "daily"

  anti_bot:
    requires_javascript: false
    has_captcha: false
    rate_limit_seconds: 10

  documents:
    download_enabled: true
    download_path: "./downloads/"
    naming: "{{{{date}}}}_{{{{title}}}}_{{{{filename}}}}"

    file_types:
      - ".pdf"
      - ".doc"
      - ".docx"
      - ".xls"
      - ".xlsx"
      - ".zip"
      - ".rar"

    url_discovery:
      follow_links: true
      link_selectors:
{link_selectors}
      resolve_redirects: true
      decode_percent_encoding: true

    url_patterns:
{url_patterns}

    download_rules:
      max_file_size_mb: 50
      timeout_seconds: 60
      retry_attempts: 3
      skip_duplicates: true
      verify_content_type: true
      allowed_content_types:
        - "application/pdf"
        - "application/msword"
        - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        - "application/vnd.ms-excel"
        - "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        - "application/zip"
        - "application/octet-stream"

    document_notes: |
      {doc_notes}

  output:
    format: "json"
    fields:
      - tender_id
      - title
      - description
      - published_date
      - closing_date
      - category
      - document_links
      - contact_info
{social_block}
notes: |
  {description if description else f"Organization website at {domain}. Tender keywords detected: {', '.join(sorted(all_kws))}."}
---

# {title}

**Category:** {org_type}
**Website:** {homepage}
**Tender Page:** {tender_url}
**Keywords Found:** {', '.join(sorted(all_kws))}

## Contact Information
"""

    if all_emails:
        for e in all_emails:
            readme += f"- Email: {e}\n"
    if all_phones:
        for p in all_phones:
            readme += f"- Phone: {p}\n"
    if not all_emails and not all_phones:
        readme += "- Not yet extracted. Check website.\n"

    readme += f"""
## Scraping Instructions

**Strategy:** {strategy}
**Method:** http_get

{description if description else ''}

"""

    if snippet:
        readme += f"""### Tender Content Preview

> {snippet}

"""

    if all_tender_links:
        readme += "### Known Tender URLs\n\n"
        for link in all_tender_links[:10]:
            readme += f"- {link}\n"
        readme += "\n"

    if all_doc_links:
        readme += "### Document Links Found\n\n"
        for link in all_doc_links[:10]:
            readme += f"- {link}\n"
        readme += "\n"

    readme += f"""## Document Download Instructions

The scraper MUST download all linked documents from tender pages, not just scrape metadata.

**File types to download:** PDF, DOC, DOCX, XLS, XLSX, ZIP
**Storage:** Save to `./downloads/` within this institution folder
**Naming convention:** `{{date}}_{{title}}_{{original_filename}}`

### Key behaviors:
1. **Follow all document links** on tender listing pages and individual tender detail pages
2. **Resolve redirects** — some download links redirect through CDN or auth endpoints
3. **Decode percent-encoded URLs** (e.g., `%20` → space) for readable filenames
4. **Check for documents in iframes or embedded viewers** that may wrap a PDF URL
5. **Download attachments from detail pages** — some tenders only show a summary on the listing page with full documents on a detail/inner page
6. **Skip duplicates** based on URL and file hash to avoid re-downloading

{doc_notes}

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
{slug}/
├── README.md                          # This file — scraper config & instructions
├── tenders/
│   ├── active/                        # Currently open tenders
│   │   ├── {{tender_id}}.json           # Structured tender metadata
│   │   └── ...
│   ├── closed/                        # Past/expired tenders (auto-moved after closing_date)
│   │   ├── {{tender_id}}.json
│   │   └── ...
│   └── archive/                       # Historical tenders older than 90 days
│       ├── {{tender_id}}.json
│       └── ...
├── downloads/
│   ├── {{tender_id}}/                   # One subfolder per tender
│   │   ├── original/                  # Raw downloaded files (never modified)
│   │   │   ├── tender_document.pdf
│   │   │   └── ...
│   │   └── extracted/                 # AI-extracted text/data from documents
│   │       ├── tender_document.txt    # Plain text extraction
│   │       ├── summary.json           # AI-generated structured summary
│   │       └── key_dates.json         # Extracted dates & deadlines
│   └── ...
├── scrape_log.json                    # History of all scrape runs
└── last_scrape.json                   # Last scrape result snapshot
```

### Tender JSON Schema (`tenders/active/{{tender_id}}.json`)

```json
{{{{
  "tender_id": "{slug.upper()}-2026-001",
  "institution": "{slug}",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "{slug.upper()}/T/2026/001",
  "published_date": "2026-03-01",
  "closing_date": "2026-04-15",
  "closing_time": "14:00 EAT",
  "category": "General",
  "status": "active",
  "source_url": "{tender_url}",
  "documents": [
    {{{{
      "filename": "tender_document.pdf",
      "original_url": "{homepage}storage/tender.pdf",
      "local_path": "./downloads/{slug.upper()}-2026-001/original/tender_document.pdf",
      "file_size_bytes": 2456789,
      "downloaded_at": "2026-03-13T10:30:00Z",
      "content_type": "application/pdf",
      "sha256": "abc123..."
    }}}}
  ],
  "contact": {{{{
    "name": "Procurement Department",
    "email": "{all_emails[0] if all_emails else 'tenders@' + domain}",
    "phone": "{all_phones[0] if all_phones else '+255...'}",
    "address": "..."
  }}}},
  "eligibility": "Open to all registered suppliers",
  "bid_security": "TZS ...",
  "scraped_at": "2026-03-13T10:30:00Z",
  "last_checked": "2026-03-13T10:30:00Z",
  "raw_html": "..."
}}}}
```

### Scrape Log Schema (`scrape_log.json`)

```json
{{{{
  "runs": [
    {{{{
      "run_id": "run_20260313_103000",
      "timestamp": "2026-03-13T10:30:00Z",
      "duration_seconds": 12,
      "status": "success",
      "tenders_found": 5,
      "new_tenders": 2,
      "updated_tenders": 1,
      "documents_downloaded": 3,
      "errors": []
    }}}}
  ]
}}}}
```

### Last Scrape Snapshot (`last_scrape.json`)

```json
{{{{
  "institution": "{slug}",
  "last_scrape": "2026-03-13T10:30:00Z",
  "next_scrape": "2026-03-14T10:30:00Z",
  "active_tenders_count": 0,
  "status": "success",
  "error": null
}}}}
```


## Post-Scrape Actions

After EACH successful scrape of this institution, the scraper MUST perform these steps in order:

### 1. Organize Tenders by Status
- Parse `closing_date` from each tender JSON
- **Active:** `closing_date` is in the future → `tenders/active/`
- **Closed:** `closing_date` has passed → move from `active/` to `closed/`
- **Archive:** `closing_date` is older than 90 days → move from `closed/` to `archive/`

### 2. Extract Text from Downloaded Documents
For each new document in `downloads/{{tender_id}}/original/`:
- **PDF:** Extract full text → save to `downloads/{{tender_id}}/extracted/{{filename}}.txt`
- **DOCX:** Extract full text → save to `downloads/{{tender_id}}/extracted/{{filename}}.txt`
- **XLSX:** Extract sheet names and cell data → save as JSON
- Generate `summary.json` with AI-extracted fields:
  ```json
  {{
    "tender_title": "...",
    "institution": "...",
    "scope_of_work": "Brief description of what is being procured",
    "estimated_value": "TZS ...",
    "eligibility_requirements": ["..."],
    "key_dates": {{
      "published": "2026-03-01",
      "clarification_deadline": "2026-03-20",
      "site_visit": "2026-03-25",
      "closing_date": "2026-04-15",
      "opening_date": "2026-04-16"
    }},
    "required_documents": ["..."],
    "bid_security": "...",
    "categories": ["General"],
    "contact_info": {{}}
  }}
  ```

### 3. Update `last_scrape.json`
Write/overwrite with current run status.

### 4. Append to `scrape_log.json`
Append a new entry to the runs array.

### 5. Update Global Active Tenders Index
After scraping ALL institutions, regenerate:
**`/Volumes/DATA/PROJECTS/TENDERS/institutions/active_tenders.md`**

Steps:
1. Read all `institutions/*/tenders/active/*.json` files
2. Sort by `closing_date` ascending (soonest first)
3. Group by institution category
4. Calculate summary metrics (total, new, closing soon, etc.)
5. Write the markdown file with tables

### 6. Send Email Notification
Send a summary email after each full scrape run:

```
To: andrew.s.mashamba@gmail.com
Subject: [TENDERS] {{new_count}} New Tenders Found - {{date}}

TENDER SCRAPE REPORT — {{date}}
========================================

SUMMARY
  Total active tenders:   {{total_active}}
  New tenders found:      {{new_count}}
  Closing within 7 days:  {{urgent_count}}
  Documents downloaded:    {{docs_count}}
  Institutions scraped:    {{inst_count}}
  Errors:                  {{error_count}}

CLOSING SOON (within 7 days)
----------------------------------------
  [institution] title
  Closes: closing_date (days_left days left)

NEW TENDERS
----------------------------------------
  [institution] title
  Published: published_date
  Closes: closing_date

ERRORS (if any)
----------------------------------------
  [institution] error_message

----------------------------------------
Full report: /Volumes/DATA/PROJECTS/TENDERS/institutions/active_tenders.md
```

**Email sending method (in order of preference):**
1. Python `smtplib` with SSL on port 465 to `zima.co.tz` (configured in `config/email.json`)
2. `curl` with SMTPS
3. `sendmail` / `mail` command
4. macOS `osascript` Mail.app automation
5. Write to `/Volumes/DATA/PROJECTS/TENDERS/notifications/pending/`

**SMTP Connection Example (Python):**
```python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = {{
    "host": "zima.co.tz",
    "port": 465,
    "user": "info@zima.co.tz",
    "password": "",  # Set in config/email.json
}}

msg = MIMEMultipart()
msg["From"] = "info@zima.co.tz"
msg["To"] = "andrew.s.mashamba@gmail.com"
msg["Subject"] = f"[TENDERS] {{new_count}} New Tenders Found - {{date}}"
msg.attach(MIMEText(body, "plain"))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(config["host"], config["port"], context=context) as server:
    server.login(config["user"], config["password"])
    server.send_message(msg)
```

**Email configuration** should be stored in:
`/Volumes/DATA/PROJECTS/TENDERS/config/email.json`
```json
{{
  "to": "andrew.s.mashamba@gmail.com",
  "from": "info@zima.co.tz",
  "smtp_host": "zima.co.tz",
  "smtp_port": 465,
  "smtp_encryption": "ssl",
  "smtp_user": "info@zima.co.tz",
  "smtp_password": "",
  "send_on_new_tenders": true,
  "send_on_urgent": true,
  "send_on_errors": true,
  "daily_digest": true,
  "digest_time": "08:00"
}}
```

### 7. Notification Rules
- **Immediate:** Send email if any tender is closing within 48 hours
- **Daily digest (08:00 EAT):** Summary of all active tenders, new finds, and approaching deadlines
- **Error alert:** Send if scraper fails for 3+ consecutive runs on any institution
- **Weekly report (Monday 08:00 EAT):** Full summary across all institutions with trends

## Status

- **Last Checked:** {datetime.now(timezone.utc).strftime('%d %B %Y')}
- **Active Tenders:** To be scraped
- **Signal Strength:** {"Strong" if is_strong else "Weak"} ({', '.join(sorted(strong)) if strong else 'supply/rfi only'})
"""

    return readme


async def check_domain(session, domain, sem):
    async with sem:
        results = []
        for scheme in ['https', 'http']:
            url = f"{scheme}://{domain}"
            try:
                async with session.get(url, allow_redirects=True, timeout=TIMEOUT) as resp:
                    if resp.status == 200:
                        text = await resp.text(errors='replace')
                        if len(text) > 200:
                            info = extract_page_info(text, str(resp.url), domain)
                            if info['keywords_found']:
                                results.append(info)
                                break
            except Exception:
                continue

        if not results:
            for path in TENDER_PATHS[:3]:
                for scheme in ['https', 'http']:
                    try:
                        test_url = f"{scheme}://{domain}{path}"
                        async with session.get(test_url, allow_redirects=True, timeout=TIMEOUT) as resp:
                            if resp.status == 200:
                                text = await resp.text(errors='replace')
                                if len(text) > 500:
                                    info = extract_page_info(text, str(resp.url), domain)
                                    if info['keywords_found']:
                                        results.append(info)
                                        break
                    except Exception:
                        continue
                if results:
                    break

        if results:
            return (domain, results)
        return None


def find_shallow_readmes():
    """Find all institution folders with shallow READMEs (<=30 lines)."""
    shallow = []
    for folder in sorted(INST_DIR.iterdir()):
        if not folder.is_dir():
            continue
        readme = folder / "README.md"
        if readme.exists():
            with open(readme) as f:
                lines = f.readlines()
            if len(lines) <= 30:
                # Extract domain from README
                domain = None
                for line in lines:
                    if '**Domain:**' in line:
                        domain = line.split('**Domain:**')[1].strip()
                        break
                if domain:
                    shallow.append((folder.name, domain))
    return shallow


async def main():
    shallow = find_shallow_readmes()
    fprint(f"Found {len(shallow)} shallow READMEs to re-enrich")
    fprint()

    if not shallow:
        fprint("No shallow READMEs found!")
        return

    sem = asyncio.Semaphore(CONCURRENCY)
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(ssl=ssl_ctx, limit=CONCURRENCY, ttl_dns_cache=300)

    enriched = 0
    failed = 0

    async with aiohttp.ClientSession(connector=connector) as session:
        # Process in batches of 50
        batch_size = 50
        domains = [domain for _, domain in shallow]
        folder_map = {domain: folder for folder, domain in shallow}

        for i in range(0, len(domains), batch_size):
            batch = domains[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(domains) + batch_size - 1) // batch_size
            fprint(f"Batch {batch_num}/{total_batches} ({len(batch)} domains)...")

            tasks = [check_domain(session, domain, sem) for domain in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception) or result is None:
                    failed += 1
                    continue
                domain, hits = result
                folder_name = folder_map[domain]
                folder_path = INST_DIR / folder_name

                readme_content = generate_readme(domain, hits)
                (folder_path / "README.md").write_text(readme_content)
                enriched += 1
                kws = ', '.join(hits[0].get('keywords_found', [])[:3])
                fprint(f"  ✓ {domain} → {folder_name}/ ({kws})")

            fprint(f"  Enriched: {enriched} | Failed: {failed}")

    fprint(f"\n{'='*60}")
    fprint(f"ENRICHMENT COMPLETE")
    fprint(f"{'='*60}")
    fprint(f"Total shallow READMEs: {len(shallow)}")
    fprint(f"Successfully enriched: {enriched}")
    fprint(f"Failed (domain unreachable): {failed}")


if __name__ == "__main__":
    asyncio.run(main())
