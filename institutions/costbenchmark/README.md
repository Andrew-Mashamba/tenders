---
institution:
  name: "Costbenchmark | Leading Quantity Surveyors in Tanzania"
  slug: "costbenchmark"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "costbenchmark.co.tz"

website:
  homepage: "https://costbenchmark.co.tz/"
  tender_url: "https://costbenchmark.co.tz/services.php#procurement"

contact:
  email: "info@costbenchmark.co.tz"
  phone: "0457 15 5"

scraping:
  enabled: false
  method: "http_get"
  strategy: "services.php contains only service descriptions (Cost Estimates, Project Budgets, etc.) — no tender listing or procurement notices. No dedicated tender page found."
  selectors:
    container: "main, .services-section, .services-grid"
    tender_item: ".service-card"
    title: "h3, .service-card h3"
    date: ""
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

    url_patterns:
      - "costbenchmark.co.tz/*.pdf"

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
      No tender listing page exists. services.php is a marketing page describing quantity surveying services. No document paths identified.

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
  Cost Benchmark is an AQRB registered Quantity Surveying firm based in Arusha, Tanzania, providing professional construction cost consultancy services across the country.
---

# Costbenchmark | Leading Quantity Surveyors in Tanzania

**Category:** Commercial / Private Sector
**Website:** https://costbenchmark.co.tz/
**Tender Page:** https://costbenchmark.co.tz/services.php#procurement
**Keywords Found:** bid, procurement, tender

## Contact Information
- Email: info@costbenchmark.co.tz
- Phone: 0457 15 5
- Phone: 046 3 19 3
- Phone: 046 19 19
- Phone: +255 758 012863
 
- Phone: 07989 21 6

## Scraping Instructions

**Strategy:** Scrape https://costbenchmark.co.tz/services.php#procurement for tender/procurement notices.
**Method:** http_get

Cost Benchmark is an AQRB registered Quantity Surveying firm based in Arusha, Tanzania, providing professional construction cost consultancy services across the country.

### Tender Content Preview

> Procurement Management Strategic tender documentation, bid evaluation, and contractor selection processes. Learn more

### Known Tender URLs

- https://costbenchmark.co.tz/services.php#procurement

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
costbenchmark/
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
- **Signal Strength:** Strong (procurement, tender)
