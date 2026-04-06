---
institution:
  name: "Fursa za Ajira Tanzania | Jobs & Opportunities"
  slug: "fursa"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "fursa.co.tz"

website:
  homepage: "https://fursa.co.tz/"
  tender_url: "https://fursa.co.tz/jobs/?search_category=184"

contact:
  phone: "025-11-07"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://fursa.co.tz/jobs/?search_category=184 for Tenders category (WP Job Manager). Jobs load via AJAX - requires JavaScript. Each li.job_listing links to /job/{slug}/. Follow job detail pages for document links."
  selectors:
    container: ".job_listings, ul.job_listings, #primary .entry-content"
    tender_item: "li.job_listing"
    title: ".job_listing-title, .position h3, h2 a"
    date: ".job_listing-timestamp, .posted-date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download], a[href*="/wp-content/uploads/"]'
    pagination: "a.load_more_jobs, .job-manager-pagination a, .pagination a" 
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
      - "/wp-content/uploads/"
    url_patterns:
      - "fursa.co.tz/wp-content/uploads/*.pdf"
      - "fursa.co.tz/job/*"

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
      WP Job Manager site. Job listings load via AJAX into ul.job_listings. Documents typically on job detail pages (/job/{slug}/). WordPress uploads at /wp-content/uploads/.

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
  Welcome to Fursa | Nafasi za Kazi | Job Vacancies in Tanzania. Visit this Site Regularly for Job Opportunities listings.
---

# Home - Fursa za Ajira Tanzania | Jobs &amp; Opportunities

**Category:** Commercial / Private Sector
**Website:** https://fursa.co.tz/
**Tender Page:** https://fursa.co.tz/jobs/?search_category=184
**Keywords Found:** bid, eoi, expression of interest, invitation to bid, procurement, request for proposal, rfi, rfp, rfq, supply, tender, tenders

## Contact Information
- Phone: 025-11-07
- Phone: +255 26 2322357
- Phone: 08-201-30
- Phone: 025-07-30
- Phone: 026-01-23-

## Scraping Instructions

**Strategy:** Scrape https://fursa.co.tz/jobs/?search_category=184 for tender/procurement notices.
**Method:** http_get

Welcome to Fursa | Nafasi za Kazi | Job Vacancies in Tanzania. Visit this Site Regularly for Job Opportunities listings.

### Tender Content Preview

> y=184"> Tenders 7 Open Jobs

### Known Tender URLs

- https://fursa.co.tz/jobs/?search_category=184
- https://fursa.co.tz/job/nutrition-international-invitation-to-bid-for-youth-service-centers-construction-and-renovation-march-2026/
- https://fursa.co.tz/jobs/?search_category=184

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
fursa/
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
- **Signal Strength:** Strong (eoi, expression of interest, procurement, rfp, rfq, tender, tenders)
