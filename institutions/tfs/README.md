---
institution:
  name: "Tanzania Forest Services Agency"
  slug: "tfs"
  category: "Government Agency"
  status: "active"
  country: "Tanzania"
  domain: "tfs.go.tz"

website:
  homepage: "https://www.tfs.go.tz/"
  tender_url: "https://www.tfs.go.tz/resources/documents"

contact:
  email: "mpingo@tfs.go.tz"
  phone: "003197715"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://www.tfs.go.tz/resources/documents - table lists documents with Date, Title, Category, Size, Download. Each row has direct PDF link in uploads/documents/. Follow detail page links for full tender info."
  selectors:
    container: ".post_docs_block, #atable, table.table-striped"
    tender_item: "#atable tbody tr"
    title: "td:nth-child(2) a[href*='resources/documents']"
    date: "td:nth-child(1) nobr, td:first-child"
    document_link: 'td a[href$=".pdf"], td a[href*="uploads/documents"]'
    pagination: ""
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
      - "tfs.go.tz/uploads/documents/*.pdf"

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
      Documents at https://www.tfs.go.tz/uploads/documents/. Table rows have malformed hrefs (sometimes "https://www.tfs.go.tz/ https://www.tfs.go.tz/uploads/...") - extract second URL. Download column has direct PDF links.

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
  instagram: "tanzania_forest"

notes: |
  Organization website at tfs.go.tz. Tender keywords detected: rfi, supply, tender.
---

# Tanzania Forest Services Agency

**Category:** Government Agency
**Website:** https://www.tfs.go.tz/
**Tender Page:** https://www.tfs.go.tz/resources/documents/view/extension_of_tender_no_tr47_2025_2026_afd_c_01_consultancy_services_for_provision_of_environmental_biodiversity_and_social_assessment_for_silayo_mtibwapagale_and_winoifinga_forest_plantations
**Keywords Found:** rfi, supply, tender

## Contact Information
- Email: mpingo@tfs.go.tz
- Phone: 003197715
- Phone: 026-03-12

## Scraping Instructions

**Strategy:** Scrape https://www.tfs.go.tz/resources/documents/view/extension_of_tender_no_tr47_2025_2026_afd_c_01_consultancy_services_for_provision_of_environmental_biodiversity_and_social_assessment_for_silayo_mtibwapagale_and_winoifinga_forest_plantations for government tender notices. Government sites often post zabuni/manunuzi.
**Method:** http_get



### Known Tender URLs

- https://www.tfs.go.tz/resources/documents/view/extension_of_tender_no_tr47_2025_2026_afd_c_01_consultancy_services_for_provision_of_environmental_biodiversity_and_social_assessment_for_silayo_mtibwapagale_and_winoifinga_forest_plantations

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
tfs/
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

- **Last Checked:** 15 March 2026
- **Active Tenders:** 1 (TFS-2026-003 consultancy; auction notices excluded)
- **Signal Strength:** Strong (tender)
