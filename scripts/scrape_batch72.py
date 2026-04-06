#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260315_060430_batch72
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
RUN_ID = "run_20260315_060430_batch72"
RATE_LIMIT = 10

INSTITUTIONS = [
    "mayzon", "mazingira", "mbalimbali", "mbaralidc", "mbeyacc", "mbeyadc",
    "mbeyarrh", "mbeyauwsa", "mbingatc", "mbmdaikin", "mbochiherbalife",
    "mbogomining", "mbuludc", "mbulutc", "mccohas", "mcelack", "mcellemo",
    "mcf", "mcm", "mcm-int", "mcms", "mcmsz", "mct", "mdh", "mdopeiddehotel",
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfi|eoi|bid|quotation|supply|rfq)\b",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug: str) -> dict | None:
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                cfg = yaml.safe_load(parts[1])
                return cfg or {}
            except Exception:
                pass
    m = re.search(r"tender_url:\s*[\"']?([^\"'\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1).strip()}}
    m = re.search(r"\*\*Tender Page:\*\*\s*(https?://[^\s]+)", text)
    if m:
        return {"website": {"tender_url": m.group(1).strip().rstrip("/")}}
    return None


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
            return None, f"curl exit {r.returncode}: {(r.stderr or '')[:200]}"
        return r.stdout or None, None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def extract_emails(html: str) -> list[str]:
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
    if not html:
        return []
    links = []
    parsed = urlparse(base_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    for ext in DOC_EXT:
        pat = re.compile(rf'href=["\']([^"\']*\{re.escape(ext)}[^"\']*)["\']', re.I)
        for m in pat.finditer(html):
            u = m.group(1).strip().split("?")[0]
            if u.startswith("//"):
                u = "https:" + u
            elif u.startswith("/"):
                u = base + u
            elif not u.startswith("http"):
                u = urljoin(base_url, u)
            if u not in links:
                links.append(u)
    return links


def has_tender_content(html: str) -> bool:
    if not html or len(html) < 100:
        return False
    text = re.sub(r"<[^>]+>", " ", html).lower()
    return bool(TENDER_KEYWORDS.search(text))


def parse_nest_tenders(html: str, base_url: str, slug: str) -> list[dict]:
    """Parse NEST-style government tender tables (Zabuni Zaidi, Jina la Zabuni)."""
    tenders = []
    if not html:
        return tenders
    parsed = urlparse(base_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    doc_links = extract_doc_links(html, base_url)
    prefix = slug.upper().replace("-", "")[:10]
    year = datetime.now(timezone.utc).year
    # Try table rows: <tr> with doc link - extract title from first td or link text
    tr_pat = re.compile(r"<tr[^>]*>(.*?)</tr>", re.I | re.S)
    link_pat = re.compile(r'href=["\']([^"\']+\.(?:pdf|doc|docx|xls|xlsx|zip))["\'][^>]*>([^<]*)</a>', re.I)
    for tr in tr_pat.finditer(html):
        row = tr.group(1)
        for m in link_pat.finditer(row):
            url, label = m.groups()
            if url.startswith("/"):
                url = base + url
            elif not url.startswith("http"):
                url = urljoin(base_url, url)
            if url not in doc_links:
                doc_links.append(url)
            title = (label or url.split("/")[-1].replace("%20", " ")).strip()
            if len(title) > 2 and "download" not in title.lower()[:20]:
                tid = f"{prefix}-{year}-{len(tenders)+1:03d}"
                tenders.append({
                    "tender_id": tid,
                    "title": title[:200] if title else "Tender document",
                    "published_date": None,
                    "closing_date": None,
                    "document_links": [url],
                    "source_url": base_url,
                })
    if not tenders and doc_links:
        tid = f"{prefix}-{year}-001"
        tenders.append({
            "tender_id": tid,
            "title": "Tender documents",
            "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "closing_date": None,
            "document_links": doc_links,
            "source_url": base_url,
        })
    return tenders


def parse_generic_tenders(html: str, base_url: str, slug: str) -> list[dict]:
    """Generic parse: look for blocks with tender-like content and doc links."""
    items = []
    if not html:
        return items
    doc_links = extract_doc_links(html, base_url)
    prefix = slug.upper().replace("-", "")[:10]
    year = datetime.now(timezone.utc).year
    title_pat = re.compile(r"<h[2-4][^>]*>([^<]+)</h[2-4]>", re.I)
    for t in title_pat.findall(html)[:20]:
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
        if len(t) > 10 and TENDER_KEYWORDS.search(t):
            items.append({
                "tender_id": f"{prefix}-{year}-{len(items)+1:03d}",
                "title": t[:200],
                "published_date": None,
                "closing_date": None,
                "document_links": doc_links[:10],
                "source_url": base_url,
            })
    if not items and doc_links:
        items.append({
            "tender_id": f"{prefix}-{year}-001",
            "title": "Tender documents",
            "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "closing_date": None,
            "document_links": doc_links,
            "source_url": base_url,
        })
    return items


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_doc(url: str, dest: Path) -> bool:
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


def extract_text_from_doc(doc_path: Path, extracted_dir: Path) -> bool:
    """Extract text from PDF/DOCX/XLSX using tools module."""
    try:
        ext = doc_path.suffix.lower()
        out_name = doc_path.stem + ".txt" if ext in (".pdf", ".doc", ".docx") else doc_path.stem + ".json"
        out_path = extracted_dir / out_name
        extracted_dir.mkdir(parents=True, exist_ok=True)
        if ext == ".pdf":
            r = subprocess.run(
                [sys.executable, "-m", "tools", "pdf", "read", str(doc_path)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if r.returncode == 0 and r.stdout:
                out_path.write_text(r.stdout[:500000], encoding="utf-8")
                return True
        elif ext in (".doc", ".docx"):
            r = subprocess.run(
                [sys.executable, "-m", "tools", "docx", "read", str(doc_path)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if r.returncode == 0 and r.stdout:
                out_path.write_text(r.stdout[:500000], encoding="utf-8")
                return True
        elif ext in (".xls", ".xlsx"):
            r = subprocess.run(
                [sys.executable, "-m", "tools", "xlsx", "read", str(doc_path), "--format", "json"],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if r.returncode == 0 and r.stdout:
                out_path.write_text(r.stdout[:500000], encoding="utf-8")
                return True
    except Exception:
        pass
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


def process_institution(slug: str) -> tuple[str, int, int]:
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)
    cfg = load_readme(slug)
    if not cfg:
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error="No README config")
        return ("error", 0, 0)
    tender_url = (cfg.get("website") or {}).get("tender_url")
    inst_name = (cfg.get("institution") or {}).get("name", slug)
    if isinstance(inst_name, str):
        inst_name = re.sub(r"&#\d+;", "", inst_name).strip()
    if not tender_url:
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error="No tender_url")
        return ("error", 0, 0)
    html, err = fetch_url(tender_url)
    if err:
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error=err)
        return ("error", 0, 0)
    if not html or len(html) < 200:
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error="Empty or minimal response")
        return ("error", 0, 0)
    # Government/LGA sites with NEST-style tables
    nest_slugs = ("mbaralidc", "mbeyacc", "mbeyadc", "mbingatc", "mbuludc", "mbulutc")
    if slug in nest_slugs:
        tenders = parse_nest_tenders(html, tender_url, slug)
    else:
        tenders = parse_generic_tenders(html, tender_url, slug)
    doc_links = extract_doc_links(html, tender_url)
    has_tender = has_tender_content(html) or tenders or doc_links
    tender_count = 0
    doc_count = 0
    if has_tender and (tenders or doc_links):
        contact = cfg.get("contact") or {}
        contact_email = contact.get("email") or (contact.get("alternate_emails") or [None])[0]
        for t in tenders[:15]:
            tid = t.get("tender_id", f"{slug.upper()[:10]}-2026-{tender_count+1:03d}")
            doc_urls = t.get("document_links") or []
            if not doc_urls and doc_links:
                doc_urls = doc_links[:5]
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": t.get("title", "Tender"),
                "description": t.get("description", ""),
                "published_date": t.get("published_date"),
                "closing_date": t.get("closing_date"),
                "document_links": doc_urls,
                "contact": {"email": contact_email, "phone": contact.get("phone")} if contact else {},
                "source_url": tender_url,
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
            for durl in doc_urls[:8]:
                fname = Path(urlparse(durl).path).name or "document.pdf"
                dest = dl_dir / fname
                if download_doc(durl, dest):
                    doc_count += 1
                    extract_text_from_doc(dest, ext_dir)
        if not tenders and doc_links:
            prefix = slug.upper().replace("-", "")[:10]
            tid = f"{prefix}-2026-001"
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": "Documents",
                "document_links": doc_links,
                "source_url": tender_url,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            with open(inst_dir / "tenders" / "active" / f"{tid}.json", "w", encoding="utf-8") as f:
                json.dump(tender_json, f, indent=2, ensure_ascii=False)
            tender_count = 1
            dl_dir = inst_dir / "downloads" / tid / "original"
            ext_dir = inst_dir / "downloads" / tid / "extracted"
            dl_dir.mkdir(parents=True, exist_ok=True)
            ext_dir.mkdir(parents=True, exist_ok=True)
            for durl in doc_links[:8]:
                fname = Path(urlparse(durl).path).name or "document.pdf"
                if download_doc(durl, dl_dir / fname):
                    doc_count += 1
                    extract_text_from_doc(dl_dir / fname, ext_dir)
        _update_scrape_state(inst_dir, slug, "success", tender_count, doc_count)
        return ("success", tender_count, doc_count)
    # No tenders -> create lead
    emails = extract_emails(html)
    if not emails:
        emails = _get_contact_from_readme(inst_dir)
    lead = {
        "institution_slug": slug,
        "institution_name": inst_name,
        "website_url": tender_url,
        "emails": emails[:5],
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
        "draft_email_body": f"Dear {inst_name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
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
    for i, slug in enumerate(INSTITUTIONS):
        if i > 0:
            time.sleep(RATE_LIMIT)
        try:
            status, tc, dc = process_institution(slug)
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
