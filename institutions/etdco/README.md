---
institution:
  name: "ETDCO"
  slug: "etdco"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "etdco.co.tz"

website:
  homepage: "https://etdco.co.tz/"
  tender_url: "https://etdco.co.tz/tenders/"

contact:
  email: "info@etdco.co.tz"
  alternate_emails:
    - "admin@etdco.co.tz"
  phone: "02-714522"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://etdco.co.tz/tenders/ for tender notices. Uses WordPress with Simple Job Board (sjb) plugin. Parse .sjb-page content, extract .jobpost items. Documents via Download Manager (wpdm) plugin."
  selectors:
    container: ".sjb-page, main, .entry-content, .elementor-section"
    tender_item: ".jobpost, .sjb-detail .list-data .jobpost-form, .elementor-widget-container"
    title: "h2, h3, h4, .job-title, .sjb-detail h1, .elementor-heading-title"
    date: ".date, .closing-date, .published, time, .jobpost-date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a.wpdm-download-link, a[download]'
    pagination: ".pagination a, a.next, .nav-links a, .sjb-pagination a" 
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
      - "etdco.co.tz/*.pdf"
      - "etdco.co.tz/wp-content/uploads/*"
      - "etdco.co.tz/?wpdmdl=*"

    known_document_paths:
      - "/wp-content/uploads/"
      - "/?wpdmdl=*"

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
      Uses WordPress Download Manager (wpdm). Documents may be at /wp-content/uploads/ or served via ?wpdmdl= ID. Check each tender detail page for wpdm-download-link elements.

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
  facebook: "profile.php"
  twitter: "etdco_tanzania"
  linkedin: "etdco-tanzania"
  instagram: "etdco_tz"

notes: |
  Organization website at etdco.co.tz. Tender keywords detected: bid, procurement, tender, tenders.
---

# ETDCO

**Category:** Commercial / Private Sector
**Website:** https://etdco.co.tz/
**Tender Page:** https://etdco.co.tz/tenders/
**Keywords Found:** bid, procurement, tender, tenders

## Contact Information
- Email: info@etdco.co.tz
- Email: admin@etdco.co.tz
- Phone: 02-714522
- Phone: 0 0 0 0 48
- Phone: 03-204011
- Phone: 02-298455
- Phone: 059-303270

## Scraping Instructions

**Strategy:** Scrape https://etdco.co.tz/tenders/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> item menu-item-type-custom menu-item-object-custom hfe-creative-menu"> Tenders <li id="menu-item-16465-173354" class="menu-item menu-item-type-custo

### Known Tender URLs

- https://etdco.co.tz/tenders/
- https://etdco.co.tz/procurement-policy/

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
etdco/
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
- **Signal Strength:** Strong (procurement, tender, tenders)
