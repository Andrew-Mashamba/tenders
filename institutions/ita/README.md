---
institution:
  name: "Institute of Tax Administration"
  slug: "ita"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "ita.ac.tz"

website:
  homepage: "https://ita.ac.tz/"
  tender_url: "https://ita.ac.tz/index.php/tenders"

scraping:
  enabled: true
  method: "http_get"
  strategy: |
    Scrape https://ita.ac.tz/index.php/tenders. Joomla site. Content in main#content .item-page.
    When tenders exist, they appear in [itemprop="articleBody"]. May show "No Tender at the moment".
    Documents in /images/uploads/downloads/ and sidebar .well _menu. Pagination: .pager.pagenav.
  selectors:
    container: "main#content, .item-page"
    tender_item: ".item-page [itemprop='articleBody'] p, .item-page table tr, .item-page ul li"
    title: "h2, h3, .page-header, a"
    date: ".date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href*="uploads/downloads"], a[href*="images/uploads"]'
    pagination: ".pager.pagenav a, .pagenav .next a" 
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
      - "/images/uploads/downloads/"
      - "/Documents/web content/"

    url_patterns:
      - "ita.ac.tz/images/uploads/downloads/*"
      - "ita.ac.tz/Documents/web%20content/*"
      - "ita.ac.tz/Documents/web%20content/ITA%20Fourth%20Strategic%20Plan%202019-1.pdf"
      - "ita.ac.tz/uploads/downloads/Almanac_2025_26_Rev_.pdf"

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
      Documents in /images/uploads/downloads/ (e.g. PROSPECTUS_2025-2026.pdf, Almanac_2025_26_Rev_.pdf).
      Some sidebar links use backslash path (images\uploads). Resolve to /images/uploads/.

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

notes: |
  Institute of Tax Administration website
---

# Home

**Category:** Educational Institution
**Website:** https://ita.ac.tz/
**Tender Page:** https://ita.ac.tz/index.php/tenders
**Keywords Found:** rfi, tender, tenders

## Contact Information
- Not yet extracted. Check website.

## Scraping Instructions

**Strategy:** Scrape https://ita.ac.tz/index.php/tenders for tender/procurement notices.
**Method:** http_get

Institute of Tax Administration website

### Tender Content Preview

> "item-475"> Feedback Tenders Staff mail service <a href="https://salarysli

### Known Tender URLs

- https://ita.ac.tz/index.php/tenders

### Document Links Found

- https://ita.ac.tz/images\uploads\downloads\graduation_advert_2025.pdf
- https://ita.ac.tz/images\uploads\downloads\Abstracts_of.pdf
- https://ita.ac.tz/images\uploads\downloads\PROSPECTUS_2025-2026.pdf
- https://ita.ac.tz/images\uploads\downloads\FINAL_ITA_JOURNAL_VOL_5__final_version_for_print_1.pdf
- https://ita.ac.tz/images\uploads\downloads\LIST_OF_SELECTED_CCTM_PROGRAMM_APPLICANTS_FOR_2025-2026_ACADEMIC_YEAR.pdf
- https://ita.ac.tz/images\uploads\downloads\Updated_list_of_selected_DCTM_applicants_for_Academic_year_2020-2021_.pdf
- file:///C:/Users/Magreth/Documents/web%20content/ita%20alumni%20constitution.docx.pdf
- https://ita.ac.tz/images\uploads\downloads\Selected_CFFPC_applicants_for_academic_years_2020-2021.pdf
- https://www.ita.ac.tz/images/uploads/downloads/Almanac_2025_26_Rev_.pdf
- https://ita.ac.tz/images\uploads\downloads\LIST_OF_SELECTED_DCTM_PROGRAMME__APPLICANTS_FOR_2025-2026_ACADEMIC_YEAR.pdf

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

Known document paths: /Documents/web%20content/ita%20alumni%20constitution.docx.pdf, /Documents/web%20content/ITA%20Fourth%20Strategic%20Plan%202019-1.pdf, /uploads/downloads/Almanac_2025_26_Rev_.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
ita/
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
