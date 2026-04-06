---
institution:
  name: "Thinkmate"
  slug: "thinkmate"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "thinkmate.co.tz"

website:
  homepage: "https://thinkmate.co.tz/"
  tender_url: "https://thinkmate.co.tz/ict-procurement.html"

contact:
  email: "admin@thinkmate.co.tz"
  alternate_emails:
    - "info@htmlstream.com"
  phone: "+255 762354679 "

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Page ict-procurement.html is an IT procurement product catalog (Lenovo, Dell, HP hardware),
    NOT a tender/RFP listing. No tender notices found. Documents present are company
    profiles (e.g. thinkmate.co.tz/*.pdf) - not tender documents. Disable until
    institution publishes actual tender notices.
  selectors:
    container: "section#shop-p1, .shop-p1, .business-growth-p1"
    tender_item: ".card"
    title: ".card-title a, h1, h3"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ""
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
      - "/"

    url_patterns:
      - "thinkmate.co.tz/*.pdf"

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
      Page contains product catalog, not tenders. Documents at root (e.g. our Company
      privacy Policy.pdf, Thinkmate LTD Company Profile.pdf) are company docs, not RFP.

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
  twitter: "thinkmatetz"
  instagram: "thinkmatetz"

notes: |
  Thinkmate offers custom software development, IT advisory, cybersecurity, and more. Contact us for expert IT solutions in Tanzania.
---

# Managed IT Service Provider | Broadband Providers in Tanzania

**Category:** Commercial / Private Sector
**Website:** https://thinkmate.co.tz/
**Tender Page:** https://thinkmate.co.tz/ict-procurement.html
**Keywords Found:** procurement

## Contact Information
- Email: admin@thinkmate.co.tz
- Email: info@htmlstream.com
- Phone: +255 762354679 
- Phone: 0754710970

## Scraping Instructions

**Strategy:** Scrape https://thinkmate.co.tz/ict-procurement.html for tender/procurement notices.
**Method:** http_get

Thinkmate offers custom software development, IT advisory, cybersecurity, and more. Contact us for expert IT solutions in Tanzania.

### Tender Content Preview

> IT Procurement ESG,Land&GIS Services <a class="dropdown-item" href="ai-bot.htm

### Known Tender URLs

- https://thinkmate.co.tz/ict-procurement.html

### Document Links Found

- https://thinkmate.co.tz/our Company privacy Policy.pdf
- https://thinkmate.co.tz/Thinkmate LTD Company Profile.. .pdf

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
thinkmate/
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
- **Signal Strength:** Strong (procurement)
