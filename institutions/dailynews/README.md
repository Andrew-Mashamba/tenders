---
institution:
  name: "Daily News - Tanzania Standard Newspapers"
  slug: "dailynews"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "dailynews.co.tz"

website:
  homepage: "https://dailynews.co.tz/"
  tender_url: "https://dailynews.co.tz/"

contact:
  phone: "026-03-12-"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Daily News is a newspaper — search ?s=tender returns news articles ABOUT tenders (government announcements), not actual procurement notices with bid documents. Reject news/press coverage. Only accept articles that embed downloadable tender PDFs or are official RFI/RFP notices from institutions. Parse .post-item from search results; follow article detail pages for wp-content/uploads PDFs."
  selectors:
    container: ".mag-box, .mag-box-container, #tie-block_427"
    tender_item: ".post-item"
    title: ".post-title a, .post-box-title a"
    date: ".post-meta .date, .date.meta-item"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download], .wpdm-download-link'
    pagination: ".pages-numbers a, .pages-nav a, a.next"
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
      - "dailynews.co.tz/wp-content/uploads/*.pdf"
      - "dailynews.co.tz/*.pdf"

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
      WordPress site with Download Manager plugin. Documents in /wp-content/uploads/. Tender notices appear as news articles; follow article links to detail pages for document downloads. Use site search ?s=tender for procurement-related content.

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
  facebook: "DailynewsTanzania"
  twitter: "dailynewstz"
  instagram: "dailynews_tz"

notes: |
  Daily News is the most trusted source of news in Tanzania. It is Tanzania&#039;s leading national English-language newspaper.
---

# Home - Daily News

**Category:** Commercial / Private Sector
**Website:** https://dailynews.co.tz/
**Tender Page:** https://dailynews.co.tz/
**Keywords Found:** rfi

## Contact Information
- Phone: 026-03-12-
- Phone: 021-04-12
- Phone: 0618955123
- Phone: 025-11-18
- Phone: 026-03-13-

## Scraping Instructions

**Strategy:** Scrape https://dailynews.co.tz/ for tender/procurement notices.
**Method:** http_get

Daily News is the most trusted source of news in Tanzania. It is Tanzania&#039;s leading national English-language newspaper.

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
dailynews/
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
