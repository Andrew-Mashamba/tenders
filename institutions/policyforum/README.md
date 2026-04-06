---
institution:
  name: "Policy Forum"
  slug: "policyforum"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "policyforum.or.tz"

website:
  homepage: "https://www.policyforum-tz.org/"
  tender_url: "https://www.policyforum-tz.org/opportunities/tender"

contact:
  email: "info@policyforum.or.tz"
  phone: "027-4638-9"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape Drupal tender table at /opportunities/tender. Each row links to /node/{id} for full tender details. Follow node links to get document attachments from Attachments table (sites/default/files/)."
  selectors:
    container: "table.cols-3, .region-content, main"
    tender_item: "table.cols-3 tbody tr"
    title: "td.views-field-title a, .views-field-title a"
    date: "td.views-field-field-expirationdate time, .views-field-field-expirationdate"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href*="/sites/default/files/"]'
    pagination: ".pager a, .pagination a" 
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
      - "/sites/default/files/"
    url_patterns:
      - "policyforum-tz.org/sites/default/files/*.pdf"
      - "policyforum-tz.org/node/*"

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
      Drupal site. Tender listing in table.cols-3. Each tender links to /node/{id}. Document attachments on detail pages in table with links to /sites/default/files/. Follow node links to get full ToR PDFs.

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
  facebook: "PolicyForumTZ"
  twitter: "policy_F"
  linkedin: "semkae-kilonzo"
  instagram: "policy_forum"

notes: |
  Organization website at policyforum.or.tz. Tender keywords detected: rfi, tender.
---

# Home page | Policy Forum

**Category:** NGO / Non-Profit Organization
**Website:** https://www.policyforum-tz.org/
**Tender Page:** https://www.policyforum-tz.org/opportunities/tender
**Keywords Found:** rfi, tender

## Contact Information
- Email: info@policyforum.or.tz
- Phone: 027-4638-9
- Phone: 025-12-19
- Phone: 026-02-19
- Phone: 02025-12-18
- Phone: 026-02-18

## Scraping Instructions

**Strategy:** Scrape https://www.policyforum-tz.org/opportunities/tender for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- https://www.policyforum-tz.org/opportunities/tender

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
policyforum/
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
