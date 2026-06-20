---
institution:
  name: "Kairuki University (KU)"
  slug: "hkmu"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "hkmu.ac.tz"

website:
  homepage: "https://web.ku.ac.tz/"
  tender_url: "https://web.ku.ac.tz/component/content/article/request-for-proposals-rfp-for-debt-collection-services?catid=9&Itemid=101"

contact:
  email: "vc@ku.ac.tz"
  alternate_emails:
    - "secvc@ku.ac.tz"
    - "info@ku.ac.tz"
  phone: "0596850468"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape Joomla site with Chrome User-Agent (Mod_Security blocks basic curl). Category listing /component/content/category/9 returns 404; discover tenders via homepage links and article URLs. catid=9 articles include RFPs and vacancies (reject job postings). Known RFP debt collection expired 2025-10-15."
  selectors:
    container: "main, article, .item-page, .content, #sp-main-body"
    tender_item: "article, .item-page, .sppb-addon-article"
    title: "h1, h2, .item-title, .sppb-addon-title"
    date: ".published, .date, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="irec"], a[href*="download"]'
    pagination: ".pagination a, .pager a" 
  schedule: "daily"

  anti_bot:
    requires_javascript: false
    has_captcha: false
    rate_limit_seconds: 10
    user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    mod_security: true
    mod_security_note: "Basic curl User-Agent blocked with 406 Not Acceptable; use Chrome UA and Accept headers"

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
      - "/images/"
      - "/images/documents/"
      - "/media/"
      - "/downloads/"

    url_patterns:
      - "web.ku.ac.tz/"
      - "ku.ac.tz/images/documents/*.pdf"
      - "downloads.ku.ac.tz/*.pdf"

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
      Kairuki University (KU) Joomla site. RFPs in category catid=9. Documents: /images/, /media/, downloads.ku.ac.tz. IREC link on RFP page. Example: RFP for Debt Collection Services (deadline 15 Oct 2025).

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
  instagram: "kairukiuniversity"

notes: |
  Organization website at hkmu.ac.tz. Tender keywords detected: request for proposal, rfi, rfp.
---

# Home

**Category:** Educational Institution
**Website:** https://web.ku.ac.tz/
**Tender Page:** https://web.ku.ac.tz/component/content/article/request-for-proposals-rfp-for-debt-collection-services?catid=9&amp;Itemid=101
**Keywords Found:** request for proposal, rfi, rfp

## Contact Information
- Email: vc@ku.ac.tz
- Email: secvc@ku.ac.tz
- Email: info@ku.ac.tz
- Phone: 0596850468
- Phone: 0599800381 
- Phone: 06151416 
- Phone: 0601564482
- Phone: 05532614 

## Scraping Instructions

**Strategy:** Scrape https://web.ku.ac.tz/component/content/article/request-for-proposals-rfp-for-debt-collection-services?catid=9&amp;Itemid=101 for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- https://web.ku.ac.tz/component/content/article/request-for-proposals-rfp-for-debt-collection-services?catid=9&amp;Itemid=101

### Document Links Found

- http://ku.ac.tz/images/documents/hkmu-perspective-plan.pdf
- https://web.ku.ac.tz/images/2026/KU-ALMANAC-2025-2026.pdf
- https://downloads.ku.ac.tz/prospectus2023-2024.pdf
- http://ku.ac.tz/images/documents/prospectus2023-2024.pdf

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

Known document paths: /documents/prospectus2023-2024.pdf, /documents/hkmu-perspective-plan.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
hkmu/
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
