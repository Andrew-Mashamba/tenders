---
institution:
  name: "Maendeleo Bank PLC"
  slug: "maendeleobank"
  category: "Bank"
  status: "active"
  country: "Tanzania"
  domain: "maendeleobank.co.tz"

website:
  homepage: "https://maendeleobank.co.tz/"
  tender_url: "https://maendeleobank.co.tz/index.php/tender/"

contact:
  email: "Info@maendeleobank.co.tz"
  phone: "0 842 767 846 7"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape tender page at https://maendeleobank.co.tz/index.php/tender/. Uses WordPress with Elementor and Tablesome plugin — tender data may load via JS. Parse .tablesome or .tablepress table if present; otherwise consider Tablesome REST API at /wp-json/tablesome/v1/tables/."
  selectors:
    container: ".elementor-widget-theme-post-content, .entry-content, .tablesome, table.tablepress, main"
    tender_item: "table.tablesome tbody tr, table.tablepress tbody tr"
    title: "td:first-child, .column-1, a"
    date: "td:nth-child(2), .column-2, .date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/wp-content/uploads/"]'
    pagination: ".tablesome-pagination a, .pagination a, a.next"
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
      - "/wp-content/uploads/"

    url_patterns:
      - "maendeleobank.co.tz/wp-content/uploads/*.pdf"
      - "maendeleobank.co.tz/index.php/wp-content/uploads/*"

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
      Documents stored under /wp-content/uploads/. Tablesome/Tablepress tables may contain document links. Tender data loads dynamically — consider headless browser if static HTML has no table content.

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
  facebook: "maendeleobankplctz"
  twitter: "Maendeleobanktz"
  instagram: "maendeleobankplc"

notes: |
  Organization website at maendeleobank.co.tz. Tender keywords detected: rfi, tender.
---

# Maendeleo Bank PLc

**Category:** Bank
**Website:** https://maendeleobank.co.tz/
**Tender Page:** https://maendeleobank.co.tz/index.php/tender/
**Keywords Found:** rfi, tender

## Contact Information
- Email: Info@maendeleobank.co.tz
- Phone: 0 842 767 846 7
- Phone: 03937007874
- Phone: 025						
- Phone: 04 958 771
- Phone: 0 196 150 212 1

## Scraping Instructions

**Strategy:** Scrape https://maendeleobank.co.tz/index.php/tender/ for banking tender notices and EOIs. Banks post frequently.
**Method:** http_get



### Tender Content Preview

> or-icon-list-item elementor-inline-item"> Tender<

### Known Tender URLs

- https://maendeleobank.co.tz/index.php/tender/

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
maendeleobank/
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
