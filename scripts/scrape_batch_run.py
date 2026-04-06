#!/usr/bin/env python3
"""
Scrape a batch of institutions for tenders.
Run: python3 scripts/scrape_batch_run.py loreininvestment losirwasafaris ...
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = os.environ.get("RUN_ID", f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug):
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8")
    # Parse YAML frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            import yaml
            try:
                cfg = yaml.safe_load(parts[1])
                return cfg
            except Exception:
                pass
    return None


def fetch_url(url, timeout=25):
    try:
        r = subprocess.run(
            ["curl", "-sL", "-m", str(timeout), "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def extract_doc_links(html, base_url):
    if not html:
        return []
    links = []
    for ext in DOC_EXT:
        pat = rf'href=["\']([^"\']*\{re.escape(ext)}[^"\']*)["\']'
        for m in re.finditer(pat, html, re.I):
            href = m.group(1).strip()
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                parsed = urlparse(base_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            elif not href.startswith("http"):
                href = urljoin(base_url, href)
            if href and href not in [l["url"] for l in links]:
                links.append({"url": href, "filename": href.split("/")[-1].split("?")[0]})
    return links


def extract_emails(html):
    if not html:
        return []
    return list(dict.fromkeys(EMAIL_RE.findall(html)))


def has_tender_content(html):
    if not html:
        return False
    lower = html.lower()
    keywords = ["zabuni", "tender", "procurement", "manunuzi", "rfp", "rfq", "bid notice", "tender notice"]
    return any(kw in lower for kw in keywords)


def ensure_dirs(inst_dir):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_doc(url, dest_path):
    try:
        subprocess.run(
            ["curl", "-sL", "-m", "60", "-o", str(dest_path), "-A", "Mozilla/5.0", url],
            capture_output=True,
            timeout=65,
            check=True,
        )
        return dest_path.exists() and dest_path.stat().st_size > 0
    except Exception:
        return False


def extract_text_tool(filepath):
    ext = filepath.suffix.lower()
    try:
        if ext == ".pdf":
            r = subprocess.run(
                ["python3", "-m", "tools", "pdf", "read", str(filepath)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return r.stdout if r.returncode == 0 else ""
        if ext in (".docx", ".doc"):
            r = subprocess.run(
                ["python3", "-m", "tools", "docx", "read", str(filepath)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return r.stdout if r.returncode == 0 else ""
        if ext in (".xlsx", ".xls"):
            r = subprocess.run(
                ["python3", "-m", "tools", "xlsx", "read", str(filepath), "--format", "json"],
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return r.stdout if r.returncode == 0 else ""
    except Exception:
        pass
    return ""


def process_institution(slug):
    cfg = load_readme(slug)
    if not cfg:
        return f"RESULT|{slug}|error|0|0"
    inst = cfg.get("institution", {})
    website = cfg.get("website", {})
    tender_url = website.get("tender_url") or website.get("homepage", "")
    inst_name = inst.get("name", slug)
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html = fetch_url(tender_url)
    if html is None:
        # Site down/blocked
        _update_logs(inst_dir, slug, "error", 0, 0, error="fetch_failed")
        return f"RESULT|{slug}|error|0|0"

    doc_links = extract_doc_links(html, tender_url)
    has_tenders = has_tender_content(html)

    # Check for tender listing structure (tables, lists with dates)
    tender_items = []
    if has_tenders or doc_links:
        # Try to find tender-like items
        import re
        # Look for date-like patterns
        date_pat = r"\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\d{4}[/\-]\d{1,2}[/\-]\d{1,2}"
        if re.search(date_pat, html) and (has_tenders or doc_links):
            tender_items = [{"title": "Tender/Procurement", "doc_links": doc_links}]

    if tender_items and (doc_links or has_tenders):
        # Process as tenders found
        tender_count = 0
        doc_count = 0
        year = datetime.now().year
        for i, item in enumerate(tender_items):
            tid = f"{slug.upper()[:4]}-{year}-{i+1:03d}"
            tender_json = {
                "tender_id": tid,
                "institution": slug,
                "title": item.get("title", "Tender/Procurement"),
                "description": "",
                "published_date": datetime.now().strftime("%Y-%m-%d"),
                "closing_date": "",
                "category": "General",
                "status": "active",
                "source_url": tender_url,
                "documents": [],
                "contact": cfg.get("contact", {}),
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            download_dir = inst_dir / "downloads" / tid / "original"
            extract_dir = inst_dir / "downloads" / tid / "extracted"
            download_dir.mkdir(parents=True, exist_ok=True)
            extract_dir.mkdir(parents=True, exist_ok=True)
            for d in item.get("doc_links", doc_links):
                url = d["url"] if isinstance(d, dict) else d
                fn = d.get("filename", url.split("/")[-1].split("?")[0]) if isinstance(d, dict) else url.split("/")[-1].split("?")[0]
                safe_fn = re.sub(r'[^\w\-_.]', '_', fn)[:200]
                dest = download_dir / safe_fn
                if download_doc(url, dest):
                    doc_count += 1
                    tender_json["documents"].append({
                        "filename": safe_fn,
                        "original_url": url,
                        "local_path": str(dest.relative_to(inst_dir)),
                    })
                    txt_path = extract_dir / (Path(safe_fn).stem + ".txt")
                    txt = extract_text_tool(dest)
                    if txt:
                        txt_path.write_text(txt, encoding="utf-8")
            tender_path = inst_dir / "tenders" / "active" / f"{tid}.json"
            tender_path.write_text(json.dumps(tender_json, indent=2), encoding="utf-8")
            tender_count += 1
        _update_logs(inst_dir, slug, "success", tender_count, doc_count)
        return f"RESULT|{slug}|success|{tender_count}|{doc_count}"
    else:
        # No tenders - create lead
        emails = extract_emails(html)
        contact = cfg.get("contact", {})
        if contact.get("email"):
            emails.insert(0, contact["email"])
        emails = list(dict.fromkeys(e for e in emails if "@" in e and "example" not in e.lower()))
        lead = {
            "institution_slug": slug,
            "institution_name": inst_name,
            "website_url": tender_url,
            "emails": emails[:10],
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
            "draft_email_body": f"""Dear {inst_name} Team,

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
""",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending",
        }
        leads_path = PROJECT / "opportunities" / "leads.json"
        leads = []
        if leads_path.exists():
            try:
                leads = json.loads(leads_path.read_text(encoding="utf-8"))
                if not isinstance(leads, list):
                    leads = leads.get("leads", [])
            except Exception:
                leads = []
        if not any(l.get("institution_slug") == slug for l in leads):
            leads.append(lead)
            leads_path.parent.mkdir(parents=True, exist_ok=True)
            leads_path.write_text(json.dumps(leads, indent=2), encoding="utf-8")
        _update_logs(inst_dir, slug, "no_tenders", 0, 0)
        return f"RESULT|{slug}|no_tenders|0|0"


def _update_logs(inst_dir, slug, status, tender_count, doc_count, error=None):
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "institution": slug,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
    log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    log_data = {"runs": []}
    if log_path.exists():
        try:
            log_data = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    log_data.setdefault("runs", []).append(log_entry)
    log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")


def main():
    slugs = sys.argv[1:] if len(sys.argv) > 1 else []
    if not slugs:
        print("Usage: python3 scrape_batch_run.py slug1 slug2 ...")
        sys.exit(1)
    for slug in slugs:
        try:
            out = process_institution(slug.strip())
            print(out)
        except Exception as e:
            print(f"RESULT|{slug}|error|0|0")
            inst_dir = PROJECT / "institutions" / slug
            if inst_dir.exists():
                _update_logs(inst_dir, slug, "error", 0, 0, error=str(e))


if __name__ == "__main__":
    main()
