---
institution:
  name: "Ocean Road Cancer Institute"
  slug: "orci"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "orci.or.tz"

website:
  homepage: "https://www.orci.or.tz/"
  tender_url: "https://www.orci.or.tz/tender/"

contact:
  email: "info@orci.or.tz"
  phone: "0 0 1000 600"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape tender page. Main content in article.hentry; TablePress table (#tablepress-2) for tender data; sidebar widgets (MAJARIDA) contain PDF links. Document path /oagrydee/YYYY/MM/."
  selectors:
    container: "article.hentry, article#post-1062, .site-content, #primary"
    tender_item: "table.tablepress tbody tr, .widget_custom_html, aside.widget"
    title: ".entry-title, h1.page-title, h3.widget-title"
    date: ".entry-meta, table.tablepress td"
    document_link: 'a[href$=".pdf"], a[href*="oagrydee"], .widget_custom_html a'
    pagination: ".pagination a, .nav-links a, .page-numbers"
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
      - "www.orci.or.tz/oagrydee/*/*.pdf"
      - "www.orci.or.tz/oagrydee/*/*/*.pdf"

    known_document_paths:
      - "/oagrydee/"
      - "/oagrydee/YYYY/MM/"

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
      Documents in /oagrydee/YYYY/MM/. TablePress table (#tablepress-2) for tender data. Sidebar MAJARIDA widget may contain journal PDFs (Jarida) — reject these; only create tenders for actual procurement notices with closing dates.

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
  facebook: "sharer"
  twitter: "intent"

notes: |
  Organization website at orci.or.tz. Tender keywords detected: bid, tender.
---

# Ocean Road Cancer Institute

**Category:** NGO / Non-Profit Organization
**Website:** https://www.orci.or.tz/
**Tender Page:** https://www.orci.or.tz/tender/
**Keywords Found:** bid, tender

## Contact Information
- Email: info@orci.or.tz
- Phone: 0 0 1000 600
- Phone: 02-02-2026-
- Phone: 026-01-31-
- Phone: 026-02-04-
- Phone: 026-02-02-

## Scraping Instructions

**Strategy:** Scrape https://www.orci.or.tz/tender/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> item menu-item-type-post_type menu-item-object-page menu-item-1065"> Tender CONTA

### Known Tender URLs

- https://www.orci.or.tz/tender/

### Document Links Found

- https://www.orci.or.tz/oagrydee/2024/10/ORCI-JARIDA1.pdf

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
orci/
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
- **Signal Strength:** Strong (tender)
