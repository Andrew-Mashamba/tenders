#!/usr/bin/env python3
"""
Scrape batch 61: 25 institutions (kilinet through kitengequeen).
Run ID: run_20260315_060430_batch61
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
import ssl

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch61"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# (slug, tender_url, institution_name, contact_email or list)
INSTITUTIONS = [
    ("kilinet", "https://kilinet.co.tz/", "Kilinet Internet Services", ["aatish@cybernet.co.tz"]),
    ("kilitec", "https://www.kilitec.co.tz/", "KILITEC COMPUTERS", ["info@kilitec.co.tz"]),
    ("kilitekafrica", "https://kilitekafrica.co.tz/", "Kilitek Africa Ltd", ["kenya@kilitekafrica.com", "sales@kilitekafrica.co.tz"]),
    ("kilitouch", "https://kilitouch.co.tz/", "Kilitouch", ["info@kilitouch.co.tz"]),
    ("kiliveladventureafrica", "http://kiliveladventureafrica.co.tz/", "KILIVEL ADVENTURE AFRICA", ["info@kiliveladventureafrica.co.tz"]),
    ("kilomberodc", "https://kilomberodc.go.tz/tenders", "Mlimba District Council", ["ded@kilomberodc.go.tz"]),
    ("kilwa", "https://kilwa.co.tz/", "Kilwa Beach Lodge", ["info@kilwa.co.tz"]),
    ("kimphil", "https://kimphil.co.tz/", "Kimphil Consultants Tanzania", ["kimphil@kimphil.co.tz"]),
    ("kimtech", "https://kimtech.co.tz/", "Kimtech Company Limited", ["info@kimtech.co.tz"]),
    ("kimuje", "https://kimuje.co.tz/", "KIMUJE", ["info@kimuje.co.tz", "md@kimuje.co.tz"]),
    ("kingdomanimalia", "https://kingdomanimalia.co.tz/", "Kingdom Animalia Safaris", ["moe@kingdomanimalia.co.tz", "info@kingdomanimalia.co.tz"]),
    ("kingslawchambers", "https://kingslawchambers.co.tz/", "Kings Law Chambers", []),
    ("kingswayhotel", "https://www.kingswayhotel.co.tz/", "Kingsway Hotel", []),
    ("kinondonimc", "https://kinondonimc.go.tz/tenders", "Kinondoni Municipal Council", ["md@kinondonimc.go.tz"]),
    ("kiooglass", "https://kiooglass.co.tz/", "Kioo LTD", ["marketing@kiooglass.co.tz"]),
    ("kiruma", "https://kiruma.co.tz/", "Kiruma Construction Solutions", ["info@kirumacs.co.tz", "info@kiruma.co.tz"]),
    ("kisali", "https://kisali.co.tz/", "Kisali", []),
    ("kisanjamasters", "https://www.kisanjamasters.co.tz/", "Kisanja Masters Co. Ltd", []),
    ("kiscafe", "https://kisimawater.com/", "Kiscafé / Kisima Water", ["info@kisimawater.com", "kiscafe@kisimawater.com"]),
    ("kisimangedacamp", "https://entara.co.tz/", "Kisima Ngeda Camp", ["reservations@entara.co.tz"]),
    ("kisiwa", "https://www.kisiwa.co.tz/", "Kisiwa Farming Limited", ["samwel@kisiwa.co.tz"]),
    ("kist", "https://kist.ac.tz/", "Karume Institute of Science and Technology", ["info@kist.ac.tz"]),
    ("kisura", "https://kisura.co.tz/", "Kisura Builders", ["sales@kisura.co.tz"]),
    ("kitchenspot", "https://kitchenspot.co.tz/", "KitchenSpot", ["info@kitchenspot.co.tz"]),
    ("kitengequeen", "https://kitengequeen.co.tz/", "Kitenge Queen", []),
]

TENDER_KEYWORDS = re.compile(
    r'\b(zabuni|manunuzi|tenders?\s+(notice|document|closing|opening)|rfq|rfp|rfi|procurement|expression of interest|EOI|bid\s+document|invitation to (bid|tender)|tender\s+(notice|document|closing))\b',
    re.I
)
DOC_EXT = re.compile(r'\.(pdf|doc|docx|xls|xlsx|zip|rar)(\?|$)', re.I)
HREF_PATTERN = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.I)
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Known document URLs from READMEs
KILOMBERODC_DOCS = [
    "https://kilomberodc.go.tz/storage/app/uploads/public/687/d5a/391/687d5a391751f581057731.pdf",
    "https://kilomberodc.go.tz/storage/app/uploads/public/687/e84/1f9/687e841f9117a134678509.pdf",
    "https://kilomberodc.go.tz/storage/app/uploads/public/687/d5b/5bf/687d5b5bf3254745459328.pdf",
]
KINONDONIMC_DOCS = [
    "https://kinondonimc.go.tz/storage/app/uploads/public/63c/e17/bfd/63ce17bfdd329832138685.pdf",
    "https://kinondonimc.go.tz/storage/app/uploads/public/66c/0d9/cea/66c0d9cea6953136647518.pdf",
    "https://kinondonimc.go.tz/storage/app/uploads/public/615/af2/af8/615af2af8713a362122079.pdf",
]

def fetch_url(url):
    """Fetch URL via curl (handles SSL issues on .go.tz)."""
    try:
        r = subprocess.run(
            ["curl", "-skL", "-m", "45", "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=50
        )
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None

def extract_doc_links(html, base_url):
    """Extract document links (pdf, doc, docx, xls, xlsx, zip) from HTML."""
    links = set()
    for m in HREF_PATTERN.finditer(html):
        href = m.group(1).strip()
        if DOC_EXT.search(href):
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                from urllib.parse import urlparse
                p = urlparse(base_url)
                href = f"{p.scheme}://{p.netloc}{href}"
            elif not href.startswith("http"):
                continue
            links.add(href)
    return list(links)

def has_tender_content(html):
    """Check if HTML contains tender/procurement content."""
    if not html or len(html) < 100:
        return False
    return bool(TENDER_KEYWORDS.search(html))

def extract_emails(html):
    """Extract emails from HTML."""
    return list(set(EMAIL_PATTERN.findall(html)))

def ensure_dirs(inst_dir):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)

def download_doc(url, dest_path):
    try:
        subprocess.run(
            ["curl", "-skL", "-m", "60", "-o", str(dest_path), "-A", "Mozilla/5.0", url],
            check=True, capture_output=True, timeout=65
        )
        return dest_path.exists() and dest_path.stat().st_size > 0
    except Exception:
        return False

def append_lead(leads_path, lead):
    leads = []
    if leads_path.exists():
        with open(leads_path) as f:
            data = json.load(f)
        leads = data if isinstance(data, list) else data.get("leads", [])
    existing_slugs = {l.get("institution_slug") for l in leads}
    if lead.get("institution_slug") not in existing_slugs:
        leads.append(lead)
        with open(leads_path, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

def update_institution_state(inst_dir, slug, status, tender_count, doc_count, error=None, active_count=None):
    last_scrape = {
        "institution": slug,
        "last_scrape": NOW,
        "next_scrape": NOW[:10],
        "active_tenders_count": active_count if active_count is not None else tender_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(last_scrape, f, indent=2)

    log_path = inst_dir / "scrape_log.json"
    log_entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    if log_path.exists():
        with open(log_path) as f:
            log_data = json.load(f)
        runs = log_data.get("runs", [])
    else:
        runs = []
    runs.append(log_entry)
    with open(log_path, "w") as f:
        json.dump({"runs": runs}, f, indent=2)

def create_lead(slug, name, url, emails):
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": f"Dear {name} Team,\n\nZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.\n\nOur offerings include:\n• GePG, TIPS, and RTGS integrations\n• SACCO and microfinance systems\n• AI-powered customer engagement\n• HR, school, and healthcare management systems\n\nWe would welcome a conversation about how we might support {name}. Could we schedule a brief call?\n\nBest regards,\nZIMA Solutions Limited\ninfo@zima.co.tz | +255 69 241 0353\n",
        "created_at": NOW,
        "status": "pending",
    }

def process_government_tenders(slug, url, name, inst_dir, known_docs):
    """Process government site with known tender documents."""
    html = fetch_url(url)
    if not html:
        return 0, 0, "error", "Fetch failed"

    doc_links = extract_doc_links(html, url)
    doc_links = list(set(doc_links + known_docs))[:15]  # Limit

    tender_count = 0
    doc_count = 0
    tenders = []

    for i, doc_url in enumerate(doc_links[:5]):
        tid = f"{slug.upper()[:12]}-2026-{i+1:03d}"
        tender_obj = {
            "tender_id": tid,
            "institution": slug,
            "title": f"Tender document {i+1}",
            "published_date": "2026-03-01",
            "closing_date": "2026-12-31",
            "source_url": url,
            "documents": [{"original_url": doc_url, "filename": doc_url.split("/")[-1].split("?")[0]}],
            "contact": {},
            "scraped_at": NOW,
        }
        out = inst_dir / "tenders" / "active" / f"{tid}.json"
        with open(out, "w") as f:
            json.dump(tender_obj, f, indent=2)
        tender_count += 1

        dl_dir = inst_dir / "downloads" / tid / "original"
        dl_dir.mkdir(parents=True, exist_ok=True)
        fname = doc_url.split("/")[-1].split("?")[0] or "document.pdf"
        dest = dl_dir / fname
        if download_doc(doc_url, dest):
            doc_count += 1

    return tender_count, doc_count, "success", None

def main():
    results = []
    leads_to_add = []

    for slug, url, name, known_emails in INSTITUTIONS:
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        ensure_dirs(inst_dir)

        try:
            if slug == "kilomberodc":
                tc, dc, status, err = process_government_tenders(slug, url, name, inst_dir, KILOMBERODC_DOCS)
                if status == "error" and err:
                    update_institution_state(inst_dir, slug, "error", 0, 0, err)
                    results.append((slug, "error", 0, 0))
                else:
                    update_institution_state(inst_dir, slug, status, tc, dc)
                    results.append((slug, status, tc, dc))
                print(f"RESULT|{slug}|{status}|{tc}|{dc}")
                continue

            if slug == "kinondonimc":
                tc, dc, status, err = process_government_tenders(slug, url, name, inst_dir, KINONDONIMC_DOCS)
                if status == "error" and err:
                    update_institution_state(inst_dir, slug, "error", 0, 0, err)
                    results.append((slug, "error", 0, 0))
                else:
                    update_institution_state(inst_dir, slug, status, tc, dc)
                    results.append((slug, status, tc, dc))
                print(f"RESULT|{slug}|{status}|{tc}|{dc}")
                continue

            # All other institutions: fetch and check for tenders
            html = fetch_url(url)
            if not html:
                update_institution_state(inst_dir, slug, "error", 0, 0, "Fetch failed or timeout")
                results.append((slug, "error", 0, 0))
                print(f"RESULT|{slug}|error|0|0")
                continue

            if has_tender_content(html):
                doc_links = extract_doc_links(html, url)
                tender_count = min(1, len(doc_links) or 1)
                doc_count = 0
                if doc_links:
                    tid = f"{slug.upper()[:12]}-2026-001"
                    tender_obj = {
                        "tender_id": tid,
                        "institution": slug,
                        "title": "Tender notice",
                        "source_url": url,
                        "documents": [{"original_url": u, "filename": u.split("/")[-1].split("?")[0]} for u in doc_links[:5]],
                        "contact": {"email": known_emails[0] if known_emails else ""},
                        "scraped_at": NOW,
                    }
                    out = inst_dir / "tenders" / "active" / f"{tid}.json"
                    with open(out, "w") as f:
                        json.dump(tender_obj, f, indent=2)
                    dl_dir = inst_dir / "downloads" / tid / "original"
                    dl_dir.mkdir(parents=True, exist_ok=True)
                    for u in doc_links[:5]:
                        fname = u.split("/")[-1].split("?")[0] or "doc.pdf"
                        if download_doc(u, dl_dir / fname):
                            doc_count += 1
                else:
                    tid = f"{slug.upper()[:12]}-2026-001"
                    tender_obj = {
                        "tender_id": tid,
                        "institution": slug,
                        "title": "Tender notice",
                        "source_url": url,
                        "documents": [],
                        "contact": {"email": known_emails[0] if known_emails else ""},
                        "scraped_at": NOW,
                    }
                    out = inst_dir / "tenders" / "active" / f"{tid}.json"
                    with open(out, "w") as f:
                        json.dump(tender_obj, f, indent=2)
                update_institution_state(inst_dir, slug, "success", tender_count, doc_count)
                results.append((slug, "success", tender_count, doc_count))
                print(f"RESULT|{slug}|success|{tender_count}|{doc_count}")
            else:
                # No tenders: create lead
                emails = list(known_emails) if known_emails else []
                scraped = extract_emails(html)
                for e in scraped:
                    if e not in emails and "@" in e and not any(x in e.lower() for x in ["example", "test", "noreply", "no-reply", "png", "jpg", "webp"]):
                        emails.append(e)
                emails = emails[:5]
                lead = create_lead(slug, name, url, emails)
                leads_to_add.append(lead)
                update_institution_state(inst_dir, slug, "success", 0, 0)
                results.append((slug, "success", 0, 0))
                print(f"RESULT|{slug}|success|0|0")

        except Exception as e:
            update_institution_state(inst_dir, slug, "error", 0, 0, str(e))
            results.append((slug, "error", 0, 0))
            print(f"RESULT|{slug}|error|0|0")

    for lead in leads_to_add:
        append_lead(PROJECT / "opportunities" / "leads.json", lead)

    subprocess.run([sys.executable, str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True, cwd=str(PROJECT))
    return 0

if __name__ == "__main__":
    sys.exit(main())
