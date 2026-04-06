---
institution:
  name: "Wintender"
  slug: "wintender"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "wintender.co.tz"

website:
  homepage: "https://wintender.tz/"
  tender_url: "https://portal.wintender.tz"

contact:
  email: "info@wintender.co.tz"
  phone: "0 0 448 512"

scraping:
  enabled: false
  method: "http_get"
  strategy: |
    portal.wintender.tz is a React SPA (single-page app) showing a login form. Tender content requires authentication.
    Use headless browser (Puppeteer/Playwright) or requires_javascript. After login, scrape tender listings from the dashboard.
    The page renders via JavaScript (div#root, index-e3d0ced9.js). No server-rendered tender HTML without JS.
  selectors:
    container: "#root, .tender-list, main, .content"
    tender_item: ".tender-item, .card, article, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a"
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
      - "wintender.co.tz/*.pdf"

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
      Portal requires login. Document paths unknown until authenticated scrape. Tender content loads after JS execution.

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
  facebook: "wintendertz"
  linkedin: "wintender"
  instagram: "wintender_"

notes: |
  Offering guidance to Supliers, Service Providers, and Contractors how to Apply, Win, Execute tenders.
---

# Wintender | APPLY. WIN. EXECUTE

**Category:** Commercial / Private Sector
**Website:** https://wintender.tz/
**Tender Page:** https://portal.wintender.tz
**Keywords Found:** bid, bidding, procurement, rfp, tender, tenders

## Contact Information
- Email: info@wintender.co.tz
- Phone: 0 0 448 512
- Phone: 04 119 393 8 2
- Phone: 0 0 0 48-48
- Phone: +255 736 228 228
- Phone: 0 0 0 48 48

## Scraping Instructions

**Strategy:** Scrape https://portal.wintender.tz for tender/procurement notices.
**Method:** http_get

Offering guidance to Supliers, Service Providers, and Contractors how to Apply, Win, Execute tenders.

### Tender Content Preview

> e-width, initial-scale=1.0"> <meta name="keywords" content="Apply, Win, Execute, Trade Finance, Tender, Bid, Procurement, Consultanct, Business, Perfomance Guarantee, Advance Payment, tender listing, Tender preparation, Tender listing, Market Research & Survey, Trade finance, Financial modeling,

### Known Tender URLs

- https://portal.wintender.tz
- https://www.linkedin.com/company/wintender/
- https://www.instagram.com/wintender_/
- https://www.facebook.com/wintendertz/

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
wintender/
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
- **Signal Strength:** Strong (bidding, procurement, rfp, tender, tenders)
