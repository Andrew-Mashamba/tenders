#!/usr/bin/env python3
"""Create README.md for institutions that lack them."""
import os
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
INST = PROJECT / "institutions"

INSTITUTIONS = [
    ("unitedinfrastructures", "UIS – Change with technology", "https://unitedinfrastructures.co.tz/"),
    ("unity", "Abya Travel Tours & Safaris", "https://unity.co.tz/"),
    ("untamedsafaris", "Untamed East Africa Safaris", "https://untamedsafaris.co.tz/"),
    ("upendomedia", "Upendo News Portal", "https://upendomedia.co.tz/"),
    ("urasaccos", "URA SACCOS LTD", "https://urasaccos.co.tz/"),
    ("urbanmegastore", "Urban Mega Store", "https://urbanmegastore.co.tz/"),
    ("ursa", "URSA Tanzania", "https://ursa.co.tz/"),
    ("urusecondary", "Uru Secondary School", "https://urusecondary.sc.tz/"),
    ("ushirika", "Tanzania Federation of Co-operatives (TFC)", "https://ushirika.co.tz/"),
    ("ussl", "Union Service Stores Co. Ltd", "https://ussl.co.tz/"),
    ("utegitechnical", "Utegi Technical Enterprises", "https://utegitechnical.co.tz/"),
    ("utel", "Utel Global", "https://utel.co.tz/"),
    ("utpc", "Union of Tanzania Press Clubs", "https://utpc.or.tz/"),
    ("uttamis", "UTT AMIS", "https://uttamis.co.tz/"),
    ("utumefmradio", "Utume Fm Radio", "https://utumefmradio.co.tz/"),
    ("utv", "UTV", "https://utv.co.tz/"),
    ("uwezofinancial", "Uwezo Financial Services", "https://uwezofinancial.co.tz/"),
    ("uwodo", "Uwodo", "https://uwodo.or.tz/"),
    ("uwp", "UWP Consulting Limited", "https://uwp.co.tz/"),
    ("valleyviewschools", "Valley View English Medium School", "https://valleyviewschools.ac.tz/"),
    ("vaniagroup", "Vania Group Limited", "https://vaniagroup.co.tz/"),
    ("vcc", "Victory Christian Centre Tabernacle", "https://vcc.or.tz/"),
]

TEMPLATE = '''---
institution:
  name: "{name}"
  slug: "{slug}"
  category: "Commercial / Private Sector"
  status: "active"
  country: "Tanzania"

website:
  homepage: "{url}"
  tender_url: "{url}"

scraping:
  enabled: true
  method: "http_get"
  strategy: "Scrape {url} for tender/procurement notices."
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
'''

def main():
    for slug, name, url in INSTITUTIONS:
        d = INST / slug
        if not d.exists():
            continue
        readme = d / "README.md"
        if readme.exists():
            continue
        content = TEMPLATE.format(slug=slug, name=name, url=url.rstrip("/") + "/")
        readme.write_text(content, encoding="utf-8")
        print(f"Created {readme}")

if __name__ == "__main__":
    main()
