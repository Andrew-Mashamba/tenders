---
institution:
  name: "Bodi ya Mfuko wa Barabara (Tanzania Roads Fund Board)"
  slug: "roadsfund"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "roadsfund.go.tz"

website:
  homepage: "https://roadsfund.go.tz/"
  tender_url: "https://roadsfund.go.tz/pages/zabuni"

contact:
  email: "info@roadsfund.go.tz"
  phone: "0641791-1000"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape Zabuni (tenders) at /pages/zabuni and GPN (General Procurement Notices) at /publications/13. Nav: MANUNUZI > GPN, Zabuni. Main content in .main-content, .content-border. Sidebar has .sidebar-info .info-items. Documents in /uploads/news/, /uploads/gallery/, publications. Use -k for SSL if needed."
  selectors:
    container: "section.main-content, .content-border, .content-layout"
    tender_item: ".sidebar-info .info-items .border-bottom, .sub-main-content .row, .media"
    title: "h4.sidebar-header, .media-body .news-content, .title-decoration"
    date: ".date span, .fa-calendar-alt"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/uploads/"]'
    pagination: ".pagination a, .btn-custom, a[href*='news']" 
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
      - "/uploads/news/"
      - "/uploads/gallery/"
      - "/publications/"
    url_patterns:
      - "roadsfund.go.tz/uploads/*.pdf"
      - "roadsfund.go.tz/publications/*"
      - "roadsfund.go.tz/news/*"

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
      Government agency. MANUNUZI nav has GPN (publications/13) and Zabuni (pages/zabuni). Documents in /uploads/news/, /uploads/gallery/. News items in .sidebar-info with dates. SSL may require -k flag for curl.

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
  facebook: "RFBTZ"
  twitter: "rfb_tz"
  instagram: "rfb_tz"

notes: |
  some page description here
---

# Mwanzo
| Bodi ya Mfuko wa Barabara

**Category:** Government Agency
**Website:** https://roadsfund.go.tz/
**Tender Page:** https://roadsfund.go.tz/pages/zabuni
**Keywords Found:** bid, manunuzi, rfi, zabuni

## Contact Information
- Email: info@roadsfund.go.tz
- Phone: 0641791-1000
- Phone: +255 26 2963279
- Phone: +255 26 2963277

## Scraping Instructions

**Strategy:** Scrape https://roadsfund.go.tz/pages/zabuni for government tender notices (Zabuni). Page displays "Hakuna zabuni kwa sasa" when no tenders. Government sites often post zabuni/manunuzi.
**Method:** http_get

some page description here

### Tender Content Preview

> o.tz/publications/13'>GPN Zabuni KITUO CHA HABARI <ul class='dropdown-menu dr

### Known Tender URLs

- https://roadsfund.go.tz/news/mhandisi-kalimbaga-akabidhiwa-rasmi-uongozi-wa-armfa

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
roadsfund/
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
- **Signal Strength:** Strong (manunuzi, zabuni)
