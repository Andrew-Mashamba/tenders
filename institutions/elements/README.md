---
institution:
  name: "Elements Limited"
  slug: "elements"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "elements.co.tz"

website:
  homepage: "https://elements.co.tz/"
  tender_url: "https://elements.co.tz/"

contact:
  email: "info@elements.co.tz"
  alternate_emails:
    - "ajax-loader@2x.gif"
  phone: "021-06-14"

scraping:
  enabled: true
  method: "http_get"
  strategy: "WordPress/Porto theme. Agricultural commodities company. No dedicated tender page. Homepage has portfolio grid (Pulses, Grains, Oilseeds). Scrape main content and portfolio detail pages for any procurement/RFI announcements."
  selectors:
    container: ".page-portfolios, .portfolios-grid, main, .entry-content, .wpb_wrapper"
    tender_item: "article.portfolio, .portfolio-item"
    title: ".entry-title, .portfolio-link, h2, h3, h4"
    date: ".updated, .date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a, .load-more"
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
      - "elements.co.tz/*.pdf"

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
      No tender-specific document paths found. Site is agricultural commodities (grains, pulses, oilseeds). Portfolio items at /portfolio/{slug}/. Check for RFI/supply documents on detail pages if any procurement content appears.

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
  facebook: "elementslimited"
  linkedin: "71571437"

notes: |
  Organization website at elements.co.tz. Tender keywords detected: rfi, supply.
---

# Elements Limited &#8211; Our Service is valued by People because what we do matters

**Category:** Commercial / Private Sector
**Website:** https://elements.co.tz/
**Tender Page:** https://elements.co.tz/
**Keywords Found:** rfi, supply

## Contact Information
- Email: info@elements.co.tz
- Email: ajax-loader@2x.gif
- Phone: 021-06-14
- Phone: 021-06-11
- Phone: +255 222 451 832
- Phone: 09545862313825
- Phone: 02127075195312

## Scraping Instructions

**Strategy:** Scrape https://elements.co.tz/ for tender/procurement notices.
**Method:** http_get



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
elements/
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

- **Last Checked:** 10 June 2026
- **Active Tenders:** 0
- **Signal Strength:** Weak (supply/rfi only; no procurement content on homepage)
