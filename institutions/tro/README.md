---
institution:
  name: "Office of the Registrar of Tanzania (TRO)"
  slug: "tro"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "tro.go.tz"

website:
  homepage: "https://tro.go.tz/"
  tender_url: "https://nest.go.tz/tenders/published-tenders"

contact:
  email: "info@tro.go.tz"
  phone: "0 0 500 150"

scraping:
  enabled: true
  method: "http_get"
  strategy: "TRO uses NeST (National e-Procurement System) at nest.go.tz. Angular SPA - content loads via JS; curl returns shell HTML only. Requires headless browser for scraping. No public REST API found. Tenders must be searched on NeST by procuring entity."
  selectors:
    container: "app-root, .mat-typography"
    tender_item: "app-tender-list, .tender-row, .mat-row"
    title: ".tender-title, .mat-cell"
    date: ".tender-date, .mat-cell"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href*="download"]'
    pagination: ".mat-paginator, .pagination"
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

    known_document_paths:
      - "/tenders/"
    url_patterns:
      - "nest.go.tz/tenders/*"
      - "nest.go.tz/*.pdf"

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
      NeST is Angular SPA. Requires JavaScript execution. Tenders at nest.go.tz/tenders/published-tenders. Documents may require login. TRO (tro.go.tz) links to NeST for tenders.

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
  facebook: "ofisiyamsajilihazina"
  twitter: "MsajiliHazina"
  instagram: "ofisi_ya_msajili_wa_hazina"

notes: |
  Government Website | Tovuti ya Serikali
---

# OMH |     Jamhuri ya Muungano wa Tanzania - MWANZO

**Category:** Government Agency
**Website:** https://tro.go.tz/
**Tender Page:** https://nest.go.tz/tenders/published-tenders
**Keywords Found:** tender, tenders

## Contact Information
- Email: info@tro.go.tz
- Phone: 0 0 500 150
- Phone: 0 0 2200 120
- Phone: 0000000000
- Phone: 009 - 2016
- Phone: 00
           

## Scraping Instructions

**Strategy:** Scrape https://nest.go.tz/tenders/published-tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Government Website | Tovuti ya Serikali

### Tender Content Preview

> ANREP Tender Staff Mail

### Known Tender URLs

- https://nest.go.tz/tenders/published-tenders

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
tro/
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
