---
institution:
  name: "Udzungwa Mountains College"
  slug: "udzungwamountainscollege"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "udzungwamountainscollege.ac.tz"

website:
  homepage: "https://udzungwamountainscollege.ac.tz/"
  tender_url: "https://udzungwamountainscollege.ac.tz/"

contact:
  email: "trust@udzungwamountainscollege.ac.tz"
  phone: "0003051757812"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Educational institution - no tender/procurement page. Site has course prospectuses (Prospectus menu) in /wp-content/uploads/2020/01/; NOT a tender site. Disabled until dedicated tender page exists."
  selectors:
    container: "#main-content, .entry-content, .sub-menu"
    tender_item: "article, .tender-item, .sub-menu li"
    title: "h2, h3, h4, .tender-title, a.tc-menu-inner"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href*="/wp-content/uploads/"]'
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
      - "/wp-content/uploads/2020/01/"

    url_patterns:
      - "udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/*.pdf"
      - "udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-ACCOUNTING-FINANCE.pdf"
      - "udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/Hospitality-Management-Prospectus.pdf"
      - "udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-STORE-MANAGEMENT.pdf"
      - "udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-SALES-MANAGEMENT.pdf"

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
      Known document paths: /wp-content/uploads/2020/01/ (Prospectus PDFs in menu). NOT tenders - these are course prospectuses. Scraping disabled until tender page exists.

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
  facebook: "domestictourismsafaristz"

notes: |
  Organization website at udzungwamountainscollege.ac.tz. Tender keywords detected: rfi, tender.
---

# Udzungwa Mountains  College &#8211; Udzungwa Mountains  College

**Category:** Educational Institution
**Website:** https://udzungwamountainscollege.ac.tz/
**Tender Page:** https://udzungwamountainscollege.ac.tz/wp-content/plugins/yikes-inc-easy-mailchimp-extender/public/css/yikes-inc-easy-mailchimp-extender-public.min.css
**Keywords Found:** rfi, tender

## Contact Information
- Email: trust@udzungwamountainscollege.ac.tz
- Phone: 0003051757812
- Phone: 0400231231
- Phone: 026-03-13 15
- Phone: 02813876688
- Phone: +255 762 988 420

## Scraping Instructions

**Strategy:** Scrape https://udzungwamountainscollege.ac.tz/wp-content/plugins/yikes-inc-easy-mailchimp-extender/public/css/yikes-inc-easy-mailchimp-extender-public.min.css for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> erated by Easy Forms for Mailchimp v6.9.0 (https://wordpress.org/plugins/yikes-inc-easy-mailchimp-extender/) --> <div class="wpb_column vc_column_container vc_col-sm-12 bp-back

### Known Tender URLs

- https://udzungwamountainscollege.ac.tz/wp-content/plugins/yikes-inc-easy-mailchimp-extender/public/css/yikes-inc-easy-mailchimp-extender-public.min.css

### Document Links Found

- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-HUMAN-RESOURCE-MANAGEMENT.pdf
- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-STORE-MANAGEMENT.pdf
- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/TOUR-GUIDING-PROSPECTUS-1.pdf
- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/Travel-Courses-Prospectus-2.pdf
- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/Hospitality-Management-Prospectus.pdf
- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-ACCOUNTING-FINANCE.pdf
- https://udzungwamountainscollege.ac.tz/wp-content/uploads/2020/01/PROSPECTUS-SALES-MANAGEMENT.pdf

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

Known document paths: /wp-content/uploads/2020/01/TOUR-GUIDING-PROSPECTUS-1.pdf, /wp-content/uploads/2020/01/PROSPECTUS-ACCOUNTING-FINANCE.pdf, /wp-content/uploads/2020/01/Hospitality-Management-Prospectus.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
udzungwamountainscollege/
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
- **Signal Strength:** Strong (tender)
