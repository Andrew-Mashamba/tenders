---
institution:
  name: "IBES Tanzania"
  slug: "ibes"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "ibes.co.tz"

website:
  homepage: "https://ibes.co.tz/"
  tender_url: "https://ibes.co.tz/"

contact:
  email: "info@ibes.co.tz"
  phone: "+255767690431"

scraping:
  enabled: false
  method: "http_get"
  strategy: "IBES is a daycare/school (Different Teaching Better Results). No tender page. Crawler found arch_err:/tenders (404). Homepage has school info, events. Disable until tender section exists."
  selectors:
    container: "main, .content, .elementor-element, .kadence-theme"
    tender_item: "article, .elementor-post"
    title: "h1, h2, h3, h4, .elementor-heading-title"
    date: ".date, time, .posted-on"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/wp-content/uploads/"]'
    pagination: ".pagination a, a.next"
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
      - "ibes.co.tz/*.pdf"

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
      Daycare/school site. /tenders returns 404. wp-content/uploads/ for any documents. No tender content. Re-enable if tender section added.

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
  facebook: "ibes.tanzania"
  instagram: "ibes.tz"

notes: |
  Organization website at ibes.co.tz. Tender keywords detected: tender, tenders.
---

# Page not found - IBES Tanzania

**Category:** Commercial / Private Sector
**Website:** http://ibes.co.tz/
**Tender Page:** http://ibes.co.tz/
**Keywords Found:** tender, tenders

## Contact Information
- Email: info@ibes.co.tz
- Phone: +255767690431
- Phone: 06 2-2 2-0
- Phone: 078 0-11-4
- Phone: 0 0 512 512
- Phone: +255 767 690 431

## Scraping Instructions

**Strategy:** Scrape http://ibes.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> tq.push([ "view", {"v":"ext","blog":"222426387","post":"0","tz":"0","srv":"ibes.co.tz","arch_err":"/tenders","j":"1:15.6"} ]); _stq.push([ "clickTrackerInit", "222426387", "0" ]); //# sourceURL=jetpack-stats-js-before <script src="https://stats.wp.com/e-202611.js" id="jetpack-stats-js" def

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
ibes/
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
