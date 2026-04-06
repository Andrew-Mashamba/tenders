---
institution:
  name: "ZyNOX Construction Company"
  slug: "zynox"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "zynox.co.tz"

website:
  homepage: "https://zynox.co.tz/"
  tender_url: "https://zynox.co.tz/"

contact:
  email: "info@zynox.co.tz"
  phone: "+255 762 175 079 "

scraping:
  enabled: false
  method: "http_get"
  strategy: |
    DISABLED: zynox.co.tz is a corporate construction company site - no tender/procurement listing.
    Homepage has: services, blog posts, clients. Company profile PDF at /site/assets/files/1015/zynox_company_profile.pdf.
    Re-enable if ZyNOX adds a tender/procurement page.
  selectors:
    container: "main.main, .home-services, .home-news"
    tender_item: ".col-md-4, .blog-img-box, .services .col-md-4"
    title: "h2, h4.subtitle, .subtitle a"
    date: ".blog-date .month, .blog-date .date"
    document_link: 'a[href$=".pdf"], a[href*="/site/assets/files/"]'
    pagination: ".blog-btn a, .pagination a" 
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
        - 'a[href*="/site/assets/files/"]'
        - 'a[href*="/download"]'
        - 'a[download]'
      resolve_redirects: true
      decode_percent_encoding: true

    known_document_paths:
      - "/site/assets/files/"
    url_patterns:
      - "zynox.co.tz/site/assets/files/*.pdf"
      - "zynox.co.tz/site/assets/files/*.doc"
      - "zynox.co.tz/site/assets/files/*.docx"

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
      Documents at /site/assets/files/ (e.g. 1015/zynox_company_profile.pdf). No tender listing - corporate site only.

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
  Construction company - petroleum/LPG facilities, civil works. No tender listing on site.
  Document path: /site/assets/files/. Scraping disabled - corporate site only.
---

# About ZyNOX | ZyNOX Construction Company - Tanzania

**Category:** Commercial / Private Sector
**Website:** https://zynox.co.tz/
**Tender Page:** https://zynox.co.tz/
**Keywords Found:** tender

## Contact Information
- Email: info@zynox.co.tz
- Phone: +255 762 175 079 

## Scraping Instructions

**Strategy:** Scrape https://zynox.co.tz/ for tender/procurement notices.
**Method:** http_get

Offshore - Responsive HTML Template

### Tender Content Preview

> > Our recognised expertise in design &amp; construct, construction management, and conventional tendering, has enabled us to demonstrate solid and steady growth. Working harmoniously with our clients, at all times we bring a fully-cooperative approach to every project stage – from initia

### Document Links Found

- https://zynox.co.tz/site/assets/files/1015/zynox_company_profile.pdf

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

Known document paths: /assets/files/1015/zynox_company_profile.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
zynox/
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
