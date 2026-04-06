---
institution:
  name: "Ol Mesera African Restaurant"
  slug: "olmesera"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "olmesera.co.tz"

website:
  homepage: "https://olmeserarestaurant.com/"
  tender_url: "https://olmeserarestaurant.com/"

contact:
  email: "info@olmeserarestaurant.com"
  phone: "08439526190"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Restaurant website. 'Tender' in content refers to food (tender beef). Menu PDFs only; no procurement tenders."
  selectors:
    container: ".entry-content, .et_pb_section, main"
    tender_item: ".et_pb_module, .et_pb_row"
    title: ".et_pb_module, h2, h3"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"]'
    pagination: null
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
      - "olmeserarestaurant.com/wp-content/uploads/*/Olmesera*.pdf"
      - "olmeserarestaurant.com/wp-content/uploads/*/OlMesera*.pdf"

    known_document_paths:
      - "/wp-content/uploads/2025/12/"
      - "/wp-content/uploads/2024/03/"

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
      Restaurant menus only. /wp-content/uploads/YYYY/MM/ for menu PDFs. No procurement tenders.

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
  facebook: "olmeserarestaurant"
  instagram: "olmesera"

notes: |
  At Olmesera, we blend local Tanzanian recipes with contemporary twists, creating a menu that delights with both comfort and originality.
---

# Ol Mesera African Restaurant - Traditional Tanzanian Cuisine With Modern Flair

**Category:** Commercial / Private Sector
**Website:** https://olmeserarestaurant.com/
**Tender Page:** https://olmeserarestaurant.com/
**Keywords Found:** rfi, tender

## Contact Information
- Email: info@olmeserarestaurant.com
- Phone: 08439526190
- Phone: 025-12-22
- Phone: 09266968166
- Phone: 024-01-11
- Phone: 026-03-11 23

## Scraping Instructions

**Strategy:** Scrape https://olmeserarestaurant.com/ for tender/procurement notices.
**Method:** http_get

At Olmesera, we blend local Tanzanian recipes with contemporary twists, creating a menu that delights with both comfort and originality.

### Tender Content Preview

> pb_text_align_left et_pb_bg_layout_light"> Tender beef short rib, slow-braised and then grilled for an irresistible smoky flavor. <div class="et_pb_module et_pb_divider et_pb_divider_0 et_pb_divider_position_center et_p

### Document Links Found

- https://olmeserarestaurant.com/wp-content/uploads/2025/12/Olmesera_Menu-2025.pdf
- https://olmeserarestaurant.com/wp-content/uploads/2024/03/OlMesera_Menu_2024.pdf

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

Known document paths: /wp-content/uploads/2025/12/Olmesera_Menu-2025.pdf, /wp-content/uploads/2024/03/OlMesera_Menu_2024.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
olmesera/
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
