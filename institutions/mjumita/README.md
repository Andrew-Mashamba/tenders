---
institution:
  name: "Mjumita &#8211; Tanzania&#039;s Community Forest Network"
  slug: "mjumita"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "mjumita.or.tz"

website:
  homepage: "https://mjumita.or.tz/"
  tender_url: "https://mjumita.or.tz/latest/"

contact:
  email: "info@mjumita.or.tz"
  phone: "08-5278-1 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://mjumita.or.tz/latest/ for opportunities (ToR, consultancy calls). Filter for 'Opportunity' category. Each item has title, date, category, and Read more link. Documents under /wp-content/uploads/."
  selectors:
    container: ".bde-loop, .content, main, .entry-content"
    tender_item: ".bde-loop-item, .ee-loop-item, article"
    title: ".ee-post-title, h3, h4, .bde-post-title"
    date: ".ee-post-meta-date, .date, time, .post-meta"
    document_link: 'a[href$=".pdf"], a[href*="/wp-content/uploads/"], a[href$=".doc"], a[href$=".docx"], a[download]'
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
      - "mjumita.or.tz/wp-content/uploads/2025/09/MJUMITA-Strategy-2025-2029-compressed.pdf"

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

    known_document_paths:
      - "/wp-content/uploads/"
    document_notes: |
      Mjumita WordPress site. Documents under /wp-content/uploads/{year}/{month}/. Filter items by 'Opportunity' category for tenders/ToR. Read more links lead to detail pages with PDF attachments.

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
  facebook: "MJUMITA"
  linkedin: "mjumita-linkledin-tz"
  instagram: "mjumita1"

notes: |
  Organization website at mjumita.or.tz. Tender keywords detected: procurement.
---

# Mjumita &#8211; Tanzania&#039;s Community Forest Network

**Category:** NGO / Non-Profit Organization
**Website:** https://mjumita.or.tz/
**Tender Page:** https://mjumita.or.tz/2025/09/16/tor-development-of-standard-operating-procedures-sops-for-procurement-sexual-harassment-and-updating-the-human-resources-hr-manual-for-mjumita/
**Keywords Found:** procurement

## Contact Information
- Email: info@mjumita.or.tz
- Phone: 08-5278-1 
- Phone: 00-5312-1 
- Phone: 025-2029-
- Phone: 04-5278-1 
- Phone: 07-5278-1 

## Scraping Instructions

**Strategy:** Scrape https://mjumita.or.tz/2025/09/16/tor-development-of-standard-operating-procedures-sops-for-procurement-sexual-harassment-and-updating-the-human-resources-hr-manual-for-mjumita/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> " href="https://mjumita.or.tz/2025/09/16/tor-development-of-standard-operating-procedures-sops-for-procurement-sexual-harassment-and-updating-the-human-resources-hr-manual-for-mjumita/" aria-label="ToR: Development of Standard Operating Procedures (SOPs) for Procurement, Sexual Harassment, and upda

### Known Tender URLs

- https://mjumita.or.tz/2025/09/16/tor-development-of-standard-operating-procedures-sops-for-procurement-sexual-harassment-and-updating-the-human-resources-hr-manual-for-mjumita/

### Document Links Found

- https://mjumita.or.tz/wp-content/uploads/2025/09/MJUMITA-Strategy-2025-2029-compressed.pdf

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

Known document paths: /wp-content/uploads/2025/09/MJUMITA-Strategy-2025-2029-compressed.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
mjumita/
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
