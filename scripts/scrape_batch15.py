#!/usr/bin/env python3
"""
Scrape batch 15 institutions: bimapap through bme.
Run ID: run_20260315_060430_batch15
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch15"
INSTITUTIONS = [
    ("bimapap", "https://www.bimapap.co.tz/", "Insurance | BimaPap"),
    ("bimasokoni", "https://bimasokoni.co.tz/", "BimaSokoni"),
    ("bimtech", "https://bimtech.co.tz/", "BIMTECH"),
    ("binzubeiry", "https://www.binzubeiry.co.tz/", "BIN ZUBEIRY SPORTS"),
    ("biosolution", "https://biosolution.co.tz/", "Biosolution"),
    ("bismatraders", "https://bismatraders.co.tz/", "Bisma Traders"),
    ("bison", "https://bison.co.tz/", "Bison Engineering"),
    ("bkassociates", "https://bkassociates.co.tz/", "BK Associates"),
    ("bklogistics", "https://bklogistics.co.tz/", "BK Logistics"),
    ("blackball", "https://blackball.co.tz/", "Black Ball"),
    ("blackunicornstudios", "https://www.blackunicornstudios.co.tz/", "Black Unicorn Studio"),
    ("blc", "https://www.blc.co.tz/", "BLC Investments"),
    ("blinds", "https://blinds.co.tz/", "RENZO Blinds"),
    ("blrc", "https://blrc.go.tz/", "BLRC"),
    ("bluechiptechnologies", "https://bluechiptechnologies.co.tz/", "Bluechip Technologies"),
    ("bluecrosstanzania", "https://bluecrosstanzania.or.tz/", "Blue Cross Tanzania"),
    ("blueeconomysmz", "https://blueeconomysmz.go.tz/service/utoaji-wa-vibali-vya-usafirishaji-wa-bidhaa-za-mazao-ya-baharini-nje-ya-nchi/", "WUBU Blue Economy"),
    ("bluefinsolutions", "https://bluefinsolutions.co.tz/", "Bluefin Solutions"),
    ("bluerecruits", "https://bluerecruits.co.tz/", "Blue Recruits"),
    ("bluestar", "https://bluestar.co.tz/", "Blue Star Luxury"),
    ("bluestone", "https://bluestone.co.tz/", "Bluestone"),
    ("bluesystems", "https://bluesystems.co.tz/", "Blue Systems"),
    ("bluetrain", "https://www.bluetrain.africa/", "Bluetrain"),
    ("bluewave", "https://bluewave.co.tz/", "Blue Wave Island Boat Trips"),
    ("bme", "https://www.bme.co.tz/", "Black Mountain Enterprises"),
]

TENDER_KEYWORDS = re.compile(
    r"tender|zabuni|procurement|manunuzi|request for (proposal|quotation|information)|rfi|eoi|rfp|rfq|bid\s+(document|notice)|invitation to bid",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0", "--connect-timeout", "15", "--max-time", "30", url],
            capture_output=True, text=True, timeout=35
        )
        if r.returncode == 0:
            return r.stdout, None
        return None, f"curl exit {r.returncode}"
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


def extract_emails(html: str, base_url: str) -> list[str]:
    """Extract unique valid emails from HTML."""
    emails = set()
    for m in EMAIL_PATTERN.finditer(html):
        e = m.group(0).lower()
        if not any(x in e for x in ["example.com", "domain.com", "yoursite", "email.com", "sentry", "wix.com", "parastorage", "blogger", "google", "facebook", "twitter", "gravatar", "schema.org"]):
            emails.add(e)
    return sorted(emails)


def has_tender_content(html: str) -> bool:
    """Check if page has formal tender/procurement notices."""
    if not html or len(html) < 500:
        return False
    # Look for structured tender indicators
    if TENDER_KEYWORDS.search(html):
        # Exclude generic footer/legal text
        if "procurement of substitute" in html.lower() or "procurement of goods" in html.lower():
            return False
        # Check for tender listing structure
        if any(x in html.lower() for x in [".pdf", "closing date", "closing_date", "reference number", "reference_number", "tender document", "bid document"]):
            return True
    return False


def find_document_links(html: str, base_url: str) -> list[dict]:
    """Find PDF/DOC/DOCX/XLS/XLSX/ZIP links."""
    links = []
    for ext in DOC_EXT:
        pat = re.compile(rf'href\s*=\s*["\']([^"\']*\{re.escape(ext)}[^"\']*)["\']', re.I)
        for m in pat.finditer(html):
            url = m.group(1).strip()
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("/"):
                url = urljoin(base_url, url)
            elif not url.startswith("http"):
                url = urljoin(base_url, url)
            if url and url not in [l["url"] for l in links]:
                links.append({"url": url, "filename": os.path.basename(urlparse(url).path) or f"document{ext}"})
    return links


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def write_last_scrape(inst_dir: Path, status: str, tender_count: int, error: str | None = None):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "institution": inst_dir.name,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
        "run_id": RUN_ID,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(data, f, indent=2)


def append_scrape_log(inst_dir: Path, status: str, tender_count: int, doc_count: int, err: str | None = None):
    log_path = inst_dir / "scrape_log.json"
    runs = []
    if log_path.exists():
        try:
            data = json.loads(log_path.read_text())
            runs = data.get("runs", [])
        except Exception:
            pass
    runs.append({
        "run_id": RUN_ID,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [err] if err else [],
    })
    with open(log_path, "w") as f:
        json.dump({"runs": runs[-100:]}, f, indent=2)


def download_document(url: str, dest: Path) -> bool:
    try:
        subprocess.run(
            ["curl", "-sL", "-o", str(dest), "-A", "Mozilla/5.0", "--connect-timeout", "20", "--max-time", "60", url],
            capture_output=True, timeout=65, check=True
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def process_institution(slug: str, url: str, name: str) -> tuple[str, int, int]:
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        write_last_scrape(inst_dir, "error", 0, err)
        append_scrape_log(inst_dir, "error", 0, 0, err)
        return "error", 0, 0

    doc_links = find_document_links(html or "", url)
    has_tenders = has_tender_content(html or "")

    # blueeconomysmz: known document from README
    if slug == "blueeconomysmz" and not doc_links:
        doc_links = [{"url": "https://blueeconomysmz.go.tz/wp-content/uploads/2026/02/VIINGILIO-VYA-MAENEO-YA-HIFADHI-ZA-BAHARI.pdf", "filename": "VIINGILIO-VYA-MAENEO-YA-HIFADHI-ZA-BAHARI.pdf"}]
        has_tenders = True

    tender_count = 0
    doc_count = 0

    if (has_tenders or doc_links) and doc_links:
        # Create tender record and download docs
        tender_id = f"{slug.upper().replace('-', '')}-2026-001"
        tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
        download_dir = inst_dir / "downloads" / tender_id / "original"
        extracted_dir = inst_dir / "downloads" / tender_id / "extracted"
        download_dir.mkdir(parents=True, exist_ok=True)
        extracted_dir.mkdir(parents=True, exist_ok=True)

        docs = []
        for d in doc_links[:10]:  # Limit to 10 docs per tender
            dest = download_dir / (d["filename"].replace("%20", "_")[:100])
            if download_document(d["url"], dest):
                doc_count += 1
                docs.append({
                    "filename": dest.name,
                    "original_url": d["url"],
                    "local_path": str(dest.relative_to(PROJECT)),
                })

        tender_data = {
            "tender_id": tender_id,
            "institution": slug,
            "title": f"Tender from {name}",
            "source_url": url,
            "published_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "closing_date": None,
            "status": "active",
            "documents": docs,
            "scraped_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_id": RUN_ID,
        }
        with open(tender_path, "w") as f:
            json.dump(tender_data, f, indent=2)
        tender_count = 1

    write_last_scrape(inst_dir, "success", tender_count)
    append_scrape_log(inst_dir, "success", tender_count, doc_count)
    return "success", tender_count, doc_count


def create_lead(slug: str, name: str, url: str, emails: list[str]) -> dict:
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, ICT services, or partnership.",
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
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "pending",
    }


def main():
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        try:
            data = json.loads(leads_path.read_text())
            leads = data if isinstance(data, list) else data.get("leads", [])
        except Exception:
            pass

    results = []
    for slug, url, name in INSTITUTIONS:
        status, tender_count, doc_count = process_institution(slug, url, name)
        results.append((slug, status, tender_count, doc_count))
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        if tender_count == 0 and status == "success":
            html, _ = fetch_url(url)
            emails = extract_emails(html or "", url) if html else []
            if not emails:
                # Use README contact if available
                readme = PROJECT / "institutions" / slug / "README.md"
                if readme.exists():
                    txt = readme.read_text()
                    emails = list(set(EMAIL_PATTERN.findall(txt)))
                    emails = [e for e in emails if "REMOVETHIS" not in e and "example" not in e][:5]
            lead = create_lead(slug, name, url, emails[:5])
            if not any(l.get("institution_slug") == slug for l in leads):
                leads.append(lead)

    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Sync leads CSV
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], capture_output=True, cwd=str(PROJECT))

    return 0


if __name__ == "__main__":
    sys.exit(main())
