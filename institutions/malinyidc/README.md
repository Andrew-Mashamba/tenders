---
institution:
  name: "Malinyi District Council"
  slug: "malinyidc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "malinyidc.go.tz"

website:
  homepage: "https://malinyidc.go.tz/"
  tender_url: "https://malinyidc.go.tz/manunuzi"

contact:
  email: "ded@malinyidc.go.tz"
  alternate_emails:
    - "www.ict@ajira.go.tz"
  phone: "017-04-03 --- "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://malinyidc.go.tz/manunuzi (Manunuzi/Zabuni). October CMS with Mikumi theme. Tenders in .right-sidebar-content; documents at /storage/app/uploads/public/."
  selectors:
    container: ".right-sidebar-content, .publications-listing"
    tender_item: "ul.publications-listing li, ul.publications-listing > *, .right-sidebar-content article"
    title: "a p, a, h3, h4"
    date: "span, .date"
    document_link: 'a[href*="storage"][href$=".pdf"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: ".pagination a, a.next"
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
      - "/storage/app/uploads/public/"

    url_patterns:
      - "malinyidc.go.tz/storage/app/uploads/public/*/*/*/*.pdf"

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
      October CMS stores documents at /storage/app/uploads/public/{hash}/{hash}/{hash}/{hash}.pdf. Same structure as other .go.tz district councils.

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

# Home &#124; Malinyi District Council

**Category:** Local Government Authority
**Website:** https://malinyidc.go.tz/
**Tender Page:** https://malinyidc.go.tz/manunuzi
**Keywords Found:** bid, manunuzi, tender, tenders, zabuni

## Contact Information
- Email: ded@malinyidc.go.tz
- Email: www.ict@ajira.go.tz
- Phone: 017-04-03 --- 
- Phone: 017-03-25
- Phone: 0252026-3
- Phone: 0643111999 
- Phone: 017-03-26

## Scraping Instructions

**Strategy:** Scrape https://malinyidc.go.tz/manunuzi for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ome-page-title">Zabuni Zaidi Tender Name

### Known Tender URLs

- https://malinyidc.go.tz/manunuzi
- https://malinyidc.go.tz/new/meneja-nmb-kanda-ya-kati-akabidhi-msaada-wa-viti-na-meza-100-pamoja-na-madawati-100-kwa-mkuu-wa-wilaya-ya-malinyi
- https://malinyidc.go.tz/tenders

### Document Links Found

- https://malinyidc.go.tz/storage/app/uploads/public/58d/772/8b2/58d7728b24fef273819231.pdf
- https://malinyidc.go.tz/storage/app/uploads/public/58d/770/a74/58d770a74852f969420114.pdf
- https://malinyidc.go.tz/storage/app/uploads/public/58d/771/d9a/58d771d9a5ec4517687945.pdf
- https://malinyidc.go.tz/storage/app/uploads/public/58d/76f/d24/58d76fd247c49294119767.pdf
- https://malinyidc.go.tz/storage/app/uploads/public/58d/771/994/58d771994cc5e957833845.pdf

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

Known document paths: /storage/app/uploads/public/58d/772/8b2/58d7728b24fef273819231.pdf, /storage/app/uploads/public/58d/770/a74/58d770a74852f969420114.pdf, /storage/app/uploads/public/58d/771/d9a/58d771d9a5ec4517687945.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
malinyidc/
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
