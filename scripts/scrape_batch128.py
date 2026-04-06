#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260313_205329_batch128
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch128"
RATE_LIMIT = 10

INSTITUTIONS = [
    ("wcf", "https://wcf.go.tz/", "WCF | Ofisi ya Waziri Mkuu Kazi, Ajira na Mahusiano - Mwanzo"),
    ("we", "https://we.co.tz/", "Home 02 - W and E Solution - Shop"),
    ("webdesign", "https://webdesign.co.tz/", "Web Design – The website designers blog"),
    ("webexperts", "https://webexperts.co.tz/", "Web Experts Tanzania"),
    ("webhost", "https://konekta.co.tz/", "WebHost Tanzania"),
    ("webhosting", "https://webhosting.co.tz/", "Malampe Farmers Co. Ltd."),
    ("webhosting.ne.tz", "https://proserver1.at/", "Server Error 404: not found - proserver1.at"),
    ("webline", "https://webline.co.tz/", "Portal Home - Webline Africa Limited"),
    ("webmagic", "https://www.webmagic.co.tz/", "WebMagic Tanzania"),
    ("websitehosting", "https://websitehosting.co.tz/", "Web Hosting in Tanzania"),
    ("webtechnologies", "https://webtechnologies.co.tz/", "Web, Software, ICT, Tracking, Business, Networking and Training Solutions Company"),
    ("wecab", "https://wecab.co.tz/", "WeCab | Book your Tour, Excursions & Safari"),
    ("wecobhas", "https://wecobhas.ac.tz/", "West Evan College of Business, Health and Allied Science"),
    ("wedding", "https://wedding.co.tz/", "Francis & Caroline"),
    ("wegmar", "https://wegmar.co.tz/", "Wegmar Limited"),
    ("wegrow", "https://wegrow.co.tz/", "Wegrow Marketing Agency"),
    ("weldfits", "https://weldfits.co.tz/", "Weldfits Construction Company Ltd"),
    ("wemaconsult", "http://wemaconsult.com/", "Welcome to Wema Consult"),
    ("wemanage", "https://www.wemanage.co.tz/", "Wemanage Networks"),
    ("wendyrayna", "https://wendyrayna.ac.tz/", "WendyRayna School"),
    ("westbmc", "https://westbmc.go.tz/", "Baraza la Manispaa Magharibi B Zanzibar"),
    ("westernhauliers", "https://westernhauliers.co.tz/", "Western Hauliers"),
    ("wetnwild", "https://wetnwild.co.tz/", "Kunduchi Wet 'N' Wild Water Park"),
    ("wewin", "https://wewin.co.tz/", "wewin – wewin risk"),
    ("wflogistics", "https://wflogistics.co.tz/", "WF LOGISTICS"),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfi|eoi|bid|quotation|supply)\b",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-skL", "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", "--max-time", str(timeout), url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}: {r.stderr[:200] if r.stderr else 'unknown'}"
        return r.stdout or None, None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def extract_emails(html: str) -> list[str]:
    """Extract valid emails from HTML."""
    if not html:
        return []
    seen = set()
    out = []
    for m in EMAIL_RE.finditer(html):
        e = m.group(0).lower()
        if e not in seen and "@" in e and not any(x in e for x in [".png", ".jpg", ".gif", ".svg", "example@"]):
            seen.add(e)
            out.append(e)
    return out


def extract_doc_links(html: str, base_url: str) -> list[str]:
    """Extract document links (pdf, doc, docx, xls, xlsx, zip) from HTML."""
    if not html:
        return []
    links = []
    for ext in DOC_EXT:
        pat = re.compile(rf'href=["\']([^"\']*\{re.escape(ext)}[^"\']*)["\']', re.I)
        for m in pat.finditer(html):
            u = m.group(1).strip()
            if u.startswith("/"):
                u = urljoin(base_url, u)
            elif not u.startswith("http"):
                u = urljoin(base_url, u)
            if u not in links:
                links.append(u)
    return links


def has_tender_content(html: str) -> bool:
    """Check if page has tender/procurement content."""
    if not html or len(html) < 100:
        return False
    text = re.sub(r"<[^>]+>", " ", html).lower()
    return bool(TENDER_KEYWORDS.search(text))


def parse_tender_items(html: str, base_url: str) -> list[dict]:
    """Heuristic parse: look for blocks with tender-like content."""
    items = []
    if not html:
        return items
    doc_links = extract_doc_links(html, base_url)
    title_pat = re.compile(r"<h[2-4][^>]*>([^<]+)</h[2-4]>", re.I)
    titles = title_pat.findall(html)
    for t in titles[:20]:
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) > 10 and TENDER_KEYWORDS.search(t):
            items.append({
                "title": t[:200],
                "published_date": None,
                "closing_date": None,
                "document_links": doc_links[:10],
                "contact_info": {},
            })
    if not items and doc_links:
        items.append({
            "title": "Tender documents",
            "published_date": None,
            "closing_date": None,
            "document_links": doc_links,
            "contact_info": {},
        })
    return items


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_doc(url: str, dest: Path) -> bool:
    """Download a document to dest."""
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["curl", "-skL", "-o", str(dest), "--max-time", "60", url],
            capture_output=True,
            timeout=70,
            check=True,
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def _get_contact_from_readme(inst_dir: Path) -> list[str]:
    emails = []
    readme = inst_dir / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for m in EMAIL_RE.finditer(text):
            e = m.group(0).lower()
            if "@" in e and ".png" not in e and "example@" not in e:
                emails.append(e)
    return list(dict.fromkeys(emails))[:5]


def _update_scrape_state(inst_dir: Path, slug: str, status: str, tender_count: int, doc_count: int, error: str | None = None):
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "institution": slug,
        "last_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w", encoding="utf-8") as f:
        json.dump(last, f, indent=2)
    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        with open(log_path, encoding="utf-8") as f:
            log = json.load(f)
    log["runs"] = log.get("runs", []) + [{
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }]
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def process_institution(slug: str, url: str, name: str) -> tuple[str, int, int]:
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    html, err = fetch_url(url)
    if err:
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error=err)
        return ("error", 0, 0)
    if not html or len(html) < 200:
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error="Empty or minimal response")
        return ("error", 0, 0)
    items = parse_tender_items(html, base_url=url)
    doc_links = extract_doc_links(html, url)
    has_tender = has_tender_content(html) or items or doc_links
    tender_count = 0
    doc_count = 0
    if has_tender and (items or doc_links):
        year = datetime.now(timezone.utc).year
        for i, item in enumerate(items[:10]):
            tid_base = slug.split(".")[0].split("-")[0].upper()[:10]
            tid = f"{tid_base}-{year}-{i+1:03d}"
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": item.get("title", "Tender"),
                "description": "",
                "published_date": item.get("published_date"),
                "closing_date": item.get("closing_date"),
                "document_links": item.get("document_links", []),
                "contact_info": item.get("contact_info", {}),
                "source_url": url,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            tender_path = inst_dir / "tenders" / "active" / f"{tid}.json"
            with open(tender_path, "w", encoding="utf-8") as f:
                json.dump(tender_json, f, indent=2, ensure_ascii=False)
            tender_count += 1
            dl_dir = inst_dir / "downloads" / tid / "original"
            ext_dir = inst_dir / "downloads" / tid / "extracted"
            dl_dir.mkdir(parents=True, exist_ok=True)
            ext_dir.mkdir(parents=True, exist_ok=True)
            for durl in (item.get("document_links") or [])[:5]:
                fname = Path(urlparse(durl).path).name or "document.pdf"
                dest = dl_dir / fname
                if download_doc(durl, dest):
                    doc_count += 1
        if not items and doc_links:
            tid_base = slug.split(".")[0].split("-")[0].upper()[:10]
            tid = f"{tid_base}-{year}-001"
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": "Documents",
                "document_links": doc_links,
                "source_url": url,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            (inst_dir / "tenders" / "active" / f"{tid}.json").parent.mkdir(parents=True, exist_ok=True)
            with open(inst_dir / "tenders" / "active" / f"{tid}.json", "w", encoding="utf-8") as f:
                json.dump(tender_json, f, indent=2, ensure_ascii=False)
            tender_count = 1
            dl_dir = inst_dir / "downloads" / tid / "original"
            dl_dir.mkdir(parents=True, exist_ok=True)
            for durl in doc_links[:5]:
                fname = Path(urlparse(durl).path).name or "document.pdf"
                if download_doc(durl, dl_dir / fname):
                    doc_count += 1
        _update_scrape_state(inst_dir, slug, "success", tender_count, doc_count)
        return ("success", tender_count, doc_count)
    # No tenders -> create lead
    emails = extract_emails(html)
    if not emails:
        emails = _get_contact_from_readme(inst_dir)
    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails[:5],
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path, encoding="utf-8") as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    if slug not in existing_slugs:
        leads.append(lead)
        with open(leads_path, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
    _update_scrape_state(inst_dir, slug, "no_tenders", 0, 0)
    return ("no_tenders", 0, 0)


def main():
    for i, (slug, url, name) in enumerate(INSTITUTIONS):
        if i > 0:
            time.sleep(RATE_LIMIT)
        try:
            status, tc, dc = process_institution(slug, url, name)
        except Exception as e:
            status, tc, dc = "error", 0, 0
            inst_dir = PROJECT / "institutions" / slug
            ensure_dirs(inst_dir)
            _update_scrape_state(inst_dir, slug, "error", 0, 0, error=str(e))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], cwd=PROJECT, capture_output=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
