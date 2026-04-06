---
institution:
  name: "Ukerewe District Council"
  slug: "ukerewedc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "ukerewedc.go.tz"

website:
  homepage: "https://ukerewedc.go.tz/"
  tender_url: "https://ukerewedc.go.tz/tenders"

contact:
  phone: "01769907158046"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://ukerewedc.go.tz/tenders for government zabuni (tenders). Tenders are in a table.table.table-striped; each row has title (td:first-child), published date (td:nth-child(2)), closing date (td:nth-child(3)), and Download link (td a[href*='.pdf']). Documents at /storage/app/uploads/public/."
  selectors:
    container: ".right-sidebar-content, table.table.table-striped"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: 'td a[href$=".pdf"], td a[href*="/storage/"]'
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
      - "ukerewedc.go.tz/storage/app/uploads/public/*/*/*/*.pdf"
      - "ukerewedc.go.tz/storage/app/uploads/public/5d3/c3c/747/5d3c3c747752f527083672.pdf"
      - "ukerewedc.go.tz/storage/app/uploads/public/59a/690/7b5/59a6907b5915f803520518.pdf"
      - "ukerewedc.go.tz/storage/app/uploads/public/5c4/6b2/202/5c46b2202d27f913148329.pdf"
      - "ukerewedc.go.tz/storage/app/uploads/public/5b0/bef/6a0/5b0bef6a01769907158046.pdf"

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
      Known document paths: /storage/app/uploads/public/ (hash-based subdirs e.g. 5c4/6b2/202/). Each tender row has Download link to PDF. Table columns: Title | Published | Closing | Download.

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

# Home &#124; Ukerewe District Council

**Category:** Local Government Authority
**Website:** https://ukerewedc.go.tz/
**Tender Page:** https://ukerewedc.go.tz/tenders
**Keywords Found:** bid, manunuzi, tender, tenders, zabuni

## Contact Information
- Phone: 01769907158046
- Phone: 021-10-22 --- 
- Phone: 022-05-30
- Phone: 022-06-16
- Phone: 022-03-15 --- 

## Scraping Instructions

**Strategy:** Scrape https://ukerewedc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ome-page-title">Zabuni Zaidi Tender Name

### Known Tender URLs

- https://ukerewedc.go.tz/tenders

### Document Links Found

- https://ukerewedc.go.tz/storage/app/uploads/public/5d3/c3c/747/5d3c3c747752f527083672.pdf
- https://ukerewedc.go.tz/storage/app/uploads/public/5c4/6b2/202/5c46b2202d27f913148329.pdf
- https://ukerewedc.go.tz/storage/app/uploads/public/5b0/bef/6a0/5b0bef6a01769907158046.pdf
- https://ukerewedc.go.tz/storage/app/uploads/public/58f/9aa/b04/58f9aab04b73a617425996.pdf
- https://ukerewedc.go.tz/storage/app/uploads/public/59a/690/7b5/59a6907b5915f803520518.pdf
- https://ukerewedc.go.tz/storage/app/uploads/public/58f/f91/890/58ff91890002f307505410.pdf
- https://ukerewedc.go.tz/storage/app/uploads/public/59a/d6c/b58/59ad6cb58da65086801157.pdf

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

Known document paths: /storage/app/uploads/public/5d3/c3c/747/5d3c3c747752f527083672.pdf, /storage/app/uploads/public/59a/690/7b5/59a6907b5915f803520518.pdf, /storage/app/uploads/public/59a/d6c/b58/59ad6cb58da65086801157.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
ukerewedc/
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
