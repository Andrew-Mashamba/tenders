---
institution:
  name: "Afyaplus Organization"
  slug: "afyaplustz"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "afyaplustz.or.tz"

website:
  homepage: "https://afyaplustz.or.tz/"
  tender_url: "https://afyaplustz.or.tz/reports.html"

contact:
  email: "info@afyaplustz.or.tz"
  phone: "+255 759 505 309"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape reports.html for Reports & Resources. Static HTML with Bootstrap. Documents in /assets/pdf/. Each report has title, size, date, and Download link. Use Load More for pagination (24 docs total)."
  selectors:
    container: ".reports-section, main, .container"
    tender_item: ".report-card, .report-item, .col-xl-4, [class*='report']"
    title: "h3, h4, .report-title, a[href$='.pdf']"
    date: ".report-date, .meta-box .style2, small"
    document_link: 'a[href$=".pdf"], a[href*="/assets/pdf/"]'
    pagination: "button[class*='load'], .load-more, a[href*='page']"
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
      - "/assets/pdf/"
    url_patterns:
      - "afyaplustz.or.tz/assets/pdf/*.pdf"

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
      Reports stored at /assets/pdf/ (e.g. AFYAPLUS-QUARTER-ONE-REPORT-2025.pdf). Reports page at /reports.html. Quarterly reports, annual reports, financial statements. Load More shows 8 of 24 initially.

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
  facebook: "afyaplustanzania"
  linkedin: "afyaplustanzania"
  instagram: "afyaplustanzania"

notes: |
  Afyaplus is a Tanzanian NGO focus is on promoting clean water, good hygiene, proper nutrition and strong communities. We empower adolescent girls and young women by engaging with
---

# Afyaplus Organization

**Category:** NGO / Non-Profit Organization
**Website:** https://afyaplustz.or.tz/
**Tender Page:** https://afyaplustz.or.tz/
**Keywords Found:** eoi, supply

## Contact Information
- Email: info@afyaplustz.or.tz
- Phone: +255 759 505 309

## Scraping Instructions

**Strategy:** Scrape https://afyaplustz.or.tz/ for tender/procurement notices.
**Method:** http_get

Afyaplus is a Tanzanian NGO focus is on promoting clean water, good hygiene, proper nutrition and strong communities. We empower adolescent girls and young women by engaging with

### Document Links Found

- https://afyaplustz.or.tz/assets/pdf/AFYAPLUS-QUARTER-ONE-REPORT-2025.pdf
- https://afyaplustz.or.tz/assets/pdf/AFYAPLUS QUARTER TWO II REPORT 2025.pdf
- https://afyaplustz.or.tz/assets/pdf/AFYAPLUS QUARTER THREE REPORT 2025.pdf

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
afyaplustz/
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
- **Signal Strength:** Strong (eoi)
