#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders. Run ID: run_20260313_205329_batch78
Institutions: mtmerugamelodge, mtt, mtuwasa, mtwaraktc, mtwaramikindanimc, muhezadc,
muhunda, mukonossolutions, mukurucamps, mul-t-lock, mulas, mulebadc, mulika,
multiplexsystems, multistruct, mum, munawarfoods, murtazaversi, musabeschools,
musomavijijini, must, mutokitilabs, muungwanaopenschool, muwasa, muwsa
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch78"

INST_CONFIG = [
    ("mtmerugamelodge", "https://mountmerugamelodge.co.tz/", "MMGL: Home"),
    ("mtt", "https://mtt.co.tz/", "MASTERMIND TOBACCO TANZANIA"),
    ("mtuwasa", "https://mtuwasa.go.tz/", "MTUWASA"),
    ("mtwaraktc", "https://mtwaraktc.ac.tz/", "Ministry of Water Water Institute"),
    ("mtwaramikindanimc", "https://mtwaramikindanimc.go.tz/new/idara-ya-ardhi-yakabidhiwa-pikipiki-kudhibiti-ujenzi-holela", "Mtwara Mikindani Municipal Council"),
    ("muhezadc", "https://muhezadc.go.tz/procurement", "Muheza District Council"),
    ("muhunda", "https://www.muhunda.co.tz/", "Muhunda Resources Limited"),
    ("mukonossolutions", "https://mukonossolutions.co.tz/", "Mukonos Solutions"),
    ("mukurucamps", "https://mukurucamps.co.tz/", "Mukuru Eco-Tented Camps"),
    ("mul-t-lock", "https://www.mul-t-lock.com/", "MUL-T-LOCK"),
    ("mulas", "https://mulas.co.tz/", "Mulas car rental"),
    ("mulebadc", "https://mulebadc.go.tz/tenders", "Muleba District Council"),
    ("mulika", "https://www.mulika.or.tz/", "mulika youth organization"),
    ("multiplexsystems", "https://multiplexsystems.co.tz/", "Multiplex Systems Limited"),
    ("multistruct", "https://www.multistruct.co.tz/", "MultiStruct Tanzania Ltd"),
    ("mum", "https://mum.ac.tz/single-news-and-events/mum-iium-kuanzisha-mradi-wa-bidhaa-halali", "Muslim University"),
    ("munawarfoods", "https://munawarfoods.co.tz/", "Munawar Food"),
    ("murtazaversi", "https://murtazaversi.co.tz/", "Murtaza Versi"),
    ("musabeschools", "https://musabeschools.ac.tz/", "Musabe Schools"),
    ("musomavijijini", "https://www.musomavijijini.or.tz/", "Musoma Vijijini"),
    ("must", "https://must.ac.tz/directorates/vice-chancellor/procurement-management-unit", "Mbeya University of Science and Technology"),
    ("mutokitilabs", "https://www.mutokitilabs.co.tz/", "Mutokiti Diagonistic Laboratories"),
    ("muungwanaopenschool", "https://muungwanaopenschool.ac.tz/", "Muungwana Open School"),
    ("muwasa", "https://muwasa.go.tz/", "MUWASA"),
    ("muwsa", "https://muwsa.go.tz/", "MUWSA"),
]

INST_EMAILS = {
    "mtmerugamelodge": ["info@mtmerugamelodge.co.tz", "reservations@mtmerugamelodge.co.tz"],
    "mtt": [],
    "mtuwasa": ["info@mtuwasa.go.tz", "info@muwaza.go.tz"],
    "mtwaraktc": ["rector@waterinstitute.ac.tz"],
    "mtwaramikindanimc": ["md@mtwaramikindanimc.go.tz"],
    "muhezadc": ["ded@muhezadc.go.tz"],
    "muhunda": ["gerald.nyerere@muhunda.co.tz", "muhunda@muhunda.co.tz"],
    "mukonossolutions": ["info@mukonossolutions.co.tz"],
    "mukurucamps": ["info@mukurucamps.co.tz"],
    "mul-t-lock": [],
    "mulas": ["support@zanzibarcarrent.co.tz", "info@zanzibarcarrent.co.tz"],
    "mulebadc": ["ded@mulebadc.go.tz"],
    "mulika": ["info@mulika.or.tz", "ceo@mulika.or.tz", "programs@mulika.or.tz"],
    "multiplexsystems": [],
    "multistruct": ["info@multistruct.co.tz"],
    "mum": ["mum@mum.ac.tz"],
    "munawarfoods": ["info@munawarfoods.co.tz", "munawarnuts@yahoo.com"],
    "murtazaversi": [],
    "musabeschools": ["info@musabeschools.ac.tz"],
    "musomavijijini": [],
    "must": ["must@must.ac.tz"],
    "mutokitilabs": ["info@mutokitilabs.co.tz"],
    "muungwanaopenschool": ["info@muungwanaopenschool.ac.tz"],
    "muwasa": ["ps@muwasa.go.tz"],
    "muwsa": ["info@muwsa.go.tz"],
}

TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfq|rfi|bid|auction|supply)\b",
    re.I,
)
DOC_EXT = re.compile(r"\.(pdf|doc|docx|xls|xlsx|zip|rar)$", re.I)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, timeout: int = 15) -> tuple[str | None, str | None]:
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

    # Check for tender keywords
    if not TENDER_KEYWORDS.search(html):
        return tenders, doc_urls

    # Find document links
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = m.group(1).strip()
        if DOC_EXT.search(href):
            full = urljoin(base_url, href)
            if full not in doc_urls:
                doc_urls.append(full)

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
        tid = f"{slug.upper().replace('-', '')[:8]}-{year}-{i:03d}"
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


def extract_text_from_docs(inst_dir: Path) -> int:
    """Extract text from downloaded docs using tools. Returns count of extracted files."""
    extracted = 0
    try:
        for tid_dir in (inst_dir / "downloads").iterdir():
            if not tid_dir.is_dir():
                continue
            orig = tid_dir / "original"
            extr = tid_dir / "extracted"
            if not orig.exists():
                continue
            extr.mkdir(parents=True, exist_ok=True)
            for f in orig.iterdir():
                if f.suffix.lower() in (".pdf", ".docx"):
                    out_txt = extr / (f.stem + ".txt")
                    if out_txt.exists():
                        continue
                    try:
                        subprocess.run(
                            [sys.executable, "-m", "tools", "pdf" if f.suffix.lower() == ".pdf" else "docx", "read", str(f)],
                            cwd=str(PROJECT),
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )
                        # tools prints to stdout; we'd need to capture - for now skip extraction
                        # to avoid complexity
                    except Exception:
                        pass
    except Exception:
        pass
    return extracted


def main():
    results = []
    leads_added = 0

    for slug, url, name in INST_CONFIG:
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)

        html, err = fetch_url(url)
        if err or not html:
            update_last_scrape(inst_dir, "error", 0, err or "Fetch failed")
            append_scrape_log(inst_dir, "error", 0, 0, [err or "Fetch failed"])
            emails = INST_EMAILS.get(slug, [])
            if append_lead(slug, name, url, emails, "sell", f"Site {url} unreachable or timeout. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."):
                leads_added += 1
            print(f"RESULT|{slug}|error|0|0")
            results.append((slug, "error", 0, 0))
            continue

        tenders, doc_urls = parse_tenders(html, url)
        tender_count = len(tenders)
        doc_count = 0

        if tender_count > 0:
            doc_count = save_tenders_and_download(inst_dir, slug, tenders, doc_urls, url)
            status = "success"
        else:
            status = "success"
            emails = INST_EMAILS.get(slug, []) + extract_emails(html)
            emails = list(dict.fromkeys(e for e in emails if "example" not in e.lower() and "sentry" not in e.lower()))
            if append_lead(slug, name, url, emails):
                leads_added += 1

        update_last_scrape(inst_dir, status, tender_count)
        append_scrape_log(inst_dir, status, tender_count, doc_count, [])
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")
        results.append((slug, status, tender_count, doc_count))

    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], cwd=str(PROJECT), check=False)

    print(f"\n--- BATCH COMPLETE: {len(results)} institutions, {leads_added} new leads appended ---")


if __name__ == "__main__":
    main()
