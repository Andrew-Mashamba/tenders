---
institution:
  name: "Beach.co.tz"
  slug: "beach"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "beach.co.tz"

website:
  homepage: "https://www.beach.co.tz/"
  tender_url: "https://www.beach.co.tz/"

contact:
  email: "info@beach.co.tz"
  phone: "0204472605346"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Beach.co.tz is a watersports/kayak shop. No tender listings; 'procurement' keywords refer to product sales. Page uses WordPress (Divi) with .et_pb_column product cards."
  selectors:
    container: "main, .et_pb_section, .entry-content"
    tender_item: ".et_pb_column, .et_pb_module"
    title: "h2, h3, h4, .et_pb_module_title"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href*="wp-content/uploads"]'
    pagination: null 
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
      - "beach.co.tz/wp-content/uploads/*.pdf"

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
      No tender content. Site has sales brochure at /wp-content/uploads/2023/02/Beach.co_.tz-Sales-Brochure-2023.pdf. Disabled 2026-03-15.

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
  Organization website at beach.co.tz. Tender keywords detected: procurement, rfi, rfq.
---

# Home - Beach.co.tz

**Category:** Commercial / Private Sector
**Website:** https://www.beach.co.tz/
**Tender Page:** https://www.beach.co.tz/
**Keywords Found:** procurement, rfi, rfq

## Contact Information
- Email: info@beach.co.tz
- Phone: 0204472605346
- Phone: 0196078431
- Phone: 05882353 0
- Phone: 01960784314
- Phone: 039215686275 1

## Scraping Instructions

**Strategy:** Scrape https://www.beach.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> eight: bold;">from 1,000,000 learn more <div class="et_pb_column et_pb_column_4_4 et_pb_column_6 et_pb_css_mix_blend

### Document Links Found

- http://www.beach.co.tz/wp-content/uploads/2023/02/Beach.co_.tz-Sales-Brochure-2023.pdf
- https://www.beach.co.tz/wp-content/uploads/2023/02/Beach.co_.tz-Sales-Brochure-2023.pdf

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

Known document paths: /wp-content/uploads/2023/02/Beach.co_.tz-Sales-Brochure-2023.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
beach/
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
- **Signal Strength:** Strong (procurement, rfq)
