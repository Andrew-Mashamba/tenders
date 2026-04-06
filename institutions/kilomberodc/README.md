---
institution:
  name: "Halmashauri ya Wilaya ya Mlimba (MLIMBA DISTRICT COUNCIL)"
  slug: "kilomberodc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "kilomberodc.go.tz"

website:
  homepage: "https://kilomberodc.go.tz/"
  tender_url: "https://kilomberodc.go.tz/tenders"

contact:
  email: "ded@kilomberodc.go.tz"
  phone: "025-12-01 --- "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://kilomberodc.go.tz/tenders. Tenders are in a table (table.table-striped) with columns Tender Name, Date Added, Expire Date. Follow tender detail links for document downloads. Documents stored under /storage/app/uploads/public/ with path pattern {hash1}/{hash2}/{hash3}/{hash}.pdf."
  selectors:
    container: ".right-sidebar-content"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child a, td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: 'td a[href$=".pdf"], td a[href$=".doc"], td a[href$=".docx"], td a[href*="/storage/"], a[href*="/storage/app/uploads/public/"]'
    pagination: "nav.text-center a, .pagination a" 
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
      - "/storage/app/uploads/public/"
    url_patterns:
      - "kilomberodc.go.tz/storage/app/uploads/public/58d/2d2/271/58d2d227131ad057045709.pdf"
      - "kilomberodc.go.tz/storage/app/uploads/public/687/e84/1f9/687e841f9117a134678509.pdf"
      - "kilomberodc.go.tz/storage/app/uploads/public/687/d5b/5bf/687d5b5bf3254745459328.pdf"
      - "kilomberodc.go.tz/storage/app/uploads/public/687/d5a/391/687d5a391751f581057731.pdf"
      - "kilomberodc.go.tz/storage/app/uploads/public/58d/25c/83c/58d25c83cdf79771953364.pdf"

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
      Documents use path pattern /storage/app/uploads/public/{3-char}/{3-char}/{3-char}/{hash}.pdf (e.g. 58d/2d2/271/58d2d227131ad057045709.pdf). Follow tender detail links from table rows to reach document download links. Table may be empty when no active tenders.

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
  A default home page
---

# Home &#124; MLIMBA DISTRICT COUNCIL

**Category:** Local Government Authority
**Website:** https://kilomberodc.go.tz/
**Tender Page:** https://kilomberodc.go.tz/tenders
**Keywords Found:** manunuzi, tender, tenders, zabuni

## Contact Information
- Email: ded@kilomberodc.go.tz
- Phone: 025-12-01 --- 
- Phone: 023 293 1523 
- Phone: 025-04-01
- Phone: 0232931523 
- Phone: 024-11-01 --- 

## Scraping Instructions

**Strategy:** Scrape https://kilomberodc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> e-page-title">Zabuni zaidi Tender Name

### Known Tender URLs

- https://kilomberodc.go.tz/tenders

### Document Links Found

- http://gwf.egatest.go.tz/kilomberodc/storage/app/uploads/public/58d/25c/83c/58d25c83cdf79771953364.pdf
- https://kilomberodc.go.tz/storage/app/uploads/public/687/d5a/391/687d5a391751f581057731.pdf
- http://gwf.egatest.go.tz/kilomberodc/storage/app/uploads/public/58d/266/d99/58d266d99961a372879853.pdf
- https://kilomberodc.go.tz/storage/app/uploads/public/687/28a/9d9/68728a9d97649390639868.pdf
- https://kilomberodc.go.tz/storage/app/uploads/public/687/a34/0bf/687a340bf145f729800929.pdf
- https://kilomberodc.go.tz/storage/app/uploads/public/687/e84/1f9/687e841f9117a134678509.pdf
- https://kilomberodc.go.tz/storage/app/uploads/public/687/d5b/5bf/687d5b5bf3254745459328.pdf
- http://gwf.egatest.go.tz/kilomberodc/storage/app/uploads/public/58d/2d2/271/58d2d227131ad057045709.pdf
- http://www.kilomberodc.go.tz/storage/app/uploads/public/58d/8a5/829/58d8a582995fe512619623.pdf

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

Known document paths: /storage/app/uploads/public/58d/2d2/271/58d2d227131ad057045709.pdf, /storage/app/uploads/public/687/e84/1f9/687e841f9117a134678509.pdf, /storage/app/uploads/public/687/d5b/5bf/687d5b5bf3254745459328.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
kilomberodc/
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
- **Signal Strength:** Strong (manunuzi, tender, tenders, zabuni)
