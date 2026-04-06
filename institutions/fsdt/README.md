---
institution:
  name: "Financial Inclusion | Digital Financial Services Tanzania | FSDT"
  slug: "fsdt"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "fsdt.or.tz"

website:
  homepage: "https://www.fsdt.or.tz/"
  tender_url: "https://www.fsdt.or.tz/work-with-us/"

contact:
  email: "info@fsdt.or.tz"
  phone: "0 842 767 846 7"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.fsdt.or.tz/work-with-us/ — 'CURRENT OPPORTUNITIES' section lists tender/RFP PDFs with direct links. Each list item (li) contains a link to PDF. Extract title from link text, document from href."
  selectors:
    container: "main#content, .entry-content"
    tender_item: "a[href*='wp-content/uploads'][href$='.pdf']"
    title: "a"
    date: null
    document_link: 'a[href$=".pdf"], a[href*="wp-content/uploads"]'
    pagination: null
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
      - "fsdt.or.tz/wp-content/uploads/*.pdf"
      - "www.fsdt.or.tz/wp-content/uploads/*.pdf"

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
      Documents in /wp-content/uploads/{year}/{month}/. CURRENT OPPORTUNITIES lists PDFs (ToR, EoI, RFPs). Title = link text, document = href. No dates on listing.

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
  facebook: "fsdtanzania"
  twitter: "FSDTanzania"
  linkedin: "financial-sector-deepening-trust"
  instagram: "fsdtanzania"

notes: |
  FSDT calls for financial inclusion in Tanzania and innovations in the fiscal sector through partnerships with financial stakeholders
---

# Financial Inclusion | Digital Financial Services Tanzania | FSDT

**Category:** NGO / Non-Profit Organization
**Website:** https://www.fsdt.or.tz/
**Tender Page:** https://www.fsdt.or.tz/
**Keywords Found:** bid, rfi, tender

## Contact Information
- Email: info@fsdt.or.tz
- Phone: 0 842 767 846 7
- Phone: 04 846 713 829
- Phone: 022-12-22
- Phone: 08 454 696 446
- Phone: 0 196 150 212 1

## Scraping Instructions

**Strategy:** Scrape https://www.fsdt.or.tz/ for tender/procurement notices.
**Method:** http_get

FSDT calls for financial inclusion in Tanzania and innovations in the fiscal sector through partnerships with financial stakeholders

### Tender Content Preview

> elihood, wellbeing, and empowerment of Tanzanians? Keep an eye out for our partnership, career, and tender opportunities. <li clas

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
fsdt/
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
