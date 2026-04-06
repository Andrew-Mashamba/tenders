---
institution:
  name: "Dar es Salaam Institute of Technology"
  slug: "dit"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "dit.ac.tz"

website:
  homepage: "https://dit.ac.tz/"
  tender_url: "https://dit.ac.tz/"

contact:
  email: "rector@dit.ac.tz"
  phone: "025
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape DIT homepage and Useful Docs (/ad18942s08oub/publication). No dedicated tender listing page; documents and procurement notices may appear in news/events. Check Finance & Accounts department pages for procurement. Extract all document links from /documents/ path."
  selectors:
    container: ".dit-body-wrapper, .dit-body-outer-wrapper, main"
    tender_item: ".gdlr-core-blog-item, .gdlr-core-pbf-element, li.menu-item"
    title: "h2, h3, h4, h5, .gdlr-core-blog-item-title, a"
    date: ".date, .gdlr-core-blog-item-date, time, span"
    document_link: 'a[href*="/documents/"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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
      - "/documents/"
      - "/storage/images/"

    url_patterns:
      - "dit.ac.tz/documents/*.pdf"
      - "dit.ac.tz/documents/dit_*.pdf"

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
      Documents stored at /documents/ (e.g. dit_student_welfare.pdf, dit_accommodation.pdf, dit_academic_calender_2025_2026.pdf, dit_almanac_2025_2026.pdf, dit_ditso_constitution.pdf, dit_prospectus_2025_2026.pdf). Useful Docs page at /ad18942s08oub/publication. No dedicated tender listing; procurement may appear in news or department pages.

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
  facebook: "Official.DIT"
  instagram: "dit_tanzania"

notes: |
  Organization website at dit.ac.tz. Tender keywords detected: procurement, rfi, supply.
---

# Dar es Salaam Institute of Technology

**Category:** Educational Institution
**Website:** https://dit.ac.tz/
**Tender Page:** https://dit.ac.tz/
**Keywords Found:** procurement, rfi, supply

## Contact Information
- Email: rector@dit.ac.tz
- Phone: 025
          
- Phone: 044400-600
- Phone: 02-2026
      
- Phone: 0 0 1 22 16
- Phone: 0526219-600

## Scraping Instructions

**Strategy:** Scrape https://dit.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> The DIT Rector, Prof.Preksedis M. Ndomba (at the middle), speaking to the Director of Procurement and Supply from the Ministry of Education, Science and Technology, Metrida Kaijage (right) during a site visit to an ongoing EASTRIP project at Mwanza Campus. At the left is Dr. Fredrick

### Document Links Found

- https://dit.ac.tz/documents/dit_almanac_2025_2026.pdf
- https://dit.ac.tz/documents/dit_accommodation.pdf
- https://dit.ac.tz/documents/dit_prospectus_2025_2026.pdf
- https://dit.ac.tz/documents/dit_ditso_constitution.pdf
- https://dit.ac.tz/documents/dit_academic_calender_2025_2026.pdf
- https://dit.ac.tz/documents/dit_student_welfare.pdf

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

Known document paths: /documents/dit_student_welfare.pdf, /documents/dit_accommodation.pdf, /documents/dit_academic_calender_2025_2026.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
dit/
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
