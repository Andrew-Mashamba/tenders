#!/usr/bin/env python3
"""
Scrape batch 18 institutions: btelesec through buwasa.
Run ID: run_20260315_060430_batch18
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
RUN_ID = "run_20260315_060430_batch18"

# (slug, tender_url, institution_name) - from READMEs
INSTITUTIONS = [
    ("btelesec", "https://btelesec.co.tz/", "Beyond Telesec Ltd"),
    ("btx", "https://btx.co.tz/", "BTX Tanzania Limited"),
    ("buchosadc", "https://buchosadc.go.tz/tenders", "Buchosa District Council"),
    ("buckreef", "https://buckreef.co.tz/", "Buckreef Gold"),
    ("budget", "https://www.budget.co.tz/", "Budget Car Rentals"),
    ("budgetfreightltd", "https://budgetfreightltd.co.tz/", "Budget Freight Limited"),
    ("bugando", "https://bugando.ac.tz/procurement.php", "Catholic University of Health and Allied Sciences"),
    ("buhigwedc", "https://buhigwedc.go.tz/tenders", "Buhigwe District Council"),
    ("buildmart", "https://buildmart.co.tz/", "Buildmart Limited"),
    ("bukobadc", "https://bukobadc.go.tz/event/watumishi-wajengewa-uwezo-matumizi-ya-mfumo-wa-manunuzi-nest", "Bukoba District Council"),
    ("bukobamc", "https://bukobamc.go.tz/procurement-and-supply-management", "Bukoba Municipal Council"),
    ("bumbulidc", "http://bumbulidc.go.tz/tenders", "Bumbuli District Council"),
    ("bundahospital", "https://bundahospital.co.tz/", "Bunda Hospital"),
    ("bunge", "https://www.parliament.go.tz/", "Bunge (Tanzania Parliament)"),
    ("bureauveritas", "https://www.bureauveritas.co.tz/", "Bureau Veritas Tanzania"),
    ("burhaniinfosys", "https://burhaniinfosys.co.tz/", "Burhani Infosys Ltd"),
    ("bushandforest", "https://bushandforest.co.tz/", "Bush and Forest Collections"),
    ("bushbucksafaris", "https://www.bushbuckltd.com/", "Bushbuck Safaris"),
    ("bushlink", "https://bushlink.co.tz/", "BushLink Agro-Venture Ltd"),
    ("business", "https://business.go.tz/", "TNBP (Tanzania National Business Portal)"),
    ("businesstimes", "https://businesstimes.co.tz/", "Business Times"),
    ("busokelodc", "https://busokelodc.go.tz/procurement-and-supplies", "Busokelo District Council"),
    ("butchershop", "https://butchershop.co.tz/", "Butcher Shop"),
    ("butimbatc", "https://butimbatc.ac.tz/", "Butimba Teacher's College"),
    ("buwasa", "https://nest.go.tz/tenders/published-tenders", "BUWASA"),
]

TENDER_KEYWORDS = re.compile(
    r"tender|zabuni|procurement|manunuzi|request for (proposal|quotation|information)|rfi|eoi|rfp|rfq|bid\s+(document|notice)|invitation to bid",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error). Uses -k for SSL issues."""
    try:
        r = subprocess.run(
            ["curl", "-skL", "-A", "Mozilla/5.0", "--connect-timeout", "15", "--max-time", "30", url],
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
    if TENDER_KEYWORDS.search(html):
        if any(x in html.lower() for x in [".pdf", "closing date", "closing_date", "reference number", "reference_number", "tender document", "bid document", "zabuni", "manunuzi"]):
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
            ["curl", "-skL", "-o", str(dest), "-A", "Mozilla/5.0", "--connect-timeout", "20", "--max-time", "60", url],
            capture_output=True, timeout=65, check=True
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def extract_text_from_doc(doc_path: Path, extracted_dir: Path) -> bool:
    """Extract text from PDF/DOCX using tools module."""
    try:
        ext = doc_path.suffix.lower()
        base = doc_path.stem
        out_txt = extracted_dir / f"{base}.txt"
        if ext == ".pdf":
            r = subprocess.run(
                [sys.executable, "-m", "tools", "pdf", "read", str(doc_path)],
                capture_output=True, text=True, timeout=30, cwd=str(PROJECT)
            )
            if r.returncode == 0 and r.stdout:
                out_txt.write_text(r.stdout[:500000], encoding="utf-8")
                return True
        elif ext in (".docx", ".doc"):
            r = subprocess.run(
                [sys.executable, "-m", "tools", "docx", "read", str(doc_path)],
                capture_output=True, text=True, timeout=30, cwd=str(PROJECT)
            )
            if r.returncode == 0 and r.stdout:
                out_txt.write_text(r.stdout[:500000], encoding="utf-8")
                return True
        elif ext in (".xlsx", ".xls"):
            r = subprocess.run(
                [sys.executable, "-m", "tools", "xlsx", "read", str(doc_path), "--format", "json"],
                capture_output=True, text=True, timeout=30, cwd=str(PROJECT)
            )
            if r.returncode == 0 and r.stdout:
                (extracted_dir / f"{base}.json").write_text(r.stdout[:500000], encoding="utf-8")
                return True
    except Exception:
        pass
    return False


# Known document URLs from READMEs for gov sites that may need them
KNOWN_DOCS = {
    "buchosadc": [
        "https://buchosadc.go.tz/storage/app/uploads/public/667/d64/963/667d649639df3613803168.pdf",
        "https://buchosadc.go.tz/storage/app/uploads/public/5de/1ae/654/5de1ae654cb2f326088574.pdf",
        "https://buchosadc.go.tz/storage/app/uploads/public/59c/b9e/13a/59cb9e13a71e1854195128.pdf",
        "https://buchosadc.go.tz/storage/app/uploads/public/5cc/d23/5c6/5ccd235c6eade854852053.pdf",
    ],
    "buhigwedc": [
        "https://buhigwedc.go.tz/storage/app/uploads/public/669/a3d/e51/669a3de512db7676544581.pdf",
        "https://buhigwedc.go.tz/storage/app/uploads/public/612/5e5/383/6125e53836b0b672006482.pdf",
        "https://buhigwedc.go.tz/storage/app/uploads/public/669/a3d/197/669a3d1973a12087144613.pdf",
    ],
    "bukobadc": [
        "https://bukobadc.go.tz/storage/app/uploads/public/682/2d5/1a1/6822d51a16edc918078000.pdf",
        "https://bukobadc.go.tz/storage/app/uploads/public/682/2d4/455/6822d4455e59a245136801.pdf",
    ],
    "bukobamc": [
        "https://bukobamc.go.tz/storage/app/uploads/public/68d/b93/b16/68db93b165c51601904779.pdf",
        "https://bukobamc.go.tz/storage/app/uploads/public/67c/e90/7f8/67ce907f89c93895671483.pdf",
    ],
    "bumbulidc": [
        "http://bumbulidc.go.tz/storage/app/uploads/public/63f/756/640/63f756640d7a8847417079.pdf",
        "http://bumbulidc.go.tz/storage/app/uploads/public/63a/98d/cf0/63a98dcf011de250925076.pdf",
    ],
    "busokelodc": [
        "https://busokelodc.go.tz/storage/app/uploads/public/684/15d/748/68415d748b8b7565079505.pdf",
        "https://busokelodc.go.tz/storage/app/uploads/public/666/198/ecb/666198ecbdc4e859026186.pdf",
    ],
    "buildmart": [
        "https://buildmart.co.tz/wp-content/uploads/2025/06/NEW-COMPANY-PROFILE.pdf",
    ],
}


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
    # Add known docs from README if page has tender content but few doc links
    if slug in KNOWN_DOCS and (has_tender_content(html or "") or len(doc_links) < 3):
        for u in KNOWN_DOCS[slug]:
            if not any(d["url"] == u for d in doc_links):
                doc_links.append({"url": u, "filename": os.path.basename(urlparse(u).path) or "document.pdf"})

    has_tenders = has_tender_content(html or "")

    tender_count = 0
    doc_count = 0

    if (has_tenders or doc_links) and doc_links:
        tender_id = f"{slug.upper().replace('-', '')}-2026-001"
        tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
        download_dir = inst_dir / "downloads" / tender_id / "original"
        extracted_dir = inst_dir / "downloads" / tender_id / "extracted"
        download_dir.mkdir(parents=True, exist_ok=True)
        extracted_dir.mkdir(parents=True, exist_ok=True)

        docs = []
        for d in doc_links[:15]:
            fname = (d["filename"].replace("%20", "_")[:100] or "document.pdf")
            dest = download_dir / fname
            if download_document(d["url"], dest):
                doc_count += 1
                docs.append({
                    "filename": dest.name,
                    "original_url": d["url"],
                    "local_path": str(dest.relative_to(PROJECT)),
                })
                extract_text_from_doc(dest, extracted_dir)

        tender_data = {
            "tender_id": tender_id,
            "institution": slug,
            "title": f"Tender from {name}",
            "source_url": url,
            "published_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "closing_date": None,
            "status": "active",
            "documents": docs,
            "contact": {},
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
        try:
            status, tender_count, doc_count = process_institution(slug, url, name)
        except Exception as e:
            status, tender_count, doc_count = "error", 0, 0
            inst_dir = PROJECT / "institutions" / slug
            write_last_scrape(inst_dir, "error", 0, str(e))
            append_scrape_log(inst_dir, "error", 0, 0, str(e))
        results.append((slug, status, tender_count, doc_count))
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        if tender_count == 0 and status == "success":
            html, _ = fetch_url(url)
            emails = extract_emails(html or "", url) if html else []
            if not emails:
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

    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], capture_output=True, cwd=str(PROJECT))

    return 0


if __name__ == "__main__":
    sys.exit(main())
