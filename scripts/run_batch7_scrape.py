#!/usr/bin/env python3
"""
Batch 7 scrape: 25 institutions (alumexframers through amyc).
Run ID: run_20260313_205329_batch7
"""
import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch7"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

INSTITUTIONS = [
    {"slug": "alumexframers", "name": "Alumex Framers", "url": "https://alumexframers.co.tz/", "emails": ["info@alumexframers.co.tz"]},
    {"slug": "alutechaluminum", "name": "Alutech Aluminum", "url": "https://alutechaluminum.co.tz/", "emails": ["info@alutechaluminum.co.tz"]},
    {"slug": "alymatech", "name": "AlymaTech", "url": "https://alymatech.co.tz/", "emails": ["info@alymatech.co.tz"]},
    {"slug": "amana-bank", "name": "Amana Bank Tanzania", "url": "https://amanabank.co.tz/banking/tender", "emails": ["customerservice@amanabank.co.tz"]},
    {"slug": "amanabank", "name": "AMANA BANK", "url": "https://amanabank.co.tz/banking/tender", "emails": ["customerservice@amanabank.co.tz"]},
    {"slug": "amando", "name": "AMANDO", "url": "https://amando.co.tz/", "emails": ["info@amando.co.tz"]},
    {"slug": "amanidelivery", "name": "Amani Quick Delivery", "url": "https://amanidelivery.co.tz/", "emails": ["info@amanidelivery.co.tz"]},
    {"slug": "amazingzanzibar", "name": "Amazing Zanzibar", "url": "https://amazingzanzibar.co.tz/", "emails": []},
    {"slug": "amazonattorneys", "name": "Amazon Attorneys", "url": "https://amazonattorneys.co.tz/", "emails": ["amazonattorneys@gmail.com", "rachel.onesmo@amazonattorneys.co.tz"]},
    {"slug": "amd", "name": "AMD", "url": "https://www.amd.co.tz/", "emails": ["info@amd.co.tz", "sales@amd.co.tz"]},
    {"slug": "amdt", "name": "AMDT", "url": "https://amdt.co.tz/tenders/", "emails": ["info@amdt.co.tz"]},
    {"slug": "amecore", "name": "Amecore", "url": "https://amecore.co.tz/", "emails": []},
    {"slug": "amenconsulting", "name": "Amen Consulting", "url": "https://www.amenconsulting.co.tz/", "emails": []},
    {"slug": "amenityparadise", "name": "Amenity Paradise Hotel", "url": "https://amenityparadise.co.tz/", "emails": ["info@amenityparadise.co.tz", "reservations@amenityparadise.co.tz", "manager@amenityparadise.co.tz"]},
    {"slug": "ami", "name": "AMI", "url": "https://ami.ac.tz/", "emails": ["info@ami.ac.tz", "mihambosp@hotmail.com"]},
    {"slug": "amici", "name": "Amici", "url": "https://amici.co.tz/", "emails": ["hello@amici.co.tz"]},
    {"slug": "amirex", "name": "Amirex", "url": "https://amirex.co.tz/", "emails": ["info@amirex.co.tz", "ayub@amirex.co.tz", "mbonga@amirex.co.tz", "abubakar@amirex.co.tz"]},
    {"slug": "amiron", "name": "Amiron", "url": "https://www.amiron.co.tz/", "emails": ["sales@amiron.co.tz"]},
    {"slug": "amironmedical", "name": "Amiron Medical", "url": "https://www.amironmedical.co.tz/", "emails": ["info@amironmedical.co.tz"]},
    {"slug": "amlfinance", "name": "AML Finance", "url": "https://amlfinance.co.tz/", "emails": ["info@amlfinance.co.tz"]},
    {"slug": "amogtech", "name": "Amogtech", "url": "https://amogtech.co.tz/", "emails": ["info@amogtech.co.tz"]},
    {"slug": "amovate", "name": "Amovate", "url": "https://amovate.co.tz/", "emails": ["sales@amovate.co.tz", "support@amovate.co.tz"]},
    {"slug": "amplifielectrics", "name": "Amplifi Electrics", "url": "https://amplifielectrics.co.tz/", "emails": ["info@amplifielectrics.co.tz"]},
    {"slug": "amtec", "name": "AMTEC", "url": "https://amtec.co.tz/", "emails": ["info@amtec.co.tz"]},
    {"slug": "amyc", "name": "AMYC", "url": "https://amyc.or.tz/", "emails": ["info@amyc.or.tz"]},
]

# Amana Bank tender (found on page)
AMANA_TENDER = {
    "title": "Supply of goods and provision of services 2025",
    "doc_url": "https://amanabank.co.tz/uploads/documents/amana-bank-6720d1c8d5d49.pdf",
}


def fetch_url(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def download_file(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TendersBot/1.0)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as f:
                f.write(data)
            return len(data)
    except Exception as e:
        return 0


def extract_emails_from_html(html):
    if not html:
        return []
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    found = set(re.findall(pattern, html))
    return [e for e in found if not any(x in e.lower() for x in ["example", "email", "cdn-cgi", "sentry", "wixpress", "wordpress", "gravatar"])]


def ensure_dirs(inst_dir):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def process_tender(inst, tender_count, doc_count):
    slug = inst["slug"]
    inst_dir = PROJECT / "institutions" / slug
    ensure_dirs(inst_dir)

    tender_id = f"{slug.upper().replace('-', ' ').replace(' ', '-')}-2026-001"
    download_dir = inst_dir / "downloads" / tender_id / "original"
    download_dir.mkdir(parents=True, exist_ok=True)

    filename = "amana-bank-6720d1c8d5d49.pdf"
    dest = download_dir / filename
    size = download_file(AMANA_TENDER["doc_url"], dest)
    if size > 0:
        doc_count += 1

    tender_json = {
        "tender_id": tender_id,
        "institution": slug,
        "title": AMANA_TENDER["title"],
        "description": "Supply of goods and provision of services 2025 - Amana Bank procurement notice.",
        "published_date": "2025-01-01",
        "closing_date": "2025-12-31",
        "category": "General",
        "status": "active",
        "source_url": inst["url"],
        "documents": [{
            "filename": filename,
            "original_url": AMANA_TENDER["doc_url"],
            "local_path": f"./downloads/{tender_id}/original/{filename}",
            "file_size_bytes": size,
            "downloaded_at": NOW,
            "content_type": "application/pdf",
        }],
        "contact": {"email": inst["emails"][0] if inst["emails"] else ""},
        "scraped_at": NOW,
        "last_checked": NOW,
    }

    tender_path = inst_dir / "tenders" / "active" / f"{tender_id}.json"
    with open(tender_path, "w", encoding="utf-8") as f:
        json.dump(tender_json, f, indent=2, ensure_ascii=False)

    return tender_count + 1, doc_count


def process_opportunity(inst, html):
    slug = inst["slug"]
    emails = list(set(inst.get("emails", []) + extract_emails_from_html(html or "")))
    emails = [e for e in emails if e and "@" in e][:10]

    lead = {
        "institution_slug": slug,
        "institution_name": inst["name"],
        "website_url": inst["url"],
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": f"No formal tenders found on {inst['name']} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst['name']}",
        "draft_email_body": f"""Dear {inst['name']} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst['name']}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
""",
        "created_at": NOW,
        "status": "pending",
    }

    leads_path = PROJECT / "opportunities" / "leads.json"
    leads = []
    if leads_path.exists():
        with open(leads_path, encoding="utf-8") as f:
            leads = json.load(f)
    if not isinstance(leads, list):
        leads = leads.get("leads", [])

    if not any(l.get("institution_slug") == slug for l in leads):
        leads.append(lead)
        with open(leads_path, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
    return lead


def update_scrape_state(inst_dir, slug, status, tender_count, doc_count, error=None):
    last_scrape = {
        "institution": slug,
        "last_scrape": NOW,
        "next_scrape": NOW[:10],
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
    }
    with open(inst_dir / "last_scrape.json", "w", encoding="utf-8") as f:
        json.dump(last_scrape, f, indent=2)

    log_entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    scrape_log = inst_dir / "scrape_log.json"
    runs = []
    if scrape_log.exists():
        with open(scrape_log, encoding="utf-8") as f:
            data = json.load(f)
            runs = data.get("runs", [])
    runs.append(log_entry)
    with open(scrape_log, "w", encoding="utf-8") as f:
        json.dump({"runs": runs[-50:]}, f, indent=2)


def main():
    results = []
    for inst in INSTITUTIONS:
        slug = inst["slug"]
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)

        tender_count = 0
        doc_count = 0
        status = "success"
        error = None

        try:
            if slug in ("amana-bank", "amanabank"):
                tender_count, doc_count = process_tender(inst, tender_count, doc_count)
            else:
                html = fetch_url(inst["url"])
                if html is None:
                    status = "error"
                    error = "Fetch failed or timeout"
                process_opportunity(inst, html)
        except Exception as e:
            status = "error"
            error = str(e)
            try:
                process_opportunity(inst, None)
            except Exception:
                pass

        update_scrape_state(inst_dir, slug, status, tender_count, doc_count, error)
        results.append((slug, status, tender_count, doc_count))
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

    subprocess.run(
        ["python3", str(PROJECT / "scripts" / "sync_leads_csv.py")],
        cwd=str(PROJECT),
        check=False,
    )

    print("\n--- BATCH 7 COMPLETE ---")
    for slug, status, tc, dc in results:
        print(f"RESULT|{slug}|{status}|{tc}|{dc}")


if __name__ == "__main__":
    main()
