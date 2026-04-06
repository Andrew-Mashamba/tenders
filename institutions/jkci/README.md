---
institution:
  name: "Jakaya Kikwete Cardiac Institute"
  slug: "jkci"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "jkci.or.tz"

website:
  homepage: "https://jkci.or.tz/"
  tender_url: "https://jkci.or.tz/"

contact:
  email: "info@jkci.or.tz"
  phone: "026
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    JKCI homepage shows News & Events. No dedicated tender page. Check Procurement Management Unit
    at /directorates/9e076133-1c3c-4240-bb28-7af39450bba1 for procurement notices.
    Scrape .tg-events for news items; follow links to /news-and-event/{uuid} for detail pages.
    Uses Livewire (server-rendered HTML, no SPA). Documents may appear in news/event detail pages.
  selectors:
    container: "#tg-content, .tg-events, .tg-sectionspace"
    tender_item: "article.tg-themepost.tg-eventpost, .tg-eventpost"
    title: ".tg-titledescription h1, .tg-eventpost h3, h4"
    date: "time, .tg-postdate, span"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a, a[href*=\"all-news\"]"
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
      - "/storage/sliders/"
      - "/storage/director_statements/"

    url_patterns:
      - "jkci.or.tz/storage/*.pdf"
      - "jkci.or.tz/*.pdf"

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
      Uses /storage/ for images and documents. Tender/procurement notices may appear in News & Events
      or under Procurement Management Unit directorate. Follow news-and-event links for full content.

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
  instagram: "taasisiyamoyo_jkci"

notes: |
  JKCI
---

# Home-JKCI

**Category:** NGO / Non-Profit Organization
**Website:** https://jkci.or.tz/
**Tender Page:** https://jkci.or.tz/
**Keywords Found:** bid, procurement

## Contact Information
- Email: info@jkci.or.tz
- Phone: 026
          
- Phone: 08-7332-4
- Phone: 0466218913

## Scraping Instructions

**Strategy:** Scrape https://jkci.or.tz/ for tender/procurement notices.
**Method:** http_get

JKCI

### Tender Content Preview

> a class="dropdown-item" href="https://jkci.or.tz/directorates/9e076133-1c3c-4240-bb28-7af39450bba1">Procurement Management Unit Clinic

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
jkci/
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
