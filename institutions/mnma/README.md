---
institution:
  name: "Mwalimu Nyerere Memorial Academy (MNMA)"
  slug: "mnma"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "mnma.ac.tz"

website:
  homepage: "https://www.mnma.ac.tz/"
  tender_url: "https://www.mnma.ac.tz/"

contact:
  email: "rector@mnma.ac.tz"
  phone: "026-02-26"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.mnma.ac.tz/ homepage. ANNOUNCEMENT section contains EOI, PPP, and procurement notices as table rows with PDF links. Each row has title (link) and Posted date. Also check DOWNLOADS section for documents."
  selectors:
    container: "main, .content, table, .announcement-section, section"
    tender_item: "table tbody tr, table td a[href$='.pdf']"
    title: "a[href$='.pdf'], a[href*='media_doc'], a[href*='/doc/']"
    date: ".date, [Posted:], td"
    document_link: 'a[href$=".pdf"], a[href*="media_doc"], a[href*="/doc/"]'
    pagination: "a[href*='Read More'], .pagination a, a.next"
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
      - "/media_doc/"
      - "/doc/"

    url_patterns:
      - "mnma.ac.tz/media_doc/*.pdf"
      - "mnma.ac.tz/doc/*.pdf"

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
      ANNOUNCEMENT section lists notices with format [TITLE [Posted: DD, Mon YYYY]]. Documents in /media_doc/ (ANNOUNCEMENT-YYYY-MM-DD_*.pdf) and /doc/ (institutional docs). DOWNLOADS section has Student By Law, Almanac, etc.

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
  facebook: "MNMA_official-109164944860312"
  twitter: "MNMA_official"
  instagram: "mnma_official21"

notes: |
  Organization website at mnma.ac.tz. Tender keywords detected: bid, expression of interest.
---

# MNMA | MAIN CAMPUS

**Category:** Educational Institution
**Website:** https://www.mnma.ac.tz/
**Tender Page:** https://www.mnma.ac.tz/
**Keywords Found:** bid, expression of interest

## Contact Information
- Email: rector@mnma.ac.tz
- Phone: 026-02-26
- Phone: 024-12-03
- Phone: 023-07-14
- Phone: 023-06-20
- Phone: 025-08-12

## Scraping Instructions

**Strategy:** Scrape https://www.mnma.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Document Links Found

- https://www.mnma.ac.tz/media_doc/ANNOUNCEMENT-2025-12-08_024910.pdf
- https://www.mnma.ac.tz/media_doc/ANNOUNCEMENT-2025-11-21_015318.pdf
- https://www.mnma.ac.tz/media_doc/ANNOUNCEMENT-2025-10-07_133704.pdf
- https://www.mnma.ac.tz/media_doc/ANNOUNCEMENT-2025-11-09_104454.pdf
- https://www.mnma.ac.tz/doc/STUDENT-BY-LAWS-1.pdf
- https://www.mnma.ac.tz/media_doc/ANNOUNCEMENT-2025-12-14_084804.pdf
- https://www.mnma.ac.tz/doc/MNMA-ALMANAC_FOR_THE_ACADEMIC_YEAR_2024-2025_REVISED.pdf
- https://www.mnma.ac.tz/doc/PDF_GENERAL_EXAMINATION_REGULATIONS_AND_GUIDELINES_2024-1.pdf
- https://www.mnma.ac.tz/media_doc/ANNOUNCEMENT-2025-10-10_022919.pdf
- https://www.mnma.ac.tz/doc/1773211452_54bfb8d16c72379cdb6e.pdf

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
mnma/
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
- **Signal Strength:** Strong (expression of interest)
