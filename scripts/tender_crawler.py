#!/usr/bin/env python3
"""
Fast Tender Discovery Crawler
==============================
Scans 10,000+ Tanzanian domains for tender/procurement content.
Pure async HTTP — no AI, no tokens. Designed for max speed.

Usage:
  # Full scan (auto-splits into parallel workers)
  python3 tender_crawler.py

  # Run specific chunk (for manual parallelism)
  python3 tender_crawler.py --chunk 0 --chunks 4    # Worker 0 of 4
  python3 tender_crawler.py --chunk 1 --chunks 4    # Worker 1 of 4

  # Launch N parallel workers automatically
  python3 tender_crawler.py --workers 8

  # Phase 2: Deep crawl hits from Phase 1
  python3 tender_crawler.py --deep

  # Phase 3: Cleanup misses
  python3 tender_crawler.py --cleanup

  # Dry run (no folder changes)
  python3 tender_crawler.py --dry-run
"""

import asyncio
import aiohttp
import aiohttp.resolver
import ssl
import warnings
warnings.filterwarnings('ignore')
# Suppress noisy DNS errors from dead domains
import logging as _logging
_logging.getLogger('asyncio').setLevel(_logging.CRITICAL)
_logging.getLogger('aiohttp').setLevel(_logging.CRITICAL)
import os
import re
import json
import sys
import time
import shutil
import signal
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser

# ─── Config ───────────────────────────────────────────────────────────────────

BASE_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
INSTITUTIONS_DIR = BASE_DIR / "institutions"
DOMAINS_FILE = INSTITUTIONS_DIR / "tz.txt"
RESULTS_DIR = BASE_DIR / "scripts" / ".crawler_results"
HITS_FILE = RESULTS_DIR / "hits.jsonl"
MISSES_FILE = RESULTS_DIR / "misses.txt"
ERRORS_FILE = RESULTS_DIR / "errors.txt"
PROGRESS_FILE = RESULTS_DIR / "progress.json"

CONCURRENCY = 30            # Connections per worker (lower to avoid DNS overload)
CONNECT_TIMEOUT = 10        # Seconds
READ_TIMEOUT = 20           # Seconds
MAX_BODY = 500_000          # 500KB max per page read
MAX_URLS_PER_DOMAIN = 6     # Homepage + 5 tender paths

# Tender keywords — lowercase
KEYWORDS = {
    # English
    'tender', 'tenders', 'procurement', 'rfp', 'rfq',
    'request for proposal', 'request for quotation',
    'expression of interest', 'prequalification',
    'invitation to bid', 'invitation to tender',
    'invitation for tender', 'invitation for bid',
    'competitive quotation', 'call for proposal',
    'bid document', 'bid submission', 'bidding document',
    'procurement notice', 'tender notice',
    # Swahili
    'zabuni', 'manunuzi', 'tangazo la zabuni',
    'mwaliko wa zabuni', 'ununuzi',
}

# Single-word keywords for fast first-pass check
FAST_KEYWORDS = {'tender', 'tenders', 'procurement', 'rfp', 'rfq',
                 'zabuni', 'manunuzi', 'prequalification', 'bidding'}

# Paths to probe after homepage
TENDER_PATHS = [
    '/tenders', '/tender', '/procurement', '/zabuni',
    '/en/tenders', '/about-us/tender', '/rfp',
]

DOC_EXTENSIONS = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip')


# ─── Fast HTML Parser (no BeautifulSoup needed) ──────────────────────────────

class LinkExtractor(HTMLParser):
    """Extract links and title from HTML without external dependencies."""
    def __init__(self):
        super().__init__()
        self.links = []
        self.doc_links = []
        self.title = ""
        self._in_title = False
        self.emails = []

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self._in_title = True
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                self.links.append(href)
                if any(href.lower().endswith(ext) for ext in DOC_EXTENSIONS):
                    self.doc_links.append(href)

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def error(self, message):
        pass


def scan_text(text: str) -> list[str]:
    """Fast keyword scan. Returns matched keywords."""
    lower = text.lower()
    # Quick check — if no fast keywords, skip detailed scan
    if not any(kw in lower for kw in FAST_KEYWORDS):
        return []
    return [kw for kw in KEYWORDS if kw in lower]


def extract_emails(text: str) -> list[str]:
    """Extract email addresses from text."""
    return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))


def extract_info(html: str, base_url: str) -> dict:
    """Extract links, title, emails from HTML."""
    parser = LinkExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Resolve relative URLs
    full_links = []
    full_doc_links = []
    for href in parser.links:
        try:
            full = urljoin(base_url, href)
            full_links.append(full)
        except Exception:
            pass
    for href in parser.doc_links:
        try:
            full_doc_links.append(urljoin(base_url, href))
        except Exception:
            pass

    emails = extract_emails(html)

    return {
        'title': parser.title.strip()[:200],
        'links': full_links,
        'doc_links': full_doc_links,
        'emails': emails,
    }


# ─── Domain Scanner ──────────────────────────────────────────────────────────

async def fetch(session: aiohttp.ClientSession, url: str) -> tuple[str, int]:
    """Fetch URL, return (body, status). Returns ('', 0) on failure."""
    try:
        async with session.get(url, allow_redirects=True, timeout=aiohttp.ClientTimeout(
                total=READ_TIMEOUT, connect=CONNECT_TIMEOUT)) as resp:
            if resp.status in (200, 301, 302):
                body = await resp.text(encoding=None, errors='ignore')
                return body[:MAX_BODY], resp.status
            return '', resp.status
    except Exception:
        return '', 0


async def try_url(session: aiohttp.ClientSession, domain: str, path: str = '') -> tuple[str, str]:
    """Try HTTPS then HTTP for domain+path. Returns (body, full_url) or ('', '')."""
    for scheme in ('https', 'http'):
        url = f"{scheme}://{domain}{path}"
        body, status = await fetch(session, url)
        if body and len(body) > 300:
            return body, url
    return '', ''


async def scan_domain(session: aiohttp.ClientSession, domain: str,
                      sem: asyncio.Semaphore) -> dict:
    """Scan a single domain for tender content. Returns result dict."""
    result = {
        'domain': domain,
        'status': 'miss',
        'reachable': False,
        'keywords': [],
        'tender_url': '',
        'doc_links': [],
        'emails': [],
        'title': '',
    }

    async with sem:
        # Step 1: Try homepage
        body, url = await try_url(session, domain)
        if body:
            result['reachable'] = True
            info = extract_info(body, url)
            result['title'] = info['title']
            result['emails'] = info['emails'][:10]

            # Check homepage for keywords
            keywords = scan_text(body)
            if keywords:
                result['status'] = 'hit'
                result['keywords'] = keywords
                result['tender_url'] = url
                result['doc_links'] = info['doc_links'][:20]
                return result

            # Step 2: Probe tender paths
            for path in TENDER_PATHS:
                body2, url2 = await try_url(session, domain, path)
                if body2:
                    keywords2 = scan_text(body2)
                    if keywords2:
                        info2 = extract_info(body2, url2)
                        result['status'] = 'hit'
                        result['keywords'] = keywords2
                        result['tender_url'] = url2
                        result['doc_links'] = info2['doc_links'][:20]
                        result['emails'] = (result['emails'] + info2['emails'])[:10]
                        return result

            # Reachable but no keywords
            result['status'] = 'miss'
            return result

        # Unreachable
        result['status'] = 'error'
        return result


# ─── Institution Folder Management ───────────────────────────────────────────

def domain_to_slug(domain: str) -> str:
    """Convert domain to institution slug."""
    # Remove TLD (.co.tz, .or.tz, .go.tz, .ac.tz, etc.)
    slug = re.sub(r'\.(co|or|go|ac|ne|me|hotel|sc|mil|info)\.tz$', '', domain)
    # Clean up
    slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


def get_category(domain: str) -> str:
    """Determine institution category from domain TLD."""
    tld = domain.rsplit('.', 2)
    if len(tld) >= 2:
        tld_map = {
            'go': 'Government', 'or': 'NGO/Non-Profit', 'ac': 'Academic',
            'co': 'Commercial', 'ne': 'Network/ISP', 'mil': 'Military',
        }
        return tld_map.get(tld[-2], 'Commercial')
    return 'Unknown'


def get_institution_name(hit: dict, slug: str) -> str:
    """Extract a clean institution name from crawler hit data."""
    title = hit.get('title', '')
    if title:
        # Clean common suffixes/noise from page titles
        for sep in ['|', ' - ', ' – ', ' — ', ' :: ']:
            if sep in title:
                title = title.split(sep)[0].strip()
        # Remove "Home", "Welcome to", etc.
        title = re.sub(r'^(Home|Welcome to|Welcome)\s*[-–—:]?\s*', '', title, flags=re.IGNORECASE).strip()
        if len(title) >= 3 and len(title) <= 100:
            return title
    return slug.replace('-', ' ').title()


def generate_readme(hit: dict) -> str:
    """Generate a gold-standard README.md matching CRDB bank format."""
    slug = domain_to_slug(hit['domain'])
    category = get_category(hit['domain'])
    name = get_institution_name(hit, slug)
    tender_url = hit.get('tender_url', '')
    homepage = f"https://{hit['domain']}"
    doc_links = hit.get('doc_links', [])
    emails = [e for e in hit.get('emails', []) if not any(x in e for x in ['sentry', 'wixpress', 'webmaster@'])]
    keywords = hit.get('keywords', [])

    # Infer document paths from doc_links
    known_paths = set()
    url_patterns = []
    for link in doc_links:
        parsed = urlparse(link)
        path_dir = '/'.join(parsed.path.split('/')[:-1]) + '/'
        if path_dir and path_dir != '/':
            known_paths.add(path_dir)
        # Build URL pattern
        ext = os.path.splitext(parsed.path)[1].lower()
        if ext in ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip'):
            pattern = f"{hit['domain']}{path_dir}*{ext}"
            url_patterns.append(pattern)

    known_paths = sorted(known_paths)[:5]
    url_patterns = sorted(set(url_patterns))[:10]

    # Infer scraping strategy from what we found
    tender_path = urlparse(tender_url).path if tender_url else ''
    if tender_path and tender_path != '/':
        strategy = f'Scrape {tender_path} page for tender listings, download all linked documents.'
    elif doc_links:
        strategy = f'Scrape homepage and linked pages for tender/procurement documents. {len(doc_links)} document links discovered.'
    elif 'zabuni' in keywords or 'manunuzi' in keywords:
        strategy = 'Scrape for Swahili tender content (zabuni/manunuzi). Check for PDF links in main content area.'
    else:
        strategy = 'Scrape tender/procurement page. Identify document links and tender listings.'

    # Determine if JS might be needed (Wix, React, Angular hints)
    requires_js = False
    title_lower = (hit.get('title') or '').lower()
    if any(x in tender_url.lower() for x in ['wix', 'squarespace', 'webflow']):
        requires_js = True

    # Build known_document_paths YAML
    known_paths_yaml = ""
    if known_paths:
        known_paths_yaml = "\n    known_document_paths:\n"
        for p in known_paths:
            known_paths_yaml += f'      - "{p}"\n'

    # Build url_patterns YAML
    url_patterns_yaml = ""
    if url_patterns:
        url_patterns_yaml = "\n    url_patterns:\n"
        for p in url_patterns:
            url_patterns_yaml += f'      - "{p}"\n'

    # Build document_notes
    if known_paths:
        doc_notes = f"Documents found under {', '.join(known_paths[:3])}. Check for additional paths during scraping."
    else:
        doc_notes = "Document paths not yet confirmed. The scraper should discover document links during the first run."

    # Emails for notes
    emails_str = ', '.join(emails[:5]) if emails else 'None found yet'

    readme = f"""---
institution:
  name: "{name}"
  slug: "{slug}"
  category: "{category}"
  status: "active"
  country: "Tanzania"

website:
  homepage: "{homepage}"
  tender_url: "{tender_url}"

scraping:
  enabled: true
  method: "http_get"
  strategy: "{strategy}"
  selectors:
    container: ".tender-list, .content, main, .page-content, .entry-content, article"
    tender_item: "article, .tender-item, .card, .row, tr, li"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a"
  schedule: "daily"

  anti_bot:
    requires_javascript: {"true" if requires_js else "false"}
    has_captcha: false
    rate_limit_seconds: 10

  documents:
    download_enabled: true
    download_path: "./downloads/"
    naming: "{{{{date}}}}_{{{{title}}}}_{{{{filename}}}}"

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
{known_paths_yaml}{url_patterns_yaml}
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
      {doc_notes}

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

notes: |
  Category: {category}. Keywords found: {', '.join(keywords[:5])}.
  Emails: {emails_str}.
  Discovered by crawler on {datetime.now().strftime('%Y-%m-%d')}.
---

# {name}

**Category:** {category}
**Website:** {homepage}
**Tender Page:** {tender_url or 'To be identified by scraper'}

## Scraping Instructions

**Strategy:** {strategy}
**Method:** http_get

{f"Keywords found on site: {', '.join(keywords)}" if keywords else ""}

## Document Download Instructions

The scraper MUST download all linked documents from tender pages, not just scrape metadata.

**File types to download:** PDF, DOC, DOCX, XLS, XLSX, ZIP
**Storage:** Save to `./downloads/` within this institution folder
**Naming convention:** `{{date}}_{{title}}_{{original_filename}}`

### Key behaviors:
1. **Follow all document links** on tender listing pages and individual tender detail pages
2. **Resolve redirects** — some download links redirect through CDN or auth endpoints
3. **Decode percent-encoded URLs** (e.g., `%20` → space) for readable filenames
4. **Check for documents in iframes or embedded viewers** that may wrap a PDF URL
5. **Download attachments from detail pages** — some tenders only show a summary on the listing page with full documents on a detail/inner page
6. **Skip duplicates** based on URL and file hash to avoid re-downloading

{f"Known document paths: {', '.join(known_paths)}" if known_paths else "Document paths will be discovered during the first scrape run."}

## Folder Structure

After scraping, this institution folder MUST be organized as follows:

```
{slug}/
├── README.md                          # This file — scraper config & instructions
├── tenders/
│   ├── active/                        # Currently open tenders
│   │   ├── {{tender_id}}.json           # Structured tender metadata
│   │   └── ...
│   ├── closed/                        # Past/expired tenders (auto-moved after closing_date)
│   │   ├── {{tender_id}}.json
│   │   └── ...
│   └── archive/                       # Historical tenders older than 90 days
│       ├── {{tender_id}}.json
│       └── ...
├── downloads/
│   ├── {{tender_id}}/                   # One subfolder per tender
│   │   ├── original/                  # Raw downloaded files (never modified)
│   │   │   ├── tender_document.pdf
│   │   │   ├── specifications.docx
│   │   │   └── bill_of_quantities.xlsx
│   │   └── extracted/                 # AI-extracted text/data from documents
│   │       ├── tender_document.txt    # Plain text extraction from PDF
│   │       ├── specifications.txt
│   │       ├── summary.json           # AI-generated structured summary
│   │       └── key_dates.json         # Extracted dates & deadlines
│   └── ...
├── scrape_log.json                    # History of all scrape runs
└── last_scrape.json                   # Last scrape result snapshot
```

### Tender JSON Schema (`tenders/active/{{tender_id}}.json`)

```json
{{{{
  "tender_id": "{slug.upper()}-2026-001",
  "institution": "{slug}",
  "title": "Example Tender Title",
  "description": "Full description of the tender...",
  "reference_number": "",
  "published_date": "2026-01-01",
  "closing_date": "2026-02-01",
  "closing_time": "14:00 EAT",
  "category": "{category}",
  "status": "active",
  "source_url": "{tender_url}",
  "documents": [
    {{{{
      "filename": "tender_document.pdf",
      "original_url": "",
      "local_path": "./downloads/{slug.upper()}-2026-001/original/tender_document.pdf",
      "content_type": "application/pdf",
      "downloaded_at": ""
    }}}}
  ],
  "contact": {{{{
    "name": "Procurement Department",
    "email": "{emails[0] if emails else ''}",
    "phone": "",
    "address": ""
  }}}},
  "eligibility": "Open to all registered suppliers",
  "scraped_at": "",
  "last_checked": ""
}}}}
```

## Post-Scrape Actions

After EACH successful scrape of this institution, the scraper MUST perform these steps in order:

### 1. Organize Tenders by Status
- Parse `closing_date` from each tender JSON
- **Active:** `closing_date` is in the future → `tenders/active/`
- **Closed:** `closing_date` has passed → move from `active/` to `closed/`
- **Archive:** `closing_date` is older than 90 days → move from `closed/` to `archive/`

### 2. Extract Text from Downloaded Documents
For each new document in `downloads/{{tender_id}}/original/`:
- **PDF:** Extract full text → save to `downloads/{{tender_id}}/extracted/{{filename}}.txt`
- **DOCX:** Extract full text → save to `downloads/{{tender_id}}/extracted/{{filename}}.txt`
- **XLSX:** Extract sheet names and cell data → save as JSON
- Generate `summary.json` with AI-extracted fields

### 3. Update `last_scrape.json`
Write/overwrite with current run status.

### 4. Append to `scrape_log.json`
Append a new entry to the runs array.

### 5. Update Global Active Tenders Index
After scraping, update: `/Volumes/DATA/PROJECTS/TENDERS/institutions/active_tenders.md`

### 6. Send Email Notification
Send a summary email using config from `/Volumes/DATA/PROJECTS/TENDERS/config/email.json`
"""
    return readme


def create_institution_folder(hit: dict):
    """Create institution folder with gold-standard README.md for a hit."""
    slug = domain_to_slug(hit['domain'])
    folder = INSTITUTIONS_DIR / slug

    if folder.exists():
        # Already exists — check if README needs upgrade
        readme = folder / "README.md"
        if readme.exists():
            content = readme.read_text(errors='ignore')
            # Upgrade if it's a minimal/partial README (lacks download_rules)
            if 'download_rules:' not in content and 'allowed_content_types' not in content:
                # Regenerate with gold standard
                new_content = generate_readme(hit)
                readme.write_text(new_content)
            elif 'tender_url: ""' in content and hit.get('tender_url'):
                content = content.replace(
                    'tender_url: ""',
                    f'tender_url: "{hit["tender_url"]}"'
                )
                readme.write_text(content)
        else:
            # No README — create one
            (folder / "tenders" / "active").mkdir(parents=True, exist_ok=True)
            (folder / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
            (folder / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
            (folder / "downloads").mkdir(parents=True, exist_ok=True)
            readme.write_text(generate_readme(hit))
        return folder

    # Create new folder with full structure
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (folder / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (folder / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (folder / "downloads").mkdir(parents=True, exist_ok=True)

    (folder / "README.md").write_text(generate_readme(hit))
    return folder


def enrich_readme_with_agent(slug: str, batch: list[str] = None):
    """Use Agent CLI to visit the institution website and generate institution-specific
    CSS selectors, document paths, and scraping strategy. Updates README.md in-place."""
    agent_bin = "/Users/andrewmashamba/.local/bin/agent"
    if not os.path.isfile(agent_bin):
        print(f"  Agent CLI not found at {agent_bin}")
        return False

    if batch:
        # Batch mode: enrich multiple institutions in one agent call
        inst_list = []
        for s in batch:
            folder = INSTITUTIONS_DIR / s
            readme = folder / "README.md"
            if not readme.exists():
                continue
            inst_list.append(s)

        if not inst_list:
            return False

        slugs_str = '\n'.join(f"  - {s} (README: {INSTITUTIONS_DIR / s / 'README.md'})" for s in inst_list)

        prompt = f"""You are a website analysis agent. For each institution below, do the following:

1. Read its current README.md to get the tender_url and homepage
2. Fetch the tender page using curl or WebFetch
3. Analyze the ACTUAL HTML structure of the page
4. Update the README.md YAML frontmatter with institution-specific values:

   a. **selectors.container** — the ACTUAL CSS selector for the main content area containing tenders
      (e.g., ".tender-listing", "#tenders-table", ".procurement-section", "table.tenders")
   b. **selectors.tender_item** — the ACTUAL CSS selector for individual tender entries
      (e.g., "table.tenders tr", ".tender-card", ".procurement-item")
   c. **selectors.title** — the ACTUAL selector for tender titles within each item
   d. **selectors.date** — the ACTUAL selector for dates
   e. **selectors.document_link** — the ACTUAL selector for document download links
   f. **selectors.pagination** — the ACTUAL pagination selector (if pagination exists)
   g. **known_document_paths** — ACTUAL paths where documents are stored on this server
      (e.g., "/wp-content/uploads/tenders/", "/storage/app/media/", "/sites/default/files/")
   h. **url_patterns** — ACTUAL URL patterns for this institution's documents
   i. **strategy** — a specific, actionable description of how to scrape THIS institution
   j. **anti_bot.requires_javascript** — set to true only if the page uses React/Angular/Vue/SPA
   k. **document_notes** — specific notes about how this institution organizes its documents
   l. **institution.name** — the ACTUAL name of the institution (from the page, not guessed)

RULES:
- Keep the EXISTING README structure (YAML frontmatter + markdown body)
- Only update fields where you found better/specific values from the actual website
- If the tender page is unreachable or has no tender content, set scraping.enabled to false and add a note
- Do NOT add generic/placeholder selectors — only use what you actually find in the HTML
- If a selector can't be determined, leave the existing generic one
- Process ALL institutions listed below. Do NOT stop early.

Institutions to enrich:
{slugs_str}

Project directory: {BASE_DIR}
"""
        log_file = RESULTS_DIR / f"enrich_batch.log"
        cmd = [
            agent_bin, '-p', '--force', '--trust',
            '--model', 'composer-1.5',
            '--workspace', str(BASE_DIR),
            prompt
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            with open(log_file, 'a') as f:
                f.write(f"\n{'='*60}\nBatch: {', '.join(inst_list[:5])}...\n")
                f.write(result.stdout[-2000:] if result.stdout else "")
                if result.stderr:
                    f.write(f"\nSTDERR: {result.stderr[-500:]}")
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"  Agent CLI timed out for batch")
            return False
        except Exception as e:
            print(f"  Agent CLI error: {e}")
            return False

    # Single institution mode
    folder = INSTITUTIONS_DIR / slug
    readme = folder / "README.md"
    if not readme.exists():
        print(f"  No README.md for {slug}")
        return False

    prompt = f"""You are a website analysis agent. Analyze the institution at {INSTITUTIONS_DIR / slug}:

1. Read {readme} to get the tender_url and homepage
2. Fetch the tender page using curl or WebFetch
3. Analyze the ACTUAL HTML structure
4. Update {readme} with institution-specific CSS selectors, document paths, and scraping strategy

Update these YAML fields with ACTUAL values from the website HTML:
- selectors.container — the real CSS selector for the tender content area
- selectors.tender_item — the real selector for each tender entry
- selectors.title, selectors.date, selectors.document_link, selectors.pagination
- known_document_paths — real paths where documents are stored
- url_patterns — real URL patterns for documents
- strategy — specific scraping instructions for this site
- anti_bot.requires_javascript — true only if it's an SPA (React/Angular/Vue)
- document_notes — how this institution organizes documents
- institution.name — the actual institution name from the page

Only update fields where you find better values. Keep existing structure. Do NOT use generic selectors.
Project directory: {BASE_DIR}"""

    log_file = RESULTS_DIR / f"enrich_{slug}.log"
    cmd = [
        agent_bin, '-p', '--force', '--trust',
        '--model', 'composer-1.5',
        '--workspace', str(BASE_DIR),
        prompt
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        with open(log_file, 'w') as f:
            f.write(result.stdout or "")
            if result.stderr:
                f.write(f"\nSTDERR: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  Agent CLI timed out for {slug}")
        return False
    except Exception as e:
        print(f"  Agent CLI error for {slug}: {e}")
        return False


def remove_institution_folder(domain: str):
    """Remove an institution folder for a miss/error domain."""
    slug = domain_to_slug(domain)
    folder = INSTITUTIONS_DIR / slug
    if folder.exists():
        # Don't delete if it has active tenders
        active = folder / "tenders" / "active"
        if active.exists() and any(active.iterdir()):
            return False
        shutil.rmtree(folder)
        return True
    return False


# ─── Worker / Runner ─────────────────────────────────────────────────────────

async def run_scan(domains: list[str], worker_id: int = 0) -> dict:
    """Scan a list of domains. Returns stats dict."""
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(
        limit=CONCURRENCY, ttl_dns_cache=300, ssl=ssl_ctx,
        enable_cleanup_closed=True
    )
    session = aiohttp.ClientSession(
        connector=connector,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; ZimaTenderBot/1.0)'},
    )

    sem = asyncio.Semaphore(CONCURRENCY)
    stats = {'scanned': 0, 'hits': 0, 'misses': 0, 'errors': 0, 'worker': worker_id}
    start_time = time.time()

    # Ensure results dir exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Output files (per-worker to avoid conflicts)
    hits_file = RESULTS_DIR / f"hits_w{worker_id}.jsonl"
    misses_file = RESULTS_DIR / f"misses_w{worker_id}.txt"
    errors_file = RESULTS_DIR / f"errors_w{worker_id}.txt"

    hits_f = open(hits_file, 'a')
    misses_f = open(misses_file, 'a')
    errors_f = open(errors_file, 'a')

    try:
        # Process in batches
        batch_size = 200
        total = len(domains)

        for batch_start in range(0, total, batch_size):
            batch = domains[batch_start:batch_start + batch_size]
            tasks = [scan_domain(session, d, sem) for d in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for r in results:
                stats['scanned'] += 1

                if isinstance(r, Exception):
                    stats['errors'] += 1
                    continue

                if r['status'] == 'hit':
                    stats['hits'] += 1
                    hits_f.write(json.dumps(r) + '\n')
                    hits_f.flush()
                elif r['status'] == 'miss':
                    stats['misses'] += 1
                    misses_f.write(r['domain'] + '\n')
                elif r['status'] == 'error':
                    stats['errors'] += 1
                    errors_f.write(r['domain'] + '\n')

            elapsed = time.time() - start_time
            rate = stats['scanned'] / elapsed if elapsed > 0 else 0
            print(f"  [W{worker_id}] {stats['scanned']}/{total} "
                  f"({rate:.0f}/s) hits={stats['hits']} "
                  f"miss={stats['misses']} err={stats['errors']}",
                  flush=True)

    finally:
        hits_f.close()
        misses_f.close()
        errors_f.close()
        await session.close()

    elapsed = time.time() - start_time
    stats['elapsed'] = round(elapsed, 1)
    stats['rate'] = round(stats['scanned'] / elapsed, 1) if elapsed > 0 else 0

    # Save worker stats
    with open(RESULTS_DIR / f"stats_w{worker_id}.json", 'w') as f:
        json.dump(stats, f, indent=2)

    return stats


def load_domains(chunk: int = 0, chunks: int = 1) -> list[str]:
    """Load domains from tz.txt, optionally selecting a chunk."""
    with open(DOMAINS_FILE) as f:
        all_domains = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if chunks <= 1:
        return all_domains

    # Split into chunks
    chunk_size = len(all_domains) // chunks
    start = chunk * chunk_size
    end = start + chunk_size if chunk < chunks - 1 else len(all_domains)
    return all_domains[start:end]


def merge_results():
    """Merge per-worker results into single files."""
    # Merge hits
    all_hits = []
    for f in sorted(RESULTS_DIR.glob("hits_w*.jsonl")):
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    all_hits.append(json.loads(line))

    with open(HITS_FILE, 'w') as f:
        for h in all_hits:
            f.write(json.dumps(h) + '\n')

    # Merge misses
    all_misses = set()
    for f in sorted(RESULTS_DIR.glob("misses_w*.txt")):
        all_misses.update(line.strip() for line in open(f) if line.strip())

    with open(MISSES_FILE, 'w') as f:
        f.write('\n'.join(sorted(all_misses)) + '\n')

    # Merge errors
    all_errors = set()
    for f in sorted(RESULTS_DIR.glob("errors_w*.txt")):
        all_errors.update(line.strip() for line in open(f) if line.strip())

    with open(ERRORS_FILE, 'w') as f:
        f.write('\n'.join(sorted(all_errors)) + '\n')

    # Merge stats
    total_stats = {'scanned': 0, 'hits': 0, 'misses': 0, 'errors': 0, 'elapsed': 0}
    for f in sorted(RESULTS_DIR.glob("stats_w*.json")):
        with open(f) as fh:
            s = json.load(fh)
            for k in ['scanned', 'hits', 'misses', 'errors']:
                total_stats[k] += s.get(k, 0)
            total_stats['elapsed'] = max(total_stats['elapsed'], s.get('elapsed', 0))

    total_stats['rate'] = round(total_stats['scanned'] / total_stats['elapsed'], 1) if total_stats['elapsed'] > 0 else 0

    return all_hits, all_misses, all_errors, total_stats


def print_report(hits, misses, errors, stats):
    """Print scan report."""
    print("\n" + "=" * 70)
    print("TENDER DISCOVERY REPORT")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    print(f"\n  Domains scanned:   {stats['scanned']:,}")
    print(f"  Hits (tenders):    {stats['hits']:,}")
    print(f"  Misses:            {stats['misses']:,}")
    print(f"  Errors:            {stats['errors']:,}")
    print(f"  Time:              {stats['elapsed']:.0f}s ({stats['rate']:.0f} domains/sec)")

    if hits:
        print(f"\n  Top hits by keyword count:")
        top = sorted(hits, key=lambda x: -len(x.get('keywords', [])))[:30]
        for h in top:
            kws = ', '.join(h.get('keywords', [])[:3])
            docs = len(h.get('doc_links', []))
            emails = len(h.get('emails', []))
            print(f"    {h['domain']:40s} kw=[{kws}] docs={docs} emails={emails}")

    print("\n" + "=" * 70)


# ─── Commands ─────────────────────────────────────────────────────────────────

async def cmd_scan(args):
    """Phase 1: Scan domains for tender keywords."""
    domains = load_domains(args.chunk, args.chunks)
    print(f"Scanning {len(domains)} domains (worker {args.chunk}/{args.chunks}, "
          f"concurrency={CONCURRENCY})")

    stats = await run_scan(domains, worker_id=args.chunk)

    print(f"\nWorker {args.chunk} done: {stats['scanned']} scanned, "
          f"{stats['hits']} hits, {stats['elapsed']}s ({stats['rate']}/s)")

    # If single worker, merge and report
    if args.chunks <= 1:
        hits, misses, errors, total_stats = merge_results()
        print_report(hits, misses, errors, total_stats)


def cmd_parallel(args):
    """Launch N parallel scan workers as subprocesses."""
    workers = args.workers
    print(f"Launching {workers} parallel workers...")

    # Clear old results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for f in RESULTS_DIR.glob("*_w*.jsonl"):
        f.unlink()
    for f in RESULTS_DIR.glob("*_w*.txt"):
        f.unlink()
    for f in RESULTS_DIR.glob("stats_w*.json"):
        f.unlink()

    script = str(BASE_DIR / "scripts" / "tender_crawler.py")
    procs = []

    for i in range(workers):
        log_file = RESULTS_DIR / f"worker_{i}.log"
        cmd = [sys.executable, script, 'scan', '--chunk', str(i), '--chunks', str(workers)]
        p = subprocess.Popen(cmd, stdout=open(log_file, 'w'), stderr=subprocess.STDOUT)
        procs.append((i, p, log_file))
        print(f"  Worker {i} started (PID {p.pid}) → {log_file}")

    print(f"\nAll {workers} workers running. Waiting...")

    # Wait for all to finish
    for i, p, log_file in procs:
        p.wait()
        print(f"  Worker {i} finished (exit={p.returncode})")

    # Merge results
    hits, misses, errors, total_stats = merge_results()
    print_report(hits, list(misses), list(errors), total_stats)

    # Save merged hits count
    with open(RESULTS_DIR / "final_stats.json", 'w') as f:
        json.dump(total_stats, f, indent=2)

    return hits


def cmd_build(args):
    """Create institution folders for all hits."""
    if not HITS_FILE.exists():
        print("No hits file found. Run scan first.")
        return

    hits = []
    with open(HITS_FILE) as f:
        for line in f:
            if line.strip():
                hits.append(json.loads(line))

    print(f"Building institution folders for {len(hits)} hits...")

    created = 0
    updated = 0
    for hit in hits:
        slug = domain_to_slug(hit['domain'])
        folder = INSTITUTIONS_DIR / slug
        existed = folder.exists()

        if args.dry_run:
            action = "UPDATE" if existed else "CREATE"
            print(f"  {action}: {slug} ({hit['domain']})")
        else:
            create_institution_folder(hit)
            if existed:
                updated += 1
            else:
                created += 1

    print(f"\nDone: {created} created, {updated} updated"
          + (" (DRY RUN)" if args.dry_run else ""))


def cmd_enrich(args):
    """Use Agent CLI to analyze websites and generate institution-specific README configs."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which institutions to enrich
    if args.slug:
        # Single institution
        slugs = [args.slug]
    elif args.incomplete:
        # Find all institutions with generic/partial READMEs
        slugs = []
        for d in sorted(os.listdir(INSTITUTIONS_DIR)):
            readme = INSTITUTIONS_DIR / d / "README.md"
            if not readme.is_file():
                continue
            content = readme.read_text(errors='ignore')
            # Skip already-enriched (has institution-specific selectors, not generic ones)
            if 'container: ".tender-list, .content, main' in content or \
               'container: "main, .content, article, .tender-list' in content:
                slugs.append(d)
            elif 'download_rules:' not in content:
                slugs.append(d)
        print(f"Found {len(slugs)} institutions with generic/partial READMEs")
    else:
        # Default: use hits from crawler
        if not HITS_FILE.exists():
            print("No hits file found. Run scan first or use --incomplete.")
            return
        hits = []
        with open(HITS_FILE) as f:
            for line in f:
                if line.strip():
                    hits.append(json.loads(line))
        slugs = [domain_to_slug(h['domain']) for h in hits]
        # Filter to ones that exist
        slugs = [s for s in slugs if (INSTITUTIONS_DIR / s / "README.md").exists()]

    if not slugs:
        print("No institutions to enrich.")
        return

    # Apply offset/limit
    total = len(slugs)
    start = args.start
    batch_size = args.batch
    slugs = slugs[start:start + batch_size] if batch_size else slugs[start:]

    print(f"\nEnriching {len(slugs)} institutions (of {total} total, offset {start})")
    print(f"Agent CLI batch size: {args.agent_batch}")
    print(f"{'DRY RUN' if args.dry_run else 'LIVE — agent CLI will be invoked'}")
    print("=" * 60)

    if args.dry_run:
        for i, slug in enumerate(slugs[:20]):
            print(f"  [{i+1}] {slug}")
        if len(slugs) > 20:
            print(f"  ... and {len(slugs) - 20} more")
        return

    # Process in agent batches
    agent_batch_size = args.agent_batch
    success_count = 0
    fail_count = 0

    for batch_start in range(0, len(slugs), agent_batch_size):
        batch = slugs[batch_start:batch_start + agent_batch_size]
        batch_num = batch_start // agent_batch_size + 1
        total_batches = (len(slugs) + agent_batch_size - 1) // agent_batch_size

        print(f"\n  Batch {batch_num}/{total_batches}: {', '.join(batch[:3])}{'...' if len(batch) > 3 else ''}")

        ok = enrich_readme_with_agent(batch[0], batch=batch)
        if ok:
            success_count += len(batch)
            print(f"    ✓ {len(batch)} institutions enriched")
        else:
            fail_count += len(batch)
            print(f"    ✗ Batch failed")

    print(f"\n{'='*60}")
    print(f"Enrichment complete: {success_count} succeeded, {fail_count} failed")
    print(f"{'='*60}")


def cmd_upgrade(args):
    """Upgrade all partial/minimal READMEs to gold standard format using crawler data."""
    if not HITS_FILE.exists():
        print("No hits file found. Run scan first.")
        return

    hits = {}
    with open(HITS_FILE) as f:
        for line in f:
            if line.strip():
                h = json.loads(line)
                slug = domain_to_slug(h['domain'])
                hits[slug] = h

    upgraded = 0
    skipped = 0
    already_good = 0

    for d in sorted(os.listdir(INSTITUTIONS_DIR)):
        folder = INSTITUTIONS_DIR / d
        readme = folder / "README.md"
        if not folder.is_dir() or not readme.is_file():
            continue

        content = readme.read_text(errors='ignore')

        # Skip if already gold standard (has download_rules + allowed_content_types)
        if 'allowed_content_types:' in content and 'document_notes:' in content:
            already_good += 1
            continue

        # Need crawler hit data to upgrade
        hit = hits.get(d)
        if not hit:
            skipped += 1
            continue

        if args.dry_run:
            print(f"  UPGRADE: {d}")
            upgraded += 1
            continue

        # Generate and write gold standard README
        new_content = generate_readme(hit)
        readme.write_text(new_content)
        upgraded += 1

    print(f"\n{'='*60}")
    print(f"Upgrade complete:")
    print(f"  Upgraded:      {upgraded}")
    print(f"  Already good:  {already_good}")
    print(f"  Skipped (no crawler data): {skipped}")
    print(f"{'='*60}")


def cmd_cleanup(args):
    """Remove institution folders for misses (no tender content)."""
    if not MISSES_FILE.exists():
        print("No misses file found. Run scan first.")
        return

    with open(MISSES_FILE) as f:
        misses = [line.strip() for line in f if line.strip()]

    # Also add errors (unreachable domains)
    if ERRORS_FILE.exists():
        with open(ERRORS_FILE) as f:
            misses.extend(line.strip() for line in f if line.strip())

    print(f"Checking {len(misses)} domains for cleanup...")

    to_remove = []
    to_keep = []

    for domain in misses:
        slug = domain_to_slug(domain)
        folder = INSTITUTIONS_DIR / slug
        if not folder.exists():
            continue

        # Keep if it has active tenders
        active = folder / "tenders" / "active"
        if active.exists() and any(active.iterdir()):
            to_keep.append(slug)
            continue

        to_remove.append((slug, folder))

    print(f"  To remove: {len(to_remove)} folders")
    print(f"  To keep:   {len(to_keep)} folders (have active tenders)")

    if args.dry_run:
        print("\n  DRY RUN — no folders removed")
        for slug, _ in to_remove[:20]:
            print(f"    Would remove: {slug}")
        if len(to_remove) > 20:
            print(f"    ... and {len(to_remove) - 20} more")
    else:
        removed = 0
        for slug, folder in to_remove:
            try:
                shutil.rmtree(folder)
                removed += 1
            except Exception as e:
                print(f"    Failed: {slug} — {e}")
        print(f"\n  Removed {removed} folders")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Fast Tender Discovery Crawler')
    sub = parser.add_subparsers(dest='command', help='Command to run')

    # scan — single worker
    p_scan = sub.add_parser('scan', help='Scan domains (single worker)')
    p_scan.add_argument('--chunk', type=int, default=0, help='Chunk index (0-based)')
    p_scan.add_argument('--chunks', type=int, default=1, help='Total chunks')

    # parallel — launch N workers
    p_par = sub.add_parser('parallel', help='Launch N parallel scan workers')
    p_par.add_argument('--workers', '-w', type=int, default=4, help='Number of workers')

    # build — create folders for hits
    p_build = sub.add_parser('build', help='Create institution folders for hits')
    p_build.add_argument('--dry-run', action='store_true')

    # cleanup — remove miss folders
    p_clean = sub.add_parser('cleanup', help='Remove folders for misses')
    p_clean.add_argument('--dry-run', action='store_true')

    # upgrade — upgrade partial READMEs to gold standard using crawler data (no AI)
    p_upgrade = sub.add_parser('upgrade', help='Upgrade partial READMEs to gold standard format')
    p_upgrade.add_argument('--dry-run', action='store_true')

    # enrich — use Agent CLI to analyze websites and add institution-specific selectors
    p_enrich = sub.add_parser('enrich', help='Use Agent CLI to generate institution-specific configs')
    p_enrich.add_argument('--slug', type=str, help='Enrich a single institution')
    p_enrich.add_argument('--incomplete', action='store_true', help='Enrich all with generic selectors')
    p_enrich.add_argument('--start', type=int, default=0, help='Start offset')
    p_enrich.add_argument('--batch', type=int, default=0, help='Total institutions to process (0=all)')
    p_enrich.add_argument('--agent-batch', type=int, default=10,
                          help='Institutions per agent CLI call (default 10)')
    p_enrich.add_argument('--dry-run', action='store_true')

    # report — show results
    sub.add_parser('report', help='Show scan results')

    args = parser.parse_args()

    if args.command == 'scan':
        asyncio.run(cmd_scan(args))
    elif args.command == 'parallel':
        cmd_parallel(args)
    elif args.command == 'build':
        cmd_build(args)
    elif args.command == 'cleanup':
        cmd_cleanup(args)
    elif args.command == 'upgrade':
        cmd_upgrade(args)
    elif args.command == 'enrich':
        cmd_enrich(args)
    elif args.command == 'report':
        if HITS_FILE.exists():
            hits, misses, errors, stats = merge_results()
            print_report(hits, list(misses), list(errors), stats)
        else:
            print("No results found. Run scan first.")
    else:
        parser.print_help()
        print("\nQuick start:")
        print("  python3 tender_crawler.py parallel -w 8   # Scan all 10K domains with 8 workers")
        print("  python3 tender_crawler.py build            # Create/upgrade folders for hits")
        print("  python3 tender_crawler.py upgrade          # Upgrade all partial READMEs (no AI)")
        print("  python3 tender_crawler.py enrich           # Use Agent CLI for institution-specific configs")
        print("  python3 tender_crawler.py cleanup          # Remove miss folders")


if __name__ == '__main__':
    main()
