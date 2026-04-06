---
institution:
  name: "Keko Pharmaceutical Industries (1997) Ltd"
  slug: "kekopharma"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "kekopharma.co.tz"

website:
  homepage: "https://kekopharma.co.tz/"
  tender_url: "https://kekopharma.co.tz/publications/tender"

contact:
  email: "priva.shayo@kekopharma.co.tz"
  alternate_emails:
    - "info@kekopharma.co.tz"
  phone: "0736996486"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://kekopharma.co.tz/publications/tender (Zabuni page). Tender page in Kituo cha Habari dropdown. Documents at /uploads/documents/ with sw-TIMESTAMP-Filename format."
  selectors:
    container: ".container, .main-container, .rich-text, .ega-section, .list-item"
    tender_item: ".list-item, .d-flex.w-100.list-item, .dropdown-item"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" 
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
      - "kekopharma.co.tz/uploads/documents/*.pdf"
      - "kekopharma.co.tz/uploads/documents/*.doc"
      - "kekopharma.co.tz/uploads/documents/*.docx"
      - "kekopharma.co.tz/uploads/documents/*.xlsx"

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
      Documents at /uploads/documents/ with format sw-{timestamp}-{filename} (e.g. sw-1655360567-New Microsoft Word Document (5).DOCX). Include a[href*="/uploads/"] in link discovery.

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
  facebook: "kekopharma"
  instagram: "keko_pharmaceutical_industries"

notes: |
  Government Website | Tovuti ya Serikali
---

# KPI |   Mwanzo

**Category:** Commercial / Private Sector
**Website:** https://kekopharma.co.tz/
**Tender Page:** https://kekopharma.co.tz/publications/tender
**Keywords Found:** bid, manunuzi, tender, zabuni

## Contact Information
- Email: priva.shayo@kekopharma.co.tz
- Email: info@kekopharma.co.tz
- Phone: 0736996486
- Phone: +255 222866237
- Phone: 0432272987
- Phone: +255 22 2866790

## Scraping Instructions

**Strategy:** Scrape https://kekopharma.co.tz/publications/tender for tender/procurement notices.
**Method:** http_get

Government Website | Tovuti ya Serikali

### Tender Content Preview

> ari Tender Maktaba ya Picha <a class='dropdown-item' href= 'https://kekopharma.co.tz/pres

### Known Tender URLs

- https://kekopharma.co.tz/publications/tender

### Document Links Found

- https://kekopharma.co.tz/uploads/documents/sw-1655360567-New Microsoft Word Document (5).DOCX
- https://kekopharma.co.tz/uploads/documents/sw-1655360017-PRICE FOR ALL ITEMS MANUFACTURED AT KPI-3_FOB (1).xlsx
- https://kekopharma.co.tz/uploads/documents/sw-1653121129-ICT-SERA 2016.pdf
- https://kekopharma.co.tz/uploads/documents/sw-1655360278-New Microsoft Word Document (5).DOCX
- https://kekopharma.co.tz/uploads/documents/sw-1655359692-requisition form.pdf

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
kekopharma/
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
- **Signal Strength:** Strong (manunuzi, tender, zabuni)
