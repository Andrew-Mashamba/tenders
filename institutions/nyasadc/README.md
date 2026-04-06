---
institution:
  name: "Nyasa District Council"
  slug: "nyasadc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "nyasadc.go.tz"

website:
  homepage: "https://nyasadc.go.tz/"
  tender_url: "https://nyasadc.go.tz/manunuzi-na-ugavi"

contact:
  email: "ps.ded@nyasadc.go.tz"
  phone: "025 -2952003 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /manunuzi-na-ugavi (Procurement and Supply) and /tenders. Tender ads at /advertisement/{slug}. Documents in /storage/app/uploads/public/{hash}/. Follow links to advertisement detail pages for full tender docs."
  selectors:
    container: "main, .content, .page-content, section containing tenders"
    tender_item: "a[href*='/advertisement/'], .tender-item, article, li"
    title: "h2, h3, h4, .tender-title, a[href*='/advertisement/']"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href*="/storage/app/uploads/"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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
        - 'a[href*="/storage/app/uploads/"]'
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
      - "/storage/app/uploads/public/"
      - "/storage/app/media/uploaded-files/"

    url_patterns:
      - "nyasadc.go.tz/storage/app/uploads/public/*/*.pdf"
      - "nyasadc.go.tz/storage/app/uploads/public/*/*/*.pdf"

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
      Documents in /storage/app/uploads/public/{3-char}/{3-char}/{3-char}/{hash}.pdf. October CMS style paths. Tender ads link to advertisement detail pages with PDF attachments.

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
  A default home page
---

# Home &#124; Nyasa District Council

**Category:** Local Government Authority
**Website:** https://nyasadc.go.tz/
**Tender Page:** https://nyasadc.go.tz/manunuzi-na-ugavi
**Keywords Found:** manunuzi, procurement, quotation, supply, tender, tenders, zabuni

## Contact Information
- Email: ps.ded@nyasadc.go.tz
- Phone: 025 -2952003 
- Phone: 01242-14904585
- Phone: 016 - 2019

## Scraping Instructions

**Strategy:** Scrape https://nyasadc.go.tz/manunuzi-na-ugavi for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> href="https://nyasadc.go.tz/manunuzi-na-ugavi" > Procurement and Supply <a

### Known Tender URLs

- https://nyasadc.go.tz/manunuzi-na-ugavi
- https://nyasadc.go.tz/tenders
- https://nyasadc.go.tz/advertisement/tangazo-la-zabuni-ya-utengenezaji-wa-nguzo-za-barabara-za-anuani-za-makazi

### Document Links Found

- https://nyasadc.go.tz/storage/app/uploads/public/5cf/0f0/f83/5cf0f0f8355a3533625786.pdf
- https://nyasadc.go.tz/storage/app/uploads/public/61d/bd0/e29/61dbd0e29ba78568445741.pdf
- https://nyasadc.go.tz/storage/app/uploads/public/5bf/2dc/a46/5bf2dca462f4e924262232.pdf
- https://nyasadc.go.tz/storage/app/uploads/public/5bf/2dd/16d/5bf2dd16def68114184534.pdf
- https://nyasadc.go.tz/storage/app/uploads/public/5bf/2dd/744/5bf2dd744405d173278367.pdf
- https://nyasadc.go.tz/storage/app/uploads/public/5d5/283/66a/5d528366a7afc909371981.pdf
- https://nyasadc.go.tz/storage/app/uploads/public/5fa/97b/222/5fa97b222236d155439789.pdf

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

Known document paths: /storage/app/uploads/public/5bf/2dd/16d/5bf2dd16def68114184534.pdf, /storage/app/uploads/public/61d/bd0/e29/61dbd0e29ba78568445741.pdf, /storage/app/uploads/public/5fa/97b/222/5fa97b222236d155439789.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
nyasadc/
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
- **Signal Strength:** Strong (manunuzi, procurement, tender, tenders, zabuni)
