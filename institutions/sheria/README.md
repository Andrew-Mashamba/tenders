---
institution:
  name: "Wizara ya Katiba na Sheria (Ministry of Constitutional and Legal Affairs)"
  slug: "sheria"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "sheria.go.tz"

website:
  homepage: "https://sheria.go.tz/"
  tender_url: "https://sheria.go.tz/"

contact:
  email: "km@sheria.go.tz"
  phone: "026
          "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape homepage and https://sheria.go.tz/pages/procurement-management-unit for procurement notices. Site requires curl -k (SSL cert issue). Homepage Matangazo section has announcements; filter for zabuni/manunuzi only — reject mediator accreditation lists and news. Known documents at /uploads/documents/ with pattern sw-{timestamp}-{filename}.pdf"
  selectors:
    container: ".content, main, .entry-content, article"
    tender_item: "article, .tender-item, .list-item, li"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href*="/uploads/documents/"], a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
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

    known_document_paths:
      - "/uploads/documents/"
    url_patterns:
      - "sheria.go.tz/uploads/documents/sw-*.pdf"

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
      Documents at /uploads/documents/ with pattern sw-{timestamp}-{filename}.pdf (e.g. sw-1768552381-Mkataba katiba na sheria.pdf). Site unreachable during analysis.

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
  facebook: "profile.php"
  twitter: "Sheria_Katiba"
  linkedin: "katiba-na-sheria-tanzania-9b3250243"
  instagram: "katibanasheria_"

notes: |
  Tume ya Taifa ya Uchaguzi (NEC) ni Taasisi huru ya Serikali iliyoanzishwa mwaka 1993 chini ya Ibara ya 74(1) ya Katiba ya Jamhuri ya Muungano wa Tanzania ya Mwaka 1977 |     Wizara ya Katiba na Sheria - Mwanzo
---

# MoCLA |     Wizara ya Katiba na Sheria - Mwanzo

**Category:** Government Agency
**Website:** https://sheria.go.tz/
**Tender Page:** https://sheria.go.tz/
**Keywords Found:** procurement

## Contact Information
- Email: km@sheria.go.tz
- Phone: 026
          
- Phone: 025
          
- Phone: +255 26 2310019
- Phone: 0262-160-360-
- Phone: 0 25 0 0 43

## Scraping Instructions

**Strategy:** Scrape https://sheria.go.tz/ for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Tume ya Taifa ya Uchaguzi (NEC) ni Taasisi huru ya Serikali iliyoanzishwa mwaka 1993 chini ya Ibara ya 74(1) ya Katiba ya Jamhuri ya Muungano wa Tanzania ya Mwaka 1977 |     Wizara ya Katiba na Sheria - Mwanzo

### Tender Content Preview

> anning'>Idara ya Sera na Mipango Kitengo cha Ununuzi na Ugavi Kitengo cha Uangalizi wa Uta

### Document Links Found

- https://sheria.go.tz/uploads/documents/sw-1768552381-Mkataba katiba na sheria.pdf1 (1).pdf
- https://sheria.go.tz/uploads/documents/sw-1765345554-TAARIFA KWA UMMA DHR.pdf
- https://sheria.go.tz/uploads/documents/sw-1764692897-JAMHURI YA MUUNGANO WA TANZANIA (1).pdf
- https://sheria.go.tz/uploads/documents/sw-1765200062-DLAS TANGAZO.pdf

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
sheria/
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
- **Active Tenders:** 0 (no open procurement notices; announcements are mediator accreditation lists)
- **Signal Strength:** Strong (procurement)
