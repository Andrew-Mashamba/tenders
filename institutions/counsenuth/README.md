---
institution:
  name: "COUNSENUTH – Care is our duty"
  slug: "counsenuth"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "counsenuth.or.tz"

website:
  homepage: "https://counsenuth.or.tz/"
  tender_url: "https://counsenuth.or.tz/news/"

contact:
  email: "info@counsenuth.or.tz"
  phone: "0 842 767 846 7"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage and /news/ for tender/procurement notices. WordPress (Bosa/Elementor). Tenders appear in News & Events and Notices sections. Follow article links to detail pages for document PDFs. Also check homepage Advert section for direct PDF links."
  selectors:
    container: "main, #primary, .elementor, .entry-content, .site-main, article"
    tender_item: "article.post, article.hentry, .elementor-post, .widget_recent_entries li, a[href*='invitation-for-bidders'], a[href*='competitive-quotation'], a[href*='expression-of-interest']"
    title: "h2.entry-title, h3.elementor-heading-title, .entry-title a, .catg_title"
    date: ".entry-meta, .posted-on, time"
    document_link: 'a[href$=".pdf"], a[href*="/wp-content/uploads/"]'
    pagination: ".nav-links a, .page-numbers, a.next"
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
      - "counsenuth.or.tz/wp-content/uploads/*/*/*.pdf"

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
      WordPress stores documents under /wp-content/uploads/YYYY/MM/. Procurement adverts and tender PDFs linked from homepage Advert section and /news/ article detail pages. Follow Read More links to extract document URLs from post content.

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
  facebook: "counsenuth"
  instagram: "counsenuth98"

notes: |
  Organization website at counsenuth.or.tz. Tender keywords detected: bid, expression of interest, procurement, quotation, rfi, supply.
---

# COUNSENUTH &#8211; Care is our duty

**Category:** NGO / Non-Profit Organization
**Website:** https://counsenuth.or.tz/
**Tender Page:** https://counsenuth.or.tz/wp-content/uploads/2026/03/COUNSENUTH-Advert-for-2026-Annual-Procurement-Revised-FINAL.pdf
**Keywords Found:** bid, expression of interest, procurement, quotation, rfi, supply

## Contact Information
- Email: info@counsenuth.or.tz
- Phone: 0 842 767 846 7
- Phone: 04 958 771
- Phone: 098438347
- Phone: 0 196 150 212 1
- Phone: +255 766 555 540

## Scraping Instructions

**Strategy:** Scrape https://counsenuth.or.tz/wp-content/uploads/2026/03/COUNSENUTH-Advert-for-2026-Annual-Procurement-Revised-FINAL.pdf for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> <svg aria-hidden="true" class="e-font-icon-svg e-fas-check" viewBox="0 0 512 512" xmlns="http://www.w3.org/2

### Known Tender URLs

- https://counsenuth.or.tz/wp-content/uploads/2026/03/COUNSENUTH-Advert-for-2026-Annual-Procurement-Revised-FINAL.pdf
- https://counsenuth.or.tz/counsenuth-procurement-manual/
- https://counsenuth.or.tz/invitation-for-bidders-to-supply-goods-services-for-financial-year-2026/
- https://counsenuth.or.tz/competitive-quotation-hydro-geophysical-survey-borehole-drilling-in-bahi-kondoa-district-councils/

### Document Links Found

- https://counsenuth.or.tz/wp-content/uploads/2026/03/COUNSENUTH-Advert-for-2026-Annual-Procurement-Revised-FINAL.pdf
- https://counsenuth.or.tz/wp-content/uploads/2026/03/JD-Communication-and-Visibility-Intern-SM-SN-Final-1.pdf

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

Known document paths: /wp-content/uploads/2026/03/JD-Communication-and-Visibility-Intern-SM-SN-Final-1.pdf, /wp-content/uploads/2026/03/COUNSENUTH-Advert-for-2026-Annual-Procurement-Revised-FINAL.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
counsenuth/
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
- **Signal Strength:** Strong (expression of interest, procurement)
