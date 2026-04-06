---
institution:
  name: "Comenius Polytechnic Institute (CPI)"
  slug: "cpi"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "cpi.ac.tz"

website:
  homepage: "https://cpi.ac.tz/"
  tender_url: "https://cpi.ac.tz/"

contact:
  phone: "0658551404"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage for announcements and employment/tender notices. LATEST NEWS ticker (ul#ticker01.news_sticker) and ANNOUNCEMENTS (article.all-browsers > article.browser) contain job ads and document links. Documents stored in /doc/ path. Employment Opportunity and timetable PDFs are primary targets."
  selectors:
    container: "#newsSection, .all-browsers, #contentSection, .left_content, main"
    tender_item: "ul#ticker01 li, article.browser, .latest_postnav li"
    title: "a, h2, .catg_title, li a"
    date: ""
    document_link: 'a[href$=".pdf"], a[href*="doc/"]'
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
      - "/doc/"

    url_patterns:
      - "cpi.ac.tz/doc/*.pdf"

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
      Documents stored in /doc/ (e.g. doc/JOB.pdf, doc/time24.pdf, doc/pros.pdf, doc/almanac.pdf). Employment ads and timetables in LATEST NEWS and ANNOUNCEMENTS. Bootstrap-based site.

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
  Organization website at cpi.ac.tz. Tender keywords detected: procurement, supply.
---

# Comenius Polytechnic Institute

**Category:** Educational Institution
**Website:** https://cpi.ac.tz/
**Tender Page:** https://cpi.ac.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Phone: 0658551404
- Phone: 0755670307
- Phone: 0733737223
  

## Scraping Instructions

**Strategy:** Scrape https://cpi.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> mg/proc.jpg"> 1.PROCUREMENT AND SUPPLY MANAGEMENT <a href="#" class="med

### Document Links Found

- https://cpi.ac.tz/doc/JOB.pdf
- https://cpi.ac.tz/doc/job.pdf
- https://cpi.ac.tz/doc/fee structure.pdf
- https://cpi.ac.tz/doc/time24.pdf
- https://cpi.ac.tz/doc/pros.pdf
- https://cpi.ac.tz/doc/almanac.pdf

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
cpi/
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
