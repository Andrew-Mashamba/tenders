---
institution:
  name: "PASADA - Pastoral Activities and Services for people with AIDS Dar es Salaam Archdiocese"
  slug: "pasada"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "pasada.or.tz"

website:
  homepage: "https://pasada.or.tz/"
  tender_url: "https://pasada.or.tz/category/tenders"

contact:
  email: "procurement@pasada.or.tz"
  alternate_emails:
    - "info@pasada.or.tz"
    - "recruitment@pasada.or.tz"
  phone: "00092012386881"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://pasada.or.tz/category/tenders. PASADA uses blog-style listing. Each tender is .blog-item with title in h2 a, excerpt in .text p, Read More links to detail. Follow detail pages for full ToR and document links. Pagination: ?page=2"
  selectors:
    container: ".blog-area, .col-md-8"
    tender_item: ".blog-item"
    title: ".blog-item .text h2 a, .blog-item h2 a"
    date: ".blog-item .text p"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: "nav ul.pagination a.page-link, .pagination .page-link"
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
      - "/uploads/"
    url_patterns:
      - "pasada.or.tz/blog/*"
      - "pasada.or.tz/uploads/*/*.pdf"

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
      Tenders listed as blog posts. Detail pages (blog/*) contain full ToR; documents may be attached or linked. Follow Read More to get full content per tender.

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
  facebook: "profile.php"
  twitter: "PasadaTz"
  instagram: "pasadatanzania"

notes: |
  PASADA - Pastoral Activities and Services for people with AIDS Dar es Salaam Archdiocese
---

# PASADA - Pastoral Activities and Services for people with AIDS Dar es Salaam Archdiocese

**Category:** NGO / Non-Profit Organization
**Website:** https://pasada.or.tz/
**Tender Page:** https://pasada.or.tz/blog/procurement-officer
**Keywords Found:** bid, procurement, request for proposal, rfp, tender, tenders

## Contact Information
- Email: procurement@pasada.or.tz
- Email: info@pasada.or.tz
- Email: recruitment@pasada.or.tz
- Phone: 00092012386881
- Phone: +255 22 286-6618
- Phone: 023
          
- Phone: 024
          

## Scraping Instructions

**Strategy:** Scrape https://pasada.or.tz/blog/procurement-officer for tender/procurement notices.
**Method:** http_get

PASADA - Pastoral Activities and Services for people with AIDS Dar es Salaam Archdiocese

### Known Tender URLs

- https://pasada.or.tz/blog/procurement-officer
- https://pasada.or.tz/category/tenders
- https://pasada.or.tz/blog/job-title-procurement-officer
- https://pasada.or.tz/blog/Tender2
- https://pasada.or.tz/blog/tender-for-delivery-of-car-hire-service
- https://pasada.or.tz/blog/rfp-title-facilitation-of-sharing-health-testing-counselling-best-practices-and-publications
- https://pasada.or.tz/blog/Tender1

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
pasada/
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
- **Signal Strength:** Strong (procurement, rfp, tender, tenders)
- **Note:** All listed tenders had closing dates before 2026-03-15 (expired)
