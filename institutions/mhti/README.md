---
institution:
  name: "Machame Health Training Institute"
  slug: "mhti"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "mhti.ac.tz"

website:
  homepage: "https://mhti.ac.tz/"
  tender_url: "https://mhti.ac.tz/procurement/"

contact:
  email: "info@mhti.ac.tz"
  alternate_emails:
    - "admission@mhti.ac.tz"
  phone: "026-03-12 03"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Scrape https://mhti.ac.tz/procurement/ (WordPress/Elementor page). Page has minimal visible content—check for embedded Elementor widgets, contact info, and any document links. Follow wp-content/uploads/ for documents."
  selectors:
    container: ".elementor-section, .elementor-widget-wrap, main, .entry-content"
    tender_item: "article, .elementor-widget-container, .row"
    title: "h2, h3, h4, .elementor-headline"
    date: ".date, .elementor-icon-list-text, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/wp-content/uploads/"]'
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
      - "/wp-content/uploads/"

    url_patterns:
      - "mhti.ac.tz/wp-content/uploads/*"
      - "mhti.ac.tz/*.pdf"

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
      WordPress site with Elementor. Procurement page at /procurement/ has minimal content (contacts, links). Documents may be in wp-content/uploads/. No tender listings found on page—may need to check subpages or linked pages.

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
  twitter: "kcmucotz"
  instagram: "machame_hti"

notes: |
  Organization website at mhti.ac.tz. Tender keywords detected: bid, procurement, rfi.
---

# Machame Health Training Institute &#8211;     .

**Category:** Educational Institution
**Website:** https://mhti.ac.tz/
**Tender Page:** https://mhti.ac.tz/procurement/
**Keywords Found:** bid, procurement, rfi

## Contact Information
- Email: info@mhti.ac.tz
- Email: admission@mhti.ac.tz
- Phone: 026-03-12 03
- Phone: +255 742 506 567
- Phone: +255 766 860 241
- Phone: 025           
- Phone: +255 621327568

## Scraping Instructions

**Strategy:** Scrape https://mhti.ac.tz/procurement/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> item menu-item-type-post_type menu-item-object-page menu-item-9435"> Procurement <a class="dropdown-ite

### Known Tender URLs

- https://mhti.ac.tz/procurement/

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
mhti/
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
- **Signal Strength:** Strong (procurement)
