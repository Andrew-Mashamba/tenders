---
institution:
  name: "FINCA Tanzania"
  slug: "finca"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "finca.co.tz"

website:
  homepage: "https://finca.co.tz/"
  tender_url: "https://finca.co.tz/tenders/"

contact:
  phone: "+255 755 980 350"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://finca.co.tz/tenders/ — each tender is a fusion-builder-nested-column with h6 title, date range, and 'See More' link to document. Extract title, date range, and document URL from each item."
  selectors:
    container: ".fusion-fullwidth.fusion-builder-row-5, main#content, .fusion-builder-row"
    tender_item: ".fusion-layout-column.fusion_builder_column_inner.fusion-column-has-shadow, .fusion-column-wrapper.fusion-column-has-shadow"
    title: "h6, .fusion-title"
    date: ".fusion-text, p, div"
    document_link: 'a[href*="wp-content/uploads"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: null
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
      - "/wp-content/uploads/sites/13/"
    url_patterns:
      - "finca.co.tz/wp-content/uploads/sites/13/*.pdf"
      - "finca.co.tz/wp-content/uploads/sites/13/*.doc"
      - "finca.co.tz/wp-content/uploads/sites/13/*.docx"

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
      Documents in /wp-content/uploads/sites/13/{year}/{month}/. Each tender has a 'See More' link to the RFP document (DOCX/PDF). Date format: DD/MM/YYYY – DD/MM/YYYY.

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
  facebook: "FINCAMicrofinanceBankTz"
  twitter: "FINCATz"
  linkedin: "finca-microfinance-bank-tz"
  instagram: "fincatz"

notes: |
  FINCA Tanzania
---

# FINCA Tanzania

**Category:** Commercial / Private Sector
**Website:** https://finca.co.tz/
**Tender Page:** https://finca.co.tz/tenders/
**Keywords Found:** rfi, tender, tenders

## Contact Information
- Phone: +255 755 980 350
- Phone: +255222212200
- Phone: +2550755980350

## Scraping Instructions

**Strategy:** Scrape https://finca.co.tz/tenders/ for tender/procurement notices.
**Method:** http_get

FINCA Tanzania

### Tender Content Preview

> ain-background-active awb-menu__main-background-active_center"> Tenders </

### Known Tender URLs

- https://finca.co.tz/tenders/

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
finca/
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
