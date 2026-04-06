---
institution:
  name: "Maple Group"
  slug: "maple"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "maple.co.tz"

website:
  homepage: "https://maple.co.tz/"
  tender_url: "https://maple.co.tz/tenders/"

contact:
  phone: "095814981"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://maple.co.tz/tenders/ for tender notices. WordPress with WPBakery/LiteSpeed. Content may be lazy-loaded; follow links to tender detail pages for documents."
  selectors:
    container: ".entry-content, .wpb_wrapper, main, .vc_row"
    tender_item: "article, .post, .tender-item, .vc_column"
    title: "h2, h3, h4, .entry-title, a"
    date: ".date, .posted-on, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/wp-content/uploads/"]'
    pagination: ".pagination a, .nav-links a, a.next"
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
      - "maple.co.tz/wp-content/uploads/*.pdf"

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
      WordPress; documents typically at /wp-content/uploads/. Tenders page may use WPBakery shortcodes; follow links to individual tender posts for full documents.

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
  facebook: "maplegrouptanzania"
  linkedin: "maplegrouptanzania"

notes: |
  Organization website at maple.co.tz. Tender keywords detected: rfi, tender, tenders.
---

# Maple &#8211; Maple Group is a leading private BPO organisation in Tanzania

**Category:** Commercial / Private Sector
**Website:** https://maple.co.tz/
**Tender Page:** https://maple.co.tz/tenders/
**Keywords Found:** rfi, tender, tenders

## Contact Information
- Phone: 095814981
- Phone: 095976494
- Phone: 0280766950 
- Phone: 026-02-14
- Phone: +255 687 204 760

## Scraping Instructions

**Strategy:** Scrape https://maple.co.tz/tenders/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> nu-item menu-item-type-post_type menu-item-object-page menu-item-2328"> Tenders News <li id="menu-item-174

### Known Tender URLs

- https://maple.co.tz/tenders/

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
maple/
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
