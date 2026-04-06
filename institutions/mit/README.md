---
institution:
  name: "MIT | Matukio/Matangazo (Ministry of Industry and Trade)"
  slug: "mit"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "mit.go.tz"

website:
  homepage: "https://www.viwanda.go.tz/"
  tender_url: "https://www.viwanda.go.tz/events"

contact:
  email: "ps@mit.go.tz"
  alternate_emails:
    - "dawatilamsaada@mit.go.tz"
    - "info@mit.go.tz"
  phone: "026
         "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.viwanda.go.tz/events for Matukio/Matangazo (events/announcements). Each item has date, title, and Soma zaidi link to detail page. Documents under /uploads/documents/."
  selectors:
    container: ".post-slide7, .content, main, .entry-content, .page-content, ul"
    tender_item: ".post-slide7, .post-description, li"
    title: ".post-description a, h3, h4, a"
    date: ".post-bar li, .date, time"
    document_link: 'a[href$=".pdf"], a[href*="/uploads/documents/"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination .page-link, .pagination a, a.next" 
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
      - "mit.go.tz/uploads/documents/sw-1717152088-HOTUBA%20YA%20BAJETI%20%20YA%20WIZARA%20YA%20VIWANDA%20NA%20BIASHARA%20-%202024-2025%20.pdf"
      - "mit.go.tz/uploads/documents/sw-1755520772-Tangazo%20-%20MIT%20%202025%20Mnada.pdf"
      - "mit.go.tz/uploads/documents/en-1747115028-hotuba_online_compressed.pdf"

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
      - "/uploads/documents/"
    document_notes: |
      MIT/viwanda.go.tz stores documents under /uploads/documents/ with pattern sw-{timestamp}-{name}.pdf or en-{timestamp}-{name}.pdf. Follow Soma zaidi links to detail pages for document downloads.

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
  facebook: "profile.php"
  twitter: "viwandabiashara"
  instagram: "viwandabiashara"

notes: |
  Organization website at mit.go.tz. Tender keywords detected: bid, procurement, supply.
---

# MIT |   Mwanzo

**Category:** Government Agency
**Website:** https://www.viwanda.go.tz/
**Tender Page:** https://www.viwanda.go.tz/
**Keywords Found:** bid, procurement, supply

## Contact Information
- Email: ps@mit.go.tz
- Email: dawatilamsaada@mit.go.tz
- Email: info@mit.go.tz
- Phone: 026
         
- Phone: 02024-2025
- Phone: 0 0 2000 128
- Phone: 00979116411617
- Phone: 0528347876

## Scraping Instructions

**Strategy:** Scrape https://www.viwanda.go.tz/ for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get



### Tender Content Preview

> >Mawasiliano Serikalini Usimamizi wa Ununuzi Huduma za Sheria <a class='dropdown-item' href= 'ht

### Document Links Found

- https://www.viwanda.go.tz/uploads/documents/en-1747115028-hotuba_online_compressed.pdf
- https://www.viwanda.go.tz/uploads/documents/sw-1717152088-HOTUBA%20YA%20BAJETI%20%20YA%20WIZARA%20YA%20VIWANDA%20NA%20BIASHARA%20-%202024-2025%20.pdf
- https://www.viwanda.go.tz/uploads/documents/sw-1755520772-Tangazo%20-%20MIT%20%202025%20Mnada.pdf

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

Known document paths: /uploads/documents/sw-1717152088-HOTUBA%20YA%20BAJETI%20%20YA%20WIZARA%20YA%20VIWANDA%20NA%20BIASHARA%20-%202024-2025%20.pdf, /uploads/documents/sw-1755520772-Tangazo%20-%20MIT%20%202025%20Mnada.pdf, /uploads/documents/en-1747115028-hotuba_online_compressed.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
mit/
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
