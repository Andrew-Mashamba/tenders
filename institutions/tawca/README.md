---
institution:
  name: "TAWCA"
  slug: "tawca"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "tawca.or.tz"

website:
  homepage: "https://tawca.netlify.app/"
  tender_url: "https://tawca.netlify.app/Opportunities/Tenders/"

contact:
  email: "info@tawca.or.tz"
  phone: "06 0 0 1-3 0"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Next.js SPA on Netlify. Tender page at /Opportunities/Tenders/. Content is client-rendered - requires JS. When tenders exist, parse main content area. Currently shows 'No Tenders Available'."
  selectors:
    container: "main, .w-full.max-w-6xl.mx-auto, [class*='max-w-6xl']"
    tender_item: "article, .tender-item, .card, [class*='tender'], div[class*='rounded']"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a, button[class*='next']" 
  schedule: "daily"

  anti_bot:
    requires_javascript: true
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
      - "tawca.or.tz/*.pdf"

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
      Next.js/Netlify SPA. Documents may be hosted on Netlify or external. When tenders exist, follow document links from tender cards. No static document path pattern yet.

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
  facebook: "TawcaTawca"
  twitter: "TAWCA_Tanzania"
  linkedin: "tanzania-association-of-women-certified-accountants-tawca"
  instagram: "tawca"

notes: |
  Organization website at tawca.or.tz. Tender keywords detected: tender, tenders.
---

# TAWCA

**Category:** NGO / Non-Profit Organization
**Website:** https://tawca.netlify.app/
**Tender Page:** https://tawca.netlify.app/Opportunities/Tenders/
**Keywords Found:** tender, tenders

## Contact Information
- Email: info@tawca.or.tz
- Phone: 06 0 0 1-3 0
- Phone: 046 4 19 4
- Phone: 0 1 1 6 0 3 3 0
- Phone: +255 696 455 015
- Phone: 0 0 1 12 13

## Scraping Instructions

**Strategy:** Scrape https://tawca.netlify.app/Opportunities/Tenders/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ss="block px-4 py-2 text-sm text-gray-700 hover:bg-[#074EA3] hover:text-white" href="/Opportunities/Tenders/">Tenders Job Vacancies <div class=

### Known Tender URLs

- https://tawca.netlify.app/Opportunities/Tenders/

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
tawca/
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
