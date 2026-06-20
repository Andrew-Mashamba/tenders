---
institution:
  name: "UIS – Change with technology"
  slug: "unitedinfrastructures"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"

website:
  homepage: "https://unitedinfrastructures.co.tz/"
  tender_url: "https://unitedinfrastructures.co.tz/"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape https://unitedinfrastructures.co.tz/ for tender/procurement notices."
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
  email: "info@unitedinfrastructures.co.tz"
  phone: "+255715123550"

notes: |
  UIS (United Infrastructure Solutions) — ICT infrastructure company (CCTV, IP-PBX, fire alarm, video conferencing). No procurement/tender section on site. Partner/sell opportunity for Zima ICT services. Emails: info@unitedinfrastructures.co.tz, sales@unitedinfrastructures.co.tz.
