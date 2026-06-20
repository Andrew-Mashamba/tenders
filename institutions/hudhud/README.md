---
institution:
  name: "HUD HUD COMPANY LTD"
  slug: "hudhud"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "hudhud.co.tz"

website:
  homepage: "https://hudhud.co.tz/"
  tender_url: "https://hudhud.co.tz/"

contact:
  email: "info@hudhud.co.tz"
  phone: "+255784418341"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Laravel/Livewire site. IT services company (software, consulting, hardware procurement). No dedicated tender page. Homepage content loaded via wire:snapshot. Scrape services/products pages for procurement-related links. Check /services for Hardware Procurement section."
  selectors:
    container: ".container, main, .pq-menu-contain, .banner"
    tender_item: ".pq-menu-contain li a, .service-content, .pq-button-block"
    title: "h1, h2, h3, h4, .elementor-heading-title, h6"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/public/storage/"]'
    pagination: ""
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
      - "/public/storage"

    url_patterns:
      - "hudhud.co.tz/public/storage/*"
      - "hudhud.co.tz/*.pdf"

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
      Livewire site—content may require JS. Documents in /public/storage/. Hardware Procurement section under Services. No formal tender listing; IT services company. May post RFPs via contact or separate page.

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
  Organization website at hudhud.co.tz. Tender keywords detected: procurement, supply.
---

# Home

**Category:** Commercial / Private Sector
**Website:** https://hudhud.co.tz/
**Tender Page:** https://hudhud.co.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Email: info@hudhud.co.tz
- Phone: +255784418341
- Phone: 045497 100
- Phone: 00
           

## Scraping Instructions

**Strategy:** Scrape https://hudhud.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ="service-content"> Hardware Procurement We supply Laptops, Desktops, Workstations/Servers, Networking Equipment, Storag

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
hudhud/
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

- **Last Checked:** 10 June 2026
- **Active Tenders:** 0 (IT vendor; Hardware Procurement is a service, not an open tender)
- **Signal Strength:** None (no tender listings)
