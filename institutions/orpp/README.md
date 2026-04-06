---
institution:
  name: "Ofisi ya Msajili wa Vyama vya Siasa (ORPP)"
  slug: "orpp"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "orpp.go.tz"

website:
  homepage: "https://orpp.go.tz/"
  tender_url: "https://orpp.go.tz/"

contact:
  email: "info@orpp.go.tz"
  phone: "026
         "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage. ORPP is Office of Registrar of Political Parties - posts press releases and public notices. PDF documents in 'Vyombo vya habari' and 'How do I' sections. Look for links under Zabuni menu and document sections."
  selectors:
    container: "main, .content, .entry-content, section"
    tender_item: "article, .card, .news-item, li"
    title: "h2, h3, h4, h5, h6, .tender-title, a"
    date: ".date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ""
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
      - "/uploads/pressreleases/"
    url_patterns:
      - "orpp.go.tz/uploads/pressreleases/*.pdf"

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
      Documents stored at /uploads/pressreleases/ (e.g. sw1748424514-TAARIFA KWA UMMA.pdf). Mostly press releases, not traditional procurement tenders.

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
  facebook: "orpp.msajili"
  twitter: "orppdigital"

notes: |
  Organization website at orpp.go.tz. Tender keywords detected: bid, zabuni.
---

# orpp |     JAMHURI YA MUUNGANO WA TANZANIA - Mwanzo

**Category:** Government Agency
**Website:** https://orpp.go.tz/
**Tender Page:** https://orpp.go.tz/
**Keywords Found:** bid, zabuni

## Contact Information
- Email: info@orpp.go.tz
- Phone: 026
         
- Phone: 05458892-
- Phone: 05458872-
- Phone: 05458813-
- Phone: +255 26 23322500

## Scraping Instructions

**Strategy:** Scrape https://orpp.go.tz/ for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get



### Tender Content Preview

> Zabuni <div class="position-absolute search-toggle top-right text-white text-hover-secondary hover-bg-pr

### Document Links Found

- https://orpp.go.tz/uploads/pressreleases/sw1748424514-TAARIFA KWA UMMA.pdf
- https://orpp.go.tz/uploads/pressreleases/sw1741898879-MAAZIMIO MKUTANO WA BARAZA TAREHE 13 MACHI 2025.pdf
- https://orpp.go.tz/uploads/pressreleases/sw1748425297-TAARIFA KWA UMMA_compressed.pdf
- https://orpp.go.tz/uploads/pressreleases/sw1650017512-TAARIFA KWA UMMA KUTOKA KWA KIKOSI KAZI_220414_172_220414_172936.pdf

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
orpp/
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

- **Last Checked:** 15 March 2026
- **Active Tenders:** 0
- **Signal Strength:** Strong (zabuni) — Zabuni links to nest.go.tz (external)
