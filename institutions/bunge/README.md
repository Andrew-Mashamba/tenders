---
institution:
  name: "Bunge la Tanzania (Tanzania Parliament)"
  slug: "bunge"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "bunge.go.tz"

website:
  homepage: "https://www.parliament.go.tz/"
  tender_url: "https://www.parliament.go.tz/documents/press-release"

contact:
  email: "cna@bunge.go.tz"
  phone: "00
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape parliament.go.tz. No dedicated /zabuni or /tenders page. Tender/job announcements (e.g. TANGAZO LA KUITWA KAZINI) in /documents/press-release. Also check /order_paper, /bills. Documents at parliament.go.tz/uploads/documents/ and polis.bunge.go.tz/uploads/bills/, polis.bunge.go.tz/uploads/documents/."
  selectors:
    container: "main, .content, .page-content, .document-list, article"
    tender_item: "article, .document-item, .news-item, li, .list-group-item"
    title: "h2, h3, h4, .title, a"
    date: ".date, .published, time, small"
    document_link: 'a[href$=".pdf"], a[href*="/uploads/"]'
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

    known_document_paths:
      - "/uploads/documents/"
      - "/uploads/bills/"
    url_patterns:
      - "parliament.go.tz/uploads/documents/*"
      - "polis.bunge.go.tz/uploads/documents/*"
      - "polis.bunge.go.tz/uploads/bills/*"

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
      Two domains: parliament.go.tz and polis.bunge.go.tz. Documents at parliament.go.tz/uploads/documents/{timestamp}-{filename}.pdf and polis.bunge.go.tz/uploads/{bills|documents}/{timestamp}-{filename}.pdf. Mix of legislation, order papers, press releases, job announcements (TANGAZO LA KUITWA KAZINI).

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
  facebook: "bungetz1"
  instagram: "bunge.tanzania"

notes: |
  Tanzania Parliament | Bunge la Tanzania
---

# BUNGE | Mwanzo

**Category:** Government Agency
**Website:** https://www.parliament.go.tz/
**Tender Page:** https://www.parliament.go.tz/
**Keywords Found:** zabuni

## Contact Information
- Email: cna@bunge.go.tz
- Phone: 00
          
- Phone: 025-02-11
- Phone: 026
         
- Phone: 023100 1769062
- Phone: 025-06-26

## Scraping Instructions

**Strategy:** Scrape https://www.parliament.go.tz/ for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Tanzania Parliament | Bunge la Tanzania

### Tender Content Preview

> si Zabuni Ajira <a class='nav-link' href='https://www.parliam

### Document Links Found

- https://www.parliament.go.tz/uploads/documents/sw-1771839275-PRESS RELEASE MUSWADA.pdf
- https://polis.bunge.go.tz/uploads/documents/1772799407-BJT05FEBRUARI2026.pdf
- https://polis.bunge.go.tz/uploads/documents/1773137612-BJT06FEBRUARI2026.pdf
- https://polis.bunge.go.tz/uploads/bills/acts/1744276345-ACT NO. 4 - THE LABOUR LAWS (AMENDMENTS) ACT, 2024 CHAPA DOM.pdf
- https://www.parliament.go.tz/uploads/documents/sw-1770278210-JARIDA LA BUNGE TOLEO LA KUMI NA MOJA.pdf
- https://polis.bunge.go.tz/uploads/bills/1770366301-Muswada_wa_Sheria_ya_Mikopo_kwa_Dhamana_za_Mali_Zinazohamishika_wa_Mwaka_2026.pdf
- https://www.parliament.go.tz/uploads/documents/sw-1767688228-RATIBA YA VIKAO VYA KAMATI ZA BUNGE.pdf
- https://www.parliament.go.tz/uploads/documents/sw-1767689087-VIKAO VYA KAMATI JANUARI, 2026.pdf
- https://polis.bunge.go.tz/uploads/documents/1771830546-BJT03FEBRUARI2026.pdf
- https://polis.bunge.go.tz/uploads/documents/1770344872-OP 06 Feb, 2026.pdf

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

Known document paths: /uploads/bills/1770366114-Muswada_wa_Sheria_ya_Marekebisho_ya_Sheria_Mbalimbali_wa_Mwaka_2026_[The_Written.pdf, /uploads/documents/1771566333-BJT02FEBRUARI2026.pdf, /uploads/documents/1773137612-BJT06FEBRUARI2026.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
bunge/
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
  "tender_id": "BUNGE-2026-001",
  "institution": "bunge",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "BUNGE/T/2026/001",
  "published_date": "2026-03-01",
  "closing_date": "2026-04-15",
  "closing_time": "14:00 EAT",
  "category": "General",
  "status": "active",
  "source_url": "https://www.parliament.go.tz/",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "https://www.parliament.go.tz/storage/tender.pdf",
      "local_path": "./downloads/BUNGE-2026-001/original/tender_document.pdf",
      "file_size_bytes": 2456789,
      "downloaded_at": "2026-03-13T10:30:00Z",
      "content_type": "application/pdf",
      "sha256": "abc123..."
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "cna@bunge.go.tz",
    "phone": "00
          ",
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
  "institution": "bunge",
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
- **Signal Strength:** Strong (zabuni)
