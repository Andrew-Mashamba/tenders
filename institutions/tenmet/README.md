---
institution:
  name: "TEN/MET Education Network"
  slug: "tenmet"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tenmet.or.tz"

website:
  homepage: "https://tenmet.or.tz/"
  tender_url: "https://tenmet.or.tz/tenders.html"

contact:
  email: "info@tenmet.or.tz"
  phone: "025-12-15"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://tenmet.or.tz/tenders.html. Tender board has sidebar (.tender-list) with .tender-item buttons. Detail panel and #tenderDownload link are populated by JavaScript when tender is selected. Use headless browser to click each .tender-item and extract from #tenderDetail, #tenderDownload."
  selectors:
    container: ".tender-board, .tender-board-layout"
    tender_item: ".tender-item, button.tender-item"
    title: ".tender-item-title"
    date: ".tender-meta-deadline"
    document_link: "#tenderDownload, a.tender-download"
    pagination: ""
  schedule: "daily"

  anti_bot:
    requires_javascript: true
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
      - "tenmet.or.tz/*.pdf"

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
      Document URL is in #tenderDownload href, populated by JS when user selects a tender from sidebar. Tender content in #tenderDetail (hidden until selection). No pagination - all tenders on single page.

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
  facebook: "share"
  linkedin: "tenmet"
  instagram: "tenmet"

notes: |
  Organization website at tenmet.or.tz. Tender keywords detected: tender, tenders.
---

# TEN/MET Education Network

**Category:** NGO / Non-Profit Organization
**Website:** https://tenmet.or.tz/
**Tender Page:** https://tenmet.or.tz/tenders.html
**Keywords Found:** tender, tenders

## Contact Information
- Email: info@tenmet.or.tz
- Phone: 025-12-15
- Phone: +255 022 277 5324
- Phone: 026-01-28 22
- Phone: +255 748 137 089
- Phone: +255744760112

## Scraping Instructions

**Strategy:** Scrape https://tenmet.or.tz/tenders.html for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ass="dropdown-menu"> Jobs Tenders Contact Us

### Known Tender URLs

- https://tenmet.or.tz/tenders.html

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
tenmet/
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

- **Last Checked:** 10 June 2026
- **Active Tenders:** 1 (TENMET-2026-003 ICT equipment; job postings and expired tenders excluded)
- **Signal Strength:** Strong (tender, tenders)
