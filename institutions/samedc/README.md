---
institution:
  name: "Same District Council"
  slug: "samedc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "samedc.go.tz"

website:
  homepage: "https://samedc.go.tz/"
  tender_url: "https://samedc.go.tz/tenders"

contact:
  phone: "03-1490508007"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /tenders page. Tenders in table.table.table-striped. Each tr: td[1]=title, td[2]=published, td[3]=closing, td[4]=document link (Pakua)."
  selectors:
    container: ".right-sidebar-content, table.table.table-striped"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: 'td a[href*="/storage/"], a[href$=".pdf"]'
    pagination: "a.view-all, .pagination a" 
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
      - "samedc.go.tz/storage/app/uploads/public/699/6db/a8c/6996dba8c556f455621318.pdf"
      - "samedc.go.tz/storage/app/uploads/public/688/31d/ed4/68831ded49625480866634.pdf"
      - "samedc.go.tz/storage/app/uploads/public/699/6db/06e/6996db06ef28c830135173.pdf"
      - "samedc.go.tz/storage/app/uploads/public/68f/0fa/964/68f0fa964ec0e972540423.pdf"
      - "samedc.go.tz/storage/app/uploads/public/688/33c/1ad/68833c1ad883e741149572.pdf"

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
      Documents in /storage/app/uploads/public/{hex}/{hex}/{hex}/{hash}.pdf. Download links in table column 4 with text 'Pakua'.

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

# Home &#124; Same District Council

**Category:** Local Government Authority
**Website:** https://samedc.go.tz/
**Tender Page:** https://samedc.go.tz/tenders
**Keywords Found:** manunuzi, tender, tenders, zabuni

## Contact Information
- Phone: 03-1490508007
- Phone: 025
          
- Phone: 0602666532

## Scraping Instructions

**Strategy:** Scrape https://samedc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ="home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://samedc.go.tz/tenders

### Document Links Found

- https://samedc.go.tz/storage/app/uploads/public/688/33c/1ad/68833c1ad883e741149572.pdf
- https://samedc.go.tz/storage/app/uploads/public/58d/65f/ff3/58d65fff3e68d768619790.pdf
- https://samedc.go.tz/storage/app/uploads/public/699/6db/06e/6996db06ef28c830135173.pdf
- https://samedc.go.tz/storage/app/uploads/public/688/31d/ed4/68831ded49625480866634.pdf
- https://samedc.go.tz/storage/app/uploads/public/68f/0fa/964/68f0fa964ec0e972540423.pdf
- https://samedc.go.tz/storage/app/uploads/public/699/6db/a8c/6996dba8c556f455621318.pdf

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

Known document paths: /storage/app/uploads/public/699/6db/a8c/6996dba8c556f455621318.pdf, /storage/app/uploads/public/688/31d/ed4/68831ded49625480866634.pdf, /storage/app/uploads/public/699/6db/06e/6996db06ef28c830135173.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
samedc/
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
