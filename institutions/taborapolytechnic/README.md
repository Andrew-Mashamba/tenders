---
institution:
  name: "Tabora Polytechnic College"
  slug: "taborapolytechnic"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "taborapolytechnic.ac.tz"

website:
  homepage: "https://taborapolytechnic.ac.tz/"
  tender_url: "https://taborapolytechnic.ac.tz/"

contact:
  email: "taborapolytechnic@yahoo.com"
  phone: "0150616901100 "

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Homepage has "AVAILABLE DOWNLOADS" and "NEWS & EVENTS" sections. Download items show title + "Placed On" date.
    Documents at /www/100/news/{hash}filename-{name}.pdf. Also scrape https://taborapolytechnic.ac.tz/news for more.
  selectors:
    container: "main, .content, .entry-content, .page-content, section"
    tender_item: "a[href$='.pdf'], .download-item, li, .row"
    title: "a[href$='.pdf'], h2, h3, h4, .title"
    date: ".date, .placed-on, .mh-meta-date, time"
    document_link: 'a[href$=".pdf"], a[href*="/www/100/news/"]'
    pagination: "a[href*='/news'], .pagination a, a.next" 
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
      - "/www/100/news/"
    url_patterns:
      - "taborapolytechnic.ac.tz/www/100/news/*"

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
      Documents at /www/100/news/{hash}filename-{name}.pdf. URL-encoded filenames. Application forms, not tenders.
      More at /news. Decode percent-encoding for readable filenames.

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
  TABORA POLYTECHNIC COLLEGE
---

# Home

**Category:** Educational Institution
**Website:** https://taborapolytechnic.ac.tz/
**Tender Page:** https://taborapolytechnic.ac.tz/
**Keywords Found:** rfi

## Contact Information
- Email: taborapolytechnic@yahoo.com
- Phone: 0150616901100 
- Phone: +255754 366 331
- Phone: 025-06-02
- Phone: 026-02-25
- Phone: +255628000443

## Scraping Instructions

**Strategy:** Scrape https://taborapolytechnic.ac.tz/ for tender/procurement notices.
**Method:** http_get

TABORA POLYTECHNIC COLLEGE

### Document Links Found

- https://taborapolytechnic.ac.tz/www/100/news/39495c1e97filename-TPC APPLICATION FORM FOR DEMA 2026.pdf
- https://taborapolytechnic.ac.tz/www/100/news/75448c7ee5filename-TPC 1 APPLICATION FORM 2025-2025 (1).pdf
- https://taborapolytechnic.ac.tz/www/100/news/d65e11ef37filename-TPC12 APPLICATION FORM FOR HEALTH AND ALLIED SCIENCES SEPT 2025(2) - Copy.pdf
- https://taborapolytechnic.ac.tz/www/100/news/51c1be15e8filename-TPC APPLICATION FORM FOR DEMA SEPT 2024.pdf

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
taborapolytechnic/
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
- **Signal Strength:** Weak (supply/rfi only)
