#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260313_205329_batch127
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch127"

INSTITUTIONS = [
    "viseletraining",
    "visionfund",
    "vitalwellness",
    "vlsmartsolutions",
    "vmg",
    "vodacomaccelerator",
    "volunteerkivolex",
    "voyohede",
    "vpo",
    "vrb",
    "vtech",
    "vukatimbers",
    "vwonders",
    "wachapoaching",
    "waendelee",
    "wated",
    "waterinstitute",
    "waterweys",
    "wauzaji",
    "wayatek",
    "wazalendosaccos",
    "waziri",
    "wazoefu",
    "wazohost",
    "wazolangu",
]

DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|rfp|rfq|eoi|rfi|manunuzi|invitation to bid|procurement|bid|supply)\b",
    re.I
)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug):
    path = PROJECT / "institutions" / slug / "README.md"
    if not path.exists():
        return None, None, None
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                fm = yaml.safe_load(parts[1])
                inst = fm.get("institution", {}) or {}
                web = fm.get("website", {}) or {}
                return (
                    web.get("tender_url") or web.get("homepage", ""),
                    inst.get("name", slug),
                    fm.get("contact", {}) or {}
                )
            except Exception:
                pass
            fm = parts[1]
            tender_url = None
            homepage = None
            for m in re.finditer(r"tender_url:\s*[\"']?([^\"'\n]+)[\"']?", fm):
                tender_url = m.group(1).strip()
                break
            for m in re.finditer(r"homepage:\s*[\"']?([^\"'\n]+)[\"']?", fm):
                homepage = m.group(1).strip()
                break
            name = slug
            for m in re.finditer(r"name:\s*[\"']([^\"']+)[\"']", fm):
                name = m.group(1).strip()
                break
            return (tender_url or homepage, name, {})
    return None, None, None


def fetch_url(url, timeout=30):
    try:
        result = subprocess.run(
            ["curl", "-skL", "-A", "Mozilla/5.0 (compatible; TendersBot/1.0)", "--max-time", str(timeout), url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        return None
    return None


def extract_emails(html):
    if not html:
        return []
    seen = set()
    out = []
    for m in EMAIL_RE.finditer(html):
        e = m.group(0).lower()
        if e not in seen and "@" in e and not any(x in e for x in [".png", ".jpg", ".gif", ".svg", "example@", "wixpress", "schema.org", "gravatar", "w3.org"]):
            seen.add(e)
            out.append(e)
    return out[:10]


def extract_doc_links(html, base_url):
    if not html:
        return []
    links = []
    for ext in DOC_EXTENSIONS:
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


def has_tender_content(html):
    if not html or len(html) < 100:
        return False
    text = re.sub(r"<[^>]+>", " ", html).lower()
    return bool(TENDER_KEYWORDS.search(text))


def parse_tender_items(html, base_url):
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


def ensure_dirs(inst_dir):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_doc(url, dest):
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


def extract_text_from_doc(filepath, extracted_dir):
    """Extract text from PDF/DOCX/XLSX using tools package."""
    try:
        ext = filepath.suffix.lower()
        out_name = filepath.stem + (".txt" if ext != ".xlsx" else ".json")
        out_path = extracted_dir / out_name
        if ext == ".pdf":
            r = subprocess.run(
                [sys.executable, "-m", "tools", "pdf", "read", str(filepath)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if r.returncode == 0 and r.stdout:
                out_path.write_text(r.stdout, encoding="utf-8")
                return True
        elif ext == ".docx":
            r = subprocess.run(
                [sys.executable, "-m", "tools", "docx", "read", str(filepath)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if r.returncode == 0 and r.stdout:
                out_path.write_text(r.stdout, encoding="utf-8")
                return True
        elif ext == ".xlsx":
            r = subprocess.run(
                [sys.executable, "-m", "tools", "xlsx", "read", str(filepath), "--format", "json"],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if r.returncode == 0 and r.stdout:
                out_path.write_text(r.stdout, encoding="utf-8")
                return True
    except Exception:
        pass
    return False


def _get_contact_from_readme(inst_dir):
    emails = []
    readme = inst_dir / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for m in EMAIL_RE.finditer(text):
            e = m.group(0).lower()
            if "@" in e and ".png" not in e and "example@" not in e:
                emails.append(e)
    return list(dict.fromkeys(emails))[:5]


def _update_scrape_state(inst_dir, slug, status, tender_count, doc_count, error=None):
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


def process_institution(slug):
    tender_url, inst_name, contact = load_readme(slug)
    if not tender_url:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error="No README or tender_url")
        return "error", 0, 0

    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html = fetch_url(tender_url)
    if not html or len(html) < 200:
        err = "Fetch failed or empty response"
        if "Account Suspended" in html or "suspended" in html.lower():
            err = "Account suspended"
        _update_scrape_state(inst_dir, slug, "error", 0, 0, error=err)
        return "error", 0, 0

    items = parse_tender_items(html, base_url=tender_url)
    doc_links = extract_doc_links(html, tender_url)
    has_tender = has_tender_content(html) or items or doc_links

    tender_count = 0
    doc_count = 0

    if has_tender and (items or doc_links):
        year = datetime.now(timezone.utc).year
        for i, item in enumerate(items[:10]):
            tid = f"{slug.upper()[:4]}-{year}-{i+1:03d}"
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": item.get("title", "Tender"),
                "description": "",
                "published_date": item.get("published_date"),
                "closing_date": item.get("closing_date"),
                "document_links": item.get("document_links", []),
                "contact_info": item.get("contact_info", {}),
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

            for durl in (item.get("document_links") or [])[:10]:
                fname = Path(urlparse(durl).path).name or "document.pdf"
                dest = dl_dir / fname
                if download_doc(durl, dest):
                    doc_count += 1
                    extract_text_from_doc(dest, ext_dir)

        if not items and doc_links:
            tid = f"{slug.upper()[:4]}-{year}-001"
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
            for durl in doc_links[:10]:
                fname = Path(urlparse(durl).path).name or "document.pdf"
                if download_doc(durl, dl_dir / fname):
                    doc_count += 1
                    extract_text_from_doc(dl_dir / fname, ext_dir)

        _update_scrape_state(inst_dir, slug, "success", tender_count, doc_count)
        return "success", tender_count, doc_count

    emails = extract_emails(html)
    if not emails:
        emails = _get_contact_from_readme(inst_dir)
    contact = contact or {}
    contact_emails = contact.get("email") or contact.get("alternate_emails") or []
    if isinstance(contact_emails, str):
        contact_emails = [contact_emails]
    for e in contact_emails:
        if e and e not in emails:
            emails.insert(0, e)

    lead = {
        "institution_slug": slug,
        "institution_name": inst_name or slug,
        "website_url": tender_url,
        "emails": emails[:5],
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {inst_name or slug} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name or slug}",
        "draft_email_body": f"Dear {inst_name or slug} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst_name or slug}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
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
    return "no_tenders", 0, 0


def main():
    for slug in INSTITUTIONS:
        try:
            status, tc, dc = process_institution(slug)
        except Exception as e:
            status, tc, dc = "error", 0, 0
            inst_dir = PROJECT / "institutions" / slug
            inst_dir.mkdir(parents=True, exist_ok=True)
            _update_scrape_state(inst_dir, slug, "error", 0, 0, error=str(e))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")

    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], cwd=PROJECT, capture_output=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
