---
institution:
  name: "National Development Corporation (NDC)"
  slug: "ndc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "ndc.go.tz"

website:
  homepage: "https://ndc.go.tz/"
  tender_url: "https://ndc.go.tz/"

contact:
  email: "info@ndc.go.tz"
  phone: "+255 22 2113618"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Homepage uses Elementor/WordPress. News loop in elementor-loop-container. Check for tender/zabuni in post titles. Documents at /wp-content/uploads/. May need to scrape dedicated tender page if one exists in menu."
  selectors:
    container: ".elementor-loop-grid, .elementor-posts-container, main, article"
    tender_item: ".elementor-post, .e-loop-item, article"
    title: "h3.elementor-image-box-title, .elementor-heading-title, a"
    date: ".elementor-post-date, .date, time"
    document_link: 'a[href*="/wp-content/uploads/"], a[href$=".pdf"], a[href$=".doc"], a[download]'
    pagination: ".elementor-pagination a, .nav-links a"
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
      - "/wp-content/uploads/"
    url_patterns:
      - "ndc.go.tz/wp-content/uploads/*"

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
      WordPress/Elementor site. Homepage shows news carousel. Tender content may be in dedicated section - check menu for zabuni/tenders. Documents at /wp-content/uploads/.

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
  facebook: "ndctanzania"
  twitter: "ndctanzania"
  linkedin: "national-development-corporation-ndc-abb668129"
  instagram: "ndctanzania"

notes: |
  Organization website at ndc.go.tz. Tender keywords detected: bid.
---

# National Development Corporation &#8211; Keeping you Cool, in Every Step

**Category:** Local Government Authority
**Website:** https://ndc.go.tz/
**Tender Page:** https://ndc.go.tz/
**Keywords Found:** bid

## Contact Information
- Email: info@ndc.go.tz
- Phone: +255 22 2113618
- Phone: 023-02-15-
- Phone: 026-01-17-
- Phone: 025-12-18-
- Phone: 0748450711

## Scraping Instructions

**Strategy:** Scrape https://ndc.go.tz/ for government tender notices. Government sites often post zabuni/manunuzi.
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
ndc/
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
- **Signal Strength:** Weak (supply/rfi only)
