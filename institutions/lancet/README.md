---
institution:
  name: "Cerba Lancet Africa"
  slug: "lancet"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "lancet.co.tz"

website:
  homepage: "https://cerbalancetafrica.com/"
  tender_url: "https://cerbalancetafrica.com/"

contact:
  email: "info@cerbalancetafrica.com"
  phone: "0 592 7505"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Pathology/diagnostics company. Homepage has services, news, network - no tender listing. CSS has p.tender-text but no tender content found. Documents at /media/. Re-enable if they add /tenders or /procurement."
  selectors:
    container: "main, .container, .rich-text"
    tender_item: ".ServiceItem, .event-block, article"
    title: "h2, h3, h4, .tender-text"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href*="/media/"], a.download-button'
    pagination: ".pagination a" 
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
      - "lancet.co.tz/media/0vlhum3i/paia-manual-cerba-lancet-africa-2024.pdf"

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
      Documents at /media/{hash}/{filename}.pdf. No tender listing. PAIA manual found. Disabled until tender section added.

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
  facebook: "lancetlabstanzania"
  twitter: "lancet_tanzania"
  linkedin: "cerba-lancet-africa"
  instagram: "lancetlabstanzania"

notes: |
  Lancet Laboratories Tanzania is part of the Cerba Lancet Africa Group of Laboratories. To make diagnostics more accessible, we provide home and office visit services in Dar es Salaam and other regions, with specimen collection carried out by our team of highly trained phlebotomists. Whether you&#x2019;re a healthcare professional or a private individual, Lancet Laboratories Tanzania ensures that convenient, reliable testing is always within reach.
---

# Cerba Lancet Tanzania | Our Footprint is in Africa  | Cerba Lancet Africa

**Category:** Commercial / Private Sector
**Website:** https://cerbalancetafrica.com/
**Tender Page:** https://cerbalancetafrica.com/
**Keywords Found:** bid, rfi, tender

## Contact Information
- Email: info@cerbalancetafrica.com
- Phone: 0 592 7505

## Scraping Instructions

**Strategy:** Scrape https://cerbalancetafrica.com/ for tender/procurement notices.
**Method:** http_get

Lancet Laboratories Tanzania is part of the Cerba Lancet Africa Group of Laboratories. To make diagnostics more accessible, we provide home and office visit services in Dar es Salaam and other regions, with specimen collection carried out by our team of highly trained phlebotomists. Whether you&#x2019;re a healthcare professional or a private individual, Lancet Laboratories Tanzania ensures that convenient, reliable testing is always within reach.

### Tender Content Preview

> and (max-width: 436px){ h2{ font-size: 2em; } a.btn.country { width: 100%; } } p.tender-text { min-height: 120px; } <script id="Cookiebot" data-cbid="97d155d8-984e-4e09-9de8-71c939ac9ebc" data-blockingmode="auto" type="text/javascript" src="https://con

### Document Links Found

- https://cerbalancetafrica.com/media/0vlhum3i/paia-manual-cerba-lancet-africa-2024.pdf

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

Known document paths: /media/0vlhum3i/paia-manual-cerba-lancet-africa-2024.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
lancet/
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
