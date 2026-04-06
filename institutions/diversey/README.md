---
institution:
  name: "Solenis (formerly Diversey)"
  slug: "diversey"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"
  domain: "diversey.co.tz"

website:
  homepage: "https://www.solenis.com/"
  tender_url: "https://www.solenis.com/link/5723ead4cf9044cca31ead1849606616.aspx?type=procurement"

contact:
  email: "registration.coupa@solenis.com"
  alternate_emails:
    - "outreach-requests@taulia.com"
  phone: "037 886 698"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Procurement URL redirects to Sustainability & Regulatory Library. Filter by Category=Procurement returns 0 results. Page lists policy/certification PDFs. Scrape document cards; filter for Procurement category. Documents at /globalassets/resources/sustainability--regulatory-library/*.pdf. No traditional tender listings."
  selectors:
    container: ".sustainability-layout, main, .results-container"
    tender_item: "a[href$='.pdf'], .document-card, .result-item"
    title: "h5, h6, .document-title, a"
    date: ".date, time"
    document_link: 'a[href$=".pdf"]'
    pagination: ".pagination a, a.next"
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
      - "/globalassets/resources/sustainability--regulatory-library/"
      - "/globalassets/resources/supplier-documents/"

    url_patterns:
      - "solenis.com/globalassets/resources/sustainability--regulatory-library/*.pdf"
      - "solenis.com/globalassets/resources/supplier-documents/*.pdf"

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
      Procurement filter returns 0 results. Library has policy/certification PDFs. Document paths: /globalassets/resources/sustainability--regulatory-library/, /globalassets/resources/supplier-documents/. Page uses filters (Industry, Topic, Category) - Procurement category empty. Consider scraping for supplier registration info.

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
  facebook: "Solenis-285432878481907"
  twitter: "TeamSolenis"
  linkedin: "solenis"
  instagram: "solenis.llc"

notes: |
  Our suppliers help us to meet the needs of our customers with responsibly produced products and services. Learm more about our suppliers.
---

# Quality Chemical Products & Services Suppliers | Solenis

**Category:** Commercial / Private Sector
**Website:** https://www.solenis.com/
**Tender Page:** https://www.solenis.com/link/5723ead4cf9044cca31ead1849606616.aspx?type=procurement
**Keywords Found:** procurement, supply

## Contact Information
- Email: registration.coupa@solenis.com
- Email: outreach-requests@taulia.com
- Phone: 037 886 698
- Phone: 0215 1022
- Phone: 01901767-944
- Phone: 0 0 177 40
- Phone: 0467836 36

## Scraping Instructions

**Strategy:** Scrape https://www.solenis.com/link/5723ead4cf9044cca31ead1849606616.aspx?type=procurement for tender/procurement notices.
**Method:** http_get

Our suppliers help us to meet the needs of our customers with responsibly produced products and services. Learm more about our suppliers.

### Tender Content Preview

> Solenis is partnering with Coupa to launch a new procurement program that will improve efficiencies and help get you paid faster.&nbsp;Once we launch our new program, all purchase orders, invoices, and payments will be handled electronically using t

### Known Tender URLs

- https://www.solenis.com/link/5723ead4cf9044cca31ead1849606616.aspx?type=procurement

### Document Links Found

- https://www.solenis.com/globalassets/resources/supplier-documents/company-information---solenis-taiwan-for-local-suppliers.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/for-suppliers-docs/for-suppliers---how-to-view-a-purchase-order.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/company-information---solenis-taiwan-for-overseas-suppliers.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/w-9-form-for-solenis-llc.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/billing-and-invoice-standards---latin-america-english.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/billing-and-invoice-standards---latin-america-portuguese.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/billing-and-invoice-standards---europe.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/billing-and-invoice-standards---latin-america-spanish.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/2025.08.06-supplier-th-qa.pdf
- https://www.solenis.com/globalassets/resources/supplier-documents/for-suppliers-docs/for-suppliers---how-a-purchase-order-is-structured-in-coupa.pdf

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
diversey/
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
