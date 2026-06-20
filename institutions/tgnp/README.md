---
institution:
  name: "Tanzania Gender Networking Program (TGNP)"
  slug: "tgnp"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tgnp.or.tz"

website:
  homepage: "https://tgnp.or.tz/"
  tender_url: "https://tgnp.or.tz/blog/category/tenders/"

contact:
  email: "info@tgnp.or.tz"
  phone: "0 0 0 0 48"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://tgnp.or.tz/blog/category/tenders/ - WordPress category archive (Astra theme). Each post is a tender. Follow post links for full content and documents."
  selectors:
    container: ".site-content, #content, .ast-archive-description + *"
    tender_item: ".ast-article-post, article.post"
    title: ".entry-title a, .ast-post-title a"
    date: ".entry-meta .posted-on, .ast-post-meta"
    document_link: 'a[href$=".pdf"], a[href*="wp-content/uploads"]'
    pagination: ".ast-pagination, .nav-links, .page-numbers"
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
      - "tgnp.or.tz/wp-content/uploads/*.pdf"

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
      WordPress. Documents in /wp-content/uploads/. Tender posts may link PDFs in content. Example: Comparative-Reach-2024.pdf.

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
  facebook: "tgnptz1"
  twitter: "tgnptz"
  linkedin: "tgnptz"
  instagram: "tgnptz"

notes: |
  Organization website at tgnp.or.tz. Tender keywords detected: tender, tenders.
---

# TGNP &#8211; Tanzania Gender Networking Program

**Category:** NGO / Non-Profit Organization
**Website:** https://tgnp.or.tz/
**Tender Page:** https://tgnp.or.tz/blog/category/tenders/
**Keywords Found:** tender, tenders

## Contact Information
- Email: info@tgnp.or.tz
- Phone: 0 0 0 0 48
- Phone: 0 0 0 48-48
- Phone: 0 0 352 512
- Phone: 0 0 0-48-48
- Phone: 0555555555556

## Scraping Instructions

**Strategy:** Scrape https://tgnp.or.tz/blog/category/tenders/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> Tenders <a href="https://tgnp.or.tz/blog/ca

### Known Tender URLs

- https://tgnp.or.tz/blog/category/tenders/

### Document Links Found

- https://tgnp.or.tz/wp-content/uploads/Comparative-Reach-2024.pdf

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

Known document paths: /wp-content/uploads/Comparative-Reach-2024.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
tgnp/
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

- **Last Checked:** 10 June 2026
- **Active Tenders:** 1 (TGNP-2026-001; category page returns 500 but direct post/PDF accessible)
- **Signal Strength:** Strong (tender, tenders)
