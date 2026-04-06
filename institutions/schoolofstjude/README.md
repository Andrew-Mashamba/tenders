---
institution:
  name: "The School of St Jude"
  slug: "schoolofstjude"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "schoolofstjude.co.tz"

website:
  homepage: "https://www.schoolofstjude.org/"
  tender_url: "https://www.schoolofstjude.org/tenders/"

contact:
  phone: "088-370045"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /tenders/ page. Tenders in .fieldlist_wrapper as .fielditem elements. Each has title in .fielditem__heading, reference in .fieldlist__block--ref, closing date in .tender_expiry, PDF link in .button--download. Follow pagination via .oxy-repeater-pages-wrap."
  selectors:
    container: ".fieldlist-wrapper, .oxy-dynamic-list.fieldlist_wrapper"
    tender_item: ".fielditem.fielditem--margin"
    title: ".fielditem__heading, h4.ct-headline"
    date: ".tender_expiry, .code_block.tender_expiry"
    document_link: 'a.button--download, a.ct-link[href$=".pdf"]'
    pagination: ".oxy-repeater-pages-wrap .page-numbers, a.next.page-numbers" 
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
      - "schoolofstjude.org/wp-content/uploads/*/Tender-advert-*.pdf"
      - "schoolofstjude.org/wp-content/uploads/*/*/*.pdf"

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
      Tender PDFs in /wp-content/uploads/YYYY/MM/ (e.g. Tender-advert-IT-Servers.pdf). Reference in .fieldlist__block--ref (e.g. TSOSJ/2026/Server). Date format: DD/MM/YYYY HH:MM am. Pagination: /tenders/page/2/, etc.

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
  facebook: "schoolofstjude"
  twitter: "uwt"
  linkedin: "school-of-st-jude"
  instagram: "schoolofstjude"

notes: |
  The School of St Jude is a pioneering leader in charitable education within Africa.
---

# The School of St Jude &ndash; Fighting poverty through education

**Category:** Commercial / Private Sector
**Website:** https://www.schoolofstjude.org/
**Tender Page:** https://www.schoolofstjude.org/tenders/
**Keywords Found:** eoi, rfi, tender, tenders

## Contact Information
- Phone: 088-370045
- Phone: 03-370045
- Phone: 005-370045
- Phone: 062-308467
- Phone: 064-308467

## Scraping Instructions

**Strategy:** Scrape https://www.schoolofstjude.org/tenders/ for tender/procurement notices.
**Method:** http_get

The School of St Jude is a pioneering leader in charitable education within Africa.

### Tender Content Preview

> iv> <img id="image-226-52" alt="" src="https://www.schoolofstjude.org/wp-content/uploads/2021/10/tender_ico.svg" c

### Known Tender URLs

- https://www.schoolofstjude.org/tenders/

### Document Links Found

- https://www.schoolofstjude.org/wp-content/uploads/2025/05/Visitor-Brochure.pdf

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

Known document paths: /wp-content/uploads/2025/05/Visitor-Brochure.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
schoolofstjude/
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
- **Signal Strength:** Strong (eoi, tender, tenders)
