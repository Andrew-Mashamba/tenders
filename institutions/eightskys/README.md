---
institution:
  name: "Eight Sky&#039;s Consulting &#8211; Sky is the Limit"
  slug: "eightskys"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "eightskys.co.tz"

website:
  homepage: "https://eightskys.co.tz/"
  tender_url: "https://eightskys.co.tz/"

contact:
  email: "info@eightskys.co.tz"
  phone: "00692751 15"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Scrape https://eightskys.co.tz/ and blog for tender/procurement. EightSkys Consulting - accounting software. Homepage shows no posts; no dedicated tender page. Monitor blog for EOI/RFI/RFP."
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

    known_document_paths:
      - "/wp-content/uploads/"
    url_patterns:
      - "eightskys.co.tz/wp-content/uploads/*.pdf"

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
      WordPress site. Documents likely in /wp-content/uploads/. No tender content found; blog shows 'no posts'. Monitor for future EOI/RFP announcements.

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
  facebook: "EightSkys"
  linkedin: "eightskys-consulting-limited"
  instagram: "eightskys"

notes: |
  Organization website at eightskys.co.tz. Tender keywords detected: eoi, rfi, rfp, rfq.
---

# Eight Sky&#039;s Consulting &#8211; Sky is the Limit

**Category:** Commercial / Private Sector
**Website:** https://eightskys.co.tz/
**Tender Page:** data:image/png;base64,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
**Keywords Found:** eoi, rfi, rfp, rfq

## Contact Information
- Email: info@eightskys.co.tz
- Phone: 00692751 15
- Phone: 0 000          
- Phone: 000945288
- Phone: 00615009 15
- Phone: +255740007053

## Scraping Instructions

**Strategy:** Scrape data:image/png;base64,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 for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- data:image/png;base64,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
- data:image/png;base64,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

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
eightskys/
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
- **Signal Strength:** Strong (eoi, rfp, rfq)
