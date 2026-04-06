---
institution:
  name: "Creditinfo Tanzania"
  slug: "creditinfo"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "creditinfo.co.tz"

website:
  homepage: "https://creditinfo.co.tz/"
  tender_url: "https://creditinfo.co.tz/"

contact:
  email: "logoBSI@2x.png"
  alternate_emails:
    - "citinfo@creditinfo.co.tz"
    - "BGorgranicwaves_grey@2x.jpg"
    - "icoLocation@2x.png"
    - "icoPhone@2x.png"
  phone: "0015824 5"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Homepage only. No dedicated tender page. 'Tender' appears only in case study text (CIASA credit registry). Creditinfo is a credit bureau; they do not publish procurement tenders."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
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

    url_patterns:
      - "creditinfo.co.tz/*.pdf"

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
      No tender documents. Site is a credit bureau; no procurement/tender listings found.

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
  facebook: "CreditinfoTanzania"
  linkedin: "creditinfo-tanzania-limited"

notes: |
  Creditinfo is a leading service provider for credit information and risk management solutions worldwide. It has established more than 25 credit bureaus in mature and emerging markets over 4 continents.
---

# Creditinfo | We Facilitate Access to Finance

**Category:** Commercial / Private Sector
**Website:** https://creditinfo.co.tz/
**Tender Page:** https://creditinfo.co.tz/
**Keywords Found:** tender

## Contact Information
- Email: logoBSI@2x.png
- Email: citinfo@creditinfo.co.tz
- Email: BGorgranicwaves_grey@2x.jpg
- Email: icoLocation@2x.png
- Email: icoPhone@2x.png
- Phone: 0015824 5
- Phone: 022377 0 
- Phone: 00588488 15
- Phone: 055266 19
- Phone: 0666666 1

## Scraping Instructions

**Strategy:** Scrape https://creditinfo.co.tz/ for tender/procurement notices.
**Method:** http_get

Creditinfo is a leading service provider for credit information and risk management solutions worldwide. It has established more than 25 credit bureaus in mature and emerging markets over 4 continents.

### Tender Content Preview

> he control of the Central Bank of Sudan. After the data had built up the over a period of 4 years a tender of leading International providers was made to select a company for developed of a credit bureau credit score model. <a href="https://creditinfo.co.tz/case-studies/ciasa-cre

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
creditinfo/
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
