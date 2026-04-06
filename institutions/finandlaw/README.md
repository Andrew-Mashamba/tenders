---
institution:
  name: "FIN & LAW"
  slug: "finandlaw"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "finandlaw.co.tz"

website:
  homepage: "https://finandlaw.co.tz/"
  tender_url: "https://finandlaw.co.tz/procurement-and-disposal-of-assets-advisor/"

contact:
  email: "info@finandlaw.co.tz"
  phone: "058-1-768"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Procurement page is a legal advisory service description only. No tender listings, RFPs, or document links. FIN & LAW offers procurement legal advice but does not publish tenders."
  selectors:
    container: "main, .entry-content, .content"
    tender_item: "article, .tender-item"
    title: "h1, h2, .tender-title"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
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

    url_patterns:
      - "finandlaw.co.tz/*.pdf"

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
      No document links found on procurement page. Page describes legal advisory services only. Scraping disabled: no tender content.

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
  twitter: "finandlaw"
  linkedin: "fin"
  instagram: "finandlaw"

notes: |
  Fin &amp; Law is a reputable law firm in Tanzania specializing in corporate law, family disputes, and business legal services. Our experienced lawyers are dedicated to protecting your rights and providing strategic legal guidance you can trust.
---

# Home - FIN &amp; LAW

**Category:** Commercial / Private Sector
**Website:** https://finandlaw.co.tz/
**Tender Page:** https://finandlaw.co.tz/procurement-and-disposal-of-assets-advisor/
**Keywords Found:** procurement

## Contact Information
- Email: info@finandlaw.co.tz
- Phone: 058-1-768
- Phone: 024-05-21 11
- Phone: 025-11-19
- Phone: +255 22 277 3815
- Phone: 058-1-320

## Scraping Instructions

**Strategy:** Scrape https://finandlaw.co.tz/procurement-and-disposal-of-assets-advisor/ for tender/procurement notices.
**Method:** http_get

Fin &amp; Law is a reputable law firm in Tanzania specializing in corporate law, family disputes, and business legal services. Our experienced lawyers are dedicated to protecting your rights and providing strategic legal guidance you can trust.

### Tender Content Preview

> tem menu-item-type-post_type menu-item-object-page menu-item-4448"> Procurement and Disposal of Assets Advisor <li id="menu-item-4449" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-444

### Known Tender URLs

- https://finandlaw.co.tz/procurement-and-disposal-of-assets-advisor/

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
finandlaw/
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
