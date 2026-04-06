---
institution:
  name: "Tanzania Commission for AIDS (TACAIDS)"
  slug: "tacaids"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "tacaids.go.tz"

website:
  homepage: "https://tacaids.go.tz/"
  tender_url: "https://tacaids.go.tz/pages/tender"

contact:
  email: "info@tacaids.go.tz"
  phone: "0 0 2000 128"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Tender page at /pages/tender. Page states "This page will be used to advertise tenders from TACAIDS".
    Bootstrap + DataTables. Check for table.tender, .col-md-12 content, card/row structures.
    Documents likely at /uploads/ or /documents/. Follow document links from tender rows.
  selectors:
    container: ".col-md-12, .container, main, .content"
    tender_item: "tr, .card, .list-inline-item, .row"
    title: "h2, h3, h4, .title, a, td"
    date: ".date, .published, time, td"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/uploads/"], a[href*="/documents/"]'
    pagination: ".pagination a, a.next, .page-link" 
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
      - "/uploads/"
      - "/documents/"
    url_patterns:
      - "tacaids.go.tz/uploads/*"
      - "tacaids.go.tz/documents/*"

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
      /uploads/ for news images; /documents/ for reports, speeches. Tender docs may use either.
      Page uses DataTables; content may load dynamically. Check for table tbody tr rows.

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
  facebook: "hqtacaids"
  twitter: "tacaidsinfo"
  instagram: "tacaidsinfo"

notes: |
  Tanzania Commission for AIDS (TACAIDS) | Tume ya Kudhibiti UKIMWI Tanzania
---

# TACAIDS |   Home

**Category:** Government Agency
**Website:** https://tacaids.go.tz/
**Tender Page:** https://tacaids.go.tz/pages/tender
**Keywords Found:** tender

## Contact Information
- Email: info@tacaids.go.tz
- Phone: 0 0 2000 128
- Phone: 066980166045
- Phone: 066439605195
- Phone: 026 2190600
- Phone: 030
         

## Scraping Instructions

**Strategy:** Scrape https://tacaids.go.tz/pages/tender for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Tanzania Commission for AIDS (TACAIDS) | Tume ya Kudhibiti UKIMWI Tanzania

### Tender Content Preview

> .go.tz'>ess Tender <div class="col-md-12 m

### Known Tender URLs

- https://tacaids.go.tz/pages/tender

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
tacaids/
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
- **Signal Strength:** Strong (tender)
