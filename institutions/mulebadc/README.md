---
institution:
  name: "Halmashauri ya Wilaya ya Muleba (Muleba District Council)"
  slug: "mulebadc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "mulebadc.go.tz"

website:
  homepage: "https://mulebadc.go.tz/"
  tender_url: "https://mulebadc.go.tz/tenders"

contact:
  email: "ded@mulebadc.go.tz"
  phone: "06-2025-2"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Fetch https://mulebadc.go.tz/tenders (OctoberCMS). Parse tender items from main content. Documents use /storage/app/uploads/public/{hash}/ path. Follow each tender link to detail page for full documents. Site may be slow or unreachable at times."
  selectors:
    container: "main, .content, .page-content, .entry-content, [role='main']"
    tender_item: ".tender-item, .list-group-item, article, .card, .row .col, li"
    title: "h2, h3, h4, .tender-title, .title, a"
    date: ".date, .closing-date, .published, time, .meta"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/storage/"]'
    pagination: ".pagination a, a.next, .nav-links a, .page-link" 
  schedule: "daily"

  anti_bot:
    requires_javascript: false
    has_captcha: false
    rate_limit_seconds: 10

  documents:
    download_enabled: true
    download_path: "./downloads/"
    naming: "{{date}}_{{title}}_{{filename}}"

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
        - 'a[href$=".pdf"]'
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
        - 'a[download]'
      resolve_redirects: true
      decode_percent_encoding: true

    url_patterns:
      - "mulebadc.go.tz/storage/app/uploads/public/669/907/d44/669907d44f8ca715091757.pdf"
      - "mulebadc.go.tz/storage/app/uploads/public/58a/43d/f94/58a43df944090312121104.pdf"
      - "mulebadc.go.tz/storage/app/uploads/public/665/9c4/a55/6659c4a55afd4719242325.pdf"
      - "mulebadc.go.tz/storage/app/uploads/public/64f/ff7/6e7/64fff76e7023e155983380.pdf"
      - "mulebadc.go.tz/storage/app/uploads/public/654/093/eb6/654093eb6524e959481146.pdf"

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

    known_document_paths:
      - "/storage/app/uploads/public/"
    document_notes: |
      OctoberCMS storage. Documents at /storage/app/uploads/public/{xxx}/{xxx}/{xxx}/{hash}.pdf. Example: 669907d44f8ca715091757.pdf. Site may timeout; retry with rate_limit_seconds: 15.

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

notes: |
  A default home page
---

# Home &#124; Halmashauri ya Wilaya ya Muleba

**Category:** Local Government Authority
**Website:** https://mulebadc.go.tz/
**Tender Page:** https://mulebadc.go.tz/tenders
**Keywords Found:** bid, tender, tenders, zabuni

## Contact Information
- Email: ded@mulebadc.go.tz
- Phone: 06-2025-2
- Phone: 090312121104
- Phone: 06-2025
	     

## Scraping Instructions

**Strategy:** Scrape https://mulebadc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> home-page-title">Zabuni Zaidi Jina la zabuni

### Known Tender URLs

- https://mulebadc.go.tz/tenders

### Document Links Found

- https://mulebadc.go.tz/storage/app/uploads/public/669/907/d44/669907d44f8ca715091757.pdf
- https://mulebadc.go.tz/storage/app/uploads/public/665/9c4/a55/6659c4a55afd4719242325.pdf
- https://mulebadc.go.tz/storage/app/uploads/public/64f/ff6/d79/64fff6d79d7de534438350.pdf
- https://mulebadc.go.tz/storage/app/uploads/public/64f/ff7/6e7/64fff76e7023e155983380.pdf
- https://mulebadc.go.tz/storage/app/uploads/public/654/093/eb6/654093eb6524e959481146.pdf
- https://mulebadc.go.tz/storage/app/uploads/public/58a/43d/f94/58a43df944090312121104.pdf

## Document Download Instructions

The scraper MUST download all linked documents from tender pages, not just scrape metadata.

**File types to download:** PDF, DOC, DOCX, XLS, XLSX, ZIP
**Storage:** Save to `./downloads/` within this institution folder
**Naming convention:** `{date}_{title}_{original_filename}`

### Key behaviors:
1. **Follow all document links** on tender listing pages and individual tender detail pages
2. **Resolve redirects** — some download links redirect through CDN or auth endpoints
3. **Decode percent-encoded URLs** (e.g., `%20` → space) for readable filenames
4. **Check for documents in iframes or embedded viewers** that may wrap a PDF URL
5. **Download attachments from detail pages** — some tenders only show a summary on the listing page with full documents on a detail/inner page
6. **Skip duplicates** based on URL and file hash to avoid re-downloading

Known document paths: /storage/app/uploads/public/669/907/d44/669907d44f8ca715091757.pdf, /storage/app/uploads/public/58a/43d/f94/58a43df944090312121104.pdf, /storage/app/uploads/public/665/9c4/a55/6659c4a55afd4719242325.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
mulebadc/
├── README.md                          # This file — scraper config & instructions
├── tenders/
│   ├── active/                        # Currently open tenders
│   │   ├── {tender_id}.json           # Structured tender metadata
│   │   └── ...
│   ├── closed/                        # Past/expired tenders (auto-moved after closing_date)
│   │   ├── {tender_id}.json
│   │   └── ...
│   └── archive/                       # Historical tenders older than 90 days
│       ├── {tender_id}.json
│       └── ...
├── downloads/
│   ├── {tender_id}/                   # One subfolder per tender
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

### Tender JSON Schema (`tenders/active/{tender_id}.json`)

```json
{{
  "tender_id": "MULEBADC-2026-001",
  "institution": "mulebadc",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "MULEBADC/T/2026/001",
  "published_date": "2026-03-01",
  "closing_date": "2026-04-15",
  "closing_time": "14:00 EAT",
  "category": "General",
  "status": "active",
  "source_url": "https://mulebadc.go.tz/tenders",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "https://mulebadc.go.tz/storage/tender.pdf",
      "local_path": "./downloads/MULEBADC-2026-001/original/tender_document.pdf",
      "file_size_bytes": 2456789,
      "downloaded_at": "2026-03-13T10:30:00Z",
      "content_type": "application/pdf",
      "sha256": "abc123..."
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "ded@mulebadc.go.tz",
    "phone": "06-2025-2",
    "address": "..."
  }},
  "eligibility": "Open to all registered suppliers",
  "bid_security": "TZS ...",
  "scraped_at": "2026-03-13T10:30:00Z",
  "last_checked": "2026-03-13T10:30:00Z",
  "raw_html": "..."
}}
```

### Scrape Log Schema (`scrape_log.json`)

```json
{{
  "runs": [
    {{
      "run_id": "run_20260313_103000",
      "timestamp": "2026-03-13T10:30:00Z",
      "duration_seconds": 12,
      "status": "success",
      "tenders_found": 5,
      "new_tenders": 2,
      "updated_tenders": 1,
      "documents_downloaded": 3,
      "errors": []
    }}
  ]
}}
```

### Last Scrape Snapshot (`last_scrape.json`)

```json
{{
  "institution": "mulebadc",
  "last_scrape": "2026-03-13T10:30:00Z",
  "next_scrape": "2026-03-14T10:30:00Z",
  "active_tenders_count": 0,
  "status": "success",
  "error": null
}}
```


## Post-Scrape Actions

After EACH successful scrape of this institution, the scraper MUST perform these steps in order:

### 1. Organize Tenders by Status
- Parse `closing_date` from each tender JSON
- **Active:** `closing_date` is in the future → `tenders/active/`
- **Closed:** `closing_date` has passed → move from `active/` to `closed/`
- **Archive:** `closing_date` is older than 90 days → move from `closed/` to `archive/`

### 2. Extract Text from Downloaded Documents
For each new document in `downloads/{tender_id}/original/`:
- **PDF:** Extract full text → save to `downloads/{tender_id}/extracted/{filename}.txt`
- **DOCX:** Extract full text → save to `downloads/{tender_id}/extracted/{filename}.txt`
- **XLSX:** Extract sheet names and cell data → save as JSON
- Generate `summary.json` with AI-extracted fields:
  ```json
  {
    "tender_title": "...",
    "institution": "...",
    "scope_of_work": "Brief description of what is being procured",
    "estimated_value": "TZS ...",
    "eligibility_requirements": ["..."],
    "key_dates": {
      "published": "2026-03-01",
      "clarification_deadline": "2026-03-20",
      "site_visit": "2026-03-25",
      "closing_date": "2026-04-15",
      "opening_date": "2026-04-16"
    },
    "required_documents": ["..."],
    "bid_security": "...",
    "categories": ["General"],
    "contact_info": {}
  }
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
Subject: [TENDERS] {new_count} New Tenders Found - {date}

TENDER SCRAPE REPORT — {date}
========================================

SUMMARY
  Total active tenders:   {total_active}
  New tenders found:      {new_count}
  Closing within 7 days:  {urgent_count}
  Documents downloaded:    {docs_count}
  Institutions scraped:    {inst_count}
  Errors:                  {error_count}

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

config = {
    "host": "zima.co.tz",
    "port": 465,
    "user": "info@zima.co.tz",
    "password": "",  # Set in config/email.json
}

msg = MIMEMultipart()
msg["From"] = "info@zima.co.tz"
msg["To"] = "andrew.s.mashamba@gmail.com"
msg["Subject"] = f"[TENDERS] {new_count} New Tenders Found - {date}"
msg.attach(MIMEText(body, "plain"))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(config["host"], config["port"], context=context) as server:
    server.login(config["user"], config["password"])
    server.send_message(msg)
```

**Email configuration** should be stored in:
`/Volumes/DATA/PROJECTS/TENDERS/config/email.json`
```json
{
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
}
```

### 7. Notification Rules
- **Immediate:** Send email if any tender is closing within 48 hours
- **Daily digest (08:00 EAT):** Summary of all active tenders, new finds, and approaching deadlines
- **Error alert:** Send if scraper fails for 3+ consecutive runs on any institution
- **Weekly report (Monday 08:00 EAT):** Full summary across all institutions with trends

## Status

- **Last Checked:** 13 March 2026
- **Active Tenders:** To be scraped
- **Signal Strength:** Strong (tender, tenders, zabuni)
