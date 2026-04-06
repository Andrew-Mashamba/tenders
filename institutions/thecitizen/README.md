---
institution:
  name: "The Citizen"
  slug: "thecitizen"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "thecitizen.co.tz"

website:
  homepage: "https://www.thecitizen.co.tz/"
  tender_url: "https://www.thecitizen.co.tz/tanzania/notices/tenders"

contact:
  phone: "00195312 1"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.thecitizen.co.tz/tanzania/notices/tenders. Newspaper CMS - tender notices under /tanzania/notices/tenders. Page partially loaded during analysis. Follow article links for full notices and documents."
  selectors:
    container: "main, .main-content, [data-content]"
    tender_item: "article, .article-item, .notice-item, a[href*='/tanzania/']"
    title: "h2, h3, .article-title, .headline"
    date: ".date, .published, time, .article-meta"
    document_link: 'a[href$=".pdf"], a[href*="resource/crblob"]'
    pagination: ".pagination, .nav-links"
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
      - "thecitizen.co.tz/*.pdf"

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
      Tender page under notices section. Documents may use /resource/crblob/ paths. Verify structure when page accessible.

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
  facebook: "TheCitizenTanzania"

notes: |
  Organization website at thecitizen.co.tz. Tender keywords detected: rfi, supply, tender, tenders.
---

# The Citizen

**Category:** Commercial / Private Sector
**Website:** https://www.thecitizen.co.tz/
**Tender Page:** https://www.thecitizen.co.tz/tanzania/notices/tenders
**Keywords Found:** rfi, supply, tender, tenders

## Contact Information
- Phone: 00195312 1
- Phone: 0228516 11
- Phone: 0152-0153
- Phone: 024-4583414-18
- Phone: 0568359 6

## Scraping Instructions

**Strategy:** Scrape https://www.thecitizen.co.tz/tanzania/notices/tenders for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ="/tanzania/notices" class="categories-nav_link ">Notices Tenders <a href="/tanzania/notices" class="categories-nav_link ca

### Known Tender URLs

- https://www.thecitizen.co.tz/tanzania/notices/tenders

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
thecitizen/
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
