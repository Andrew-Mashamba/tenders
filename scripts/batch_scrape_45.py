#!/usr/bin/env python3
"""
Batch scrape 25 institutions for run_20260315_060430_batch45.
Processes: hallmarkattorneys, halogame, halotel, hampshire, hamtours, hanangdc,
handenitc, handman, hanspaul, happychildren, harmonyhotel, harusi, hasa, hasafa,
hashtech, hasnet, hawa, hawaii, haydom, hbtattorneys, head2toeclinic, heavengates,
heckilimanjarosafaris, heet, hekimawaldorfschool
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
RUN_ID = "run_20260315_060430_batch45"
INSTITUTIONS = [
    ("hallmarkattorneys", "https://hallmarkattorneys.co.tz/", "Hallmark Attorneys"),
    ("halogame", "http://halogame.co.tz/", "Halotel EARN COINS"),
    ("halotel", "https://halotel.co.tz/", "Halotel"),
    ("hampshire", "https://hampshire.co.tz/", "Hampshire Hathaway"),
    ("hamtours", "https://hamtours.com/", "Hamtours"),
    ("hanangdc", "https://hanangdc.go.tz/tenders", "Hanang District Council"),
    ("handenitc", "https://handenitc.go.tz/procurement-and-supply", "Handeni Town Council"),
    ("handman", "https://handman.co.tz/", "Handman"),
    ("hanspaul", "https://hanspaul.co.tz/", "Hanspaul Group"),
    ("happychildren", "https://happychildren.or.tz/", "Happy Children"),
    ("harmonyhotel", "https://harmonyhotel.co.tz/", "Harmony Hotel"),
    ("harusi", "https://warioba.ventures/", "Warioba Ventures"),
    ("hasa", "https://hasa.co.tz/", "HASA Clearing and Forwarding"),
    ("hasafa", "https://hasafa.co.tz/", "Hasafa Health Sciences"),
    ("hashtech", "https://hashtech.co.tz/", "Hashtech Tanzania"),
    ("hasnet", "https://hasnet.co.tz/", "Hasnet ICT Solution"),
    ("hawa", "https://hawa.or.tz/", "HAWA"),
    ("hawaii", "https://hawaii.co.tz/", "Hawaii Products Supplies"),
    ("haydom", "https://haydom.or.tz/", "Haydom Lutheran Hospital"),
    ("hbtattorneys", "https://hbtattorneys.co.tz/", "HBT Attorneys"),
    ("head2toeclinic", "https://head2toeclinic.co.tz/", "Head 2 Toe Physiotherapy Clinic"),
    ("heavengates", "http://heavengates.co.tz/", "Heaven Gates Funeral Services"),
    ("heckilimanjarosafaris", "https://heckilimanjarosafaris.co.tz/", "HEC Kilimanjaro Safaris"),
    ("heet", "https://heet.co.tz/", "HEET Tanzania"),
    ("hekimawaldorfschool", "https://hekimawaldorfschool.ac.tz/", "Hekima Waldorf School"),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfi|eoi|expression of interest|"
    r"invitation to bid|bid document|closing date|deadline for submission)\b",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-A", "Mozilla/5.0", "--connect-timeout", "15", "--max-time", str(timeout), url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}"
        if "Error code 523" in r.stdout or "origin web server" in r.stdout.lower():
            return None, "Site unreachable (523)"
        if "503 Service Unavailable" in r.stdout[:500]:
            return None, "503 Service Unavailable"
        if "Account Suspended" in r.stdout[:2000]:
            return r.stdout, None  # Still return content for email extraction
        if "PLEASE LOG ON" in r.stdout and "Username" in r.stdout:
            return None, "Login required"
        return r.stdout, None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def extract_emails(html: str) -> list[str]:
    """Extract email addresses from HTML."""
    if not html:
        return []
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html))
    return sorted(e for e in emails if not any(x in e.lower() for x in ["example", "sentry", "wixpress", "png", "jpg", "gif", "svg", "2x"]))


def extract_doc_links(html: str, base_url: str) -> list[str]:
    """Extract document links (PDF, DOC, etc.) from HTML."""
    if not html:
        return []
    links = set()
    for ext in DOC_EXT:
        for m in re.finditer(rf'href=["\']([^"\']*\{re.escape(ext)}[^"\']*)["\']', html, re.I):
            u = m.group(1)
            if u.startswith("//"):
                u = "https:" + u
            elif u.startswith("/"):
                u = urljoin(base_url, u)
            elif not u.startswith("http"):
                u = urljoin(base_url, u)
            if base_url in u or urlparse(base_url).netloc in u or urlparse(u).netloc:
                links.add(u)
    return list(links)


def has_tender_content(html: str) -> bool:
    """Check if page contains tender/procurement content."""
    if not html:
        return False
    return bool(TENDER_KEYWORDS.search(html))


def parse_tenders_from_html(html: str, slug: str, url: str, inst_name: str) -> list[dict]:
    """Parse tender items from HTML. Returns list of tender dicts."""
    tenders = []
    year = datetime.now().year

    # hanangdc: government tenders page - check for tender listings
    if slug == "hanangdc" and html:
        # Look for tender items, PDF links in storage
        doc_links = re.findall(r'href=["\']([^"\']*hanangdc\.go\.tz/storage[^"\']*\.pdf[^"\']*)["\']', html, re.I)
        if doc_links or "tender" in html.lower() or "zabuni" in html.lower() or "manunuzi" in html.lower():
            # Extract tender titles from page
            for m in re.finditer(r'<[^>]+>(.*?)(?:tender|zabuni|manunuzi)[^<]*</[^>]+>', html, re.I | re.DOTALL):
                title = re.sub(r'<[^>]+>', '', m.group(0))[:200].strip()
                if title and len(title) > 10:
                    tenders.append({
                        "tender_id": f"HANANGDC-{year}-{len(tenders)+1:03d}",
                        "institution": slug,
                        "title": title[:150] or "Tender Notice",
                        "description": "Government tender from Hanang District Council",
                        "source_url": url,
                        "documents": [{"original_url": u} for u in doc_links[:5]],
                        "contact": {"email": "ded@hanangdc.go.tz"},
                        "scraped_at": datetime.utcnow().isoformat() + "Z",
                    })
            if not tenders and doc_links:
                tenders.append({
                    "tender_id": f"HANANGDC-{year}-001",
                    "institution": slug,
                    "title": "Hanang District Council Tenders",
                    "description": "Government tenders with linked documents",
                    "source_url": url,
                    "documents": [{"original_url": u} for u in doc_links[:10]],
                    "contact": {"email": "ded@hanangdc.go.tz"},
                    "scraped_at": datetime.utcnow().isoformat() + "Z",
                })

    # handenitc: procurement page
    if slug == "handenitc" and html and ("procurement" in html.lower() or "tender" in html.lower() or "supply" in html.lower()):
        doc_links = re.findall(r'href=["\']([^"\']*\.(?:pdf|doc|docx)[^"\']*)["\']', html, re.I)
        doc_links = [urljoin(url, u) if u.startswith("/") else u for u in doc_links if "handenitc" in u or u.startswith("/")]
        if doc_links or "tender" in html.lower():
            tenders.append({
                "tender_id": f"HANDENITC-{year}-001",
                "institution": slug,
                "title": "Handeni Town Council Procurement and Supply",
                "description": "Procurement and supply tenders",
                "source_url": url,
                "documents": [{"original_url": u} for u in doc_links[:10]],
                "contact": {"email": "td@handenitc.go.tz"},
                "scraped_at": datetime.utcnow().isoformat() + "Z",
            })

    # haydom: has job/vacancy PDFs - Tangazo la kazi = job announcement (not necessarily tender)
    # Only add if we find actual tender content
    if slug == "haydom" and html and has_tender_content(html):
        doc_links = re.findall(r'href=["\']([^"\']*\.(?:pdf|doc|docx)[^"\']*)["\']', html, re.I)
        doc_links = [urljoin(url, u) if u.startswith("/") else u for u in doc_links]
        tenders.append({
            "tender_id": f"HAYDOM-{year}-001",
            "institution": slug,
            "title": "Haydom Lutheran Hospital Tender/Procurement",
            "description": "Tender or procurement notice",
            "source_url": url,
            "documents": [{"original_url": u} for u in doc_links[:10]],
            "contact": {"email": "post@haydom.co.tz"},
            "scraped_at": datetime.utcnow().isoformat() + "Z",
        })

    return tenders


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def update_last_scrape(inst_dir: Path, status: str, tender_count: int, error: str | None = None):
    now = datetime.utcnow().isoformat() + "Z"
    data = {
        "institution": inst_dir.name,
        "last_scrape": now,
        "next_scrape": now,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(data, f, indent=2)


def append_scrape_log(inst_dir: Path, run_id: str, status: str, tender_count: int, doc_count: int, error: str | None = None):
    log_path = inst_dir / "scrape_log.json"
    data = {"runs": []}
    if log_path.exists():
        with open(log_path) as f:
            data = json.load(f)
    data["runs"].append({
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    })
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)


def download_document(url: str, dest_dir: Path) -> bool:
    """Download a document to dest_dir. Returns True if successful."""
    try:
        fname = url.split("/")[-1].split("?")[0] or "document.pdf"
        fname = re.sub(r'[^\w.\-]', '_', fname)[:100]
        dest = dest_dir / (fname or "document.pdf")
        r = subprocess.run(
            ["curl", "-sL", "-o", str(dest), "-w", "%{http_code}", url],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if r.returncode == 0 and r.stdout.strip() == "200" and dest.exists() and dest.stat().st_size > 0:
            return True
    except Exception:
        pass
    return False


def append_lead(slug: str, name: str, url: str, emails: list[str], opportunity_type: str, description: str):
    """Append a lead to opportunities/leads.json (skip if already exists)."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            leads = json.load(f)
    if not isinstance(leads, list):
        leads = leads.get("leads", [])
    if any(l.get("institution_slug") == slug for l in leads):
        return  # already have this lead
    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": opportunity_type,
        "opportunity_description": description,
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
        "created_at": datetime.utcnow().isoformat() + "Z",
        "status": "pending",
    }
    leads.append(lead)
    with open(leads_path, "w") as f:
        json.dump(leads, f, indent=2)


def process_institution(slug: str, url: str, name: str) -> tuple[str, int, int]:
    """Process one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        update_last_scrape(inst_dir, "error", 0, err)
        append_scrape_log(inst_dir, RUN_ID, "error", 0, 0, err)
        return "error", 0, 0

    doc_links = extract_doc_links(html, url)
    tenders = parse_tenders_from_html(html, slug, url, name)

    if tenders:
        doc_count = 0
        for t in tenders:
            tid = t["tender_id"]
            if "documents" not in t:
                t["documents"] = []
            docs = t.get("documents", [])
            download_dir = inst_dir / "downloads" / tid / "original"
            extract_dir = inst_dir / "downloads" / tid / "extracted"
            download_dir.mkdir(parents=True, exist_ok=True)
            extract_dir.mkdir(parents=True, exist_ok=True)
            urls_to_dl = [d.get("original_url") for d in docs if isinstance(d, dict) and d.get("original_url")]
            if not urls_to_dl:
                urls_to_dl = doc_links
            for durl in urls_to_dl[:15]:
                if durl and download_document(durl, download_dir):
                    doc_count += 1
                    t["documents"].append({"original_url": durl, "local_path": str(download_dir)})
            # Save to active or closed based on closing_date
            closing = t.get("closing_date")
            is_closed = False
            if closing:
                m = re.search(r"(\d{4})", str(closing))
                if m:
                    yr = int(m.group(1))
                    if yr < datetime.now().year:
                        is_closed = True
                    elif yr == datetime.now().year:
                        for fmt in ["%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%Y-%m-%d", "%d/%m/%Y"]:
                            try:
                                dt = datetime.strptime(str(closing).strip()[:50], fmt)
                                if dt.date() < datetime.now().date():
                                    is_closed = True
                                break
                            except ValueError:
                                continue
            subdir = "closed" if is_closed else "active"
            (inst_dir / "tenders" / subdir).mkdir(parents=True, exist_ok=True)
            tender_path = inst_dir / "tenders" / subdir / f"{tid}.json"
            with open(tender_path, "w") as f:
                json.dump(t, f, indent=2)
        update_last_scrape(inst_dir, "success", len(tenders))
        append_scrape_log(inst_dir, RUN_ID, "success", len(tenders), doc_count)
        return "success", len(tenders), doc_count
    else:
        # No tenders: opportunities workflow
        emails = extract_emails(html)
        if not emails:
            domain = urlparse(url).netloc.replace("www.", "")
            emails = [f"info@{domain}"]
        append_lead(slug, name, url, emails, "sell",
            f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.")
        update_last_scrape(inst_dir, "no_tenders", 0)
        append_scrape_log(inst_dir, RUN_ID, "no_tenders", 0, 0)
        return "no_tenders", 0, 0


def main():
    results = []
    for slug, url, name in INSTITUTIONS:
        try:
            status, tc, dc = process_institution(slug, url, name)
            results.append((slug, status, tc, dc))
            print(f"RESULT|{slug}|{status}|{tc}|{dc}")
        except Exception as e:
            inst_dir = PROJECT / "institutions" / slug
            ensure_dirs(inst_dir)
            update_last_scrape(inst_dir, "error", 0, str(e))
            append_scrape_log(inst_dir, RUN_ID, "error", 0, 0, str(e))
            results.append((slug, "error", 0, 0))
            print(f"RESULT|{slug}|error|0|0")
    # Sync leads CSV if any no_tenders
    if any(r[1] == "no_tenders" for r in results):
        subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
