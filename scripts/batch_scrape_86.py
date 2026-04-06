#!/usr/bin/env python3
"""Process scrape results for run_20260315_060430_batch86 - 25 institutions."""
import json
import os
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Volumes/DATA/PROJECTS/TENDERS")
RUN_ID = "run_20260315_060430_batch86"
NOW = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# Scrape results: (slug, status, tender_count, doc_count, error?)
RESULTS = [
    ("nps", "error", 0, 0, "Fetch timeout"),
    ("nrap", "error", 0, 0, "Account suspended"),
    ("nsamboshop", "success", 0, 0, None),  # E-commerce, no tenders
    ("nsconsulting", "success", 0, 0, None),  # Agribusiness consulting
    ("nshishiattorneys", "success", 0, 0, None),  # Law firm
    ("nssf", "error", 0, 0, "Fetch timeout"),
    ("ntdcp", "error", 0, 0, "Fetch timeout"),
    ("ntech", "success", 0, 0, None),  # ICT company
    ("ntlp", "success", 0, 0, None),  # TB/Leprosy program - news only
    ("nts", "success", 0, 0, None),  # Hardware distributor
    ("ntuli", "success", 0, 0, None),  # Lab supplies
    ("nukta", "success", 0, 0, None),  # News site
    ("nuktaafrica", "error", 0, 0, "Fetch timeout"),
    ("numaes", "success", 0, 0, None),  # Logistics
    ("nwf", "success", 0, 0, None),  # Publications only, no tenders
    ("nyaishozicollege", "success", 0, 0, None),  # College
    ("nyamweziteachers", "success", 0, 0, None),  # College - application forms
    ("nyanzamines", "success", 0, 0, None),  # Salt producer
    ("nyaraka", "error", 0, 0, "Fetch timeout"),
    ("nyasadc", "success", 0, 0, None),  # Announcements, no tender docs
    ("nyotarays", "success", 0, 0, None),  # Media company
    ("nypplus", "success", 0, 0, None),  # NGO
    ("nzegatc", "success", 0, 0, None),  # 2 closed tenders from 2017
    ("oasisgroup", "success", 0, 0, None),  # Tax/financial services
    ("obp-tanzania", "success", 0, 0, None),  # Procurement consultancy
]


def ensure_dirs(inst_dir: Path):
    (inst_dir / "tenders" / "active").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "closed").mkdir(parents=True, exist_ok=True)
    (inst_dir / "tenders" / "archive").mkdir(parents=True, exist_ok=True)
    (inst_dir / "downloads").mkdir(parents=True, exist_ok=True)


def update_last_scrape(inst_dir: Path, slug: str, status: str, tender_count: int, err: str):
    data = {
        "institution": slug,
        "last_scrape": NOW,
        "active_tenders_count": tender_count,
        "status": status,
        "error": err,
    }
    with open(inst_dir / "last_scrape.json", "w") as f:
        json.dump(data, f, indent=2)


def append_scrape_log(inst_dir: Path, slug: str, status: str, tender_count: int, doc_count: int, err: str):
    log_path = inst_dir / "scrape_log.json"
    if log_path.exists():
        with open(log_path) as f:
            log = json.load(f)
    else:
        log = {"runs": []}
    run = {
        "run_id": RUN_ID,
        "timestamp": NOW,
        "duration_seconds": 0,
        "status": status,
        "tenders_found": tender_count,
        "new_tenders": 0,
        "updated_tenders": 0,
        "documents_downloaded": doc_count,
        "errors": [err] if err else [],
    }
    log["runs"].append(run)
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def main():
    inst_names = {
        "nps": "NPS | OFISI YA TAIFA YA MASHTAKA",
        "nrap": "Account Suspended",
        "nsamboshop": "Nsambo Shop",
        "nsconsulting": "NS Consulting",
        "nshishiattorneys": "Nshishi Attorneys & Tax Consultants",
        "nssf": "NSSF",
        "ntdcp": "NTDCP",
        "ntech": "NTECH",
        "ntlp": "National Tuberculosis & Leprosy Programme",
        "nts": "New Tahery Stores",
        "ntuli": "Ntuli Tanzania",
        "nukta": "Nukta Habari",
        "nuktaafrica": "Nukta Africa",
        "numaes": "NUMAES",
        "nwf": "Nation Water Fund",
        "nyaishozicollege": "Nyaishozi College",
        "nyamweziteachers": "Nyamwezi Teachers College",
        "nyanzamines": "Nyanza Mines",
        "nyaraka": "Nyaraka",
        "nyasadc": "Nyasa District Council",
        "nyotarays": "Nyota Rays",
        "nypplus": "NYPPLUS",
        "nzegatc": "Nzega Town Council",
        "oasisgroup": "Oasis Group",
        "obp-tanzania": "Ocean Business Partners",
    }
    urls = {
        "nps": "https://nps.go.tz/",
        "nrap": "https://nrap.co.tz/",
        "nsamboshop": "https://nsamboshop.co.tz/",
        "nsconsulting": "https://nsconsulting.co.tz/",
        "nshishiattorneys": "https://nshishiattorneys.co.tz/",
        "nssf": "https://nssf.go.tz/",
        "ntdcp": "https://ntdcp.go.tz/",
        "ntech": "https://ntech.co.tz/",
        "ntlp": "https://ntlp.go.tz/",
        "nts": "https://nts.co.tz/",
        "ntuli": "http://ntuli.co.tz/",
        "nukta": "https://nukta.co.tz/",
        "nuktaafrica": "https://nuktaafrica.co.tz/",
        "numaes": "https://numaes.co.tz/",
        "nwf": "https://www.nwf.go.tz/",
        "nyaishozicollege": "https://nyaishozi.info/",
        "nyamweziteachers": "https://nyamweziteachers.ac.tz/",
        "nyanzamines": "https://nyanzamines.co.tz/",
        "nyaraka": "https://nyaraka.go.tz/",
        "nyasadc": "https://nyasadc.go.tz/manunuzi-na-ugavi",
        "nyotarays": "https://nyotarays.co.tz/",
        "nypplus": "https://nypplus.or.tz/",
        "nzegatc": "https://nzegatc.go.tz/tenders",
        "oasisgroup": "https://oasisgroup.co.tz/",
        "obp-tanzania": "https://obp-tanzania.co.tz/ourservices.html#procurement",
    }
    emails = {
        "nsamboshop": ["info@nsamboshop.co.tz"],
        "nsconsulting": ["nuhu@nsconsulting.co.tz", "info@nsconsulting.co.tz"],
        "nshishiattorneys": ["info@nshishiattorneys.co.tz"],
        "ntech": ["info@ntech.co.tz"],
        "ntlp": ["info@ntlp.go.tz"],
        "nts": [],
        "ntuli": [],
        "nukta": ["newsroom@nukta.co.tz"],
        "numaes": ["info@numaes.co.tz"],
        "nwf": ["info@nwf.go.tz"],
        "nyaishozicollege": ["info@nyaishozicollege.ac.tz"],
        "nyamweziteachers": ["nyamweziteachers@yahoo.com"],
        "nyanzamines": ["info@nyanzamines.co.tz"],
        "nyasadc": ["ps.ded@nyasadc.go.tz"],
        "nyotarays": [],
        "nypplus": ["info@nypplus.or.tz"],
        "nzegatc": ["td@nzegatc.go.tz"],
        "oasisgroup": ["taxadvise@oasisgroup.co.tz", "marketing@oasisgroup.co.tz"],
        "obp-tanzania": ["info@obp-tanzania.co.tz"],
    }

    leads_to_append = []
    for slug, status, tender_count, doc_count, err in RESULTS:
        inst_dir = PROJECT / "institutions" / slug
        ensure_dirs(inst_dir)
        update_last_scrape(inst_dir, slug, status, tender_count, err)
        append_scrape_log(inst_dir, slug, status, tender_count, doc_count, err)
        print(f"RESULT|{slug}|{status}|{tender_count}|{doc_count}")

        if err or tender_count > 0:
            continue
        if slug in ("nrap", "nps", "nssf", "ntdcp", "nyaraka", "nuktaafrica"):
            continue
        inst_name = inst_names.get(slug, slug)
        url = urls.get(slug, "")
        ems = emails.get(slug, [])
        if not ems and url:
            ems = ["info@" + url.split("@")[-1] if "@" in url else ""]
        if not ems:
            ems = []
        leads_to_append.append({
            "institution_slug": slug,
            "institution_name": inst_name,
            "website_url": url,
            "emails": [e for e in ems if e],
            "opportunity_type": "sell",
            "opportunity_description": f"No formal tenders found on {inst_name} website. ZIMA Solutions could offer digital transformation, fintech integrations, or ICT services.",
            "draft_email_subject": f"Partnership Opportunity – ZIMA Solutions & {inst_name}",
            "draft_email_body": f"""Dear {inst_name} Team,

ZIMA Solutions Limited specialises in digital transformation for financial institutions and enterprises in Tanzania. We noticed your organisation and believe we could support your technology and innovation goals.

Our offerings include:
• GePG, TIPS, and RTGS integrations
• SACCO and microfinance systems
• AI-powered customer engagement
• HR, school, and healthcare management systems

We would welcome a conversation about how we might support {inst_name}. Could we schedule a brief call?

Best regards,
ZIMA Solutions Limited
info@zima.co.tz | +255 69 241 0353
""",
            "created_at": NOW,
            "status": "pending",
        })

    if leads_to_append:
        leads_path = PROJECT / "opportunities" / "leads.json"
        with open(leads_path) as f:
            leads = json.load(f)
        existing = {l.get("institution_slug") for l in leads}
        new_leads = [l for l in leads_to_append if l["institution_slug"] not in existing]
        leads.extend(new_leads)
        with open(leads_path, "w") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        print(f"\nAppended {len(new_leads)} new leads (skipped {len(leads_to_append) - len(new_leads)} duplicates)")


if __name__ == "__main__":
    main()
