---
institution:
  name: "Urban Mega Store"
  slug: "urbanmegastore"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://urbanmegastore.co.tz/"
  tender_url: "https://urbanmegastore.co.tz/"

scraping:
  enabled: false
  method: "http_get"
  strategy: "Site returns login page only; no public tender/procurement content. Homepage redirects to admin login."
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
  Site returns login page only; no public content. Disabled until public tender section exists.
