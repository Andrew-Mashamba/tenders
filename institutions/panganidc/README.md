---
institution:
  name: "Pangani District Council"
  slug: "panganidc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "panganidc.go.tz"

website:
  homepage: "https://panganidc.go.tz/"
  tender_url: "https://panganidc.go.tz/advertisement/tangazo-la-zabuni-2"

contact:
  email: "ded@panganidc.go.tz"
  phone: "015-06-22 --- "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://panganidc.go.tz/advertisement/tangazo-la-zabuni-2. Pangani District Council - Tangazo la zabuni page. Main content in .right-sidebar-content; PDF links in sidebar and publications. Use -k for SSL if needed."
  selectors:
    container: ".right-sidebar-content, .left-sidebar-wrapper"
    tender_item: ".article-head, .right-sidebar-container, ul li"
    title: ".page-title, h1, h2"
    date: ".article-head .date, .date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: ""
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
      - "panganidc.go.tz/storage/app/uploads/public/*.pdf"
      - "gwf.egatest.go.tz/panganidc/storage/app/uploads/public/*.pdf"

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
      PDFs in /storage/app/uploads/public/ (hash-based subpaths). Some links use gwf.egatest.go.tz/panganidc/ mirror.

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
  facebook: "Pangani-District-Council-260553657466128"
  instagram: "panganidistrictcouncil"

notes: |
  A default home page
---

# Home &#124; Pangani District Council

**Category:** Local Government Authority
**Website:** https://panganidc.go.tz/
**Tender Page:** https://panganidc.go.tz/advertisement/tangazo-la-zabuni-2
**Keywords Found:** manunuzi, procurement, supply, tender, tenders, zabuni

## Contact Information
- Email: ded@panganidc.go.tz
- Phone: 015-06-22 --- 
- Phone: 016-11-01 --- 
- Phone: 0553657466128
- Phone: 017-10-01
- Phone: 09011778346518

## Scraping Instructions

**Strategy:** Scrape https://panganidc.go.tz/advertisement/tangazo-la-zabuni-2 for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ome-page-title">Zabuni Zaidi Jina la zabuni

### Known Tender URLs

- https://panganidc.go.tz/advertisement/tangazo-la-zabuni-2
- https://panganidc.go.tz/tenders
- https://panganidc.go.tz/advertisement/tangazo-la-zabuni
- https://panganidc.go.tz/procurement-and-supply

### Document Links Found

- https://panganidc.go.tz/storage/app/uploads/public/67e/e21/ae0/67ee21ae0f681462138342.pdf
- https://panganidc.go.tz/storage/app/uploads/public/682/18b/7b5/68218b7b57afd306693820.pdf
- http://gwf.egatest.go.tz/panganidc/storage/app/uploads/public/58d/522/190/58d52219076f3212065623.pdf
- http://panganidc.go.tz/storage/app/uploads/public/5ac/4ab/c4e/5ac4abc4e2543142259599.pdf

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

Known document paths: /storage/app/uploads/public/682/18b/7b5/68218b7b57afd306693820.pdf, /storage/app/uploads/public/5ac/4ab/c4e/5ac4abc4e2543142259599.pdf, /storage/app/uploads/public/58d/522/190/58d52219076f3212065623.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
panganidc/
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

- **Last Checked:** 15 March 2026
- **Active Tenders:** 0
- **Signal Strength:** Strong (manunuzi, procurement, tender, tenders, zabuni)
- **Note:** Tangazo la zabuni page links to Mwongozo wa Tehama and Ratiba ya Vikao (not tender docs)
