---
institution:
  name: "Ofisi ya Makamu wa Rais (Office of the Vice President)"
  slug: "vpo"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "vpo.go.tz"

website:
  homepage: "https://www.vpo.go.tz/"
  tender_url: "https://www.vpo.go.tz/publications/tender"

contact:
  email: "ps@vpo.go.tz"
  phone: "026
         "

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.vpo.go.tz/publications/tender (Zabuni). Tenders displayed as card grid. Each card is an anchor with PDF link. Link text format: '[date] Title' (e.g. '22nd Jun 2020 Terms of Reference...'). Parse date from link text. Documents at /uploads/publications/, /uploads/files/, /uploads/speeches/docs/."
  selectors:
    container: ".container-lg.shadow-lg, .row.my-4"
    tender_item: ".col-12.col-md-6.col-lg-4.mb-3, a.shadow-hover"
    title: "a.shadow-hover, .text-muted.bold-600, a"
    date: ".text-muted, div.px-2 div"
    document_link: 'a[href$=".pdf"], a[href*="/uploads/publications/"], a[href*="/uploads/files/"]'
    pagination: ".pagination a, a.next" 
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
      - "/uploads/publications/"
      - "/uploads/files/"
      - "/uploads/speeches/docs/"
    url_patterns:
      - "vpo.go.tz/uploads/publications/sw-*.pdf"
      - "vpo.go.tz/uploads/files/*.pdf"
      - "vpo.go.tz/uploads/speeches/docs/*.pdf"

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
      Documents use sw-{timestamp}-{filename}.pdf pattern in /uploads/publications/. Also /uploads/files/ and /uploads/speeches/docs/. Link text contains date (e.g. 22nd Jun 2020) and title. Bootstrap card grid layout.

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
  twitter: "vpo_tanzania"
  instagram: "ofisi_ya_makamu_wa_rais"

notes: |
  Permanent Secretary,
The Office of Vice President, 
Government City
P. O. Box 2502,
 Dodoma, Tanzania
+(255) (26) 232 9006 | Katibu Mkuu,
Ofisi ya Makamu wa Rais, 
Mji wa Serikali, 
Eneo la Mtumba,
P. O. Box 2502,
Dodoma, Tanzania
---

# VPO |   Mwanzo

**Category:** Government Agency
**Website:** https://www.vpo.go.tz/
**Tender Page:** https://www.vpo.go.tz/publications/tender
**Keywords Found:** bid, procurement, tender, zabuni

## Contact Information
- Email: ps@vpo.go.tz
- Phone: 026
         
- Phone: 026 2329007
- Phone: 021
         
- Phone: 024
         
- Phone: 025
         

## Scraping Instructions

**Strategy:** Scrape https://www.vpo.go.tz/publications/tender for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get

Permanent Secretary,
The Office of Vice President, 
Government City
P. O. Box 2502,
 Dodoma, Tanzania
+(255) (26) 232 9006 | Katibu Mkuu,
Ofisi ya Makamu wa Rais, 
Mji wa Serikali, 
Eneo la Mtumba,
P. O. Box 2502,
Dodoma, Tanzania

### Tender Content Preview

> s='list-inline-item d-none d-lg-block'> Zabuni Mkataba wa Hu

### Known Tender URLs

- https://www.vpo.go.tz/publications/tender

### Document Links Found

- https://www.vpo.go.tz/uploads/publications/sw-1677318093-Utaratibu wa Vikao vya Pamoja vya SJMT na SMZ vya kushughulikia masuala ya Muungano.pdf
- https://www.vpo.go.tz/uploads/speeches/docs/sw-1746676136-Statement By Of The United Republic Of Tanzania At The Copenhagen Climate Ministerial Summit - Copenhagen, Denmark, 7-8 May, 2025.pdf
- https://www.vpo.go.tz/uploads/speeches/docs/sw-1738812847-Workshop On Nexus Between Agriculture And Climate Change                 .pdf
- https://www.vpo.go.tz/uploads/publications/sw-1715925778-en-1674038035-National Carbon Trade Guidelines-2.pdf
- https://www.vpo.go.tz/uploads/publications/sw-1676617173-Sheria ya Mfuko wa Jimbo.pdf
- https://www.vpo.go.tz/uploads/publications/sw-1677317757-Mwongozo wa Vikao vya  Kuimarisha Ushirikiano wa Wizara, Idara na Taasisi ziziso za Muungano za SjMT na SMZ.pdf
- https://www.vpo.go.tz/uploads/publications/sw-1592644741-NATIONAL-GUIDELINES-FOR-STRATEGIC-ENVIRONMENTAL-ASSESSMENT.pdf
- https://www.vpo.go.tz/uploads/publications/sw-1733133094-Tanzania Investment Guide on Waste Management 2020.pdf
- https://www.vpo.go.tz/uploads/publications/sw-1714072820-Miaka 60 ya Ofisi ya Makamu wa Rais.pdf
- https://www.vpo.go.tz/uploads/speeches/docs/sw-1770647737-HOTUBA - MPANGO WA USHIRIKIAO WA ELIMU NA VIWANDA .pdf

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

Known document paths: /uploads/files/Customer%20Service%20Charter.pdf, /uploads/publications/sw-1592666339-GUIDELINES-FOR-PREPARATION-ON-ENVIRONMENT-ACTION-PLANS-FOR-SECTOR-MINISTRIES-AND-LOCAL-GOVERNMENT-AUTHORITIES.pdf, /uploads/publications/sw-1592644741-NATIONAL-GUIDELINES-FOR-STRATEGIC-ENVIRONMENTAL-ASSESSMENT.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
vpo/
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
- **Signal Strength:** Strong (procurement, tender, zabuni)
