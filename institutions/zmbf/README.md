---
institution:
  name: "Zanzibar Maisha Bora Foundation (ZMBF)"
  slug: "zmbf"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "zmbf.or.tz"

website:
  homepage: "https://zmbf.or.tz/"
  tender_url: "https://zmbf.or.tz/"

contact:
  phone: "023-12-06-"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://zmbf.or.tz/ — WordPress site. Tender-like content (Call for Consultancy, RFPs) in News & Insights section. Follow links to article pages (e.g. /call-for-consultancy-*). Each article has title, deadline, and document link. Documents in /wp-content/uploads/YYYY/MM/."
  selectors:
    container: "main, .wp-block-post-template, .wp-block-query-loop, .entry-content"
    tender_item: "article.wp-block-post, .wp-block-post, .wp-block-group, a[href*='call-for-consultancy'], a[href*='tender']"
    title: "h2.wp-block-post-title, h1.entry-title, .wp-block-heading"
    date: ".wp-block-post-date, .entry-date, time"
    document_link: 'a[href$=".pdf"], a[href*="/wp-content/uploads/"], a[href*="download"]'
    pagination: ".wp-block-query-pagination, .nav-links a"
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
      - "zmbf.or.tz/wp-content/uploads/*/*.pdf"
      - "zmbf.or.tz/*.pdf"

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
      ZMBF posts consultancy/RFP notices as news articles. Example: call-for-consultancy-srhr-advocacy-capacity-building with TOR PDF at /wp-content/uploads/2025/11/UNFPA-CALL-FOR-CONSULTANCY-SRH-2.pdf. Follow 'Read More' to article pages for full details and document links.

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
  facebook: "maishaborafdn"
  linkedin: "maishaborafdn"
  instagram: "maishaborafdn"

notes: |
  Organization website at zmbf.or.tz. Tender keywords detected: rfi, tender.
---

# ZANZIBAR MAISHA BORA FOUNDATION &#8211; Quality Life to all Zanzibaris

**Category:** NGO / Non-Profit Organization
**Website:** https://zmbf.or.tz/
**Tender Page:** https://zmbf.or.tz/
**Keywords Found:** rfi, tender

## Contact Information
- Phone: 023-12-06-
- Phone: 023-10-25-
- Phone: 026-03-13 18
- Phone: +255 24 223 0909
- Phone: 02561769368

## Scraping Instructions

**Strategy:** Scrape https://zmbf.or.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ng="async" width="630" height="354" src="https://zmbf.or.tz/wp-content/uploads/2025/11/invation-for-tender-NFPA-2.png" class="attachment-medilink-size3 size-medilink-size3 wp-post-image" alt="" />

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
zmbf/
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
