---
institution:
  name: "Advanced Engineering Solutions (AESL)"
  slug: "aesl"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "aesl.co.tz"

website:
  homepage: "https://aesl.co.tz/"
  tender_url: "https://aesl.co.tz/"

contact:
  email: "info@aesl.co.tz"
  phone: "05 011        "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://aesl.co.tz/ (WordPress/Elementor). Civil engineering consultancy. Tender-related content in blog posts and project pages. Check homepage, /blog/, and project posts. Known document: AES-PROFILE-Final-2023 in wp-content/uploads/."
  selectors:
    container: "main, .elementor-section, .entry-content, .rs-addon-content"
    tender_item: "article, .blog-item, .elementor-widget"
    title: "h2, h3, h4, .blog-title, .elementor-heading-title"
    date: ".date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/wp-content/uploads/"]'
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

    url_patterns:
      - "aesl.co.tz/wp-content/uploads/*"
      - "aesl.co.tz/*.pdf"

    known_document_paths:
      - "/wp-content/uploads/"

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
      WordPress. Documents in /wp-content/uploads/{year}/{month}/. Known: AES-PROFILE-Final-2023. Tender/project docs may appear in blog posts. Check project and news sections for RFP/tender announcements.

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
  facebook: "aesltz"

notes: |
  HOME AESL as a Civil Engineering Company as well as a Consultancy company ensures to stand on their moto of Providing future solutions now. this ensures high..
---

# HOME - Advanced Engineering Solutions (AESL)

**Category:** Commercial / Private Sector
**Website:** https://aesl.co.tz/
**Tender Page:** https://aesl.co.tz/2023/09/23/contract-signing-ceremony-for-consultancy-services-for-feasibility-study-esmp-rap-detailed-engineering-design-and-preparation-of-tender-documents-for-improvement-of-the-kitonga-escarpment-road/
**Keywords Found:** bid, bidding, rfi, tender

## Contact Information
- Email: image2021@1-300x177.jpg
- Email: info@aesl.co.tz
- Email: image2021@1.jpg
- Phone: 05 011        
- Phone: 020000			
- Phone: 02866735161465
- Phone: 02867047163974
- Phone: 022-03-23

## Scraping Instructions

**Strategy:** Scrape https://aesl.co.tz/2023/09/23/contract-signing-ceremony-for-consultancy-services-for-feasibility-study-esmp-rap-detailed-engineering-design-and-preparation-of-tender-documents-for-improvement-of-the-kitonga-escarpment-road/ for tender/procurement notices.
**Method:** http_get

HOME AESL as a Civil Engineering Company as well as a Consultancy company ensures to stand on their moto of Providing future solutions now. this ensures high..

### Tender Content Preview

> -consultancy-services-for-feasibility-study-esmp-rap-detailed-engineering-design-and-preparation-of-tender-documents-for-improvement-of-the-kitonga-escarpment-road/"> <img loading="lazy" width="310" height="270" src="https://aesl.co.tz/wp-content/uploads/

### Known Tender URLs

- https://aesl.co.tz/2023/09/23/contract-signing-ceremony-for-consultancy-services-for-feasibility-study-esmp-rap-detailed-engineering-design-and-preparation-of-tender-documents-for-improvement-of-the-kitonga-escarpment-road/

### Document Links Found

- https://aesl.co.tz/wp-content/uploads/2023/04/AES-PROFILE-Final-2023-1.pdf-1.pdf

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

Known document paths: /wp-content/uploads/2023/04/AES-PROFILE-Final-2023-1.pdf-1.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
aesl/
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
- **Signal Strength:** Strong (bidding, tender)
