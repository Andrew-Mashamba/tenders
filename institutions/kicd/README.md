---
institution:
  name: "Kaliua Institute of Community Development (KICD)"
  slug: "kicd"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "kicd.ac.tz"

website:
  homepage: "https://kicd.ac.tz/"
  tender_url: "https://kicd.ac.tz/"

contact:
  email: "kicdmzc@yahoo.com"
  alternate_emails:
    - "kaliuainstitute2024@yahoo.com"
  phone: "+255759041322"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    KICD homepage. Documents in /www/100/news/ (e.g. filename-Fomu NACTE MZA 2026.pdf). Uses AJAX
    load-more for staff, campus, partners. Check news/documents sections. Base href: https://kicd.ac.tz.
  selectors:
    container: ".contained-div, .page_content, main"
    tender_item: ".staff1_list, .campus1_list1, .partner_list1, a[href*='.pdf']"
    title: "h2, h3, h4, .title, a"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href*="/www/100/news/"]'
    pagination: ".loadmore, .pagination" 
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
      - "kicd.ac.tz/www/100/news/*.pdf"

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
      Documents at /www/100/news/ with format filename-{hash}.pdf. URL may have spaces (encoded).
      May need to follow news/announcements links for tender documents.

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
  Kaliua Institute of Community Development (KICD)
---

# Home

**Category:** Educational Institution
**Website:** https://kicd.ac.tz/
**Tender Page:** https://kicd.ac.tz/
**Keywords Found:** rfi

## Contact Information
- Email: kicdmzc@yahoo.com
- Email: kaliuainstitute2024@yahoo.com
- Phone: +255759041322
- Phone: 025-06-13
- Phone: +255628000443
- Phone: 026-01-17

## Scraping Instructions

**Strategy:** Scrape https://kicd.ac.tz/ for tender/procurement notices.
**Method:** http_get

Kaliua Institute of Community Development (KICD)

### Document Links Found

- https://kicd.ac.tz/www/100/news/8ba8a5cad9filename-Fomu NACTE MZA 2026.pdf
- https://kicd.ac.tz/www/100/news/54cb81e533filename-Fomu VETA MZA 2026.pdf

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
kicd/
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

- **Last Checked:** 10 June 2026
- **Active Tenders:** 0 (only student admission forms; no procurement tenders)
- **Signal Strength:** Weak (supply/rfi only)
