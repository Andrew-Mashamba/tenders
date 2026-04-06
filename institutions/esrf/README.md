---
institution:
  name: "Economic and Social Research Foundation (ESRF)"
  slug: "esrf"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "esrf.or.tz"

website:
  homepage: "https://esrf.or.tz/"
  tender_url: "https://esrf.or.tz/"

contact:
  email: "esrf@esrf.or.tz"
  alternate_emails:
    - "info@esrf.or.tz"
  phone: "+255 22 2926084 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "WordPress (Grassywp). Homepage shows research, departments, flagship projects. Commissioned Research dept mentions 'expression of interest for bidding tenders' but no dedicated tender listing. Strategic plans at /strategic-plans/ have PDF downloads. Check /staff/, publications for tender notices."
  selectors:
    container: "main, .vc_row, .wpb_wrapper, .entry-content"
    tender_item: "article, .wpb_column, .vc_column-inner"
    title: "h2, h3, h4, h5, .wpb_heading"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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

    url_patterns:
      - "esrf.or.tz/wp-content/uploads/*"
      - "www.esrf.or.tz/wp-content/uploads/*"

    known_document_paths:
      - "/wp-content/uploads/2022/12/"
      - "/wp-content/uploads/2020/06/"
      - "/wp-content/uploads/2024/05/"
      - "/wp-content/uploads/2025/08/"

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
      /strategic-plans/ has PDF downloads (MTSP, Annual Reports). Documents in /wp-content/uploads/YYYY/MM/. No dedicated tender listing page. Commissioned Research dept does tender work but no public listing found.

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
  facebook: "ESRFTZ"
  twitter: "ESRFTZ"
  instagram: "esrftz"

notes: |
  Organization website at esrf.or.tz. Tender keywords detected: bid, bidding, expression of interest, rfi, tender, tenders. No dedicated tender listing page. Strategic plans and publications available. Scraping disabled.
---

# ESRF &#8211; Economic and Social Research Foundation, ESRF,  ESRF TANZANIA, ESRF THINK TANK, Research Tanzania ,Tanzania development, Tanzania economy, Economic development, Research Institute, Social

**Category:** NGO / Non-Profit Organization
**Website:** https://esrf.or.tz/
**Tender Page:** https://esrf.or.tz/
**Keywords Found:** bid, bidding, expression of interest, rfi, tender, tenders

## Contact Information
- Email: esrf@esrf.or.tz
- Email: info@esrf.or.tz
- Phone: +255 22 2926084 
- Phone: +255 784 481 658 
- Phone: 05208036130
- Phone: 05541062663-1
- Phone: 09607147265

## Scraping Instructions

**Strategy:** Scrape https://esrf.or.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ng demand driven commissioned researches, writing proposals and expression of interests for bidding tenders , supervision of projects and attending various meeting for disseminating study results. <div class="wpb_column vc_column_container

### Document Links Found

- https://www.esrf.or.tz/wp-content/uploads/2025/08/Annual-Report-2024.pdf

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

Known document paths: /wp-content/uploads/2025/08/Annual-Report-2024.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
esrf/
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
- **Signal Strength:** Strong (bidding, expression of interest, tender, tenders)
