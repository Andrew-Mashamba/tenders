---
institution:
  name: "TotalEnergies Marketing Tanzania Limited"
  slug: "totalenergies"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "totalenergies.co.tz"

website:
  homepage: "https://totalenergies.co.tz/"
  tender_url: "https://totalenergies.co.tz/"

contact:
  phone: "093 0 0 1 2"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage for tender/EOI notices. Look for 'Expression of Interest' and news items in NEWS & EVENTS section. Follow detail page links for full documents. Drupal site."
  selectors:
    container: "main, #main-content, .view-content, .layout-container"
    tender_item: "article, .views-row, .node--type-article"
    title: "h2, h3, h4, .title_22, a.button, .field--name-title"
    date: ".date, .field--name-created, time, .views-field-created"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a, .pager__item"
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
      - "totalenergies.co.tz/*.pdf"
      - "totalenergies.co.tz/*.doc"
      - "totalenergies.co.tz/*.docx"

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
      Tenders appear in NEWS & EVENTS section and homepage carousel. Expression of Interest links go to detail pages. Check tender detail pages for download links. Documents may be in /sites/g/files/ or similar Drupal paths.

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
  facebook: "TotalEnergiesTanzania"
  instagram: "totalenergies_tz"

notes: |
  Welcome to the number one energies company in Tanzania and globally integrated that produces and markets oil, bio-fuels, natural gas, green gases, renewables an
---

# Home Tanzania | TotalEnergies Marketing Tanzania Limited

**Category:** Commercial / Private Sector
**Website:** https://totalenergies.co.tz/
**Tender Page:** https://totalenergies.co.tz/
**Keywords Found:** expression of interest

## Contact Information
- Phone: 093 0 0 1 2
- Phone: 0 0 1 5 19
- Phone: 003 0 1 1 0-6
- Phone: 003 0 0 1 0 6
- Phone: 093 0 1 1-2

## Scraping Instructions

**Strategy:** Scrape https://totalenergies.co.tz/ for tender/procurement notices.
**Method:** http_get

Welcome to the number one energies company in Tanzania and globally integrated that produces and markets oil, bio-fuels, natural gas, green gases, renewables an

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
totalenergies/
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
- **Signal Strength:** Strong (expression of interest)
