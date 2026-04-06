---
institution:
  name: "AfyaDepo Platform"
  slug: "afyadepot"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "afyadepot.co.tz"

website:
  homepage: "https://afyadepot.co.tz/"
  tender_url: "https://afyadepot.co.tz/"

contact:
  phone: "0 224 0 80 64"

scraping:
  enabled: true
  method: "http_get"
  strategy: "WordPress/WooCommerce/Elementor site. Scrape pharma-distribution-partnership page for B2B documents. Homepage shows 'Loading AfyaDepo' - may require JS for full render. Check /pharma-distribution-partnership/ and /bulk_supply/ for procurement docs."
  selectors:
    container: ".elementor-widget-wrap, .elementor-section, main, .entry-content, .ast-container"
    tender_item: "article, .elementor-element, .woocommerce-loop-product"
    title: "h2, h3, h4, .elementor-heading-title, .product_title"
    date: ".elementor-post-date, .date, time"
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

    known_document_paths:
      - "/wp-content/uploads/"
    url_patterns:
      - "afyadepot.co.tz/wp-content/uploads/*.pdf"
      - "afyadepot.co.tz/pharma-distribution-partnership/*"

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
      WordPress/WooCommerce. Documents in /wp-content/uploads/ (e.g. /2025/12/be-a-partner-afyadepo.pdf). B2B/Manufacturer partnership brochure. Site may use JS for initial load. Check pharma-distribution-partnership and bulk_supply pages.

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
  facebook: "afyadepo"
  linkedin: "afyadepo"
  instagram: "afyadepo"

notes: |
  Organization website at afyadepot.co.tz. Tender keywords detected: bid, procurement, rfi, supply, tender.
---

# AfyaDepo Platform &#8211; Enhancing Healthcare Accessibility

**Category:** Commercial / Private Sector
**Website:** https://afyadepot.co.tz/
**Tender Page:** https://afyadepot.co.tz/
**Keywords Found:** bid, procurement, rfi, supply, tender

## Contact Information
- Email: flags@2x.png
- Phone: 0 224 0 80 64
- Phone: 072 56-56
- Phone: 0 509 901 552 8
- Phone: 0588235294118
- Phone: 072 56 56 56

## Scraping Instructions

**Strategy:** Scrape https://afyadepot.co.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> et tri=1, exp=[], sgn=""; if(weeks<=13){tri=1;exp=["Morning nausea & fatigue", "Breast tenderness", "Hormonal shifts"];sgn="Early nutritional support and folic acid are vital.";} else if(weeks<=27){tri=2;exp=["Feeling fetal movement", "Increased energy", "Visible bump growt

### Document Links Found

- https://afyadepot.co.tz/wp-content/uploads/2025/12/be-a-partner-afyadepo.pdf

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

Known document paths: /wp-content/uploads/2025/12/be-a-partner-afyadepo.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
afyadepot/
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
- **Signal Strength:** Strong (procurement, tender)
