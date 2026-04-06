#!/usr/bin/env python3
"""
Crawl ALL Tanzanian .co.tz / .or.tz / .ac.tz domains for tender content.
Features:
  - Automatic resume: saves progress after each batch, picks up where it left off
  - Detailed README.md generation matching crdb-bank format
  - Deep page analysis: finds tender URLs, document links, contact info
  - Rate-limited and polite crawling
  - JSON state file for tracking progress

Usage:
  python3 scripts/crawl_all_tz.py                    # Resume from last checkpoint
  python3 scripts/crawl_all_tz.py --reset             # Start fresh
  python3 scripts/crawl_all_tz.py --batch-size 200    # Custom batch size
  python3 scripts/crawl_all_tz.py --concurrency 30    # Custom concurrency
"""

import asyncio
import aiohttp
import ssl
import re
import json
import time
import logging
import warnings
import argparse
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone

# Suppress noise
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")

# ─── Configuration ───
BASE_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
INST_DIR = BASE_DIR / "institutions"
DOMAIN_FILE = BASE_DIR / "institutions" / "tz.txt"
STATE_FILE = BASE_DIR / "scripts" / ".crawl_state.json"
RESULTS_FILE = BASE_DIR / "scripts" / ".crawl_results.json"
WEBSITES_MD = INST_DIR / "websites.md"

DEFAULT_BATCH_SIZE = 100
DEFAULT_CONCURRENCY = 40
TIMEOUT = aiohttp.ClientTimeout(total=12, connect=6)

TENDER_KEYWORDS = [
    'tender', 'tenders', 'procurement', 'rfp', 'rfq', 'rfi',
    'expression of interest', 'eoi', 'bidding', 'bid',
    'zabuni', 'manunuzi',
    'quotation', 'invitation to bid', 'request for proposal',
    'supply', 'prequalification',
]

STRONG_KEYWORDS = {
    'tender', 'tenders', 'procurement', 'rfp', 'rfq', 'eoi',
    'expression of interest', 'bidding', 'zabuni', 'manunuzi', 'prequalification',
}

TENDER_PATHS = [
    '/tenders', '/tender', '/procurement', '/tenders/', '/tender/',
    '/procurement/', '/bids', '/opportunities',
    '/zabuni', '/manunuzi',
    '/en/tenders', '/en/procurement',
]

DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar'}


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def load_state():
    """Load crawl state from disk."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "completed_domains": [],
        "last_batch": 0,
        "total_found": 0,
        "started_at": None,
        "last_checkpoint": None,
    }


def save_state(state):
    """Save crawl state to disk."""
    state["last_checkpoint"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def load_results():
    """Load accumulated results from disk."""
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return {}


def save_results(results):
    """Save accumulated results to disk."""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)


def classify_domain(domain):
    """Classify domain into organization type."""
    d = domain.lower()
    if '.go.tz' in d:
        # Sub-classify government
        if any(x in d for x in ['dc.go', 'mc.go', 'tc.go', 'cc.go']):
            return "Local Government Authority"
        elif any(x in d for x in ['wasa', 'uwsa', 'wssa']):
            return "Water Utility"
        elif any(x in d for x in ['hospital', 'health']):
            return "Government Hospital"
        else:
            return "Government Agency"
    elif '.ac.tz' in d or '.sc.tz' in d:
        return "Educational Institution"
    elif '.or.tz' in d:
        return "NGO / Non-Profit Organization"
    elif any(x in d for x in ['bank', 'benki']):
        return "Bank"
    elif any(x in d for x in ['insurance', 'bima']):
        return "Insurance Company"
    elif any(x in d for x in ['saccos', 'sacco']):
        return "SACCOS"
    elif any(x in d for x in ['finance', 'microfinance']):
        return "Microfinance / Financial Services"
    elif any(x in d for x in ['hospital', 'clinic', 'health', 'medical']):
        return "Healthcare"
    elif any(x in d for x in ['mining', 'oil', 'gas', 'energy', 'electric']):
        return "Energy / Mining"
    elif any(x in d for x in ['transport', 'logistics', 'shipping', 'freight']):
        return "Transport / Logistics"
    elif any(x in d for x in ['hotel', 'safari', 'travel', 'tour']):
        return "Tourism / Hospitality"
    elif any(x in d for x in ['invest', 'capital', 'securities', 'broker']):
        return "Investment / Securities"
    elif any(x in d for x in ['construction', 'building', 'engineer']):
        return "Construction / Engineering"
    elif any(x in d for x in ['tech', 'software', 'ict', 'digital', 'computer']):
        return "ICT / Technology"
    else:
        return "Commercial / Private Sector"


def extract_page_info(text, url, domain):
    """Deep extraction of page information."""
    text_lower = text.lower()
    info = {
        'url': url,
        'title': '',
        'description': '',
        'keywords_found': [],
        'tender_links': [],
        'document_links': [],
        'contact_email': [],
        'contact_phone': [],
        'address': [],
        'social_media': {},
        'has_tender_page': False,
        'tender_page_urls': [],
        'document_download_paths': [],
        'raw_text_snippet': '',
    }

    # Title
    m = re.search(r'<title[^>]*>([^<]+)</title>', text, re.I)
    info['title'] = m.group(1).strip()[:200] if m else domain

    # Meta description
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', text, re.I)
    if not m:
        m = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']description["\']', text, re.I)
    if m:
        info['description'] = m.group(1).strip()[:500]

    # Tender keywords
    for kw in TENDER_KEYWORDS:
        if kw in text_lower:
            info['keywords_found'].append(kw)

    # Tender-related links
    tender_link_re = re.compile(
        r'href=["\']([^"\']*(?:tender|procurement|rfp|rfq|bid|zabuni|manunuzi|quotation)[^"\']*)["\']',
        re.I
    )
    for m in tender_link_re.finditer(text):
        link = m.group(1)
        if not link.startswith(('javascript:', 'mailto:', '#', 'tel:')):
            full = urljoin(url, link)
            info['tender_links'].append(full)
    info['tender_links'] = list(set(info['tender_links']))[:20]

    if info['tender_links']:
        info['has_tender_page'] = True
        info['tender_page_urls'] = info['tender_links'][:5]

    # Document links
    doc_link_re = re.compile(
        r'href=["\']([^"\']+\.(?:pdf|doc|docx|xls|xlsx|zip|rar))["\']',
        re.I
    )
    for m in doc_link_re.finditer(text):
        full = urljoin(url, m.group(1))
        info['document_links'].append(full)
    info['document_links'] = list(set(info['document_links']))[:20]

    # Document download paths (common CMS patterns)
    path_patterns = [
        r'/(?:storage|uploads|media|wp-content/uploads|assets|files|documents|content/dam)/[^"\'>\s]+',
    ]
    for pat in path_patterns:
        for m in re.finditer(pat, text, re.I):
            path = m.group(0)
            if any(path.lower().endswith(ext) for ext in DOCUMENT_EXTENSIONS):
                info['document_download_paths'].append(path)
    info['document_download_paths'] = list(set(info['document_download_paths']))[:10]

    # Contact emails
    email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    emails = set(email_re.findall(text))
    # Filter out common non-contact emails
    info['contact_email'] = [e for e in emails if not any(x in e.lower() for x in
        ['example.com', 'sentry.io', 'wordpress', 'wixpress', 'schema.org',
         'w3.org', 'google.com', 'facebook.com', 'twitter.com', 'jquery',
         'cloudflare', 'gravatar', 'github'])][:5]

    # Phone numbers (Tanzanian format)
    phone_re = re.compile(r'(?:\+255|0)\s*\d[\d\s\-]{7,12}')
    info['contact_phone'] = list(set(phone_re.findall(text)))[:5]

    # Social media
    social_patterns = {
        'facebook': r'(?:facebook\.com|fb\.com)/([a-zA-Z0-9._-]+)',
        'twitter': r'twitter\.com/([a-zA-Z0-9_]+)',
        'linkedin': r'linkedin\.com/(?:company|in)/([a-zA-Z0-9._-]+)',
        'instagram': r'instagram\.com/([a-zA-Z0-9._-]+)',
    }
    for platform, pat in social_patterns.items():
        m = re.search(pat, text, re.I)
        if m:
            info['social_media'][platform] = m.group(1)

    # Text snippet (around tender keywords)
    for kw in ['tender', 'procurement', 'zabuni']:
        idx = text_lower.find(kw)
        if idx > 0:
            start = max(0, idx - 100)
            end = min(len(text), idx + 200)
            # Strip HTML tags
            snippet = re.sub(r'<[^>]+>', ' ', text[start:end])
            snippet = re.sub(r'\s+', ' ', snippet).strip()
            if len(snippet) > 20:
                info['raw_text_snippet'] = snippet[:300]
                break

    return info


async def check_domain(session, domain, sem):
    """Check a single domain for tender content. Returns (domain, info_list) or None."""
    async with sem:
        results = []

        for scheme in ['https', 'http']:
            url = f"{scheme}://{domain}"
            try:
                async with session.get(url, allow_redirects=True, timeout=TIMEOUT) as resp:
                    if resp.status == 200:
                        text = await resp.text(errors='replace')
                        if len(text) > 200:
                            info = extract_page_info(text, str(resp.url), domain)
                            if info['keywords_found']:
                                results.append(info)
                                break  # Got homepage, no need for HTTP fallback
            except Exception:
                continue

        # If homepage had no results, try tender paths
        if not results:
            for path in TENDER_PATHS[:3]:
                for scheme in ['https', 'http']:
                    try:
                        test_url = f"{scheme}://{domain}{path}"
                        async with session.get(test_url, allow_redirects=True, timeout=TIMEOUT) as resp:
                            if resp.status == 200:
                                text = await resp.text(errors='replace')
                                if len(text) > 500:
                                    info = extract_page_info(text, str(resp.url), domain)
                                    if info['keywords_found']:
                                        results.append(info)
                                        break
                    except Exception:
                        continue
                if results:
                    break

        if results:
            return (domain, results)
        return None


def generate_readme(domain, hits):
    """Generate a detailed README.md matching the crdb-bank format."""
    title = hits[0]['title']
    url = hits[0]['url']
    org_type = classify_domain(domain)
    parsed = urlparse(url)
    homepage = f"{parsed.scheme}://{parsed.netloc}/"

    all_kws = set()
    all_tender_links = []
    all_doc_links = []
    all_emails = []
    all_phones = []
    social = {}
    doc_paths = []
    description = ''
    snippet = ''

    for h in hits:
        all_kws.update(h.get('keywords_found', []))
        all_tender_links.extend(h.get('tender_links', []))
        all_doc_links.extend(h.get('document_links', []))
        all_emails.extend(h.get('contact_email', []))
        all_phones.extend(h.get('contact_phone', []))
        social.update(h.get('social_media', {}))
        doc_paths.extend(h.get('document_download_paths', []))
        if h.get('description') and not description:
            description = h['description']
        if h.get('raw_text_snippet') and not snippet:
            snippet = h['raw_text_snippet']

    all_tender_links = list(set(all_tender_links))[:15]
    all_doc_links = list(set(all_doc_links))[:15]
    all_emails = list(set(all_emails))[:5]
    all_phones = list(set(all_phones))[:5]
    doc_paths = list(set(doc_paths))[:10]

    # Determine tender URL
    tender_url = all_tender_links[0] if all_tender_links else homepage
    strong = all_kws & STRONG_KEYWORDS
    is_strong = bool(strong)

    # Determine scraping method
    if any(x in domain for x in ['.go.tz']):
        strategy = f"Scrape {tender_url} for government tender notices. Government sites often post zabuni/manunuzi."
    elif 'bank' in domain:
        strategy = f"Scrape {tender_url} for banking tender notices and EOIs. Banks post frequently."
    else:
        strategy = f"Scrape {tender_url} for tender/procurement notices."

    slug = domain.replace('.co.tz', '').replace('.go.tz', '').replace('.or.tz', '').replace('.ac.tz', '').replace('.sc.tz', '')

    # Build selectors based on common patterns
    selectors_block = """  selectors:
    container: ".tender-list, .content, main, .entry-content, .page-content, article"
    tender_item: "article, .tender-item, .card, .row, li, tr"
    title: "h2, h3, h4, .tender-title, a"
    date: ".date, .closing-date, .published, time"
    document_link: 'a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[download]'
    pagination: ".pagination a, a.next, .nav-links a" """

    # Document URL patterns
    url_patterns = ""
    if doc_paths:
        url_patterns = "\n".join(f'      - "{domain}{p}"' for p in doc_paths[:5])
    else:
        url_patterns = f'      - "{domain}/*.pdf"'

    # Build file type selectors
    link_selectors = """        - 'a[href$=".pdf"]'
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
        - 'a[download]'"""

    doc_notes = ""
    if doc_paths:
        doc_notes = f"Known document paths: {', '.join(doc_paths[:3])}"
    else:
        doc_notes = "Document storage paths not yet identified. Check tender detail pages for download links."

    # Contact block
    contact_block = ""
    if all_emails or all_phones:
        contact_block = "\ncontact:\n"
        if all_emails:
            contact_block += f"  email: \"{all_emails[0]}\"\n"
            if len(all_emails) > 1:
                contact_block += f"  alternate_emails:\n"
                for e in all_emails[1:]:
                    contact_block += f"    - \"{e}\"\n"
        if all_phones:
            contact_block += f"  phone: \"{all_phones[0]}\"\n"

    # Social media block
    social_block = ""
    if social:
        social_block = "\nsocial_media:\n"
        for platform, handle in social.items():
            social_block += f"  {platform}: \"{handle}\"\n"

    readme = f"""---
institution:
  name: "{title}"
  slug: "{slug}"
  category: "{org_type}"
  status: "active"
  country: "Tanzania"
  domain: "{domain}"

website:
  homepage: "{homepage}"
  tender_url: "{tender_url}"
{contact_block}
scraping:
  enabled: true
  method: "http_get"
  strategy: "{strategy}"
{selectors_block}
  schedule: "daily"

  anti_bot:
    requires_javascript: false
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
{link_selectors}
      resolve_redirects: true
      decode_percent_encoding: true

    url_patterns:
{url_patterns}

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
{social_block}
notes: |
  {description if description else f"Organization website at {domain}. Tender keywords detected: {', '.join(sorted(all_kws))}."}
---

# {title}

**Category:** {org_type}
**Website:** {homepage}
**Tender Page:** {tender_url}
**Keywords Found:** {', '.join(sorted(all_kws))}

## Contact Information
"""

    if all_emails:
        for e in all_emails:
            readme += f"- Email: {e}\n"
    if all_phones:
        for p in all_phones:
            readme += f"- Phone: {p}\n"
    if not all_emails and not all_phones:
        readme += "- Not yet extracted. Check website.\n"

    readme += f"""
## Scraping Instructions

**Strategy:** {strategy}
**Method:** http_get

{description if description else ''}

"""

    if snippet:
        readme += f"""### Tender Content Preview

> {snippet}

"""

    if all_tender_links:
        readme += "### Known Tender URLs\n\n"
        for link in all_tender_links[:10]:
            readme += f"- {link}\n"
        readme += "\n"

    if all_doc_links:
        readme += "### Document Links Found\n\n"
        for link in all_doc_links[:10]:
            readme += f"- {link}\n"
        readme += "\n"

    readme += f"""## Document Download Instructions

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

{doc_notes}

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

- **Last Checked:** {datetime.now(timezone.utc).strftime('%d %B %Y')}
- **Active Tenders:** To be scraped
- **Signal Strength:** {"Strong" if is_strong else "Weak"} ({', '.join(sorted(strong)) if strong else 'supply/rfi only'})
"""

    return readme


async def main():
    parser = argparse.ArgumentParser(description="Crawl TZ domains for tenders")
    parser.add_argument('--reset', action='store_true', help='Start fresh, ignore previous progress')
    parser.add_argument('--batch-size', type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument('--concurrency', type=int, default=DEFAULT_CONCURRENCY)
    args = parser.parse_args()

    # Load all domains
    with open(DOMAIN_FILE) as f:
        all_domains = [line.strip() for line in f if line.strip()]

    # Load or reset state
    if args.reset:
        state = {"completed_domains": [], "last_batch": 0, "total_found": 0,
                 "started_at": datetime.now(timezone.utc).isoformat(), "last_checkpoint": None}
        results = {}
        save_state(state)
        save_results(results)
        fprint("Starting fresh crawl...")
    else:
        state = load_state()
        results = load_results()

    if not state.get("started_at"):
        state["started_at"] = datetime.now(timezone.utc).isoformat()

    completed = set(state.get("completed_domains", []))
    remaining = [d for d in all_domains if d not in completed]

    fprint(f"Total domains: {len(all_domains)}")
    fprint(f"Already completed: {len(completed)}")
    fprint(f"Remaining: {len(remaining)}")
    fprint(f"Results so far: {len(results)}")
    fprint(f"Batch size: {args.batch_size}, Concurrency: {args.concurrency}")
    fprint()

    if not remaining:
        fprint("All domains already crawled! Use --reset to start over.")
        return

    sem = asyncio.Semaphore(args.concurrency)
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(ssl=ssl_ctx, limit=args.concurrency, ttl_dns_cache=300)

    new_found = 0
    new_folders = 0
    batch_num = 0

    async with aiohttp.ClientSession(connector=connector) as session:
        total_batches = (len(remaining) + args.batch_size - 1) // args.batch_size

        for i in range(0, len(remaining), args.batch_size):
            batch = remaining[i:i + args.batch_size]
            batch_num += 1
            fprint(f"Batch {batch_num}/{total_batches} ({len(completed) + i + 1}-{len(completed) + i + len(batch)} of {len(all_domains)})...")

            tasks = [check_domain(session, domain, sem) for domain in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            batch_found = 0
            for result in batch_results:
                if isinstance(result, Exception) or result is None:
                    continue
                domain, hits = result
                results[domain] = hits
                batch_found += 1
                new_found += 1

                # Create institution folder
                slug = domain.replace('.co.tz', '').replace('.go.tz', '').replace('.or.tz', '').replace('.ac.tz', '').replace('.sc.tz', '')
                folder = INST_DIR / slug
                if not folder.exists():
                    folder.mkdir(parents=True, exist_ok=True)
                    readme = generate_readme(domain, hits)
                    (folder / "README.md").write_text(readme)
                    new_folders += 1
                    fprint(f"  + {domain} → {slug}/ ({', '.join(hits[0].get('keywords_found', [])[:3])})")

            # Update completed list
            completed.update(batch)
            state["completed_domains"] = list(completed)
            state["last_batch"] = len(completed)
            state["total_found"] = len(results)

            # Checkpoint save
            save_state(state)
            save_results(results)

            fprint(f"  Batch: {batch_found} found | Total: {len(results)} | New folders: {new_folders}")

    # Final summary
    fprint(f"\n{'='*60}")
    fprint(f"CRAWL COMPLETE")
    fprint(f"{'='*60}")
    fprint(f"Total domains crawled: {len(completed)}")
    fprint(f"Domains with tender content: {len(results)}")
    fprint(f"New folders created this run: {new_folders}")
    fprint(f"State saved to: {STATE_FILE}")
    fprint(f"Results saved to: {RESULTS_FILE}")

    # Regenerate websites.md
    fprint(f"\nRegenerating {WEBSITES_MD}...")
    generate_websites_md(results)
    fprint("Done!")


def generate_websites_md(results):
    """Regenerate the master websites.md index."""
    strong = {}
    weak = {}
    for domain, hits in results.items():
        kws = set()
        for h in hits:
            kws.update(h.get('keywords_found', []))
        if kws & STRONG_KEYWORDS:
            strong[domain] = hits
        else:
            weak[domain] = hits

    def sort_key(item):
        kws = set()
        for h in item[1]:
            kws.update(h.get('keywords_found', []))
        return -len(kws & STRONG_KEYWORDS)

    strong_sorted = sorted(strong.items(), key=sort_key)

    gov = [(d, h) for d, h in strong_sorted if '.go.tz' in d]
    bank_kws = ['bank', 'crdb', 'nbc', 'nmb', 'kcb', 'stanbic', 'absa', 'dtb', 'exim', 'amana', 'pbz', 'cdb', 'mhb', 'nic']
    banks = [(d, h) for d, h in strong_sorted if any(kw in d for kw in bank_kws)]
    bank_d = {x[0] for x in banks}
    fin_kws = ['finance', 'insurance', 'saccos', 'sacco', 'capital', 'invest', 'securities', 'broker']
    finance = [(d, h) for d, h in strong_sorted if any(kw in d for kw in fin_kws) and d not in bank_d]
    fin_d = {x[0] for x in finance}
    gov_d = {x[0] for x in gov}
    other = [(d, h) for d, h in strong_sorted if d not in gov_d and d not in bank_d and d not in fin_d]

    def write_table(f, items):
        f.write("| # | Domain | Title | Tender Keywords | Link |\n")
        f.write("|---|--------|-------|-----------------|------|\n")
        for i, (domain, hits) in enumerate(items, 1):
            title = hits[0].get('title', domain)[:55].replace('|', '-').replace('\n', ' ')
            kws = set()
            links = []
            for h in hits:
                kws.update(h.get('keywords_found', []))
                links.extend(h.get('tender_links', []))
            kw_str = ', '.join(sorted(kws & STRONG_KEYWORDS))
            link = links[0] if links else f"https://{domain}"
            f.write(f"| {i} | {domain} | {title} | {kw_str} | [link]({link}) |\n")

    with open(WEBSITES_MD, 'w') as f:
        f.write("# Tanzanian Websites with Tender/Procurement Content\n\n")
        f.write(f"**Last Updated:** {datetime.now(timezone.utc).strftime('%d %B %Y %H:%M UTC')}\n")
        f.write(f"**Total Domains Crawled:** {len(results) + len(weak)}\n")
        f.write(f"**Strong Tender Signals:** {len(strong)} domains\n")
        f.write(f"**Weak Signals (rfi/supply only):** {len(weak)} domains\n\n---\n\n")

        f.write(f"## Government Agencies ({len(gov)})\n\n")
        write_table(f, gov)
        f.write(f"\n## Banks ({len(banks)})\n\n")
        write_table(f, banks)
        f.write(f"\n## Financial Services ({len(finance)})\n\n")
        write_table(f, finance)
        f.write(f"\n## Other Organizations ({len(other)})\n\n")
        write_table(f, other)

        # Also list weak signals
        if weak:
            weak_sorted = sorted(weak.items(), key=lambda x: x[0])
            f.write(f"\n## Weak Signals — Supply/RFI Only ({len(weak)})\n\n")
            f.write("| # | Domain | Title |\n")
            f.write("|---|--------|-------|\n")
            for i, (domain, hits) in enumerate(weak_sorted, 1):
                title = hits[0].get('title', domain)[:60].replace('|', '-').replace('\n', ' ')
                f.write(f"| {i} | {domain} | {title} |\n")


if __name__ == "__main__":
    asyncio.run(main())
