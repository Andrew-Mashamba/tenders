---
institution:
  name: "BIN ZUBEIRY SPORTS &#8212; ONLINE"
  slug: "binzubeiry"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "binzubeiry.co.tz"

website:
  homepage: "https://www.binzubeiry.co.tz/"
  tender_url: "https://www.binzubeiry.co.tz/"

contact:
  email: "4thebetter@gmail.com"
  alternate_emails:
    - "txkang.REMOVETHIS@hotmail.com"
    - "princezub@hotmail.com"
  phone: "007-2010 "

scraping:
  enabled: true
  method: "http_get"
  strategy: "BIN ZUBEIRY SPORTS is a sports news blog (Tanzania Premier League, football). No tender/procurement content. Keywords 'bid' are from sports context, not procurement."
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
      - "binzubeiry.co.tz/*.pdf"

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
      Document storage paths not yet identified. Check tender detail pages for download links.

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
  facebook: "2008"
  twitter: "BINZUBEIRY2016"

notes: |
  BIN ZUBEIRY SPORTS - ONLINE contains reliable and researched stories as well as effective, attractive and eye catching pictures of various events both locally and internationally. From Tanzania Mainland Premier League to European leagues notably Spanish La Liga, Germany’s Bundesliga, French Ligue One, Italian Serie A and the English Premier League as well as continental competitions like UEFA Champions League and UEFA Europa League.
---

# BIN ZUBEIRY SPORTS &#8212; ONLINE

**Category:** Commercial / Private Sector
**Website:** https://www.binzubeiry.co.tz/
**Tender Page:** https://www.dailymail.co.uk/sport/football/article-15642401/Sheffield-Wednesday-supporters-trust-bidder-bribery.html?ns_mchannel=rss&ns_campaign=1490&ito=1490
**Keywords Found:** bid, procurement, rfi

## Contact Information
- Email: 4thebetter@gmail.com
- Email: txkang.REMOVETHIS@hotmail.com
- Email: princezub@hotmail.com
- Phone: 007-2010 
- Phone: 026-03-07
- Phone: 04927521546517
- Phone: 08949996304093
- Phone: 0 134 197 194 9

## Scraping Instructions

**Strategy:** Scrape https://www.dailymail.co.uk/sport/football/article-15642401/Sheffield-Wednesday-supporters-trust-bidder-bribery.html?ns_mchannel=rss&ns_campaign=1490&ito=1490 for tender/procurement notices.
**Method:** http_get

BIN ZUBEIRY SPORTS - ONLINE contains reliable and researched stories as well as effective, attractive and eye catching pictures of various events both locally and internationally. From Tanzania Mainland Premier League to European leagues notably Spanish La Liga, Germany’s Bundesliga, French Ligue One, Italian Serie A and the English Premier League as well as continental competitions like UEFA Champions League and UEFA Europa League.

### Tender Content Preview

> IRECT, INCIDENTAL, SPECIAL, * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR T

### Known Tender URLs

- https://www.dailymail.co.uk/sport/football/article-15642401/Sheffield-Wednesday-supporters-trust-bidder-bribery.html?ns_mchannel=rss&ns_campaign=1490&ito=1490

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
binzubeiry/
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
