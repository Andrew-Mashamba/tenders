---
institution:
  name: "RAFIKI-SDO | Centre for Youth & Children's Rights"
  slug: "rafikisdo"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "rafikisdo.or.tz"

website:
  homepage: "https://rafikisdo.or.tz/"
  tender_url: "https://rafikisdo.or.tz/tender.html"

contact:
  email: "info@rafikisdo.or.tz"
  alternate_emails:
    - "accounts@thememascot.com"
  phone: "0622 448 838"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://rafikisdo.or.tz/tender.html. Tenders are listed under h2 'NEW RAFIKI-SDO TENDER ADVERTISEMENTS'. Each tender is an ol.breadcrumb > li containing an anchor with PDF href. Title and deadline are in the link text. Documents are relative PDF paths in same directory."
  selectors:
    container: ".breadcrumb.text-center.mt-10.white, section .container .row"
    tender_item: "ol.breadcrumb.text-center.mt-10.white li"
    title: "a"
    date: "a"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: null
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
      - "/"
    url_patterns:
      - "rafikisdo.or.tz/*.pdf"
      - "rafikisdo.or.tz/tender.html"

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
      PDFs are stored in same directory as tender.html (relative paths like "FINAL PRE-QUALIFIED VENDORS.pdf"). Resolve to https://rafikisdo.or.tz/PDF.pdf. Title and deadline embedded in link text (e.g. "Deadline for submission is 15th December,2024 at 17:00 hours").

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
  facebook: "rafikisdotz"
  twitter: "rafikisdotz"
  instagram: "rafikisdotz"

notes: |
  RAFIKI-SDO | Nonprofit,Centre for Youth & Children`s Rights
---

# RAFIKI-SDO | Centre for Youth & Children`s Rights

**Category:** NGO / Non-Profit Organization
**Website:** https://rafikisdo.or.tz/
**Tender Page:** https://rafikisdo.or.tz/tender.html
**Keywords Found:** rfi, tender

## Contact Information
- Email: info@rafikisdo.or.tz
- Email: accounts@thememascot.com
- Phone: 0622 448 838
- Phone: +255 754 448 838

## Scraping Instructions

**Strategy:** Scrape https://rafikisdo.or.tz/tender.html for tender/procurement notices.
**Method:** http_get

RAFIKI-SDO | Nonprofit,Centre for Youth & Children`s Rights

### Tender Content Preview

> | Tender | PRS-Rafiki SDO LogIn

### Known Tender URLs

- https://rafikisdo.or.tz/tender.html

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
rafikisdo/
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
- **Signal Strength:** Strong (tender)
