---
institution:
  name: "Topshop – Pro Audio and Electronics in Tanzania"
  slug: "topshop"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "topshop.co.tz"

website:
  homepage: "https://topshop.co.tz/"
  tender_url: "https://topshop.co.tz/"

contact:
  email: "info@topshoptz.com"
  phone: "0 842 767 846 7"

scraping:
  enabled: false
  method: "http_get"
  strategy: |
    Pro audio/electronics retailer. Homepage shows product catalog (speakers, guitars, mixers). No tender notices,
    no procurement section. RFI/RFQ keywords found in product context. Disable until institution publishes tenders.
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
      - "topshop.co.tz/*.pdf"

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
      Document storage paths not yet identified. Check tender detail pages for download links.

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
  instagram: "topshop_music"

notes: |
  Organization website at topshop.co.tz. Tender keywords detected: rfi, rfq.
---

# Topshop &#8211; Pro Audio and Electronics in Tanzania

**Category:** Commercial / Private Sector
**Website:** https://topshop.co.tz/
**Tender Page:** https://topshop.co.tz/
**Keywords Found:** rfi, rfq

## Contact Information
- Email: info@topshoptz.com
- Phone: 0 842 767 846 7
- Phone: +255784326341
- Phone: 0 0 352 512
- Phone: 08 454 696 446
- Phone: 09819 100

## Scraping Instructions

**Strategy:** Scrape https://topshop.co.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 for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- https://topshop.co.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

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
topshop/
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
- **Signal Strength:** Strong (rfq)
