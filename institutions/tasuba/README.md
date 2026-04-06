---
institution:
  name: "Taasisi ya Sanaa na Utamaduni Bagamoyo (TaSUBa)"
  slug: "tasuba"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "tasuba.ac.tz"

website:
  homepage: "https://tasuba.ac.tz/"
  tender_url: "https://tasuba.ac.tz/tenders"

contact:
  email: "application@tasuba.ac.tz"
  alternate_emails:
    - "bagamoyofest@tasuba.ac.tz"
    - "info@tasuba.ac.tz"
  phone: "0365-149010383"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /tenders page. Laravel-style site with documents at /storage/app/uploads/public/. Page has 'Zabuni Zaidi' (More Tenders) - table or list structure. Follow document links from tender rows."
  selectors:
    container: ".tender-list, .content, main, table, .home-page-title, [class*='zabuni']"
    tender_item: "table tbody tr, article, .tender-item, .card, .row, li"
    title: "h2, h3, h4, .tender-title, td a, a[href*='storage']"
    date: ".date, .closing-date, .published, time, td"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/storage/app/uploads/"]'
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

    url_patterns:
      - "tasuba.ac.tz/storage/app/uploads/public/65d/d8c/21c/65dd8c21c79f7577816580.pdf"
      - "tasuba.ac.tz/storage/app/uploads/public/66a/1dc/9f1/66a1dc9f1661d680635355.pdf"
      - "tasuba.ac.tz/storage/app/uploads/public/65d/d8c/65c/65dd8c65cfb11285040298.pdf"
      - "tasuba.ac.tz/storage/app/uploads/public/66f/b9c/c04/66fb9cc04c34d826035970.pdf"
      - "tasuba.ac.tz/storage/app/uploads/public/65d/d97/2da/65dd972dab214291285955.pdf"

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

    known_document_paths:
      - "/storage/app/uploads/public/"

    document_notes: |
      Documents in /storage/app/uploads/public/ with hash-style paths (e.g. 65d/d8c/21c/filename.pdf). Page may be slow to load - consider longer timeout. Tender table has 'Jina la Zabuni' (Tender Name) column.

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
  facebook: "Taasisi-ya-Sanaa-na-Utamaduni-Bagamoyo-1495193530767653"
  twitter: "TAASISISANAA"
  instagram: "tasuba_bagamoyo"

notes: |
  A default home page
---

# Home &#124; TAASISI YA SANAA NA UTAMADUNI BAGAMOYO (TaSUBa)

**Category:** Educational Institution
**Website:** https://tasuba.ac.tz/
**Tender Page:** https://tasuba.ac.tz/tenders
**Keywords Found:** tender, tenders, zabuni

## Contact Information
- Email: application@tasuba.ac.tz
- Email: bagamoyofest@tasuba.ac.tz
- Email: info@tasuba.ac.tz
- Phone: 0365-149010383
- Phone: 025-2026
	    
- Phone: 026
	        
- Phone: +255 762544613 
- Phone: +255 766 264 581 

## Scraping Instructions

**Strategy:** Scrape https://tasuba.ac.tz/tenders for tender/procurement notices.
**Method:** http_get

A default home page

### Tender Content Preview

> ="home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://tasuba.ac.tz/tenders

### Document Links Found

- https://tasuba.ac.tz/storage/app/uploads/public/65d/d8c/65c/65dd8c65cfb11285040298.pdf
- https://tasuba.ac.tz/storage/app/uploads/public/65d/d97/2da/65dd972dab214291285955.pdf
- https://tasuba.ac.tz/storage/app/uploads/public/66a/1dc/9f1/66a1dc9f1661d680635355.pdf
- https://tasuba.ac.tz/storage/app/uploads/public/65d/d8c/21c/65dd8c21c79f7577816580.pdf
- https://tasuba.ac.tz/storage/app/uploads/public/66f/b9c/c04/66fb9cc04c34d826035970.pdf

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

Known document paths: /storage/app/uploads/public/65d/d8c/21c/65dd8c21c79f7577816580.pdf, /storage/app/uploads/public/66a/1dc/9f1/66a1dc9f1661d680635355.pdf, /storage/app/uploads/public/65d/d8c/65c/65dd8c65cfb11285040298.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tasuba/
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
- **Signal Strength:** Strong (tender, tenders, zabuni)
