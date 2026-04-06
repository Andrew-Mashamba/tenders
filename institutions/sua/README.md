---
institution:
  name: "Sokoine University of Agriculture"
  slug: "sua"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "sua.ac.tz"

website:
  homepage: "https://sua.ac.tz/"
  tender_url: "https://sua.ac.tz/"

contact:
  phone: "007742267"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape sua.ac.tz. Drupal 8 site. Homepage has news (block-views-block-news-block-1), events, useful links. Tenders may be at external site (sites.google.com/site/sualisa2020). Scrape news view for tender-related items; follow document links in Staff/ICT menus. Documents in /sites/default/files/."
  selectors:
    container: "main, #main-content, .region-content, .view-content, .block-views-block-news-block-1"
    tender_item: ".view-id-news .views-row, article, .node--type-news, .views-row"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href*="/sites/default/files/"]'
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
      - "sua.ac.tz/sites/default/files/*"
      - "www.sua.ac.tz/sites/default/files/*"

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
      Documents in /sites/default/files/ (Drupal default). Paths: /sites/default/files/2025-11/, /sites/default/files/2025-12/, /sites/default/files/documents/regulations/, /sites/default/files/documents/manual/. Tender listings may be on external SUA LISA site (sites.google.com).

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
  facebook: "SokoineUniversityOfAgriculture"
  twitter: "sokoineu"
  instagram: "sokoineuniversity"

notes: |
  Sokoine University of Agriculture (SUA) is a public University based in Morogoro Tanzania. The university is located on the slopes of the Uluguru mountains. SUA is  best known for offering courses and programmes widely in a field of Agriculture, Veterinary Science, Forestry, Animal Science, Wildlife Management, Tourism Management, Environmental Science,Food Science, Natural Resources,Nutrition,Rural Development, since its establishment.
---

# Sokoine University of Agriculture

**Category:** Educational Institution
**Website:** https://sua.ac.tz/
**Tender Page:** https://sua.ac.tz/
**Keywords Found:** procurement, rfi, tender, tenders

## Contact Information
- Phone: 007742267
- Phone: 015-09-15-11-2
- Phone: 02024-1-1
- Phone: 025-6317-4565-
- Phone: 05-4969-9288-1

## Scraping Instructions

**Strategy:** Scrape https://sua.ac.tz/ for tender/procurement notices.
**Method:** http_get

Sokoine University of Agriculture (SUA) is a public University based in Morogoro Tanzania. The university is located on the slopes of the Uluguru mountains. SUA is  best known for offering courses and programmes widely in a field of Agriculture, Veterinary Science, Forestry, Animal Science, Wildlife Management, Tourism Management, Environmental Science,Food Science, Natural Resources,Nutrition,Rural Development, since its establishment.

### Tender Content Preview

> cee47b-2fdd-43ce-aa63-4278e48668a8" class="sf-depth-3 sf-no-children"> Tenders &amp; Procurement Services <a href="https://sites.google.com/site/sualisa2020/" cl

### Document Links Found

- https://sua.ac.tz/sites/default/files/documents/regulations/Software-Hardware-Change-Request-Form.pdf
- https://www.sua.ac.tz/sites/default/files/2025-11/SUA%20INVESTMENT%20POLICY%20AND%20GUIDELINES.pdf
- https://sua.ac.tz/sites/default/files/documents/regulations/ICT-Service-Request-Form.pdf
- https://sua.ac.tz/sites/default/files/JARIDA%20LA%20MATUKIO%20YA%20SUA%20-%20JANUARI%20HADI%20MACHI%2C%202024.pdf
- https://sua.ac.tz/sites/default/files/MATUKIO%20YA%20SUA%20APRILI%20HADI%20JUNI%2C%202025_FINAL.pdf
- https://sua.ac.tz/sites/default/files/JARIDA%20LA%20MATUKIO%20YA%20SUA%20OKTOBA%20HADI%20DESEMBA%2C%202023.pdf
- https://sua.ac.tz/sites/default/files/HEET%20NEWSLETTER%2C%202025.pdf
- https://sua.ac.tz/sites/default/files/JARIDA%20LA%20MATUKIO%20YA%20SUA%20JANUARI%20HADI%20MACHI%2C%202025-final.pdf
- https://sua.ac.tz/sites/default/files/RAMANI%20HALISI%20YA%20TANZANIA_.pdf
- https://www.sua.ac.tz/sites/default/files/documents/manual/EDMS-User-Guide.pdf

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

Known document paths: /files/SUA%20CLIENTS%20SERVICE%20Book%20A5%20Pg%2052%2024%20Aug%202024.pdf, /files/2025-12/SUA%20Almanac%20for%20the%202025-26%20Academic%20year.pdf, /files/documents/regulations/ICT-Service-Request-Form.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
sua/
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
- **Signal Strength:** Strong (procurement, tender, tenders)
