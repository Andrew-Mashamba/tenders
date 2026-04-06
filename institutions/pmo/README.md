---
institution:
  name: "Ofisi ya Waziri Mkuu (Prime Minister's Office)"
  slug: "pmo"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "pmo.go.tz"

website:
  homepage: "https://www.pmo.go.tz/"
  tender_url: "https://www.pmo.go.tz/documents/tender"

contact:
  email: "ps@pmo.go.tz"
  phone: "022-09-23"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape tender listing from https://www.pmo.go.tz/documents/tender (Zabuni). Also check homepage Machapisho section and /documents/speeches-1 for Hotuba documents. Documents use /uploads/documents/ path with format sw-{timestamp}-{filename} or en-{timestamp}-{filename}."
  selectors:
    container: ".home-page, .container, main, .row"
    tender_item: ".carousel-item, .list-group-item, article, .document-item, tr"
    title: "h2, h3, h4, .tender-title, .dropdown-item, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/uploads/documents/"]'
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
      - "/uploads/documents/"
    url_patterns:
      - "pmo.go.tz/uploads/documents/*.pdf"
      - "pmo.go.tz/uploads/documents/*.doc"

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
      Documents stored at /uploads/documents/ with format sw-{timestamp}-{filename}.pdf or en-{timestamp}-{filename}.doc. Tender page at /documents/tender. Hotuba (speeches) at /documents/speeches-1. Follow document links from Machapisho dropdown (Zabuni, Taarifa U&T, etc).

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
  twitter: "tzwazirimkuu"
  instagram: "owm_tz"

notes: |
  Organization website at pmo.go.tz. Tender keywords detected: bid, manunuzi, procurement, tender, zabuni.
---

# PMO |   Mwanzo

**Category:** Government Agency
**Website:** https://www.pmo.go.tz/
**Tender Page:** https://www.pmo.go.tz/
**Keywords Found:** bid, manunuzi, procurement, tender, zabuni

## Contact Information
- Email: ps@pmo.go.tz
- Phone: 022-09-23
- Phone: 023-2024   
- Phone: 023-04-05
- Phone: 077450249370
- Phone: 022-04-27

## Scraping Instructions

**Strategy:** Scrape https://www.pmo.go.tz/ for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get



### Tender Content Preview

> el-reports'>Taarifa U&T Zabuni Kalenda ya Serikali <a class='dropdown-item' href= 'https://www.pmo.go.tz/do

### Document Links Found

- https://www.pmo.go.tz/uploads/documents/sw-1656588920-30.06.2022 - edited HOJA YA WAZIRI MKUU KUAHIRISHA MKUTANO WA 7 WA BUNGE LA 12.doc
- https://www.pmo.go.tz/uploads/documents/sw-1652256010-27.04.2022 edited HOTUBA YA WAZIRI MKUU TATHMINI NA UFUATILIAJI.doc
- https://www.pmo.go.tz/uploads/documents/sw-1680696717-05.04.2023 HOTUBA YA BAJETI OWM 2023-2024 Waandishi.doc
- https://www.pmo.go.tz/uploads/documents/sw-1744092373-HOTUBA YA WAZIRI MKUU WA JAMHURI YA MUUNGANO WA TANZANIA - KUWASILISHA BAJETI 2025-2026.pdf
- https://www.pmo.go.tz/uploads/documents/sw-1676020482-HOTUBA YA WAZIRI MKUU KUAHIRISHA MKUTANO WA 10 WA BUNGE LA 12 10.02.2023 .doc
- https://www.pmo.go.tz/uploads/documents/sw-1663938304-FINAL-HOJA YA WM - KUAHIRISHA BUNGE 23.09.2022.doc

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
pmo/
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
- **Signal Strength:** Strong (manunuzi, procurement, tender, zabuni)
