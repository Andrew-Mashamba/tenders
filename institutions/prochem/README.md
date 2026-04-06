---
institution:
  name: "Prochem - Tanzania's Leading Chemical Distributors"
  slug: "prochem"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "prochem.co.tz"

website:
  homepage: "https://prochem.co.tz/"
  tender_url: "https://prochem.co.tz/#procurement"

contact:
  email: "sales@prochem.co.tz"
  phone: "+255 629 780 734"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Site has no dedicated tender listing. The #procurement section describes company services (Global Procurement, International Logistics), not tender notices. No tender items or document links found in HTML."
  selectors:
    container: ".service-section-s2"
    tender_item: ".service-grids .grid"
    title: "h4 a, h4"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" 
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
      - "prochem.co.tz/*.pdf"

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
      No tender documents found. Site is a marketing/corporate site. Assets stored under /assets/images/ and /assets/css/. No tender-specific document paths.

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
  facebook: "ProchemTZ"
  linkedin: "prochem-trading-limited"
  instagram: "prochem_tz"

notes: |
  We are chemical and commodity trading company based in Dar Es Salaam, Tanzania. Suppliers of high-quality &amp; wide range of polymers, industrial and mining chemicals. When you think of Chemicals in Dar es Salaam, Tanzania. Think Chemicals Think of Us.
---

# Prochem - Tanzania&#039;s Leading Chemical Distributors

**Category:** Commercial / Private Sector
**Website:** https://prochem.co.tz/
**Tender Page:** https://prochem.co.tz/#procurement
**Keywords Found:** procurement, quotation, rfi, supply

## Contact Information
- Email: sales@prochem.co.tz
- Phone: +255 629 780 734
- Phone: +255 757 753 473
- Phone: +255 626 422 174
- Phone: 0 0 100 100
- Phone: +255 22 292 3576

## Scraping Instructions

**Strategy:** Scrape https://prochem.co.tz/#procurement for tender/procurement notices.
**Method:** http_get

We are chemical and commodity trading company based in Dar Es Salaam, Tanzania. Suppliers of high-quality &amp; wide range of polymers, industrial and mining chemicals. When you think of Chemicals in Dar es Salaam, Tanzania. Think Chemicals Think of Us.

### Tender Content Preview

> Global Procurement International Logistics <a href="https://pr

### Known Tender URLs

- https://prochem.co.tz/#procurement

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
prochem/
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
