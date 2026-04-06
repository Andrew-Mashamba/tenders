---
institution:
  name: "Kijana Jasiri Resilience Organization"
  slug: "kjro"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "kjro.or.tz"

website:
  homepage: "https://kjro.or.tz/"
  tender_url: "https://kjro.or.tz/"

contact:
  email: "info@kjro.or.tz"
  phone: "07 352 256 352"

scraping:
  enabled: true
  method: "http_get"
  strategy: "WordPress/Elementor NGO site. No dedicated tender page. Homepage has team (Procurement Officer), one PDF at /wp-content/uploads/2026/01/. Scrape main content and elementor-widget for document links. Tenders may be posted occasionally."
  selectors:
    container: ".elementor-widget-wrap, main, .entry-content, .elementor-section"
    tender_item: ".elementor-element, article, .elementor-widget-text-editor"
    title: "h2, h3, h4, .elementor-heading-title"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href*="/wp-content/uploads/"]'
    pagination: ".pagination a, a.next" 
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
      - "kjro.or.tz/wp-content/uploads/*/*/*.pdf"

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
      WordPress uploads at /wp-content/uploads/{year}/{month}/. Current PDF is annual report, not tender. Has Procurement Officer; check for future tender posts.

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
  facebook: "p"
  linkedin: "kjro"
  instagram: "kijana_jasiri_resilience_org"

notes: |
  Kijana Jasiri Resilience Organization A resourceful and resilient community. Dr. Marcelina Director &amp; Founder, KJRO WELCOME Welcome to Kijana Jasiri Resilience
---

# HOME -

**Category:** NGO / Non-Profit Organization
**Website:** https://kjro.or.tz/
**Tender Page:** https://kjro.or.tz/
**Keywords Found:** bid, procurement

## Contact Information
- Email: info@kjro.or.tz
- Phone: 07 352 256 352
- Phone: 05 400 256 400
- Phone: 0 0 0 48-48
- Phone: 0 0 0-48-48
- Phone: 063 0 0 0 0-29

## Scraping Instructions

**Strategy:** Scrape https://kjro.or.tz/ for tender/procurement notices.
**Method:** http_get

Kijana Jasiri Resilience Organization A resourceful and resilient community. Dr. Marcelina Director &amp; Founder, KJRO WELCOME Welcome to Kijana Jasiri Resilience

### Tender Content Preview

> or-image-box-title">Kester Peter Administrator &amp; Procurement Officer, KJRO <div class="elementor-element elementor-element-efb1d1e elementor-widget elementor-widget-text-editor" data-id="efb1d1e" data-element

### Document Links Found

- https://kjro.or.tz/wp-content/uploads/2026/01/End-of-year-2025-KJRO.pdf

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

Known document paths: /wp-content/uploads/2026/01/End-of-year-2025-KJRO.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
kjro/
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
- **Signal Strength:** Strong (procurement)
