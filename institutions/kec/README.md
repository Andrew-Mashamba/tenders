---
institution:
  name: "Shirika La Elimu Kibaha (KEC)"
  slug: "kec"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "kec.or.tz"

website:
  homepage: "https://kec.or.tz/"
  tender_url: "https://kec.or.tz/"

contact:
  email: "kec@kec.or.tz"
  phone: "0232402142"

scraping:
  enabled: true
  method: "http_get"
  strategy: "KEC uses ega.gov-style CMS. No dedicated tender page in main menu. Check /publications/, /press-releases/, and procurement unit page. Menu: Machapisho (publications), Kituo cha habari (news). Tenders may be under procurement unit or press releases."
  selectors:
    container: ".container, .main-container, .rich-text, .ega-section"
    tender_item: ".list-item, .drop-item, .pr-1.py-2, article"
    title: "h2, h3, h4, .tender-title, .title, a"
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
      - "kec.or.tz/*.pdf"

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
      Documents may be under /uploads/. Check publications and press release pages for PDF links. Site structure similar to kekopharma (ega.gov CMS).

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
  instagram: "kec_tanzania"

notes: |
  SHIRIKA LA ELIMU KIBAHA |     Shirika La Elimu Kibaha - Mwanzo
---

# KEC |     Shirika La Elimu Kibaha - Mwanzo

**Category:** NGO / Non-Profit Organization
**Website:** https://kec.or.tz/
**Tender Page:** https://kec.or.tz/
**Keywords Found:** bid, procurement

## Contact Information
- Email: kec@kec.or.tz
- Phone: 0232402142
- Phone: 0 25 0 0 43
- Phone: 0930548356865
- Phone: 0232402324
- Phone: 0 0 25 0 75 43

## Scraping Instructions

**Strategy:** Scrape https://kec.or.tz/ for tender/procurement notices.
**Method:** http_get

SHIRIKA LA ELIMU KIBAHA |     Shirika La Elimu Kibaha - Mwanzo

### Tender Content Preview

> unit'>Kitengo Cha Miliki na Majengo Kitengo Cha Mipango Ufuatiliaji na Tathmini <a class='drop-item' href= 'https://kec.or.tz/pages/the-functions-of-the-public-relations-communicati

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
kec/
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
