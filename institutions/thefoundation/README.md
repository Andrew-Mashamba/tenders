---
institution:
  name: "Foundation For Civil Society (FCS)"
  slug: "thefoundation"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "thefoundation.or.tz"

website:
  homepage: "https://www.thefoundation.or.tz/"
  tender_url: "https://www.thefoundation.or.tz/news-media/tenders"

contact:
  phone: "04-104 56 58-2"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.thefoundation.or.tz/news-media/tenders. Webflow site. Tenders in .tender-cl list. Each .tender-ci links to /tenders/{slug}. Follow detail pages for documents (PDFs on cdn.prod.website-files.com)."
  selectors:
    container: ".press-collection, .tender-clw, .tender-cl"
    tender_item: ".tender-ci, .tender-ci.w-dyn-item"
    title: ".event_item-title"
    date: ".event_top-bottom .text-size-regular"
    document_link: 'a[href$=".pdf"], a[href*="cdn.prod.website-files.com"]'
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
      - "cdn.prod.website-files.com/67aeab3ad63a0b7f2506ae9d/"

    url_patterns:
      - "thefoundation.or.tz/tenders/*"
      - "cdn.prod.website-files.com/*.pdf"

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
      Webflow. Tender listing links to /tenders/{slug} detail pages. Documents (e.g. FCS-Strategic-Plan) on cdn.prod.website-files.com. Follow each tender link for PDF attachments.

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
  facebook: "FCSTZ"
  linkedin: "foundation-for-civil-society-fcs"
  instagram: "fcstanzania"

notes: |
  FCS is an independent Tanzanian non-profit organization that provides grants and capacity-building services to civil society organizations (CSOs).
---

# Foundation For Civil Society (FCS)

**Category:** NGO / Non-Profit Organization
**Website:** https://www.thefoundation.or.tz/
**Tender Page:** https://www.thefoundation.or.tz/news-media/tenders
**Keywords Found:** tender, tenders

## Contact Information
- Phone: 04-104 56 58-2
- Phone: 0 320-320 320-5
- Phone: 025-2030 
- Phone: 0478515625
- Phone: 0 320-320 57 56

## Scraping Instructions

**Strategy:** Scrape https://www.thefoundation.or.tz/news-media/tenders for tender/procurement notices.
**Method:** http_get

FCS is an independent Tanzanian non-profit organization that provides grants and capacity-building services to civil society organizations (CSOs).

### Tender Content Preview

> _dd-link w-inline-block"> Upcoming Events Tenders Archives <div class="navb

### Known Tender URLs

- https://www.thefoundation.or.tz/news-media/tenders

### Document Links Found

- https://cdn.prod.website-files.com/67aeab3ad63a0b7f2506ae9d/67c57d142d5120b2c1d2d98c_FCS-Strategic-Plan-2025-2030.pdf

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
thefoundation/
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
- **Active Tenders:** 0 (all listed tenders expired; moved to closed)
- **Signal Strength:** Strong (tender, tenders)
