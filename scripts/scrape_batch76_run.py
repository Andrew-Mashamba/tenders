#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders. Run ID: run_20260315_060430_batch76
Institutions: mkurabita, mkuzachicksltd, mkwabi, mlc, mlg, mlimanicity, mlimaniholdings,
mloganzila, mm-safaris, mmgroup, mnkanda, mnma, moassurance, mobikey, mobilepower,
moccobeachvilla, modans, modelltransport, moe, moez, mof, mofzanzibar, moh, moha, mohsinsumar
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch76"

INST_SLUGS = [
    "mkurabita", "mkuzachicksltd", "mkwabi", "mlc", "mlg",
    "mlimanicity", "mlimaniholdings", "mloganzila", "mm-safaris", "mmgroup",
    "mnkanda", "mnma", "moassurance", "mobikey", "mobilepower",
    "moccobeachvilla", "modans", "modelltransport", "moe", "moez",
    "mof", "mofzanzibar", "moh", "moha", "mohsinsumar",
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfq|rfi|bid|auction|supply|eoi|expression of interest)\b",
    re.I,
)
DOC_EXT = re.compile(r"\.(pdf|doc|docx|xls|xlsx|zip|rar)$", re.I)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def load_readme(slug: str) -> dict | None:
    """Load config from institution README frontmatter."""
    readme = PROJECT / "institutions" / slug / "README.md"
    if not readme.exists():
        return None
    try:
        content = readme.read_text(encoding="utf-8")
        if "---" not in content:
            return None
        parts = content.split("---", 2)
        if len(parts) < 2:
            return None
        import yaml
        cfg = yaml.safe_load(parts[1])
        return cfg or {}
    except Exception:
        return None


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, timeout: int = 25) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-m", str(timeout), "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, r.stderr or "curl failed"
        return r.stdout, None
    except Exception as e:
        return None, str(e)


def parse_tenders(html: str, base_url: str) -> tuple[list[dict], list[str]]:
    """Parse HTML for tender listings and document links. Returns (tenders, doc_urls)."""
    tenders = []
    doc_urls = []
    if not html or len(html) < 100:
        return tenders, doc_urls

    # Find document links
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = m.group(1).strip()
        if DOC_EXT.search(href):
            full = urljoin(base_url, href)
            if full not in doc_urls:
                doc_urls.append(full)

    # Check for tender keywords
    if not TENDER_KEYWORDS.search(html):
        return tenders, doc_urls

    # Try to find tender table rows (common in gov sites)
    if "zabuni" in html.lower() or "tender" in html.lower() or "manunuzi" in html.lower() or "procurement" in html.lower():
        rows = re.findall(r"<tr[^>]*>.*?</tr>", html, re.DOTALL | re.I)
        for row in rows:
            if TENDER_KEYWORDS.search(row):
                cells = re.findall(r"<t[dh][^>]*>([^<]*)</t[dh]>", row, re.I)
                if len(cells) >= 2:
                    title = cells[1].strip() if len(cells) > 1 else cells[0].strip()
                    if len(title) > 5 and "imefungwa" not in title.lower():
                        tenders.append({"title": title, "description": "", "doc_links": []})
        # Also try list items / links in tender sections
        if not tenders and doc_urls:
            for m in re.finditer(r'<a[^>]+href=["\']([^"\']+\.(?:pdf|doc|docx|xls|xlsx|zip))["\'][^>]*>([^<]*)</a>', html, re.I):
                title = m.group(2).strip()
                if len(title) > 3 and not title.startswith("http"):
                    tenders.append({"title": title or "Tender Document", "description": "", "doc_links": []})
        # If still no tenders but we have doc links and tender keywords, create one
        if not tenders and doc_urls:
            tenders.append({"title": "Tender/Procurement Documents", "description": "", "doc_links": doc_urls})

    if "under construction" in html.lower() or "under constuction" in html.lower():
        return [], doc_urls

    return tenders, doc_urls


def extract_emails(html: str) -> list[str]:
    """Extract emails from HTML."""
    return list(dict.fromkeys(EMAIL_RE.findall(html)))


def update_last_scrape(inst_dir: Path, status: str, tender_count: int = 0, error: str = None):
    now = datetime.now(timezone.utc).isoformat()
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


def append_scrape_log(inst_dir: Path, status: str, tender_count: int, doc_count: int, errors: list):
    log_path = inst_dir / "scrape_log.json"
    data = {"runs": []}
    if log_path.exists():
        with open(log_path) as f:
            data = json.load(f)
    run = {
        "run_id": RUN_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "new_tenders": 0,
        "updated_tenders": 0,
        "documents_downloaded": doc_count,
        "errors": errors or [],
    }
    data["runs"] = data.get("runs", []) + [run]
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)


def append_lead(slug: str, name: str, url: str, emails: list, opportunity_type: str = "sell", desc: str = None):
    if desc is None:
        desc = f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
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
        "website_url": url.rstrip("/"),
        "emails": emails or [],
        "opportunity_type": opportunity_type,
        "opportunity_description": desc,
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing = {l.get("institution_slug") for l in leads}
    if slug not in existing:
        leads.append(lead)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    return False


def save_tenders_and_download(inst_dir: Path, slug: str, tenders: list, doc_urls: list, source_url: str) -> int:
    """Save tender JSONs and download documents. Returns doc_count."""
    doc_count = 0
    year = datetime.now().year
    for i, t in enumerate(tenders[:20], 1):
        tid = f"{slug.upper()[:8].replace('-','')}-{year}-{i:03d}"
        tender_json = {
            "tender_id": tid,
            "institution": slug,
            "title": t.get("title", "Untitled"),
            "description": t.get("description", ""),
            "published_date": "",
            "closing_date": "",
            "status": "active",
            "source_url": source_url,
            "documents": [],
            "contact": {},
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }
        (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
        with open(inst_dir / "tenders" / "active" / f"{tid}.json", "w") as f:
            json.dump(tender_json, f, indent=2)

        download_dir = inst_dir / "downloads" / tid / "original"
        download_dir.mkdir(parents=True, exist_ok=True)
        for doc_url in doc_urls[:5]:
            try:
                fname = Path(urlparse(doc_url).path).name or "document.pdf"
                fname = re.sub(r'[^\w\-._]', '_', fname)[:80]
                out = download_dir / fname
                subprocess.run(
                    ["curl", "-sL", "-m", "30", "-o", str(out), doc_url],
                    capture_output=True,
                    timeout=35,
                )
                if out.exists() and out.stat().st_size > 0:
                    doc_count += 1
            except Exception:
                pass
    return doc_count


def main():
    results = []
    leads_added = 0

    for slug in INST_SLUGS:
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)

        cfg = load_readme(slug)
        if not cfg:
            update_last_scrape(inst_dir, "error", 0, "No README config")
            append_scrape_log(inst_dir, "error", 0, 0, ["No README config"])
            print(f"RESULT|{slug}|error|0|0")
            results.append((slug, "error", 0, 0))
            continue

        website = cfg.get("website", {})
        tender_url = website.get("tender_url") or website.get("homepage")
        inst = cfg.get("institution", {})
        inst_name = inst.get("name", slug)
        if isinstance(inst_name, str):
            inst_name = re.sub(r"&#\d+;", "", inst_name).strip()

        contact = cfg.get("contact", {})
        emails_from_readme = []
        if contact.get("email"):
            emails_from_readme.append(contact["email"])
        emails_from_readme.extend(contact.get("alternate_emails", []))

        if not tender_url:
            update_last_scrape(inst_dir, "error", 0, "No tender_url")
            append_scrape_log(inst_dir, "error", 0, 0, ["No tender_url"])
            print(f"RESULT|{slug}|error|0|0")
            results.append((slug, "error", 0, 0))
            continue

        # mof: tender_url points to PDF; use pages/tenders for listing
        if slug == "mof":
            parsed = urlparse(tender_url)
            tender_url = f"{parsed.scheme}://{parsed.netloc}/pages/tenders"

        html, err = fetch_url(tender_url)
        if err or not html:
            update_last_scrape(inst_dir, "error", 0, err or "Fetch failed")
            append_scrape_log(inst_dir, "error", 0, 0, [err or "Fetch failed"])
            if append_lead(slug, inst_name, tender_url, emails_from_readme, "sell", f"Site {tender_url} unreachable or timeout. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."):
                leads_added += 1
            print(f"RESULT|{slug}|error|0|0")
            results.append((slug, "error", 0, 0))
            time.sleep(2)
            continue

        tenders, doc_urls = parse_tenders(html, tender_url)
        tender_count = len(tenders)
        doc_count = 0

        if tender_count > 0:
            doc_count = save_tenders_and_download(inst_dir, slug, tenders, doc_urls, tender_url)
            status = "success"
        else:
            status = "success"
            emails = emails_from_readme + extract_emails(html)
            emails = list(dict.fromkeys(e for e in emails if "example" not in e.lower() and "sentry" not in e.lower()))
            if append_lead(slug, inst_name, tender_url, emails):
                leads_added += 1

        update_last_scrape(inst_dir, status, tender_count)
        append_scrape_log(inst_dir, status, tender_count, doc_count, [])
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
        results.append((slug, status, tender_count, doc_count))
        time.sleep(2)

    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], cwd=str(PROJECT), check=False)

    print(f"\n--- BATCH COMPLETE: {len(results)} institutions, {leads_added} new leads appended ---")


if __name__ == "__main__":
    main()
