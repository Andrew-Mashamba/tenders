---
institution:
  name: "Morogoro Water Supply and Sanitation Authority (MORUWASA)"
  slug: "moruwasa"
  category: "Water Utility"
  status: "active"
  country: "Tanzania"
  domain: "moruwasa.go.tz"

website:
  homepage: "https://moruwasa.go.tz/"
  tender_url: "https://moruwasa.go.tz/pages/Tenders.html"

contact:
  email: "md@moruwasa.go.tz"
  alternate_emails:
    - "info@moruwasa.go.tz"
  phone: "020           "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Fetch https://moruwasa.go.tz/pages/Tenders.html. Page shows 'Under construction Update.' — no tender table yet. When live, parse .sub-main-content or .content-border. Documents linked from /pages/ (e.g. *.pdf). Check periodically for when page goes live."
  selectors:
    container: ".sub-main-content, .content-border, .tender-list, main"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .title-decoration, .tender-title, a"
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

    known_document_paths:
      - "/pages/"
    url_patterns:
      - "moruwasa.go.tz/pages/*.pdf"
      - "moruwasa.go.tz/pages/*.doc"
      - "moruwasa.go.tz/pages/*.docx"

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
      Tenders page shows 'Under construction Update.' Documents stored in /pages/ (e.g. Tenders.html, NEW CONNECTION FORM-NEW.pdf, JARIDA MORUWASA YETU .2024.pdf). Re-check when page goes live.

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
  Morogoro Water Supply and Sanitation Authority(MORUWASA)  is an entity charged with the overall operation and management of water supply and sanitation services in Morogoro Municipality replacing the former Urban Water Supply Department, which operated under the Regional Administration.
---

# Home
| Morogoro Water Supply and Sanitation Authority(MORUWASA)

**Category:** Water Utility
**Website:** https://moruwasa.go.tz/
**Tender Page:** https://moruwasa.go.tz/pages/Tenders.html
**Keywords Found:** bid, procurement, rfi, supply, tender, tenders

## Contact Information
- Email: md@moruwasa.go.tz
- Email: info@moruwasa.go.tz
- Phone: 020           
- Phone: 0800751011

## Scraping Instructions

**Strategy:** Scrape https://moruwasa.go.tz/pages/Tenders.html for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Morogoro Water Supply and Sanitation Authority(MORUWASA)  is an entity charged with the overall operation and management of water supply and sanitation services in Morogoro Municipality replacing the former Urban Water Supply Department, which operated under the Regional Administration.

### Tender Content Preview

> lass="list-inline-item"> Tenders <a class="btn btn-success btn-sm" href="pages/contact

### Known Tender URLs

- https://moruwasa.go.tz/pages/Tenders.html

### Document Links Found

- https://moruwasa.go.tz/pages/HUDUMA KWA MTEJA JANUARI0001.pdf
- https://moruwasa.go.tz/pages/JARIDA MORUWASA YETU .2024.pdf
- https://moruwasa.go.tz/pages/GN.-928-MOROGORO-TARIFF-ORDER-2019-ENGLISH.pdf
- https://moruwasa.go.tz/pages/TANGAZO FINAL 060125.pdf
- https://moruwasa.go.tz/pages/JARIDA MORUWASA .pdf
- https://moruwasa.go.tz/pages/ HOTUBA YA WIZARA YA MAJI 2022-2023.pdf
- https://moruwasa.go.tz/pages/NEW CONNECTION FORM-NEW.pdf
- https://moruwasa.go.tz/pages/Kipeperushi.pdf
- https://moruwasa.go.tz/pages/RATIBA YA MGAO WA .MAJI.pdf

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
moruwasa/
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
- **Signal Strength:** Strong (procurement, tender, tenders)
