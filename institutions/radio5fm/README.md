---
institution:
  name: "RADIO 5 FM - The Only Choice"
  slug: "radio5fm"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "radio5fm.co.tz"

website:
  homepage: "https://www.radio5fm.co.tz/"
  tender_url: "https://www.radio5fm.co.tz/ppaa-yaokoa-bilioni-586-5-yazima-zabuni-43-hewa/"

contact:
  email: "info@radio5fm.co.tz"
  phone: "058006872745"

scraping:
  enabled: false
  method: "http_get"
  strategy: "radio5fm.co.tz is a news/media site. The tender_url pointed to a single news article about PPAA (procurement authority), not a tender listing. No dedicated tender/procurement page with listing structure exists."
  selectors:
    container: "main, .entry-content, article.post"
    tender_item: "article.post"
    title: "h1.entry-title, .post-title"
    date: ".posted-on, .entry-date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".nav-links a, .pagination a"
  schedule: "daily"

  anti_bot:
    requires_javascript: false
    has_captcha: false
    rate_limit_seconds: 10

  documents:
    download_enabled: false
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
      - "radio5fm.co.tz/*.pdf"

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
      News site. No tender listing page. Documents in articles use wp-content/uploads/. Scraping disabled.

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
  facebook: "radio5tz"
  twitter: "radio5tz"
  instagram: "radio5tz"

notes: |
  Radio 5 FM is a Tanzanian news/media site. No dedicated tender listing page. Scraping disabled.
---

# RADIO 5 FM - &quot;The Only Choice&quot;

**Category:** Commercial / Private Sector
**Website:** https://www.radio5fm.co.tz/
**Tender Page:** https://www.radio5fm.co.tz/ppaa-yaokoa-bilioni-586-5-yazima-zabuni-43-hewa/
**Keywords Found:** rfi, zabuni

## Contact Information
- Email: info@radio5fm.co.tz
- Phone: 058006872745
- Phone: +255 272 970 042
- Phone: 076967-400
- Phone: 026-01-26-
- Phone: 0470888509-100

## Scraping Instructions

**Strategy:** Scrape https://www.radio5fm.co.tz/ppaa-yaokoa-bilioni-586-5-yazima-zabuni-43-hewa/ for tender/procurement notices.
**Method:** http_get

Being one of the fastest growing media in Tanzania, Incorporated under Tan Communication Media, Radio5 was established in Arusha in the year 2007.

### Tender Content Preview

> ntainer"> <img width="321" height="198" src="https://www.radio5fm.co.tz/wp-content/uploads/2026/02/IMG-20250706-WA0026-321x198.jpg" class="img-resp

### Known Tender URLs

- https://www.radio5fm.co.tz/ppaa-yaokoa-bilioni-586-5-yazima-zabuni-43-hewa/

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
radio5fm/
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
- **Signal Strength:** Strong (zabuni)
