---
institution:
  name: "Home - WLC"
  slug: "worldlogisticstz"
  category: "Transport / Logistics"
  status: "active"
  country: "Tanzania"
  domain: "worldlogisticstz.co.tz"

website:
  homepage: "https://worldlogisticstz.co.tz/"
  tender_url: "https://worldlogisticstz.co.tz/"

contact:
  email: "info@worldlogisticstz.co.tz"
  phone: "0617059 39"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    World Logistics Company (WLC) homepage at worldlogisticstz.co.tz. No dedicated tender page found.
    Homepage shows services (Clearing & Forwarding, Cargo Consulting, Transport). Check /category/ for news.
    No tender listings or document links visible. Keywords (eoi, rfi, rfp, rfq) may appear in blog posts — scrape main content area.
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
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

    url_patterns:
      - "worldlogisticstz.co.tz/*.pdf"

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
      Document storage paths not yet identified. Check tender detail pages for download links.

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
  Seamless Customs Clearance, Every Time Clearing &amp; Forwarding We handle all import and export procedures through Dar es Salaam Port, airports, and border ...
---

# Home - WLC

**Category:** Transport / Logistics
**Website:** https://worldlogisticstz.co.tz/
**Tender Page:** https://worldlogisticstz.co.tz/ (no dedicated procurement page)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
**Keywords Found:** eoi, rfi, rfp, rfq, supply

## Contact Information
- Email: info@worldlogisticstz.co.tz
- Phone: 0617059 39
- Phone: +255 784 271 957
- Phone: 046 424 381
- Phone: 0 0 425 402
- Phone: 00012 0 3

## Scraping Instructions

**Strategy:** Scrape https://worldlogisticstz.co.tz/ homepage and subpages (About, Services, Blog, Contact). No dedicated tender/procurement page found (Jun 2026).
**Method:** http_get

Seamless Customs Clearance, Every Time Clearing &amp; Forwarding We handle all import and export procedures through Dar es Salaam Port, airports, and border ...

### Known Tender URLs

- https://worldlogisticstz.co.tz/
- https://worldlogisticstz.co.tz/

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
worldlogisticstz/
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
- **Signal Strength:** Strong (eoi, rfp, rfq)
