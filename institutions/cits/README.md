---
institution:
  name: "Flex Corporate Services Limited"
  slug: "cits"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "cits.co.tz"

website:
  homepage: "https://www.flex.co.tz/"
  tender_url: "https://www.flex.co.tz/"

contact:
  email: "frontdesk@flex.co.tz"
  phone: "0 842 767 846 7"

scraping:
  enabled: false
  method: "http_get"
  strategy: |
    Homepage is a marketing site for Flex ERP/Contact Center. No dedicated tender or procurement listing page found.
    Page uses Elementor (WordPress). If tenders are added later, look for .elementor-widget-wrap, .elementor-element.
  selectors:
    container: ".elementor, main, .elementor-widget-wrap"
    tender_item: ".elementor-element, article"
    title: "h2, h3, .elementor-heading-title"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next"
  schedule: "daily"

  anti_bot:
    requires_javascript: false
    has_captcha: false
    rate_limit_seconds: 10

  documents:
    download_enabled: false
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
      - "cits.co.tz/*.pdf"

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
      No tender page or document listing found. Site is marketing-only (ERP, Contact Center). Document paths unknown.

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
  facebook: "frontdesk.cits.3"
  linkedin: "flex-corporate-services"
  instagram: "flex_tanzania"

notes: |
  Born, tested, and proven in Africa, Flex delivers cutting-edge technology solutions that drive business growth, enhance customer engagement, and power digital
---

# Flex Corporate Services Limited | AI-Powered Contact Center, Fléx ERP &amp; Payment Gateway

**Category:** Commercial / Private Sector
**Website:** https://www.flex.co.tz/
**Tender Page:** https://www.flex.co.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Email: frontdesk@flex.co.tz
- Phone: 0 842 767 846 7
- Phone: 0 0 0 0 48
- Phone: 00 408 258 167
- Phone: 04 958 771
- Phone: 0 196 150 212 1

## Scraping Instructions

**Strategy:** Scrape https://www.flex.co.tz/ for tender/procurement notices.
**Method:** http_get

Born, tested, and proven in Africa, Flex delivers cutting-edge technology solutions that drive business growth, enhance customer engagement, and power digital

### Tender Content Preview

> t-container"> Smart Inventory &amp; Procurement Management <div class="elementor-element elementor-element-5c37aaf elementor-widget-tablet__width-inherit elementor-widget-mobile__width-inherit elementor-wid

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
cits/
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
