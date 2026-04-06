---
institution:
  name: "Tiper Tanzania Ltd."
  slug: "tiper"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "tiper.co.tz"

website:
  homepage: "https://tiper.co.tz/"
  tender_url: "https://tiper.co.tz/tenders.php"

contact:
  email: "info@tiper.co.tz"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Scrape tenders.php. Tender content is in div.about section. Each tender has a
    description in .about-text p and document link in a.btn (Learn More). Documents
    stored in /Downloads/ path. Extract title from .section-header h2 or from bold
    text in description.
  selectors:
    container: "div.about"
    tender_item: "div.about"
    title: ".section-header h2, .about-text p b"
    date: ".date, .closing-date, .published, time"
    document_link: 'a.btn[href$=".pdf"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ""
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
        - 'a[href*="/Downloads/"]'
        - 'a[download]'
      resolve_redirects: true
      decode_percent_encoding: true

    known_document_paths:
      - "/Downloads/"

    url_patterns:
      - "tiper.co.tz/Downloads/*.pdf"
      - "tiper.co.tz/Downloads/*.PDF"

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
      Documents stored in /Downloads/ (e.g. Downloads/TIPPER_4X24_NEW.PDF). Each tender
      has a "Learn More" button linking to the PDF. Case-sensitive: .PDF extension.

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
  Tiper Tanzania Ltd - Corporate Website
---

# Tiper Tanzania Ltd.

**Category:** Commercial / Private Sector
**Website:** https://tiper.co.tz/
**Tender Page:** https://tiper.co.tz/tenders.php
**Keywords Found:** tender, tenders

## Contact Information
- Email: info@tiper.co.tz

## Scraping Instructions

**Strategy:** Scrape https://tiper.co.tz/tenders.php for tender/procurement notices.
**Method:** http_get

Tiper Tanzania Ltd - Corporate Website

### Tender Content Preview

> v> Tenders&nbsp; <!---/Navbar

### Known Tender URLs

- https://tiper.co.tz/tenders.php

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
tiper/
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

## Post-Scrape Actions

After EACH successful scrape:

1. **Organize tenders by status** — active/closed/archive based on closing_date
2. **Extract text from documents** — PDF→txt, DOCX→txt, XLSX→json
3. **Generate summary.json** with AI-extracted fields
4. **Update last_scrape.json** and **append to scrape_log.json**
5. **Update global active_tenders.md** index

## Status

- **Last Checked:** 13 March 2026
- **Active Tenders:** To be scraped
- **Signal Strength:** Strong (tender, tenders)
