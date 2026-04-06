#!/usr/bin/env python3
"""
Batch scrape 25 institutions for active tenders.
Run ID: run_20260315_060430_batch114
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch114"

INSTITUTIONS = [
    ("tanelec", None),
    ("taneps", None),
    ("tanescosaccos", "https://tanescosaccos.or.tz/zabuni/"),
    ("tanga", "https://tanga.go.tz/procurements"),
    ("tangacc", "https://tangacc.go.tz/tenders"),
    ("tanganyikadc", "https://tanganyikadc.go.tz/ugavi-na-manunuzi"),
    ("tanganyikaschools", None),
    ("tangatimes", "https://livanholidays.co.tz/"),
    ("tanhydro", None),
    ("tanicacafe", "https://tanicacafe.co.tz/procurement-portal/"),
    ("tanoil", None),
    ("tanpack", None),
    ("tanroads", "https://tanroads.go.tz/tenders/open"),
    ("tanscarattorneys", "https://tanscarattorneys.co.tz/"),
    ("tanserve", "http://tanserve.co.tz/category/tanzania-business-tenders/"),
    ("tansheq", None),
    ("tantrade", None),
    ("tanwat", None),
    ("tanzania", None),
    ("tanzania-tenders", "https://tanzaniatenders.com/"),
    ("tanzaniabreweries", None),
    ("tanzaniachoicesafaris", None),
    ("tanzaniadestination", None),
    ("tanzaniahotels", None),
    ("tanzaniaislamic-centre", "https://tanzaniaislamic-centre.or.tz/"),
]

DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug):
    """Load README and extract tender_url if not in INSTITUTIONS."""
    readme_path = PROJECT / "institutions" / slug / "README.md"
    if not readme_path.exists():
        return None, None
    text = readme_path.read_text(encoding="utf-8")
    # Extract tender_url from YAML
    m = re.search(r"tender_url:\s*[\"']?([^\"'\s\n]+)", text)
    url = m.group(1) if m else None
    # Extract institution name
    nm = re.search(r'name:\s*["\']([^"\']+)["\']', text)
    name = nm.group(1) if nm else slug.replace("-", " ").title()
    return url, name


def fetch_url(url, timeout=25):
    """Fetch URL with curl, skip SSL verify for .go.tz sites."""
    try:
        cmd = [
            "curl", "-sL", "-m", str(timeout),
            "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)",
            "-k",  # skip SSL verify for gov sites
            url
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        return r.stdout if r.returncode == 0 else None
    except Exception as e:
        return None


def extract_doc_links(html, base_url):
    """Extract document links (PDF, DOC, etc.) from HTML."""
    links = set()
    for ext in DOC_EXTENSIONS:
        pattern = r'href=["\']([^"\']*' + re.escape(ext) + r'[^"\']*)["\']'
        for m in re.finditer(pattern, html, re.I):
            href = m.group(1)
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                parsed = urlparse(base_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            links.add(href)
    return list(links)


def extract_emails(html):
    """Extract email addresses from HTML."""
    return list(set(EMAIL_PATTERN.findall(html)))


def has_tender_content(html):
    """Heuristic: does page contain tender-like content?"""
    if not html:
        return False
    html_lower = html.lower()
    # Look for tender keywords
    keywords = ["tender", "zabuni", "procurement", "rfp", "rfq", "eoi", "bid", "manunuzi", "closing date", "deadline"]
    for kw in keywords:
        if kw in html_lower:
            # Check for table rows or list items that look like tender entries
            if re.search(rf"<tr[^>]*>.*{kw}", html_lower, re.DOTALL):
                return True
            if re.search(rf"<li[^>]*>.*{kw}", html_lower, re.DOTALL):
                return True
            if re.search(rf"<div[^>]*class=[^>]*tender", html_lower):
                return True
            if re.search(rf"tender[^<]*</(h[1-6]|a|span)", html_lower):
                return True
    return False


def parse_tender_listings(html, base_url):
    """Extract tender-like items from HTML. Returns list of dicts."""
    tenders = []
    # Simple extraction: look for links that might be tender titles
    # Many sites use tables or cards
    doc_links = extract_doc_links(html, base_url)
    if doc_links and (has_tender_content(html) or "tender" in html.lower() or "zabuni" in html.lower()):
        # Create a single "tender" if we have doc links and tender context
        tenders.append({
            "title": "Tender Documents",
            "documents": doc_links,
            "source_url": base_url
        })
    return tenders


def ensure_dirs(inst_dir):
    """Ensure required directories exist."""
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_document(url, dest_path):
    """Download a document to dest_path."""
    try:
        cmd = ["curl", "-sL", "-m", "60", "-k", "-A", "Mozilla/5.0", "-o", str(dest_path), url]
        r = subprocess.run(cmd, capture_output=True, timeout=65)
        return r.returncode == 0 and dest_path.exists() and dest_path.stat().st_size > 0
    except Exception:
        return False


def append_lead(lead):
    """Append lead to opportunities/leads.json."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        try:
            data = json.loads(leads_path.read_text(encoding="utf-8"))
            leads = data if isinstance(data, list) else data.get("leads", [])
        except Exception:
            pass
    # Check if slug already exists
    if any(l.get("institution_slug") == lead.get("institution_slug") for l in leads):
        return
    leads.append(lead)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")


def process_institution(slug, tender_url):
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    if not inst_dir.exists():
        return "not_found", 0, 0

    # Resolve URL from README if not provided
    if tender_url is None:
        tender_url, inst_name = load_readme(slug)
        if not tender_url:
            return "no_url", 0, 0
    else:
        _, inst_name = load_readme(slug)
        if not inst_name:
            inst_name = slug.replace("-", " ").title()

    # Fetch
    html = fetch_url(tender_url)
    if html is None:
        return "fetch_error", 0, 0

    # Parse
    tenders = parse_tender_listings(html, tender_url)
    doc_links = extract_doc_links(html, tender_url)

    # Heuristic: if tender page has "zabuni" or "tender" but no structured listings, check for doc links
    if not tenders and doc_links and (has_tender_content(html) or "zabuni" in html.lower()):
        tenders = [{"title": "Tender Documents", "documents": doc_links, "source_url": tender_url}]

    if tenders:
        ensure_dirs(inst_dir)
        doc_count = 0
        year = datetime.now().year
        for i, t in enumerate(tenders):
            tender_id = f"{slug.upper().replace('-', '')[:12]}-{year}-{i+1:03d}"
            t["tender_id"] = tender_id
            t["institution"] = slug
            t["scraped_at"] = datetime.now(timezone.utc).isoformat()
            t["status"] = "active"
            json_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
            json_path.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")
            # Download documents
            docs = t.get("documents", [])
            for doc_url in docs:
                download_dir = inst_dir / "downloads" / tender_id / "original"
                download_dir.mkdir(parents=True, exist_ok=True)
                fname = doc_url.split("/")[-1].split("?")[0] or "document.pdf"
                dest = download_dir / fname
                if download_document(doc_url, dest):
                    doc_count += 1
        # Update last_scrape
        last = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).isoformat(),
            "next_scrape": datetime.now(timezone.utc).isoformat(),
            "active_tenders_count": len(tenders),
            "status": "success",
            "error": None
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
        # Append scrape_log
        log_path = inst_dir / "scrape_log.json"
        runs = []
        if log_path.exists():
            try:
                data = json.loads(log_path.read_text(encoding="utf-8"))
                runs = data if isinstance(data, list) else data.get("runs", [])
            except Exception:
                pass
        runs.append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": 0,
            "status": "success",
            "tenders_found": len(tenders),
            "new_tenders": len(tenders),
            "documents_downloaded": doc_count,
            "errors": []
        })
        log_path.write_text(json.dumps(runs, indent=2), encoding="utf-8")
        return "tenders", len(tenders), doc_count
    else:
        # No tenders: opportunity workflow
        emails = extract_emails(html)
        homepage = tender_url
        if "/" in homepage:
            parts = homepage.split("/")
            if len(parts) >= 3:
                homepage = "/".join(parts[:3])
        lead = {
            "institution_slug": slug,
            "institution_name": inst_name or slug.replace("-", " ").title(),
            "website_url": homepage,
            "emails": emails[:5],
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name or slug}",
            "draft_email_body": f"Dear {inst_name or slug} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst_name or slug}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending"
        }
        append_lead(lead)
        # Update last_scrape
        last = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).isoformat(),
            "active_tenders_count": 0,
            "status": "success",
            "error": None
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
        log_path = inst_dir / "scrape_log.json"
        runs = []
        if log_path.exists():
            try:
                data = json.loads(log_path.read_text(encoding="utf-8"))
                runs = data if isinstance(data, list) else data.get("runs", [])
            except Exception:
                pass
        runs.append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "tenders_found": 0,
            "opportunity_lead": True,
            "errors": []
        })
        log_path.write_text(json.dumps(runs, indent=2), encoding="utf-8")
        return "opportunity", 0, 0


def main():
    results = []
    for slug, url in INSTITUTIONS:
        status, tc, dc = process_institution(slug, url)
        results.append((slug, status, tc, dc))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}", flush=True)
    # Sync leads CSV if any opportunities
    if any(r[1] == "opportunity" for r in results):
        subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
