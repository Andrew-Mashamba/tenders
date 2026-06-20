---
institution:
  name: "Taifa Mining (Taifa - Civil and Mining Sector)"
  slug: "caspian"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "caspian.co.tz"

website:
  homepage: "https://taifamining.co.tz/"
  tender_url: "https://taifamining.co.tz/"

contact:
  email: "bd@taifamining.co.tz"
  alternate_emails:
    - "procurement@taifamining.co.tz"
    - "jobs@taifamining.co.tz"
    - "%20procurement@taifamining.co.tz"
  phone: "0 842 767 846 7"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape taifamining.co.tz for tender/procurement notices. WordPress/Elementor. Homepage PDFs are compliance certificates; check /news-articles/ or contact procurement@taifamining.co.tz for tender postings."
  selectors:
    container: "main, .elementor, .content-area, .ast-container, article"
    tender_item: "article, .elementor-post, .tender-item, .card, .row, li, tr"
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
      - "taifamining.co.tz/wp-content/uploads/*/*/*.pdf"
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
      Documents under /wp-content/uploads/YYYY/MM/. Homepage PDFs are compliance certs (ISO, WCF, Health & Safety). Tender documents may be posted in News or via procurement email.

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

notes: |
  Organization website at caspian.co.tz. Tender keywords detected: procurement, supply.
---

# Taifa - Civil and Mining Sector

**Category:** Commercial / Private Sector
**Website:** https://taifamining.co.tz/
**Tender Page:** https://taifamining.co.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Email: bd@taifamining.co.tz
- Email: procurement@taifamining.co.tz
- Email: jobs@taifamining.co.tz
- Email: %20procurement@taifamining.co.tz
- Phone: 0 842 767 846 7
- Phone: 00 408 258 167
- Phone: 04 958 771
- Phone: 08 500 167 742
- Phone: 0 196 150 212 1

## Scraping Instructions

**Strategy:** Scrape https://taifamining.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> <svg aria-hidden="true" class="e-font-icon-svg e-far-envelope" viewBox="0 0 512 512" xmlns="http://www.w3.or

### Document Links Found

- https://taifamining.co.tz/wp-content/uploads/2025/03/taifa-mining-civils-limited-iso9001-certificate.pdf
- https://taifamining.co.tz/wp-content/uploads/2025/03/taifa-mining-health-and-safety-certificate.pdf
- https://taifamining.co.tz/wp-content/uploads/2025/03/taifa-mining-wcf-certificate-of-registration.pdf

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

Known document paths: /wp-content/uploads/2025/03/taifa-mining-wcf-certificate-of-registration.pdf, /wp-content/uploads/2025/03/taifa-mining-civils-limited-iso9001-certificate.pdf, /wp-content/uploads/2025/03/taifa-mining-health-and-safety-certificate.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
caspian/
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
- **Active Tenders:** 0 (homepage has compliance certificates only; no tender postings)
- **Signal Strength:** Weak (procurement contact exists but no public tenders)
