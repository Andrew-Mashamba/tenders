---
institution:
  name: "St. Augustine University of Tanzania (SAUT)"
  slug: "saut"
  category: "Educational Institution"
  status: "active"
  country: "Tanzania"
  domain: "saut.ac.tz"

website:
  homepage: "https://saut.ac.tz/"
  tender_url: "https://saut.ac.tz/"

contact:
  email: "sautmalimbe@saut.ac.tz"
  phone: "026-10-19"

scraping:
  enabled: false
  method: "http_get"
  strategy: "DISABLED: saut.ac.tz returns 403 Forbidden to curl/bots (2026-03-15). Site has Announcements with PDFs at /saut_website/public/storage/pdfFile/ and /storage/downloadsPdf/. If access is fixed, use .announcement-item or similar for tender/notice items."
  selectors:
    container: ".announcements, .content, main"
    tender_item: ".announcement-item, article, .card"
    title: "h4, h5, .title, a"
    date: ".date, time"
    document_link: 'a[href$=".pdf"], a[href*="/storage/"]'
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

    url_patterns:
      - "saut.ac.tz/storage/downloadsPdf/qec0GioTPwY1LCaPBSlIauTKRzgerqfwiB61gSvu.pdf"
      - "saut.ac.tz/storage/downloadsPdf/V0r7gnLMIiI4IWI2c5XNMfswbTLkZjnqDCJj1mMC.pdf"
      - "saut.ac.tz/storage/prospectusPdf/23XWmvKcEhwlvNnNIH5evdM44NGxWXmJoHD8jey2.pdf"
      - "saut.ac.tz/storage/pdfFile/VjHLyYJGWTst2HE7jaPmsvBSJF1wEAa2BPlxBtzZ.pdf"
      - "saut.ac.tz/storage/pdfFile/aS5eFIvVvfsRvOjifLlm6xaCkpPDDjNUrJL26Qjq.pdf"

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
      Known paths: /saut_website/public/storage/pdfFile/, /storage/downloadsPdf/, /storage/prospectusPdf/. Site blocks curl (403). Announcements include 'Invitation To Tender' - PDFs in storage with hash filenames.

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
  instagram: "saut_mwanza"

notes: |
  St. Augustine University of Tanzania (SAUT) offers a variety of undergraduate and postgraduate programs, fostering a supportive learning environment. Join us to achieve your academic aspirations.
---

# The St. Augustine University of Tanzania | SAUT

**Category:** Educational Institution
**Website:** https://saut.ac.tz/
**Tender Page:** https://saut.ac.tz/
**Keywords Found:** eoi, procurement, rfi, supply, tender

## Contact Information
- Email: sautmalimbe@saut.ac.tz
- Phone: 026-10-19
- Phone: 026-05-11
- Phone: 026-08-18
- Phone: 026-03-21
- Phone: 026-05-12

## Scraping Instructions

**Strategy:** Scrape https://saut.ac.tz/ for tender/procurement notices.
**Method:** http_get

St. Augustine University of Tanzania (SAUT) offers a variety of undergraduate and postgraduate programs, fostering a supportive learning environment. Join us to achieve your academic aspirations.

### Tender Content Preview

> class="fa fa-columns"> Diploma in Procurement and Supply Chain Management <a href="https://saut.ac.tz/programme-details/41"

### Document Links Found

- https://saut.ac.tz/saut_website/public/storage/pdfFile/vm45a782oswCQYIGFMNBwZLM4mSIygQ9APlIQGy2.pdf
- https://saut.ac.tz/saut_website/public/storage/downloadsPdf/qec0GioTPwY1LCaPBSlIauTKRzgerqfwiB61gSvu.pdf
- https://saut.ac.tz/saut_website/public/storage/pdfFile/VjHLyYJGWTst2HE7jaPmsvBSJF1wEAa2BPlxBtzZ.pdf
- https://saut.ac.tz/saut_website/public/storage/prospectusPdf/23XWmvKcEhwlvNnNIH5evdM44NGxWXmJoHD8jey2.pdf
- https://saut.ac.tz/saut_website/public/storage/pdfFile/aS5eFIvVvfsRvOjifLlm6xaCkpPDDjNUrJL26Qjq.pdf
- https://saut.ac.tz/saut_website/public/storage/downloadsPdf/Lfa53PSjfnpeMKwJv9eLiYf58dGCHaqjUcS97iBF.pdf
- https://saut.ac.tz/saut_website/public/storage/pdfFile/YFjmk7FgDYm6QwVwPX4KaiMydyOpWejSHfZV312G.pdf
- https://saut.ac.tz/saut_website/public/storage/pdfFile/KZgqvLXfMshakKxtyLq8hqKjpS0PzhaKHoT8Y9EL.pdf
- https://saut.ac.tz/saut_website/public/storage/pdfFile/GdKisskS7rR9cUDrHRVKQZpdRIj7iaKJLdxWKZk2.pdf
- https://saut.ac.tz/saut_website/public/storage/pdfFile/yOvR02ayDE0OMfgIFtLccQnY0zDzl9wSJEnNXjM0.pdf

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

Known document paths: /storage/downloadsPdf/qec0GioTPwY1LCaPBSlIauTKRzgerqfwiB61gSvu.pdf, /storage/downloadsPdf/V0r7gnLMIiI4IWI2c5XNMfswbTLkZjnqDCJj1mMC.pdf, /storage/prospectusPdf/23XWmvKcEhwlvNnNIH5evdM44NGxWXmJoHD8jey2.pdf

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
saut/
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
- **Signal Strength:** Strong (eoi, procurement, tender)
