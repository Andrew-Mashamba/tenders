---
institution:
  name: "Songea Smart Professional College"
  slug: "songeasmartcollege"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "songeasmartcollege.ac.tz"

website:
  homepage: "https://songeasmartcollege.ac.tz/"
  tender_url: "https://songeasmartcollege.ac.tz/"

contact:
  email: "songeasmart@yahoo.com"
  phone: "0758 419 225 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage 'Latest Downloads' section. Each item has title (a.ck), date (p.ck1), and PDF link. Follow 'More Downloads' to News-and-events for full list."
  selectors:
    container: ".news"
    tender_item: ".tk1"
    title: "a.ck"
    date: ".ck1"
    document_link: 'a.ck[href*=".pdf"], a.ck[href*=".doc"], a.ck[href*=".docx"]'
    pagination: ".more a"
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
      - "/www/100/news/"

    url_patterns:
      - "songeasmartcollege.ac.tz/www/100/news/*"
      - "songeasmartcollege.ac.tz/*.pdf"

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
      Documents at /www/100/news/{hash}filename-{filename}.pdf. Date format in .ck1: 'Placed : : YYYY-MM-DD'. More Downloads links to /News-and-events. Application forms and joining instructions (PDFs).

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
  facebook: "sharer.php"
  twitter: "intent"

notes: |
  SONGEA SMART PROFESSIONAL COLLEGE
---

# Home

**Category:** Educational Institution
**Website:** https://songeasmartcollege.ac.tz/
**Tender Page:** https://songeasmartcollege.ac.tz/
**Keywords Found:** rfi

## Contact Information
- Email: songeasmart@yahoo.com
- Phone: 0758 419 225 
- Phone: 026-2027 
- Phone: 0713 950 111 
- Phone: 010022172
- Phone: 026-02-27

## Scraping Instructions

**Strategy:** Scrape https://songeasmartcollege.ac.tz/ for tender/procurement notices.
**Method:** http_get

SONGEA SMART PROFESSIONAL COLLEGE

### Document Links Found

- https://songeasmartcollege.ac.tz/www/100/news/0c3c62d922filename-SSPC-PHARMACY APPLICATION FORM SEPT. 2022 & 23.pdf
- https://songeasmartcollege.ac.tz/www/100/news/f1aeed592cfilename-SSPC NON HEALTH PROGRAMMES APPLICATION FORM  2025 (1).pdf
- https://songeasmartcollege.ac.tz/www/100/news/7c44805993filename-JOINING INSTRUCTIONS FOR PHARMACY 2025 (2).pdf

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
songeasmartcollege/
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
