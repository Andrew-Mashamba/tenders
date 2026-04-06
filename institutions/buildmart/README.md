---
institution:
  name: "Buildmart Limited"
  slug: "buildmart"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "buildmart.co.tz"

website:
  homepage: "https://buildmart.co.tz/"
  tender_url: "https://buildmart.co.tz/"

contact:
  email: "info@buildmart.co.tz"
  alternate_emails:
    - "gm@buildmart.co.tz"
  phone: "0 842 767 846 7"

scraping:
  enabled: false
  method: "http_get"
  strategy: "DISABLED: Homepage has no tender listing. Site is FMCG/HORECA supplier—company profile, news, products. Only PDF is company profile at /wp-content/uploads/. No procurement/tender page found."
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
    download_enabled: false
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
      - "buildmart.co.tz/wp-content/uploads/2025/06/NEW-COMPANY-PROFILE.pdf"

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
      No tender documents. Only document found: company profile at /wp-content/uploads/2025/06/NEW-COMPANY-PROFILE.pdf. Re-enable if tender/procurement page is added.

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
  facebook: "buildmartltd"
  linkedin: "buildmart-limited-fmcg-and-horeca-78a84b242"
  instagram: "buildmartltd"

notes: |
  Organization website at buildmart.co.tz. Tender keywords detected: procurement, supply.
---

# Food and Beverages Supplies - Buildmart limited

**Category:** Commercial / Private Sector
**Website:** https://buildmart.co.tz/
**Tender Page:** https://buildmart.co.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Email: info@buildmart.co.tz
- Email: gm@buildmart.co.tz
- Phone: 0 842 767 846 7
- Phone: 04 846 713 829
- Phone: 08 454 696 446
- Phone: 00000000 27
- Phone: 04 958 771

## Scraping Instructions

**Strategy:** Scrape https://buildmart.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ur one-stop shop for top-quality food &amp; beverage supplies and equipment ELEVATE YOUR HORECA OPS PROCUREMENT SOLUTIONS FMCG IMPORTATION &amp; DISTRIBUTION LEARN MORE Buildmart is your one-stop shop for streamlining procurement and elevating guest experiences in Tanzania&#8217;s vibrant HORECA sec

### Document Links Found

- https://buildmart.co.tz/wp-content/uploads/2025/06/NEW-COMPANY-PROFILE.pdf

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

Known document paths: /wp-content/uploads/2025/06/NEW-COMPANY-PROFILE.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
buildmart/
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
- **Signal Strength:** Strong (procurement)
