---
institution:
  name: "Kyerwa District Council"
  slug: "kyerwadc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "kyerwadc.go.tz"

website:
  homepage: "https://kyerwadc.go.tz/"
  tender_url: "https://kyerwadc.go.tz/tenders"

contact:
  email: "ded@kyerwadc.go.tz"
  phone: "020-12-31"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://kyerwadc.go.tz/tenders. OctCMS site (same as kongwadc/korogwedc). Zabuni section with table/list. Documents at /storage/app/uploads/public/{hash}/."
  selectors:
    container: ".right-sidebar-content, .home-page-title, table tbody, .page-content"
    tender_item: "table tbody tr, .tender-item, li"
    title: "td:first-child, h4, h6, .tender-title"
    date: "td:nth-child(2), .date"
    document_link: 'a[href*="/storage/"], a[href$=".pdf"], a[target="blank"]'
    pagination: ".pagination a, a.next, .view-more" 
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
      - "kyerwadc.go.tz/storage/app/uploads/public/5c5/3dd/c87/5c53ddc878997717826947.pdf"
      - "kyerwadc.go.tz/storage/app/uploads/public/5f4/91a/6bd/5f491a6bdc1c6901354662.pdf"
      - "kyerwadc.go.tz/storage/app/uploads/public/5f2/14b/d0e/5f214bd0e1700725736765.pdf"
      - "kyerwadc.go.tz/storage/app/uploads/public/5b9/9f3/b8d/5b99f3b8da8cd385059613.pdf"
      - "kyerwadc.go.tz/storage/app/uploads/public/696/742/390/696742390a23c480805287.pdf"

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
      OctCMS. Documents at /storage/app/uploads/public/{hash}/{filename}.pdf. Same platform as kongwadc/korogwedc. Follow /tenders and /procurement-and-supply.

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
  facebook: "kyerwadc"
  instagram: "kyerwadistrictcouncil"

notes: |
  A default home page
---

# Home &#124; Kyerwa District Council

**Category:** Local Government Authority
**Website:** https://kyerwadc.go.tz/
**Tender Page:** https://kyerwadc.go.tz/tenders
**Keywords Found:** bid, manunuzi, procurement, supply, tender, tenders, zabuni

## Contact Information
- Email: ded@kyerwadc.go.tz
- Phone: 020-12-31
- Phone: +255 754 422 746 
- Phone: 00725736765
- Phone: 019-04-30
- Phone: 022
          

## Scraping Instructions

**Strategy:** Scrape https://kyerwadc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> home-page-title">Zabuni Zaidi Jina la zabuni

### Known Tender URLs

- https://kyerwadc.go.tz/tenders
- https://kyerwadc.go.tz/procurement-and-supply

### Document Links Found

- https://kyerwadc.go.tz/storage/app/uploads/public/5f2/14b/d0e/5f214bd0e1700725736765.pdf
- https://kyerwadc.go.tz/storage/app/uploads/public/5b9/9f3/b8d/5b99f3b8da8cd385059613.pdf
- https://kyerwadc.go.tz/storage/app/uploads/public/5f4/91a/6bd/5f491a6bdc1c6901354662.pdf
- https://kyerwadc.go.tz/storage/app/uploads/public/5c5/3dd/c87/5c53ddc878997717826947.pdf
- https://kyerwadc.go.tz/storage/app/uploads/public/5ff/408/03c/5ff40803ceae9551379070.pdf
- https://kyerwadc.go.tz/storage/app/uploads/public/696/742/390/696742390a23c480805287.pdf

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

Known document paths: /storage/app/uploads/public/5c5/3dd/c87/5c53ddc878997717826947.pdf, /storage/app/uploads/public/5f4/91a/6bd/5f491a6bdc1c6901354662.pdf, /storage/app/uploads/public/5f2/14b/d0e/5f214bd0e1700725736765.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
kyerwadc/
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
  "tender_id": "KYERWADC-2026-001",
  "institution": "kyerwadc",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "KYERWADC/T/2026/001",
  "published_date": "2026-03-01",
  "closing_date": "2026-04-15",
  "closing_time": "14:00 EAT",
  "category": "General",
  "status": "active",
  "source_url": "https://kyerwadc.go.tz/tenders",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "https://kyerwadc.go.tz/storage/tender.pdf",
      "local_path": "./downloads/KYERWADC-2026-001/original/tender_document.pdf",
      "file_size_bytes": 2456789,
      "downloaded_at": "2026-03-13T10:30:00Z",
      "content_type": "application/pdf",
      "sha256": "abc123..."
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "ded@kyerwadc.go.tz",
    "phone": "020-12-31",
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
  "institution": "kyerwadc",
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
- **Signal Strength:** Strong (manunuzi, procurement, tender, tenders, zabuni)
