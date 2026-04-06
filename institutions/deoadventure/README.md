---
institution:
  name: "Deoadventure"
  slug: "deoadventure"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "deoadventure.co.tz"

website:
  homepage: "https://www.deoadventure.co.tz/"
  tender_url: "https://www.deoadventure.co.tz/"

contact:
  email: "adventure@deoadventure.co.tz"
  phone: "+255 622 825 826
"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Deoadventure is a safari/tourism company (Spanish-language site). Homepage shows safari packages, Kilimanjaro tours, testimonials. No dedicated tender/procurement section found. Check for RFI/tender notices in blog, news, or contact pages. Keyword 'tender' may appear in testimonials only."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
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

    url_patterns:
      - "deoadventure.co.tz/*.pdf"

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
      No tender document paths identified. Site is primarily safari/tourism marketing. If tenders are posted, they may appear in blog (esp/tailormadesafari, esp/gombe, etc.) or a dedicated procurement page. Check linked pages for document links.

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
  facebook: "deoadventuresafariguides"
  instagram: "deoadventure"

notes: |
  Mejor safari africano, Con Deoadventure ya no es un sueño, sino una realidad. correr por la sabana, saltar con los antilopes, acercarse...
---

# Bienvenido - Deoadventure

**Category:** Commercial / Private Sector
**Website:** https://www.deoadventure.co.tz/
**Tender Page:** https://www.deoadventure.co.tz/
**Keywords Found:** rfi, tender

## Contact Information
- Email: adventure@deoadventure.co.tz
- Phone: +255 622 825 826

- Phone: +255 622 825 826 
- Phone: 023-02-24
- Phone: 019-08-26
- Phone: 023-06-25

## Scraping Instructions

**Strategy:** Scrape https://www.deoadventure.co.tz/ for tender/procurement notices.
**Method:** http_get

Mejor safari africano, Con Deoadventure ya no es un sueño, sino una realidad. correr por la sabana, saltar con los antilopes, acercarse...

### Tender Content Preview

> stro gusto y como acordamos. De un mismo modo, tengo que decir que además de profesionales y entender sobre la fauna del lugar, también se han mostrado muy cercanos y agradables, y, teniendo en cuenta que pasamos muchas horas junto a ellos, esto segundo también es interesante tenerlo en cuenta.

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
deoadventure/
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
