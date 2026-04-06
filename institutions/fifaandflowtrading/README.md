---
institution:
  name: "Fifa & Flow Trading Company"
  slug: "fifaandflowtrading"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "fifaandflowtrading.co.tz"

website:
  homepage: "https://fifaandflowtrading.co.tz/"
  tender_url: "https://fifaandflowtrading.co.tz/"

contact:
  email: "admin@logiscotheme.co"
  alternate_emails:
    - "fifa@fifaandflowtrading.co.tz"
  phone: "+255753306494"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Homepage has no tender listing. Site is a logistics company with company profile downloads only. No procurement/tender notices found."
  selectors:
    container: "main, .logisco-body-wrapper, .content"
    tender_item: "article, .tender-item, .card"
    title: "h2, h3, h4, .tender-title"
    date: ".date, .closing-date, time"
    document_link: 'a[href*="/details/"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: null
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
      - "/details/"
    url_patterns:
      - "fifaandflowtrading.co.tz/details/*.pdf"
      - "fifaandflowtrading.co.tz/details/*.doc*"

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
      Documents stored at /details/ (e.g. /details/FIFA COMPANY PROFILE.pdf). No tender-specific documents; site has company profile only. Scraping disabled: no tender content.

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

notes: |
  Organization website at fifaandflowtrading.co.tz. Tender keywords detected: procurement, rfi, supply.
---

# Fifa & &#8211; Flow &amp; Trading Company

**Category:** Commercial / Private Sector
**Website:** https://fifaandflowtrading.co.tz/
**Tender Page:** https://fifaandflowtrading.co.tz/
**Keywords Found:** procurement, rfi, supply

## Contact Information
- Email: admin@logiscotheme.co
- Email: fifa@fifaandflowtrading.co.tz
- Phone: +255753306494
- Phone: 0092247-800
- Phone: +255 754 296 755 
- Phone: +255 22 212 2998 
- Phone: +255 754 296 755

## Scraping Instructions

**Strategy:** Scrape https://fifaandflowtrading.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> form: none ;"> Our worldwide network for procurement, distribution and aftermarket logistics ensures your components and vehicles.

### Document Links Found

- https://fifaandflowtrading.co.tz/details/FIFA COMPANY PROFILE.pdf

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
fifaandflowtrading/
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
- **Signal Strength:** Strong (procurement)
