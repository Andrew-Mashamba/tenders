---
institution:
  name: "Nyamwezi Teachers' College"
  slug: "nyamweziteachers"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "nyamweziteachers.ac.tz"

website:
  homepage: "https://nyamweziteachers.ac.tz/"
  tender_url: "https://nyamweziteachers.ac.tz/"

contact:
  email: "nyamweziteachers@yahoo.com"
  phone: "036426050102"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Homepage has AVAILABLE DOCUMENTS section with application forms and PDFs. Each item has title link and Posted date. Use Load More for pagination. Documents at /www/100/news/{hash}filename-{name}.pdf"
  selectors:
    container: ".contained-div, .main"
    tender_item: "a[href*='/www/100/news/']"
    title: "a[href*='/www/100/news/']"
    date: ".date, .post-date, .published, time"
    document_link: 'a[href*="/www/100/news/"], a[href$=".pdf"]'
    pagination: "a[href='news'] (Load More), .staff1_loadmore" 
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
        - 'a[href*="/www/100/news/"]'
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
      - "/www/100/news/"

    url_patterns:
      - "nyamweziteachers.ac.tz/www/100/news/*.pdf"
      - "nyamweziteachers.ac.tz/*.pdf"

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
      Documents in /www/100/news/{hash}filename-{filename}.pdf. URL format uses hash+filename. Application forms and joining instructions; Load More uses AJAX (morestaff1.php etc).

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
  NYAMWEZI TEACHERS’ COLLEGE - TABORA
---

# Home

**Category:** Educational Institution
**Website:** https://nyamweziteachers.ac.tz/
**Tender Page:** https://nyamweziteachers.ac.tz/
**Keywords Found:** bid, rfi

## Contact Information
- Email: nyamweziteachers@yahoo.com
- Phone: 036426050102
- Phone: 024-03-15
- Phone: 025-07-01
- Phone: 026-03-06
- Phone: 0754-366331

## Scraping Instructions

**Strategy:** Scrape https://nyamweziteachers.ac.tz/ for tender/procurement notices.
**Method:** http_get

NYAMWEZI TEACHERS’ COLLEGE - TABORA

### Document Links Found

- https://nyamweziteachers.ac.tz/www/100/news/b7a73ef33afilename-FOMU YA KUJIUNGA NYAMWENZI TEACHERS - NTC APPLICATION FORM 2026-2027.pdf
- https://nyamweziteachers.ac.tz/www/100/news/efe2ff6669filename-NTC JOINING INSTRUCTION FOR PRIMARY 2025_2026 (1).pdf
- https://nyamweziteachers.ac.tz/www/100/news/f992bf8bf6filename-a759b865cefilename-NEW-FORM-DEMA-SEPT 2024.pdf
- https://nyamweziteachers.ac.tz/www/100/news/fa8d45ffcbfilename-TPC APPLICATION FORM FOR DEMA 2026.pdf
- https://nyamweziteachers.ac.tz/www/100/news/1e4e2286fbfilename-2025-FOMU YA KUJIUNGA - NTC APPLICATION FORM 2025-2026.pdf

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
nyamweziteachers/
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
- **Signal Strength:** Weak (supply/rfi only)
