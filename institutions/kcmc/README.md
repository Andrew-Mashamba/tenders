---
institution:
  name: "KCMC · Kilimanjaro Christian Medical Centre"
  slug: "kcmc"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "kcmc.ac.tz"

website:
  homepage: "https://kcmc.ac.tz/"
  tender_url: "https://kcmc.ac.tz/"

contact:
  email: "kcmcadmin@kcmc.ac.tz"
  phone: "026
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape KCMC homepage. Tenders/jobs appear in .announce-right panel. Use .announce-header to switch between Events and Jobs tabs. Each .announce-card contains title, meta, and document links. Documents stored under /announcements/."
  selectors:
    container: ".announce-right, .announce-content, .content-pane"
    tender_item: ".announce-card.events-card"
    title: ".card-title, .card-sub"
    date: ".card-meta, .due-badge"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/announcements/"]'
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
        - 'a[href*="/announcements/"]'
        - 'a[href*="/storage/"]'
        - 'a[href*="/uploads/"]'
        - 'a[href*="/media/"]'
        - 'a[href*="/wp-content/uploads/"]'
        - 'a[href*="/download"]'
        - 'a[download]'
      resolve_redirects: true
      decode_percent_encoding: true

    known_document_paths:
      - "/announcements/"

    url_patterns:
      - "kcmc.ac.tz/announcements/*.pdf"
      - "kcmc.ac.tz/announcements/*.doc"
      - "kcmc.ac.tz/announcements/*.docx"

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
      Documents stored at /announcements/ (e.g. Job Advertisment-Data Scientist.pdf, dialysis short course may-2026.pdf). Links may be in hidden anchors; check all a[href*="/announcements/"].

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
  instagram: "kcmc1971"

notes: |
  Organization website at kcmc.ac.tz. Tender keywords detected: procurement.
  NOTE (2026-03-15): .announce-right shows Jobs (nafasi za kazi) and Events (short courses). Exclude jobs-card — job postings are NOT procurement tenders. Dialysis short course is training, not tender.
---

# KCMC · Kilimanjaro Christian Medical Centre

**Category:** Educational Institution
**Website:** https://kcmc.ac.tz/
**Tender Page:** https://kcmc.ac.tz/
**Keywords Found:** procurement

## Contact Information
- Email: kcmcadmin@kcmc.ac.tz
- Phone: 026
          
- Phone: +255 27
          
- Phone: 000
          
- Phone: 0 11-18 0 9 9 0
- Phone: 026-02-21

## Scraping Instructions

**Strategy:** Scrape https://kcmc.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ICT Procurement Finance Engineering Administr

### Document Links Found

- https://kcmc.ac.tz/announcements/Job Advertisment-Data Scientist.pdf
- https://kcmc.ac.tz/announcements/dialysis short course may-2026.pdf

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
kcmc/
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
