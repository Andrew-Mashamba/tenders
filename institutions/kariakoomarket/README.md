---
institution:
  name: "Shirika la Masoko ya Kariakoo (Kariakoo Market)"
  slug: "kariakoomarket"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "kariakoomarket.co.tz"

website:
  homepage: "https://kariakoomarket.co.tz/"
  tender_url: "https://kariakoomarket.co.tz/procurement-and-supply"

contact:
  phone: "019-06-01 --- "

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    OctoberCMS-style procurement page. As of 2026-06-10, kariakoomarket.co.tz redirects (301) to
    https://www.buwssa.go.tz/ — domain appears hijacked or misconfigured. Historically,
    /procurement-and-supply had zabuni notices with documents at /storage/app/uploads/public/{hash}/.
    Retry periodically; verify redirect chain before scraping.
  selectors:
    container: "table.table-striped, .right-sidebar-content, .home-page-title"
    tender_item: "table.table-striped tbody tr, .ads-listing li"
    title: "td:first-child, h4, a"
    date: "td:nth-child(2), td:nth-child(3), span"
    document_link: 'a[href*="/storage/app/uploads/"][href$=".pdf"], a[target="blank"]'
    pagination: "nav.text-center a, .pagination a, a.view-all" 
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
      - "kariakoomarket.co.tz/storage/app/uploads/public/*/*/*.pdf"

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
      Documents at /storage/app/uploads/public/{hash}/{hash}/{hash}/. Known paths: 68d/314/be9/,
      68d/312/4c1/, 679/d07/af4/, 679/d0d/41b/, 679/d0d/73a/. Site timed out during analysis.

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

# Home &#124; SHIRIKA LA MASOKO YA KARIAKOO

**Category:** Commercial / Private Sector
**Website:** https://kariakoomarket.co.tz/
**Tender Page:** https://kariakoomarket.co.tz/procurement-and-supply
**Keywords Found:** manunuzi, procurement, supply, tender, tenders, zabuni

## Contact Information
- Phone: 019-06-01 --- 
- Phone: 01260053248
- Phone: 0418931923
- Phone: 024-06-30
- Phone: 050-1667811170

## Scraping Instructions

**Strategy:** Scrape https://kariakoomarket.co.tz/procurement-and-supply for tender/procurement notices.
**Method:** http_get

A default home page

### Tender Content Preview

> age-title">Zabuni Zaidi Tender Name

### Known Tender URLs

- https://kariakoomarket.co.tz/procurement-and-supply
- https://kariakoomarket.co.tz/tenders

### Document Links Found

- https://kariakoomarket.co.tz/storage/app/uploads/public/679/d07/af4/679d07af45d01260053248.pdf
- https://kariakoomarket.co.tz/storage/app/uploads/public/68d/312/4c1/68d3124c130a9221574591.pdf
- https://kariakoomarket.co.tz/storage/app/uploads/public/679/d0d/73a/679d0d73a93ed185938062.pdf
- https://kariakoomarket.co.tz/storage/app/uploads/public/679/d0d/41b/679d0d41bd5f1319375119.pdf
- https://kariakoomarket.co.tz/storage/app/uploads/public/68d/314/be9/68d314be92370418931923.pdf

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

Known document paths: /storage/app/uploads/public/68d/314/be9/68d314be92370418931923.pdf, /storage/app/uploads/public/68d/312/4c1/68d3124c130a9221574591.pdf, /storage/app/uploads/public/679/d07/af4/679d07af45d01260053248.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
kariakoomarket/
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
