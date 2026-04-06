---
institution:
  name: "Zanzibar Teachers Union (ZATU)"
  slug: "zatu"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "zatu.or.tz"

website:
  homepage: "https://zatu.or.tz/"
  tender_url: "https://zatu.or.tz/"

contact:
  email: "info@zatu.or.tz"
  phone: "05882352944"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Homepage has Latest News with RFP notices (e.g. 'REQUEST FOR PROPOSALS (RFP) FOR CONDUCTING ZATU EVALUATION'). Site uses Zyrosite/Hostinger (Astro). Check /forms for RFP submission. Extract news items with RFP/tender keywords; follow document links."
  selectors:
    container: ".layout-element, .text-box, main, [data-v-4edbe80f]"
    tender_item: ".text-box, .layout-element__component"
    title: "h3, h4, h5, h6, .text-box"
    date: "h6, .layout-element"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download], a[href*="/forms"]'
    pagination: ".pagination a, a.next" 
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
      - "zatu.or.tz/*.pdf"

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
      RFP content appears in Latest News on homepage. Site may use client-side rendering (Zyrosite). Check /forms for RFP forms. Document links may be in news body or linked from detail pages.

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

notes: |
  The Zanzibar Teachers Union (ZATU) has been uniting educators across sectors since 2002. We advocate for teachers&#39; rights, promote quality education, and ensure their interests are represented on national and international platforms.
---

# Zanzibar Teachers Union: Advocating for Educators | ZATU

**Category:** NGO / Non-Profit Organization
**Website:** https://zatu.or.tz/
**Tender Page:** https://zatu.or.tz/
**Keywords Found:** request for proposal, rfp

## Contact Information
- Email: info@zatu.or.tz
- Phone: 05882352944
- Phone: 026143793
- Phone: 05882352941178
- Phone: 078431372549
- Phone: 08169934640522

## Scraping Instructions

**Strategy:** Scrape https://zatu.or.tz/ for tender/procurement notices.
**Method:** http_get

The Zanzibar Teachers Union (ZATU) has been uniting educators across sectors since 2002. We advocate for teachers&#39; rights, promote quality education, and ensure their interests are represented on national and international platforms.

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
zatu/
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
- **Signal Strength:** Strong (rfp)
