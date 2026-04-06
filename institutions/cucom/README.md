---
institution:
  name: "Catholic University of Mbeya"
  slug: "cucom"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "cucom.ac.tz"

website:
  homepage: "https://cucom.ac.tz/"
  tender_url: "https://cucom.ac.tz/"

contact:
  email: "info@cuom.ac.tz"
  phone: "+255 252 504 240"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage https://cucom.ac.tz/. Tenders (zabuni) and announcements in 'News & Announcements' section. Each item: div.ho-ev-date (date) + div.ho-ev-link (title + PDF link). Documents at /cm-posts/. Filter for zabuni/tender keywords (TANGAZO LA UZABUNI, etc.)."
  selectors:
    container: "div.ho-event"
    tender_item: "div.ho-ev-link"
    title: "p, a"
    date: "div.ho-ev-date"
    document_link: 'a[href*="/cm-posts/"]'
    pagination: "" 
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
      - "/cm-posts/"

    url_patterns:
      - "cucom.ac.tz/cm-posts/*.pdf"

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
      Documents in /cm-posts/. News & Announcements mixes tenders (TANGAZO LA UZABUNI), employment, results. Filter by title for zabuni/tender. For each .ho-ev-link item, date is in the immediately preceding .ho-ev-date sibling. Also check Upcoming Events (.singel-event) for linked docs.

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
  facebook: "tzcuom"
  instagram: "tzcuom"

notes: |
  Organization website at cucom.ac.tz. Tender keywords detected: zabuni.
---

# Catholic University of Mbeya

**Category:** Educational Institution
**Website:** https://cucom.ac.tz/
**Tender Page:** https://cucom.ac.tz/cm-posts/TANGAZO LA UZABUNI MACHI 2025.pdf
**Keywords Found:** zabuni

## Contact Information
- Email: info@cuom.ac.tz
- Phone: +255 252 504 240
- Phone: 024 - 02 
- Phone: 025 - 10 
- Phone: 024-2025 

## Scraping Instructions

**Strategy:** Scrape https://cucom.ac.tz/cm-posts/TANGAZO LA UZABUNI MACHI 2025.pdf for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> rrow-right"> TANGAZO LA UZABUNI HUDUMA YA &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CHAKULA - MACHI 2025 15:00

### Known Tender URLs

- https://cucom.ac.tz/cm-posts/TANGAZO LA UZABUNI MACHI 2025.pdf

### Document Links Found

- https://cucom.ac.tz/cm-posts/Interclass_Mootcourt_2024_2025.zip
- https://cucom.ac.tz/cm-posts/EMPLOYMENT VACANCIES FEBRUARY 2025.pdf
- https://cucom.ac.tz/cm-posts/guidelines/CUoM_POSTGRADUATE_REGULATIONS_&_GUIDELINES_2025_WEB VERSION.pdf
- https://cucom.ac.tz/cm-posts/TANGAZO LA UZABUNI MACHI 2025.pdf
- https://cucom.ac.tz/cm-posts/RESULTS_RELEASE_ANNOUNCEMENT_AUG_2024.pdf
- https://cucom.ac.tz/cm-posts/Moot_Court_Competition_Participant_Form.pdf
- https://cucom.ac.tz/cm-posts/RELEASE_OF_RESULTS_SEM_II_BAED_SEPT_2024.pdf

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
cucom/
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
- **Signal Strength:** Strong (zabuni)
