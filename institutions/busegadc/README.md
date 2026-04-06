---
institution:
  name: "Busegadc"
  slug: "busegadc"
  category: "Government"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://busegadc.go.tz"
  tender_url: "https://busegadc.go.tz/tenders"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage and linked pages for tender/procurement documents. Documents stored under /storage/app/uploads/public/. Follow links to tender detail pages for full document lists."
  selectors:
    container: "main, .content, .page-content, .entry-content, article, [role='main']"
    tender_item: "article, .tender-item, .card, .row, tr, li, .list-group-item"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
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
      - "/storage/app/uploads/public/"
      - "/storage/app/uploads/public/58d/438/ef2/"
      - "/storage/app/uploads/public/58d/439/700/"
      - "/storage/app/uploads/public/58d/43a/0e0/"
      - "/storage/app/uploads/public/58d/43a/7ee/"
      - "/storage/app/uploads/public/58d/50b/d0d/"
      - "/storage/app/uploads/public/5c2/da7/471/"
      - "/storage/app/uploads/public/5c2/da8/1a1/"

    url_patterns:
      - "busegadc.go.tz/storage/app/uploads/public/58d/438/ef2/*.pdf"
      - "busegadc.go.tz/storage/app/uploads/public/58d/439/700/*.pdf"
      - "busegadc.go.tz/storage/app/uploads/public/58d/43a/0e0/*.pdf"
      - "busegadc.go.tz/storage/app/uploads/public/58d/43a/7ee/*.pdf"
      - "busegadc.go.tz/storage/app/uploads/public/58d/50b/d0d/*.pdf"
      - "busegadc.go.tz/storage/app/uploads/public/5c2/da7/471/*.pdf"
      - "busegadc.go.tz/storage/app/uploads/public/5c2/da8/1a1/*.pdf"

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
      Documents under /storage/app/uploads/public/{hash}/ pattern (October CMS). Known paths: 58d/438/ef2/, 58d/439/700/, 58d/43a/0e0/, 58d/43a/7ee/, 58d/50b/d0d/, 5c2/da7/471/, 5c2/da8/1a1/. Site may be slow to respond.

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
  Category: Government. Keywords found: ununuzi, manunuzi, tenders, tender, zabuni.
  Emails: info@busegadc.go.tz.
  Discovered by crawler on 2026-03-15.
---

# Busegadc

**Category:** Government
**Website:** https://busegadc.go.tz
**Tender Page:** https://busegadc.go.tz

## Scraping Instructions

**Strategy:** Scrape homepage and linked pages for tender/procurement documents. 7 document links discovered.
**Method:** http_get

Keywords found on site: ununuzi, manunuzi, tenders, tender, zabuni

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

Known document paths: /storage/app/uploads/public/58d/438/ef2/, /storage/app/uploads/public/58d/439/700/, /storage/app/uploads/public/58d/43a/0e0/, /storage/app/uploads/public/58d/43a/7ee/, /storage/app/uploads/public/58d/50b/d0d/

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
busegadc/
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
  "tender_id": "BUSEGADC-2026-001",
  "institution": "busegadc",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "",
  "published_date": "2026-01-01",
  "closing_date": "2026-02-01",
  "closing_time": "14:00 EAT",
  "category": "Government",
  "status": "active",
  "source_url": "https://busegadc.go.tz",
  "documents": [
    {{
      "filename": "tender_document.pdf",
      "original_url": "",
      "local_path": "./downloads/BUSEGADC-2026-001/original/tender_document.pdf",
      "content_type": "application/pdf",
      "downloaded_at": ""
    }}
  ],
  "contact": {{
    "name": "Procurement Department",
    "email": "info@busegadc.go.tz",
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
