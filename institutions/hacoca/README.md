---
institution:
  name: "Huruma Aids Concern and Care (HACOCA)"
  slug: "hacoca"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "hacoca.or.tz"

website:
  homepage: "https://hacoca.or.tz/"
  tender_url: "https://hacoca.or.tz/tender-notice-full-rebranding-of-hacoca/"

contact:
  phone: "+255 700 000 000"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Single tender page (WordPress). Scrape tender-notice-full-rebranding-of-hacoca and tenders-at-hacoca. Extract title, deadline, scope. No document downloads - submissions via email to info@hacoca.or.tz."
  selectors:
    container: "article, .entry-content, .single-post, main"
    tender_item: "article, .entry-content"
    title: "h1, .entry-title, .page-title"
    date: ".date, .published, time, .article-info"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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

    url_patterns:
      - "hacoca.or.tz/*.pdf"

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
      No document downloads on tender pages. HACOCA requests submissions via email (info@hacoca.or.tz) as single PDF. Tender content is inline in page body.

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
  facebook: "hacocatz"
  twitter: "hacocatz"
  instagram: "hacocatz"

notes: |
  HACOCA IS support communities facing challenges like HIV/AIDS, food insecurity, income poverty, ignorance, and gender-based violence.
---

# Huruma Aids Concern and Care (HACOCA)

**Category:** NGO / Non-Profit Organization
**Website:** https://hacoca.or.tz/
**Tender Page:** https://hacoca.or.tz/tender-notice-full-rebranding-of-hacoca/
**Keywords Found:** bid, tender, tenders

## Contact Information
- Phone: +255 700 000 000
- Phone: 024-10-01-
- Phone: 025-01-16
- Phone: 01466275659824
- Phone: 0378103664 

## Scraping Instructions

**Strategy:** Scrape https://hacoca.or.tz/tender-notice-full-rebranding-of-hacoca/ for tender/procurement notices.
**Method:** http_get

HACOCA IS support communities facing challenges like HIV/AIDS, food insecurity, income poverty, ignorance, and gender-based violence.

### Tender Content Preview

> ing: 0 20px;"> Tender Notice: Full Rebranding of HACOCA <a class="spt-link" style="color: #333333;" target="_self"

### Known Tender URLs

- https://hacoca.or.tz/tender-notice-full-rebranding-of-hacoca/
- https://hacoca.or.tz/tenders-at-hacoca/

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
hacoca/
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
- **Signal Strength:** Strong (tender, tenders)
