---
institution:
  name: "Knauf Gypsum Tanzania | Mkuranga II production started - the biggest plasterboards plant in subSaharan Africa |  | German Quality Products Locally produced."
  slug: "knauf"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "knauf.co.tz"

website:
  homepage: "https://knauf.com/en-TZ"
  tender_url: "https://knauf.com/en-TZ"

contact:
  email: "u003eapp-support@knauf.com"
  alternate_emails:
    - "info-tz@knauf.com"
  phone: "026-03-10"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Knauf global site. Tanzania at knauf.com/en-TZ. Region selector first; then country page. Product downloads (tender-text, certificates) may be in product pages. No dedicated tender listing found; check country subpages for procurement."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
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

    known_document_paths:
      - "/media/"
      - "/documents/"
    url_patterns:
      - "knauf.com/*/media/*.pdf"
      - "knauf.com/*/documents/*.pdf"

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
      Global Knauf site; Tanzania uses en-TZ. Product pages have tender-text, certificates, brochures. No Tanzania-specific tender table; may post RFPs on country page.

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
  Knauf Tanzania offers solutions for interior and exterior dry wall systems. Browse our pages to get the latest products and system solutions.
---

# Knauf Gypsum Tanzania | Mkuranga II production started - the biggest plasterboards plant in subSaharan Africa |  | German Quality Products Locally produced.

**Category:** Commercial / Private Sector
**Website:** https://knauf.com/
**Tender Page:** https://knauf.com/
**Keywords Found:** bid, eoi, rfi, rfp, supply, tender

## Contact Information
- Email: u003eapp-support@knauf.com
- Email: info-tz@knauf.com
- Phone: 026-03-10
- Phone: 097348515
- Phone: 024-10-14
- Phone: 06-4297-8
- Phone: +255 766 805 140 

## Scraping Instructions

**Strategy:** Scrape https://knauf.com/ for tender/procurement notices.
**Method:** http_get

Knauf Tanzania offers solutions for interior and exterior dry wall systems. Browse our pages to get the latest products and system solutions.

### Tender Content Preview

> ificate":"Certificate","environmental-product-declaration-epd":"Environmental Product Declaration","tender-text":"Tender Text","fire-classification-report":"Fire Classification Report","flyer":"Flyer","brochure":"Brochure","catalogue":"Catalogue","pricelist":"Price List","advertisment":"Advertisemen

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
knauf/
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
- **Signal Strength:** Strong (eoi, rfp, tender)
