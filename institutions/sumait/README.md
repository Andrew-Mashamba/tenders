---
institution:
  name: "Abdulrahman Al-Sumait University (SUMAIT)"
  slug: "sumait"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "sumait.ac.tz"

website:
  homepage: "https://sumait.ac.tz/"
  tender_url: "https://sumait.ac.tz/"

contact:
  email: "info@eduker.com"
  alternate_emails:
    - "info@sumait.ac.tz"
  phone: "0 0 1 2 17"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape sumait.ac.tz homepage. 'Latest Notices' section contains JOB POSTINGS only (Bursar 2026, Assistant Lecturer Computer Sciences, Imam, DVC, Auditor) — REJECT as tenders. 'Useful Files' has almanac/fee structure only. Documents: /assets/docs/ and download.php?id=X. No procurement tenders found (verified 2026-06-11)."
  selectors:
    container: "section, .announcements, .latest-notices, main"
    tender_item: ".card.ann-card, .ann-card.mb-3, .ann-card.mb-15"
    title: "h5, h6, .card-title, .ann-card h5"
    date: ".date, .posted, .card-body small"
    document_link: 'a[href$=".pdf"], a[href*="/assets/docs/"], a[href*="download.php"]'
    pagination: ".pagination a, a.next, .nav-links a, button[aria-label*='Load']" 
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
      - "sumait.ac.tz/assets/docs/*"
      - "sumait.ac.tz/download.php?id=*"

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
      Documents in /assets/docs/ (PDFs: job adverts, almanac, prospectus) and download.php?id=X (fee structure, joining instructions, scholarship lists). Latest Notices = job/tender announcements with Download PDF links.

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
  Organization website at sumait.ac.tz. Tender keywords detected: procurement, tender.
---

# SUMAIT

**Category:** Educational Institution
**Website:** https://sumait.ac.tz/
**Tender Page:** https://sumait.ac.tz/
**Keywords Found:** procurement, tender

## Contact Information
- Email: info@eduker.com
- Email: info@sumait.ac.tz
- Phone: 0 0 1 2 17
- Phone: 000488281 10
- Phone: +255 774 635625
- Phone: 026           
- Phone: 025           

## Scraping Instructions

**Strategy:** Scrape https://sumait.ac.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ,{"date":"15\/06\/2026","end":"19\/06\/2026","title":"Term papers"},{"date":"15\/06\/2026","title":"Tender Board Meeting"},{"date":"22\/06\/2026","title":"Examination moderation second semester"},{"date":"27\/06\/2026","title":"Council Meeting"},{"date":"30\/06\/2026","title":"Submission of higher d

### Document Links Found

- https://sumait.ac.tz/assets/docs/JOB ADVERT OF POSITION OF SUMAIT BURSAR (2025).pdf
- https://sumait.ac.tz/assets/docs/FINAL ALMANAC 2025-2026 (1).pdf
- https://sumait.ac.tz/assets/docs/UniversityImamVacants-AdministrativePosts -2026.pdf
- https://sumait.ac.tz/assets/docs/JOB ADVERT OF POSITION OF SUMAIT BURSAR (2025) (2).pdf
- https://sumait.ac.tz/assets/docs/sumait_job_2026.pdf

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
sumait/
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
- **Active Tenders:** 0
- **Signal Strength:** Strong (procurement, tender)
- **Notes:** Latest Notices are job vacancies only (University Bursar, Assistant Lecturer) — not procurement.
