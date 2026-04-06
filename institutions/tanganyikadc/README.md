---
institution:
  name: "Tanganyika District Council"
  slug: "tanganyikadc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "tanganyikadc.go.tz"

website:
  homepage: "https://tanganyikadc.go.tz/"
  tender_url: "https://tanganyikadc.go.tz/ugavi-na-manunuzi"

contact:
  email: "ded@tanganyikadc.go.tz"
  phone: "017-03-08"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://tanganyikadc.go.tz/ugavi-na-manunuzi for Ugavi na Manunuzi (procurement). October CMS. News items in .right-sidebar-container with links to /new/{slug}. Documents in /storage/app/uploads/public/ with hash paths."
  selectors:
    container: ".right-sidebar-content, .right-sidebar-container, .right-sidebar-wrapper"
    tender_item: ".right-sidebar-container"
    title: "h4 a, h4"
    date: "span"
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
      - "tanganyikadc.go.tz/storage/app/uploads/public/5c0/28d/df4/5c028ddf4881c226704437.pdf"
      - "tanganyikadc.go.tz/storage/app/uploads/public/66e/d26/1f3/66ed261f38ba3110041798.pdf"
      - "tanganyikadc.go.tz/storage/app/uploads/public/631/d8f/dc8/631d8fdc812af219494722.pdf"
      - "tanganyikadc.go.tz/storage/app/uploads/public/66e/d25/9de/66ed259def58f168603966.pdf"
      - "tanganyikadc.go.tz/storage/app/uploads/public/5b7/13c/45a/5b713c45a9442963672313.pdf"

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
      October CMS. Documents in /storage/app/uploads/public/{hash}/{hash}.pdf. News items link to /new/{slug} detail pages where documents may be attached.

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
  facebook: "tTanganyikaDC"
  twitter: "tTanganyikaDC"
  instagram: "tanganyika_district_council"

notes: |
  A default home page
---

# Home &#124; Tanganyika District Council

**Category:** Local Government Authority
**Website:** https://tanganyikadc.go.tz/
**Tender Page:** https://tanganyikadc.go.tz/ugavi-na-manunuzi
**Keywords Found:** bid, manunuzi, tender, tenders, zabuni

## Contact Information
- Email: ded@tanganyikadc.go.tz
- Phone: 017-03-08
- Phone: 017-03-23 --- 
- Phone: 024-09-05 --- 
- Phone: 025-03-31
- Phone: 04251685710132

## Scraping Instructions

**Strategy:** Scrape https://tanganyikadc.go.tz/ugavi-na-manunuzi for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> Tender Zaidi <table class="table table-str

### Known Tender URLs

- https://tanganyikadc.go.tz/ugavi-na-manunuzi
- https://tanganyikadc.go.tz/event/kukabidhi-mfano-wa-hundi-kwa-vijiji-8-vya-mradi-wa-hewa-ukaa
- https://tanganyikadc.go.tz/tenders

### Document Links Found

- https://tanganyikadc.go.tz/storage/app/uploads/public/66e/d25/9de/66ed259def58f168603966.pdf
- https://tanganyikadc.go.tz/storage/app/uploads/public/66e/d26/1f3/66ed261f38ba3110041798.pdf
- https://tanganyikadc.go.tz/storage/app/uploads/public/5c0/28d/df4/5c028ddf4881c226704437.pdf
- https://tanganyikadc.go.tz/storage/app/uploads/public/5b7/13c/45a/5b713c45a9442963672313.pdf
- https://tanganyikadc.go.tz/storage/app/uploads/public/631/d8f/dc8/631d8fdc812af219494722.pdf
- https://tanganyikadc.go.tz/storage/app/uploads/public/604/0f5/95c/6040f595cbeb7395959353.pdf

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

Known document paths: /storage/app/uploads/public/5c0/28d/df4/5c028ddf4881c226704437.pdf, /storage/app/uploads/public/66e/d26/1f3/66ed261f38ba3110041798.pdf, /storage/app/uploads/public/631/d8f/dc8/631d8fdc812af219494722.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tanganyikadc/
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
- **Signal Strength:** Strong (manunuzi, tender, tenders, zabuni)
