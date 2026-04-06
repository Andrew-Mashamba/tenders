---
institution:
  name: "Global Publishers"
  slug: "globalpublishers"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "globalpublishers.co.tz"

website:
  homepage: "https://globalpublishers.co.tz/"
  tender_url: "https://globalpublishers.co.tz/category/ajira/"

contact:
  phone: "020           "

scraping:
  enabled: true
  method: "http_get"
  strategy: "DISABLED: Ajira category is job vacancies (nafasi za kazi) only, not procurement tenders. All content is employment postings. No tender/procurement content."
  selectors:
    container: ".col-lg-8 .row.g-4, .container.mb-5"
    tender_item: ".archive-card"
    title: ".post-title a, h2.post-title a"
    date: ".post-meta"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href$=".xlsx"], a[download]'
    pagination: "link[rel='next'], .pagination a, a.next" 
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
      - "globalpublishers.co.tz/wp-content/uploads/*"
      - "globalpublishers.co.tz/*.pdf"

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
      WordPress site. Documents in /wp-content/uploads/. Ajira category lists job postings; follow each article link to find PDF/DOC attachments in post content.

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
  facebook: "Globalpublishers"
  twitter: "intent"
  instagram: "globalpublishers"

notes: |
  Position: Procurement Assistant– Service Contract Appointment- G 5 Position No.18/2019 Expected appointment date: Immediate Duration: One Year (renewable on satisfactory...
---

# Procurement Assistant at World Food Programme June, 2019 - Global Publishers

**Category:** Commercial / Private Sector
**Website:** https://globalpublishers.co.tz/
**Tender Page:** https://twitter.com/intent/tweet?url=https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F&text=Procurement+Assistant+at+World+Food+Programme+June%2C+2019
**Keywords Found:** procurement, tender, tenders

## Contact Information
- Phone: 020           
- Phone: 019           
- Phone: 026-01-28-
- Phone: 019-06-05
- Phone: 021           

## Scraping Instructions

**Strategy:** Scrape https://twitter.com/intent/tweet?url=https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F&text=Procurement+Assistant+at+World+Food+Programme+June%2C+2019 for tender/procurement notices.
**Method:** http_get

Position: Procurement Assistant– Service Contract Appointment- G 5 Position No.18/2019 Expected appointment date: Immediate Duration: One Year (renewable on satisfactory...

### Tender Content Preview

> ibute documents, to support successful procurement programs and operational activities, (e.g. issue tenders, evaluate offers and negotiate/award contracts), ensuring standard processes are followed. Review, record and prioritise purchasing requests, ensuring all supporting documentation is re

### Known Tender URLs

- https://twitter.com/intent/tweet?url=https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F&text=Procurement+Assistant+at+World+Food+Programme+June%2C+2019
- https://api.whatsapp.com/send?text=Procurement+Assistant+at+World+Food+Programme+June%2C+2019 https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F
- https://globalpublishers.co.tz/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F
- https://globalpublishers.co.tz/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F&#038;format=xml
- https://globalpublishers.co.tz/2019/06/05/procurement-assistant-world-food-programme-june-2019/
- https://globalpublishers.co.tz/2019/06/30/nafasi-za-kazi-benki-ya-tib-procurement-supplies-officers/
- https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fglobalpublishers.co.tz%2F2019%2F06%2F05%2Fprocurement-assistant-world-food-programme-june-2019%2F

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
globalpublishers/
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
- **Signal Strength:** Strong (procurement, tender, tenders)
