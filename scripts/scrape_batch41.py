#!/usr/bin/env python3
"""
Scrape 25 institutions (gas through genius) for active tenders.
Run ID: run_20260315_060430_batch41
If no tenders found: append lead to opportunities/leads.json, run sync_leads_csv.py
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import urllib.request

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch41"
RATE_LIMIT = 10

# Tender keywords (Swahili/English)
TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|zabuni|manunuzi|procurement|rfp|rfq|eoi|expression of interest|"
    r"request for proposal|request for quotation|bid|bidding|prequalification|"
    r"supply|quotation|invitation to bid|rfi|closing date|deadline)\b",
    re.I,
)

DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

INSTITUTIONS = [
    ("gas", "https://gas.ac.tz/", "Guardian Angels Schools"),
    ("gasco", "https://gasco.co.tz/gasco_projects/engineering-procurement-and-construction-epc-for-natural-gas-distribution-network-in-dar-es-salaam-bq-and-energo", "GASCO"),
    ("gash", "https://gash.co.tz/", "Gupta Auto Spares & Hardware"),
    ("gatewaylogistics", "https://gatewaylogistics.co.tz/", "Gateway Logistics"),
    ("gazetini", "https://gazetini.co.tz/", "gazetini"),
    ("gcl", "https://gcl.co.tz/", "Gonelemale Company Limited"),
    ("gcla", "https://gcla.go.tz/", "GCLA Government Chemist"),
    ("gcli", "https://gcli.co.tz/", "GCL Insurance Assessors"),
    ("gcmmarketing", "https://gcmmarketing.co.tz/", "GCM Innovation & Marketing"),
    ("gctl", "https://gctl.co.tz/", "GOPA Contractors Tanzania"),
    ("geamos", "https://geamos.co.tz/", "Geamos Logistics"),
    ("geas", "https://geas.co.tz/", "GEAS Company Limited"),
    ("geestar", "https://geestar.co.tz/", "GeeStar"),
    ("gefu", "https://www.gefu.co.tz/", "GEFU AGROMART"),
    ("gem", "https://tanzanite888.tz/", "The Tanzanite Dream"),
    ("gemlab", "https://tanzanite888.tz/", "The Tanzanite Dream"),
    ("gems", "https://tanzanite888.tz/", "The Tanzanite Dream"),
    ("gemstone", "https://tanzanite888.tz/", "The Tanzanite Dream"),
    ("gemstone.tz", "https://tanzanite888.tz/", "The Tanzanite Dream"),
    ("gemstones", "https://tanzanite888.tz/", "The Tanzanite Dream"),
    ("gencode", "https://gencode.co.tz/", "GENCODE LIMITED"),
    ("generalpetroleum", "https://generalpetroleum.de/", "GP Lubricants"),
    ("genesisdevelopment", "https://genesisdevelopment.co.tz/", "Genesis Development"),
    ("gengeni", "https://gengeni.co.tz/", "Boramart/Gengeni"),
    ("genius", "https://genius.co.tz/", "Genius Consultancy"),
]


def fetch_url(url: str, timeout: int = 45) -> tuple[str | None, str | None]:
    """Fetch URL and return (html, error)."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)[:200]


def has_tender_content(html: str) -> bool:
    """Check if HTML contains tender/procurement notice content."""
    if not html or len(html) < 100:
        return False
    text = re.sub(r"<[^>]+>", " ", html)[:30000]
    return bool(TENDER_KEYWORDS.search(text))


def extract_emails(html: str) -> list[str]:
    """Extract valid emails from HTML."""
    emails = set()
    for m in EMAIL_RE.finditer(html[:100000]):
        e = m.group(0).lower()
        if any(x in e for x in ["png", "jpg", "gif", "example", "test", "wixpress", "gravatar", "sentry"]):
            continue
        if "@" in e and "." in e.split("@")[-1]:
            emails.add(e)
    return sorted(emails)


def extract_doc_links(html: str, base_url: str) -> list[dict]:
    """Extract document links (PDF, DOC, etc.) from HTML."""
    links = []
    seen = set()
    for m in re.finditer(r'href=["\']([^"\']*?\.(?:pdf|doc|docx|xls|xlsx|zip|rar))["\']', html, re.I):
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


def get_institution_info(slug: str, default_url: str) -> dict:
    """Read README frontmatter for institution name and contact."""
    readme = PROJECT / "institutions" / slug / "README.md"
    info = {"name": slug.replace("-", " ").title(), "website_url": default_url}
    if not readme.exists():
        return info
    text = readme.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            for line in fm.split("\n"):
                if "name:" in line and "institution:" in fm[:fm.find(line)]:
                    m = re.search(r'name:\s*["\']?([^"\'\n]+)["\']?', line)
                    if m:
                        n = m.group(1).strip().replace("&#8211;", "–").replace("&amp;", "&")[:80]
                        if "institution" not in line.lower():
                            info["name"] = n
                if "tender_url:" in line or "homepage:" in line:
                    m = re.search(r'https?://[^\s"\']+', line)
                    if m:
                        info["website_url"] = m.group(0).rstrip("/")
    if not info.get("website_url"):
        info["website_url"] = default_url
    return info


def create_lead(slug: str, website_url: str, institution_name: str, emails: list[str]) -> dict:
    """Create a lead entry for opportunities."""
    return {
        "institution_slug": slug,
        "institution_name": institution_name,
        "website_url": website_url if website_url else f"https://{slug}.co.tz/",
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {institution_name}",
        "draft_email_body": f"Dear {institution_name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {institution_name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    }


def append_lead(lead: dict) -> bool:
    """Append lead to opportunities/leads.json. Returns True if added."""
    path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if path.exists():
        with open(path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    slugs = {l.get("institution_slug") for l in leads}
    if lead["institution_slug"] in slugs:
        return False
    leads.append(lead)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    return True


def download_document(url: str, dest: Path) -> bool:
    """Download a document to dest. Returns True on success."""
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as resp:
            dest.write_bytes(resp.read())
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def update_institution_state(slug: str, status: str, tender_count: int, doc_count: int, error: str | None = None) -> None:
    """Update last_scrape.json and scrape_log.json."""
    inst_dir = PROJECT / "institutions" / slug
    inst_dir.mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    last = {
        "institution": slug,
        "last_scrape": now,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    log["runs"].insert(
        0,
        {
            "run_id": RUN_ID,
            "timestamp": now,
            "status": status,
            "tenders_found": tender_count,
            "new_tenders": tender_count,
            "documents_downloaded": doc_count,
            "tender_ids": [],
            "errors": [error] if error else [],
        },
    )
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def process_institution(slug: str, url: str, _: str) -> tuple[str, str, int, int]:
    """Process one institution. Returns (slug, status, tender_count, doc_count)."""
    html, err = fetch_url(url)
    if err:
        update_institution_state(slug, "error", 0, 0, err)
        info = get_institution_info(slug, url.rstrip("/"))
        lead = create_lead(slug, info["website_url"], info["name"], [])
        append_lead(lead)
        return (slug, "error", 0, 0)

    info = get_institution_info(slug, url.rstrip("/"))
    emails = extract_emails(html)
    doc_links = extract_doc_links(html, url)
    has_tenders = has_tender_content(html)

    tender_count = 0
    doc_count = 0

    if has_tenders:
        # Create tender_id and save tender JSON + download docs
        tid_slug = slug.upper().replace(".", "-").replace(" ", "")[:8]
        tender_id = f"{tid_slug}-2026-001"
        inst_dir = PROJECT / "institutions" / slug
        tender_dir = inst_dir / "tenders" / "active"
        download_base = inst_dir / "downloads" / tender_id
        orig_dir = download_base / "original"
        ext_dir = download_base / "extracted"

        tender_count = 1
        documents = []
        for link in doc_links[:20]:  # limit to 20 docs per tender
            dest = orig_dir / link["filename"]
            if download_document(link["url"], dest):
                doc_count += 1
                documents.append({
                    "filename": link["filename"],
                    "original_url": link["url"],
                    "local_path": str(dest.relative_to(inst_dir)),
                })
                # Extract text for PDF/DOCX
                if dest.suffix.lower() in (".pdf", ".docx", ".doc"):
                    ext_dir.mkdir(parents=True, exist_ok=True)
                    try:
                        if dest.suffix.lower() == ".pdf":
                            r = subprocess.run(
                                [sys.executable, "-m", "tools", "pdf", "read", str(dest)],
                                capture_output=True, text=True, cwd=str(PROJECT), timeout=30,
                            )
                            if r.returncode == 0 and r.stdout:
                                (ext_dir / f"{dest.stem}.txt").write_text(r.stdout[:500000], encoding="utf-8")
                        elif dest.suffix.lower() in (".docx", ".doc"):
                            r = subprocess.run(
                                [sys.executable, "-m", "tools", "docx", "read", str(dest)],
                                capture_output=True, text=True, cwd=str(PROJECT), timeout=30,
                            )
                            if r.returncode == 0 and r.stdout:
                                (ext_dir / f"{dest.stem}.txt").write_text(r.stdout[:500000], encoding="utf-8")
                    except Exception:
                        pass

        tender_json = {
            "tender_id": tender_id,
            "institution": slug,
            "title": info["name"] + " - Tender",
            "description": "",
            "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "closing_date": "",
            "category": "General",
            "status": "active",
            "source_url": url,
            "documents": documents,
            "contact": {"email": emails[0] if emails else "", "emails": emails},
            "scraped_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        tender_dir.mkdir(parents=True, exist_ok=True)
        (tender_dir / f"{tender_id}.json").write_text(json.dumps(tender_json, indent=2), encoding="utf-8")
        status = "tenders"
    else:
        # No tenders - create opportunity lead
        lead = create_lead(slug, info["website_url"], info["name"], emails)
        append_lead(lead)
        status = "no_tenders"

    update_institution_state(slug, "success", tender_count, doc_count)
    return (slug, status, tender_count, doc_count)


def main():
    results = []
    for i, (slug, url, _) in enumerate(INSTITUTIONS):
        if i > 0:
            time.sleep(RATE_LIMIT)
        print(f"Processing {slug}...", end=" ", flush=True)
        slug, status, tc, dc = process_institution(slug, url, _)
        results.append((slug, status, tc, dc))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")

    print("\n--- SUMMARY ---")
    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")

    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], check=True, cwd=str(PROJECT))
        print("\nSynced opportunities/leads.csv")


if __name__ == "__main__":
    main()
