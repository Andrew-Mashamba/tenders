---
institution:
  name: "Home &#124; Tanga Region"
  slug: "tanga"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "tanga.go.tz"

website:
  homepage: "https://tanga.go.tz/"
  tender_url: "https://tanga.go.tz/procurements"

contact:
  email: "ras.tanga@tamisemi.go.tz"
  phone: "019-12-31"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://tanga.go.tz/procurements for government procurement (Manunuzi). October CMS. Matangazo (announcements) and Habari mpya (news) sections. Documents in /storage/app/uploads/public/ with hash paths (e.g. /5ea/00a/2de/)."
  selectors:
    container: "#main-menu, .container, .row, .col-md-12, .banner"
    tender_item: ".news-item, article, .col-md-12 h4, .habari-mpya a"
    title: "h4 a, h2, h3, .tender-title"
    date: ".date, .published, time, small"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/storage/app/uploads/public/"]'
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
      - "tanga.go.tz/storage/app/uploads/public/5ea/00a/2de/5ea00a2de2345413590241.pdf"
      - "tanga.go.tz/storage/app/uploads/public/654/3b1/9a8/6543b19a82ee8157228485.pdf"
      - "tanga.go.tz/storage/app/uploads/public/681/e22/ebc/681e22ebc1800959371316.pdf"
      - "tanga.go.tz/storage/app/uploads/public/5ea/00b/31e/5ea00b31e5295393896302.pdf"

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

    known_document_paths:
      - "/storage/app/uploads/public/"
    document_notes: |
      October CMS. Documents in /storage/app/uploads/public/{hash}/{hash}.pdf (e.g. 5ea/00a/2de/5ea00a2de2345413590241.pdf). Matangazo and Habari mpya sections may contain tender announcements.

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
  A default home page
---

# Home &#124; Tanga Region

**Category:** Government Agency
**Website:** https://tanga.go.tz/
**Tender Page:** https://tanga.go.tz/procurements
**Keywords Found:** bid, manunuzi, procurement, tender, tenders, zabuni

## Contact Information
- Email: ras.tanga@tamisemi.go.tz
- Phone: 019-12-31
- Phone: 00959371316
- Phone: 027 2642421 
- Phone: 019-01-01 --- 

## Scraping Instructions

**Strategy:** Scrape https://tanga.go.tz/procurements for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> s="home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://tanga.go.tz/procurements
- https://tanga.go.tz/tenders

### Document Links Found

- https://tanga.go.tz/storage/app/uploads/public/681/e22/ebc/681e22ebc1800959371316.pdf
- https://tanga.go.tz/storage/app/uploads/public/5ea/00a/2de/5ea00a2de2345413590241.pdf
- https://tanga.go.tz/storage/app/uploads/public/654/3b1/9a8/6543b19a82ee8157228485.pdf
- https://tanga.go.tz/storage/app/uploads/public/5ea/00b/31e/5ea00b31e5295393896302.pdf

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

Known document paths: /storage/app/uploads/public/5ea/00a/2de/5ea00a2de2345413590241.pdf, /storage/app/uploads/public/654/3b1/9a8/6543b19a82ee8157228485.pdf, /storage/app/uploads/public/681/e22/ebc/681e22ebc1800959371316.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tanga/
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
- **Signal Strength:** Strong (manunuzi, procurement, tender, tenders, zabuni)
