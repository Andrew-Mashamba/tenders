---
institution:
  name: "AGIM Consultants | Audit Firm in Tanzania"
  slug: "agim"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "agim.co.tz"

website:
  homepage: "https://www.agim.co.tz/"
  tender_url: "https://www.agim.co.tz/"

contact:
  phone: "00000686899395"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Wix-style site. No dedicated tender page. Scrape homepage and LATEST ARTICLES for bid/EOI/RFI notices. CPA/audit firm - procurement notices may appear in articles."
  selectors:
    container: "main, .content, [data-section]"
    tender_item: "article, [data-block-type='article'], section"
    title: "h2, h3, h4, [data-block-type='heading']"
    date: "time, .date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: "a[aria-label*='page'], .pagination a"
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
      - "agim.co.tz/*.pdf"

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
      No dedicated tender page. Audit/consulting firm. Check Latest Articles for bid/EOI notices. Document paths TBD.

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
  facebook: "profile.php"
  linkedin: "agimtz"
  instagram: "agimtz"

notes: |
  AGIM is a firm of Certified Auditors and Business Consultants based in Dar-es-salaam, Tanzania. The Firm is registered by the National Board of Accountants and Auditors (NBAA) as Certified Public Accountants in Public Practice.
---

# AGIM Consultants | Audit Firm in Tanzania

**Category:** Commercial / Private Sector
**Website:** https://www.agim.co.tz/
**Tender Page:** https://www.agim.co.tz/
**Keywords Found:** bid, eoi, rfi

## Contact Information
- Phone: 00000686899395
- Phone: 0152-0153
- Phone: 0490-0491
- Phone: 054-9284-6
- Phone: 00092661823728

## Scraping Instructions

**Strategy:** Scrape https://www.agim.co.tz/ for tender/procurement notices.
**Method:** http_get

AGIM is a firm of Certified Auditors and Business Consultants based in Dar-es-salaam, Tanzania. The Firm is registered by the National Board of Accountants and Auditors (NBAA) as Certified Public Accountants in Public Practice.

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
agim/
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
- **Signal Strength:** Strong (eoi)
