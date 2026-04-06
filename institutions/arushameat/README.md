---
institution:
  name: "Arusha Meat Company"
  slug: "arushameat"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "arushameat.co.tz"

website:
  homepage: "https://www.arushameat.co.tz/"
  tender_url: "https://www.arushameat.co.tz/open-tender/"

contact:
  email: "arushameatcompany@yahoo.com"
  phone: "022-09-08"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.arushameat.co.tz/open-tender/ for tender notices. Single tender per page. Title in h1.et_pb_module_header. Document link is a.et_pb_button (Pakua Maelekezo ya zabuni)—href may be # (JS-loaded). WordPress Divi theme. Documents in /wp-content/uploads/."
  selectors:
    container: "article.hentry, .entry-content"
    tender_item: "article.hentry, .et_pb_section"
    title: "h1.et_pb_module_header"
    date: "h1.et_pb_module_header"
    document_link: 'a.et_pb_button, a[href$=".pdf"], a[href*="/wp-content/uploads/"]'
    pagination: null 
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
      - "arushameat.co.tz/wp-content/uploads/*.pdf"

    known_document_paths:
      - "/wp-content/uploads/"

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
      WordPress Divi theme. Documents in /wp-content/uploads/. Tender title and date in h1 (e.g. 'TANGAZO LA ZABUNI... imetolewa 16/10/2025'). Download button may have href="#" and load via JS—check for actual PDF link in page source or button onclick.

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
  Organization website at arushameat.co.tz. Tender keywords detected: rfi, tender.
---

# Home - Arusha Meat Company

**Category:** Commercial / Private Sector
**Website:** https://www.arushameat.co.tz/
**Tender Page:** https://www.arushameat.co.tz/open-tender/
**Keywords Found:** rfi, tender

## Contact Information
- Email: arushameatcompany@yahoo.com
- Phone: 022-09-08
- Phone: 026-01-06
- Phone: +255 734 026 766
- Phone: +255734026766
- Phone: +255734026767

## Scraping Instructions

**Strategy:** Scrape https://www.arushameat.co.tz/open-tender/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> item-type-post_type menu-item-object-page menu-item-250"> Open Tender Contact Us

### Known Tender URLs

- https://www.arushameat.co.tz/open-tender/

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
arushameat/
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
