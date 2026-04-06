#!/usr/bin/env python3
"""
Scrape 25 institutions for active tenders.
Run ID: run_20260313_205329_batch107
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
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
RUN_ID = "run_20260313_205329_batch107"

INSTITUTIONS = [
    ("smilesmedicstomatology", "https://smilesmedicstomatology.co.tz/"),
    ("soap", "https://soap.co.tz/"),
    ("sofascore", "https://www.sofascore.com/"),
    ("softmed", "https://softmed.co.tz/"),
    ("softnet", "https://softnet.co.tz/"),
    ("sokobora", "https://sokobora.co.tz/"),
    ("solomon", "https://solomon.co.tz/"),
    ("solutionplus", "https://solutionplus.co.tz/"),
    ("somaconnect", "https://somaconnect.or.tz/"),  # homepage; notes/show URL may be session-specific
    ("somaexpress", "https://somaexpress.co.tz/"),
    ("somango", "https://somango.co.tz/"),
    ("songeasmartcollege", "https://songeasmartcollege.ac.tz/"),
    ("sophytravel", "https://www.sophytravel.co.tz/"),
    ("sortsolutions", "https://sortsolutions.co.tz/"),
    ("soundandvision", "https://soundandvision.co.tz/"),
    ("southernlink", "https://southernlink.co.tz/"),
    ("souwasa", "https://nest.go.tz/tenders/published-tenders?search=souwasa"),
    ("spade", "https://spade.co.tz/"),
    ("spaide", "https://spaide.or.tz/"),
    ("spanishtiles", "https://spanishtiles.co.tz/"),
    ("spareline", "https://spareline.co.tz/"),
    ("sparklean", "https://sparklean.co.tz/"),
    ("sparks", "https://sparks.co.tz/"),
    ("spectrum-insurance", "https://spectrum-insurance.co.tz/"),
    ("speedyprint", "https://speedyprint.co.tz/"),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|procurement|zabuni|rfp|rfq|rfi|eoi|bid|quotation|supply|invitation|manunuzi)\b",
    re.I,
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-m", str(timeout), "-A", "Mozilla/5.0 (compatible; TendersBot/1.0)", url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, r.stderr or "curl failed"
        return r.stdout or "", None
    except Exception as e:
        return None, str(e)


def parse_tenders(html: str, base_url: str, slug: str) -> list[dict]:
    """Parse HTML for tender-like content. Returns list of tender dicts."""
    tenders = []
    if not html or len(html) < 100:
        return tenders

    try:
        from lxml import html as lxml_html

        tree = lxml_html.fromstring(html)
        tree.make_links_absolute(base_url)

        doc_links = []
        for a in tree.xpath("//a[@href]"):
            href = a.get("href", "")
            if any(href.lower().endswith(ext) for ext in DOC_EXT):
                doc_links.append({"url": href, "text": (a.text or "").strip()})

        containers = tree.xpath(
            "//article | //*[contains(@class,'tender')] | //*[contains(@class,'card')] | "
            "//*[contains(@class,'content')] | //main | //*[contains(@class,'entry-content')] | "
            "//*[contains(@class,'page-content')] | //li | //tr"
        )

        seen_titles = set()
        for elem in containers:
            text = (elem.text_content() or "").strip()
            if len(text) < 30:
                continue
            if not TENDER_KEYWORDS.search(text):
                continue

            title_elem = elem.xpath(".//h1 | .//h2 | .//h3 | .//h4 | .//*[contains(@class,'title')]")
            title = (title_elem[0].text_content().strip() if title_elem else text[:200]).strip()
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)

            date_elem = elem.xpath(".//*[contains(@class,'date')] | .//*[contains(@class,'closing')] | .//time")
            date_str = date_elem[0].text_content().strip() if date_elem else None

            elem_docs = []
            for a in elem.xpath(".//a[@href]"):
                href = a.get("href", "")
                if any(href.lower().endswith(ext) for ext in DOC_EXT):
                    elem_docs.append(href)

            emails = list(set(EMAIL_PATTERN.findall(text)))

            tenders.append({
                "title": title[:500],
                "description": text[:2000] if len(text) > 200 else "",
                "published_date": date_str,
                "closing_date": None,
                "document_links": elem_docs or [d["url"] for d in doc_links if d["url"] not in elem_docs][:5],
                "contact": {"email": emails[0]} if emails else {},
                "source_url": base_url,
            })
            if len(tenders) >= 20:
                break

        if not tenders and doc_links and TENDER_KEYWORDS.search(html):
            title = tree.xpath("//title/text()")
            title = title[0][:200] if title else "Tender / Procurement Notice"
            tenders.append({
                "title": title,
                "description": "",
                "published_date": None,
                "closing_date": None,
                "document_links": [d["url"] for d in doc_links[:10]],
                "contact": {},
                "source_url": base_url,
            })
    except Exception:
        pass
    return tenders


def download_document(url: str, dest: Path) -> bool:
    """Download a document to dest. Returns True on success."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-m", "60", "-A", "Mozilla/5.0 (compatible; TendersBot/1.0)", "-o", str(dest), url],
            capture_output=True,
            timeout=70,
        )
        if r.returncode != 0:
            return False
        if dest.exists() and dest.stat().st_size > 50_000_000:
            dest.unlink()
            return False
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def extract_text_from_doc(file_path: Path) -> bool:
    """Extract text from PDF/DOCX/XLSX to extracted/ folder."""
    ext = file_path.suffix.lower()
    out_dir = file_path.parent.parent / "extracted"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / (file_path.stem + ".txt")
    try:
        if ext == ".pdf":
            from tools.pdf.reader import extract_text
            text = extract_text(str(file_path))
            out_file.write_text(text, encoding="utf-8")
            return True
        elif ext == ".docx":
            from tools.docx.reader import extract_text
            text = extract_text(str(file_path))
            out_file.write_text(text, encoding="utf-8")
            return True
        elif ext in (".xls", ".xlsx"):
            from tools.xlsx.reader import extract_data
            data = extract_data(str(file_path))
            out_file.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
            return True
    except Exception:
        pass
    return False


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)


def get_tender_ids(slug: str, count: int) -> list[str]:
    slug_upper = slug.upper().replace("-", "")[:12]
    year = datetime.now(timezone.utc).strftime("%Y")
    active_dir = PROJECT / "institutions" / slug / "tenders" / "active"
    existing = list(active_dir.glob("*.json")) if active_dir.exists() else []
    base_seq = len(existing)
    return [f"{slug_upper}-{year}-{base_seq + i + 1:03d}" for i in range(count)]


def scrape_institution(slug: str, url: str) -> tuple[str, int, int]:
    """Scrape one institution. Returns (status, tender_count, doc_count)."""
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        _update_state(slug, "error", 0, 0, err)
        return "error", 0, 0

    tenders = parse_tenders(html, url, slug)

    if not tenders:
        emails = list(set(EMAIL_PATTERN.findall(html or "")))
        readme = inst_dir / "README.md"
        if readme.exists():
            emails.extend(EMAIL_PATTERN.findall(readme.read_text(encoding="utf-8")))
        emails = list(dict.fromkeys(e for e in emails if not any(x in e.lower() for x in (".png", ".jpg", "example.com", "wixpress", "sentry"))))[:10]

        inst_name = slug.replace("-", " ").title()
        lead = {
            "institution_slug": slug,
            "institution_name": inst_name,
            "website_url": url.rstrip("/"),
            "emails": emails[:5],
            "opportunity_type": "sell",
            "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
            "draft_email_body": f"Dear {inst_name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "pending",
        }
        leads_path = PROJECT / "opportunities" / "leads.json"
        leads = []
        if leads_path.exists():
            leads = json.loads(leads_path.read_text(encoding="utf-8"))
        if not isinstance(leads, list):
            leads = leads.get("leads", [])
        if not any(l.get("institution_slug") == slug for l in leads):
            leads.append(lead)
            leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

        _update_state(slug, "no_tenders", 0, 0)
        return "no_tenders", 0, 0

    doc_count = 0
    tender_ids = get_tender_ids(slug, min(len(tenders), 10))
    for i, t in enumerate(tenders[:10]):
        tender_id = tender_ids[i]
        tender_json = {
            "tender_id": tender_id,
            "institution": slug,
            "title": t["title"],
            "description": t.get("description", ""),
            "published_date": t.get("published_date"),
            "closing_date": t.get("closing_date"),
            "category": "General",
            "status": "active",
            "source_url": t.get("source_url", url),
            "documents": [],
            "contact": t.get("contact", {}),
            "scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        download_dir = inst_dir / "downloads" / tender_id / "original"
        download_dir.mkdir(parents=True, exist_ok=True)
        doc_links = t.get("document_links", [])
        for durl in doc_links[:5]:
            fname = Path(urlparse(durl).path).name or "document"
            if not any(fname.lower().endswith(ext) for ext in DOC_EXT):
                continue
            dest = download_dir / fname
            if download_document(durl, dest):
                doc_count += 1
                extract_text_from_doc(dest)
                tender_json["documents"].append({"url": durl, "local_path": str(dest.relative_to(inst_dir))})

        (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(
            json.dumps(tender_json, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    _update_state(slug, "success", len(tenders), doc_count)
    return "success", len(tenders), doc_count


def _update_state(slug: str, status: str, tender_count: int, doc_count: int, error: str | None = None):
    inst_dir = PROJECT / "institutions" / slug
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (inst_dir / "last_scrape.json").write_text(json.dumps({
        "institution": slug,
        "last_scrape": now,
        "run_id": RUN_ID,
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }, indent=2), encoding="utf-8")

    log_path = inst_dir / "scrape_log.json"
    log = {"runs": []}
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    log["runs"].append({
        "run_id": RUN_ID,
        "timestamp": now,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
    })
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")


def main():
    for i, (slug, url) in enumerate(INSTITUTIONS):
        if i > 0:
            time.sleep(10)
        try:
            status, tc, dc = scrape_institution(slug, url)
        except Exception as e:
            status, tc, dc = "error", 0, 0
            _update_state(slug, "error", 0, 0, str(e))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}", flush=True)

    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
