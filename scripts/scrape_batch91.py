#!/usr/bin/env python3
"""Scrape 25 institutions for active tenders. Run ID: run_20260315_060430_batch91"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch91"

INSTITUTIONS = [
    ("pelefina", "Pelefina", "https://pelefina.co.tz/"),
    ("penguinlogistics", "Penguin Logistics Tanzania", "https://www.penguinlogistics.co.tz/"),
    ("penuelinvestment", "Penuel's Investment", "https://penuelinvestment.co.tz/"),
    ("pepsitanzania", "SBC - Pepsi", "https://www.sbctanzania.co.tz/"),
    ("pepsitz", "SBC - Pepsi", "https://www.sbctanzania.co.tz/"),
    ("perfectfoods", "Perfect Foods", "https://perfectfoods.co.tz/"),
    ("perfectmachineryltd", "Perfect Machinery Ltd", "https://perfectmachineryltd.co.tz/"),
    ("perterms", "Perterms", "https://perterms.co.tz/"),
    ("pesacapital", "Pesa Capital", "https://pesacapital.co.tz/"),
    ("pesatu", "PesaTu", "https://pesatu.co.tz/bashe-akabidhi-magari-yenye-thamani-ya-tsh-bilioni-4-2/"),
    ("pesno", "Pesno", "https://pesno.co.tz/"),
    ("pestguard", "Pest Guard Limited", "https://pestguard.co.tz/"),
    ("petmos", "PETMOS", "https://petmos.co.tz/"),
    ("petroafrica", "Petroafrica", "https://petroafrica.co.tz/"),
    ("petrogroup", "Petro Group", "https://petrogroup.co.tz/"),
    ("petsville", "PetsVille", "https://petsville.co.tz/"),
    ("pfc", "Peace for Conservation", "https://pfc.or.tz/"),
    ("pff", "Professional Freight Forwarders", "https://pff.co.tz/"),
    ("pga", "Portwise Global Agencies", "https://www.pga.co.tz/"),
    ("pgwocade", "PGWOCADE", "https://pgwocade.or.tz/"),
    ("phsrf", "PHSRF", "https://phsrf.or.tz/"),
    ("pieradvocates", "PIER Advocates", "https://pieradvocates.co.tz/"),
    ("pihas", "Peramiho Institute", "https://pihas.ac.tz/"),
    ("piifleet", "PII LTD", "https://piifleet.co.tz/"),
    ("pimak", "Pimak Professional Kitchen", "https://pimak.co.tz/"),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|procurement|rfp|rfi|eoi|expression of interest|"
    r"request for proposal|request for quotation|zabuni|bid\s+document)\b",
    re.I
)

DOC_EXT = re.compile(r'href=["\']([^"\']*\.(?:pdf|doc|docx|xls|xlsx|zip))["\']', re.I)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", "--max-time", str(timeout), url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}"
        return r.stdout or "", None
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


def has_tender_listings(html: str, url: str) -> bool:
    """Check if page contains tender/procurement listings."""
    if not html or len(html) < 100:
        return False
    if not TENDER_KEYWORDS.search(html):
        return False
    if DOC_EXT.search(html):
        return True
    date_like = re.compile(r'\b(20\d{2}-\d{2}-\d{2}|closing|deadline|submission)\b', re.I)
    if date_like.search(html):
        return True
    return False


def extract_doc_urls(html: str, base_url: str) -> list[tuple[str, str]]:
    """Extract (url, filename) for document links."""
    seen = set()
    docs = []
    for m in DOC_EXT.finditer(html):
        path = m.group(1)
        if path.startswith("//"):
            full_url = "https:" + path
        elif path.startswith("/"):
            parsed = urlparse(base_url)
            full_url = f"{parsed.scheme}://{parsed.netloc}{path}"
        elif path.startswith("http"):
            full_url = path
        else:
            full_url = urljoin(base_url, path)
        if full_url in seen:
            continue
        seen.add(full_url)
        filename = Path(urlparse(full_url).path).name or "document.pdf"
        docs.append((full_url, filename))
    return docs


def extract_emails(html: str) -> list[str]:
    """Extract email addresses from HTML."""
    seen = set()
    emails = []
    for m in EMAIL_PATTERN.finditer(html):
        e = m.group(0).lower()
        if e not in seen and "example" not in e and "test" not in e and "sentry" not in e:
            seen.add(e)
            emails.append(e)
    return emails


def ensure_dirs(inst_dir: Path) -> None:
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)


def download_document(url: str, dest: Path, timeout: int = 60) -> bool:
    """Download a document via curl. Returns True on success."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["curl", "-sL", "-A", "Mozilla/5.0", "--max-time", str(timeout), "-o", str(dest), url],
        capture_output=True,
        timeout=timeout + 5,
    )
    return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0


def extract_text_from_doc(doc_path: Path, extracted_dir: Path) -> bool:
    """Extract text from PDF/DOCX/XLSX using tools module. Returns True on success."""
    try:
        ext = doc_path.suffix.lower()
        txt_path = extracted_dir / (doc_path.stem + ".txt")
        if ext == ".pdf":
            r = subprocess.run(
                [sys.executable, "-m", "tools", "pdf", "read", str(doc_path)],
                cwd=str(PROJECT),
                capture_output=True,
                text=True,
                timeout=60,
            )
        elif ext in (".docx", ".doc"):
            r = subprocess.run(
                [sys.executable, "-m", "tools", "docx", "read", str(doc_path)],
                cwd=str(PROJECT),
                capture_output=True,
                text=True,
                timeout=60,
            )
        elif ext in (".xlsx", ".xls"):
            r = subprocess.run(
                [sys.executable, "-m", "tools", "xlsx", "read", str(doc_path), "--format", "json"],
                cwd=str(PROJECT),
                capture_output=True,
                text=True,
                timeout=60,
            )
            txt_path = extracted_dir / (doc_path.stem + ".json")
        else:
            return False
        if r.returncode == 0 and r.stdout:
            extracted_dir.mkdir(parents=True, exist_ok=True)
            txt_path.write_text(r.stdout, encoding="utf-8")
            return True
    except Exception:
        pass
    return False


def update_last_scrape(inst_dir: Path, status: str, tender_count: int = 0, error: str | None = None) -> None:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    data = {
        "institution": inst_dir.name,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
        "run_id": RUN_ID,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def append_scrape_log(inst_dir: Path, run: dict) -> None:
    log_path = inst_dir / "scrape_log.json"
    if log_path.exists():
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"runs": []}
    else:
        data = {"runs": []}
    data.setdefault("runs", []).append(run)
    log_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def append_lead(slug: str, name: str, url: str, emails: list[str], opportunity_type: str, description: str) -> bool:
    """Append lead if not already present. Returns True if added."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        try:
            raw = json.loads(leads_path.read_text(encoding="utf-8"))
            leads = raw if isinstance(raw, list) else raw.get("leads", [])
        except json.JSONDecodeError:
            pass

    if any(l.get("institution_slug") == slug for l in leads):
        return False

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    subject = f"Partnership Opportunity – ZIMA Solutions & {name}"
    body = f"""Dear {name} Team,

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
"""
    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": opportunity_type,
        "opportunity_description": description,
        "draft_email_subject": subject,
        "draft_email_body": body,
        "created_at": now,
        "status": "pending",
    }
    leads.append(lead)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def process_institution(slug: str, name: str, url: str) -> tuple[str, int, int]:
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        update_last_scrape(inst_dir, "error", 0, err)
        append_scrape_log(inst_dir, {
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "duration_seconds": 0,
            "status": "error",
            "tenders_found": 0,
            "documents_downloaded": 0,
            "errors": [err],
        })
        return ("error", 0, 0)

    if html and ("Account Suspended" in html or "This Account has been suspended" in html):
        update_last_scrape(inst_dir, "suspended", 0, "Account suspended")
        append_scrape_log(inst_dir, {
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "duration_seconds": 0,
            "status": "suspended",
            "tenders_found": 0,
            "documents_downloaded": 0,
            "errors": ["Account suspended"],
        })
        return ("suspended", 0, 0)

    has_tenders = has_tender_listings(html, url)
    tender_count = 0
    doc_count = 0

    if has_tenders:
        docs = extract_doc_urls(html, url)
        if docs:
            # Create one tender record for documents found in tender context
            slug_upper = slug.upper().replace("-", "")
            tender_id = f"{slug_upper}-2026-001"
            tender_dir = inst_dir / "downloads" / tender_id
            orig_dir = tender_dir / "original"
            ext_dir = tender_dir / "extracted"
            orig_dir.mkdir(parents=True, exist_ok=True)
            ext_dir.mkdir(parents=True, exist_ok=True)

            now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            document_records = []
            for doc_url, filename in docs[:10]:  # Limit to 10 docs per tender
                safe_name = re.sub(r'[^\w.\-]', '_', filename)[:100]
                dest = orig_dir / safe_name
                if download_document(doc_url, dest):
                    doc_count += 1
                    document_records.append({
                        "filename": safe_name,
                        "original_url": doc_url,
                        "local_path": f"downloads/{tender_id}/original/{safe_name}",
                        "downloaded_at": now,
                    })
                    extract_text_from_doc(dest, ext_dir)

            if document_records:
                tender_json = {
                    "tender_id": tender_id,
                    "institution": slug,
                    "title": f"Procurement/Tender Documents - {name}",
                    "description": f"Documents extracted from {url}",
                    "published_date": "",
                    "closing_date": "",
                    "closing_time": "",
                    "category": "General",
                    "status": "active",
                    "source_url": url,
                    "documents": document_records,
                    "contact": {},
                    "scraped_at": now,
                    "last_checked": now,
                }
                (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(
                    json.dumps(tender_json, indent=2), encoding="utf-8"
                )
                tender_count = 1

    if tender_count > 0:
        update_last_scrape(inst_dir, "success", tender_count)
        append_scrape_log(inst_dir, {
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "duration_seconds": 0,
            "status": "success",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "errors": [],
        })
        return ("success", tender_count, doc_count)

    # No tenders: add lead
    emails = extract_emails(html)
    if not emails:
        readme = inst_dir / "README.md"
        if readme.exists():
            emails = extract_emails(readme.read_text(encoding="utf-8"))
    append_lead(
        slug, name, url, emails,
        "sell",
        f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
    )
    update_last_scrape(inst_dir, "no_tenders", 0)
    append_scrape_log(inst_dir, {
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "duration_seconds": 0,
        "status": "no_tenders",
        "tenders_found": 0,
        "documents_downloaded": 0,
        "errors": [],
    })
    return ("no_tenders", 0, 0)


def main():
    new_leads = []
    for slug, name, url in INSTITUTIONS:
        status, tender_count, doc_count = process_institution(slug, name, url)
        if status == "no_tenders":
            new_leads.append(slug)
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    if new_leads:
        subprocess.run(
            [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
            cwd=str(PROJECT),
            check=False,
        )


if __name__ == "__main__":
    main()
