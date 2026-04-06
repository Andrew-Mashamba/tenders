#!/usr/bin/env python3
"""
Batch scrape 25 institutions for active tenders.
Run ID: run_20260313_205329_batch11
"""
import sys
from pathlib import Path

# Ensure project root is on path for tools imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PROJECT = Path(__file__).resolve().parent.parent
RUN_ID = "run_20260313_205329_batch11"

INSTITUTIONS = [
    ("ate", "https://ate.or.tz/"),
    ("ateb", "https://www.ateb.co.tz/"),
    ("ati", "https://ati.co.tz/"),
    ("atlascopco", "https://www.atlascopco.com/"),
    ("atma", "https://atma.co.tz/"),
    ("atms", "https://atms.co.tz/"),
    ("atologistics", "https://atologistics.co.tz/"),
    ("atomcoffee", "https://www.atomcoffee.co.tz/"),
    ("atoz", "https://atoz.co.tz/"),
    ("atozsupermarket", "https://atozsupermarket.co.tz/"),
    ("atric", "https://atric.co.tz/"),
    ("atthewheel", "https://atthewheel.co.tz/"),
    ("aua", "https://aua.co.ke/"),  # tender_url points to PNG, use homepage
    ("auditaxinternational", "https://auditaxinternational.co.tz/training/invitation-of-you-and-your-staff-to-a-practical-5-day-fixed-assets-inventory-management-and-procurement-seminar-with-cpd-hours-to-be-held-form-11th-to-15th-may-2026-at-morena-hotel/"),
    ("auditmax", "https://auditmax.co.tz/"),
    ("auki", "https://auki.co.tz/"),
    ("aurasynergies", "https://aurasynergies.co.tz/"),
    ("auto-xpress", "https://auto-xpress.co.tz/"),
    ("autofest", "https://autofest.co.tz/"),
    ("autofreight", "https://autofreight.co.tz/"),
    ("automark", "https://www.automark.co.tz/"),
    ("autorover", "https://autorover.co.tz/"),
    ("aviasales", "https://www.aviasales.co.tz/"),
    ("aviatorsafaris", "http://aviatorsafaris.co.tz/"),
    ("avowal", "https://avowal.co.tz/"),
]

# Optional: skip already-processed (set via env BATCH_SKIP_FIRST=17 to resume)
import os
_skip = int(os.environ.get("BATCH_SKIP_FIRST", "0"))
if _skip > 0:
    INSTITUTIONS = INSTITUTIONS[_skip:]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|procurement|zabuni|rfp|rfq|rfi|eoi|bid|quotation|supply|invitation)\b",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL, return (html, error)."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        with urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except (URLError, HTTPError, OSError) as e:
        return None, str(e)


def parse_tenders(html: str, base_url: str, slug: str) -> list[dict]:
    """Parse HTML for tender-like content. Returns list of tender dicts."""
    from lxml import html as lxml_html

    tenders = []
    if not html or len(html) < 100:
        return tenders

    try:
        tree = lxml_html.fromstring(html)
        tree.make_links_absolute(base_url)

        # Look for document links
        doc_links = []
        for a in tree.xpath("//a[@href]"):
            href = a.get("href", "")
            if any(href.lower().endswith(ext) for ext in DOC_EXT):
                doc_links.append({"url": href, "text": (a.text or "").strip()})

        # Look for tender-like sections: articles, cards, list items, table rows
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

            # Extract title from h2, h3, h4, or first line
            title_elem = elem.xpath(".//h1 | .//h2 | .//h3 | .//h4 | .//*[contains(@class,'title')]")
            title = (title_elem[0].text_content().strip() if title_elem else text[:200]).strip()
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)

            # Extract dates
            date_elem = elem.xpath(".//*[contains(@class,'date')] | .//*[contains(@class,'closing')] | .//time")
            date_str = date_elem[0].text_content().strip() if date_elem else None

            # Get doc links within this element
            elem_docs = []
            for a in elem.xpath(".//a[@href]"):
                href = a.get("href", "")
                if any(href.lower().endswith(ext) for ext in DOC_EXT):
                    elem_docs.append(href)

            # Extract emails
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

        # If no structured tenders but we have doc links and tender keywords on page
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
    except Exception as e:
        pass  # Return empty on parse error
    return tenders


def download_document(url: str, dest: Path) -> bool:
    """Download a document to dest. Returns True on success."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        with urlopen(req, timeout=60) as r:
            data = r.read()
            if len(data) > 50_000_000:  # 50MB
                return False
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return True
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
    """Generate tender IDs: {SLUG}-{YEAR}-{SEQ}."""
    slug_upper = slug.upper().replace("-", "")
    year = datetime.now(timezone.utc).strftime("%Y")
    active_dir = PROJECT / "institutions" / slug / "tenders" / "active"
    existing = list(active_dir.glob("*.json")) if active_dir.exists() else []
    base_seq = len(existing)
    return [f"{slug_upper}-{year}-{base_seq + i + 1:03d}" for i in range(count)]


def scrape_institution(slug: str, url: str) -> tuple[str, int, int]:
    """
    Scrape one institution. Returns (status, tender_count, doc_count).
    status: success|no_tenders|error
    """
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        _update_state(slug, "error", 0, 0, err)
        return "error", 0, 0

    tenders = parse_tenders(html, url, slug)

    if not tenders:
        # No tenders: create lead
        emails = list(set(EMAIL_PATTERN.findall(html or "")))
        # Get contact from README
        readme = inst_dir / "README.md"
        if readme.exists():
            readme_text = readme.read_text(encoding="utf-8")
            emails.extend(EMAIL_PATTERN.findall(readme_text))
        emails = list(dict.fromkeys(e for e in emails if not e.endswith((".png", ".jpg", "example.com"))))[:10]

        inst_name = slug.replace("-", " ").title()
        lead = {
            "institution_slug": slug,
            "institution_name": inst_name,
            "website_url": url,
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
        # Avoid duplicate
        if not any(l.get("institution_slug") == slug for l in leads):
            leads.append(lead)
            leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

        _update_state(slug, "no_tenders", 0, 0)
        return "no_tenders", 0, 0

    # Save tenders and download documents
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
    results = []
    for i, (slug, url) in enumerate(INSTITUTIONS):
        if i > 0:
            time.sleep(10)  # Rate limit per anti_bot config
        try:
            status, tc, dc = scrape_institution(slug, url)
        except Exception as e:
            status, tc, dc = "error", 0, 0
            _update_state(slug, "error", 0, 0, str(e))
        print(f"RESULT|{slug}|{status}|{tc}|{dc}", flush=True)
        results.append((slug, status, tc, dc))

    # Run sync_leads_csv if any leads were added
    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=str(PROJECT), check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
