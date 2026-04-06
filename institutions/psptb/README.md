---
institution:
  name: "PSPTB - Bodi ya Wataalam wa Ununuzi na Ugavi (Procurement and Supplies Professionals and Technicians Board)"
  slug: "psptb"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "psptb.go.tz"

website:
  homepage: "https://psptb.go.tz/"
  tender_url: "https://psptb.go.tz/news"

contact:
  email: "barua@psptb.go.tz"
  phone: "0 1 1 1 1 1"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape psptb.go.tz/news for news items, psptb.go.tz/announcements for announcements, and psptb.go.tz/events for events. No dedicated tender listing - procurement-related content in news/announcements. Follow links to document pages. Documents stored at /uploads/documents/ with pattern en-{timestamp}-{filename}.pdf"
  selectors:
    container: "main, .content-area, .page-content"
    tender_item: "a[href*='/news/'], a[href*='/announcements/'], a[href*='/events/']"
    title: "h2, h3, h4, h5, h6, .entry-title, .title"
    date: ".date, .closing-date, .published, time, .post-date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/uploads/documents/"]'
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
      - "/uploads/documents/"

    url_patterns:
      - "psptb.go.tz/uploads/documents/*.pdf"
      - "psptb.go.tz/news/*"
      - "psptb.go.tz/announcements/*"
      - "psptb.go.tz/events/*"

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
      Documents use pattern /uploads/documents/en-{timestamp}-{filename}.pdf (e.g. en-1752671795-PUBLIC%20PROCUREMENT%20ACT%202023.pdf). PSPTB is a regulatory board - content is news, announcements, events; no traditional tender listing.

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
  facebook: "people"
  instagram: "psptbofficial"

notes: |
  Procurement and Supplies Professionals and Technicians Board | Bodi ya Wataalamu na Mafundi wa Ununuzi na Ugavi
---

# Mwanzo
 | PSPTB - Bodi ya Wataalam wa Ununuzi na Ugavi

**Category:** Government Agency
**Website:** https://psptb.go.tz/
**Tender Page:** https://psptb.go.tz/news/psptb-is-urge-to-take-action-against-those-who-violate-the-law-in-the-procurement-sector
**Keywords Found:** manunuzi, procurement, supply

## Contact Information
- Email: barua@psptb.go.tz
- Phone: 0 1 1 1 1 1
- Phone: 026 2962415
- Phone: 0 0 1920 100
- Phone: 0 1 1-6 0 3 3 0
- Phone: 0 1 0 0-6 3 3 0

## Scraping Instructions

**Strategy:** Scrape https://psptb.go.tz/news/psptb-is-urge-to-take-action-against-those-who-violate-the-law-in-the-procurement-sector for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Procurement and Supplies Professionals and Technicians Board | Bodi ya Wataalamu na Mafundi wa Ununuzi na Ugavi

### Tender Content Preview

> ="viewport" content="width=device-width, initial-scale=1"> <meta name="keywords" content="psptb,procurement,supply , psptb,manunuzi,ununuzi,

### Known Tender URLs

- https://psptb.go.tz/news/psptb-is-urge-to-take-action-against-those-who-violate-the-law-in-the-procurement-sector
- https://www.psptb.go.tz/uploads/documents/en-1752671795-PUBLIC%20PROCUREMENT%20ACT%202023.pdf
- https://psptb.go.tz/events/workshop-on-e-supply-chain-application-in-practice-case-of-procurement-and-inventory-management-systems-in-tanzania

### Document Links Found

- https://www.psptb.go.tz/uploads/documents/en-1745236812-PSPTB%20Code%20of%20Ethics%20and%20Conduct%20(1).pdf
- https://www.psptb.go.tz/uploads/documents/en-1752671795-PUBLIC%20PROCUREMENT%20ACT%202023.pdf

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

Known document paths: /uploads/documents/en-1752671795-PUBLIC%20PROCUREMENT%20ACT%202023.pdf, /uploads/documents/en-1745236812-PSPTB%20Code%20of%20Ethics%20and%20Conduct%20(1).pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
psptb/
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
- **Signal Strength:** Strong (manunuzi, procurement)
