---
institution:
  name: "Tanzania Public Health Association"
  slug: "tpha"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tpha.or.tz"

website:
  homepage: "https://tpha.or.tz/"
  tender_url: "https://tpha.or.tz/"

contact:
  email: "tpha1980@yahoo.com"
  phone: "+255737728254"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage. Documents are in 'News & Updates' sidebar (.box ul li). Each item has direct PDF/DOCX links. No dedicated tender listing - documents are announcements, conference forms, membership forms."
  selectors:
    container: ".box, #slideshows .col-lg-4 .box, main#main"
    tender_item: ".box ul li, .box ul li a"
    title: "a, .carousel-caption h4"
    date: ".carousel-caption h5"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
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
      - "/uploads/events_files/"
    url_patterns:
      - "tpha.or.tz/uploads/events_files/*.pdf"
      - "tpha.or.tz/uploads/events_files/*.docx"
      - "tpha.or.tz/uploads/events_files/*.doc"

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
      Documents in /uploads/events_files/ with hash-style filenames (e.g. 175879544568d516b59d7c0.docx). Link text is the document title. News & Updates sidebar lists PDFs and DOCX. Includes conference announcements, membership forms, CPD materials.

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
  facebook: "tpha.tanzania"
  twitter: "afyayajamiitz"

notes: |
  TPHA is a non-governmental organization (NGO) established in 1980 with the goal of promoting health and preventing disease in Tanzania through sound public health practices. The association draws its membership from all over Tanzania and is open to non-Tanzanians residing within and outside the country.
---

# Tanzania Public Health Association

**Category:** NGO / Non-Profit Organization
**Website:** https://tpha.or.tz/
**Tender Page:** https://tpha.or.tz/
**Keywords Found:** tender, tenders

## Contact Information
- Email: tpha1980@yahoo.com
- Phone: +255737728254
- Phone: 048951285
- Phone: 03334689398
- Phone: 065752145
- Phone: 058773695

## Scraping Instructions

**Strategy:** Scrape https://tpha.or.tz/ for tender/procurement notices.
**Method:** http_get

TPHA is a non-governmental organization (NGO) established in 1980 with the goal of promoting health and preventing disease in Tanzania through sound public health practices. The association draws its membership from all over Tanzania and is open to non-Tanzanians residing within and outside the country.

### Tender Content Preview

> a name="dcterms.Language" content="en"> <meta name="dcterms.Type" content=

### Document Links Found

- http://tpha.or.tz/uploads/events_files/1719596013667ef3edb2ce8.docx
- http://tpha.or.tz/uploads/events_files/1747911002682f015a25d9f.docx
- http://tpha.or.tz/uploads/events_files/174245762367dbcb178eaf6.pdf
- http://tpha.or.tz/uploads/events_files/1611228114600963d2deb55.pdf
- http://tpha.or.tz/uploads/events_files/1738309094679c7de65a985.pdf
- http://tpha.or.tz/uploads/events_files/175879544568d516b59d7c0.docx
- http://tpha.or.tz/uploads/events_files/174531772568076f5d0a770.pdf
- http://tpha.or.tz/uploads/events_files/1754502369689394e12b57f.pdf

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

Known document paths: /uploads/events_files/1611228114600963d2deb55.pdf, /uploads/events_files/174245762367dbcb178eaf6.pdf, /uploads/events_files/175879544568d516b59d7c0.docx

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tpha/
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
- **Signal Strength:** Strong (tender, tenders)
