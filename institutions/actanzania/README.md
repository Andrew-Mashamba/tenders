---
institution:
  name: "Agricultural Council of Tanzania (ACT)"
  slug: "actanzania"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "actanzania.or.tz"

website:
  homepage: "https://actanzania.or.tz/"
  tender_url: "https://actanzania.or.tz/index.php/act-news-media"

contact:
  email: "act@actanzania.or.tz"
  phone: "02157301808"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://actanzania.or.tz/index.php/act-news-media (Joomla/K2). Tender-like items (CALL FOR PROPOSALS, RFPs) appear in News/Media. Each article can have Dropfiles attachments. Follow article links to get full content and document downloads."
  selectors:
    container: "#sp-main-body, .k2ItemsBlock, .col-md-8"
    tender_item: ".article, div.article[itemprop='blogPost']"
    title: ".article-header h2 a, .article-header h2"
    date: ".article-info .published time, .article-info .published"
    document_link: '.dropfiles-file-link a, .dropfiles_downloadlink a, a[href*="/index.php/files/"]'
    pagination: ".pagination .page-link, .pagination a"
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
      - "actanzania.or.tz/index.php/files/*"
      - "actanzania.or.tz/*.pdf"

    known_document_paths:
      - "/index.php/files/"

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
      Joomla Dropfiles plugin. Documents at /index.php/files/{catid}/New-category/{fileid}/{filename}.pdf. Links in .dropfiles-file-link. Some articles (e.g. CALL FOR PROPOSALS) include ToR and application docs. Pagination uses ?start=N (2 items per page).

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
  facebook: "actanzania"
  twitter: "act_tz"
  linkedin: "baraza-la-kilimo-act-a56803214"
  instagram: "barazalakilimotanzania"

notes: |
  Organization website at actanzania.or.tz. Tender keywords detected: bid, rfi.
---

# Agricultural Council Of Tanzania- ACT - Welcome to Agricultural Council Of Tanzania - ACT

**Category:** NGO / Non-Profit Organization
**Website:** https://actanzania.or.tz/
**Tender Page:** https://actanzania.or.tz/index.php/act-news-media
**Keywords Found:** bid, rfi

## Contact Information
- Email: act@actanzania.or.tz
- Phone: 02157301808
- Phone: 02157301833
- Phone: 025           
- Phone: 01616868705
- Phone: 01616868714 

## Scraping Instructions

**Strategy:** Scrape https://actanzania.or.tz/index.php/act-news-media (Joomla/K2). Tender-like items (CALL FOR PROPOSALS, RFPs) appear in News/Media.
**Method:** http_get



### Known Tender URLs

- https://actanzania.or.tz/index.php/act-news-media

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
actanzania/
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
- **Signal Strength:** Weak (supply/rfi only)
