---
institution:
  name: "Ngara District Council"
  slug: "ngaradc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "ngaradc.go.tz"

website:
  homepage: "https://ngaradc.go.tz/"
  tender_url: "https://ngaradc.go.tz/tenders"

contact:
  email: "ded@ngaradc.go.tz"
  phone: "0282226016 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Tender page uses Bootstrap table. Parse table.table.table-striped: each tr = one tender. Col1=title, Col2=published date, Col3=closing date, Col4=Download link to PDF. Documents at /storage/app/uploads/public/{hash}/."
  selectors:
    container: "table.table.table-striped"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: "td a[href*='/storage/']"
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

    known_document_paths:
      - "/storage/app/uploads/public/"

    url_patterns:
      - "ngaradc.go.tz/storage/app/uploads/public/*/*/*/*.pdf"
      - "ngaradc.go.tz/storage/app/uploads/public/*/*/*/*.doc"
      - "ngaradc.go.tz/storage/app/uploads/public/*/*/*/*.docx"

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
      October CMS. Documents at /storage/app/uploads/public/{3-char}/{3-char}/{3-char}/{hash}.pdf. Table columns: Title | Published | Closing | Download. Some rows may have .jpg (images) - filter for .pdf, .doc, .docx.

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

# Home &#124; Ngara District Council

**Category:** Local Government Authority
**Website:** https://ngaradc.go.tz/
**Tender Page:** https://ngaradc.go.tz/tenders
**Keywords Found:** manunuzi, procurement, tender, tenders, zabuni

## Contact Information
- Email: ded@ngaradc.go.tz
- Phone: 0282226016 
- Phone: 017-06-30
- Phone: 009274176003
- Phone: 018-02-07 --- 
- Phone: 017-07-04

## Scraping Instructions

**Strategy:** Scrape https://ngaradc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> "home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://ngaradc.go.tz/tenders
- https://ngaradc.go.tz/procurement

### Document Links Found

- https://ngaradc.go.tz/storage/app/uploads/public/64e/f16/dbd/64ef16dbdc3e9356869388.pdf
- https://ngaradc.go.tz/storage/app/uploads/public/652/102/d32/652102d327f3c415471138.pdf
- https://ngaradc.go.tz/storage/app/uploads/public/5d2/34b/91b/5d234b91b6baf783161313.pdf
- https://ngaradc.go.tz/storage/app/uploads/public/652/455/aa7/652455aa733e4997196139.pdf
- https://ngaradc.go.tz/storage/app/uploads/public/643/fd4/76c/643fd476cc4bc463772248.pdf
- https://ngaradc.go.tz/storage/app/uploads/public/62e/211/d7a/62e211d7a8009274176003.pdf

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

Known document paths: /storage/app/uploads/public/62e/211/d7a/62e211d7a8009274176003.pdf, /storage/app/uploads/public/64e/f16/dbd/64ef16dbdc3e9356869388.pdf, /storage/app/uploads/public/652/455/aa7/652455aa733e4997196139.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
ngaradc/
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
