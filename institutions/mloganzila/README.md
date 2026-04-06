---
institution:
  name: "Muhimbili National Hospital - Mloganzila"
  slug: "mloganzila"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "mloganzila.or.tz"

website:
  homepage: "https://www.mloganzila.or.tz/"
  tender_url: "https://www.mloganzila.or.tz/tenders/"

contact:
  email: "info@mloganzila.or.tz"
  phone: "04 846 713 829"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.mloganzila.or.tz/tenders/ for tender notices. WordPress/Elementor site. Tender content in page body with 'Download Document Here'. Extract document links from elementor-widget-text-editor and .elementor-widget-container areas."
  selectors:
    container: ".elementor-widget-container, .elementor-element, main, .entry-content, .page-content"
    tender_item: ".elementor-icon-list-item, .elementor-widget-text-editor a, .elementor-element"
    title: "h2, h3, h4, .elementor-heading-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download], a[href*="wp-content/uploads"]'
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
      - "/wp-content/uploads/"

    url_patterns:
      - "mloganzila.or.tz/wp-content/uploads/*.pdf"
      - "mloganzila.or.tz/wp-content/uploads/*.docx"

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
      WordPress site. Documents stored under /wp-content/uploads/. Tenders page has 'Download Document Here' with tender notices. Check elementor-icon-list and text-editor widgets for document links.

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
  facebook: "Mloganzila"
  instagram: "muhimbili_mloganzila"

notes: |
  Muhimbili National Hospital - Mloganzila is a 608-bed, hospital in Dar es Salaam,Tanzania. It is the National referal hospital.
---

# Home - Muhimbili National Hospital - Mloganzila

**Category:** NGO / Non-Profit Organization
**Website:** https://www.mloganzila.or.tz/
**Tender Page:** https://www.mloganzila.or.tz/tenders/
**Keywords Found:** rfi, tender, tenders

## Contact Information
- Email: info@mloganzila.or.tz
- Phone: 04 846 713 829
- Phone: 08 454 696 446
- Phone: 0 0 256 512
- Phone: 08 187 708 171
- Phone: 00 288 817 288

## Scraping Instructions

**Strategy:** Scrape https://www.mloganzila.or.tz/tenders/ for tender/procurement notices.
**Method:** http_get

Muhimbili National Hospital - Mloganzila is a 608-bed, hospital in Dar es Salaam,Tanzania. It is the National referal hospital.

### Tender Content Preview

> /li> <span class="elementor-icon-list

### Known Tender URLs

- https://www.mloganzila.or.tz/tenders/

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
mloganzila/
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
