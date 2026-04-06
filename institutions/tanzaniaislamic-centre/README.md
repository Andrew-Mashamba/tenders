---
institution:
  name: "Tanzania Islamic Centre"
  slug: "tanzaniaislamic-centre"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tanzaniaislamic-centre.or.tz"

website:
  homepage: "https://tanzaniaislamic-centre.or.tz/"
  tender_url: "https://tanzaniaislamic-centre.or.tz/"

contact:
  email: "info@tanzaniaislamic-centre.or.tz"
  phone: "018-02-23"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Drupal 7 site. Homepage shows news/announcements in table.views-table. Scrape #block-views-front-page-block-1 for announcements. Each row has date in td.views-field-event-calendar-date, title in td.views-field-title a. No dedicated tender page — check /node/{id} detail pages for procurement-related content. Documents in /sites/default/files/."
  selectors:
    container: "#block-views-front-page-block-1 .view-content, .view-front-page"
    tender_item: "table.views-table tbody tr"
    title: "td.views-field-title a"
    date: "td.views-field-event-calendar-date .date-display-single"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/sites/default/files/"]'
    pagination: ".pager a, .pagination a"
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
      - "/sites/default/files/"

    url_patterns:
      - "tanzaniaislamic-centre.or.tz/sites/default/files/*"

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
      Drupal default path /sites/default/files/. No dedicated tender section — homepage lists news/events. Follow /node/{id} links to detail pages for document attachments. RFI keyword may be false positive; site is religious org.

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
  facebook: "zymphonies"
  twitter: "zymphonies"
  linkedin: "zymphonies"

notes: |
  Organization website at tanzaniaislamic-centre.or.tz. Tender keywords detected: rfi.
---

# Tanzania Islamic Centre

**Category:** NGO / Non-Profit Organization
**Website:** https://tanzaniaislamic-centre.or.tz/
**Tender Page:** https://tanzaniaislamic-centre.or.tz/
**Keywords Found:** rfi

## Contact Information
- Email: info@tanzaniaislamic-centre.or.tz
- Phone: 018-02-23
- Phone: +255 713 623 520
- Phone: 018-01-29

## Scraping Instructions

**Strategy:** Scrape https://tanzaniaislamic-centre.or.tz/ for tender/procurement notices.
**Method:** http_get



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
tanzaniaislamic-centre/
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
- **Signal Strength:** Weak (supply/rfi only)
