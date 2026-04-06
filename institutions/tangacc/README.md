---
institution:
  name: "Home &#124; Tanga City Council"
  slug: "tangacc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "tangacc.go.tz"

website:
  homepage: "https://tangacc.go.tz/"
  tender_url: "https://tangacc.go.tz/tenders"

contact:
  email: "info@tangacc.go.tz"
  phone: "018-06-30"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://tangacc.go.tz/tenders for Tanga City Council zabuni. Same October CMS as tanga.go.tz. Documents in /storage/app/uploads/public/ with hash paths."
  selectors:
    container: ".content-border, .sub-main-content, main, .container, .row"
    tender_item: "table.table tbody tr, .tender-item, article, .list-item"
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

    url_patterns:
      - "tangacc.go.tz/storage/app/uploads/public/5c2/9dc/be8/5c29dcbe8a5a8530224195.pdf"
      - "tangacc.go.tz/storage/app/uploads/public/5cd/e6f/7f4/5cde6f7f474c6693131259.pdf"
      - "tangacc.go.tz/storage/app/uploads/public/648/974/251/6489742517735429919914.pdf"
      - "tangacc.go.tz/storage/app/uploads/public/5cd/e6e/dcb/5cde6edcb0a15890744002.pdf"
      - "tangacc.go.tz/storage/app/uploads/public/5c4/6f6/a32/5c46f6a3254f8840821364.pdf"

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

    known_document_paths:
      - "/storage/app/uploads/public/"
    document_notes: |
      October CMS. Documents in /storage/app/uploads/public/{hash}/{hash}.pdf. Same structure as tanga.go.tz. Tender listing may use table or list format.

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
  facebook: "tanga.citycouncil.3"
  twitter: "TangaCC"
  instagram: "tanga_jiji"

notes: |
  A default home page
---

# Home &#124; Tanga City Council

**Category:** Local Government Authority
**Website:** https://tangacc.go.tz/
**Tender Page:** https://tangacc.go.tz/new/mkurugenzi-jiji-la-tanga-akabidhi-gari-nne-mpya-kwa-idara-na-vitengo
**Keywords Found:** bid, manunuzi, supply, tender, tenders, zabuni

## Contact Information
- Email: info@tangacc.go.tz
- Phone: 018-06-30
- Phone: 025
          
- Phone: 022-08-31
- Phone: 012-08-01 --- 
- Phone: 017-10-02

## Scraping Instructions

**Strategy:** Scrape https://tangacc.go.tz/new/mkurugenzi-jiji-la-tanga-akabidhi-gari-nne-mpya-kwa-idara-na-vitengo for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> "home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://tangacc.go.tz/new/mkurugenzi-jiji-la-tanga-akabidhi-gari-nne-mpya-kwa-idara-na-vitengo
- https://tangacc.go.tz/tenders

### Document Links Found

- https://tangacc.go.tz/storage/app/uploads/public/5cd/e6e/dcb/5cde6edcb0a15890744002.pdf
- https://tangacc.go.tz/storage/app/uploads/public/67c/b09/715/67cb09715ab68169968803.pdf
- http://tangacc.go.tz/storage/app/uploads/public/5c4/6f6/a32/5c46f6a3254f8840821364.pdf
- https://tangacc.go.tz/storage/app/uploads/public/648/974/251/6489742517735429919914.pdf
- https://tangacc.go.tz/storage/app/uploads/public/648/974/a36/648974a36d8cc929932716.pdf
- https://tangacc.go.tz/storage/app/uploads/public/5cd/e6f/7f4/5cde6f7f474c6693131259.pdf
- https://tangacc.go.tz/storage/app/uploads/public/648/975/0ea/6489750eaef5b430314288.pdf
- http://tangacc.go.tz/storage/app/uploads/public/5c2/9dc/be8/5c29dcbe8a5a8530224195.pdf
- https://tangacc.go.tz/storage/app/uploads/public/63e/e16/2b0/63ee162b012db579316660.pdf

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

Known document paths: /storage/app/uploads/public/5c2/9dc/be8/5c29dcbe8a5a8530224195.pdf, /storage/app/uploads/public/5cd/e6f/7f4/5cde6f7f474c6693131259.pdf, /storage/app/uploads/public/648/974/251/6489742517735429919914.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tangacc/
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
- **Signal Strength:** Strong (manunuzi, tender, tenders, zabuni)
