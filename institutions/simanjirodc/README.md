---
institution:
  name: "Simanjiro District Council"
  slug: "simanjirodc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "simanjirodc.go.tz"

website:
  homepage: "https://simanjirodc.go.tz/"
  tender_url: "https://simanjirodc.go.tz/tenders"

contact:
  phone: "023
	        "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://simanjirodc.go.tz/tenders. Tenders in HTML table (table.table-striped). Columns: Jina la zabuni (title), Tarehe Ongezeka (published), Expire Date (closing), Pakua (download link). Documents at /storage/app/uploads/public/."
  selectors:
    container: ".right-sidebar-content"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: "td:last-child a, a[href*='/storage/']"
    pagination: "nav.text-center a" 
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
      - "/storage/app/uploads/public/"

    url_patterns:
      - "simanjirodc.go.tz/storage/app/uploads/public/*"

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
      Documents use path /storage/app/uploads/public/{hash}/{hash}/{hash}/{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}.pdf. Download links in last column (Pakua). October CMS / Laravel storage.

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
  facebook: "halmashauriya.simanjiro"
  twitter: "simanjirodc"
  instagram: "simanjirodistrict"

notes: |
  A default home page
---

# Home &#124; Simanjiro District Council

**Category:** Local Government Authority
**Website:** https://simanjirodc.go.tz/
**Tender Page:** https://simanjirodc.go.tz/tenders
**Keywords Found:** procurement, tender, tenders, zabuni

## Contact Information
- Phone: 023
	        
- Phone: 018-07-02
- Phone: 017-02-08
- Phone: 016-10-12 --- 
- Phone: 017-07-01 --- 

## Scraping Instructions

**Strategy:** Scrape https://simanjirodc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> e-page-title">Zabuni Zaidi Jina la zabuni

### Known Tender URLs

- https://simanjirodc.go.tz/tenders
- https://simanjirodc.go.tz/procurement-mnagement-unit

### Document Links Found

- https://simanjirodc.go.tz/storage/app/uploads/public/58d/264/3b5/58d2643b5711f577289309.pdf
- https://simanjirodc.go.tz/storage/app/uploads/public/60d/34b/fb9/60d34bfb9efd3313869679.pdf
- https://simanjirodc.go.tz/storage/app/uploads/public/5ac/35a/8ac/5ac35a8acb2d1301929476.pdf
- https://simanjirodc.go.tz/storage/app/uploads/public/59e/a52/784/59ea52784d9d8881996425.pdf
- https://simanjirodc.go.tz/storage/app/uploads/public/59f/b07/789/59fb07789482c162922565.pdf
- https://simanjirodc.go.tz/storage/app/uploads/public/59f/b01/b06/59fb01b06400a440596138.pdf

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

Known document paths: /storage/app/uploads/public/59f/b01/b06/59fb01b06400a440596138.pdf, /storage/app/uploads/public/59f/b07/789/59fb07789482c162922565.pdf, /storage/app/uploads/public/58d/264/3b5/58d2643b5711f577289309.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
simanjirodc/
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
- **Signal Strength:** Strong (procurement, tender, tenders, zabuni)
