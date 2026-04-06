---
institution:
  name: "Public Procurement Regulatory Authority (PPRA)"
  slug: "ppra"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "ppra.go.tz"

website:
  homepage: "https://ppra.go.tz/"
  tender_url: "https://ppra.go.tz/"

contact:
  email: "zm.coast@ppra.go.tz"
  alternate_emails:
    - "zm.western@ppra.go.tz"
    - "zm.southern@ppra.go.tz"
    - "zm.lake@ppra.go.tz"
    - "zm.northern@ppra.go.tz"
  phone: "026
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape PPRA homepage for Public Notices, Announcements, and Publications. Documents at /uploads/documents/ with format en-{timestamp}-{filename}.pdf. PPRA publishes regulations, acts, debarment notices - not traditional tenders but procurement-related. Follow /announcements and /publications links."
  selectors:
    container: ".content, main, .region-content, .block-content"
    tender_item: ".views-row, article, .announcement-item, .publication-item"
    title: "h2, h3, h4, .field--name-title, a"
    date: ".date, .field--name-created, time"
    document_link: 'a[href$=".pdf"], a[href*="/uploads/documents/"]'
    pagination: ".pager a, .pagination a" 
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
      - "/uploads/documents/"
    url_patterns:
      - "ppra.go.tz/uploads/documents/*.pdf"

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
      Documents at /uploads/documents/ with format en-{timestamp}-{filename}.pdf. PPRA publishes Public Notices (debarments), Acts, Regulations. Scrape /announcements and /publications?category_slug= for document links.

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
  facebook: "people"
  twitter: "PpraTanzania"
  instagram: "ppra_tanzania"

notes: |
  Government Website | Tovuti ya Serikali
---

# PPRA |   Home

**Category:** Government Agency
**Website:** https://ppra.go.tz/
**Tender Page:** https://ppra.go.tz/uploads/documents/en-1736861173-THE PUBLIC PROCUREMENT ACT.pdf
**Keywords Found:** bid, procurement, tender, tenders

## Contact Information
- Email: zm.coast@ppra.go.tz
- Email: zm.western@ppra.go.tz
- Email: zm.southern@ppra.go.tz
- Email: zm.lake@ppra.go.tz
- Email: zm.northern@ppra.go.tz
- Phone: 026
          
- Phone: 026 216 0010
- Phone: 00064317954420

## Scraping Instructions

**Strategy:** Scrape https://ppra.go.tz/uploads/documents/en-1736861173-THE PUBLIC PROCUREMENT ACT.pdf for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Government Website | Tovuti ya Serikali

### Tender Content Preview

> ive Proposals Tenders and Proposal Debarment Guidelines <a class='drop-item'

### Known Tender URLs

- https://ppra.go.tz/uploads/documents/en-1736861173-THE PUBLIC PROCUREMENT ACT.pdf
- https://ppra.go.tz/news/ppra-director-general-encourages-women-taxpayers-to-utilize-tender-opportunities-through-nest
- https://ppra.go.tz/uploads/documents/en-1675173759-Public_Procurement_Act_2011.pdf
- https://ppra.go.tz/publications?category_slug=public-procurement-regulations
- https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms
- https://ppra.go.tz/news/procurement-through-nest-saves-over-35bn-cuts-carbon-emissions
- https://ppra.go.tz/uploads/documents/en-1693207350-GN.557 Public Procurement (Amendment) Regulations, 2018.pdf
- https://ppra.go.tz/publications/guide-for-registration-of-bidders-of-common-use-items-and-services-on-nest

### Document Links Found

- https://ppra.go.tz/uploads/documents/en-1736861173-THE PUBLIC PROCUREMENT ACT.pdf
- https://ppra.go.tz/uploads/documents/en-1767290203-PUBLIC NOTICE (6).pdf
- https://ppra.go.tz/uploads/documents/en-1766741278-Public Notice (5).pdf
- https://ppra.go.tz/uploads/documents/en-1675175047-ppa2004_1.pdf
- https://ppra.go.tz/uploads/documents/en-1675261693-GNNO12~1.PDF
- https://ppra.go.tz/uploads/documents/en-1675173759-Public_Procurement_Act_2011.pdf
- https://ppra.go.tz/uploads/documents/en-1719922256-GN NO518 OF 2024- KANUNI ZA UNUNUZI WA UMMA ZA MWAKA 2024.pdf
- https://ppra.go.tz/uploads/documents/en-1766741252-Public Notice (5).pdf
- https://ppra.go.tz/uploads/documents/en-1693207350-GN.557 Public Procurement (Amendment) Regulations, 2018.pdf

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

Known document paths: /uploads/documents/en-1675261693-GNNO12~1.PDF, /uploads/documents/en-1675175047-ppa2004_1.pdf, /uploads/documents/en-1675173759-Public_Procurement_Act_2011.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
ppra/
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
- **Signal Strength:** Strong (procurement, tender, tenders)
