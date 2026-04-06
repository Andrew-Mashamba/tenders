#!/usr/bin/env python3
"""
Scrape 25 institutions (salihospital through sayarinews) for active tenders.
Run ID: run_20260315_060430_batch101
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch101"

INSTITUTIONS = [
    ("salihospital", "https://salihospital.co.tz/", "Sali International Hospital"),
    ("salimaoxygen", "https://salimaoxygen.co.tz/", "Salima Oxygen Ltd"),
    ("samedc", "https://samedc.go.tz/tenders", "Same District Council"),
    ("samsonite", "https://samsonite.co.tz/", "Samsonite"),
    ("sanaa", "https://sanaa.co.tz/", "Sanaa"),
    ("sanavita", "https://sanavita.co.tz/", "Sanavita"),
    ("sandc", "https://sandc.co.tz/", "SandC Technology"),
    ("sands", "https://sands.co.tz/", "SandS Designs"),
    ("sarclawchambers", "https://www.sarclawchambers.co.tz/", "SARC Law Chambers"),
    ("sarojoah", "https://sarojoah.co.tz/", "SAROJOAH"),
    ("sas", "https://sas.co.tz/", "Safety & Security Centre"),
    ("sasandmat", "https://sasandmat.co.tz/", "SAS & MAT Company"),
    ("sasatech", "https://sasatech.co.tz/", "Sasatech"),
    ("sascom", "https://sascom.co.tz/", "Sascom Technologies"),
    ("satf", "https://satf.or.tz/", "SATF"),
    ("saut", "https://saut.ac.tz/", "St. Augustine University"),
    ("sautarusha", "https://sautarusha.ac.tz/", "SAUT Arusha"),
    ("sautdarcentre", "https://sautdarcentre.ac.tz/", "SAUT Dar Centre"),
    ("savannahplains", "https://savannahplains.ac.tz/", "Savannah Plains"),
    ("savannahtz", "https://savannahtz.co.tz/", "Savannah Tours"),
    ("savethechildren", "https://www.savethechildren.net/", "Save the Children"),
    ("savvy", "https://savvy.co.tz/", "Savvy Engineering"),
    ("sawa", "https://sawa.or.tz/", "SAWA Wanawake"),
    ("sawainitiative", "https://www.sawainitiative.or.tz/", "SAWA Initiative"),
    ("sayarinews", "https://www.sayarinews.co.tz/", "Sayari News"),
]

DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfi|eoi|bid|quotation)\b",
    re.I,
)


def extract_emails(html: str, base_url: str) -> list[str]:
    """Extract email addresses from HTML."""
    emails = set()
    for m in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html):
        e = m.group().lower()
        if not any(x in e for x in ["@2x", "example.com", "wixpress", "sentry", "gravatar"]):
            emails.add(e)
    return sorted(emails)


def extract_doc_links(soup: BeautifulSoup, base_url: str) -> list[dict]:
    """Extract document links (PDF, DOC, etc.) from page."""
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if any(href.lower().endswith(ext) for ext in DOC_EXTENSIONS):
            full_url = urljoin(base_url, href)
            links.append({"url": full_url, "text": (a.get_text() or "").strip()[:100]})
    return links


def has_tender_content(html: str, soup: BeautifulSoup) -> bool:
    """Check if page contains tender/procurement content."""
    text = soup.get_text() + " " + html
    if TENDER_KEYWORDS.search(text):
        return True
    # Check for common tender page structures
    for sel in [".tender-list", ".tender-item", "[class*='zabuni']", "[class*='tender']"]:
        if soup.select_one(sel):
            return True
    return False


def parse_tenders(soup: BeautifulSoup, base_url: str, slug: str) -> list[dict]:
    """Parse tender items from page. Returns list of tender dicts."""
    tenders = []
    # Try common selectors
    items = (
        soup.select(".tender-item")
        or soup.select("article.tender")
        or soup.select(".tender-list li")
        or soup.select("table tbody tr")
        or soup.select(".content article")
        or soup.select("main article")
    )
    if not items:
        # Fallback: look for blocks with document links
        doc_links = extract_doc_links(soup, base_url)
        if doc_links and has_tender_content("", soup):
            # Create one tender from page
            year = datetime.now().year
            seq = 1
            tender_id = f"{slug.upper()[:8]}-{year}-{seq:03d}"
            tenders.append({
                "tender_id": tender_id,
                "institution": slug,
                "title": soup.title.string if soup.title else "Tender",
                "source_url": base_url,
                "documents": [d["url"] for d in doc_links],
            })
    else:
        year = datetime.now().year
        for i, item in enumerate(items[:50], 1):
            title_el = item.select_one("h2, h3, h4, .tender-title, a")
            title = (title_el.get_text() if title_el else "").strip() or f"Tender {i}"
            date_el = item.select_one(".date, .closing-date, time")
            date_val = (date_el.get_text() if date_el else "").strip()
            doc_links = [
                urljoin(base_url, a["href"])
                for a in item.find_all("a", href=True)
                if any(a["href"].lower().endswith(ext) for ext in DOC_EXTENSIONS)
            ]
            tender_id = f"{slug.upper()[:8]}-{year}-{i:03d}"
            tenders.append({
                "tender_id": tender_id,
                "institution": slug,
                "title": title,
                "published_date": date_val,
                "closing_date": date_val,
                "source_url": base_url,
                "documents": doc_links,
            })
    return tenders


def fetch_page(url: str) -> tuple[str | None, str | None]:
    """Fetch page. Returns (html, error)."""
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        r.raise_for_status()
        return r.text, None
    except Exception as e:
        return None, str(e)


def download_document(url: str, dest: Path) -> bool:
    """Download a document to dest. Returns True on success."""
    try:
        r = requests.get(url, timeout=60, stream=True)
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return True
    except Exception:
        return False


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def process_institution(slug: str, url: str, name: str) -> dict:
    """Process one institution. Returns result dict."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_page(url)
    if err:
        result = {"status": "error", "tender_count": 0, "doc_count": 0, "error": err}
    else:
        soup = BeautifulSoup(html, "html.parser")
        tenders = parse_tenders(soup, url, slug)

        if tenders:
            doc_count = 0
            for t in tenders:
                t["description"] = ""
                t["status"] = "active"
                t["contact"] = {}
                t["scraped_at"] = datetime.now(timezone.utc).isoformat()
                tender_id = t["tender_id"]
                json_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
                json_path.parent.mkdir(parents=True, exist_ok=True)
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(t, f, indent=2, ensure_ascii=False)

                # Download documents
                download_dir = inst_dir / "downloads" / tender_id / "original"
                extract_dir = inst_dir / "downloads" / tender_id / "extracted"
                for doc_url in t.get("documents", []):
                    try:
                        fname = Path(urlparse(doc_url).path).name or "document.pdf"
                        dest = download_dir / fname
                        if download_document(doc_url, dest):
                            doc_count += 1
                            # Extract text if tools available
                            if dest.suffix.lower() == ".pdf" and (PROJECT / ".venv").exists():
                                try:
                                    ext_path = extract_dir / (dest.stem + ".txt")
                                    extract_dir.mkdir(parents=True, exist_ok=True)
                                    subprocess.run(
                                        ["python3", "-m", "tools", "pdf", "read", str(dest)],
                                        cwd=PROJECT,
                                        capture_output=True,
                                        timeout=30,
                                        env={**os.environ, "PATH": str(PROJECT / ".venv" / "bin") + ":" + os.environ.get("PATH", "")},
                                    )
                                except Exception:
                                    pass
                    except Exception:
                        pass
            result = {"status": "tenders_found", "tender_count": len(tenders), "doc_count": doc_count, "error": None}
        else:
            # No tenders: create lead
            emails = extract_emails(html, url)
            lead = {
                "institution_slug": slug,
                "institution_name": name,
                "website_url": url,
                "emails": emails if emails else [f"info@{urlparse(url).netloc}".replace("www.", "")],
                "opportunity_type": "sell",
                "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
                "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
                "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "status": "pending",
            }
            leads_path = PROJECT / "opportunities" / "leads.json"
            leads = []
            if leads_path.exists():
                with open(leads_path) as f:
                    data = json.load(f)
                leads = data if isinstance(data, list) else (data.get("leads") or [])
                if not isinstance(leads, list):
                    leads = []
            if not any(l.get("institution_slug") == slug for l in leads):
                leads.append(lead)
                with open(leads_path, "w", encoding="utf-8") as f:
                    json.dump(leads, f, indent=2, ensure_ascii=False)
            result = {"status": "no_tenders", "tender_count": 0, "doc_count": 0, "error": None}

    # Update last_scrape.json and scrape_log.json
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "run_id": RUN_ID,
        "scraped_at": now,
        "status": result["status"],
        "tender_count": result["tender_count"],
        "doc_count": result["doc_count"],
        "error": result.get("error"),
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last, f, indent=2)

    log_path = inst_dir / "scrape_log.json"
    log = []
    if log_path.exists():
        with open(log_path) as f:
            raw = json.load(f)
        log = raw if isinstance(raw, list) else (raw.get("runs") or raw.get("log") or [])
        if not isinstance(log, list):
            log = []
    log.append(last)
    with open(log_path, "w") as f:
        json.dump(log[-100:], f, indent=2)

    return result


def main():
    filter_slugs = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    results = []
    for slug, url, name in INSTITUTIONS:
        if filter_slugs and slug not in filter_slugs:
            continue
        try:
            r = process_institution(slug, url, name)
            status = r["status"]
            tc = r["tender_count"]
            dc = r["doc_count"]
            print(f"RESULT|{slug}|{status}|{tc}|{dc}")
            results.append((slug, status, tc, dc))
        except Exception as e:
            print(f"RESULT|{slug}|error|0|0")
            print(f"ERROR|{slug}|{e}", file=sys.stderr)
            results.append((slug, "error", 0, 0))

    # Run sync_leads_csv if any leads were added
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], cwd=PROJECT, capture_output=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
