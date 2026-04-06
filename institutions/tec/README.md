---
institution:
  name: "Tanzania Episcopal Conference (TEC)"
  slug: "tec"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tec.or.tz"

website:
  homepage: "https://tec.or.tz/"
  tender_url: "https://tec.or.tz/index.php/news/"

contact:
  email: "info@tec.or.tz"
  phone: "01165261019"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape News & Events page for tenders/RFPs. WordPress/Kingster theme. Tender posts mixed with news; filter by keywords (tender, RFP, proposal). Follow post links for full documents."
  selectors:
    container: ".gdlr-core-blog-item-holder, .gdlr-core-pbf-section"
    tender_item: ".gdlr-core-item-list.gdlr-core-blog-medium, .gdlr-core-blog-modern"
    title: ".gdlr-core-blog-title a, h3.gdlr-core-blog-title a"
    date: ".gdlr-core-blog-date-wrapper, .gdlr-core-blog-date-day, .gdlr-core-blog-date-month"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href*="/wp-content/uploads/"]'
    pagination: ".gdlr-core-pagination a, .page-numbers a"
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
      - "tec.or.tz/wp-content/uploads/*"

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
      WordPress site. Documents in /wp-content/uploads/ (year/month subdirs). News page mixes tenders with general news; filter by tender/RFP/proposal keywords. Tender detail pages may have attached PDFs.

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
  facebook: "profile.php"
  twitter: "BarazaTec"
  instagram: "p"

notes: |
  Organization website at tec.or.tz. Tender keywords detected: request for proposal, rfi, tender.
---

# TEC &#8211; Tanzania Episcopal Conference

**Category:** NGO / Non-Profit Organization
**Website:** https://tec.or.tz/
**Tender Page:** https://tec.or.tz/index.php/2024/01/19/mabalozi-wa-amani-ii-phase-project-media-campaign-tender/
**Keywords Found:** request for proposal, rfi, tender

## Contact Information
- Email: info@tec.or.tz
- Phone: 01165261019
- Phone: 024-05-21 11
- Phone: 01155649224499
- Phone: +255 222 928 341
- Phone: 035413002

## Scraping Instructions

**Strategy:** Scrape https://tec.or.tz/index.php/2024/01/19/mabalozi-wa-amani-ii-phase-project-media-campaign-tender/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> > <img src="https://tec.or.tz/wp-content/uploads/2024/04/tende2.png" width="672" height="216" srcset="https://tec.or.tz/wp-content/uploads/2024/04/tende2-400x128.png 400w, https://tec.or.tz/

### Known Tender URLs

- https://tec.or.tz/index.php/2024/01/19/mabalozi-wa-amani-ii-phase-project-media-campaign-tender/
- https://tec.or.tz/index.php/2024/01/19/request-for-proposal-mabalozi-wa-amani-ii-phase-project-material-development-tender/

### Document Links Found

- https://tec.or.tz/wp-content/uploads/2021/05/Catholic-Directory-2020-Edition.pdf

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

Known document paths: /wp-content/uploads/2021/05/Catholic-Directory-2020-Edition.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tec/
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
