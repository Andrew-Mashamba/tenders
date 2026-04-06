#!/usr/bin/env python3
"""Scrape 25 institutions (batch 104) for tenders. Process opportunities if none found."""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch104"

# Tender keywords (Swahili/English)
TENDER_KEYWORDS = re.compile(
    r"\b(tender|zabuni|procurement|manunuzi|rfp|rfi|eoi|expression\s+of\s+interest|"
    r"request\s+for\s+proposal|request\s+for\s+quotation|rfq|bid|bidding|"
    r"invitation\s+to\s+tender|itt|supply\s+of\s+goods|contract\s+notice|tangazo)\b",
    re.I,
)

# Email pattern
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

# Document extensions
DOC_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")

# slug, name, tender_url (from README or websites.md)
INSTITUTIONS = [
    ("sgc", "SGC Limited", "https://sgc.co.tz/"),
    ("sgi", "SGI Group", "https://sgi.co.tz/"),
    ("shagayu", "Shagayu Company Limited", "https://shagayu.co.tz/"),
    ("shah", "Shah Industries", "https://shah.co.tz/"),
    ("shah-tours", "Shah Tours", "https://shahtours.co.tz/"),
    ("shahtours", "Shah Tours", "https://shahtours.co.tz/"),
    ("shalomcarrental", "Shalom Car Hire", "https://shalomcarrental.co.tz/"),
    ("shambaaecotours", "Shambaa Eco Tours", "https://shambaaecotours.co.tz/"),
    ("shanangagroup", "Shananga Group Limited", "https://shanangagroup.co.tz/"),
    ("sharcoctech", "Sharcoctech Solutions & Consultants", "https://sharcoctech.co.tz/"),
    ("shawsafaris", "Shaw Safaris", "https://shawsafaris.co.tz/"),
    ("shcohas", "SHCOHAS - Southern Highlands College", "https://shcohas.ac.tz/"),
    ("sheqconsult", "SHEQ Consult Tanzania", "https://sheqconsult.co.tz/"),
    ("sheria", "MoCLA - Wizara ya Katiba na Sheria", "https://sheria.go.tz/"),
    ("sheriakiganjani", "Sheria Kiganjani", "https://sheriakiganjani.or.tz/"),
    ("shiftcargo", "Shift Cargo", "https://shiftcargo.co.tz/"),
    ("shima", "Prisons Corporation Sole (PCS)", "https://shima.go.tz/"),
    ("shimautita", "SHIMUTA - Shirika la Maendeleo Utafiti na Tiba", "https://shimautita.or.tz/"),
    ("shinar", "Shinar Limited", "https://shinar.co.tz/"),
    ("shipco", "SHIPCO", "https://eprocurement.zppda.go.tz/"),
    ("shipo", "SHIPO", "https://shipo.or.tz/"),
    ("shivgroup", "Shiv International Ltd", "https://shivgroup.co.tz/"),
    ("shivyawata", "SHIVYAWATA - Tanzania Federation of OPDs", "https://shivyawata.or.tz/"),
    ("shm", "Hindu Mandal Dar es Salaam", "https://shm.or.tz/"),
    ("shoponline", "SL Shop", "https://shoponline.co.tz/"),
]


def fetch_url(url: str) -> tuple[str | None, str | None]:
    """Fetch URL with curl. Returns (html, error)."""
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "-m", "45", "-A", "Mozilla/5.0 (compatible; TenderBot/1.0)", url],
            capture_output=True,
            timeout=50,
        )
        if r.returncode != 0:
            return None, f"curl exit {r.returncode}"
        return r.stdout.decode("utf-8", errors="replace"), None
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


def extract_emails(html: str, base_url: str) -> list[str]:
    """Extract emails from HTML."""
    seen = set()
    emails = []
    for m in EMAIL_PATTERN.finditer(html):
        e = m.group(0).lower()
        if e in seen:
            continue
        if any(x in e for x in [".png", ".gif", ".jpg", ".jpeg", ".webp", "example.com", "wixpress.com"]):
            continue
        if "@" in e and "." in e.split("@")[1]:
            seen.add(e)
            emails.append(e)
    return emails


def has_tender_content(html: str) -> bool:
    """Check if page has tender/procurement keywords."""
    if not html or len(html) < 100:
        return False
    text = re.sub(r"<[^>]+>", " ", html).lower()
    return bool(TENDER_KEYWORDS.search(text))


def find_document_links(html: str, base_url: str) -> list[str]:
    """Find links to PDFs, DOCs, etc. in HTML."""
    links = []
    for ext in DOC_EXTENSIONS:
        pat = re.compile(rf'href\s*=\s*["\']([^"\']*{re.escape(ext)}[^"\']*)["\']', re.I)
        for m in pat.finditer(html):
            href = m.group(1).strip()
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                parsed = urlparse(base_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            elif not href.startswith("http"):
                href = urljoin(base_url, href)
            if href not in links:
                links.append(href)
    return links


def parse_tender_items(html: str, base_url: str) -> list[dict]:
    """Try to extract tender-like items from HTML."""
    items = []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        doc_links = find_document_links(html, base_url)
        for select in ["article", ".tender-item", ".card", "tr", "li", ".publication", ".announcement"]:
            for el in soup.select(select):
                text = el.get_text(separator=" ", strip=True)
                if not text or len(text) < 20:
                    continue
                if TENDER_KEYWORDS.search(text) or doc_links:
                    title = ""
                    for h in el.select("h1, h2, h3, h4, .tender-title, a"):
                        t = h.get_text(strip=True)
                        if t and len(t) > 5:
                            title = t
                            break
                    if not title:
                        title = text[:200] + "..." if len(text) > 200 else text
                    item_docs = []
                    for a in el.find_all("a", href=True):
                        h = a.get("href", "")
                        if any(h.lower().endswith(ext) for ext in DOC_EXTENSIONS):
                            full = urljoin(base_url, h)
                            item_docs.append(full)
                    if not item_docs and doc_links:
                        item_docs = doc_links[:5]
                    items.append({
                        "title": title,
                        "description": text[:500],
                        "document_links": item_docs,
                    })
                    break
            if items:
                break
        if not items and doc_links:
            items.append({
                "title": "Publications / Documents",
                "description": "Government or institutional documents",
                "document_links": doc_links[:10],
            })
    except ImportError:
        pass
    return items


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def save_tender(inst_dir: Path, slug: str, seq: int, item: dict, url: str) -> tuple[str, int]:
    """Save tender JSON and download documents. Returns (tender_id, doc_count)."""
    year = datetime.now().year
    slug_clean = slug.upper().replace("-", "")[:12]
    tender_id = f"{slug_clean}-{year}-{seq:03d}"
    tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
    doc_links = item.get("document_links", [])
    doc_count = 0

    tender_data = {
        "tender_id": tender_id,
        "institution_slug": slug,
        "title": item.get("title", "Untitled"),
        "source_url": url,
        "document_links": doc_links,
        "published_date": item.get("published_date"),
        "closing_date": item.get("closing_date"),
        "contact_info": item.get("contact_info", {}),
        "scraped_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    download_dir = inst_dir / "downloads" / tender_id / "original"
    extract_dir = inst_dir / "downloads" / tender_id / "extracted"
    download_dir.mkdir(parents=True, exist_ok=True)
    extract_dir.mkdir(parents=True, exist_ok=True)

    for i, doc_url in enumerate(doc_links[:10]):
        try:
            ext = Path(urlparse(doc_url).path).suffix or ".pdf"
            fname = f"doc_{i+1}{ext}"
            out_path = download_dir / fname
            subprocess.run(
                ["curl", "-sS", "-L", "-m", "60", "-o", str(out_path), doc_url],
                capture_output=True,
                timeout=65,
            )
            if out_path.exists() and out_path.stat().st_size > 0:
                doc_count += 1
        except Exception:
            pass

    tender_path.write_text(json.dumps(tender_data, indent=2), encoding="utf-8")
    return tender_id, doc_count


def append_lead(slug: str, name: str, url: str, emails: list[str], opp_type: str, desc: str):
    """Append lead to leads.json (skip if slug already exists)."""
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    if any(l.get("institution_slug") == slug for l in leads):
        return

    valid_emails = [e for e in emails if "@" in e and "." in e.split("@")[1] and "png" not in e.lower() and "gif" not in e.lower()]
    if not valid_emails:
        netloc = urlparse(url).netloc.replace("www.", "") if url else ""
        valid_emails = [f"info@{netloc}"] if netloc else []

    lead = {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": valid_emails[:5],
        "opportunity_type": opp_type,
        "opportunity_description": desc,
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
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "pending",
    }
    leads.append(lead)
    with open(leads_path, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def main():
    results = []
    for slug, name, url in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        ensure_dirs(inst_dir)
        status = "ok"
        tender_count = 0
        doc_count = 0
        err_msg = None

        try:
            html, err = fetch_url(url)
            if err:
                status = "error"
                err_msg = err
                results.append((slug, status, 0, 0))
                print(f"RESULT|{slug}|error|0|0  # {err}")
                last_scrape = {
                    "run_id": RUN_ID,
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "status": "error",
                    "tender_count": 0,
                    "doc_count": 0,
                    "error": err_msg,
                }
                (inst_dir / "last_scrape.json").write_text(
                    json.dumps(last_scrape, indent=2), encoding="utf-8"
                )
                scrape_log_path = inst_dir / "scrape_log.json"
                log_entries = []
                if scrape_log_path.exists():
                    try:
                        log_entries = json.loads(scrape_log_path.read_text(encoding="utf-8"))
                        if not isinstance(log_entries, list):
                            log_entries = []
                    except Exception:
                        log_entries = []
                log_entries.append(last_scrape)
                scrape_log_path.write_text(
                    json.dumps(log_entries[-50:], indent=2), encoding="utf-8"
                )
                continue

            if not html or len(html) < 200:
                status = "error"
                err_msg = "empty or too short response"
                results.append((slug, status, 0, 0))
                print(f"RESULT|{slug}|error|0|0  # empty response")
                continue

            items = parse_tender_items(html, url)
            if items:
                for i, item in enumerate(items[:5]):
                    tid, dc = save_tender(inst_dir, slug, i + 1, item, url)
                    tender_count += 1
                    doc_count += dc
                status = "tenders"
            else:
                status = "no_tenders"

            if status == "no_tenders":
                emails = extract_emails(html, url)
                opp_type = "sell"
                desc = f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services."
                append_lead(slug, name, url, emails, opp_type, desc)

            last_scrape = {
                "run_id": RUN_ID,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "status": status,
                "tender_count": tender_count,
                "doc_count": doc_count,
                "error": err_msg,
            }
            (inst_dir / "last_scrape.json").write_text(
                json.dumps(last_scrape, indent=2), encoding="utf-8"
            )

            scrape_log_path = inst_dir / "scrape_log.json"
            log_entries = []
            if scrape_log_path.exists():
                try:
                    log_entries = json.loads(scrape_log_path.read_text(encoding="utf-8"))
                    if not isinstance(log_entries, list):
                        log_entries = []
                except Exception:
                    log_entries = []
            log_entries.append(last_scrape)
            scrape_log_path.write_text(
                json.dumps(log_entries[-50:], indent=2), encoding="utf-8"
            )

            results.append((slug, status, tender_count, doc_count))
            print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        except Exception as e:
            status = "error"
            results.append((slug, status, 0, 0))
            print(f"RESULT|{slug}|error|0|0  # {e}")
            last_scrape = {
                "run_id": RUN_ID,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "status": "error",
                "tender_count": 0,
                "doc_count": 0,
                "error": str(e),
            }
            (inst_dir / "last_scrape.json").write_text(
                json.dumps(last_scrape, indent=2), encoding="utf-8"
            )

    subprocess.run(
        [sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        capture_output=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
