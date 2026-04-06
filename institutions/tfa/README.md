---
institution:
  name: "Tanganyika Farmers Association (TFA)"
  slug: "tfa"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "tfa.co.tz"

website:
  homepage: "https://tfa.co.tz/"
  tender_url: "https://tfa.co.tz/request-for-proposal-rfp/"

contact:
  phone: "0 842 767 846 7"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://tfa.co.tz/request-for-proposal-rfp/. WordPress/Elementor page. RFP content in main area; 'Recent Post' sidebar may list items via .elementor-loop-container. Documents in wp-content/uploads. Follow post links for full tender details."
  selectors:
    container: ".elementor-widget-loop-grid, .elementor-loop-container, main .elementor-section"
    tender_item: ".e-loop-item, .elementor-loop-container article, .news-sidebar .elementor-heading-title"
    title: ".elementor-heading-title, h2, h3"
    date: ".elementor-post-date, .date, time"
    document_link: 'a[href$=".pdf"], a[href*="wp-content/uploads"]'
    pagination: ".elementor-pagination, .nav-links"
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
      - "tfa.co.tz/wp-content/uploads/*.pdf"

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
      WordPress site. Documents typically in /wp-content/uploads/. RFP page may be landing page; follow links to individual posts for documents.

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
  Organization website at tfa.co.tz. Tender keywords detected: request for proposal, rfp, supply.
---

# TFA &#8211; Tanganyika Farmers Association

**Category:** Commercial / Private Sector
**Website:** https://tfa.co.tz/
**Tender Page:** https://tfa.co.tz/request-for-proposal-rfp/
**Keywords Found:** request for proposal, rfp, supply

## Contact Information
- Phone: 0 842 767 846 7
- Phone: 00 408 258 167
- Phone: 0 0 500 500
- Phone: 04 958 771
- Phone: 0 196 150 212 1

## Scraping Instructions

**Strategy:** Scrape https://tfa.co.tz/request-for-proposal-rfp/ for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- https://tfa.co.tz/request-for-proposal-rfp/

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
tfa/
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
- **Signal Strength:** Strong (rfp)
