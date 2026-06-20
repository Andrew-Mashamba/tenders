---
institution:
  name: "Temeke Municipal Council"
  slug: "temekemc"
  category: "Local Government Authority"
  status: "active"
  country: "Tanzania"
  domain: "temekemc.go.tz"

website:
  homepage: "https://temekemc.go.tz/"
  tender_url: "https://temekemc.go.tz/tenders"

contact:
  email: "temeke@temekemc.go.tz"
  phone: "040828238"

scraping:
  enabled: true
  method: "http_get"
  strategy: "SPA (GWF CORE) requires JavaScript. Use REST API: GET https://temekemc.go.tz/api/advertisements?category=Tender&page=1&limit=50. Attachments in /minio/temekemc.go.tz/attachments/. Legacy /storage/app/uploads/public/ paths may still exist."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" 
  schedule: "daily"

  anti_bot:
    requires_javascript: true
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
      - "temekemc.go.tz/storage/app/uploads/public/691/6f0/8fb/6916f08fba521691323962.pdf"
      - "temekemc.go.tz/storage/app/uploads/public/697/9df/e73/6979dfe73f5c4577895249.pdf"
      - "temekemc.go.tz/storage/app/uploads/public/696/e4b/639/696e4b63917e5687341182.pdf"
      - "temekemc.go.tz/storage/app/uploads/public/690/08a/ccb/69008accb81b2804859198.pdf"
      - "temekemc.go.tz/storage/app/uploads/public/69b/015/946/69b015946610e040828238.pdf"

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
      Known document paths: /storage/app/uploads/public/691/6f0/8fb/6916f08fba521691323962.pdf, /storage/app/uploads/public/697/9df/e73/6979dfe73f5c4577895249.pdf, /storage/app/uploads/public/696/e4b/639/696e4b63917e5687341182.pdf

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
  facebook: "temekemanispaa"
  instagram: "temeke_mc"

notes: |
  Tender page was unreachable during analysis (SSL/timeout). Selectors kept from known document paths. Verify page structure when accessible. Documents at /storage/app/uploads/public/{hash}/{hash}/{hash}/{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}{hash}.pdf
---

# Home &#124; Temeke Municipal Council

**Category:** Local Government Authority
**Website:** https://temekemc.go.tz/
**Tender Page:** https://temekemc.go.tz/tenders
**Keywords Found:** bid, manunuzi, tender, tenders, zabuni

## Contact Information
- Email: temeke@temekemc.go.tz
- Phone: 040828238
- Phone: 021

         
- Phone: 015946610
- Phone: 021-2025
	    
- Phone: +255 22-2928132 

## Scraping Instructions

**Strategy:** Scrape https://temekemc.go.tz/tenders for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://temekemc.go.tz/tenders
- https://temekemc.go.tz/new/shule-ya-msingi-mtoni-sabasaba-yakabidhiwa-madawati-30-na-miche-60-ya-miti
- https://temekemc.go.tz/new/pongezi-kwa-wakuu-wa-idara-na-vitengo-dc-mapunda-awakabidhi-vyeti

### Document Links Found

- https://temekemc.go.tz/storage/app/uploads/public/697/9df/e73/6979dfe73f5c4577895249.pdf
- https://temekemc.go.tz/storage/app/uploads/public/691/6f0/8fb/6916f08fba521691323962.pdf
- https://temekemc.go.tz/storage/app/uploads/public/69b/015/946/69b015946610e040828238.pdf
- https://temekemc.go.tz/storage/app/uploads/public/696/e4b/639/696e4b63917e5687341182.pdf
- https://temekemc.go.tz/storage/app/uploads/public/690/08a/ccb/69008accb81b2804859198.pdf

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

Known document paths: /storage/app/uploads/public/691/6f0/8fb/6916f08fba521691323962.pdf, /storage/app/uploads/public/697/9df/e73/6979dfe73f5c4577895249.pdf, /storage/app/uploads/public/696/e4b/639/696e4b63917e5687341182.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
temekemc/
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
- **Signal Strength:** Strong (manunuzi, tender, tenders, zabuni)
