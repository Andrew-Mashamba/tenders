---
institution:
  name: "Singida District Council"
  slug: "singidadc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "singidadc.go.tz"

website:
  homepage: "https://singidadc.go.tz/"
  tender_url: "https://singidadc.go.tz/tenders"

contact:
  email: "ded.singidadc@singida.go.tz"
  phone: "023-03-16"

scraping:
  enabled: true
  method: "http_get"
  strategy: "October CMS. Scrape /tenders. Tenders in .right-sidebar-container as a[href*='/announcement/'] links. Follow to /announcement/{slug} for documents. Table may be empty; use sidebar announcement links."
  selectors:
    container: ".right-sidebar-content"
    tender_item: ".right-sidebar-container a[href*='/announcement/']"
    title: "a"
    date: "span"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href*="/storage/app/uploads/"]'
    pagination: "a.view-all[href*='announcements']"
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
      - "singidadc.go.tz/storage/app/uploads/public/*"
      - "singidadc.go.tz/announcement/*"

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
      October CMS. Documents at /storage/app/uploads/public/. Follow announcement detail pages for PDF links.

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
  facebook: "singidadc"
  twitter: "singidadc"
  instagram: "singidahalmashauri"

notes: |
  A default home page
---

# Home &#124; Singida District Council

**Category:** Local Government Authority
**Website:** https://singidadc.go.tz/
**Tender Page:** https://singidadc.go.tz/new/halmashauri-ya-wilaya-ya-singida-yakabidhi-vifaa-vya-ufugaji-nyuki-kwa-vikundi-vya-vijana
**Keywords Found:** bid, procurement, tender, tenders, zabuni

## Contact Information
- Email: ded.singidadc@singida.go.tz
- Phone: 023-03-16
- Phone: 022-06-01 --- 
- Phone: 0222023-2
- Phone: 022-12-01 --- 
- Phone: 0385500407

## Scraping Instructions

**Strategy:** Scrape https://singidadc.go.tz/new/halmashauri-ya-wilaya-ya-singida-yakabidhi-vifaa-vya-ufugaji-nyuki-kwa-vikundi-vya-vijana for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ome-page-title">Zabuni Zaidi Jina la zabuni

### Known Tender URLs

- https://singidadc.go.tz/new/halmashauri-ya-wilaya-ya-singida-yakabidhi-vifaa-vya-ufugaji-nyuki-kwa-vikundi-vya-vijana
- https://singidadc.go.tz/procurement-management
- https://singidadc.go.tz/tenders

### Document Links Found

- https://singidadc.go.tz/storage/app/uploads/public/651/3c4/4db/6513c44dbcfb8285905423.pdf
- https://singidadc.go.tz/storage/app/uploads/public/68e/36c/b75/68e36cb7523f0385500407.pdf
- https://singidadc.go.tz/storage/app/uploads/public/5ae/358/eac/5ae358eacbde1516294812.pdf
- https://singidadc.go.tz/storage/app/uploads/public/5ac/b03/199/5acb03199dbfb409306707.pdf

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

Known document paths: /storage/app/uploads/public/651/3c4/4db/6513c44dbcfb8285905423.pdf, /storage/app/uploads/public/68e/36c/b75/68e36cb7523f0385500407.pdf, /storage/app/uploads/public/5ae/358/eac/5ae358eacbde1516294812.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
singidadc/
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
- **Signal Strength:** Strong (procurement, tender, tenders, zabuni)
