---
institution:
  name: "Agricom Africa: Empowering Agribusiness in Tanzania"
  slug: "agricom"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "agricom.co.tz"

website:
  homepage: "https://agricom.co.tz/"
  tender_url: "https://agricom.co.tz/"

contact:
  email: "info@agricom.co.tz"
  phone: "+25569 999 7998"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Remix SPA — content loaded client-side. /positions returns 404 catch-all. Farm mechanization company with e-commerce at /shop. No procurement/tender section found. Static curl fetch returns shell HTML only; may need headless browser for full content."
  selectors:
    container: "main, [data-astro], #root"
    tender_item: "article, [class*='card'], [class*='item']"
    title: "h2, h3, h4, a"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: "a[href*='page'], button[class*='load']"
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
      - "agricom.co.tz/*.pdf"

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
      Remix SPA - HTML is minimal on initial load. Content in /assets/. Shop at agricom.co.tz/shop. No procurement documents found. /positions is not a valid route.

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
  facebook: "agricomafrica"
  linkedin: "agricom-africa-ltd."
  instagram: "agricomafrica"

notes: |
  Discover Agricom Africa, a leader in innovative agribusiness solutions in Tanzania. 
                We provide a comprehensive range of products and services, enhancing food and nutrition security through cutting-edge technology and expert support. 
                From farm to folk, we manage the entire supply chain, ensuring farmers have the tools to boost productivity and connect with global markets.
---

# Agricom Africa: Empowering Agribusiness in Tanzania

**Category:** Commercial / Private Sector
**Website:** https://agricom.co.tz/
**Tender Page:** https://agricom.co.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Email: info@agricom.co.tz
- Phone: +25569 999 7998
- Phone: 0321456 18
- Phone: 0504723 19
- Phone: 055 15 17
- Phone: 0 1 0 0-6 3 3 0

## Scraping Instructions

**Strategy:** Scrape https://agricom.co.tz/ for tender/procurement notices.
**Method:** http_get

Discover Agricom Africa, a leader in innovative agribusiness solutions in Tanzania. 
                We provide a comprehensive range of products and services, enhancing food and nutrition security through cutting-edge technology and expert support. 
                From farm to folk, we manage the entire supply chain, ensuring farmers have the tools to boost productivity and connect with global markets.

### Tender Content Preview

> tions, agricultural machinery, farming technology, productivity enhancement, farm gate procurement"/> <link rel="stylesheet" href="/assets/inde

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
agricom/
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
- **Active Tenders:** 0
- **Signal Strength:** Weak (Remix SPA, no procurement section found)
