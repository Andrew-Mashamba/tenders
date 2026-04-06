#!/usr/bin/env python3
"""Scrape 25 institutions for active tenders. Run ID: run_20260315_060430_batch81"""
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request
import urllib.error

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch81"

INSTITUTIONS = [
    "myloafricalimited", "mymam", "mypickup", "mzigeassociates", "mzumbesec",
    "na", "na7etechnology", "nabaki", "nabereractk", "nachingweadc", "nacp",
    "nacte", "nafakakilimo", "nafgemtanzania", "najram", "nakarahotels",
    "nam", "nanine", "nanyumbudc", "nao", "napah", "napendaadventures",
    "narco", "narinatrogonsafarisltd", "nasaha",
]

TENDER_KEYWORDS = [
    "tender", "tenders", "zabuni", "manunuzi", "procurement", "rfp", "rfi",
    "request for proposal", "request for quotation", "bid", "bidding",
    "vacancy", "vacancies", "nafasi", "kazi",
]

DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug: str) -> dict | None:
    """Load institution README and parse YAML frontmatter."""
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    import yaml
    try:
        data = yaml.safe_load(parts[1])
    except Exception:
        return None
    return data


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL and return (html, error)."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, str(e.reason) if e.reason else str(e)
    except Exception as e:
        return None, str(e)


def parse_tenders(html: str, base_url: str, slug: str) -> list[dict]:
    """Parse HTML for tender-like content. Returns list of tender dicts."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []
    soup = BeautifulSoup(html, "html.parser")
    tenders = []
    seen_titles = set()
    year = datetime.now().year
    seq = 1

    # Find document links
    doc_links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if any(href.lower().endswith(ext) for ext in DOC_EXTENSIONS):
            full = urljoin(base_url, href)
            if slug.replace("_", "") in full.lower() or base_url in full:
                doc_links.append({"url": full, "text": (a.get_text() or "").strip()[:200]})

    # Look for tender-like sections
    for tag in soup.find_all(["article", "div", "li", "tr", "section"]):
        text = tag.get_text(separator=" ", strip=True).lower()
        if not any(kw in text for kw in TENDER_KEYWORDS):
            continue
        title_el = tag.find(["h1", "h2", "h3", "h4", "a"])
        title = (title_el.get_text(strip=True) if title_el else "")[:300] or text[:200]
        if not title or title in seen_titles:
            continue
        seen_titles.add(title)

        # Extract dates
        date_el = tag.find(class_=re.compile(r"date|closing|published|time", re.I))
        date_str = date_el.get_text(strip=True) if date_el else ""

        tender_id = f"{slug.upper().replace('-', '')[:8]}-{year}-{seq:03d}"
        seq += 1

        # Get doc links within this block
        block_docs = []
        for a in tag.find_all("a", href=True):
            href = a.get("href", "")
            if any(href.lower().endswith(ext) for ext in DOC_EXTENSIONS):
                block_docs.append(urljoin(base_url, href))

        tenders.append({
            "tender_id": tender_id,
            "institution": slug,
            "title": title,
            "description": text[:1000],
            "published_date": date_str or datetime.now().strftime("%Y-%m-%d"),
            "closing_date": "",
            "source_url": base_url,
            "document_links": block_docs or [d["url"] for d in doc_links[:5]],
            "contact": {},
            "status": "active",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

    # If we found doc links but no structured tenders, create one
    if doc_links and not tenders:
        tender_id = f"{slug.upper().replace('-', '')[:8]}-{year}-001"
        tenders.append({
            "tender_id": tender_id,
            "institution": slug,
            "title": f"Tender/Procurement documents - {slug}",
            "description": "Documents found on tender page.",
            "published_date": datetime.now().strftime("%Y-%m-%d"),
            "closing_date": "",
            "source_url": base_url,
            "document_links": [d["url"] for d in doc_links],
            "contact": {},
            "status": "active",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

    return tenders


def extract_emails(html: str) -> list[str]:
    """Extract email addresses from HTML."""
    emails = set(EMAIL_PATTERN.findall(html))
    return sorted(e for e in emails if not any(
        x in e.lower() for x in ["example.com", "domain.com", "email.com", "wixpress", "sentry"]
    ))


def download_file(url: str, dest: Path) -> bool:
    """Download file to dest. Returns True on success."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(resp.read())
            return True
    except Exception:
        return False


def extract_doc_text(filepath: Path) -> str:
    """Extract text from PDF/DOCX/XLSX."""
    ext = filepath.suffix.lower()
    try:
        if ext == ".pdf":
            from tools.pdf.reader import extract_text
            return extract_text(str(filepath))
        if ext == ".docx":
            from tools.docx.reader import extract_text
            return extract_text(str(filepath))
        if ext in (".xls", ".xlsx"):
            from tools.xlsx.reader import extract_text
            return extract_text(str(filepath))
    except Exception:
        pass
    return ""


def ensure_dirs(inst_dir: Path):
    """Ensure tender and download dirs exist."""
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def process_institution(slug: str) -> tuple[str, int, int]:
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    config = load_readme(slug)
    if not config:
        return "error", 0, 0

    website = config.get("website", {}) or {}
    tender_url = website.get("tender_url") or website.get("homepage") or ""
    if not tender_url:
        return "error", 0, 0

    inst_name = (config.get("institution") or {})
    if isinstance(inst_name, dict):
        inst_name = inst_name.get("name", slug)
    else:
        inst_name = str(inst_name)

    # Rate limit
    time.sleep(2)

    html, err = fetch_url(tender_url)
    if err:
        _write_last_scrape(inst_dir, "error", 0, err)
        _append_scrape_log(inst_dir, "error", 0, 0, [err])
        return "error", 0, 0

    tenders = parse_tenders(html, tender_url, slug)
    doc_count = 0

    if tenders:
        for t in tenders:
            tid = t["tender_id"]
            tender_path = inst_dir / "tenders" / "active" / f"{tid}.json"
            download_dir = inst_dir / "downloads" / tid / "original"
            extract_dir = inst_dir / "downloads" / tid / "extracted"

            docs = t.get("document_links", [])
            downloaded = []
            for i, url in enumerate(docs[:20]):  # Limit 20 docs per tender
                try:
                    parsed = urlparse(url)
                    fname = Path(parsed.path).name or f"doc_{i+1}.pdf"
                    if "?" in fname:
                        fname = fname.split("?")[0]
                    if not any(fname.lower().endswith(ext) for ext in DOC_EXTENSIONS):
                        fname += ".pdf"
                    dest = download_dir / fname
                    if download_file(url, dest):
                        doc_count += 1
                        downloaded.append({"url": url, "local_path": str(dest)})
                        # Extract text
                        extract_dir.mkdir(parents=True, exist_ok=True)
                        txt = extract_doc_text(dest)
                        if txt:
                            (extract_dir / f"{dest.stem}.txt").write_text(txt, encoding="utf-8")
                except Exception:
                    pass

            t["documents"] = downloaded
            tender_path.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")

        _write_last_scrape(inst_dir, "success", len(tenders), None)
        _append_scrape_log(inst_dir, "success", len(tenders), doc_count, [])
        return "success", len(tenders), doc_count

    # No tenders: create lead
    emails = extract_emails(html)
    contact = config.get("contact", {}) or {}
    if isinstance(contact, dict):
        ce = contact.get("email") or ""
        alt = contact.get("alternate_emails") or []
        if isinstance(ce, str) and ce:
            alt = [ce] + (alt if isinstance(alt, list) else [])
        alt = [a for a in alt if isinstance(a, str) and "@" in a]
        emails = list(set(emails + alt))
    emails = [e for e in emails if e and "@" in e][:10]

    opp_type = "sell"
    opp_desc = f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."

    draft_subject = f"Partnership Opportunity – ZIMA Solutions & {inst_name}"
    draft_body = f"""Dear {inst_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""

    lead = {
        "institution_slug": slug,
        "institution_name": inst_name,
        "website_url": tender_url,
        "emails": emails,
        "opportunity_type": opp_type,
        "opportunity_description": opp_desc,
        "draft_email_subject": draft_subject,
        "draft_email_body": draft_body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }

    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        try:
            leads = json.loads(leads_path.read_text(encoding="utf-8"))
            if not isinstance(leads, list):
                leads = leads.get("leads", []) or []
        except Exception:
            leads = []

    # Avoid duplicate
    if not any(l.get("institution_slug") == slug for l in leads):
        leads.append(lead)
        leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

    _write_last_scrape(inst_dir, "no_tenders", 0, None)
    _append_scrape_log(inst_dir, "no_tenders", 0, 0, [])
    return "no_tenders", 0, 0


def _write_last_scrape(inst_dir: Path, status: str, count: int, error: str | None):
    data = {
        "institution": inst_dir.name,
        "last_scrape": datetime.now(timezone.utc).isoformat(),
        "next_scrape": datetime.now(timezone.utc).isoformat(),
        "active_tenders_count": count,
        "status": status,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def _append_scrape_log(inst_dir: Path, status: str, tenders: int, docs: int, errors: list):
    log_path = inst_dir / "scrape_log.json"
    runs = []
    if log_path.exists():
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
            runs = data.get("runs", []) or []
        except Exception:
            pass
    runs.append({
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tenders,
        "documents_downloaded": docs,
        "errors": errors,
    })
    log_path.write_text(json.dumps({"runs": runs[-100:]}, indent=2), encoding="utf-8")


def main():
    print(f"Run ID: {RUN_ID}")
    print(f"Institutions: {len(INSTITUTIONS)}")
    print("-" * 60)

    for slug in INSTITUTIONS:
        try:
            status, tender_count, doc_count = process_institution(slug)
            print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
        except Exception as e:
            inst_dir = PROJECT / "institutions" / slug
            ensure_dirs(inst_dir)
            _write_last_scrape(inst_dir, "error", 0, str(e))
            _append_scrape_log(inst_dir, "error", 0, 0, [str(e)])
            print(f"RESULT|{slug}|error|0|0  # {e}")

    # Sync leads CSV
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        import subprocess
        subprocess.run(["python3", str(sync_script)], cwd=str(PROJECT), check=False)

    print("-" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
