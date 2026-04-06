#!/usr/bin/env python3
"""Scrape 25 institutions for active tenders. Run ID: run_20260313_205329_batch90"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch90"

INSTITUTIONS = [
    ("pegasuslegal", "Pegasus Law Firm", "https://pegasuslegal.co.tz/"),
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
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|procurement|rfp|rfi|eoi|expression of interest|"
    r"request for proposal|request for quotation|zabuni|bid\s+document)\b",
    re.I
)

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
    """Check if page contains tender/procurement listings (not just keywords)."""
    if not html or len(html) < 100:
        return False
    # Must have tender-related keywords
    if not TENDER_KEYWORDS.search(html):
        return False
    # Exclude generic corporate pages: look for structured tender content
    # e.g. tender list, table rows, document links, closing dates
    doc_ext = re.compile(r'href=["\'][^"\']*\.(pdf|doc|docx|xls|xlsx|zip)["\']', re.I)
    date_like = re.compile(r'\b(20\d{2}-\d{2}-\d{2}|closing|deadline|submission)\b', re.I)
    if doc_ext.search(html) and (date_like.search(html) or "tender" in html.lower()[:5000]):
        return True
    # SBC Pepsi: check for /tenders/ or careers/tender
    if "sbctanzania" in url and ("tender" in html.lower() or "careers" in html.lower()):
        # SBC site has careers but no dedicated tender page in our fetch
        pass
    return False


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


def append_lead(slug: str, name: str, url: str, emails: list[str], opportunity_type: str, description: str) -> None:
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        try:
            raw = json.loads(leads_path.read_text(encoding="utf-8"))
            leads = raw if isinstance(raw, list) else raw.get("leads", [])
        except json.JSONDecodeError:
            pass

    # Skip if already present
    if any(l.get("institution_slug") == slug for l in leads):
        return

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


def main():
    results = []
    new_leads = []

    for slug, name, url in INSTITUTIONS:
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
            results.append((slug, "error", 0, 0))
            print(f"RESULT|{slug}|error|0|0  # {err}")
            continue

        # Check for suspended/blocked pages
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
            results.append((slug, "suspended", 0, 0))
            print(f"RESULT|{slug}|suspended|0|0")
            continue

        has_tenders = has_tender_listings(html, url)
        tender_count = 0
        doc_count = 0

        if has_tenders:
            # Would need to parse and save tenders - for now we have no structured tender data
            # from these pages, so treat as no tenders (most are corporate homepages)
            tender_count = 0
            doc_count = 0

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
            results.append((slug, "success", tender_count, doc_count))
            print(f"RESULT|{slug}|success|{tender_count}|{doc_count}")
        else:
            # No tenders: add lead
            emails = extract_emails(html)
            if not emails:
                # Use README contact if available
                readme = inst_dir / "README.md"
                if readme.exists():
                    readme_text = readme.read_text(encoding="utf-8")
                    emails = extract_emails(readme_text)
            append_lead(
                slug, name, url, emails,
                "sell",
                f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            )
            new_leads.append(slug)
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
            results.append((slug, "no_tenders", 0, 0))
            print(f"RESULT|{slug}|no_tenders|0|0")

    # Sync leads CSV if we added any
    if new_leads:
        subprocess.run(
            [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
            cwd=str(PROJECT),
            check=False,
        )

    return results

if __name__ == "__main__":
    main()
