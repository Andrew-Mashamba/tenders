---
institution:
  name: "Catholic University of Health and Allied Sciences (CUHAS)"
  slug: "bugando"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "bugando.ac.tz"

website:
  homepage: "https://bugando.ac.tz/"
  tender_url: "https://bugando.ac.tz/procurement.php"

contact:
  email: "procurement@bugando.ac.tz"
  phone: "007 0 0 1-1"

scraping:
  enabled: false
  method: "http_get"
  strategy: "DISABLED: procurement.php is department info only, no tender listing. No tender table or list. PDFs at /pdf/YYYY/ and /policy/ are admissions/employment docs. Re-enable when tender/EOI page is added."
  selectors:
    container: "main, .content, .page-content"
    tender_item: "article, .tender-item, .announcement, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href*="/pdf/"], a[href*="/policy/"]'
    pagination: null
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

    known_document_paths:
      - "/pdf/"
      - "/policy/"
    url_patterns:
      - "bugando.ac.tz/pdf/*"
      - "bugando.ac.tz/policy/*"

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
      procurement.php shows department info only. PDFs found at /pdf/YYYY/filename.pdf and /policy/. No dedicated tender listing page discovered—current PDFs are admissions, employment, policy docs. Monitor for procurement/EOI announcements.

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
  facebook: "cuhasbugando"
  twitter: "cuhas_bugando"
  instagram: "cuhasbugando"

notes: |
  Organization website at bugando.ac.tz. Tender keywords detected: eoi, procurement.
---

# HOME|CATHOLIC UNIVERSITY OF HEALTH AND ALLIED SCIENCES

**Category:** Educational Institution
**Website:** https://bugando.ac.tz/
**Tender Page:** https://bugando.ac.tz/procurement.php
**Keywords Found:** eoi, procurement

## Contact Information
- Email: vc@bugando.ac.tz
- Phone: 007 0 0 1-1
- Phone: 0 0 0 2 14
- Phone: +255 28 298 3384
- Phone: 09 0 1 0 0 8
- Phone: 0 0 1 8 13

## Scraping Instructions

**Strategy:** Scrape https://bugando.ac.tz/procurement.php for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> it Department Procurement Department <a class="nav-link dropdown-toggle" href="#" data-bs-toggle=

### Known Tender URLs

- https://bugando.ac.tz/procurement.php

### Document Links Found

- https://bugando.ac.tz/pdf/2025/ADVERT_UNDERGRADUATE_2025_2026_SECOND_ROUND.pdf
- https://bugando.ac.tz/pdf/2025/Undergraduate_Advert_2025_2026.pdf
- https://bugando.ac.tz/policy/CUHAS_Training_and_Development_Policy.pdf
- https://bugando.ac.tz/pdf/2025/CUHAS_Volunteering_Opportunity_September_2025.pdf
- https://bugando.ac.tz/pdf/2025/CUHAS_Employment_Opportunities_December_2025.pdf
- https://bugando.ac.tz/pdf/2025/ROUND_2 _SINGLE_ADMISSIONS_2025_2026.pdf
- https://bugando.ac.tz/pdf/2026/Advert_Postgraduate_2026_2027.pdf
- https://bugando.ac.tz/pdf/2025/UNDERGRADUATE_SINGLE_ROUND1_2025_2026.pdf
- https://bugando.ac.tz/pdf/2025/ROUND_3_SINGLE_ADMISSIONS_2025_2026.pdf
- https://bugando.ac.tz/pdf/cuhas_Strategic_plan_20211.pdf

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
bugando/
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
- **Signal Strength:** Strong (eoi, procurement)
