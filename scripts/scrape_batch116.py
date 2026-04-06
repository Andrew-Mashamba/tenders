#!/usr/bin/env python3
"""Scrape batch 116: tbs, tcaa, tcb, tcb-bank, tcbcedu, tccia, tcciainvest, tccs, tcd, tcdc, tcfpa, tcindustries, tcra-ccc, tcrasaccos, tcrs, tcu, tdb, tdya, tea-association, teaboard, teachersjunction, tec, tecden, techcom, techhub."""
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
sys.path.insert(0, str(PROJECT))
RUN_ID = sys.argv[1] if len(sys.argv) > 1 else "run_20260313_205329_batch116"

# Tender/procurement keywords to detect
TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|procurement|rfp|rfi|rfq|zabuni|bid\s+document|invitation\s+to\s+bid|request\s+for\s+proposal|manunuzi)\b",
    re.I,
)

# Document extensions
DOC_EXTS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")

# Email regex
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


class LinkExtractor(HTMLParser):
    """Extract links and document URLs from HTML."""

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
            if "example" not in e and "domain" not in e and "sentry" not in e:
                self.emails.add(e)


def fetch_url(url: str, timeout: int = 30) -> tuple[str | None, str | None]:
    """Fetch URL and return (html, error)."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)


def has_tender_content(html: str, text: str) -> bool:
    """Check if page contains tender/procurement content."""
    combined = (html + " " + text).lower()
    return bool(TENDER_KEYWORDS.search(combined))


def extract_tender_items(html: str, base_url: str) -> tuple[list[dict], list[str]]:
    """Parse HTML for tender-like items (title, date, doc links). Returns (items, emails)."""
    parser = LinkExtractor(base_url)
    try:
        parser.feed(html)
    except Exception:
        pass
    items = []
    # Heuristic: look for document links as tender attachments
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
    """Download a document to dest. Returns True if successful."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.read())
            return True
    except Exception:
        return False


def extract_text_from_doc(file_path: Path, extracted_dir: Path) -> bool:
    """Extract text from PDF/DOCX/XLSX to extracted/."""
    try:
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            from tools.pdf.reader import extract_text
            text = extract_text(str(file_path))
        elif ext == ".docx":
            from tools.docx.reader import extract_text
            text = extract_text(str(file_path))
        elif ext == ".xlsx":
            from tools.xlsx.reader import extract_data
            data = extract_data(str(file_path))
            text = json.dumps(data, indent=2) if data else ""
        else:
            return False
        out = extracted_dir / f"{file_path.stem}.txt"
        out.write_text(text, encoding="utf-8")
        return True
    except Exception:
        return False


def scrape_institution(slug: str, name: str, tender_url: str, inst_dir: Path) -> dict:
    """Scrape one institution. Returns result dict."""
    ensure_dirs(inst_dir)
    html, err = fetch_url(tender_url)
    if err:
        return {
            "status": "error",
            "error": err,
            "tender_count": 0,
            "doc_count": 0,
        }

    items, emails = extract_tender_items(html, tender_url)
    parser = LinkExtractor(tender_url)
    try:
        parser.feed(html)
        emails = list(parser.emails)
        text_combined = " ".join(parser.text_parts)
    except Exception:
        text_combined = html
    has_tenders = has_tender_content(html, text_combined)

    # Tender items: only when we have doc links on a tender-related page
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
                "document_links": item.get("document_links", []),
                "contact_info": {"email": emails[0] if emails else ""},
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
                    ext_dir = download_dir / "extracted"
                    extract_text_from_doc(dest, ext_dir)

        return {
            "status": "success",
            "tender_count": len(tender_items),
            "doc_count": doc_count,
        }
    else:
        return {
            "status": "no_tenders",
            "tender_count": 0,
            "doc_count": 0,
            "emails": emails,
            "has_tender_keywords": has_tenders,
        }


def append_lead(slug: str, name: str, url: str, emails: list, opportunity_type: str, desc: str):
    """Append a lead to opportunities/leads.json."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])

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


INSTITUTIONS = [
    ("tbs", "Tanzania Bureau of Standards", "https://tbs.go.tz/announcements/taarifa-kwa-umma-kuhusu-usajili-na-ukaguzi-wa-maeneo-ya-biashara-ya-bidhaa-za-chakula-na-vipodozi"),
    ("tcaa", "Tanzania Civil Aviation Authority", "https://tcaa.go.tz/"),
    ("tcb", "Bodi ya Pamba Tanzania", "https://tcb.go.tz/"),
    ("tcb-bank", "Tanzania Commercial Bank (TCB)", "https://www.tcbbank.co.tz/tenders/en"),
    ("tcbcedu", "Tanga Christian Bible College", "https://web.facebook.com/permalink.php?story_fbid=2291954577602079&id=743501032447449&__tn__=-R"),
    ("tccia", "TCCIA", "https://www.tccia.co.tz/"),
    ("tcciainvest", "Afriprise", "https://afriprise.co.tz/"),
    ("tccs", "Tanzania Commercial Cattle Society", "https://tccs.or.tz/"),
    ("tcd", "Tanzania Centre for Democracy", "https://tcd.or.tz/"),
    ("tcdc", "Tanzania Cooperative Development Commission", "https://www.ushirika.go.tz/administration/procurement-management-unit"),
    ("tcfpa", "TCFPA", "https://tcfpa.co.tz/"),
    ("tcindustries", "TC Industries Limited", "https://www.tcindustries.co.tz/"),
    ("tcra-ccc", "TCRA-CCC", "https://tcra-ccc.go.tz/"),
    ("tcrasaccos", "TCRA SACCOS", "https://tcrasaccos.or.tz/"),
    ("tcrs", "Tanganyika Christian Refugee Service", "https://tcrs.or.tz/"),
    ("tcu", "Tanzania Commission for Universities", "https://tcu.go.tz/"),
    ("tdb", "Tanzania Dairy Board", "https://tdb.go.tz/"),
    ("tdya", "TDYA", "https://tdya.co.tz/"),
    ("tea-association", "Tea Association", "https://tea-association.co.tz/"),
    ("teaboard", "Tea Board Tanzania", "https://teaboard.go.tz/"),
    ("teachersjunction", "Teachers Junction", "https://teachersjunction.co.tz/"),
    ("tec", "Tanzania Episcopal Conference", "https://tec.or.tz/index.php/2024/01/19/mabalozi-wa-amani-ii-phase-project-media-campaign-tender/"),
    ("tecden", "Tanzania Early Childhood Development Network", "https://www.tecden.or.tz/"),
    ("techcom", "Techchom Distribution", "https://techcom.co.tz/"),
    ("techhub", "TECH HUB LTD", "https://techhub.co.tz/"),
]


def main():
    for slug, name, url in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)

        result = scrape_institution(slug, name, url, inst_dir)

        if result.get("status") == "no_tenders":
            emails = result.get("emails", [])
            append_lead(
                slug, name, url,
                emails,
                "sell",
                "No formal tenders found on website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            )

        # Build final status
        status = result.get("status", "error")
        if status == "no_tenders":
            status = "opportunity"
        tender_count = result.get("tender_count", 0)
        doc_count = result.get("doc_count", 0)

        # Update last_scrape.json
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

        # Append to scrape_log.json
        log_path = inst_dir / "scrape_log.json"
        runs = []
        if log_path.exists():
            raw = json.loads(log_path.read_text(encoding="utf-8"))
            runs = raw.get("runs", raw) if isinstance(raw, dict) else raw
        runs.append({
            "run_id": RUN_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success" if status in ("success", "opportunity") else "error",
            "tenders_found": tender_count,
            "documents_downloaded": doc_count,
            "error": result.get("error"),
        })
        log_path.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")

        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        time.sleep(10)  # Rate limit per institution README

    # Sync leads CSV
    sync_script = PROJECT / "scripts" / "sync_leads_csv.py"
    if sync_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(sync_script)], cwd=str(PROJECT), check=False)


if __name__ == "__main__":
    main()
