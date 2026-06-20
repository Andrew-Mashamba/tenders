---
institution:
  name: "The Institute of Public Administration"
  slug: "ipa"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "ipa.ac.tz"

website:
  homepage: "https://ipa.ac.tz/"
  tender_url: "https://ipa.ac.tz/"

contact:
  email: "info@ipa.ac.tz"
  phone: "+255 777 432 610"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Scrape https://ipa.ac.tz/ homepage and https://ipa.ac.tz/pmdu_unit.php for procurement notices.
    Announcements section (.card-comment) currently shows student admission lists only — not procurement.
    PMDU page has no active tender documents as of 2026-06-10. Documents stored under /documents/ when tenders are posted.
  selectors:
    container: "#why-us .card-success, .card.card-widget"
    tender_item: ".card-comment, .row.mb-2"
    title: ".comment-text, .comment-text a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="documents/"]'
    pagination: "" 
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
      - "/documents/3.9.2024/"

    url_patterns:
      - "ipa.ac.tz/documents/*"
      - "ipa.ac.tz/*.pdf"

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
      Documents stored under /documents/ (e.g. documents/3.9.2024/). Announcements section may link to PDFs.
      Downloads section uses relative paths; some links may use href="#" (broken). Verify before download.

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
  Organization website at ipa.ac.tz. Tender keywords detected: procurement.
---

# IPA

**Category:** Educational Institution
**Website:** https://ipa.ac.tz/
**Tender Page:** https://ipa.ac.tz/
**Keywords Found:** procurement

## Contact Information
- Email: info@ipa.ac.tz
- Phone: +255 777 432 610
- Phone: 025 - 
      

## Scraping Instructions

**Strategy:** Scrape https://ipa.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> /a> Legal Unit (LU) Procurement Management and Disposal Unit (PMDU) A

### Document Links Found

- https://ipa.ac.tz/documents/3.9.2024/selected student batch1 MSc.Human Resources.pdf

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
ipa/
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
