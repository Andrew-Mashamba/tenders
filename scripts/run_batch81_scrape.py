#!/usr/bin/env python3
"""Process scrape results for run_20260313_205329_batch81 - 25 institutions."""
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260313_205329_batch81"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Scrape results: slug -> (status, tender_count, doc_count, error?)
# status: success|error|no_tenders
RESULTS = {
    "nasaha": ("no_tenders", 0, 0),
    "naselecom": ("no_tenders", 0, 0),
    "nasia": ("no_tenders", 0, 0),
    "natevision": ("no_tenders", 0, 0),
    "nattydogs": ("no_tenders", 0, 0),
    "nbaa": ("error", 0, 0, "Fetch timed out"),
    "nbc": ("success", 1, 1),  # RFP Commercial Credit Origination
    "nbc-bank": ("success", 1, 1),  # Same as nbc
    "nbeconsulting": ("no_tenders", 0, 0),
    "nbreliabletechnologies": ("no_tenders", 0, 0),
    "nbts": ("error", 0, 0, "Fetch timed out"),
    "ncbagroup": ("no_tenders", 0, 0),
    "ncbct": ("no_tenders", 0, 0),
    "nchas": ("no_tenders", 0, 0),
    "ncd": ("no_tenders", 0, 0),
    "ncltz": ("no_tenders", 0, 0),
    "ncultd": ("success", 1, 0),  # Tangazo la zabuni - need to check for docs
    "ndalatc": ("no_tenders", 0, 0),
    "ndarakwai": ("no_tenders", 0, 0),
    "ndc": ("error", 0, 0, "Fetch timed out"),
    "ndegeinsurance": ("no_tenders", 0, 0),
    "ndotoinaction": ("error", 0, 0, "Fetch timed out"),
    "ndotozetu": ("no_tenders", 0, 0),
    "nduviniautoworks": ("no_tenders", 0, 0),
    "nebulahealthcare": ("no_tenders", 0, 0),
}

# Lead data for no_tenders institutions
LEAD_DATA = {
    "nasaha": ("Nasaha Consultant", "https://nasaha.co.tz/", ["hello@domain.com", "habibussi@nasaha.co.tz"]),
    "naselecom": ("Naselecom", "https://naselecom.co.tz/", ["info@naselecom.co.tz"]),
    "nasia": ("Nasia Consult Limited", "https://nasia.co.tz/", ["nasia@nasia.co.tz"]),
    "natevision": ("NateVision", "https://natevision.co.tz/", []),
    "nattydogs": ("Natty Dogs", "https://nattydogs.co.tz/", ["info@nattydogs.co.tz"]),
    "nbeconsulting": ("NBE Consulting", "https://www.nbeconsulting.co.tz/", ["director@nbeconsulting.co.tz"]),
    "nbreliabletechnologies": ("NB Reliable Technologies", "https://nbreliabletechnologies.co.tz/", ["info@nbreliabletechnologies.co.tz"]),
    "ncbagroup": ("NCBA Tanzania", "https://ncbagroup.co.tz/", ["ncbagroup@tip-offs.com"]),
    "ncbct": ("Nyaishozi College", "https://nyaishozi.info/", ["info@nyaishozicollege.ac.tz"]),
    "nchas": ("Nyaishozi College", "https://nyaishozi.info/", ["info@nyaishozicollege.ac.tz"]),
    "ncd": ("Tanzania National Commercial Directory", "https://ncd.co.tz/", ["info@ncd.co.tz"]),
    "ncltz": ("Next Couriers and Logistics", "https://nextcouriers.net/", ["info@nextcouriers.net", "sales@nextcouriers.net"]),
    "ndalatc": ("Water Institute", "https://ndalatc.ac.tz/", ["rector@waterinstitute.ac.tz"]),
    "ndarakwai": ("Ndarakwai Ranch", "https://www.ndarakwai.co.tz/", ["bookings@ndarakwai.co.tz"]),
    "ndegeinsurance": ("Ndege Insurance Brokers", "https://www.ndegeinsurance.com/", []),
    "ndotozetu": ("Ndoto Zetu", "https://ndotozetu.or.tz/", ["info@ndotozetu.or.tz"]),
    "nduviniautoworks": ("Nduvini Auto Works", "https://nduviniautoworks.co.tz/", ["nduvin@hotmail.com"]),
    "nebulahealthcare": ("Nebula Healthcare", "https://www.nebulahealthcare.co.tz/", ["info@nebulahealthcare.co.tz"]),
}


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)


def update_last_scrape(inst_dir: Path, slug: str, status: str, tender_count: int, error: str = None):
    data = {
        "institution": slug,
        "last_scrape": NOW,
        "next_scrape": "2026-03-15T06:00:00Z",
        "active_tenders_count": tender_count,
        "status": status,
        "error": error,
        "run_id": RUN_ID,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(data, f, indent=2)


def update_scrape_log(inst_dir: Path, slug: str, status: str, tender_count: int, doc_count: int, error: str = None):
    log_path = inst_dir / "scrape_log.json"
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    else:
        log = {"runs": []}
    run_entry = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "new_tenders": tender_count,
        "documents_downloaded": doc_count,
        "errors": [error] if error else [],
    }
    log["runs"].append(run_entry)
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def download_file(url: str, dest: Path) -> bool:
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["curl", "-sL", "-o", str(dest), "--connect-timeout", "30", "--max-time", "60", url],
            check=True,
            capture_output=True,
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def process_nbc():
    """Create NBC tender and download RFP PDF."""
    inst_dir = PROJECT / "institutions" / "nbc"
    ensure_dirs(inst_dir)
    tender_id = "NBC-2026-001"
    pdf_url = "https://www.nbc.co.tz/content/dam/nbc/tanzania/pdf/procurement/nbc-rfp-credit.pdf"
    download_dir = inst_dir / "downloads" / tender_id / "original"
    download_dir.mkdir(parents=True, exist_ok=True)
    dest = download_dir / "nbc-rfp-credit.pdf"
    ok = download_file(pdf_url, dest)
    tender = {
        "tender_id": tender_id,
        "institution": "nbc",
        "title": "RFP Commercial Credit Origination, Assessment & Workflow Platform",
        "description": "NBC procurement for Commercial Credit Origination platform.",
        "published_date": "",
        "closing_date": "",
        "closing_time": "",
        "category": "ICT",
        "status": "active",
        "source_url": "https://www.nbc.co.tz/en/procurement/",
        "documents": [
            {
                "filename": "nbc-rfp-credit.pdf",
                "original_url": pdf_url,
                "local_path": f"downloads/{tender_id}/original/nbc-rfp-credit.pdf",
                "downloaded_at": NOW,
            }
        ],
        "contact": {"email": "contact.centre@nbc.co.tz", "phone": "+255 76 898 4000"},
        "scraped_at": NOW,
        "last_checked": NOW,
    }
    (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(json.dumps(tender, indent=2))
    update_last_scrape(inst_dir, "nbc", "success", 1)
    update_scrape_log(inst_dir, "nbc", "success", 1, 1 if ok else 0)
    return 1, 1 if ok else 0


def process_nbc_bank():
    """NBC-bank uses same procurement page as nbc - same tender."""
    inst_dir = PROJECT / "institutions" / "nbc-bank"
    ensure_dirs(inst_dir)
    tender_id = "NBC-BANK-2026-001"
    pdf_url = "https://www.nbc.co.tz/content/dam/nbc/tanzania/pdf/procurement/nbc-rfp-credit.pdf"
    download_dir = inst_dir / "downloads" / tender_id / "original"
    download_dir.mkdir(parents=True, exist_ok=True)
    dest = download_dir / "nbc-rfp-credit.pdf"
    ok = download_file(pdf_url, dest)
    tender = {
        "tender_id": tender_id,
        "institution": "nbc-bank",
        "title": "RFP Commercial Credit Origination, Assessment & Workflow Platform",
        "description": "NBC procurement for Commercial Credit Origination platform.",
        "published_date": "",
        "closing_date": "",
        "closing_time": "",
        "category": "ICT",
        "status": "active",
        "source_url": "https://www.nbc.co.tz/en/procurement/",
        "documents": [
            {
                "filename": "nbc-rfp-credit.pdf",
                "original_url": pdf_url,
                "local_path": f"downloads/{tender_id}/original/nbc-rfp-credit.pdf",
                "downloaded_at": NOW,
            }
        ],
        "contact": {"email": "contact.centre@nbc.co.tz", "phone": "+255 76 898 4000"},
        "scraped_at": NOW,
        "last_checked": NOW,
    }
    (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(json.dumps(tender, indent=2))
    update_last_scrape(inst_dir, "nbc-bank", "success", 1)
    update_scrape_log(inst_dir, "nbc-bank", "success", 1, 1 if ok else 0)
    return 1, 1 if ok else 0


def process_ncultd():
    """NCU LTD - Tangazo la zabuni ya ujenzi."""
    inst_dir = PROJECT / "institutions" / "ncultd"
    ensure_dirs(inst_dir)
    tender_id = "NCULTD-2026-001"
    tender = {
        "tender_id": tender_id,
        "institution": "ncultd",
        "title": "Tangazo la zabuni ya ujenzi kwa wazabuni wote wenye sifa",
        "description": "Chama Kikuu cha Ushirika Nyanza (1984) Ltd kinawatangazia zabuni ya ujenzi.",
        "published_date": "",
        "closing_date": "",
        "closing_time": "",
        "category": "Construction",
        "status": "active",
        "source_url": "https://website.ncultd.or.tz/",
        "documents": [],
        "contact": {"email": "info@ncultd.or.tz", "phone": "0282500676"},
        "scraped_at": NOW,
        "last_checked": NOW,
    }
    (inst_dir / "tenders" / "active" / f"{tender_id}.json").write_text(json.dumps(tender, indent=2))
    update_last_scrape(inst_dir, "ncultd", "success", 1)
    update_scrape_log(inst_dir, "ncultd", "success", 1, 0)
    return 1, 0


def append_lead(slug: str, name: str, url: str, emails: list):
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
    return {
        "institution_slug": slug,
        "institution_name": name,
        "website_url": url,
        "emails": emails,
        "opportunity_type": "sell",
        "opportunity_description": "No formal tenders found. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
        "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {name}",
        "draft_email_body": body,
        "created_at": NOW,
        "status": "pending",
    }


def main():
    leads_to_append = []
    for slug, r in RESULTS.items():
        inst_dir = PROJECT / "institutions" / slug
        inst_dir.mkdir(parents=True, exist_ok=True)
        if len(r) == 4:
            status, tc, dc, err = r
        else:
            status, tc, dc = r
            err = None
        if status == "success":
            if slug == "nbc":
                tc, dc = process_nbc()
            elif slug == "nbc-bank":
                tc, dc = process_nbc_bank()
            elif slug == "ncultd":
                tc, dc = process_ncultd()
        elif status == "no_tenders":
            if slug in LEAD_DATA:
                name, url, emails = LEAD_DATA[slug]
                leads_to_append.append(append_lead(slug, name, url, emails))
            update_last_scrape(inst_dir, slug, "success", 0)
            update_scrape_log(inst_dir, slug, "success", 0, 0)
        else:
            update_last_scrape(inst_dir, slug, "error", 0, err)
            update_scrape_log(inst_dir, slug, "error", 0, 0, err)
        # Print result line
        s = status if status != "no_tenders" else "no_tenders"
        print(f"RESULT|{slug}|{s}|{tc}|{dc}")
    if leads_to_append:
        leads_path = PROJECT / "opportunities" / "leads.json"
        with open(leads_path) as f:
            leads = json.load(f)
        if not isinstance(leads, list):
            leads = leads.get("leads", [])
        leads.extend(leads_to_append)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2)
        subprocess.run(["/usr/bin/env", "python3", str(PROJECT / "scripts" / "sync_leads_csv.py")], check=True)


if __name__ == "__main__":
    main()
