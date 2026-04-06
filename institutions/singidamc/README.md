---
institution:
  name: "Singida Municipal Council"
  slug: "singidamc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "singidamc.go.tz"

website:
  homepage: "https://singidamc.go.tz/"
  tender_url: "https://singidamc.go.tz/tenders"

contact:
  email: "md.singidamc@singida.go.tz"
  phone: "067321357291"

scraping:
  enabled: true
  method: "http_get"
  strategy: "October CMS. Scrape /tenders. Page has table.table-striped (may be empty) and .right-sidebar-container with a[href*='/announcement/'] links. Follow to /announcement/{slug} for documents."
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
      - "singidamc.go.tz/storage/app/uploads/public/*"
      - "singidamc.go.tz/announcement/*"

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

notes: |
  A default home page
---

# Home &#124; Singida Municipal Council

**Category:** Local Government Authority
**Website:** https://singidamc.go.tz/
**Tender Page:** https://singidamc.go.tz/tenders
**Keywords Found:** bid, manunuzi, tender, tenders, zabuni

## Contact Information
- Email: md.singidamc@singida.go.tz
- Phone: 067321357291
- Phone: 023-05-02 --- 
- Phone: 025-07-01
- Phone: 0222023-4
- Phone: 023-04-10 --- 

## Scraping Instructions

**Strategy:** Scrape https://singidamc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ome-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://singidamc.go.tz/tenders

### Document Links Found

- https://singidamc.go.tz/storage/app/uploads/public/62c/7fc/4b3/62c7fc4b36454209355172.pdf
- https://singidamc.go.tz/storage/app/uploads/public/62f/a5e/4f3/62fa5e4f3c2cc485799861.pdf
- https://singidamc.go.tz/storage/app/uploads/public/656/99f/ef7/65699fef7d067321357291.pdf
- https://singidamc.go.tz/storage/app/uploads/public/624/074/333/6240743334ad3918175683.pdf
- https://singidamc.go.tz/storage/app/uploads/public/66f/28c/0fc/66f28c0fc4fb1683255209.pdf

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

Known document paths: /storage/app/uploads/public/62c/7fc/4b3/62c7fc4b36454209355172.pdf, /storage/app/uploads/public/624/074/333/6240743334ad3918175683.pdf, /storage/app/uploads/public/66f/28c/0fc/66f28c0fc4fb1683255209.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
singidamc/
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
