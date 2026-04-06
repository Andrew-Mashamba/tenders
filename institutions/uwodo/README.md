---
institution:
  name: "Uwodo"
  slug: "uwodo"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://uwodo.or.tz/"
  tender_url: "https://uwodo.or.tz/"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://uwodo.or.tz/ for tender/procurement notices."
  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a"
  schedule: "daily"
  anti_bot:
    requires_javascript: false
    has_captcha: false
    rate_limit_seconds: 10
  documents:
    download_enabled: true
    file_types: [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar"]
  output:
    format: "json"
    fields: [tender_id, title, description, published_date, closing_date, document_links, contact_info]

notes: |
  Scrape homepage for tenders/procurement. If none found, identify opportunities and add to leads.
