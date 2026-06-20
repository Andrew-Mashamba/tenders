---
institution:
  name: "Savannah Plains"
  slug: "savannahplains"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "savannahplains.ac.tz"

website:
  homepage: "https://savannahplains.ac.tz/"
  tender_url: "https://savannahplains.ac.tz/"

contact:
  email: "info@savannahplains.ac.tz"
  phone: "015-05-03"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Educational institution — no procurement tenders. /admission/ has joining/application PDFs only (reject as non-tender). Homepage has no tender listings. WordPress site."
  selectors:
    container: "#main-content, .main-section, .page-section .container"
    tender_item: ".cs-holder, article, .cs-newslist article"
    title: "h2, h4, .cs-section-title, .pdf-file"
    date: ".date, time"
    document_link: 'a.pdf-file, a[href$=".pdf"]'
    pagination: ".pagination a, a.next" 
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
      - "savannahplains.ac.tz/wp-content/uploads/*/*/*.pdf"

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
      Documents in /wp-content/uploads/YYYY/MM/. Links use class .pdf-file. Mostly joining instructions and application forms; RFI/procurement content is weak.

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
  Organization website at savannahplains.ac.tz. Tender keywords detected: rfi.
---

# Savannah Plains

**Category:** Educational Institution
**Website:** https://savannahplains.ac.tz/
**Tender Page:** https://savannahplains.ac.tz/
**Keywords Found:** rfi

## Contact Information
- Email: info@savannahplains.ac.tz
- Phone: 015-05-03
- Phone: 0 1 0 0 12 6 6 
- Phone: +255 742 555 550
- Phone: 0 0 0 0-12
- Phone: 026-03-09 09

## Scraping Instructions

**Strategy:** Scrape https://savannahplains.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Document Links Found

- https://savannahplains.ac.tz/wp-content/uploads/2022/01/O-AND-A-LEVEL-Application-Form-2022.pdf
- https://savannahplains.ac.tz/wp-content/uploads/2024/12/DOC-20241211-WA0227.pdf
- https://savannahplains.ac.tz/wp-content/uploads/2024/01/Joining-Instruction-A-Level-new-2024.pdf
- https://savannahplains.ac.tz/wp-content/uploads/2026/02/PRE-FORM-5-JOINING-INSTRUCTIONS-2026.pdf

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

Known document paths: /wp-content/uploads/2026/02/PRE-FORM-5-JOINING-INSTRUCTIONS-2026.pdf, /wp-content/uploads/2024/12/DOC-20241211-WA0227.pdf, /wp-content/uploads/2024/01/Joining-Instruction-A-Level-new-2024.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
savannahplains/
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

- **Last Checked:** 11 June 2026
- **Active Tenders:** 0 (admission/joining forms only — not procurement)
- **Signal Strength:** None (no procurement section)
