---
institution:
  name: "Auditax International"
  slug: "auditaxinternational"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "auditaxinternational.co.tz"

website:
  homepage: "https://auditaxinternational.co.tz/"
  tender_url: "https://auditaxinternational.co.tz/mec-category/seminars/"

contact:
  email: "info@auditaxinternational.co.tz"
  phone: "026-05-11"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape /mec-category/seminars/ (Modern Events Calendar). NOTE: Content is training/seminar invitations (CPD events), NOT procurement tenders. Do NOT create tender records for seminar invitations. Only create records for actual RFPs, RFQs, or procurement notices if found elsewhere on site."
  selectors:
    container: ".mec-skin-list-events-container, .mec-wrap, #main-content"
    tender_item: "article.mec-event-article"
    title: ".mec-event-title a, h4.mec-event-title"
    date: ".mec-event-date .mec-start-date-label, .mec-event-date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], .mec-event-title a, .mec-event-image a'
    pagination: ".mec-load-more, a[href*='page/']" 
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
      - "/wp-content/uploads/"

    url_patterns:
      - "auditaxinternational.co.tz/wp-content/uploads/*/*/*.pdf"

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
      WordPress; documents in /wp-content/uploads/YYYY/MM/. Event titles often link directly to PDF. Some events link to detail page (/training/...) - follow for download link. Invitation letters use 'Download-XXX-Invitation-Letter-Here.pdf' pattern.

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
  linkedin: "auditax-international"

notes: |
  We help transform your busuiness through Audit and Risk Management, Tax Services, Business Advisory and Accounting Services
---

# Home | Auditax International

**Category:** Commercial / Private Sector
**Website:** https://auditaxinternational.co.tz/
**Tender Page:** https://auditaxinternational.co.tz/training/invitation-of-you-and-your-staff-to-a-practical-5-day-fixed-assets-inventory-management-and-procurement-seminar-with-cpd-hours-to-be-held-form-11th-to-15th-may-2026-at-morena-hotel/
**Keywords Found:** bid, procurement, rfi

## Contact Information
- Email: info@auditaxinternational.co.tz
- Phone: 026-05-11
- Phone: 0038844-391
- Phone: +255 719 878490 
- Phone: 026-05-15
- Phone: 026-05-04

## Scraping Instructions

**Strategy:** Scrape https://auditaxinternational.co.tz/training/invitation-of-you-and-your-staff-to-a-practical-5-day-fixed-assets-inventory-management-and-procurement-seminar-with-cpd-hours-to-be-held-form-11th-to-15th-may-2026-at-morena-hotel/ for tender/procurement notices.
**Method:** http_get

We help transform your busuiness through Audit and Risk Management, Tax Services, Business Advisory and Accounting Services

### Tender Content Preview

> raining/invitation-of-you-and-your-staff-to-a-practical-5-day-fixed-assets-inventory-management-and-procurement-seminar-with-cpd-hours-to-be-held-form-11th-to-15th-may-2026-at-morena-hotel/" target="_blank" rel="noopener"><img loading="lazy" decoding="async" width="474" height="324" src="https://aud

### Known Tender URLs

- https://auditaxinternational.co.tz/training/invitation-of-you-and-your-staff-to-a-practical-5-day-fixed-assets-inventory-management-and-procurement-seminar-with-cpd-hours-to-be-held-form-11th-to-15th-may-2026-at-morena-hotel/

### Document Links Found

- https://auditaxinternational.co.tz/wp-content/uploads/2026/02/Download-Tax-Accounting-20-24-April-2026-Bagamoyo-Invitation.pdf
- https://auditaxinternational.co.tz/wp-content/uploads/2026/03/Download-A-Year-End-Financial-Reporting-ESG-Advanced-Excel-and-Tax-Seminar-11-16-May-Invitation-Letter-Here.pdf
- https://auditaxinternational.co.tz/wp-content/uploads/2026/03/DOWNLOAD-PRACTICAL-VAT-INVOICE-TAX-AND-TAX-ADMINISTRATION-ACT-SEMINAR-4-8-MAY-INVITATION-LETTER-HERE.pdf
- https://auditaxinternational.co.tz/wp-content/uploads/2026/02/Download-Financial-Reporting-Advanced-Excel-and-Tax-Seminar-23rd-to-27th-March-2026-Nashera-Hotel.pdf
- https://auditaxinternational.co.tz/wp-content/uploads/2026/03/Download-Comprehensive-IPSAS-and-Financial-Reporting-18-22-May-Invitation-Letter-Here.pdf
- https://auditaxinternational.co.tz/wp-content/uploads/2026/03/Download-Board-and-Commitee-Members-and-Management-Seminar-18-23-May-Invitation-Letter-Here.pdf

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

Known document paths: /wp-content/uploads/2026/03/Download-Board-and-Commitee-Members-and-Management-Seminar-18-23-May-Invitation-Letter-Here.pdf, /wp-content/uploads/2026/02/Download-Tax-Accounting-20-24-April-2026-Bagamoyo-Invitation.pdf, /wp-content/uploads/2026/03/Download-A-Year-End-Financial-Reporting-ESG-Advanced-Excel-and-Tax-Seminar-11-16-May-Invitation-Letter-Here.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
auditaxinternational/
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
