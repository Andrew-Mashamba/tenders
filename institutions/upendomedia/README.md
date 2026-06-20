---
institution:
  name: "Upendo News Portal"
  slug: "upendomedia"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://upendomedia.co.tz/"
  tender_url: "https://upendomedia.co.tz/"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://upendomedia.co.tz/ for tender/procurement notices."
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

contact:
  email: "newsportal@upendomedia.co.tz"
  phone: "+255769181984"

notes: |
  Upendo News Portal — digital news/media site. No procurement section. Sell opportunity for CMS, digital publishing, or ICT services.
