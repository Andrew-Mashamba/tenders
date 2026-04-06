---
institution:
  name: "SIDO - Shirika la Maendeleo ya Viwanda Vidogo"
  slug: "sido"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "sido.go.tz"

website:
  homepage: "https://sido.go.tz/"
  tender_url: "https://nest.go.tz/tenders/published-tenders"
  note: "SIDO uses NeST (National e-Procurement System). Tender URL points to nest.go.tz."

contact:
  email: "dg@sido.go.tz"
  phone: "074028131"

scraping:
  enabled: true
  method: "http_get"
  strategy: "NeST is an Angular SPA. Content loads via JavaScript after page load. Use headless browser (Puppeteer/Playwright) or NeST API if available. HTTP GET returns only loading spinner - no tender HTML in initial response."
  selectors:
    container: "app-root"
    tender_item: "N/A - SPA loads content dynamically"
    title: "N/A"
    date: "N/A"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: "N/A" 
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
      - "nest.go.tz/*"
      - "sido.go.tz/*.pdf"

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
      NeST is PPRA's e-procurement portal. Documents may be behind login. Check tender detail pages within the SPA for download links. SIDO posts via NeST.

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
  facebook: "sidotanzania"
  twitter: "SIDOtanzania"
  instagram: "sido_tanzania"

notes: |
  jaVasCript:/-/⁠ /*\ ⁠/*&#039;/&quot;//(/ */onerror=alert(&#039;eGSOC&#039;) )//%0D%0A%0d%0a//&lt;/stYle/&lt;/titLe/&lt;/teXtarEa/&lt;/scRipt/--!&gt;\x3csVg/&lt;sVg/oNloAd=alert(&#039;eGSOC&#039;)//&gt;\x3e
---

# SIDO |     Shirika la Maendeleo ya Viwanda Vidogo - Mwanzo

**Category:** Government Agency
**Website:** https://sido.go.tz/
**Tender Page:** https://nest.go.tz/tenders/published-tenders
**Keywords Found:** bid, tender, tenders

## Contact Information
- Email: dg@sido.go.tz
- Phone: 074028131
- Phone: 086075428471
- Phone: 07
          
- Phone: +255 22 215 1948

## Scraping Instructions

**Strategy:** Scrape https://nest.go.tz/tenders/published-tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

jaVasCript:/-/⁠ /*\ ⁠/*&#039;/&quot;//(/ */onerror=alert(&#039;eGSOC&#039;) )//%0D%0A%0d%0a//&lt;/stYle/&lt;/titLe/&lt;/teXtarEa/&lt;/scRipt/--!&gt;\x3csVg/&lt;sVg/oNloAd=alert(&#039;eGSOC&#039;)//&gt;\x3e

### Tender Content Preview

> iv class="pr-1 py-2"> Mfumo wa NesT <a class="" target="_blank" rel="noopener noreferrer" href="https://ess.ut

### Known Tender URLs

- https://nest.go.tz/tenders/published-tenders

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
sido/
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
