---
institution:
  name: "El-Olam Health Center"
  slug: "el-olamhospital"
  category: "Healthcare"
  status: "active"
  country: "Tanzania"
  domain: "el-olamhospital.co.tz"

website:
  homepage: "https://el-olamhospital.co.tz/"
  tender_url: "https://el-olamhospital.co.tz/"

contact:
  email: "info@el-olamhospital.co.tz"
  alternate_emails:
    - "reception@el-olamhospital.co.tz"
  phone: "+255743573807"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://el-olamhospital.co.tz/ for tender/procurement. El-Olam Health Center - healthcare facility. No dedicated tender section found on homepage. Monitor for procurement announcements."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" 
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
      - "el-olamhospital.co.tz/*.pdf"

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
      No dedicated tender section or document links found. El-Olam Health Center homepage; documents may appear in /storage/ or /wp-content/uploads/ if tender content is added.

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

social_media:
  facebook: "elolamhospital"
  instagram: "elolamhospital"

notes: |
  Fight for Your Better Health
---

# El-Olam Health Center

**Category:** Healthcare
**Website:** https://el-olamhospital.co.tz/
**Tender Page:** https://el-olamhospital.co.tz/
**Keywords Found:** eoi, rfi, rfp, rfq

## Contact Information
- Email: info@el-olamhospital.co.tz
- Email: reception@el-olamhospital.co.tz
- Phone: +255743573807
- Phone: +255 753825717
- Phone: 0832530860
- Phone: +255753825717
- Phone: 0 0 100 100

## Scraping Instructions

**Strategy:** Scrape https://el-olamhospital.co.tz/ for tender/procurement notices.
**Method:** http_get

Fight for Your Better Health

### Known Tender URLs

- https://el-olamhospital.co.tz/
- https://el-olamhospital.co.tz/

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

Document storage paths not yet identified. Check tender detail pages for download links.

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
el-olamhospital/
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
  "tender_id": "EL-OLAMHOSPITAL-2026-001",
  "institution": "el-olamhospital",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "EL-OLAMHOSPITAL/T/2026/001",
  "published_date": "2026-03-01",
  "closing_date": "2026-04-15",
  "closing_time": "14:00 EAT",
  "category": "General",
  "status": "active",
  "source_url": "https://el-olamhospital.co.tz/"AAAANSUhEUgAAAgAAAAIACAMAAADDpiTIAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAv1QTFRFAAAAAB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05AB05BrNJ4wAAAP90Uk5TABFos+L/YQ8aivXziRw7qvw5BVzLyloEFH3n5nsTJJf2lSI9sP2tAlbJxlIBEHbg3XEOJ5r0JVC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",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "https://el-olamhospital.co.tz/storage/tender.pdf",
      "local_path": "./downloads/EL-OLAMHOSPITAL-2026-001/original/tender_document.pdf",
      "file_size_bytes": 2456789,
      "downloaded_at": "2026-03-13T10:30:00Z",
      "content_type": "application/pdf",
      "sha256": "abc123..."
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "info@el-olamhospital.co.tz",
    "phone": "+255743573807",
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
  "institution": "el-olamhospital",
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
- **Signal Strength:** Strong (eoi, rfp, rfq)
