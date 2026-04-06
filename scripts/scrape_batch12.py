#!/usr/bin/env python3
"""Scrape 25 institutions for active tenders. Run ID: run_20260315_060430_batch12"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
sys.path.insert(0, str(PROJECT))
RUN_ID = "run_20260315_060430_batch12"

# (slug, tender_url, institution_name) - bakwata uses homepage (tender_url is JS file)
INSTITUTIONS = [
    ("axis-tanzania", "https://www.axis.mu/", "Axis - Trusted first - Axis"),
    ("azampesa", "https://azampesa.co.tz/", "Azampesa Website | Rahisisha Malipo"),
    ("azamtv", "https://azamtv.co.tz/", "home"),
    ("azamupholstery", "https://www.azamupholstery.co.tz/", "Azam Upholstery Car Interiors"),
    ("azania-bank", "https://azaniabank.co.tz/tenders/", "Azania Bank Tanzania"),
    ("azaniabank", "https://azaniabank.co.tz/tenders/", "Azania Bank"),
    ("azaniasecondary", "https://azaniasecondary.sc.tz/", "Azania Secondary"),
    ("aziendagroup", "https://aziendagroup.co.tz/", "AZIENDA"),
    ("azura", "https://azura.co.tz/", "Fayheroes fitness club Ltd"),
    ("azzaman", "https://www.azzaman.co.tz/", "AzZaman Shopping"),
    ("b2zlogistics", "https://b2zlogistics.co.tz/b2z-pipeline#a-z-procurement", "B2Z Logistics"),
    ("babaoffice", "https://babaoffice.co.tz/", "Baba Office Supplies & Solutions Ltd"),
    ("babatidc", "https://babatidc.go.tz/tenders", "Babati District Council"),
    ("babatitc", "https://babatitc.go.tz/procurement", "Babati Town Council"),
    ("bac", "https://bac.co.tz/", "Burhani Associates & Co"),
    ("backbone", "http://backbone.co.tz/", "Login to Cacti"),
    ("backyardrecords", "https://backyardrecords.co.tz/", "BACKYARD RECORDS"),
    ("bagamoyo", "https://bagamoyo.sc.tz/", "Bagamoyo Secondary School"),
    ("bajeti", "https://www.bajeti.co.tz/", "Bajeti"),  # homepage; tender_url was Facebook
    ("bakaid", "https://bakaid.or.tz/", "BAKAID"),
    ("bakhita", "https://www.bakhita.ac.tz/", "St Bakhita Health Training Institute"),
    ("bakita", "https://bakita.go.tz/", "BAKITA"),
    ("bakwata", "https://bakwata.or.tz/", "BAKWATA"),
    ("balajipharma", "https://balajipharma.co.tz/", "balajipharma"),
    ("balloonsafaris", "https://www.balloonsafaris.com/", "Serengeti Balloon Safaris"),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|procurement|zabuni|manunuzi|rfp|rfi|rfq|eoi|bid\s+document|invitation\s+to\s+bid|request\s+for\s+proposal|supply|quotation)\b",
    re.I,
)
DOC_EXTS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


class LinkExtractor(HTMLParser):
    """Extract links, document URLs, and emails from HTML."""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links = []
        self.doc_links = []
        self.emails = set()
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href and not href.startswith("#") and not href.startswith("javascript:"):
                full = urljoin(self.base_url, href)
                self.links.append(full)
                low = full.lower()
                if any(low.endswith(ext) for ext in DOC_EXTS):
                    self.doc_links.append(full)
        elif tag == "script" or tag == "style":
            self._skip = True
        else:
            self._skip = getattr(self, "_skip", False)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = False

    def handle_data(self, data):
        if getattr(self, "_skip", False):
            return
        text = data.strip()
        if text:
            self.text_parts.append(text)
        for m in EMAIL_RE.finditer(data):
            e = m.group(0).lower()
            if "example" not in e and "domain" not in e and "sentry" not in e and ".png" not in e:
                self.emails.add(e)


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL via curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-skL", "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", "--max-time", str(timeout), url],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}: {(r.stderr or '')[:200]}"
        return r.stdout or "", None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def has_tender_content(html: str, text: str) -> bool:
    """Check if page contains tender/procurement content."""
    combined = (html + " " + text).lower()
    return bool(TENDER_KEYWORDS.search(combined))


def extract_tender_items(html: str, base_url: str) -> tuple[list[dict], list[str]]:
    """Parse HTML for tender-like items. Returns (items, emails)."""
    parser = LinkExtractor(base_url)
    try:
        parser.feed(html)
    except Exception:
        pass
    items = []
    for doc_url in parser.doc_links:
        items.append({
            "title": Path(urlparse(doc_url).path).name or "Document",
            "document_links": [doc_url],
            "source_url": base_url,
        })
    if not items and parser.links:
        for link in parser.links[:20]:
            if any(link.lower().endswith(ext) for ext in DOC_EXTS):
                items.append({
                    "title": Path(urlparse(link).path).name or "Document",
                    "document_links": [link],
                    "source_url": base_url,
                })
                break
    return items, list(parser.emails)


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def download_document(url: str, dest: Path) -> bool:
    """Download a document to dest."""
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["curl", "-skL", "-o", str(dest), "--max-time", "60", "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", url],
            capture_output=True,
            timeout=70,
            check=True,
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def extract_text_from_doc(file_path: Path, extracted_dir: Path) -> bool:
    """Extract text from PDF/DOCX/XLSX to extracted/."""
    try:
        ext = file_path.suffix.lower()
        extracted_dir.mkdir(parents=True, exist_ok=True)
        out_name = file_path.stem + (".json" if ext == ".xlsx" else ".txt")
        out_path = extracted_dir / out_name
        if ext == ".pdf":
            from tools.pdf.reader import extract_text
            text = extract_text(str(file_path))
            out_path.write_text(text or "", encoding="utf-8")
            return True
        elif ext == ".docx":
            from tools.docx.reader import extract_text
            text = extract_text(str(file_path))
            out_path.write_text(text or "", encoding="utf-8")
            return True
        elif ext == ".xlsx":
            from tools.xlsx.reader import extract_data
            data = extract_data(str(file_path))
            out_path.write_text(json.dumps(data or {}, indent=2), encoding="utf-8")
            return True
    except Exception:
        pass
    return False


def scrape_institution(slug: str, name: str, tender_url: str, inst_dir: Path) -> dict:
    """Scrape one institution. Returns result dict."""
    ensure_dirs(inst_dir)
    html, err = fetch_url(tender_url)
    if err:
        return {"status": "error", "error": err, "tender_count": 0, "doc_count": 0}

    items, emails = extract_tender_items(html, tender_url)
    parser = LinkExtractor(tender_url)
    try:
        parser.feed(html)
        emails = list(parser.emails)
        text_combined = " ".join(parser.text_parts)
    except Exception:
        text_combined = html
    has_tenders = has_tender_content(html, text_combined)
    tender_items = items if (items and has_tenders) else []

    doc_count = 0
    if tender_items:
        for i, item in enumerate(tender_items[:10]):
            tender_id = f"{slug.upper().replace('-', '')[:8]}-2026-{i+1:03d}"
            tender_json = {
                "tender_id": tender_id,
                "institution": slug,
                "title": item.get("title", "Tender"),
                "description": "",
                "published_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "closing_date": "",
                "source_url": item.get("source_url", tender_url),
                "documents": [],
                "contact": {"email": emails[0] if emails else ""},
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
            tender_path.write_text(json.dumps(tender_json, indent=2), encoding="utf-8")

            download_dir = inst_dir / "downloads" / tender_id
            for doc_url in item.get("document_links", [])[:5]:
                fname = Path(urlparse(doc_url).path).name or "document.pdf"
                dest = download_dir / "original" / fname
                if download_document(doc_url, dest):
                    doc_count += 1
                    extract_text_from_doc(dest, download_dir / "extracted")

        return {"status": "success", "tender_count": len(tender_items), "doc_count": doc_count}
    else:
        return {
            "status": "no_tenders",
            "tender_count": 0,
            "doc_count": 0,
            "emails": emails,
            "has_tender_keywords": has_tenders,
        }


def append_lead(slug: str, name: str, url: str, emails: list, opportunity_type: str, desc: str):
    """Append a lead to opportunities/leads.json (only if not already present)."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path, encoding="utf-8") as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    if slug in existing_slugs:
        return

    draft_subject = f"Partnership Opportunity – ZIMA Solutions & {name}"
    draft_body = f"""Dear {name} Team,

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
        "website_url": url,
        "emails": emails[:5],
        "opportunity_type": opportunity_type,
        "opportunity_description": desc,
        "draft_email_subject": draft_subject,
        "draft_email_body": draft_body,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }
    leads.append(lead)
    with open(leads_path, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def get_emails_from_readme(inst_dir: Path) -> list[str]:
    """Extract emails from README if page had none."""
    readme = inst_dir / "README.md"
    if not readme.exists():
        return []
    text = readme.read_text(encoding="utf-8")
    emails = []
    for m in EMAIL_RE.finditer(text):
        e = m.group(0).lower()
        if "@" in e and ".png" not in e and "example@" not in e:
            emails.append(e)
    return list(dict.fromkeys(emails))[:5]


def main():
    for slug, url, name in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        try:
            result = scrape_institution(slug, name, url, inst_dir)
        except Exception as e:
            result = {"status": "error", "error": str(e), "tender_count": 0, "doc_count": 0}

        if result.get("status") == "no_tenders":
            emails = result.get("emails", [])
            if not emails:
                emails = get_emails_from_readme(inst_dir)
            append_lead(
                slug, name, url,
                emails,
                "sell",
                f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            )

        status = result.get("status", "error")
        if status == "no_tenders":
            status = "opportunity"
        tender_count = result.get("tender_count", 0)
        doc_count = result.get("doc_count", 0)

        last = {
            "institution": slug,
            "last_scrape": datetime.now(timezone.utc).isoformat(),
            "run_id": RUN_ID,
            "active_tenders_count": tender_count,
            "documents_downloaded": doc_count,
            "status": "success" if status in ("success", "opportunity") else "error",
            "error": result.get("error"),
        }
        (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")

        log_path = inst_dir / "scrape_log.json"
        log = {"runs": []}
        if log_path.exists():
            log = json.loads(log_path.read_text(encoding="utf-8"))
        log["runs"].append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success" if status in ("success", "opportunity") else "error",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "error": result.get("error"),
        })
        log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        time.sleep(2)

    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
