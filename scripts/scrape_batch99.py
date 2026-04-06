#!/usr/bin/env python3
"""
Scrape batch 99: 25 institutions (rosehotel through ruwasa).
Run ID: run_20260315_060430_batch99
"""
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch99"

# slug, name, tender_url, emails from README
INSTITUTIONS = [
    ("rosehotel", "UrbanRose Hotel & Apartments", "https://rosehotel.co.tz/", ["info@rosehotel.co.tz", "gm@rosehotel.co.tz"]),
    ("rotech", "Rotech Bar Management POS & Security", "https://www.rotech.co.tz/", ["info@rotech.co.tz"]),
    ("royal", "ROYAL LOGISTICS", "https://royal.co.tz/", []),
    ("royalfamilyschools", "Royal Family School", "https://royalfamilyschools.ac.tz/", ["info@royalfamilyschools.ac.tz"]),
    ("royalfreight", "Royal Freight Ltd", "https://royalfreight.co.tz/", ["royalfreight@royalfreight.co.tz"]),
    ("royalfurnishers", "Royal Furnishers", "https://royalfurnisherstz.com/", ["info@royalfurnishers.co.tz", "info@rfl.co.tz"]),
    ("royaloven", "Royal Oven", "https://royaloven.co.tz/", ["info@royaloven.co.tz"]),
    ("royalstarshipping", "Royal Star Shipping Company", "https://royalstarshipping.co.tz/", ["warehouse@transcargo.com", "dsm@royalstarshipping.co.tz", "info@royalstarshipping.co.tz"]),
    ("roysafaris", "Roy Safaris", "https://roysafaris.co.tz/", ["enquiries@roysafaris.co.tz"]),
    ("rrbs", "RNR Business Solutions", "https://rrbs.co.tz/", ["info@rrbs.co.tz"]),
    ("rsgattorneys", "RSG Attorneys", "https://rsgattorneys.co.tz/", []),
    ("rskgroup", "RSK Tanzania", "https://rskgroup.co.tz/", []),
    ("rtexpress", "RT EXPRESS", "https://rtexpress.co.tz/", ["info@rtexpress.co.tz", "info@rtepress.co.tz"]),
    ("rthosting", "Supersite / RT Hosting", "https://rthosting.co.tz/", []),
    ("ruahacdti", "Ruaha Community Development Training Institute", "https://ruahacdti.ac.tz/", ["pruaha@jamii.go.tz"]),
    ("ruangwadc", "Ruangwa District Council", "https://ruangwadc.go.tz/tenders", ["ded@ruangwadc.go.tz"]),  # tender_url was YouTube, use /tenders
    ("rubberstamp", "Tanzania Rubber Stamp", "https://www.rubberstamp.co.tz/", ["cjmodessa@rubberstamp.co.tz", "sales@rubberstamp.co.tz"]),
    ("rudi", "RUDI", "https://rudi.or.tz/", ["Info@rudi.or.tz"]),
    ("rudys", "The Grand Grill & Bar", "https://rudys.co.tz/", ["info@grandgrillbar.com"]),
    ("rukacreatives", "Ruka Creatives Limited", "https://rukacreatives.co.tz/", ["info@rukacreatives.or.tz"]),
    ("ruksa", "Ruksa", "https://www.ruksa.co.tz/", ["sales@ruksa.co.tz", "info@ruksa.co.tz"]),
    ("runerconsult", "Rural Natures Environmental Resources Ltd", "https://www.runerconsult.co.tz/", ["info@runerconsult.co.tz"]),
    ("rungwedc", "Rungwe District Council", "https://rungwedc.go.tz/announcement/mwaliko-wa-zabuni-ujenzi-na-uendeshaji-maduka-kiwira", ["ded@rungwedc.go.tz"]),
    ("rungwehotel", "Rungwe Hotels", "https://rungwehotel.co.tz/", ["info@rungwehotel.co.tz"]),
    ("ruwasa", "RUWASA", "https://ruwasa.go.tz/", ["dg@ruwasa.go.tz"]),
]

TENDER_KEYWORDS = re.compile(
    r"\b(tender|procurement|zabuni|rfp|rfq|rfi|eoi|bid|quotation|supply|invitation|manunuzi)\b",
    re.I
)
DOC_EXT = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def fetch_url(url: str, timeout: int = 20) -> tuple[str | None, str | None]:
    """Fetch URL, return (html, error)."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        with urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except (URLError, HTTPError, OSError) as e:
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
            "//*[contains(@class,'page-content')] | //*[contains(@class,'announcement')] | "
            "//li | //tr | //*[contains(@class,'zabuni')]"
        )

        seen_titles = set()
        for elem in containers:
            text = (elem.text_content() or "").strip()
            if len(text) < 25:
                continue
            if not TENDER_KEYWORDS.search(text):
                continue
            # Skip menu/footer noise
            if "pork tenderloin" in text.lower() or "tender steak" in text.lower():
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
                "document_links": elem_docs or [d["url"] for d in doc_links if d["url"] not in elem_docs][:10],
                "contact_info": {"email": emails[0]} if emails else {},
                "source_url": base_url,
            })
            if len(tenders) >= 25:
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
                "contact_info": {},
                "source_url": base_url,
            })
    except Exception:
        pass
    return tenders


def download_file(url: str, dest: Path) -> bool:
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        with urlopen(req, timeout=45) as r:
            data = r.read()
            if len(data) > 50_000_000:
                return False
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return True
    except Exception:
        return False


def extract_text_pdf(pdf_path: Path) -> bool:
    txt_path = pdf_path.parent.parent / "extracted" / (pdf_path.stem + ".txt")
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ["python3", "-m", "tools", "pdf", "read", str(pdf_path)],
            cwd=PROJECT, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout:
            txt_path.write_text(result.stdout, encoding="utf-8")
            return True
    except Exception:
        pass
    return False


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def get_tender_ids(slug: str, count: int) -> list[str]:
    slug_upper = slug.upper().replace("-", "")
    year = datetime.now(timezone.utc).strftime("%Y")
    active_dir = PROJECT / "institutions" / slug / "tenders" / "active"
    existing = list(active_dir.glob("*.json")) if active_dir.exists() else []
    base_seq = len(existing)
    return [f"{slug_upper}-{year}-{base_seq + i + 1:03d}" for i in range(count)]


def create_lead(slug: str, name: str, url: str, emails: list) -> dict:
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": [e for e in emails if "@" in e and "." in e.split("@")[-1]],
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
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
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }


def append_leads(new_leads: list):
    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        data = json.loads(leads_path.read_text(encoding="utf-8"))
        leads = data if isinstance(data, list) else data.get("leads", [])
    leads.extend(new_leads)
    leads_path.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")


def update_scrape_state(inst_dir: Path, status: str, tender_count: int, doc_count: int, error: str = None):
    now = datetime.now(timezone.utc).isoformat()
    last = {
        "run_id": RUN_ID,
        "scraped_at": now,
        "status": status,
        "tender_count": tender_count,
        "doc_count": doc_count,
        "error": error,
    }
    (inst_dir / "last_scrape.json").write_text(json.dumps(last, indent=2), encoding="utf-8")
    log_path = inst_dir / "scrape_log.json"
    log_entries = []
    if log_path.exists():
        log_entries = json.loads(log_path.read_text(encoding="utf-8"))
    log_entries.append({"run_id": RUN_ID, "scraped_at": now, "status": status, "tender_count": tender_count, "doc_count": doc_count})
    log_path.write_text(json.dumps(log_entries[-100:], indent=2), encoding="utf-8")


def scrape_institution(slug: str, name: str, url: str, known_emails: list, leads_out: list) -> tuple[str, int, int]:
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    html, err = fetch_url(url)
    if err:
        update_scrape_state(inst_dir, "error", 0, 0, err)
        return "error", 0, 0

    # Scrape emails from page
    page_emails = list(set(EMAIL_PATTERN.findall(html or "")))
    all_emails = list(dict.fromkeys(known_emails + [e for e in page_emails if not any(x in e for x in [".png", "example.com", "wix.com"])]))[:10]

    tenders = parse_tenders(html, url, slug)

    if not tenders:
        lead = create_lead(slug, name, url, all_emails)
        leads_out.append(lead)
        update_scrape_state(inst_dir, "no_tenders", 0, 0)
        return "no_tenders", 0, 0

    ids = get_tender_ids(slug, len(tenders))
    doc_count = 0
    for i, t in enumerate(tenders):
        tid = ids[i]
        tender_json = {
            "tender_id": tid,
            "institution_slug": slug,
            "title": t.get("title", ""),
            "description": t.get("description", ""),
            "published_date": t.get("published_date"),
            "closing_date": t.get("closing_date"),
            "category": "procurement",
            "document_links": t.get("document_links", []),
            "contact_info": t.get("contact_info", {}),
            "source_url": t.get("source_url", url),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }
        (inst_dir / "tenders" / "active" / f"{tid}.json").write_text(
            json.dumps(tender_json, indent=2), encoding="utf-8"
        )
        download_dir = inst_dir / "downloads" / tid / "original"
        download_dir.mkdir(parents=True, exist_ok=True)
        for doc_url in t.get("document_links", [])[:10]:
            fname = Path(doc_url.split("?")[0]).name or "document.pdf"
            dest = download_dir / fname
            if not dest.exists() and download_file(doc_url, dest):
                doc_count += 1
                if dest.suffix.lower() == ".pdf":
                    extract_text_pdf(dest)

    update_scrape_state(inst_dir, "tenders_found", len(tenders), doc_count)
    return "tenders_found", len(tenders), doc_count


def main():
    results = []
    leads_to_add = []

    for slug, name, url, emails in INSTITUTIONS:
        try:
            status, tc, dc = scrape_institution(slug, name, url, emails, leads_to_add)
            results.append(f"RESULT|{slug}|{status}|{tc}|{dc}")
            print(results[-1])
        except Exception as e:
            inst_dir = PROJECT / "institutions" / slug
            ensure_dirs(inst_dir)
            update_scrape_state(inst_dir, "error", 0, 0, str(e))
            results.append(f"RESULT|{slug}|error|0|0")
            print(results[-1])

        # Rate limit
        import time
        time.sleep(2)

    # Dedupe and append new leads
    if leads_to_add:
        leads_path = PROJECT / "opportunities" / "leads.json"
        existing_slugs = set()
        if leads_path.exists():
            data = json.loads(leads_path.read_text(encoding="utf-8"))
            existing = data if isinstance(data, list) else data.get("leads", [])
            existing_slugs = {l.get("institution_slug") for l in existing if l.get("institution_slug")}
        new_leads = [l for l in leads_to_add if l.get("institution_slug") not in existing_slugs]
        if new_leads:
            append_leads(new_leads)
            subprocess.run(["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], cwd=PROJECT, check=True)

    print("\n--- BATCH 99 COMPLETE ---")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
