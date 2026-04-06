---
institution:
  name: "Petroleum Bulk Procurement Agency (PBPA)"
  slug: "pbpa"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "pbpa.go.tz"

website:
  homepage: "https://pbpa.go.tz/"
  tender_url: "https://pbpa.go.tz/publications/tender-results-for-supply-of-petroleum-products"

contact:
  email: "info@pbpa.go.tz"
  phone: "00756954-"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://pbpa.go.tz/publications/tender-results-for-supply-of-petroleum-products and homepage. PBPA uses custom Bootstrap layout. Documents in /uploads/announcements/ and /uploads/documents/. Tender results and announcements may be on homepage or publications pages."
  selectors:
    container: ".home-page-bodyyyy, .containerrrr, .container, main"
    tender_item: ".mb-2, .flow-hidden, .has-hover-text-primary, article, .rich-text"
    title: "h2, h3, h4, .tender-title, .text-bold"
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
      - "/uploads/announcements/"
      - "/uploads/documents/"

    url_patterns:
      - "pbpa.go.tz/uploads/announcements/*"
      - "pbpa.go.tz/uploads/documents/*"

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
      Documents use pattern /uploads/announcements/en{timestamp}-{filename}.pdf and /uploads/documents/en-{timestamp}-{filename}.pdf. Tender results page and announcements contain PDF links.

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
  facebook: "PbpaTanzania"
  twitter: "PbpaTanzania"
  instagram: "pbpa_tanzania"

notes: |
  Government Website | Government Website
---

# PBPA |     United Republic of Tanzania - Home

**Category:** Government Agency
**Website:** https://pbpa.go.tz/
**Tender Page:** https://pbpa.go.tz/uploads/documents/en-1730979432-PETRTOLEUM- BULK PROCUREMENT (AMENDMENT) REUGULATION, 2024.pdf
**Keywords Found:** bid, prequalification, procurement, supply, tender

## Contact Information
- Email: info@pbpa.go.tz
- Phone: 00756954-
- Phone: 01686700-
- Phone: +255 222 129 009

## Scraping Instructions

**Strategy:** Scrape https://pbpa.go.tz/uploads/documents/en-1730979432-PETRTOLEUM- BULK PROCUREMENT (AMENDMENT) REUGULATION, 2024.pdf for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Government Website | Government Website

### Tender Content Preview

> ons and Guidelines BPS Tender Calendars Registered Oil Marketing Companies <a class='' href= 'https://pbpa.go.tz/publications/pbpa-establi

### Known Tender URLs

- https://pbpa.go.tz/uploads/documents/en-1730979432-PETRTOLEUM- BULK PROCUREMENT (AMENDMENT) REUGULATION, 2024.pdf
- https://pbpa.go.tz/publications/tender-results-for-supply-of-petroleum-products
- https://pbpa.go.tz/uploads/documents/en-1730979629-PETROLEUM BULK PROCUREMENT SYSTEM IMPLEMENTATION MANUAL, 2024.pdf

### Document Links Found

- https://pbpa.go.tz/uploads/announcements/en1748235645-TO ALL PRE.pdf
- https://pbpa.go.tz/uploads/documents/en-1730979629-PETROLEUM BULK PROCUREMENT SYSTEM IMPLEMENTATION MANUAL, 2024.pdf
- https://pbpa.go.tz/uploads/documents/en-1700756954-PBPA-REGULATION-2017.pdf
- https://pbpa.go.tz/uploads/documents/en-1772608861-PBPA Bulletin Toleo Na. 4 Februari, 2026 (1)_compressed.pdf
- https://pbpa.go.tz/uploads/documents/en-1767777693-PBPA Bulletin Toleo la Pili Juni, 2025 (5)_compressed.pdf
- https://pbpa.go.tz/uploads/documents/en-1730979432-PETRTOLEUM- BULK PROCUREMENT (AMENDMENT) REUGULATION, 2024.pdf
- https://pbpa.go.tz/uploads/announcements/en1744215274-en-1744206990-Petroleum Sub-Sector Performance Report FY 2023-24. pdf.pdf
- https://pbpa.go.tz/uploads/documents/en-1767777566-PBPA Bulletin online-1_compressed (1).pdf
- https://pbpa.go.tz/uploads/announcements/en1711399712-sw-1701686700-The-Petroleum-Act-2015.pdf

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

Known document paths: /uploads/announcements/en1711399712-sw-1701686700-The-Petroleum-Act-2015.pdf, /uploads/documents/en-1700756954-PBPA-REGULATION-2017.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
pbpa/
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
- **Signal Strength:** Strong (prequalification, procurement, tender)
