---
institution:
  name: "Dodoma City Council (Halmashauri ya Jiji la Dodoma)"
  slug: "dodomamc"
  category: "Government"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://dodomamc.go.tz"
  tender_url: "https://dodomamc.go.tz/procurement"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /procurement page (Manunuzi). Tender links (Zabuni) in sidebar/list. As of 2026-03-15 only expired 2018 tenders listed (Zabuni za Wakala, Zabuni ya Usafi wa Mazingira - closing June 2018). News items in li with col-md-4/col-md-8. Documents at /storage/app/uploads/public/*. Use -k for SSL. October CMS."
  selectors:
    container: ".container, #main-menu, .col-md-8, .sidebar"
    tender_item: "li a[href*='storage'], .col-md-4, .col-md-8, li"
    title: "h4, a"
    date: "span"
    document_link: 'a[href*="storage/app/uploads/public"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: ".pagination a, a.next"
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
      - "/storage/app/uploads/public/5b1/803/1e7/"
      - "/storage/app/uploads/public/5b1/803/dd6/"
      - "/storage/app/uploads/public/668/cce/dd5/"
      - "/storage/app/uploads/public/668/ccf/253/"
      - "/storage/app/uploads/public/66c/d6c/96d/"

    url_patterns:
      - "dodomamc.go.tz/storage/app/uploads/public/*/*/*/*.pdf"

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
      Dodoma City Council (Halmashauri ya Jiji la Dodoma). Zabuni (tenders) linked from /procurement. Documents at /storage/app/uploads/public/{hash}/{hash}/{hash}/. Example: Zabuni za Wakala wa Ukusanyaji Mapato, Zabuni ya Usafi wa Mazingira. News at /new/{slug}. Use curl -k for SSL.

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
  Category: Government. Keywords found: manunuzi, tenders, tender, procurement, zabuni.
  Emails: cd@dodomacc.go.tz.
  Discovered by crawler on 2026-03-15.
---

# Dodomamc

**Category:** Government
**Website:** https://dodomamc.go.tz
**Tender Page:** https://dodomamc.go.tz

## Scraping Instructions

**Strategy:** Scrape homepage and linked pages for tender/procurement documents. 7 document links discovered.
**Method:** http_get

Keywords found on site: manunuzi, tenders, tender, procurement, zabuni

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

Known document paths: /storage/app/uploads/public/5b1/803/1e7/, /storage/app/uploads/public/5b1/803/dd6/, /storage/app/uploads/public/668/cce/dd5/, /storage/app/uploads/public/668/ccf/253/, /storage/app/uploads/public/66c/d6c/96d/

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
dodomamc/
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
  "tender_id": "DODOMAMC-2026-001",
  "institution": "dodomamc",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "",
  "published_date": "2026-01-01",
  "closing_date": "2026-02-01",
  "closing_time": "14:00 EAT",
  "category": "Government",
  "status": "active",
  "source_url": "https://dodomamc.go.tz",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "",
      "local_path": "./downloads/DODOMAMC-2026-001/original/tender_document.pdf",
      "content_type": "application/pdf",
      "downloaded_at": ""
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "cd@dodomacc.go.tz",
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
