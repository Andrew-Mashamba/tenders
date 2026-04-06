---
institution:
  name: "TARA - Tanzania Roads Association"
  slug: "tara"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tara.or.tz"

website:
  homepage: "https://tara.or.tz/"
  tender_url: "https://tara.or.tz/"

contact:
  email: "info@tara.or.tz"
  phone: "000235727"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Drupal 7 site. No dedicated tender page. Scrape Resources (#block-views-resources-block) for bulletins with PDF downloads; Events (#block-views-events-block) for procurement-related training/seminars; News (#block-views-news-events-block) for announcements. Documents via /file/{id}/download?token=... and /sites/default/files/."
  selectors:
    container: "#block-views-resources-block .view-resources, #block-views-events-block .view-events, #block-views-news-events-block .view-news-events"
    tender_item: ".view-resources .views-row, .view-events .views-row, .view-news-events .views-row"
    title: ".views-field-title a, .fntitle a"
    date: ".views-field-created .field-content, .views-field-field-event-date .date-display-single, .nedate"
    document_link: 'a[href*="/file/"][href*="download"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: ".pager a, .pagination a"
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
        - 'a[href*="/file/"][href*="download"]'
        - 'a[href$=".pdf"]'
        - 'a[href$=".doc"]'
        - 'a[href$=".docx"]'
        - 'a[href$=".xls"]'
        - 'a[href$=".xlsx"]'
        - 'a[href$=".zip"]'
        - 'a[href*="/storage/"]'
        - 'a[href*="/uploads/"]'
        - 'a[href*="/sites/default/files/"]'
        - 'a[href*="/media/"]'
        - 'a[href*="/wp-content/uploads/"]'
        - 'a[href*="/download"]'
        - 'a[download]'
      resolve_redirects: true
      decode_percent_encoding: true

    known_document_paths:
      - "/sites/default/files/"
      - "/file/"

    url_patterns:
      - "tara.or.tz/file/*/download*"
      - "tara.or.tz/sites/default/files/*"

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
      Resources: bulletins via /file/{id}/download?token=... (e.g. /file/2589/download). Files in /sites/default/files/. No traditional tender listing — TARA is Roads Association; scrape Events (training, seminars) and Resources (bulletins) for procurement-related content.

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
  facebook: "tanzaniaroadsassociation"
  instagram: "tanzania_roads_association"

notes: |
  Organization website at tara.or.tz. Tender keywords detected: rfi.
---

# TARA - Tanzania Roads Association |

**Category:** NGO / Non-Profit Organization
**Website:** https://tara.or.tz/
**Tender Page:** https://tara.or.tz/
**Keywords Found:** rfi

## Contact Information
- Email: info@tara.or.tz
- Phone: 000235727
- Phone: +255 754 362157
- Phone: 024-08-19-15-2
- Phone: 000235709

## Scraping Instructions

**Strategy:** Scrape https://tara.or.tz/ for tender/procurement notices.
**Method:** http_get



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
tara/
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
