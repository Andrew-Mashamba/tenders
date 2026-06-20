---
institution:
  name: "Autofest - Tanzania Motoring Home"
  slug: "autofest"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "autofest.co.tz"

website:
  homepage: "https://autofest.co.tz/"
  tender_url: "https://autofest.co.tz/"

contact:
  email: "booking@autofest.co.tz"
  alternate_emails:
    - "ceo@vision.co.tz"
    - "edirector@autofest.co.tz"
    - "your.address@email.com"
    - "your-email@website.com"
  phone: "+255677300500"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage for exhibitor/vendor opportunities. Event brief PDF at /13TH_ED_Autofest.pdf (current) and legacy /Autofest_2025_Event_Brief.pdf. Exhibitor booking at /exhibitor.html — NOT procurement tenders. Only create records for actual RFPs/RFQs if posted."
  selectors:
    container: "main, .content, section, .welcome-note"
    tender_item: "article, .event-item, .card, a[href$='.pdf']"
    title: "h2, h3, h4, .event-title"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href*="Event_Brief"]'
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
      - "/"
      - "/13TH_ED_Autofest.pdf"

    url_patterns:
      - "autofest.co.tz/Autofest_*.pdf"
      - "autofest.co.tz/13TH_ED_Autofest.pdf"

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
      Event brief PDF at root: /13TH_ED_Autofest.pdf (13th edition, updated Apr 2026). Legacy: /Autofest_2025_Event_Brief.pdf. Exhibitor booking is commercial sales, not institutional procurement.

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
  facebook: "tools"
  twitter: "docs"
  instagram: "autofest_255"

notes: |
  Autofest is the heartbeat of the automotive community, bringing together car enthusiasts, racers, and industry professionals under one vibrant and dynamic platform. As the core business of our operations, Autofest is dedicated to celebrating the passion for motorsport, car culture, and automotive innovation.
---

# Autofest - Tanzania Motoring Home

**Category:** Commercial / Private Sector
**Website:** https://autofest.co.tz/
**Tender Page:** https://autofest.co.tz/
**Keywords Found:** quotation, rfi

## Contact Information
- Email: booking@autofest.co.tz
- Email: ceo@vision.co.tz
- Email: edirector@autofest.co.tz
- Email: your.address@email.com
- Email: your-email@website.com
- Phone: +255677300500
- Phone: +255 677 300 500 
- Phone: 06587944983061
- Phone: 018-10-01

## Scraping Instructions

**Strategy:** Scrape https://autofest.co.tz/ for tender/procurement notices.
**Method:** http_get

Autofest is the heartbeat of the automotive community, bringing together car enthusiasts, racers, and industry professionals under one vibrant and dynamic platform. As the core business of our operations, Autofest is dedicated to celebrating the passion for motorsport, car culture, and automotive innovation.

### Document Links Found

- https://autofest.co.tz/Autofest_2025_Event_Brief.pdf

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
autofest/
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
