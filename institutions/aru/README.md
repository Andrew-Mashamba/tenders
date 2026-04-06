---
institution:
  name: "Ardhi University (ARU)"
  slug: "aru"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "aru.ac.tz"

website:
  homepage: "https://aru.ac.tz/"
  tender_url: "https://aru.ac.tz/"

contact:
  email: "aru@aru.ac.tz"
  phone: "026
         "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://aru.ac.tz/ for tender/procurement notices. Tenders are in dropdown menus. Documents in /uploads/documents/, /uploads/announcements/, /uploads/text-editor/files/. Follow dropdown-item links for tender PDFs."
  selectors:
    container: ".content, main, .dropdown-menu, .entry-content, article"
    tender_item: ".dropdown-item, article, .tender-item"
    title: "h2, h3, h4, .tender-title, .dropdown-item"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/uploads/"]'
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
      - "aru.ac.tz/uploads/documents/*.pdf"
      - "aru.ac.tz/uploads/announcements/*.pdf"
      - "aru.ac.tz/uploads/text-editor/files/*.pdf"

    known_document_paths:
      - "/uploads/documents/"
      - "/uploads/announcements/"
      - "/uploads/text-editor/files/"

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
      Documents in /uploads/documents/, /uploads/announcements/, /uploads/text-editor/files/. Pattern: en-{timestamp}-{filename}.pdf. Tenders in dropdown menu. Fetch failed (SSL/timeout) during analysis—selectors may need verification.

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
  instagram: "ardhi.university"

notes: |
  Ardhi University | Chuo Kikuu Ardhi
---

# ARDHI |   Home

**Category:** Educational Institution
**Website:** https://aru.ac.tz/
**Tender Page:** https://aru.ac.tz/
**Keywords Found:** bid, procurement, tender, tenders

## Contact Information
- Email: aru@aru.ac.tz
- Phone: 026
         
- Phone: 024-2025
    
- Phone: 07553332-
- Phone: 025-2026-
- Phone: 0 0 2000 128

## Scraping Instructions

**Strategy:** Scrape https://aru.ac.tz/ for tender/procurement notices.
**Method:** http_get

Ardhi University | Chuo Kikuu Ardhi

### Tender Content Preview

> a class='dropdown-item' href= 'https://www.aru.ac.tz/uploads/documents/en-1707553332-Invitation for Tenders.pdf'>Invitation for Tender Internationalization <ul class='dropdown-menu

### Document Links Found

- https://www.aru.ac.tz/uploads/documents/en-1766479156-Revised%20University%20Almanac%202025-26%20Academic%20Year.pdf
- https://aru.ac.tz/uploads/announcements/en-1760535266-Employment Opportunities October 2025.pdf
- https://aru.ac.tz/uploads/announcements/en-1771217112-ARU_short_course_calendar_2026.pdf
- https://aru.ac.tz/uploads/announcements/en-1751457052-CFE Programme Catalogue.pdf
- https://aru.ac.tz/uploads/announcements/en-1752771861-PGD ADVERT 2025-26.pdf
- https://www.aru.ac.tz/uploads/documents/en-1743666554-Adhi University Prospectus 2024-2025.pdf

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

Known document paths: /uploads/documents/en-1676637321-ACTEA.pdf, /uploads/documents/en-1707134843-Environmental%20and%20Social%20Impact%20Assessment%20Report%20ARU-MWANZA_CAMPUS.pdf, /uploads/documents/en-1771216880-ARU_short_course_calendar_2026.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
aru/
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
- **Signal Strength:** Strong (procurement, tender, tenders)
