#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.

For each institution:
- If tenders found: save JSON, download docs, extract text
- If no tenders: append to leads.json, run sync_leads_csv
- Update last_scrape.json, scrape_log.json
- Print RESULT|slug|status|tender_count|doc_count
"""
import json
import os
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request

# SSL context that doesn't verify certs (for gov sites with cert issues)
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch56"

INSTITUTIONS = [
    ("jumbo", "Mr. Jumbo Supplies", "https://jumbo.co.tz/"),
    ("jumintech", "jumintech.co.tz", "https://jumintech.co.tz/"),
    ("junaco", "JUNACO", "http://www.junacogroup.com/"),
    ("jvaa", "JV ADVISORY & ADVOCATES", "https://jvaa.co.tz/"),
    ("jvspek", "JV SPEK", "https://jvspek.co.tz/"),
    ("jwempo", "Journal of Water Resources", "https://jwempo.ac.tz/"),
    ("jwt", "Jumuiya ya Wafanyabiashara Tanzania", "https://jwt.or.tz/"),
    ("k2technology", "K2 Technology Limited", "https://k2technology.co.tz/"),
    ("kacce", "Kacce", "https://kacce.or.tz/"),
    ("kachenje", "Kachenje Advocates", "https://kachenje.co.tz/"),
    ("kacultd", "KACU Ltd", "https://kacultd.co.tz/"),
    ("kadacom", "kadacom.co.tz", "https://kadacom.co.tz/"),
    ("kaecobeta", "KAECO TANZANIA LTD", "https://kaecobeta.co.tz/"),
    ("kageni", "Kageni Consulting", "https://kageni.or.tz/"),
    ("kagera", "KAGERA REGIONAL", "https://kagera.go.tz/tenders"),
    ("kagera-sugar", "Kagera Sugar Limited", "https://kagera-sugar.co.tz/"),
    ("kahamatc", "Kahama Municipal Council", "https://kahamatc.go.tz/tenders"),
    ("kahawapakaya", "Pakaya Koffie", "https://www.pakayakoffie.nl/"),
    ("kakakuona", "Kakakuona Resort", "https://www.kakakuona.co.tz/"),
    ("kalamandalam", "Kalamandalam", "https://kalamandalam.or.tz/"),
    ("kalamufoundation", "Kalamu Education Foundation", "https://kalamufoundation.or.tz/"),
    ("kalamutech", "Kalamu Technologies", "https://kalamutech.co.tz/"),
    ("kalax", "KALAX", "https://kalax.co.tz/"),
    ("kalen", "Kalen Limited", "https://kalen.co.tz/"),
    ("kalkaalow", "Kalkaalow Transport LTD", "https://kalkaalow.co.tz/"),
]

TENDER_KEYWORDS = re.compile(
    r"(tender|zabuni|procurement|manunuzi|bid\s+doc|rfp|rfi|request\s+for\s+(proposal|quotation|information)|"
    r"invitation\s+to\s+bid|tender\s+document|closing\s+date|closing\s+date|deadline\s+for)",
    re.I
)

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 45) -> tuple[str | None, str | None]:
    """Fetch URL and return (html, error)."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TenderScraper/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as resp:
            return resp.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)


def has_tender_content(html: str) -> bool:
    """Check if page contains tender-related content."""
    if not html:
        return False
    text = html[:50000]  # limit scan
    return bool(TENDER_KEYWORDS.search(text))


def extract_emails(html: str) -> list[str]:
    """Extract emails from HTML."""
    if not html:
        return []
    found = set()
    for m in EMAIL_PATTERN.finditer(html):
        e = m.group(0).lower()
        if not any(x in e for x in ["example.com", "wixpress", "sentry", "gravatar", "gstatic", "w3.org"]):
            found.add(e)
    return sorted(found)


def extract_doc_links(html: str, base_url: str) -> list[str]:
    """Extract PDF/DOC/DOCX/XLS/XLSX/ZIP links."""
    ext = r"\.(pdf|doc|docx|xls|xlsx|zip)(?:\?|$)"
    pat = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.I)
    found = []
    for m in pat.finditer(html):
        href = m.group(1).strip()
        if re.search(ext, href, re.I):
            full = urljoin(base_url, href)
            if full not in found:
                found.append(full)
    return found


def ensure_dirs(inst_dir: Path):
    """Ensure institution directories exist."""
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_doc(url: str, dest: Path) -> bool:
    """Download a document to dest."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TenderScraper/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(resp.read())
            return True
    except Exception:
        return False


def process_institution(slug: str, name: str, url: str) -> tuple[str, int, int]:
    """
    Process one institution. Returns (status, tender_count, doc_count).
    status: success|error|no_tenders
    """
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        _update_metadata(inst_dir, slug, "error", 0, 0, err)
        return ("error", 0, 0)

    if not has_tender_content(html):
        # No tenders: create opportunity lead
        emails = extract_emails(html)
        if not emails:
            # Try README contact
            readme = inst_dir / "README.md"
            if readme.exists():
                t = readme.read_text(encoding="utf-8")
                for m in EMAIL_PATTERN.finditer(t):
                    e = m.group(0).lower()
                    if "@" in e and "example" not in e:
                        emails.append(e)
        emails = list(dict.fromkeys(emails))[:10]  # dedupe, limit

        lead = {
            "institution_slug": slug,
            "institution_name": name,
            "website_url": url,
            "emails": emails,
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
            "draft_email_body": f"""Dear {name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {name}. Could we schedule a brief call?

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
            except Exception:
                leads = []
        if not isinstance(leads, list):
            leads = leads.get("leads", []) or []
        # Skip if already in leads
        if not any(l.get("institution_slug") == slug for l in leads):
            leads.append(lead)
            leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

        _update_metadata(inst_dir, slug, "no_tenders", 0, 0, None)
        return ("no_tenders", 0, 0)

    # Tenders found: parse and save
    doc_links = extract_doc_links(html, url)
    tender_count = 1  # Assume 1 tender from page or count items
    doc_count = 0
    year = datetime.now().year
    tender_id = f"{slug.upper().replace('-', '')[:6]}-{year}-001"

    tender_data = {
        "tender_id": tender_id,
        "institution": slug,
        "title": f"Tender from {name}",
        "description": "Scraped from tender page.",
        "source_url": url,
        "published_date": datetime.now().strftime("%Y-%m-%d"),
        "closing_date": None,
        "status": "active",
        "contact": {},
        "documents": [],
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }

    download_dir = inst_dir / "downloads" / tender_id
    orig_dir = download_dir / "original"
    ext_dir = download_dir / "extracted"
    orig_dir.mkdir(parents=True, exist_ok=True)
    ext_dir.mkdir(parents=True, exist_ok=True)

    for i, doc_url in enumerate(doc_links[:20]):  # limit
        parsed = urlparse(doc_url)
        fname = os.path.basename(parsed.path) or f"doc_{i+1}.pdf"
        if not re.search(r"\.(pdf|doc|docx|xls|xlsx|zip)$", fname, re.I):
            fname += ".pdf"
        dest = orig_dir / fname
        if download_doc(doc_url, dest):
            doc_count += 1
            tender_data["documents"].append({
                "filename": fname,
                "original_url": doc_url,
                "local_path": str(dest.relative_to(inst_dir)),
            })
            # Extract text if tools available
            try:
                ext_path = ext_dir / (Path(fname).stem + ".txt")
                if fname.lower().endswith(".pdf"):
                    r = subprocess.run(
                        ["python3", "-m", "tools", "pdf", "read", str(dest)],
                        cwd=PROJECT,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if r.returncode == 0 and r.stdout:
                        ext_path.write_text(r.stdout[:50000], encoding="utf-8")
                elif fname.lower().endswith((".docx", ".doc")):
                    r = subprocess.run(
                        ["python3", "-m", "tools", "docx", "read", str(dest)],
                        cwd=PROJECT,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if r.returncode == 0 and r.stdout:
                        ext_path.write_text(r.stdout[:50000], encoding="utf-8")
            except Exception:
                pass

    tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
    tender_path.write_text(json.dumps(tender_data, indent=2, ensure_ascii=False), encoding="utf-8")
    _update_metadata(inst_dir, slug, "success", tender_count, doc_count, None)
    return ("success", tender_count, doc_count)


def _update_metadata(inst_dir: Path, slug: str, status: str, tender_count: int, doc_count: int, error: str | None):
    """Update last_scrape.json and scrape_log.json."""
    now = datetime.now(timezone.utc)
    last = {
        "institution": slug,
        "last_scrape": now.isoformat(),
        "next_scrape": None,
        "active_tenders_count": tender_count,
        "status": "success" if status in ("success", "no_tenders") else "error",
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": now.isoformat(),
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "error": error,
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
    results = []
    for slug, name, url in INSTITUTIONS:
        try:
            status, tc, dc = process_institution(slug, name, url)
        except Exception as e:
            status, tc, dc = "error", 0, 0
            inst_dir = PROJECT / "institutions" / slug
            inst_dir.mkdir(parents=True, exist_ok=True)
            _update_metadata(inst_dir, slug, "error", 0, 0, str(e))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")
        results.append((slug, status, tc, dc))

    # Run sync_leads_csv if any no_tenders
    if any(r[1] == "no_tenders" for r in results):
        sync = PROJECT / "scripts" / "sync_leads_csv.py"
        if sync.exists():
            subprocess.run([sys.executable, str(sync)], cwd=PROJECT, check=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())
