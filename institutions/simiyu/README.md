---
institution:
  name: "Ofisi ya Mkuu wa Mkoa wa Simiyu"
  slug: "simiyu"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "simiyu.go.tz"

website:
  homepage: "https://simiyu.go.tz/"
  tender_url: "https://simiyu.go.tz/tenders"
  note: "Tender page at /tenders. Fetch failed (SSL/timeout) - set enabled false until reachable. When live, likely same structure as simanjirodc."

contact:
  email: "ras@simiyu.go.tz"
  phone: "028-2700011"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Simiyu Regional Commissioner's Office. Use /tenders URL. Likely same October CMS structure as simanjirodc - table with Jina la Zabuni, dates, Pakua links. Documents at /storage/app/uploads/public/. Site was unreachable during analysis - may need -k for SSL."
  selectors:
    container: ".right-sidebar-content"
    tender_item: "table.table.table-striped tbody tr"
    title: "td:first-child"
    date: "td:nth-child(2), td:nth-child(3)"
    document_link: "td:last-child a, a[href*='/storage/']"
    pagination: "nav.text-center a" 
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
      - "simiyu.go.tz/storage/app/uploads/public/58e/4e2/320/58e4e2320912a761222055.pdf"
      - "simiyu.go.tz/storage/app/uploads/public/58e/4e3/29c/58e4e329c6235617525354.pdf"
      - "simiyu.go.tz/storage/app/uploads/public/5ea/6cb/54b/5ea6cb54b149c996712966.pdf"
      - "simiyu.go.tz/storage/app/uploads/public/590/8e6/38e/5908e638e2ef0108429716.pdf"
      - "simiyu.go.tz/storage/app/uploads/public/65d/445/1bb/65d4451bb45c2137216918.pdf"

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
      Known document paths: /storage/app/uploads/public/58e/4e2/320/58e4e2320912a761222055.pdf, /storage/app/uploads/public/58e/4e3/29c/58e4e329c6235617525354.pdf, /storage/app/uploads/public/5ea/6cb/54b/5ea6cb54b149c996712966.pdf

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
  facebook: "Simiyu-Regional-Commissioners-Office-290504338052416"
  instagram: "simiyu_region"

notes: |
  A default home page
---

# Home &#124; OFISI YA MKUU WA MKOA WA SIMIYU

**Category:** Government Agency
**Website:** https://simiyu.go.tz/
**Tender Page:** https://simiyu.go.tz/new/mashindao-ya-umiseta-na-umitashumta-yazinduliwa-kimkoa-maswa-dc-ngatumbura-asisitiza-nidhamu-na-bidii-ili-kupata-ushindi-katika-ngazi-ya-taifa
**Keywords Found:** bid, tender, tenders, zabuni

## Contact Information
- Email: ras@simiyu.go.tz
- Phone: 028-2700011
- Phone: 0504338052416
- Phone: 0108429716
- Phone: 024
	        

## Scraping Instructions

**Strategy:** Scrape https://simiyu.go.tz/new/mashindao-ya-umiseta-na-umitashumta-yazinduliwa-kimkoa-maswa-dc-ngatumbura-asisitiza-nidhamu-na-bidii-ili-kupata-ushindi-katika-ngazi-ya-taifa for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

A default home page

### Tender Content Preview

> ="home-page-title">Zabuni Zaidi Jina la Zabuni

### Known Tender URLs

- https://simiyu.go.tz/new/mashindao-ya-umiseta-na-umitashumta-yazinduliwa-kimkoa-maswa-dc-ngatumbura-asisitiza-nidhamu-na-bidii-ili-kupata-ushindi-katika-ngazi-ya-taifa
- https://simiyu.go.tz/tenders

### Document Links Found

- https://simiyu.go.tz/storage/app/uploads/public/58e/4e2/320/58e4e2320912a761222055.pdf
- https://simiyu.go.tz/storage/app/uploads/public/590/8e6/38e/5908e638e2ef0108429716.pdf
- https://simiyu.go.tz/storage/app/uploads/public/58e/4e3/29c/58e4e329c6235617525354.pdf
- https://simiyu.go.tz/storage/app/uploads/public/5ea/6cb/54b/5ea6cb54b149c996712966.pdf
- https://simiyu.go.tz/storage/app/uploads/public/65d/445/1bb/65d4451bb45c2137216918.pdf

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

Known document paths: /storage/app/uploads/public/58e/4e2/320/58e4e2320912a761222055.pdf, /storage/app/uploads/public/58e/4e3/29c/58e4e329c6235617525354.pdf, /storage/app/uploads/public/5ea/6cb/54b/5ea6cb54b149c996712966.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
simiyu/
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
- **Signal Strength:** Strong (tender, tenders, zabuni)
