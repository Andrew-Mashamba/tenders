---
institution:
  name: "MS Training Centre for Development Cooperation (MS-TCDC)"
  slug: "mstcdc"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "mstcdc.or.tz"

website:
  homepage: "https://mstcdc.or.tz/"
  tender_url: "https://mstcdc.or.tz/tenders"

contact:
  email: "mstcdc@mstcdc.or.tz"
  phone: "+255 754 651 715"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Drupal 10 site. Fetch https://mstcdc.or.tz/tenders. Tenders listed under 'OPEN TENDERS' in .region.region-content. Each tender: h2 (title) + .halfbox__link a (LEARN MORE → detail page). Follow detail page links (e.g. /tender-maintenance-and-repair-ict-infrastructure) for full description and document links. Documents likely in /sites/default/files/."
  selectors:
    container: ".region.region-content"
    tender_item: ".region.region-content h2"
    title: "h2"
    date: ".field--name-field-date, time"
    document_link: ".halfbox__link a, a[href$='.pdf'], a[href*='sites/default/files']"
    pagination: ".pager a, .pagination a" 
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
      - "/sites/default/files/"
    url_patterns:
      - "mstcdc.or.tz/sites/default/files/*.pdf"
      - "mstcdc.or.tz/tender-*"

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
      Drupal 10. Tender listing shows h2 titles + LEARN MORE links to detail pages. Documents on detail pages. Follow /tender-* URLs for full tender content and attachments.

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
  facebook: "share.php"
  instagram: "mstcdc"

notes: |
  MS-TCDC is a renowned Pan-African training center, situated in Tanzania, unique in our dedication to high quality capacity development for social transformation.
---

# MS-TCDC - MS Training Centre for Development Cooperation | MS-TCDC

**Category:** NGO / Non-Profit Organization
**Website:** https://mstcdc.or.tz/
**Tender Page:** https://mstcdc.or.tz/tenders
**Keywords Found:** tender, tenders

## Contact Information
- Email: mstcdc@mstcdc.or.tz
- Phone: +255 754 651 715
- Phone: 0870554538

## Scraping Instructions

**Strategy:** Scrape https://mstcdc.or.tz/tenders for tender/procurement notices.
**Method:** http_get

MS-TCDC is a renowned Pan-African training center, situated in Tanzania, unique in our dedication to high quality capacity development for social transformation.

### Tender Content Preview

> class="field__item"> Jobs Open Tenders <div id="block-menublockaboutuscontact" class="block block-block-content block-bloc

### Known Tender URLs

- https://mstcdc.or.tz/tenders

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
mstcdc/
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
- **Signal Strength:** Strong (tender, tenders)
