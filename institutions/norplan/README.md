---
institution:
  name: "NORPLAN"
  slug: "norplan"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "norplan.co.tz"

website:
  homepage: "https://norplan.co.tz/"
  tender_url: "https://norplan.co.tz/projects/"

contact:
  email: "admin@norplan.co.tz"
  phone: "015572177880"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Engineering consultancy firm. Portfolio/project pages at /portfolio/ and /projects/ showcase completed work (case studies), not open procurement. No tender listings or downloadable RFPs on site as of 2026-06-11. Monitor homepage and projects page for new procurement notices."
  selectors:
    container: ".themetechmount-portfolio-details, .portfolio-description, #main, .main-holder .site-content"
    tender_item: "article.tm_portfolio, .single-tm_portfolio .portfolio-description"
    title: ".tm-titlebar h1.entry-title, .portfolio-description h2, .themetechmount-portfolio-details h2"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="wp-content/uploads"], a[download]'
    pagination: ".themetechmount-pagination .page-numbers, .nav-links a" 
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
        - 'a[href*="/wp-content/uploads/"]'
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
      - "norplan.co.tz/wp-content/uploads/*.pdf"
      - "norplan.co.tz/*.pdf"

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
      WordPress site. Documents in /wp-content/uploads/. Uses embed-pdf-viewer plugin. Single portfolio project pages contain project details and linked documents.

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
  twitter: "norplantz"
  linkedin: "norplan-tanzania-limited-a26a5622a"
  instagram: "norplantanzanialimited"

notes: |
  Organization website at norplan.co.tz. Tender keywords detected: supply, tender.
---

# NORPLAN

**Category:** Commercial / Private Sector
**Website:** https://norplan.co.tz/
**Tender Page:** https://norplan.co.tz/portfolio/consultancy-services-for-feasibility-studies-environmental-social-impact-assessment-detailed-engineering-design-and-preparation-of-tender-documents-for-upgrading-of-msangama-namanyere/
**Keywords Found:** supply, tender

## Contact Information
- Email: admin@norplan.co.tz
- Phone: 015572177880
- Phone: 0742424155
- Phone: +255 222 780 183
- Phone: +255 222 780 742
- Phone: +255222780183

## Scraping Instructions

**Strategy:** Scrape https://norplan.co.tz/portfolio/consultancy-services-for-feasibility-studies-environmental-social-impact-assessment-detailed-engineering-design-and-preparation-of-tender-documents-for-upgrading-of-msangama-namanyere/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> dies, Environmental &#038; Social Impact Assessment, Detailed Engineering Design and Preparation of Tender Documents for Upgrading of Msangama &#8211; Namanyere – Katongoro – New Kipili Port (62km) To Bitumen Standard in Rukwa Region." href="https://norplan.co.tz/wp-content/uploads/2024/04/r8.04.jpg

### Known Tender URLs

- https://norplan.co.tz/portfolio/consultancy-services-for-feasibility-studies-environmental-social-impact-assessment-detailed-engineering-design-and-preparation-of-tender-documents-for-upgrading-of-msangama-namanyere/

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
norplan/
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

- **Last Checked:** 11 June 2026
- **Active Tenders:** 0 (portfolio pages are completed projects, not open tenders)
- **Signal Strength:** Strong (tender)
