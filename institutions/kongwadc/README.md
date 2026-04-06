---
institution:
  name: "Kongwa District Council"
  slug: "kongwadc"
  category: "Government"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://kongwadc.go.tz"
  tender_url: "https://kongwadc.go.tz"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage for Zabuni section (table with Jina la Zabuni). Tenders appear in a table under .home-page-title. Also scrape /tenders and /tender for full listings. Documents at /storage/app/uploads/public/*/."
  selectors:
    container: ".right-sidebar-content .page-title, .home-page-title, table tbody"
    tender_item: "table tbody tr"
    title: "td:first-child, h4"
    date: "td:nth-child(2), .date"
    document_link: 'a[href*="/storage/"], a[href$=".pdf"], a[target="blank"]'
    pagination: ".pagination a, a.next, .view-more"
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
      - "/storage/app/media/uploaded-files/"
      - "/storage/app/uploads/public/5eb/d19/2f2/"
      - "/storage/app/uploads/public/5eb/d19/989/"
      - "/storage/app/uploads/public/5eb/d1a/576/"
      - "/storage/app/uploads/public/5f9/2eb/b10/"

    url_patterns:
      - "kongwadc.go.tz/storage/app/media/uploaded-files/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/5eb/d19/2f2/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/5eb/d19/989/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/5eb/d1a/576/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/5f9/2eb/b10/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/624/587/f55/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/62a/9ed/ad1/*.pdf"
      - "kongwadc.go.tz/storage/app/uploads/public/64b/fa6/c07/*.pdf"

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
      OctCMS site. Documents under /storage/app/media/uploaded-files/ and /storage/app/uploads/public/{hash}/. Each tender row has a "Pakua" (Download) link. Follow /tenders and /tender for full listings.

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
  Category: Government. Keywords found: procurement, tender, manunuzi, zabuni, tenders.
  Emails: ded@kongwadc.go.tz.
  Discovered by crawler on 2026-03-15.
---

# Kongwadc

**Category:** Government
**Website:** https://kongwadc.go.tz
**Tender Page:** https://kongwadc.go.tz

## Scraping Instructions

**Strategy:** Scrape homepage and linked pages for tender/procurement documents. 8 document links discovered.
**Method:** http_get

Keywords found on site: procurement, tender, manunuzi, zabuni, tenders, tangazo la zabuni

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

Known document paths: /storage/app/media/uploaded-files/, /storage/app/uploads/public/5eb/d19/2f2/, /storage/app/uploads/public/5eb/d19/989/, /storage/app/uploads/public/5eb/d1a/576/, /storage/app/uploads/public/5f9/2eb/b10/

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
kongwadc/
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
│   │   │   ├── specifications.docx
│   │   │   └── bill_of_quantities.xlsx
│   │   └── extracted/                 # AI-extracted text/data from documents
│   │       ├── tender_document.txt    # Plain text extraction from PDF
│   │       ├── specifications.txt
│   │       ├── summary.json           # AI-generated structured summary
│   │       └── key_dates.json         # Extracted dates & deadlines
│   └── ...
├── scrape_log.json                    # History of all scrape runs
└── last_scrape.json                   # Last scrape result snapshot
```

### Tender JSON Schema (`tenders/active/{tender_id}.json`)

```json
{{
  "tender_id": "KONGWADC-2026-001",
  "institution": "kongwadc",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "",
  "published_date": "2026-01-01",
  "closing_date": "2026-02-01",
  "closing_time": "14:00 EAT",
  "category": "Government",
  "status": "active",
  "source_url": "https://kongwadc.go.tz",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "",
      "local_path": "./downloads/KONGWADC-2026-001/original/tender_document.pdf",
      "content_type": "application/pdf",
      "downloaded_at": ""
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "ded@kongwadc.go.tz",
    "phone": "",
    "address": ""
  }},
  "eligibility": "Open to all registered suppliers",
  "scraped_at": "",
  "last_checked": ""
}}
```

## Post-Scrape Actions

After EACH successful scrape of this institution, the scraper MUST perform these steps in order:

### 1. Organize Tenders by Status
- Parse `closing_date` from each tender JSON
- **Active:** `closing_date` is in the future → `tenders/active/`
- **Closed:** `closing_date` has passed → move from `active/` to `closed/`
- **Archive:** `closing_date` is older than 90 days → move from `closed/` to `archive/`

### 2. Extract Text from Downloaded Documents
For each new document in `downloads/{tender_id}/original/`:
- **PDF:** Extract full text → save to `downloads/{tender_id}/extracted/{filename}.txt`
- **DOCX:** Extract full text → save to `downloads/{tender_id}/extracted/{filename}.txt`
- **XLSX:** Extract sheet names and cell data → save as JSON
- Generate `summary.json` with AI-extracted fields

### 3. Update `last_scrape.json`
Write/overwrite with current run status.

### 4. Append to `scrape_log.json`
Append a new entry to the runs array.

### 5. Update Global Active Tenders Index
After scraping, update: `/Volumes/DATA/PROJECTS/TENDERS/institutions/active_tenders.md`

### 6. Send Email Notification
Send a summary email using config from `/Volumes/DATA/PROJECTS/TENDERS/config/email.json`
