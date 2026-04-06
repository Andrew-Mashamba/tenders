#!/usr/bin/env python3
"""
Batch scrape script for run_20260313_205329_batch16.
Scrapes 25 institutions: bmtelecomms through bradda.
"""
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch16"
RATE_LIMIT = 10  # seconds between requests

# Tender keywords (Swahili/English)
TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|zabuni|manunuzi|procurement|rfp|rfq|eoi|expression of interest|"
    r"request for proposal|request for quotation|bid|bidding|prequalification|"
    r"supply|quotation|invitation to bid)\b",
    re.I,
)

# Document extensions
DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar")

INSTITUTIONS = [
    {"slug": "bmtelecomms", "name": "BM Telecomms & Networks", "url": "https://bmtelecomms.co.tz/", "contact": {"email": "info@bmtelecomms.co.tz"}},
    {"slug": "bmz", "name": "Zanzibar Examinations Council", "url": "https://eprocurement.zppda.go.tz/", "contact": {"email": "info@bmz.go.tz"}},
    {"slug": "bnc", "name": "BNC", "url": "https://bnc.co.tz/", "contact": {}},
    {"slug": "bnhchs", "name": "Bishop Nicodemus Hhando College of Health Science", "url": "https://bnhchs.ac.tz/", "contact": {"email": "bashnethealthcollege@gmail.com"}},
    {"slug": "bnmgeneral", "name": "BNM General", "url": "http://bnmgeneral.co.tz/", "contact": {"email": "wilbert@bnmgeneral.co.tz"}},
    {"slug": "boatanzania", "name": "Bank of Africa Tanzania", "url": "https://boatanzania.co.tz/", "contact": {"email": "info@boatanzania.co.tz"}},
    {"slug": "boavida", "name": "Boavida Paints", "url": "https://boavida.co.tz/", "contact": {}},
    {"slug": "bobgrow", "name": "BOB-GROW Trading & Services", "url": "https://bobgrow.co.tz/", "contact": {"email": "info@bobgrow.co.tz"}},
    {"slug": "bogach", "name": "BOGACH Finance Company", "url": "https://bogach.co.tz/", "contact": {"email": "Info@bogach.co.tz"}},
    {"slug": "boitanzania", "name": "BOI Tanzania", "url": "https://boitanzania.co.tz/", "contact": {}},
    {"slug": "bongonews", "name": "BONGO NEWS", "url": "https://bongonews.co.tz/", "contact": {}},
    {"slug": "bongovip", "name": "Bongo VIP", "url": "https://bongovip.co.tz/", "contact": {}},
    {"slug": "boraagrica", "name": "BORA KILIMO-BIASHARA", "url": "https://www.boraagrica.co.tz/", "contact": {}},
    {"slug": "borderless", "name": "Borderless Solutions Ltd", "url": "https://borderless.co.tz/", "contact": {"email": "info@borderless.co.tz"}},
    {"slug": "bosch-professional", "name": "Bosch Power Tools Professional", "url": "https://www.bosch-professional.com/", "contact": {"email": "dashq@das-bosch.com"}},
    {"slug": "bosch-pt", "name": "Bosch Power Tools", "url": "https://www.bosch-pt.com/", "contact": {"email": "kontakt@bosch.de"}},
    {"slug": "boss", "name": "Boss Limited", "url": "https://boss.co.tz/", "contact": {"email": "boss@boss.co.tz"}},
    {"slug": "boston", "name": "Boston City Campus", "url": "https://www.boston.ac.za/", "contact": {"email": "info@boston.co.za"}},
    {"slug": "bot", "name": "Bank of Tanzania", "url": "https://www.bot.go.tz/CallsforTender", "contact": {"email": "botcommunications@bot.go.tz"}},
    {"slug": "bpc", "name": "Brain Power Consultancy", "url": "https://bpc.co.tz/services.php", "contact": {"email": "info@bpc.co.tz"}},
    {"slug": "bphacoh", "name": "BPHACOH", "url": "https://bphacoh.ac.tz/", "contact": {"email": "info@bphacoh.ac.tz"}},
    {"slug": "bpra", "name": "BPRA", "url": "https://www.bpra.go.tz/", "contact": {"email": "info@bpra.go.tz"}},
    {"slug": "brac-etender", "name": "BRAC e-Tender", "url": "https://tender.brac.net/", "contact": {}},
    {"slug": "brac-tanzania", "name": "BRAC Tanzania", "url": "https://procurement.brac.net/", "contact": {}},
    {"slug": "bradda", "name": "Bradda", "url": "https://bradda.co.tz/", "contact": {"email": "info@bradda.co.tz"}},
]


def fetch_url(url: str) -> tuple[str | None, str | None]:
    """Fetch URL with curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0 (compatible; TenderScraper/1.0)", "--connect-timeout", "30", "--max-time", "60", url],
            capture_output=True,
            text=True,
            timeout=65,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}: {r.stderr[:200] if r.stderr else 'unknown'}"
        return r.stdout or "", None
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except Exception as e:
        return None, str(e)[:200]


def extract_emails(html: str) -> list[str]:
    """Extract email addresses from HTML."""
    emails = set()
    for m in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html):
        e = m.group(0).lower()
        if not any(x in e for x in ["example.com", "sentry.io", "wixpress", "gravatar", "schema.org", "placeholder"]):
            emails.add(e)
    return sorted(emails)


def extract_doc_links(html: str, base_url: str) -> list[dict]:
    """Extract document links (PDF, DOC, etc.) from HTML."""
    links = []
    seen = set()
    for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']*?\.(?:pdf|doc|docx|xls|xlsx|zip|rar))["\']', html, re.I):
        href = m.group(1).strip()
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = urljoin(base_url, href)
        elif not href.startswith("http"):
            href = urljoin(base_url, href)
        if href not in seen:
            seen.add(href)
            fn = Path(urlparse(href).path).name or "document"
            links.append({"url": href, "filename": fn})
    return links


def has_tender_content(html: str) -> bool:
    """Check if page contains tender/procurement content."""
    if not html or len(html) < 100:
        return False
    # Block reCAPTCHA / Cloudflare pages
    if "recaptcha" in html.lower() or "checking your browser" in html.lower()[:500]:
        return False
    text = re.sub(r"<[^>]+>", " ", html)[:15000]
    return bool(TENDER_KEYWORDS.search(text))


def download_document(url: str, dest: Path) -> bool:
    """Download a document to dest. Returns True on success."""
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            ["curl", "-sL", "-o", str(dest), "-A", "Mozilla/5.0", "--connect-timeout", "30", "--max-time", "90", url],
            capture_output=True,
            timeout=95,
        )
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def extract_text_from_file(filepath: Path, extracted_dir: Path) -> bool:
    """Extract text from PDF/DOCX/XLSX using tools. Returns True on success."""
    try:
        ext = filepath.suffix.lower()
        base = filepath.stem
        out_txt = extracted_dir / f"{base}.txt"
        if ext == ".pdf":
            r = subprocess.run(
                ["python3", "-m", "tools", "pdf", "read", str(filepath)],
                capture_output=True,
                text=True,
                cwd=str(PROJECT),
                timeout=30,
            )
            if r.returncode == 0 and r.stdout:
                out_txt.write_text(r.stdout[:500000], encoding="utf-8")
                return True
        elif ext in (".docx", ".doc"):
            r = subprocess.run(
                ["python3", "-m", "tools", "docx", "read", str(filepath)],
                capture_output=True,
                text=True,
                cwd=str(PROJECT),
                timeout=30,
            )
            if r.returncode == 0 and r.stdout:
                out_txt.write_text(r.stdout[:500000], encoding="utf-8")
                return True
        elif ext in (".xlsx", ".xls"):
            r = subprocess.run(
                ["python3", "-m", "tools", "xlsx", "read", str(filepath), "--format", "json"],
                capture_output=True,
                text=True,
                cwd=str(PROJECT),
                timeout=30,
            )
            if r.returncode == 0 and r.stdout:
                (extracted_dir / f"{base}.json").write_text(r.stdout[:500000], encoding="utf-8")
                return True
    except Exception:
        pass
    return False


def create_opportunity_lead(inst: dict, html: str, website_url: str) -> dict:
    """Create opportunity lead for institution with no tenders."""
    emails = extract_emails(html)
    if not emails and inst.get("contact", {}).get("email"):
        emails = [inst["contact"]["email"]]
    name = inst["name"]
    slug = inst["slug"]
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": website_url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }


def append_lead(lead: dict) -> None:
    """Append lead to opportunities/leads.json (skip if slug already exists)."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    if any(l.get("institution_slug") == lead["institution_slug"] for l in leads):
        return
    leads.append(lead)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def update_institution_state(inst_dir: Path, status: str, tender_count: int, doc_count: int, error: str | None = None) -> None:
    """Update last_scrape.json and scrape_log.json."""
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "institution": inst_dir.name,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2))

    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    log["runs"] = log.get("runs", [])[:49]
    log["runs"].insert(0, {
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def scrape_institution(inst: dict) -> tuple[str, int, int]:
    """Scrape one institution. Returns (status, tender_count, doc_count)."""
    slug = inst["slug"]
    url = inst["url"]
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

    html, err = fetch_url(url)
    if err:
        update_institution_state(inst_dir, "error", 0, 0, err)
        return "error", 0, 0

    doc_links = extract_doc_links(html, url)
    has_tenders = has_tender_content(html) and doc_links

    if not has_tenders:
        # No tenders: create opportunity lead
        lead = create_opportunity_lead(inst, html, url)
        append_lead(lead)
        update_institution_state(inst_dir, "no_tenders", 0, 0)
        return "no_tenders", 0, 0

    # Has tender content and doc links: create tender JSON, download docs
    year = datetime.now().year
    seq = 1
    active_dir = inst_dir / "tenders" / "active"
    for f in active_dir.glob("*.json"):
        try:
            m = re.match(r".*-(\d{4})-(\d+).json", f.stem)
            if m and int(m.group(1)) == year:
                seq = max(seq, int(m.group(2)) + 1)
        except Exception:
            pass
    slug_upper = slug.upper().replace("-", "")
    tender_id = f"{slug_upper}-{year}-{seq:03d}"

    downloads_dir = inst_dir / "downloads" / tender_id
    original_dir = downloads_dir / "original"
    extracted_dir = downloads_dir / "extracted"
    original_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    documents = []
    doc_count = 0
    for d in doc_links[:20]:
        dest = original_dir / d["filename"]
        if download_document(d["url"], dest):
            doc_count += 1
            documents.append({
                "filename": d["filename"],
                "original_url": d["url"],
                "local_path": str(dest.relative_to(PROJECT)),
                "downloaded_at": datetime.now(timezone.utc).isoformat(),
            })
            extract_text_from_file(dest, extracted_dir)
        time.sleep(2)

    tender_json = {
        "tender_id": tender_id,
        "institution": slug,
        "title": inst["name"] + " – Tenders",
        "description": "",
        "published_date": "",
        "closing_date": "",
        "status": "active",
        "source_url": url,
        "documents": documents,
        "contact": inst.get("contact", {}),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "last_checked": datetime.now(timezone.utc).isoformat(),
    }
    (active_dir / f"{tender_id}.json").write_text(json.dumps(tender_json, indent=2, ensure_ascii=False))

    update_institution_state(inst_dir, "success", 1, doc_count)
    return "success", 1, doc_count


def main():
    results = []
    for i, inst in enumerate(INSTITUTIONS):
        if i > 0:
            time.sleep(RATE_LIMIT)
        try:
            status, tender_count, doc_count = scrape_institution(inst)
        except Exception as e:
            inst_dir = PROJECT / "institutions" / inst["slug"]
            update_institution_state(inst_dir, "error", 0, 0, str(e)[:200])
            status, tender_count, doc_count = "error", 0, 0
        results.append((inst["slug"], status, tender_count, doc_count))
        print(f"RESULT|{inst['slug']}|{status}|{tender_count}|{doc_count}")

    # Run sync_leads_csv
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run(["python3", str(sync_script)], cwd=str(PROJECT), capture_output=True)

    return results


if __name__ == "__main__":
    main()
