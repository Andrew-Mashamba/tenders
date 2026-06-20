---
institution:
  name: "Mamlaka ya Rufani ya Zabuni za Umma (PPAA - Public Procurement Appeals Authority)"
  slug: "ppaa"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "ppaa.go.tz"

website:
  homepage: "https://ppaa.go.tz/"
  tender_url: "https://ppaa.go.tz/"

contact:
  email: "es@ppaa.go.tz"
  phone: "0544563322"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape PPAA homepage and news for bulletins and procurement documents. Documents at /uploads/documents/ with format sw-{timestamp}-{filename}.pdf. PPAA publishes bulletins and regulatory docs; follow news links and document links."
  selectors:
    container: ".content, main, .page-content, article"
    tender_item: "article, .news-item, .document-item, .card"
    title: "h2, h3, h4, .title, a"
    date: ".date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href*="/uploads/documents/"]'
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
      - "/uploads/documents/"
    url_patterns:
      - "ppaa.go.tz/uploads/documents/*.pdf"

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
      Documents at /uploads/documents/ with format sw-{timestamp}-{filename}.pdf. PPAA bulletins and regulatory docs. Site may be slow to respond.

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
  facebook: "ppaa_tz"
  twitter: "ppaa_tz"
  instagram: "ppaa_tz"

notes: |
  Mamlaka ya Rufani ya zabuni za Umma |     Mamlaka ya Rufani ya Zabuni za Umma - Mwanzo
---

# PPAA |     Mamlaka ya Rufani ya Zabuni za Umma - Mwanzo

**Category:** Government Agency
**Website:** https://ppaa.go.tz/
**Tender Page:** https://ppaa.go.tz/news/public-procurement-act-2023
**Keywords Found:** manunuzi, procurement, tender, zabuni

## Contact Information
- Email: es@ppaa.go.tz
- Phone: 0544563322
- Phone: 0743505505
- Phone: +255262962411
- Phone: 09183286356124

## Scraping Instructions

**Strategy:** Scrape https://ppaa.go.tz/news/public-procurement-act-2023 for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Mamlaka ya Rufani ya zabuni za Umma |     Mamlaka ya Rufani ya Zabuni za Umma - Mwanzo

### Tender Content Preview

> a Umma | Mamlaka ya Rufani ya Zabuni za Umma - Mwanzo "> <meta name="theme-

### Known Tender URLs

- https://ppaa.go.tz/news/public-procurement-act-2023

### Document Links Found

- https://ppaa.go.tz/uploads/documents/sw-1753722788-ppaa bulettin April-June-2025 (1).pdf
- https://ppaa.go.tz/uploads/documents/sw-1768551086-ORGANIZATION STRUCTURE.pdf
- https://ppaa.go.tz/uploads/documents/sw-1769498939-PPAA Bulettin Oct - Dec 2025.pdf
- https://ppaa.go.tz/uploads/documents/sw-1746369018-PPAA Bulettin Na-3-Oktoba-Desemba-2024-FINAL.pdf
- https://ppaa.go.tz/uploads/documents/sw-1762328506-PPAA Bulettin July - Sept-2025 Final.pdf

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

Known document paths: /uploads/documents/en-1768551086-ORGANIZATION%20STRUCTURE.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
ppaa/
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
- **Active Tenders:** 0 (publishes appeal bulletins, not procurement tenders)
- **Signal Strength:** Strong (manunuzi, procurement, tender, zabuni)
