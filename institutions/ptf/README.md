---
institution:
  name: "Presidential Trust Fund for Self Reliance - Mfuko wa Rais wa Kujitegemea"
  slug: "ptf"
  category: "NGO / Non-Profit Organization"
  status: "active"
  country: "Tanzania"
  domain: "ptf.or.tz"

website:
  homepage: "https://www.ptf.or.tz/"
  tender_url: "https://www.ptf.or.tz/"

contact:
  phone: "+255 22 2760450"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape ptf.or.tz homepage and /habari-na-matukio/ (News & Events). WordPress site. Slider mentions 'Mkopo wa Zabuni' (tender loans). News/blog items in .blog_slider_ul. Check /mikopo/ (Loans) for tender-related content. No dedicated tender listing found."
  selectors:
    container: ".blog_slider_ul, .Latest_news ul, #Content, .sections_group"
    tender_item: ".blog_slider_ul li, .post-item, .Latest_news ul li, article"
    title: "h4 a, h2.entry-title, .desc h4, .post-title"
    date: ".date_label, .date, .closing-date, .published, time, .post-date"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a, .pager .pages a" 
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
      - "ptf.or.tz/wp-content/uploads/*.pdf"
      - "ptf.or.tz/habari-na-matukio/*"
      - "ptf.or.tz/mikopo/*"

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
      WordPress site. Documents in /wp-content/uploads/ (e.g. /2017/11/, /2018/10/). News at /habari-na-matukio/. 'Mkopo wa Zabuni' (tender loans) in slider - check /mikopo/ for loan/tender info.

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
  facebook: "mfukowarais"
  twitter: "mfukowarais"
  instagram: "mfukowarais"

notes: |
  Organization website at ptf.or.tz. Tender keywords detected: bid, rfi, zabuni.
---

# Presidential Trust Fund for Self Reliance &#8211; Mfuko wa Rais wa Kujitegemea

**Category:** NGO / Non-Profit Organization
**Website:** https://www.ptf.or.tz/
**Tender Page:** https://www.ptf.or.tz/
**Keywords Found:** bid, rfi, zabuni

## Contact Information
- Phone: +255 22 2760450
- Phone: +255 738 752 425

## Scraping Instructions

**Strategy:** Scrape https://www.ptf.or.tz/ for tender/procurement notices.
**Method:** http_get



### Tender Content Preview

> ight: 65px; font-weight: 300; color: #ffffff; letter-spacing: 0px;font-family:Poppins;"> Mkopo wa Zabuni var htmlDiv = document.getElementById("rs-plugin-settings-inline-css"); var htmlDivCss=""; if(htmlDiv) { htmlDiv.innerHTML = htmlDiv.innerHTML + h

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
ptf/
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
- **Signal Strength:** Strong (zabuni)
