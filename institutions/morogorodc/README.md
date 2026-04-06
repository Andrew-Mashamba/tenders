---
institution:
  name: "Morogoro District Council"
  slug: "morogorodc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "morogorodc.go.tz"

website:
  homepage: "https://morogorodc.go.tz/"
  tender_url: "https://morogorodc.go.tz/tenders"

contact:
  email: "ded@morogorodc.go.tz"
  phone: "+255 23 2935458 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Fetch https://morogorodc.go.tz/tenders. Parse table.table.table-striped inside .right-sidebar-content. Each tbody tr = one tender. Columns: Tender Name (td:first-child), Tarehe iliyoongezwa (td:nth-child(2)), Tarehe ya Mwisho (td:nth-child(3)), document link 'Pakua' (td:nth-child(4) a). Download from href. Follow nav.text-center for pagination."
  selectors:
    container: ".right-sidebar-content"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: 'td a[href*=".pdf"], td a[href*=".doc"], td a[href*=".docx"], td a[href*=".zip"], td a[target="blank"]'
    pagination: "nav.text-center a"
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
      - "/storage/app/media/uploaded-files/"
    url_patterns:
      - "morogorodc.go.tz/storage/app/uploads/public/*"
      - "morogorodc.go.tz/storage/app/media/uploaded-files/*"

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
      October CMS. Documents in /storage/app/uploads/public/{hash}/ (PDF, ZIP) and /storage/app/media/uploaded-files/. Table has 'Pakua' (Download) links in last column. Resolve relative hrefs to full URLs.

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

# Home &#124; Morogoro District Council

**Category:** Local Government Authority
**Website:** https://morogorodc.go.tz/
**Tender Page:** http://gwf.egatest.go.tz/morogorodc/storage/app/media/uploaded-files/Tanzania%20Public%20Procurement%20Act%202011.pdf
**Keywords Found:** manunuzi, procurement, tender, tenders, zabuni

## Contact Information
- Email: ded@morogorodc.go.tz
- Phone: +255 23 2935458 
- Phone: 018-09-20
- Phone: 06400000000-
- Phone: 016-11-11 --- 
- Phone: 024
          

## Scraping Instructions

**Strategy:** Scrape http://gwf.egatest.go.tz/morogorodc/storage/app/media/uploaded-files/Tanzania%20Public%20Procurement%20Act%202011.pdf for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> me-page-title">Zabuni Zaidi Tender Name

### Known Tender URLs

- http://gwf.egatest.go.tz/morogorodc/storage/app/media/uploaded-files/Tanzania%20Public%20Procurement%20Act%202011.pdf
- https://morogorodc.go.tz/procurement-and-supplies
- https://morogorodc.go.tz/tenders

### Document Links Found

- http://gwf.egatest.go.tz/morogorodc/storage/app/media/uploaded-files/Tanzania%20Public%20Procurement%20Act%202011.pdf
- http://gwf.egatest.go.tz/morogorodc/storage/app/media/uploaded-files/Land%20Act%202004.pdf
- https://morogorodc.go.tz/storage/app/uploads/public/5a3/377/009/5a3377009b367562941850.pdf
- https://morogorodc.go.tz/storage/app/uploads/public/5bc/33f/465/5bc33f4658cda103332905.pdf
- https://morogorodc.go.tz/storage/app/uploads/public/5bc/341/103/5bc341103de0c973003325.pdf
- https://morogorodc.go.tz/storage/app/uploads/public/612/758/0b0/6127580b057d4167606376.pdf
- https://morogorodc.go.tz/storage/app/uploads/public/5a3/18a/124/5a318a12475d3840738674.zip
- https://morogorodc.go.tz/storage/app/uploads/public/671/2af/ea9/6712afea97f9e807758909.pdf

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

Known document paths: /storage/app/uploads/public/671/2af/ea9/6712afea97f9e807758909.pdf, /storage/app/uploads/public/5bc/33f/465/5bc33f4658cda103332905.pdf, /storage/app/uploads/public/5a3/377/009/5a3377009b367562941850.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
morogorodc/
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
- **Signal Strength:** Strong (manunuzi, procurement, tender, tenders, zabuni)
