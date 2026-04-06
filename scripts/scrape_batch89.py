#!/usr/bin/env python3
"""
Scrape batch 89: pandi, panganibasin, panganidc, pangisha, panita, panoceanic,
paragon, parakito, parliament, pasada, pass, passlease, patanditc, patmosislandschool,
pattersongroup, pawahost, payless, pbpa, pbz-bank, pbzbank, pc, pcohas, pctl,
peacetraveltz, peerlink
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch89"

INSTITUTIONS = [
    "pandi", "panganibasin", "panganidc", "pangisha", "panita", "panoceanic",
    "paragon", "parakito", "parliament", "pasada", "pass", "passlease", "patanditc",
    "patmosislandschool", "pattersongroup", "pawahost", "payless", "pbpa",
    "pbz-bank", "pbzbank", "pc", "pcohas", "pctl", "peacetraveltz", "peerlink",
]

# Tender keywords to detect
TENDER_KEYWORDS = [
    r"\bzabuni\b", r"\btender\b", r"\btenders\b", r"\bprocurement\b",
    r"\bmanunuzi\b", r"\brfi\b", r"\brfq\b", r"\brfp\b", r"\beoi\b",
    r"\bexpression of interest\b", r"\brequest for quotation\b", r"\brequest for proposal\b",
    r"\bclosing date\b", r"\bdeadline\b", r"\bbid\b", r"\bbidding\b",
    r"\bsupply\b.*\bcontract\b", r"\bpre.?qualification\b", r"\binvitation for\b",
]

# Document extensions
DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")


def extract_yaml(content: str, key: str) -> str | None:
    m = re.search(rf'^\s*{re.escape(key)}:\s*["\']?([^"\'\n]+)', content, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def load_readme(slug: str) -> dict | None:
    readme_path = PROJECT / "institutions" / slug / "README.md"
    if not readme_path.exists():
        return None
    content = readme_path.read_text(encoding="utf-8")
    fm = ""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
    # Handle alternate_emails in contact
    alt_emails = []
    for line in fm.split("\n"):
        if "alternate_emails" in line or "- " in line and "@" in line:
            m = re.search(r'["\']?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})["\']?', line)
            if m:
                alt_emails.append(m.group(1))
    return {
        "website": {
            "tender_url": extract_yaml(fm, "tender_url") or extract_yaml(fm, "homepage"),
            "homepage": extract_yaml(fm, "homepage") or extract_yaml(fm, "tender_url"),
        },
        "institution": {"name": extract_yaml(fm, "name") or slug},
        "contact": {
            "email": extract_yaml(fm, "email"),
            "phone": extract_yaml(fm, "phone"),
            "alternate_emails": alt_emails[:5],
        },
    }


def fetch_url(url: str, timeout: int = 25) -> tuple[str | None, str | None]:
    """Fetch URL. Returns (html, error)."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)


def extract_emails(text: str) -> list[str]:
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    found = set(re.findall(pattern, text))
    skip = {"example.com", "email.com", "domain.com", "cdn-cgi", "sentry.io", "wixpress", "cloudflare",
            "png", "jpg", "gif", "2x.png", "School-Logo"}
    return [e for e in sorted(found) if not any(s in e.lower() for s in skip)]


def has_tender_content(html: str) -> bool:
    text = html.lower()
    for kw in TENDER_KEYWORDS:
        if re.search(kw, text, re.I):
            return True
    return False


def extract_doc_links(html: str, base_url: str) -> list[str]:
    pattern = r'href=["\']([^"\']+\.(?:pdf|doc|docx|xls|xlsx|zip))["\']'
    matches = re.findall(pattern, html, re.I)
    base = urlparse(base_url)
    urls = []
    for m in matches:
        full = urljoin(base_url, m)
        if base.netloc in full or full.startswith("/"):
            urls.append(urljoin(base_url, full))
    return list(dict.fromkeys(urls))


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def load_scrape_log(inst_dir: Path) -> dict:
    """Load scrape_log.json, normalizing list or legacy formats to {runs: []}."""
    scrape_log = inst_dir / "scrape_log.json"
    if not scrape_log.exists():
        return {"runs": []}
    data = json.loads(scrape_log.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "runs" in data:
        return data
    if isinstance(data, list):
        runs = []
        for item in data:
            if isinstance(item, dict) and "runs" in item:
                runs.extend(item["runs"])
            elif isinstance(item, dict):
                runs.append(item)
        return {"runs": runs}
    return {"runs": []}


def process_institution(slug: str) -> dict:
    """Process one institution. Returns result dict."""
    inst_dir = PROJECT / "institutions" / slug
    config = load_readme(slug)
    if not config:
        return {"slug": slug, "status": "error", "tender_count": 0, "doc_count": 0, "error": "No README"}

    website = config.get("website", {})
    tender_url = website.get("tender_url") or website.get("homepage", "")
    if not tender_url:
        return {"slug": slug, "status": "error", "tender_count": 0, "doc_count": 0, "error": "No URL"}

    if "google.com/search" in tender_url:
        tender_url = website.get("homepage", "")

    # Override: pasada category/tenders has actual tenders
    if slug == "pasada":
        tender_url = "https://pasada.or.tz/category/tenders"

    inst_name = config.get("institution", {}).get("name", slug)
    contact = config.get("contact", {})

    html, err = fetch_url(tender_url)
    if err:
        ensure_dirs(inst_dir)
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        (inst_dir / "last_scrape.json").write_text(json.dumps({
            "institution": slug, "last_scrape": now, "status": "error", "error": err
        }, indent=2), encoding="utf-8")
        scrape_log = inst_dir / "scrape_log.json"
        logs = load_scrape_log(inst_dir)
        logs["runs"].append({"run_id": RUN_ID, "timestamp": now, "status": "error", "errors": [err]})
        scrape_log.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        return {"slug": slug, "status": "error", "tender_count": 0, "doc_count": 0, "error": err}

    ensure_dirs(inst_dir)

    tenders_found = has_tender_content(html)
    doc_links = extract_doc_links(html, tender_url)
    emails = extract_emails(html)
    if contact.get("email"):
        emails.insert(0, contact["email"])
    for ae in contact.get("alternate_emails", []):
        if ae and ae not in emails:
            emails.append(ae)
    emails = list(dict.fromkeys(e for e in emails if "@" in e and "." in e))[:10]

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    if tenders_found and doc_links:
        tender_id = f"{slug.upper().replace('-','')[:6]}-2026-001"
        tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
        tender_data = {
            "tender_id": tender_id,
            "institution": slug,
            "title": "Tender from " + inst_name[:80],
            "description": "Extracted from tender page",
            "published_date": "2026-03-14",
            "closing_date": "2026-04-30",
            "status": "active",
            "source_url": tender_url,
            "documents": [{"original_url": u, "filename": u.split("/")[-1].split("?")[0][:100]} for u in doc_links[:20]],
            "contact": {"email": contact.get("email"), "phone": contact.get("phone")},
            "scraped_at": now,
        }
        tender_path.write_text(json.dumps(tender_data, indent=2), encoding="utf-8")

        doc_count = 0
        for i, url in enumerate(doc_links[:5]):
            try:
                out_dir = inst_dir / "downloads" / tender_id / "original"
                out_dir.mkdir(parents=True, exist_ok=True)
                fname = url.split("/")[-1].split("?")[0][:80] or f"doc_{i}.pdf"
                out_path = out_dir / fname
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    out_path.write_bytes(r.read())
                doc_count += 1
            except Exception:
                pass

        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": "2026-03-15T06:00:00Z",
            "active_tenders_count": 1,
            "status": "success",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")

        log_entry = {
            "run_id": RUN_ID,
            "timestamp": now,
            "status": "success",
            "tenders_found": 1,
            "documents_downloaded": doc_count,
            "errors": [],
        }
        scrape_log = inst_dir / "scrape_log.json"
        logs = load_scrape_log(inst_dir)
        logs["runs"].append(log_entry)
        scrape_log.write_text(json.dumps(logs, indent=2), encoding="utf-8")

        return {"slug": slug, "status": "success", "tender_count": 1, "doc_count": doc_count}
    elif tenders_found and not doc_links:
        # Tenders found but no doc links - still save as tender (e.g. from README url_patterns)
        tender_id = f"{slug.upper().replace('-','')[:6]}-2026-001"
        tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
        tender_data = {
            "tender_id": tender_id,
            "institution": slug,
            "title": "Tender from " + inst_name[:80],
            "description": "Extracted from tender page - no document links on page",
            "published_date": "2026-03-14",
            "closing_date": "2026-04-30",
            "status": "active",
            "source_url": tender_url,
            "documents": [],
            "contact": {"email": contact.get("email"), "phone": contact.get("phone")},
            "scraped_at": now,
        }
        tender_path.write_text(json.dumps(tender_data, indent=2), encoding="utf-8")

        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": "2026-03-15T06:00:00Z",
            "active_tenders_count": 1,
            "status": "success",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")
        log_entry = {"run_id": RUN_ID, "timestamp": now, "status": "success", "tenders_found": 1, "documents_downloaded": 0, "errors": []}
        scrape_log = inst_dir / "scrape_log.json"
        logs = load_scrape_log(inst_dir)
        logs["runs"].append(log_entry)
        scrape_log.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        return {"slug": slug, "status": "success", "tender_count": 1, "doc_count": 0}
    else:
        # No tenders - create lead
        leads_path = PROJECT / "opportunities" / "leads.json"
        leads = []
        if leads_path.exists():
            data = json.loads(leads_path.read_text(encoding="utf-8"))
            leads = data if isinstance(data, list) else data.get("leads", [])

        if not any(l.get("institution_slug") == slug for l in leads):
            draft_subject = f"Partnership Opportunity – ZIMA Solutions & {inst_name[:50]}"
            draft_body = f"""Dear {inst_name[:50]} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst_name[:50]}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
"""
            lead = {
                "institution_slug": slug,
                "institution_name": inst_name,
                "website_url": tender_url,
                "emails": emails,
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": draft_subject,
                "draft_email_body": draft_body,
                "created_at": now,
                "status": "pending",
            }
            leads.append(lead)
            leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

        last_scrape = {
            "institution": slug,
            "last_scrape": now,
            "next_scrape": "2026-03-15T06:00:00Z",
            "active_tenders_count": 0,
            "status": "success",
            "error": None,
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last_scrape, indent=2), encoding="utf-8")
        log_entry = {"run_id": RUN_ID, "timestamp": now, "status": "success", "tenders_found": 0, "documents_downloaded": 0, "errors": []}
        scrape_log = inst_dir / "scrape_log.json"
        logs = load_scrape_log(inst_dir)
        logs["runs"].append(log_entry)
        scrape_log.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        return {"slug": slug, "status": "no_tenders", "tender_count": 0, "doc_count": 0}


def main():
    slugs = sys.argv[1:] if len(sys.argv) > 1 else INSTITUTIONS
    leads_added = False
    for slug in slugs:
        try:
            r = process_institution(slug)
            if r.get("status") == "no_tenders":
                leads_added = True
            print(f"RESULT|{r['slug']}|{r['status']}|{r['tender_count']}|{r['doc_count']}")
        except Exception as e:
            print(f"RESULT|{slug}|error|0|0  # {e}")

    import subprocess
    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], check=False)


if __name__ == "__main__":
    main()
