---
institution:
  name: "Singida Regional Website"
  slug: "singida"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "singida.go.tz"

website:
  homepage: "https://singida.go.tz/"
  tender_url: "https://singida.go.tz/procurement-and-supply"

contact:
  email: "info@singida.go.tz"
  alternate_emails:
    - "ras@singida.go.tz"
  phone: "019-12-31"

scraping:
  enabled: true
  method: "http_get"
  strategy: "October CMS site. Scrape .right-sidebar-content for procurement announcements. Each tender is an a[href*='/announcement/'] link. Follow to /announcement/{slug} for detail and documents. Also check /announcements for full list."
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

    url_patterns:
      - "singida.go.tz/storage/app/uploads/public/*"
      - "singida.go.tz/announcement/*"

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
      October CMS. Documents at /storage/app/uploads/public/{hash}/{hash}/{hash}/{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}.pdf. Follow announcement detail pages for document links.

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
  facebook: "singida.rs"

notes: |
  A default home page
---

# Home &#124; Singida Regional Website

**Category:** Government Agency
**Website:** https://singida.go.tz/
**Tender Page:** https://singida.go.tz/procurement-and-supply
**Keywords Found:** manunuzi, procurement, supply, tender, tenders, zabuni

## Contact Information
- Email: info@singida.go.tz
- Email: ras@singida.go.tz
- Phone: 019-12-31
- Phone: 02295798318759
- Phone: 017-07-30
- Phone: 02665350392
- Phone: 017 - 2021

## Scraping Instructions

**Strategy:** Scrape https://singida.go.tz/procurement-and-supply for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> "home-page-title">Zabuni Zaidi Tender Name

### Known Tender URLs

- https://singida.go.tz/procurement-and-supply
- https://singida.go.tz/tenders
- https://singida.go.tz/announcement/general-procurement-notice-for-year-2022-2023-singida-rs

### Document Links Found

- http://www.singida.go.tz/storage/app/uploads/public/590/2f7/d99/5902f7d998ef0486452081.pdf
- https://singida.go.tz/storage/app/uploads/public/67e/8d0/c3b/67e8d0c3b1358114609802.pdf
- https://singida.go.tz/storage/app/uploads/public/673/aed/85b/673aed85b1923534283486.pdf
- https://singida.go.tz/storage/app/uploads/public/698/add/923/698add9231e84994598713.pdf
- https://singida.go.tz/storage/app/uploads/public/67c/030/fd3/67c030fd37843309222668.pdf
- https://singida.go.tz/storage/app/uploads/public/673/aee/4c2/673aee4c24408157557190.pdf
- https://singida.go.tz/storage/app/uploads/public/67d/70c/345/67d70c345bc02665350392.pdf

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

Known document paths: /storage/app/uploads/public/590/2f7/d99/5902f7d998ef0486452081.pdf, /storage/app/uploads/public/673/aed/85b/673aed85b1923534283486.pdf, /storage/app/uploads/public/67c/030/fd3/67c030fd37843309222668.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
singida/
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
