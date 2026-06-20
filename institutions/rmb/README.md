---
institution:
  name: "RMB - a leading African Corporate and Investment Bank"
  slug: "rmb"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "rmb.co.tz"

website:
  homepage: "https://www.rmb.co.za/"
  tender_url: "https://grid.rmb.co.za/Default.aspx?tabid=57&returnurl=%2f"

contact:
  email: "info@rmb.co.za"
  phone: "000304973 0 0"

scraping:
  enabled: true
  method: "http_get"
  strategy: "RMB grid site still returns HTTP 503 Service Unavailable (checked June 2026). Retry periodically. Tender URL: https://grid.rmb.co.za/Default.aspx?tabid=57"
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" 
  schedule: "daily"

  anti_bot:
    requires_javascript: true
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
      - "rmb.co.tz/files/pdf/legal/firstRand-group-supplier-and-business-partner-privacy-notice.pdf"
      - "rmb.co.tz/files/pdf/legal/Code-of-Conduct-for-the-BASA.pdf"

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
      Site currently 503. When available: documents at assets.rmb.co.za/files/pdf/legal/. ASP.NET site may require JavaScript for tender listing.

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
  facebook: "RMBCIB"
  twitter: "RMBCIB"
  linkedin: "rand-merchant-bank"
  instagram: "rmb_cib"

notes: |
  We harness our curious minds to unlock opportunity &amp; create innovative solutions
---

# RMB - a leading African Corporate and Investment Bank

**Category:** Commercial / Private Sector
**Website:** https://www.rmb.co.za/
**Tender Page:** https://grid.rmb.co.za/Default.aspx?tabid=57&returnurl=%2f
**Keywords Found:** bid

## Contact Information
- Email: info@rmb.co.za
- Phone: 000304973 0 0
- Phone: 000304973 14 0
- Phone: 03-01-2019
- Phone: 000304973 0
- Phone: 0003 14 8

## Scraping Instructions

**Strategy:** Scrape https://grid.rmb.co.za/Default.aspx?tabid=57&returnurl=%2f for tender/procurement notices.
**Method:** http_get

We harness our curious minds to unlock opportunity &amp; create innovative solutions

### Known Tender URLs

- https://grid.rmb.co.za/Default.aspx?tabid=57&returnurl=%2f
- https://grid.rmb.co.za/Default.aspx?tabid=57&returnurl=%2fDefault.aspx%3ftabid%3d89%26goto%3dgmresearchportal%2findex.asp

### Document Links Found

- https://assets.rmb.co.za/files/pdf/legal/Code-of-Conduct-for-the-BASA.pdf
- https://assets.rmb.co.za/files/pdf/legal/firstRand-group-supplier-and-business-partner-privacy-notice.pdf

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

Known document paths: /files/pdf/legal/firstRand-group-supplier-and-business-partner-privacy-notice.pdf, /files/pdf/legal/Code-of-Conduct-for-the-BASA.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
rmb/
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

- **Last Checked:** 11 June 2026
- **Active Tenders:** Unknown (grid.rmb.co.za HTTP 503)
- **Signal Strength:** Weak (site unavailable)
