---
institution:
  name: "TAWLA - Tanzania Women Lawyers Association"
  slug: "tawla"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tawla.or.tz"

website:
  homepage: "https://www.tawla.or.tz/"
  tender_url: "https://www.tawla.or.tz/"

contact:
  phone: "024-11-02-"

scraping:
  enabled: true
  method: "http_get"
  strategy: "WordPress (WPBakery). TOR/RFI opportunities on homepage and tawla-recent-news. Parse posts with Terms of Reference. Documents via fivo_docs shortcode - follow 'Read more' to detail pages. Also check /tawla-recent-news/."
  selectors:
    container: ".wrapper-page, .vc_column_container, .content-inner, .vc_custom_1535689861668"
    tender_item: ".widget, .post, article, .vc_row"
    title: "h3, h4, h5, .widget .info h3, a[href*='terms-of-reference'], a[href*='tor']"
    date: ".date, .closing-date, .published, time, .entry-meta"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/wp-content/uploads/"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a, .page-numbers a"
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
      - "tawla.or.tz/wp-content/uploads/*.pdf"
      - "tawla.or.tz/wp-content/uploads/*.doc"
      - "tawla.or.tz/wp-content/uploads/*.docx"

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
      WordPress. Documents in /wp-content/uploads/. TOR/RFI use fivo_docs shortcode - follow 'Read more' links to get document IDs. PDF embedder may wrap docs.

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
  facebook: "dialog"
  twitter: "TawlaTZ"
  linkedin: "tawla-tanzania-76875282"
  instagram: "TawlaTZ"

notes: |
  We are dedicated to the ideal of lifelong learning for women through the advocacy of civil rights, social justice, transparency, integrity, respect, gender equity, good governance and accountability
---

# Home - TAWLA | Tanzania Women Lawyers Association

**Category:** NGO / Non-Profit Organization
**Website:** https://www.tawla.or.tz/
**Tender Page:** https://www.tawla.or.tz/
**Keywords Found:** rfi

## Contact Information
- Phone: 024-11-02-
- Phone: 025-12-18
- Phone: 08479557110079
- Phone: 000153037
- Phone: +255 719 481 794

## Scraping Instructions

**Strategy:** Scrape https://www.tawla.or.tz/ for tender/procurement notices.
**Method:** http_get

We are dedicated to the ideal of lifelong learning for women through the advocacy of civil rights, social justice, transparency, integrity, respect, gender equity, good governance and accountability

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
tawla/
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
