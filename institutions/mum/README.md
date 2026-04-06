---
institution:
  name: "Muslim University of Morogoro (MUM)"
  slug: "mum"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "mum.ac.tz"

website:
  homepage: "https://mum.ac.tz/"
  tender_url: "https://mum.ac.tz/single-news-and-events/mum-iium-kuanzisha-mradi-wa-bidhaa-halali"

contact:
  email: "mum@mum.ac.tz"
  phone: "026
          "

scraping:
  enabled: false
  method: "http_get"
  strategy: "DISABLED: tender_url points to a single news article about halal products project, NOT a tender listing page. No tender content found. Search mum.ac.tz for actual tender/procurement page if one exists."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
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
      - "mum.ac.tz/storage/app/uploads/public/68f/9e7/09d/68f9e709d7bb2596540644.pdf"
      - "mum.ac.tz/storage/app/uploads/public/68f/9e6/89e/68f9e689ed702983602613.pdf"
      - "mum.ac.tz/storage/app/uploads/public/68f/9ee/9b1/68f9ee9b19a13019682907.pdf"
      - "mum.ac.tz/storage/app/uploads/public/68f/9e6/ccc/68f9e6ccc7f7e843363004.pdf"
      - "mum.ac.tz/storage/app/uploads/public/68f/9e6/3e5/68f9e63e51524329142825.pdf"

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
      Known document paths: /storage/app/uploads/public/68f/9e7/09d/68f9e709d7bb2596540644.pdf, /storage/app/uploads/public/68f/9e6/89e/68f9e689ed702983602613.pdf, /storage/app/uploads/public/68f/9ee/9b1/68f9ee9b19a13019682907.pdf

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
  Organization website at mum.ac.tz. Current tender_url is a news article page with no tender listing. Scraping disabled until actual tender page is identified.
---

# Muslim University Official Website - home

**Category:** Educational Institution
**Website:** https://mum.ac.tz/
**Tender Page:** https://mum.ac.tz/single-news-and-events/mum-iium-kuanzisha-mradi-wa-bidhaa-halali
**Keywords Found:** bid

## Contact Information
- Email: mum@mum.ac.tz
- Phone: 026
          
- Phone: 025
          
- Phone: 019682907
- Phone: 04042134767
- Phone: 0608170871

## Scraping Instructions

**Strategy:** Scrape https://mum.ac.tz/single-news-and-events/mum-iium-kuanzisha-mradi-wa-bidhaa-halali for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- https://mum.ac.tz/single-news-and-events/mum-iium-kuanzisha-mradi-wa-bidhaa-halali

### Document Links Found

- https://mum.ac.tz/storage/app/uploads/public/68f/9e6/ccc/68f9e6ccc7f7e843363004.pdf
- https://mum.ac.tz/storage/app/uploads/public/68f/9e6/3e5/68f9e63e51524329142825.pdf
- http://localhost/mumweb/storage/app/media/Prospectus/mum-prospectus-2020.pdf
- https://mum.ac.tz/storage/app/uploads/public/68f/9e7/09d/68f9e709d7bb2596540644.pdf
- https://mum.ac.tz/storage/app/uploads/public/68f/9e6/89e/68f9e689ed702983602613.pdf
- https://mum.ac.tz/storage/app/uploads/public/68f/9ee/9b1/68f9ee9b19a13019682907.pdf

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

Known document paths: /storage/app/uploads/public/68f/9e7/09d/68f9e709d7bb2596540644.pdf, /storage/app/uploads/public/68f/9e6/89e/68f9e689ed702983602613.pdf, /storage/app/uploads/public/68f/9ee/9b1/68f9ee9b19a13019682907.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
mum/
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
