---
institution:
  name: "National Institute of Transport (NIT)"
  slug: "nit"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "nit.ac.tz"

website:
  homepage: "https://nit.ac.tz/"
  tender_url: "https://nit.ac.tz/posts/announcements/"

contact:
  email: "rector@nit.ac.tz"
  phone: "026
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://nit.ac.tz/posts/announcements/ and homepage carousel. Uses Alpine.js. Announcements have title (h4), date, and direct PDF links. Documents at /media/uploads/files/ (hash filenames) and /media/uploads/downloads/."
  selectors:
    container: "main, .content, .announcements, .posts-list"
    tender_item: "article, .post-item, .announcement-item, .card, a[href$='.pdf']"
    title: "h4, h3, .title, a"
    date: ".date, .created_at, time, span"
    document_link: 'a[href$=".pdf"], a[href*="/media/uploads/"]'
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
      - "/media/uploads/files/"
      - "/media/uploads/downloads/"
    url_patterns:
      - "nit.ac.tz/media/uploads/files/*.pdf"
      - "nit.ac.tz/media/uploads/downloads/*.pdf"

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
      Documents at /media/uploads/files/ (hash filenames) and /media/uploads/downloads/. Announcements link directly to PDFs.

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
  twitter: "nit_tanzania"
  instagram: "nit_tanzania1"

notes: |
  The National Institute of Transport (NIT) is a leading higher education institution specializing in logistics, management, and transport technology including aviation and pilot progammes. Accredited by NACTVET, NIT offers diverse programs, including certificates, diplomas, degrees, and specialized training courses.
---

# Home  | National Institute of Transport (NIT)

**Category:** Educational Institution
**Website:** https://nit.ac.tz/
**Tender Page:** https://nit.ac.tz/
**Keywords Found:** procurement

## Contact Information
- Email: rector@nit.ac.tz
- Phone: 026
          
- Phone: 0 11-4 0 2 2 0 
- Phone: 025-2026 
- Phone: 002 0 00-4-5
- Phone: 0 0 0 2 -2

## Scraping Instructions

**Strategy:** Scrape https://nit.ac.tz/ for tender/procurement notices.
**Method:** http_get

The National Institute of Transport (NIT) is a leading higher education institution specializing in logistics, management, and transport technology including aviation and pilot progammes. Accredited by NACTVET, NIT offers diverse programs, including certificates, diplomas, degrees, and specialized training courses.

### Tender Content Preview

> Procurement Management

### Document Links Found

- https://nit.ac.tz/media/uploads/downloads/NIT_PPROSPECTUS_2025_2026_FINAL_DRAFT_.pdf
- https://nit.ac.tz/media/uploads/downloads/NIT-_BOOK_OF_PROCEEDINGS__FOR_THE_3RD_ICTLM.pdf
- https://nit.ac.tz/media/uploads/downloads/JLMES_MANUSRIPT_TEMPLATE.pdf
- https://nit.ac.tz/media/uploads/downloads/FEE_STRUCTURE_FOR_POSTGRADUATE_DIPLOMA_PROGRAMMES_ZvMd5Ij.pdf
- https://nit.ac.tz/media/uploads/files/426f0a2baca7461c9f593b08bf479b42.pdf
- https://nit.ac.tz/media/uploads/downloads/NIT_ADMISSION_GUIDE_BOOK.pdf
- https://nit.ac.tz/media/uploads/downloads/CLIENT_SERVICE_CHATER.pdf
- https://nit.ac.tz/media/uploads/downloads/JANUARY_TO_JUNE_2026_ACTION_PROGRAM__FINAL_REVISED.pdf
- https://nit.ac.tz/media/uploads/downloads/FEE_STRUCTURE_FOR_ORDINARY_DIPLOMA_PROGRAMMES_u6cs44C.pdf
- https://nit.ac.tz/media/uploads/downloads/PROCEEDINGS_2024_-_FINAL.pdf

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

Known document paths: /media/uploads/downloads/JLMES_MANUSRIPT_TEMPLATE.pdf, /media/uploads/downloads/FEE_STRUCTURE_FOR_ORDINARY_DIPLOMA_PROGRAMMES_u6cs44C.pdf, /media/uploads/downloads/CLIENT_SERVICE_CHATER.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
nit/
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
