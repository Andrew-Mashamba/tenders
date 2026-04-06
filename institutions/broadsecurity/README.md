---
institution:
  name: "Broad Security Technologies"
  slug: "broadsecurity"
  category: "Commercial / Private Sector"
  status: "inactive"
  country: "Tanzania"
  domain: "broadsecurity.co.tz"

website:
  homepage: "http://broadsecurity.co.tz/"
  tender_url: "http://broadsecurity.co.tz/tenders"

contact:
  email: "user@email.com"
  alternate_emails:
    - "info@broadsecurity.co.tz"
  phone: "07
           "

scraping:
  enabled: false
  method: "http_get"
  strategy: "DISABLED: /tenders returns 404 Page Not Found. No scrapable tender content. Re-enable when tender page is restored."
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
      - "broadsecurity.co.tz/*.pdf"

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
  instagram: "broadsecuritytechnologies"

notes: |
  Organization website at broadsecurity.co.tz. Tender keywords detected: tender, tenders.
---

# 404 - Broad Security Technologies

**Category:** Commercial / Private Sector
**Website:** http://broadsecurity.co.tz/
**Tender Page:** https://api.whatsapp.com/send?phone=9000775857&text=Check%20out%20this%20link:%20http%3A%2F%2Fbroadsecurity.co.tz%2Ftenders
**Keywords Found:** tender, tenders

## Contact Information
- Email: user@email.com
- Email: info@broadsecurity.co.tz
- Phone: 07
           
- Phone: 0 1 0 0 512
- Phone: 08
           
- Phone: +255 673 221 933 
- Phone: +255 754 059 801

## Scraping Instructions

**Strategy:** Scrape https://api.whatsapp.com/send?phone=9000775857&text=Check%20out%20this%20link:%20http%3A%2F%2Fbroadsecurity.co.tz%2Ftenders for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> sapp.com/send?phone=9000775857&text=Check%20out%20this%20link:%20http%3A%2F%2Fbroadsecurity.co.tz%2Ftenders" target="_blank"> -->

### Known Tender URLs

- https://api.whatsapp.com/send?phone=9000775857&text=Check%20out%20this%20link:%20http%3A%2F%2Fbroadsecurity.co.tz%2Ftenders
- https://wa.me/+255673221933/?text=Check%20out%20this%20URL:http%3A%2F%2Fbroadsecurity.co.tz%2Ftenders

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
broadsecurity/
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
- **Signal Strength:** Strong (tender, tenders)
