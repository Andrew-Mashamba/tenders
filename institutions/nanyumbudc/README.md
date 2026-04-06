---
institution:
  name: "Nanyumbu District Council"
  slug: "nanyumbudc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "nanyumbudc.go.tz"

website:
  homepage: "https://nanyumbudc.go.tz/"
  tender_url: "https://nanyumbudc.go.tz/tenders"

contact:
  email: "info@nanyumbudc.go.tz"
  phone: "018
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /tenders page. Uses Bootstrap table (table.table.table-striped). Each row: col1=title, col2=date added (Tarehe Iliyoongezwa), col3=expire date, col4=Pakua (download) link. Documents at /storage/app/uploads/public/."
  selectors:
    container: "table.table.table-striped"
    tender_item: "table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: 'td a[href*="/storage/app/uploads/"], a[href$=".pdf"], a[target="blank"]'
    pagination: "nav.text-center a, .pagination a"
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
      - "nanyumbudc.go.tz/storage/app/uploads/public/*/*/*/*.pdf"
      - "nanyumbudc.go.tz/storage/app/uploads/public/*/*/*/*.doc"

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
      Documents at /storage/app/uploads/public/XXX/XXX/XXX/filename.pdf (hash-based path). Download link text is 'Pakua'. Table columns: Tender Name, Tarehe Iliyoongezwa, Expire Date, Download.

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
  facebook: "people"
  twitter: "nanyumbudc"
  instagram: "nanyumbudc_1"

notes: |
  A default home page
---

# Home &#124; Nanyumbu District Council

**Category:** Local Government Authority
**Website:** https://nanyumbudc.go.tz/
**Tender Page:** https://nanyumbudc.go.tz/tenders
**Keywords Found:** manunuzi, procurement, tender, tenders, zabuni

## Contact Information
- Email: info@nanyumbudc.go.tz
- Phone: 018
          
- Phone: 022-07-01 --- 
- Phone: 0232934112
- Phone: 00015942246982
- Phone: 017-08-31

## Scraping Instructions

**Strategy:** Scrape https://nanyumbudc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> Tender Zaidi <table class="table table-strip

### Known Tender URLs

- https://nanyumbudc.go.tz/tenders
- https://nanyumbudc.go.tz/procurement-management

### Document Links Found

- https://nanyumbudc.go.tz/storage/app/uploads/public/657/71a/378/65771a378f975795230893.pdf
- https://nanyumbudc.go.tz/storage/app/uploads/public/657/71a/6b8/65771a6b86e8f461375074.pdf
- https://nanyumbudc.go.tz/storage/app/uploads/public/657/712/3a3/6577123a3c167455700573.pdf
- https://nanyumbudc.go.tz/storage/app/uploads/public/657/712/9a3/6577129a3a4f2271250833.pdf
- https://nanyumbudc.go.tz/storage/app/uploads/public/657/716/4b2/6577164b2ba17823654965.pdf
- https://nanyumbudc.go.tz/storage/app/uploads/public/653/d34/a0f/653d34a0f3f2e039574063.pdf
- https://nanyumbudc.go.tz/storage/app/uploads/public/654/cc3/bcb/654cc3bcbfa9e884603629.pdf

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

Known document paths: /storage/app/uploads/public/657/712/9a3/6577129a3a4f2271250833.pdf, /storage/app/uploads/public/657/712/3a3/6577123a3c167455700573.pdf, /storage/app/uploads/public/657/71a/6b8/65771a6b86e8f461375074.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
nanyumbudc/
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
