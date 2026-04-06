---
institution:
  name: "Tanzania Red Cross Society"
  slug: "trcs"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "trcs.or.tz"

website:
  homepage: "https://trcs.or.tz/"
  tender_url: "https://trcs.or.tz/tenders-opportunities/"

contact:
  email: "info@trcs.or.tz"
  alternate_emails:
    - "info@trcs.co.tz"
  phone: "0800 750 151"

scraping:
  enabled: true
  method: "http_get"
  strategy: "WordPress/Elementor site. Tenders displayed as blog-style posts. Parse .blog-style_2 items, follow .text_btn links to detail pages for documents. Uses The Events Calendar (tribe-events) for dates."
  selectors:
    container: ".blog_post_section, .blog_container, section.blog_post_section"
    tender_item: ".blog-style_2, .blog-style_2.mb_40"
    title: ".title_22 a, .title_22"
    date: ".date_tm time, .date_tm"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download], .text_btn'
    pagination: ".pagination_blog .page-numbers, .pagination a"
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
      - "/wp-content/uploads/"
    url_patterns:
      - "trcs.or.tz/wp-content/uploads/*.pdf"
      - "trcs.or.tz/news/*"

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
      Tender detail pages at /news/{slug}/. Documents linked from detail pages. Follow Event Details / text_btn links. WordPress uploads in /wp-content/uploads/.

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
  facebook: "pages"
  instagram: "tanzaniaredcross"

notes: |
  Organization website at trcs.or.tz. Tender keywords detected: quotation, rfi, tender, tenders.
---

# Tanzania Redcross Society

**Category:** NGO / Non-Profit Organization
**Website:** https://trcs.or.tz/
**Tender Page:** https://trcs.or.tz/tenders-opportunities/
**Keywords Found:** quotation, rfi, tender, tenders

## Contact Information
- Email: info@trcs.or.tz
- Email: info@trcs.co.tz
- Phone: 0800 750 151
- Phone: 0800 750 150 -
- Phone: 0831529424260
- Phone: 0800 750 150 
- Phone: 025-11-28-

## Scraping Instructions

**Strategy:** Scrape https://trcs.or.tz/tenders-opportunities/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> activate menu_default menu_noa menu-item-6840 nav-item" > Tenders &#038; Opportunities <li class="menu-item menu-item-type-custom m

### Known Tender URLs

- https://trcs.or.tz/tenders-opportunities/

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
trcs/
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
