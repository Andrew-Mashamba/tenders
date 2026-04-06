---
institution:
  name: "PANITA - Partnership for Nutrition in Tanzania"
  slug: "panita"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "panita.or.tz"

website:
  homepage: "https://panita.or.tz/"
  tender_url: "https://panita.or.tz/"

contact:
  email: "info@panita.co.tz"
  alternate_emails:
    - "info@panita.or.tz"
  phone: "085210968961"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://panita.or.tz/ homepage. PANITA (Partnership for Nutrition in Tanzania) - Latest News section lists tenders/EOI as article.comment-body. Each item has title in .comment_postinfo .fn, date in .comment_date, PDF link in .comment-content a."
  selectors:
    container: ".et_pb_section, div[class*='comment']"
    tender_item: "article.comment-body"
    title: ".comment_postinfo .fn, .comment_postinfo span.fn"
    date: ".comment_date"
    document_link: '.comment-content a[href$=".pdf"], a[href$=".pdf"], a[target="_blank"][href*=".pdf"]'
    pagination: "a[href='news.php']"
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
      - "/wp-content/uploads/2014/04/"
    url_patterns:
      - "panita.or.tz/wp-content/uploads/2014/04/*.pdf"

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
      Documents in /wp-content/uploads/2014/04/. Tenders mixed with news (e.g. panita_tender1.pdf, audit reports). Follow 'More News...' to news.php for full list.

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
  facebook: "tr"
  twitter: "panita_tz"

notes: |
  Organization website at panita.or.tz. Tender keywords detected: expression of interest, rfi, tender, tenders.
---

# panita

**Category:** NGO / Non-Profit Organization
**Website:** https://panita.or.tz/
**Tender Page:** https://panita.or.tz/wp-content/uploads/2014/04/panita_tender1.pdf
**Keywords Found:** expression of interest, rfi, tender, tenders

## Contact Information
- Email: info@panita.co.tz
- Email: info@panita.or.tz
- Phone: 085210968961
- Phone: 021
          

## Scraping Instructions

**Strategy:** Scrape https://panita.or.tz/wp-content/uploads/2014/04/panita_tender1.pdf for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> em menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-6453"> Tenders <a href="proposal.ph

### Known Tender URLs

- https://panita.or.tz/wp-content/uploads/2014/04/panita_tender1.pdf

### Document Links Found

- https://panita.or.tz/wp-content/uploads/2014/04/working_paper_1.pdf
- https://panita.or.tz/wp-content/uploads/2014/04/audit_2021.pdf
- https://panita.or.tz/wp-content/uploads/2014/04/audit_2019.pdf
- https://panita.or.tz/wp-content/uploads/2014/04/audit_2020.pdf
- https://panita.or.tz/wp-content/uploads/2014/04/pongezi.pdf
- https://panita.or.tz/wp-content/uploads/2014/04/panita_tender1.pdf
- https://panita.or.tz/wp-content/uploads/2014/04/annual_report_2019.pdf

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

Known document paths: /wp-content/uploads/2014/04/audit_2020.pdf, /wp-content/uploads/2014/04/annual_report_2019.pdf, /wp-content/uploads/2014/04/panita_tender1.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
panita/
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

- **Last Checked:** 15 March 2026
- **Active Tenders:** 0
- **Signal Strength:** Strong (expression of interest, tender, tenders)
- **Note:** Latest EOI (panita_tender1.pdf) was FY2021 audit — expired
