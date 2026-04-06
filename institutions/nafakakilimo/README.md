---
institution:
  name: "NAFAKA KILIMO"
  slug: "nafakakilimo"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "nafakakilimo.or.tz"

website:
  homepage: "https://nafakakilimo.or.tz/"
  tender_url: "https://nafakakilimo.or.tz/"
  news_url: "https://nafakakilimo.or.tz/news.php"

contact:
  email: "info@nafakakilimo.or.tz"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage and news.php for job announcements (NAFAKA KILIMO - Job announcement). News items list job/tender posts. Documents in /assets/docs/."
  selectors:
    container: "main, .content, .news-section, .post-list"
    tender_item: ".post-item, .news-item, article, li"
    title: "h4, h3, h2, .post-title, a"
    date: ".date, .post-date, time, small"
    document_link: 'a[href*="/assets/docs/"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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

    known_document_paths:
      - "/assets/docs/"
    url_patterns:
      - "nafakakilimo.or.tz/assets/docs/*.pdf"
      - "nafakakilimo.or.tz/assets/docs/*.doc"

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
      Job announcement PDFs stored at /assets/docs/ (e.g. NKJobAnnouncementPost 20240225.pdf, NKJobAnnouncementPost 20250225.pdf). Scrape news.php for job/tender announcements.

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
  twitter: "nafakakilimo"
  linkedin: "nafaka-kilimo"
  instagram: "nafakakilimo"

notes: |
  NAFAKA KILIMO Official Website
---

# Home - NAFAKA KILIMO

**Category:** NGO / Non-Profit Organization
**Website:** https://nafakakilimo.or.tz/
**Tender Page:** https://nafakakilimo.or.tz/
**Keywords Found:** rfi

## Contact Information
- Email: info@nafakakilimo.or.tz

## Scraping Instructions

**Strategy:** Scrape https://nafakakilimo.or.tz/ for tender/procurement notices.
**Method:** http_get

NAFAKA KILIMO Official Website

### Document Links Found

- https://nafakakilimo.or.tz/assets/docs/NKJobAnnouncementPost 20240225.pdf
- https://nafakakilimo.or.tz/assets/docs/NKJobAnnouncementPost 20250225.pdf

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
nafakakilimo/
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
