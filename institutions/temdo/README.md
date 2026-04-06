---
institution:
  name: "Taasisi ya Uhandisi na Usanifu Mitambo Tanzania (TEMDO)"
  slug: "temdo"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "temdo.or.tz"

website:
  homepage: "https://temdo.or.tz/"
  tender_url: "https://temdo.or.tz/tenders"

contact:
  email: "dg@temdo.or.tz"
  phone: "+255 738 188 652"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /tenders page. Each tender is p.download with a link; title and closing date (Tarehe ya Mwisho) in link text. Documents in /uploads/tenders/."
  selectors:
    container: ".sub-main-content, .content-border"
    tender_item: "p.download"
    title: "p.download a"
    date: "p.download a"
    document_link: 'p.download a[href*="/uploads/tenders/"], a[download]'
    pagination: ".nav-pagination .pagination a, .pagination li a"
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
      - "/uploads/tenders/"

    url_patterns:
      - "temdo.or.tz/uploads/tenders/*"

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
      Documents in /uploads/tenders/ (e.g. sw1564651416-advert TEMDO WORKSHOP PARTITION.pdf). Closing date in link text as "Tarehe ya Mwisho YYYY-MM-DD". Each tender is single PDF link.

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
  instagram: "temdotanzania"

notes: |
  some page description here
---

# Mwanzo
    |Taasisi ya Uhandisi na Usanifu Mitambo TANZANIA.

**Category:** NGO / Non-Profit Organization
**Website:** https://temdo.or.tz/
**Tender Page:** https://temdo.or.tz/tenders
**Keywords Found:** bid, rfi, tender, tenders, zabuni

## Contact Information
- Email: dg@temdo.or.tz
- Phone: +255 738 188 652
- Phone: 09889264-
- Phone: 0282501-10

## Scraping Instructions

**Strategy:** Scrape https://temdo.or.tz/tenders for tender/procurement notices.
**Method:** http_get

some page description here

### Tender Content Preview

> Barua Pepe Zabuni Ajira <!-- it shou

### Known Tender URLs

- https://temdo.or.tz/tenders

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
temdo/
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
- **Signal Strength:** Strong (tender, tenders, zabuni)
