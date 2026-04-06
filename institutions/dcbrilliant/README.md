---
institution:
  name: "DC Brilliant College"
  slug: "dcbrilliant"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "dcbrilliant.ac.tz"

website:
  homepage: "https://dcbrilliant.ac.tz/"
  tender_url: "https://dcbrilliant.ac.tz/"

contact:
  email: "dcbrilliant.ac@gmail.com"
  phone: "01866544769"

scraping:
  enabled: true
  method: "http_get"
  strategy: "DC Brilliant College uses Joomla/SP Page Builder. Main content in #sp-main-body. Check Announcements (index.php/news-events), Documents Links section, and component content. Documents are primarily academic (syllabus, exam papers) - tender/procurement content is rare. Scrape .jmm-item for news/announcements, a[href*='/images/doc/'] for document links."
  selectors:
    container: "#sp-main-body, main#sp-component, .page-content, .sppb-section"
    tender_item: ".jmm-item, .sppb-addon-module .jmm-item, article"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href*="/images/doc/"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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
      - "/images/doc/"

    url_patterns:
      - "dcbrilliant.ac.tz/images/doc/*.pdf"

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
      Documents stored under /images/doc/ (e.g. CHEMISTRY.pdf, F2_CHEM_EXAMINATION_SERIES.pdf). These are primarily academic/syllabus materials. Announcements may link to tender-related content. Check News & Events and component content articles.

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
  facebook: "dcbrilliant0628981577"

notes: |
  Organization website at dcbrilliant.ac.tz. Tender keywords detected: rfi.
---

# DC Brilliant College

**Category:** Educational Institution
**Website:** https://dcbrilliant.ac.tz/
**Tender Page:** https://dcbrilliant.ac.tz/
**Keywords Found:** rfi

## Contact Information
- Email: dcbrilliant.ac@gmail.com
- Phone: 01866544769
- Phone: 01866544735 
- Phone: 081857316
- Phone: 0 0 1920 700
- Phone: +255 789 625 113

## Scraping Instructions

**Strategy:** Scrape https://dcbrilliant.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Document Links Found

- https://dcbrilliant.ac.tz/images/doc/CHEMISTRY.pdf
- https://dcbrilliant.ac.tz/images/doc/F2_CHEM_EXAMINATION_SERIES.pdf

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
dcbrilliant/
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
