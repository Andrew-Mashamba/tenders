#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders. Run ID: run_20260313_205329_batch76
Institutions: mohsinsumar, moi, moic, moinfotech, mongarecollege, moprints, mopsquad,
morakasafaris, morogorodc, morogoroutaliicollege, morrisgems, moruwasa, moshidc, moshifm,
motherofmercy, mottocottages, mow, mowara, mozeti, mpabusinessassociates, mpandadc,
mpandaradio, mpi, mpl, mpomabiva
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch76"

INST_CONFIG = [
    ("mohsinsumar", "https://mohsinsumar.co.tz/", "Mohsin Sumar"),
    ("moi", "https://www.moi.ac.tz/", "Muhimbili Orthopaedic Institute"),
    ("moic", "https://moic.go.tz/zabuni.html", "WUMU - Ministry of Infrastructure"),
    ("moinfotech", "https://moinfotech.co.tz/", "MoinfoTech"),
    ("mongarecollege", "https://mongarecollege.ac.tz/", "Mongare College"),
    ("moprints", "https://moprints.co.tz/", "MO Prints"),
    ("mopsquad", "https://www.mopsquad.co.tz/", "Mopsquad"),
    ("morakasafaris", "https://morakasafaris.co.tz/", "Moraka Africa Safaris"),
    ("morogorodc", "https://morogorodc.go.tz/tenders", "Morogoro District Council"),
    ("morogoroutaliicollege", "https://morogoroutaliicollege.ac.tz/", "Morogoro Utalii College"),
    ("morrisgems", "https://morrisgems.co.tz/", "Morris Gems"),
    ("moruwasa", "https://moruwasa.go.tz/pages/Tenders.html", "MORUWASA"),
    ("moshidc", "https://moshidc.go.tz/tenders", "Moshi District Council"),
    ("moshifm", "https://moshifm.co.tz/", "MOSHI FM Radio"),
    ("motherofmercy", "https://motherofmercy.ac.tz/", "Mother of Mercy Academy"),
    ("mottocottages", "https://mottocottages.com/", "Motto Cottages"),
    ("mow", "https://mow.go.tz/", "Ministry of Works"),
    ("mowara", "https://mowara.co.tz/", "Mowara Limited"),
    ("mozeti", "https://mozeti.co.tz/", "Mozeti"),
    ("mpabusinessassociates", "https://mpabusinessassociates.co.tz/", "MPA Business Associates"),
    ("mpandadc", "https://mpandadc.go.tz/ugavi-na-manunuzi", "Tanganyika District Council"),
    ("mpandaradio", "https://mpandaradio.co.tz/", "Mpanda Radio FM"),
    ("mpi", "https://mpi.co.tz/", "M Plus Insurance"),
    ("mpl", "https://mpl.co.tz/", "Metal Products Limited"),
    ("mpomabiva", "https://mpomabiva.co.tz/", "Mpomabiva Investments"),
]

# Emails from READMEs
INST_EMAILS = {
    "mohsinsumar": [],
    "moi": ["info@moi.ac.tz"],
    "moic": ["info@moic.go.tz"],
    "moinfotech": ["info@moinfo.co.tz"],
    "mongarecollege": ["mongarecollege@yahoo.com"],
    "moprints": [],
    "mopsquad": ["info@mopsquad.co.tz", "webmaster@mopsquad.co.tz"],
    "morakasafaris": ["info@morakasafaris.co.tz"],
    "morogorodc": ["ded@morogorodc.go.tz"],
    "morogoroutaliicollege": ["webmaster@morogoroutaliicollege.ac.tz"],
    "morrisgems": [],
    "moruwasa": ["md@moruwasa.go.tz", "info@moruwasa.go.tz"],
    "moshidc": ["info@moshidc.go.tz", "ded@moshidc.go.tz"],
    "moshifm": ["moshifm@gmail.com", "radiomoshifm@gmail.com"],
    "motherofmercy": ["info@motherofmercy.ac.tz"],
    "mottocottages": [],
    "mow": ["ps@mow.go.tz"],
    "mowara": ["info@mowara.co.tz"],
    "mozeti": [],
    "mpabusinessassociates": ["info@mpabusinessassociate.co.tz"],
    "mpandadc": ["ded@tanganyikadc.go.tz"],
    "mpandaradio": [],
    "mpi": [],
    "mpl": ["sales@mpl.co.tz"],
    "mpomabiva": [],
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
    if "zabuni" in html.lower() or "tender" in html.lower():
        # Look for table structure
        rows = re.findall(r"<tr[^>]*>.*?</tr>", html, re.DOTALL | re.I)
        for row in rows:
            if TENDER_KEYWORDS.search(row):
                cells = re.findall(r"<t[dh][^>]*>([^<]*)</t[dh]>", row, re.I)
                if len(cells) >= 2:
                    title = cells[1].strip() if len(cells) > 1 else cells[0].strip()
                    if len(title) > 5 and "imefungwa" not in title.lower():
                        tenders.append({"title": title, "description": "", "doc_links": []})

    # If no table tenders but has tender keywords, check for "under construction" etc
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
    for i, t in enumerate(tenders[:20], 1):  # cap at 20
        tid = f"{slug.upper()[:8]}-{year}-{i:03d}"
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

        # Download docs for this tender
        download_dir = inst_dir / "downloads" / tid / "original"
        download_dir.mkdir(parents=True, exist_ok=True)
        for doc_url in doc_urls[:5]:  # limit docs per tender
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
