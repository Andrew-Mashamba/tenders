---
institution:
  name: "Home | University of Dar es Salaam"
  slug: "udsm"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "udsm.ac.tz"

website:
  homepage: "https://udsm.ac.tz/"
  tender_url: "https://udsm.ac.tz/announcement/invitation-tender"

contact:
  email: "vc@udsm.ac.tz"
  phone: "024-05-09"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://udsm.ac.tz/announcement/invitation-tender for tender/procurement notices."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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
      - "udsm.ac.tz/files/UDSM_Audited_Financial_statement_24.pdf"
      - "udsm.ac.tz/files/facts_and_figures_24.pdf"
      - "udsm.ac.tz/files/2025-09/call%20for%20papers.pdf"
      - "udsm.ac.tz/files/2025-11/Call_for_Abstracts_Papers.pdf"
      - "udsm.ac.tz/files/2026-01/ALMANAC_2025-2026.pdf"

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
      Known document paths: /files/UDSM_Audited_Financial_statement_24.pdf, /files/facts_and_figures_24.pdf, /files/2025-09/call%20for%20papers.pdf

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
  facebook: "University-of-Dar-es-Salaam-281353046083466"
  instagram: "udsmofficial"

notes: |
  Organization website at udsm.ac.tz. Tender keywords detected: bid, expression of interest, procurement, rfi, supply, tender.
---

# Home | University of Dar es Salaam

**Category:** Educational Institution
**Website:** https://udsm.ac.tz/
**Tender Page:** https://udsm.ac.tz/announcement/invitation-tender
**Keywords Found:** bid, expression of interest, procurement, rfi, supply, tender

## Contact Information
- Email: vc@udsm.ac.tz
- Phone: 024-05-09
- Phone: 025-03-03
- Phone: 025-03-10
- Phone: 08565722655
- Phone: 025-07-14

## Scraping Instructions

**Strategy:** Scrape https://udsm.ac.tz/announcement/invitation-tender for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> class="views-field views-field-title"> Invitation for Tender 2025-02-19 </spa

### Known Tender URLs

- https://udsm.ac.tz/announcement/invitation-tender
- https://udsm.ac.tz/announcement/invitation-bids-supply-installation-and-commissioning-ict-infrastructure-university
- https://udsm.ac.tz/procurement

### Document Links Found

- https://udsm.ac.tz/sites/default/files/2026-01/ALMANAC_2025-2026.pdf
- https://udsm.ac.tz/sites/default/files/2025-11/Call_for_Abstracts_Papers.pdf
- https://udsm.ac.tz/sites/default/files/2025-09/call%20for%20papers.pdf
- https://udsm.ac.tz/sites/default/files/facts_and_figures_24.pdf
- https://udsm.ac.tz/sites/default/files/UDSM_Audited_Financial_statement_24.pdf

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

Known document paths: /files/UDSM_Audited_Financial_statement_24.pdf, /files/facts_and_figures_24.pdf, /files/2025-09/call%20for%20papers.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
udsm/
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
- **Signal Strength:** Strong (expression of interest, procurement, tender)
