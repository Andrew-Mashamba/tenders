---
institution:
  name: "Rungwe District Council"
  slug: "rungwedc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "rungwedc.go.tz"

website:
  homepage: "https://rungwedc.go.tz/"
  tender_url: "https://rungwedc.go.tz/announcement/mwaliko-wa-zabuni-ujenzi-na-uendeshaji-maduka-kiwira"

contact:
  email: "ded@rungwedc.go.tz"
  phone: "023
	        "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape tender_url for single announcement with document. Also scrape /announcements for listing. Documents in .right-sidebar-content via a.fr-file or a[href*='/storage/']."
  selectors:
    container: ".right-sidebar-content, .middle-content-wrapper"
    tender_item: "a[href*='/announcement/']"
    title: "h1, h2, h4, a"
    date: "span.date, span"
    document_link: 'a.fr-file, a[href*="/storage/app/media/uploaded-files/"], a[href*="/storage/app/uploads/public/"], a[href$=".pdf"]'
    pagination: "a.view-all" 
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
      - "rungwedc.go.tz/storage/app/uploads/public/685/e68/5fa/685e685faaaf9777644704.pdf"
      - "rungwedc.go.tz/storage/app/uploads/public/687/8ad/92d/6878ad92d135c878600765.pdf"
      - "rungwedc.go.tz/storage/app/uploads/public/687/8ae/baa/6878aebaa8364430652829.pdf"
      - "rungwedc.go.tz/storage/app/uploads/public/66a/9f1/a98/66a9f1a98013f412024826.pdf"
      - "rungwedc.go.tz/storage/app/uploads/public/63c/93f/e2e/63c93fe2ea882297353839.pdf"

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
      - "/storage/app/media/uploaded-files/"
      - "/storage/app/uploads/public/"
    document_notes: |
      Two document paths: /storage/app/media/uploaded-files/ (PDFs in announcement body) and /storage/app/uploads/public/ (hex hash subdirs). Use a.fr-file for inline links.

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
  facebook: "dedrungwe"
  instagram: "rungwedc_official"

notes: |
  A default home page
---

# Home &#124; Rungwe District Council

**Category:** Local Government Authority
**Website:** https://rungwedc.go.tz/
**Tender Page:** https://rungwedc.go.tz/announcement/mwaliko-wa-zabuni-ujenzi-na-uendeshaji-maduka-kiwira
**Keywords Found:** manunuzi, supply, tender, tenders, zabuni

## Contact Information
- Email: ded@rungwedc.go.tz
- Phone: 023
	        
- Phone: 024-05-30
- Phone: 025-08-31
- Phone: 023-05-05 --- 
- Phone: 024
	        

## Scraping Instructions

**Strategy:** Scrape https://rungwedc.go.tz/announcement/mwaliko-wa-zabuni-ujenzi-na-uendeshaji-maduka-kiwira for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> home-page-title">Zabuni Zaidi Jina la zabuni

### Known Tender URLs

- https://rungwedc.go.tz/announcement/mwaliko-wa-zabuni-ujenzi-na-uendeshaji-maduka-kiwira
- https://rungwedc.go.tz/project-details/zabuni-ya-ujenzi-soko-la-ndizi-kiwira
- https://rungwedc.go.tz/tenders

### Document Links Found

- https://rungwedc.go.tz/storage/app/uploads/public/687/8ae/baa/6878aebaa8364430652829.pdf
- https://rungwedc.go.tz/storage/app/uploads/public/66e/d3d/c4a/66ed3dc4a93a9060390970.pdf
- https://rungwedc.go.tz/storage/app/uploads/public/687/8ad/92d/6878ad92d135c878600765.pdf
- https://rungwedc.go.tz/storage/app/uploads/public/685/e68/5fa/685e685faaaf9777644704.pdf
- https://rungwedc.go.tz/storage/app/uploads/public/66a/9f1/a98/66a9f1a98013f412024826.pdf
- https://rungwedc.go.tz/storage/app/uploads/public/63c/93f/e2e/63c93fe2ea882297353839.pdf
- https://rungwedc.go.tz/storage/app/uploads/public/61e/7cf/692/61e7cf692c2c4114888869.pdf

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

Known document paths: /storage/app/uploads/public/685/e68/5fa/685e685faaaf9777644704.pdf, /storage/app/uploads/public/687/8ad/92d/6878ad92d135c878600765.pdf, /storage/app/uploads/public/687/8ae/baa/6878aebaa8364430652829.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
rungwedc/
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
