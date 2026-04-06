---
institution:
  name: "Chai Bora - Kilele Cha Ubora"
  slug: "chaibora"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "chaibora.co.tz"

website:
  homepage: "https://chaibora.co.tz/"
  tender_url: "https://chaibora.co.tz/"

contact:
  email: "info@chaibora.co.tz"
  phone: "09819 100"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Chai Bora is a tea/coffee company (WooCommerce). The 'rfq' keyword comes from WooCommerce RFQ plugin for product quotes, not procurement tenders. No dedicated tender page. Disabled until tender content is identified."
  selectors:
    container: ".content, main, .entry-content, .page-content"
    tender_item: ".product, .woocommerce-loop-product"
    title: "h2, h3, .product-title"
    date: null
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"]'
    pagination: ".woocommerce-pagination, .pagination"
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
      No tender/procurement content found. Site is e-commerce (tea, coffee, sauces). RFQ plugin is for product quotes. Re-enable if tender page is added.

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
  facebook: "chaiboraltdtz"
  twitter: "ChaiBora"
  instagram: "chaiboraltd"

notes: |
  Organization website at chaibora.co.tz. Tender keywords detected: rfq.
---

# Chai Bora &#8211; Kilele Cha Ubora

**Category:** Commercial / Private Sector
**Website:** https://chaibora.co.tz/
**Tender Page:** https://chaibora.co.tz/wp-content/plugins/woo-rfq-for-woocommerce/gpls_assets/css/gpls_wh.css?ver=70792
**Keywords Found:** rfq

## Contact Information
- Email: info@chaibora.co.tz
- Phone: 09819 100
- Phone: 04352 100

## Scraping Instructions

**Strategy:** Scrape https://chaibora.co.tz/wp-content/plugins/woo-rfq-for-woocommerce/gpls_assets/css/gpls_wh.css?ver=70792 for tender/procurement notices.
**Method:** http_get



### Known Tender URLs

- https://chaibora.co.tz/wp-content/plugins/woo-rfq-for-woocommerce/gpls_assets/css/gpls_wh.css?ver=70792
- https://chaibora.co.tz/wp-content/plugins/woo-rfq-for-woocommerce/gpls_assets/css/gpls_woo_rfq.css?ver=74539

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
chaibora/
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
- **Signal Strength:** Strong (rfq)
