---
institution:
  name: "WhizzTanzania"
  slug: "whiztanzania"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "whiztanzania.co.tz"

website:
  homepage: "https://www.whizztanzania.com/"
  tender_url: "https://www.whizztanzania.com/tenders"

contact:
  email: "info@saifeehospital.co.tz"
  alternate_emails:
    - "admin@whizztanzania.com"
    - "holidays.dar@sterlingtravels.com"
    - "arknt_res@turacocollection.com"
    - "zena.sapi@elementdaressalaam.com"
  phone: "025-12-09 14"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Scrape https://www.whizztanzania.com/tenders. WhizzTanzania business directory aggregates
    tenders from multiple sources. Nuxt/Vue SPA - content may require JS. Tender cards with
    title, "Read more" link. Categories: Auctions, Service Tenders, Supplies, Work Tenders.
  selectors:
    container: "[data-v-d519ddf0], main, .container-xxl"
    tender_item: "[data-v-dd54ccf0], .tender-card, a[href*='Read more']"
    title: "h3, h4, .tender-title"
    date: ".date, .closing-date, .published"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, [data-v-d519ddf0] a"
  schedule: "daily"

  anti_bot:
    requires_javascript: true
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
      - "/storage/"
      - "api.whizztanzania.com/upload/"

    url_patterns:
      - "whizztanzania.com/*.pdf"
      - "whizztanzania.com/storage/*"
      - "api.whizztanzania.com/upload/*"

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
      Tenders aggregated from external sources. Follow "Read more" to detail pages for documents.
      API at api.whizztanzania.com. Storage paths from detail page links.

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
  facebook: "whizztanzaniaonline"
  twitter: "whizztanzania"
  linkedin: "whizztanzania"
  instagram: "whizztanzania"

notes: |
  WhizzTanzania stands as Tanzania
---

# Business directory, business directory in tanzania, business e-commerce, business listings, business website, business marketplace, companies business listings, companies database tanzania, companies 

**Category:** Commercial / Private Sector
**Website:** https://www.whizztanzania.com/
**Tender Page:** https://www.youtube.com/channel/UCXUYhLRfPuFuPIpgt1JZGFA
**Keywords Found:** bid, eoi, expression of interest, rfi, rfp, rfq, supply, tender, tenders

## Contact Information
- Email: info@saifeehospital.co.tz
- Email: admin@whizztanzania.com
- Email: holidays.dar@sterlingtravels.com
- Email: arknt_res@turacocollection.com
- Email: zena.sapi@elementdaressalaam.com
- Phone: 025-12-09 14
- Phone: 0783 639 335
- Phone: 0 0 1 0-16
- Phone: 0 0 0 16-16
- Phone: 026-03-10 08

## Scraping Instructions

**Strategy:** Scrape https://www.youtube.com/channel/UCXUYhLRfPuFuPIpgt1JZGFA for tender/procurement notices.
**Method:** http_get

WhizzTanzania stands as Tanzania

### Tender Content Preview

> ref="/events" class="" data-v-d519ddf0>Events Tenders SOS <a hre

### Known Tender URLs

- https://www.youtube.com/channel/UCXUYhLRfPuFuPIpgt1JZGFA
- https://www.whizztanzania.com/tenders

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
whiztanzania/
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
- **Signal Strength:** Strong (eoi, expression of interest, rfp, rfq, tender, tenders)
