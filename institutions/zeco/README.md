---
institution:
  name: "Zanzibar Electricity Corporation (ZECO)"
  slug: "zeco"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "zeco.co.tz"

website:
  homepage: "https://zeco.co.tz/"
  tender_url: "https://zeco.co.tz/index.php/procurement"

contact:
  email: "info@zeco.co.tz"
  phone: "065054893"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Joomla/SP Page Builder. Scrape /index.php/procurement for procurement info and document links. Also scrape /index.php/news for tender articles and /index.php/projects?layout=table for projects. Documents in /images/docs/ (e.g. ZECO_GPN_2022-20231.pdf)."
  selectors:
    container: ".sp-page-builder .page-content, .sppb-addon-content, main, #sp-main-body"
    tender_item: ".sppb-addon, .article-list .article, .NEWS .article"
    title: "h1, h2, h3, h4, .sppb-addon-title, .article-header"
    date: ".article-date, .date, time"
    document_link: 'a[href$=".pdf"], a[href*="/images/docs/"], a[href$=".doc"], a[href$=".docx"]'
    pagination: ".pagination a, .NEWS .pagination a" 
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
      - "/images/docs/"

    url_patterns:
      - "zeco.co.tz/images/docs/*.pdf"
      - "zeco.co.tz/index.php/news/*"
      - "zeco.co.tz/index.php/projects*"

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
      Procurement documents in /images/docs/ (e.g. General Procurement Plan). News section has tender articles. Projects page at /index.php/projects?layout=table. Contact: pmu@zeco.co.tz for procurement info.

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
  twitter: "widgets"

notes: |
  Zanzibar Electricity Corporation
---

# Home

**Category:** Commercial / Private Sector
**Website:** https://zeco.co.tz/
**Tender Page:** https://zeco.co.tz/index.php/procurement
**Keywords Found:** bid, bidding, eoi, procurement, rfi

## Contact Information
- Email: info@zeco.co.tz
- Phone: 065054893
- Phone: +255772877879
- Phone: 065054893-
- Phone: 065054958 
- Phone: 065054958-

## Scraping Instructions

**Strategy:** Scrape /index.php/procurement, /index.php/news, and /index.php/projects for tender/procurement notices. Documents in /images/docs/.
**Method:** http_get

Zanzibar Electricity Corporation

### Tender Content Preview

> href="/index.php/our-services" >Our Services Procurement Gallery News <li class="sp-men

### Known Tender URLs

- https://zeco.co.tz/index.php/procurement
- https://zeco.co.tz/index.php/news
- https://zeco.co.tz/index.php/projects?layout=table

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
zeco/
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
- **Signal Strength:** Strong (bidding, eoi, procurement)
