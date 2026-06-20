---
institution:
  name: "Rungwe International College of Business and Entrepreneurship Development"
  slug: "ricobed"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "ricobed.ac.tz"

website:
  homepage: "https://ricobed.ac.tz/"
  tender_url: "https://ricobed.ac.tz/"

contact:
  email: "info@ricobed.ac.tz"
  alternate_emails:
    - "directorricobed@gmail.com"
  phone: "0 0 16000 16000"

scraping:
  enabled: true
  method: "http_get"
  strategy: "RICOBED college has procurement department but no dedicated tender listing. Scrape #hpage_latestnews for news, #hpage_specials for college info. Documents at site root (e.g. fee_structure_for_certificate_and_diploma.pdf, new_application_form.pdf)."
  selectors:
    container: "#container, .wrapper.row3, #hpage_latestnews, #hpage_specials"
    tender_item: "#hpage_latestnews li, #hpage_specials li"
    title: "h2.title, .latestnews, .readmore a"
    date: "N/A - dates in news items"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: "N/A" 
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
      - "/"
    url_patterns:
      - "ricobed.ac.tz/*.pdf"
      - "ricobed.ac.tz/fee_structure_for_certificate_and_diploma.pdf"
      - "ricobed.ac.tz/new_application_form.pdf"
      - "ricobed.ac.tz/RICOBED_PROSPECTUS_*.pdf"

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
      Documents at site root. No dedicated tender section. Department of Procurements and Supply Management exists; check Job_opportunities.html and news for procurement notices.

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
  facebook: "rungweinternational"

notes: |
  Organization website at ricobed.ac.tz. Tender keywords detected: procurement, supply.
---

# Rungwe International College of Business and Entrepreneurship Development

**Category:** Educational Institution
**Website:** https://ricobed.ac.tz/
**Tender Page:** https://ricobed.ac.tz/
**Keywords Found:** procurement, supply

## Contact Information
- Email: info@ricobed.ac.tz
- Email: directorricobed@gmail.com
- Phone: 0 0 16000 16000
- Phone: +255 252 552 664
- Phone: +255 252 552 664 
- Phone: +255 689 175 843
- Phone: 021-2022  

## Scraping Instructions

**Strategy:** Scrape https://ricobed.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> rtificate (NTA level 4), Technician Certificate (NTA level 5) and Ordinary Diploma (NTA Level 6) in Procurement and Supply course. Our commitment to life-long learning takes many forms. RICOBED partners with Government Institutions and employers within reach to improve learning outcomes, pro

### Document Links Found

- https://ricobed.ac.tz/fee_structure_for_certificate_and_diploma.pdf
- https://ricobed.ac.tz/new_application_form.pdf
- https://ricobed.ac.tz/RICOBED_PROSPECTUS_2016-2017.pdf

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
ricobed/
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

- **Last Checked:** 11 June 2026
- **Active Tenders:** 0 (Job_opportunities.html lists employment vacancies, not procurement)
- **Signal Strength:** Weak (procurement course/department mentions only)
